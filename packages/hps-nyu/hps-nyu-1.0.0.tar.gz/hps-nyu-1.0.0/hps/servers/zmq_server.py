"""
A ZeroMQ based server for games like Auction where mass communication
is required
"""
import atexit
from datetime import datetime
import uuid

import zmq

from .base import BaseServer


class ZmqServer(BaseServer):
    """A ZeroMQ based server for sending and receiving messages from
    multiple clients in an async manner

    This server allows one-to-many sends and one-to-one receives with
    the clients. All messages are sent to all clients and every receive
    from a client requires a response. This is suitable for games
    like Auction where the clients will send and receive messages
    simultaneously.

    The server uses two sockets, a PUSH socket and a REPLY socket
    from the ZeroMQ socket types. The PUSH socket is responsible
    for sending out the messages to the clients. It will send the message
    to all clients connected to it, via their PULL socket.

    The client can send a request to the server using its REQUEST socket,
    which will be received by the REPLY socket of the server. The server
    will send ``'200 ' + data`` as a reponse if it can reply immediately,
    '202' if it cannot reply immediately and 400 if the client is unknown.

    To establish connections to the server, the clients must send a
    request with the client's id and the server will provide a UUID as
    a response. All future requests for the client must include the
    UUID as a key if sending as JSON, or should be the first item in
    a space separated string otherwise.
    """

    def __init__(self, host, send_port, recv_port, num_clients):
        """
        Args:
            :host:
                The host name of the server
            :server_send_port:
                The port from which the server sends data. This will
                be the port on which the client receives data.
            :server_recv_port:
                The port on which the server receives data. This will
                be the port to which the client will send data.
            :num_clients:
                The number of clients that the server will communicate
                with
        """
        self.context = zmq.Context(io_threads=num_clients)
        self.push_sck = self.context.socket(zmq.PUSH)
        self.push_sck.bind('tcp://%s:%d' % (host, send_port))
        self.rep_sck = self.context.socket(zmq.REP)
        self.rep_sck.bind('tcp://%s:%d' % (host, recv_port))
        self.client_ids = {}
        self.__client_caches = {}
        self.num_clients = num_clients
        atexit.register(self.close)

    def __del__(self):
        self.close()

    def close(self):
        """Close the connections"""
        self.push_sck.close()
        self.rep_sck.close()
        self.context.destroy()

    def establish_client_connections(self):
        """Establish connections with the clients

        This method recieves an id from each client and responds with
        a UUID for the client.
        """
        i = self.num_clients
        while i > 0:
            client_id = self.rep_sck.recv_string()
            if client_id.split(' ')[0] in self.client_ids.values():
                self.rep_sck.send_string('202', flags=zmq.NOBLOCK)
                continue
            if not client_id:
                raise ValueError('Client id %s is invalid' % str(client_id))
            self.client_ids[client_id] = uuid.uuid4().hex
            self.__client_caches[client_id] = {'rep': [], 'req': []}
            self.rep_sck.send_string('%s' % self.client_ids[client_id], flags=zmq.NOBLOCK)
            i -= 1

    def send_to(self, data, client_idx, **kwargs):
        """Send data to a particular client

        This method will keep receiving requests until a request from the
        particular client is received. For all other requests, it will
        reply with ``'202'`` (HTTP status code for Accepted). For the given
        client, it will reply with ``'200 %s' % data``. Clients should
        keep requesting until they receive a message starting with 200.

        Args:
            :data (str): The data to send to the client
            :client_idx: The key of the client in ``self.client_ids``
            :**kwargs: Any kwargs to pass to the send_string method
                of zmq socket

        Return:
            The request received from the client
        """
        if client_idx not in self.client_ids:
            raise ValueError('Unknown client_idx')

        while True:
            req = self.rep_sck.recv_string().split(' ')
            req_uuid = req[0]
            req_client_idx = [k for k, v in self.client_ids.items() if v == req_uuid][0]
            if req_client_idx == client_idx:
                self.rep_sck.send_string('200 {0}'.format(data).rstrip(' '), **kwargs)
                return ' '.join(req[1:])
            if req_client_idx in self.client_ids:
                self.rep_sck.send_string('202', **kwargs)
            else:
                self.rep_sck.send_string('400', **kwargs)

    def send_to_all(self, data, **kwargs):
        """Send data to all clients

        Args:
            :data (str): The data to send to the client
            :**kwargs: kwargs accepted by the ZeroMQ socket
                ``send_string`` method
        """
        for _ in range(0, self.num_clients):
            self.push_sck.send_string(data, flags=zmq.NOBLOCK, **kwargs)

    def send_file(self, file_name, client_idx=None):
        """Send a file to one or all clients

        If ``client_idx`` is None, the contents of the file are sent to
        all clients, otherwise they are sent to specified client. When
        sending to a particular client, the ``send_to`` method is used
        and the same constraints on responses apply.

        Args:
            :file_name: The name of the file to send
            :client_idx: The key of the client in ``self.client_ids``
        """
        with open(file_name, 'r') as filp:
            if client_idx is None:
                self.send_to_all(filp.read())
            else:
                self.send_to(filp.read(), client_idx)

    def receive_from_all(self, size=4096, **kwargs):
        """Receive a message from all clients

        Note:
            There is no need to run this asynchronously. ZeroMQ will
            always return messages in the order they arrived.

            Also, this method will block clients until all messages
            have been received to prevent receiving message from same
            client twice.

        Args:
            :**kwargs:
                kwargs accepted by the ZeroMQ socket ``recv_string`` method

        Return:
            A list of dicts containing the data received, the time
            it was received and the client id it was received from
            if it was sent with a valid uuid. The keys are ``time``,
            ``data`` and ``client_id``.
        """
        msgs = []
        for _ in range(0, self.num_clients):
            data = self.rep_sck.recv_string(**kwargs).split(' ')
            client_uuid = data[0]

            if client_uuid not in self.client_ids.values():
                self.rep_sck.send_string('400')
                continue

            msgs.append({'time': datetime.now(),
                         'uuid': client_uuid,
                         'data': ' '.join(data[1:])})
            self.rep_sck.send_string('200')

        for msg in msgs:
            msg['client_id'] = [k for k, v in self.client_ids.items() if v == msg['uuid']][0]
            msg.pop('uuid')

        return msgs

    def receive_from(self, client_idx, size=4096, **kwargs):
        """Receive data from a particular client

        This method will keep receiving requests until a request from the
        particular client is received. For all other requests, it will
        reply with ``'202'`` (HTTP status code for Accepted). For the given
        client, it will reply with ``'200'``. Clients should keep requesting
        until they receive a message starting with 200.

        Args:
            :client_idx: The key of the client in ``self.client_ids``
            :size: This is ignored and is only provided to maintain
                consistency with the signature of the base class
            :**kwargs: Any kwargs to pass to the send_string method
                of zmq socket

        Return:
            The request received from the client
        """
        return self.send_to('', client_idx, **kwargs)

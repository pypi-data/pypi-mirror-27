"""
A ZeroMQ based client for the ``hps.servers.ZmqServer`` class
"""
import atexit

import zmq


class ZmqClient(object):
    """Client class for the ZmqServer in the hps package"""

    def __init__(self, host, server_send_port, server_recv_port,
                 client_id):
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
            :client_id: An identifier for the client, which has to be
                unique for all clients connected to a single server.
                This should be a string
        """
        self.context = zmq.Context()
        self.pull_sck = self.context.socket(zmq.PULL)
        self.pull_sck.connect('tcp://%s:%d' % (host, server_send_port))
        self.req_sck = self.context.socket(zmq.REQ)
        self.req_sck.connect('tcp://%s:%d' % (host, server_recv_port))
        self.req_sck.send_string(client_id)
        self.token = self.req_sck.recv_string()
        atexit.register(self.close)

    def __del__(self):
        self.close()

    def close(self):
        """Close the connections"""
        self.pull_sck.close()
        self.req_sck.close()
        self.context.destroy()

    def receive_data(self, **kwargs):
        """Receive a message from the server

        Args:
            :**kwargs:
                kwargs accepted by the ZeroMQ socket ``recv_string`` method

        Return:
            The message received from the server as string
        """
        return self.pull_sck.recv_string(**kwargs)

    def send_data(self, data, **kwargs):
        """Send data to the server

        The client will send the data to server until it gets a 200
        response from the server. If the server does not respond
        with a 202 or 200 status, an error is raised.

        Args:
            :data (str):
                The data to send to the server
            :**kwargs:
                kwargs accepted by the ZeroMQ socket ``send_string`` method

        Return:
            The reply send from the server as string
        """
        resp = ['202']
        while resp[0] != '200':
            self.req_sck.send_string('%s %s' % (self.token, data), **kwargs)
            resp = self.req_sck.recv_string().split(' ')
            if resp[0] not in ('200', '202'):
                raise ValueError('Expected 200 or 202 response. '
                                 + 'Server responded with %s.' % resp)
        return ' '.join(resp[1:])

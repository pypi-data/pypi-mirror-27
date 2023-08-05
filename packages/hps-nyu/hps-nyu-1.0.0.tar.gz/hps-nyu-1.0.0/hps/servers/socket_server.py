"""
A socket based for server for use in games where the communication is
mostly one to one and can be blocking
"""
import atexit
import socket

from .base import BaseServer


class SocketServer(BaseServer):
    """A socket based server class that is good for one to one
    and blocking communications
    """

    def __init__(self, host, port, num_clients):
        """
        Args:
            :host: The hostname or IP address on which the server
                should run
            :port: The port on which the server should listen
            :num_clients: The number of clients the server will connect
                to
        """
        self.sck = socket.socket()
        self.sck.setblocking(True)
        self.sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sck.bind((host, port))
        self.client_sockets = [None] * num_clients
        atexit.register(self.close)

    def __del__(self):
        self.close()

    def close(self):
        """Close connections to all clients"""
        self.sck.close()

    @staticmethod
    def __send_data(data):
        """Normalize data before sending

        Args:
            :data: The data to be sent

        Return:
            A ``bytes`` or ``bytearray`` instance of the data
            that can be sent over socket
        """
        return data if isinstance(data, (bytes, bytearray)) else data.encode('utf-8')

    @staticmethod
    def __return_data(data, as_bytes):
        """Normalize data after receiving

        Args:
            :data: The ``byte`` or ``bytearray`` received from
                the client
            :as_bytes: If ``True``, the raw bytes are returned

        Return:
            The data received from server after transforming as
            specified
        """
        return data if as_bytes else data.decode('utf-8')

    def establish_client_connections(self):
        """Accept connections from client

        This method will accept exactly the same number of clients
        as specified in the constructor. It will block until all
        clients have connected.

        The client sockets are available in the ``client_sockets``
        attribute, which is a list in the order in which the
        connections were accepted. The list can be mutated to
        change the order.
        """
        self.sck.listen(len(self.client_sockets))
        for i in range(0, len(self.client_sockets)):
            self.client_sockets[i] = self.sck.accept()[0]

    def send_to(self, data, client_idx):
        """Send data to a specific client

        Args:
            :data: The data to send either as a ``str`` or
                as a JSON serializable object
            :client_idx: The index of the receiving client's socket in
                ``self.client_sockets``
        """
        self.client_sockets[client_idx].sendall(self.__send_data(data))

    def send_to_all(self, data):
        """Send data to all clients

        Args:
            :data: The data to send either as a ``str`` or
                as a JSON serializable object
        """
        _data = self.__send_data(data)
        for sck in self.client_sockets:
            sck.sendall(_data)

    def send_file(self, file_name, client_idx=None):
        """Send data from a file to a specific or all client

        This is a high performance method and should be preferred
        when sending data from a file. It can also be used to send
        large data efficiently.

        Args:
            :data: The data to send either as a ``str`` or
                as a JSON serializable object
            :client_idx: The index of the receiving client's socket in
                ``self.client_sockets`` or ``None`` to send to all
                clients.
        """
        with open(file_name, 'rb') as filp:
            if client_idx is None:
                for sck in self.client_sockets:
                    sck.sendfile(filp)
            else:
                self.client_sockets[client_idx].sendfile(filp)

    def receive_from(self, client_idx, size=4096, as_bytes=False):
        """Receive data from a specific client

        Args:
            :client_idx: The index of the sending client's socket in
                ``self.client_sockets``
            :size: The size of data to receive. Default is 4096.
            :as_bytes: If ``True``, the raw bytes are returned

        Return:
            The data received from the client
        """
        return self.__return_data(self.client_sockets[client_idx].recv(size), as_bytes)

    def receive_from_until(self, client_idx, condition, size=4096, as_bytes=False):
        """Receive data from a specific client until a condition is statisfied

        This method recieves data from the client and checks whether a condition
        is satisfied or not. It returns after the condition is satisfied.

        Args:
            :client_idx: The index of the sending client's socket in
                ``self.client_sockets``
            :condition: A callable which takes 1 argument, the data
                received so far as a bytearray, and returns a
                Boolean
            :size: The size of data to receive. Default is 4096.
            :as_bytes: If ``True``, the raw bytes are returned

        Return:
            The data received from the client
        """
        _data = bytearray()
        while not condition(_data):
            _data.extend(self.receive_from(client_idx, size=size, as_bytes=True))
        return self.__return_data(_data, as_bytes)

    def receive_from_all(self, size=4096, as_bytes=False):
        """Receive data from all clients

        Args:
            :size: The size of data to receive. Default is 4096.
            :as_bytes: If ``True``, the raw bytes are returned

        Return:
            A list of the data received from the clients
        """
        data = []
        for i in range(0, len(self.client_sockets)):
            data.append(self.receive_from(i, size, as_bytes=as_bytes))
        return data

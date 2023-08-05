"""
A socket based client for the ``hps.servers.SocketServer`` class
"""

import atexit
import socket


class SocketClient(object):
    """A client class for ``hps.servers.SocketServer``"""

    def __init__(self, host, port):
        """
        Args:
            :host: The hostname of the server
            :port: The port of the server
        """
        self.sck = socket.socket()
        self.sck.setblocking(True)
        self.sck.connect((host, port))
        atexit.register(self.close)

    def __del__(self):
        self.close()

    def close(self):
        """Close the connection"""
        self.sck.close()

    @staticmethod
    def __send_data(data):
        """Normalize data before sending to the server

        Args:
            :data: The data to send. This is either a ``str``,
                ``bytes``, ``bytearray`` or a JSON-serializable
                object.
        """
        return data if isinstance(data, (bytes, bytearray)) else data.encode('utf-8')

    @staticmethod
    def __return_data(data, as_bytes):
        """Normalize the data before returning to user

        Args:
            :data: The data received from the server
            :as_bytes: If ``True, return data as raw bytes

        Return:
            The data after normalizing
        """
        return data.decode('utf-8') if not as_bytes else data

    def send_data(self, data):
        """Send data to the server

        Args:
            :data: The data to send to the server. It can be a
                ``str``, ``bytes`` or ``bytearray`` object
        """
        self.sck.sendall(self.__send_data(data))

    def send_file(self, file_name):
        """Send the contents of file to the server

        This uses the high-performance ``os.sendfile`` on POSIX
        systems. This should be used to send large data.

        Args:
            :file_name: The name of the file to send
        """
        with open(file_name, 'rb') as filp:
            self.sck.sendfile(filp)

    def receive_data(self, size=4096, as_bytes=False):
        """Receive data from the server

        Args:
            :size: The size of data to receive. Default is 4096
            :as_bytes: If ``True``, raw bytes are returned instead
                of ``str``

        Return:
            The data received from server. Default type is ``str``
            but that can be changed using the arguments.
        """
        return self.__return_data(self.sck.recv(size), as_bytes)

    def receive_large(self, chunk_size=8092, timeout=1.0, as_bytes=False):
        """Receive a large piece of data from the server

        This method fetches chunks of data from the server until the
        socket times out. So, timeout must be set to a resaonable amount
        to avoid waiting too long.

        Args:
            :chunk_size: The chunk size to receive. Default is 8092.
            :timeout: The time after which data revceived should be
                considered complete.
            :as_bytes: If ``True, raw bytes of the data are returned

        Return:
            The data received from the server.
        """
        if not (isinstance(timeout, float) and not timeout):
            raise ValueError('timeout must be a non-zero floating point number')
        _data = bytearray()
        self.sck.settimeout(timeout)
        while True:
            try:
                _data.append(self.receive(size=chunk_size, as_bytes=True))
            except socket.timeout:
                break
        self.sck.setblocking(True)
        return self.__return_data(_data, as_bytes)

    def receive_until(self, condition, size=4096, as_bytes=False):
        """Receive data from the server until a condition is satisfied

        This method receives data and checks whether the received data
        satisfies the condition. Until then, it will keep receiving
        data from the server.

        Args:
            :condition: A callable that takes once argument, the
                data received so far as bytearray and returns a boolean
            :size: The size for each individual receive. Default is
                4096
            :as_bytes: If ``True``, rae bytes of the data are returned

        Return:
            The data received from the server
        """
        _data = bytearray()
        while not condition(_data):
            _data.extend(self.receive(size=size, as_bytes=True))
        return self.__return_data(_data, as_bytes)

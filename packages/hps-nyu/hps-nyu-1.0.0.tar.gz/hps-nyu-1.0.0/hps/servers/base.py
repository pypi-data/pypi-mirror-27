"""
This file contains the base class to inherit from when implementing
a new server class.
"""

class BaseServer(object):
    """A base class from which implementations can inherit.

    All methods will raise ``NotImplementedError`` if not overridden
    by the implementations
    """

    def close(self):
        """Cleanup function

        Most implementations will need to override this. It should also
        be registered as an atexit handler in the __init__ function
        """
        raise NotImplementedError

    def establish_client_connections(self):
        """Method that will initialize the connection with the clients"""
        raise NotImplementedError

    def send_to(self, data, client_idx):
        """Method to send data to one established client

        Args:
            :data:
                The data to send to the client
            :client_idx:
                The identifier for the client. This will depend on the
                implementation
        """
        raise NotImplementedError

    def send_to_all(self, data):
        """Method to send data to all established client

        Args:
            :data:
                The data to send to the client
        """
        raise NotImplementedError

    def send_file(self, file_name, client_idx=None):
        """Method to send a file to one or all clients

        Args:
            :data:
                The data to send to the client
            :client_idx:
                The identifier for the client. This will depend on the
                implementation. If ``None``, the file will be sent to
                all clients
        """
        raise NotImplementedError

    def receive_from(self, client_idx, size=4096):
        """Receive data from an established client

        Args:
            :client_idx:
                The identifier for the client. This will depend on the
                implementation
            :size int:
                The size of data to receive. Default is 4096.
        """
        raise NotImplementedError

    def receive_from_until(self, client_idx, condition, size=4096):
        """Receive data from an established client until a condition is met

        Args:
            :client_idx:
                The identifier for the client. This will depend on the
                implementation
            :condition:
                A callable that returns a truthy value when a condition
                is met. The callable must take a single argument, which
                is the data received so far.
            :size int:
                The size of data to receive in a single step. Default is
                4096.
        """
        raise NotImplementedError

    def receive_from_all(self, size=4096):
        """Receive data from all clients

        Args:
            :size int:
                The size of data to receive. Default is 4096.
        """
        raise NotImplementedError

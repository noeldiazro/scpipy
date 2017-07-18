from abc import ABCMeta, abstractmethod
from socket import socket

class Link(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def read(self, number_of_bytes):
        pass

    @abstractmethod
    def write(self, message):
        pass

    
class TcpIpAddress(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port


class TcpIpLink(Link):
    def __init__(self, address, timeout=None, alt_socket=None):
        self.address = address
        self.timeout = timeout
        self._socket = alt_socket or socket()

        if timeout is not None:
            self._socket.settimeout(timeout)
        
    def open(self):
        self._socket.connect((self.address.host, self.address.port))

    def close(self):
        self._socket.close()

    def read(self, number_of_bytes):
        return self._socket.recv(number_of_bytes)

    def write(self, request):
        return self._socket.send(request)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

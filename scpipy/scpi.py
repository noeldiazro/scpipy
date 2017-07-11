from enum import Enum
from scpipy.links import TcpIpAddress, TcpIpLink

class State(Enum):
    LOW = '0'
    HIGH = '1'


class Direction(Enum):
    INPUT = 'IN'
    OUTPUT = 'OUTPUT'


class ScpiConnection(object):
    delimiter = '\r\n'
    
    def __init__(self, link):
        self._link = link

    def open(self):
        self._link.open()

    def close(self):
        self._link.close()

    def write(self, message):
        return self._link.write(message + self.delimiter) - len(self.delimiter)

    def read(self, number_of_bytes=4096):
        message = ''
        while True:
            chunk = self._link.read(number_of_bytes).replace('ERR!', '')
            message += chunk
            if message.endswith(self.delimiter):
                break
        return message.rstrip(self.delimiter)


class ScpiSession(object):
    
    def __init__(self, connection):
        self._connection = connection

    def open(self):
        self._connection.open()

    def close(self):
        self._connection.close()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def set_digital_output_state(self, pin, state):
        message = 'DIG:PIN {},{}'.format(pin, state.value)
        self._connection.write(message)

    def set_digital_direction(self, pin, direction):
        message = 'DIG:PIN DIR {},{}'.format(direction.value, pin)
        self._connection.write(message)

    def get_digital_state(self, pin):
        request = 'DIG:PIN? {}'.format(pin)
        self._connection.write(request)
        return State(self._connection.read())


class ScpiSessionFactory(object):
    def get_scpi_session(self, host, port=5000, timeout=None, alt_socket=None):
        link = TcpIpLink(TcpIpAddress(host, port))
        connection = ScpiConnection(link)
        return ScpiSession(connection)


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


class ScpiController(object):
    
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

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

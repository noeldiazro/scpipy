from unittest import TestCase
from scpipy.links import TcpIpLink, TcpIpAddress

class TcpIpLinkTest(TestCase):
    host = 'rp-f0060c.local'
    port = 5000
    timeout = 1
    
    def setUp(self):
        self.link = TcpIpLink(TcpIpAddress(self.host, self.port), self.timeout, alt_socket=TestSocket('abcde'))
        self.link.open()
        
    def test_create_ethernet_link(self):
        self.assertEqual(self.host, self.link.address.host)
        self.assertEqual(self.port, self.link.address.port)
        self.assertEqual(self.timeout, self.link.timeout)    

    def test_read_ethernet_link(self):
        self.link.open()
        response = self.link.read(4096)
        self.assertEqual('abcde', response)

    def test_write_ethernet_link(self):
        number_of_bytes = self.link.write(request='12345')
        self.assertEqual(5, number_of_bytes)
        
    def tearDown(self):
        self.link.close()
        

class TestSocket(object):
    def __init__(self, buffer=''):
        self._buffer = buffer
    
    def settimeout(self, timeout):
        pass

    def connect(self, address):
        pass

    def close(self):
        pass

    def recv(self, number_of_bytes):
        return self._buffer

    def send(self, request):
        self._buffer = request
        return len(request)
    

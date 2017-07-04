from unittest import TestCase
from mock import Mock
from scpipy import ScpiConnection, ScpiController
from scpipy.links import TcpIpLink

class ScpiConnectionTest(TestCase):
    def test_create_scpi_connection(self):
        test_link = Mock(TcpIpLink)
        connection = ScpiConnection(test_link)

    def test_open_scpi_connection(self):
        test_link = Mock(TcpIpLink)
        connection = ScpiConnection(test_link)
        connection.open()

    def test_close_spi_connection(self):
        test_link = Mock(TcpIpLink)
        connection = ScpiConnection(test_link)
        connection.close()

    def test_write_spi_connection(self):
        message = 'DIG:PIN LED0,1'
        test_link = Mock(TcpIpLink)
        test_link.write.return_value = len(message) + 2
        connection = ScpiConnection(test_link)

        number_of_bytes = connection.write(message)

        self.assertEqual(len(message), number_of_bytes)

class ScpiControllerTest(TestCase):
    def test_create_scpi_controller(self):
        test_connection = Mock(ScpiConnection)
        controller = ScpiController(test_connection)

    def test_open_close_scpi_controller(self):
        test_connection = Mock(ScpiConnection)
        controller = ScpiController(test_connection)
        controller.open()
        controller.close()


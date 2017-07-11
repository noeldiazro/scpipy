from unittest import TestCase
from mock import Mock
from scpipy import ScpiConnection, ScpiSession, State, Direction
from scpipy.links import TcpIpLink

class ScpiConnectionTest(TestCase):
    def test_create_scpi_connection(self):
        test_link = Mock(TcpIpLink)
        connection = ScpiConnection(test_link)

    def test_open_scpi_connection(self):
        test_link = Mock(TcpIpLink)
        connection = ScpiConnection(test_link)
        connection.open()

    def test_close_scpi_connection(self):
        test_link = Mock(TcpIpLink)
        connection = ScpiConnection(test_link)
        connection.close()

    def test_write_scpi_connection(self):
        message = 'DIG:PIN LED0,1'
        test_link = Mock(TcpIpLink)
        test_link.write.return_value = len(message) + 2
        connection = ScpiConnection(test_link)

        number_of_bytes = connection.write(message)

        self.assertEqual(len(message), number_of_bytes)

    def test_read_text(self):
        test_link = Mock(TcpIpLink)
        test_link.read.return_value = 'ABCDEFG\r\n'
        connection = ScpiConnection(test_link)

        message = connection.read()
        self.assertEqual('ABCDEFG', message)


class ScpiSessionTest(TestCase):
    def test_create_scpi_session(self):
        test_connection = Mock(ScpiConnection)
        session = ScpiSession(test_connection)

    def test_open_close_scpi_session(self):
        test_connection = Mock(ScpiConnection)
        session = ScpiSession(test_connection)
        session.open()
        session.close()

    def test_set_digital_output_state(self):
        test_connection = Mock(ScpiConnection)
        with ScpiSession(test_connection) as session:
            session.set_digital_output_state('LED0', State.HIGH)

    def test_set_digital_direction_output(self):
        test_connection = Mock(ScpiConnection)
        with ScpiSession(test_connection) as session:
            session.set_digital_direction('LED0', Direction.OUTPUT)

    def test_get_digital_state(self):
        test_connection = Mock(ScpiConnection)
        test_connection.read.return_value = '1'
        with ScpiSession(test_connection) as session:
            state = session.get_digital_state('DIO0_N')
        self.assertEqual(State.HIGH, state)

    def test_get_analog_input(self):
        test_connection = Mock(ScpiConnection)
        test_connection.read.return_value = '1.8'
        with ScpiSession(test_connection) as session:
            pin = 'AIN3'
            input_value = session.get_analog_input(pin)
        self.assertAlmostEqual(1.8, input_value, delta=0.0001)

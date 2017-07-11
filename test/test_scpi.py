from unittest import TestCase
from mock import Mock
from scpipy import ScpiConnection, State, Direction, DigitalController, AnalogController
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


class DigitalControllerTest(TestCase):
    def setUp(self):
        self.connection = Mock(ScpiConnection)
        self.connection.open()
        self.controller = DigitalController(self.connection)

    def test_set_state(self):
        pin = 'LED0'
        state = State.HIGH
        self.controller.set_state(pin, state)

    def test_set_direction(self):
        pin = 'LED0'
        direction = Direction.OUTPUT
        self.controller.set_direction(pin, direction)

    def test_get_state(self):
        self.connection.read.return_value = '1'
        pin = 'DIO0_N'
        state = self.controller.get_state('DIO0_N')
        self.assertEqual(State.HIGH, state)

    def tearDown(self):
        self.connection.close()
        

class AnalogControllerTest(TestCase):
    def setUp(self):
        self.connection = Mock(ScpiConnection)
        self.connection.open()
        self.controller = AnalogController(self.connection)

    def test_get_analog_input(self):
        self.connection.read.return_value = '1.8'
        pin = 'AIN3'
        voltage = self.controller.get_analog_input(pin)
        self.assertAlmostEqual(1.8, voltage, delta=0.0001)

    def test_set_analog_output(self):
        pin = 'AOUT3'
        value = 1.34
        self.controller.set_analog_output(pin, value)

    def tearDown(self):
        self.connection.close()

        
class GeneratorTest(TestCase):
    def test_reset_generator(self):
        with Mock(ScpiConnection) as test_connection:
            generator = Generator(test_connection)
            generator.reset()

class TestScpiConnection(object):
    def __init__(self, buffer = 'ABCDEF'):
        self.buffer = buffer
        
    def open(self):
        pass

    def close(self):
        pass

    def write(self, message):
        return len(message)

    def read(self, number_of_bytes=4096):
        return self.buffer

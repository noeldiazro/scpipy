from unittest import TestCase
from mock import Mock
from scpipy import *
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
    def setUp(self):
        self.connection = Mock(ScpiConnection)
        self.connection.open()
        self.generator = Generator(self.connection)
        
    def test_reset_generator(self):
        self.generator.reset()

    def test_set_waveform(self):
        channel = 1
        waveform = Waveform.SINE
        self.generator.set_waveform(channel, waveform)

    def test_set_frequency(self):
        channel = 1
        frequency = 100000
        self.generator.set_frequency(channel, frequency)

    def test_set_amplitude(self):
        channel = 2
        amplitude = 0.5
        self.generator.set_amplitude(channel, amplitude)

    def test_enable_output(self):
        channel = 1
        self.generator.enable_output(channel)

    def test_disable_output(self):
        channel = 1
        self.generator.disable_output(channel)

    def test_enable_burst_mode(self):
        channel = 1
        self.generator.enable_burst(channel)

    def test_disable_burst_mode(self):
        channel = 2
        self.generator.disable_burst(channel)

    def test_set_burst_count(self):
        channel = 1
        count = 3
        self.generator.set_burst_count(channel, count)

    def test_set_burst_repetitions(self):
        channel = 2
        repetitions = 5
        self.generator.set_burst_repetitions(channel, repetitions)

    def test_set_burst_period(self):
        channel = 1
        period_in_us = 2000
        self.generator.set_burst_period(channel, period_in_us)

    def test_trigger_immediately(self):
        channel = 1
        self.generator.trigger_immediately(channel)

    def test_set_arbitrary_waveform_data(self):
        channel = 1
        data = [1, 0.5, 0.2]
        self.generator.set_arbitrary_waveform_data(channel, data)
        
    def tearDown(self):
        self.connection.close()


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

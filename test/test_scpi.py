from unittest import TestCase, skip
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


class OscilloscopeTest(TestCase):

    def setUp(self):
        self.connection = TestScpiConnection()
        self.connection.open()
        self.oscilloscope = Oscilloscope(self.connection)

    def test_start(self):
        self.connection.buffer = '64'        
        self.oscilloscope.start()

    def test_stop(self):
        self.oscilloscope.stop()

    def test_reset(self):
        self.oscilloscope.reset()

    def test_set_decimation_factor(self):
        factor = 65536
        self.connection.buffer = '65536'
        self.oscilloscope.set_decimation_factor(factor)

    def test_get_decimation_factor(self):
        self.connection.buffer = '65536'
        factor = self.oscilloscope.get_decimation_factor()
        self.assertEqual(65536, factor)

    def test_enable_averaging(self):
        self.oscilloscope.enable_averaging()

    def test_disable_averaging(self):
        self.oscilloscope.disable_averaging()

    def test_disable_trigger(self):
        self.oscilloscope.disable_trigger()

    def test_trigger_inmediately(self):
        self.oscilloscope.trigger_inmediately()

    def test_set_trigger_event(self):
        source = TriggerSource.CH1
        edge = Edge.POSITIVE
        self.oscilloscope.set_trigger_event(source, edge)

    def test_set_trigger_level(self):
        voltage_in_mV = 125
        self.oscilloscope.set_trigger_level(voltage_in_mV)

    def test_get_trigger_level(self):
        self.connection.buffer = '123'
        self.assertEqual(123, self.oscilloscope.get_trigger_level())

    def test_set_trigger_delay_in_samples(self):
        number_of_samples = 2314
        self.oscilloscope.set_trigger_delay_in_samples(number_of_samples)

    def test_get_trigger_delay_in_samples(self):
        self.connection.buffer = '2314'
        self.assertEqual(2314, self.oscilloscope.get_trigger_delay_in_samples())

    def test_get_trigger_state_when_disabled(self):
        self.connection.buffer = 'TD'
        self.assertEqual(TriggerState.DISABLED, self.oscilloscope.get_trigger_state())

    def test_get_trigger_state_when_waiting(self):
        self.connection.buffer = 'WAIT'
        self.assertEqual(TriggerState.WAITING, self.oscilloscope.get_trigger_state())

    def test_get_data(self):
        self.connection.buffer = '{1.2,3.2,-1.2  }'
        channel = 1
        self.assertAlmostEqual([1.2, 3.2, -1.2], self.oscilloscope.get_data(channel)) 


    @skip('WIP: get_acquisition needs two distinct connection buffer outputs')
    def test_get_acquisition(self):
        channel = 1
        times, voltages = self.oscilloscope.get_acquisition(channel)

    def test_set_trigger_delay_in_ns(self):
        connection = MockScpiConnection('ACQ:TRIG:DLY:NS 128')
        oscilloscope = Oscilloscope(connection)

        trigger_delay_in_ns = 128
        oscilloscope.set_trigger_delay_in_ns(trigger_delay_in_ns)

        self.assertTrue(connection.is_write_called)

    def test_message_get_trigger_delay_in_ns(self):
        connection = MockScpiConnection('ACQ:TRIG:DLY:NS?', '128')
        oscilloscope = Oscilloscope(connection)
        oscilloscope.get_trigger_delay_in_ns()
        self.assertTrue(connection.is_write_called)
        
    def test_get_trigger_delay_in_ns(self):
        self.connection.buffer = '128'
        self.assertEqual(128, self.oscilloscope.get_trigger_delay_in_ns())

    def tearDown(self):
        self.connection.close()


class TestScpiConnection(object):
    def __init__(self, buffer = ''):
        self._buffer = buffer
        self._open = False
        
    def open(self):
        self._open = True

    def close(self):
        self._open = False

    def write(self, message):
        return len(message)

    def read(self, number_of_bytes=4096):
        return self._buffer
    
    @property
    def buffer(self):
        return self._buffer

    @buffer.setter
    def buffer(self, buffer):
        self._buffer = buffer

class MockScpiConnection(object):
    def __init__(self, expected_message, response=None):
        self._expected_message = expected_message
        self._response = response
        self._is_write_called = False
        self._is_read_called = False

    def open(self):
        pass

    def close(self):
        pass

    @property
    def is_write_called(self):
        return self._is_write_called
    
    def write(self, message):
        self._is_write_called = True
        if message != self._expected_message:
            raise Exception('Write received unexpected message. Expected {0} - '
                            'Received {1}'.format(self._expected_message, message))
        return len(message)

    @property
    def is_read_called(self):
        return self._is_read_called
    
    def read(self, number_of_bytes=4096):
        self._is_read_called = True
        return self._response

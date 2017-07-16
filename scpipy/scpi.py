from enum import Enum
from scpipy.links import TcpIpAddress, TcpIpLink

class State(Enum):
    LOW = '0'
    HIGH = '1'


class Direction(Enum):
    INPUT = 'IN'
    OUTPUT = 'OUTPUT'


class Waveform(Enum):
    SINE = 'SINE'
    SQUARE = 'SQUARE'
    TRIANGLE = 'TRIANGLE'
    SAWU = 'SAWU'
    SAWD = 'SAWD'
    PWD = 'PWD'
    ARBITRARY = 'ARBITRARY'


class TriggerSource(Enum):
    CH1 = 'CH1'
    CH2 = 'CH2'
    EXT = 'EXT'
    AWG = 'AWG'


class Edge(Enum):
    POSITIVE = 'PE'
    NEGATIVE = 'NE'
    

class TriggerState(Enum):
    DISABLED = 'TD'
    WAITING = 'WAIT'
    
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

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def get_tcpip_scpi_connection(host, port=5000, timeout=None, alt_socket=None):
    link = TcpIpLink(TcpIpAddress(host, port))
    return ScpiConnection(link)

        
class DigitalController(object):
    def __init__(self, connection):
        self._connection = connection

    def set_state(self, pin, state):
        message = 'DIG:PIN {},{}'.format(pin, state.value)
        self._connection.write(message)

    def set_direction(self, pin, direction):
        message = 'DIG:PIN DIR {},{}'.format(direction.value, pin)
        self._connection.write(message)

    def get_state(self, pin):
        request = 'DIG:PIN? {}'.format(pin)
        self._connection.write(request)
        return State(self._connection.read())


class AnalogController(object):
    def __init__(self, connection):
        self._connection = connection

    def get_analog_input(self, pin):
        request = 'ANALOG:PIN? {}'.format(pin)
        self._connection.write(request)
        return float(self._connection.read())

    def set_analog_output(self, pin, value):
        message = 'ANALOG:PIN {},{}'.format(pin, str(value))
        self._connection.write(message)


class Generator(object):
    def __init__(self, connection):
        self._connection = connection

    def command(self, message):
        self._connection.write(message)
        
    def reset(self):
        self.command('GEN:RST')

    def set_waveform(self, channel, waveform=Waveform.SINE):
        self.command('SOUR{}:FUNC {}'.format(channel, waveform.value))

    def set_frequency(self, channel, frequency=1000):
        self.command('SOUR{}:FREQ:FIX {}'.format(channel, frequency))

    def set_amplitude(self, channel, amplitude=1):
        self.command('SOUR{}:VOLT {}'.format(channel, amplitude))

    def _set_output_state(self, channel, state):
        self.command('OUTPUT{}:STATE {}'.format(channel, state))
        
    def enable_output(self, channel):
        self._set_output_state(channel, 'ON')

    def disable_output(self, channel):
        self._set_output_state(channel, 'OFF')

    def _set_gen_mode(self, channel, burst):
        self.command('SOUR{}:BURS:STAT {}'.format(channel, burst))

    def enable_burst(self, channel):
        self._set_gen_mode(channel, 'ON')

    def disable_burst(self, channel):
        self._set_gen_mode(channel, 'OFF')

    def set_burst_count(self, channel, count=1):
        self.command('SOUR{}:BURS:NCYC {}'.format(channel, count))

    def set_burst_repetitions(self, channel, repetitions=1):
        self.command('SOUR{}:BURS:NOR {}'.format(channel, repetitions))

    def set_burst_period(self, channel, period_in_us):
        self.command('SOUR{}:BURS:INT:PER {}'.format(channel, period_in_us))

    def trigger_immediately(self, channel):
        self.command('SOUR{}:TRIG:IMM'.format(channel))

    def set_arbitrary_waveform_data(self, channel, data):
        self.command('SOUR{}:TRAC:DATA:DATA {}'.format(channel, ','.join('{:1.2f}'.format(value) for value in data)))


class Oscilloscope(object):

    def __init__(self, connection):
        self._connection = connection

    def command(self, message):
        self._connection.write(message)
        
    def query(self, message):
        self._connection.write(message)
        return self._connection.read()

    def start(self):
        self.command('ACQ:START')

    def stop(self):
        self.command('ACQ:STOP')

    def reset(self):
        self.command('ACQ:RST')

    def set_decimation_factor(self, factor = 1):
        self.command('ACQ:DEC {}'.format(factor))

    def get_decimation_factor(self):
        return int(self.query('ACQ:DEC?'))

    def _set_averaging_state(self, state):
        self.command('ACQ:AVG {}'.format(state))

    def enable_averaging(self):
        self._set_averaging_state('ON')

    def disable_averaging(self):
        self._set_averaging_state('OFF')

    def disable_trigger(self):
        self.command('ACQ:TRIG DISABLED')

    def trigger_inmediately(self):
        self.command('ACQ:TRIG NOW')

    def set_trigger_event(self, source, edge):
        self.command('ACQ:TRIG {}_{}'.format(source.value, edge.value))

    def set_trigger_level(self, voltage_in_mV):
        self.command('ACQ:TRIG:LEV {}'.format(voltage_in_mV))

    def get_trigger_level(self):
        return int(self.query('ACQ:TRIG:LEV?'))

    def set_trigger_delay_in_samples(self, number_of_samples):
        self.command('ACQ:TRIG:DLY {}'.format(number_of_samples))

    def get_trigger_delay_in_samples(self):
        return int(self.query('ACQ:TRIG:DLY?'))

    def get_trigger_state(self):
        return TriggerState(self.query('ACQ:TRIG:STAT?'))

    def get_data(self, channel):
        raw_data = self.query('ACQ:SOUR{}:DATA?'.format(channel))
        return [float(datapoint) for datapoint in raw_data.strip('{}').split(',')]

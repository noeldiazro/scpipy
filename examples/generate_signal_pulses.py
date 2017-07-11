import sys
from scpipy import get_tcpip_scpi_connection, Generator, Waveform

def main(host):
    with get_tcpip_scpi_connection(host) as connection:
        generator = Generator(connection)
        generator.reset()

        generator.set_waveform(1, Waveform.SINE)
        generator.set_frequency(1, 1000)
        generator.set_amplitude(1, 0.5)


        generator.set_burst_count(1, 1)
        generator.set_burst_repetitions(1, 7)
        generator.set_burst_period(1, 2000)
        generator.enable_output(1)
        generator.enable_burst(1)        
        generator.trigger_immediately(1)


        
if __name__ == '__main__':
    host = sys.argv[1]
    main(host)


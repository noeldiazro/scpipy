import sys
from scpipy import get_tcpip_scpi_connection, Generator, Waveform

def main(host):
    with get_tcpip_scpi_connection(host) as connection:
        generator = Generator(connection)
        generator.reset()

        generator.set_waveform(1, Waveform.ARBITRARY)
        n_samples = 16384
        generator.set_arbitrary_waveform_data(1, [i * 1.0 / n_samples for i in range(n_samples)]) 
        generator.set_frequency(1, int(1/16e-6))
        generator.set_amplitude(1, 1)

        generator.enable_output(1)

        
if __name__ == '__main__':
    host = sys.argv[1]
    main(host)

import matplotlib.pyplot as plt
import sys
from scpipy import *

def main(host):
    with get_tcpip_scpi_connection(host) as connection:
        generator = Generator(connection)
        generator.reset()

        generator.set_waveform(1, Waveform.ARBITRARY)
        n_samples = 16384
        generator.set_arbitrary_waveform_data(1, [i * 1.0 / n_samples for i in range(n_samples)]) 
        #generator.set_waveform(1, Waveform.SINE)
        generator.set_frequency(1, 50000)
        generator.set_amplitude(1, 1)


        generator.enable_burst(1)
        generator.set_burst_count(1, 1)

        scope = Oscilloscope(connection)
        scope.reset()
        scope.set_decimation_factor(1)
        scope.set_trigger_level(0.1)
        scope.start()
        scope.set_trigger_event(TriggerSource.CH1, Edge.POSITIVE)
        generator.enable_output(1)


        time, data = scope.get_acquisition(1)
        
        plt.plot(time, data, 'b-')
        plt.grid(True)
        plt.show()

        
if __name__ == '__main__':
    host = sys.argv[1]
    main(host)

import matplotlib.pyplot as plt
import sys
import scpipy

def main(host):
    with scpipy.get_tcpip_scpi_connection(host) as connection:
        generator = scpipy.Generator(connection)
        generator.reset()
        generator.set_waveform(1, scpipy.Waveform.SINE)
        generator.set_frequency(1, 1000)
        generator.set_amplitude(1, 0.8)

        generator.enable_burst(1)
        generator.set_burst_count(1, 1)


        scope = scpipy.Oscilloscope(connection)
        scope.reset()
        scope.set_decimation_factor(64)
        scope.start()
        scope.set_trigger_event(scpipy.TriggerSource.CH1, scpipy.Edge.POSITIVE)
        generator.enable_output(1)    
        time, data = scope.get_acquisition(1)

        
        plt.plot(time, data)
        plt.grid(True)
        plt.show()
        
if __name__ == '__main__':
    host = sys.argv[1]
    main(host)

from pprint import pprint
import sys
from time import sleep
from scpipy import get_tcpip_scpi_connection, Oscilloscope, TriggerState

def main(host):
    with get_tcpip_scpi_connection(host) as connection:
        scope = Oscilloscope(connection)
        scope.start()
        scope.trigger_inmediately()
        while not scope.get_trigger_state() == TriggerState.DISABLED:
            sleep(0.001)
        data = scope.get_data(1)
        pprint(data[:100])
        
if __name__ == '__main__':
    host = sys.argv[1]
    main(host)

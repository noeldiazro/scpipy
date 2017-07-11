import sys
from time import sleep
from scpipy import get_tcpip_scpi_connection, AnalogController

def main(host):
    period = 1
    with get_tcpip_scpi_connection(host) as connection:
        controller = AnalogController(connection)
        try:
            while True:
                voltage = controller.get_analog_input('AIN3')
                print(voltage)
                sleep(period)
        except KeyboardInterrupt:
            print('Bye!')

if __name__ == '__main__':
    host = sys.argv[1]
    main(host)

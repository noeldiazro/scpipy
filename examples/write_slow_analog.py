import sys
from time import sleep
from scpipy import get_tcpip_scpi_connection, AnalogController

def main(host):
    period = 1
    with get_tcpip_scpi_connection(host) as connection:
        controller = AnalogController(connection)
        for i in range(60):
            controller.set_analog_output('AOUT3', i * 0.03)
            sleep(period)

if __name__ == '__main__':
    host = sys.argv[1]
    main(host)

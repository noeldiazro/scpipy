import sys
from time import sleep
from scpipy import get_tcpip_scpi_connection, DigitalController, State

def main(host):
    period = 1
    with get_tcpip_scpi_connection(host) as connection:
        controller = DigitalController(connection)
        try:
            while True:
                controller.set_state('LED0', State.HIGH)
                sleep(period / 2.0)
                controller.set_state('LED0', State.LOW)
                sleep(period / 2.0)
        except KeyboardInterrupt:
            print('Bye!')

if __name__ == '__main__':
    host = sys.argv[1]
    main(host)

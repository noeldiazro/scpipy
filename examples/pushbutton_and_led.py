import sys
from time import sleep
from scpipy import get_tcpip_scpi_connection, DigitalController, Direction

def main(host):
    with get_tcpip_scpi_connection(host) as connection:
        controller = DigitalController(connection)
        controller.set_direction('DIO5_N', Direction.INPUT)
        try:
            while True:
                state = controller.get_state('DIO5_N') 
                controller.set_state('LED5', state)
                sleep(0.1)
        except KeyboardInterrupt:
            print('Bye!')


if __name__ == '__main__':
    host = sys.argv[1]
    main(host)

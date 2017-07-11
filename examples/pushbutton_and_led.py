import sys
from time import sleep
from scpipy import ScpiSessionFactory, Direction

def main(host):
    with ScpiSessionFactory().get_scpi_session(host) as session:
        session.set_digital_direction('DIO5_N', Direction.INPUT)
        try:
            while True:
                state = session.get_digital_state('DIO5_N') 
                session.set_digital_output_state('LED5', state)
                sleep(0.1)
        except KeyboardInterrupt:
            print('Bye!')


if __name__ == '__main__':
    host = sys.argv[1]
    main(host)

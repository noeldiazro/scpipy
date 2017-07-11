import sys
from time import sleep
from scpipy import ScpiSessionFactory, State

def main(host):
    period = 1
    with ScpiSessionFactory().get_scpi_session(host) as session:
        try:
            while True:
                session.set_digital_output_state('LED0', State.HIGH)
                sleep(period / 2.0)
                session.set_digital_output_state('LED0', State.LOW)
                sleep(period / 2.0)
        except KeyboardInterrupt:
            print('Bye!')

if __name__ == '__main__':
    host = sys.argv[1]
    main(host)

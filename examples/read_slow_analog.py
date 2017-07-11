import sys
from time import sleep
from scpipy import ScpiSessionFactory

def main(host):
    period = 1
    with ScpiSessionFactory().get_scpi_session(host) as session:
        try:
            while True:
                voltage = session.get_analog_input('AIN3')
                print(voltage)
                sleep(period)
        except KeyboardInterrupt:
            print('Bye!')

if __name__ == '__main__':
    host = sys.argv[1]
    main(host)

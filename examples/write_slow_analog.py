import sys
from time import sleep
from scpipy import ScpiSessionFactory

def main(host):
    period = 1
    with ScpiSessionFactory().get_scpi_session(host) as session:
        for i in range(60):
            session.set_analog_output('AOUT3', i * 0.03)
            sleep(period)

if __name__ == '__main__':
    host = sys.argv[1]
    main(host)

"""Easy tunnel program"""
import logging

import tunnel

LOGLEVEL = logging.DEBUG
LOGFORMAT = '%(name)s - %(levelname)s - %(message)s'


def dummyhandler(_):
    pass

if __name__ == '__main__':
    logging.basicConfig(format=LOGFORMAT, level=LOGLEVEL)
    t = tunnel.Tunnel(mode='tun')

    def echohandler(data):
        """Echo the received data back to the sender"""
        t.send(data)
    t.set_rx_handler(echohandler)
    t.monitor()

    try:
        raw_input('Wait indefinitely. Press ctrl-c to quit.')
    except KeyboardInterrupt:
        t.close()



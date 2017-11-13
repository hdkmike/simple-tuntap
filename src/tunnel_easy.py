"""Easy tunnel program"""
import dpkt
import logging
import socket

import tunnel

LOGLEVEL = logging.DEBUG
LOGFORMAT = '%(name)s - %(levelname)s - %(message)s'


def dummyhandler(_):
    pass

if __name__ == '__main__':
    logging.basicConfig(format=LOGFORMAT, level=LOGLEVEL)
    t = tunnel.Tunnel(mode='tun')

    def echohandler(data):
        """Echo the received data back to the sender
        but swap source and dest IPs"""
        # Assume it's L3
        leading_bytes = data[:4]
        data = data[4:]  # Strip off the first 4 bytes
        ip_pkt = dpkt.ip.IP(data)
        src = ip_pkt.src
        dst = ip_pkt.dst
        ip_pkt.src = dst
        ip_pkt.dst = src
        data = leading_bytes + ip_pkt.__bytes__()
        t.send(data)
    t.set_rx_handler(echohandler)
    t.monitor()

    try:
        raw_input('Wait indefinitely. Press ctrl-c to quit.')
    except KeyboardInterrupt:
        t.close()



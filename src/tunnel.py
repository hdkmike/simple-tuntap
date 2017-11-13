"""Simple TUN/TAP module for Linux only"""
import logging
import os
import socket

import pytun
import select
from threading import Event, Thread


class Tunnel(object):
    """Class to tunnel data"""

    def __init__(self, mode=None):
        self._logger = logging.getLogger(self.__module__)
        self._logger.debug('Tunnel class created')
        self._threadEvent = Event()
        self._handler = None
        self._stopsocket1, self._stopsocket2 = socket.socketpair()

        if mode is None or mode.lower() == 'tun':
            tunmode = 'tun'
        elif mode.lower() == 'tap':
            tunmode = 'tap'
        else:
            self._logger.critical('Tunnel Mode %s is not supported', mode)
            raise Exception("Tunnel mode not supported")

        self._tun = pytun.open(tunmode)

        # TODO Set up addressing
        os.system('ip link set %s up' % self._tun.name)
        os.system('ip address add 192.168.40.1/32 dev %s' % self._tun.name)
        os.system('ip route add 192.168.40.2/32 dev %s' % self._tun.name)

    def close(self):
        """Shutdown and close the tunnel"""
        self._threadEvent.set()
        self._stopsocket2.close()  # Closing this socket will break out of the select

    def monitor(self):
        """Wrapper for monitoring incoming connections"""
        self._logger.info('Monitoring socket...')

        rx_thread = Thread(target=self._monitor_socket)
        rx_thread.start()

    def _monitor_socket(self):
        """Monitor the tun adapter for incoming packets and call the handler with param of data received"""
        while not self._threadEvent.isSet():
            fds = select.select([self._tun, self._stopsocket1], [], [])
            r, _, _ = fds
            for f in r:
                if f == self._tun:
                    self._logger.debug('Handling packet...')
                    data = f.recv()
                    if self._handler:
                        self._handler(data)

    def send(self, data):
        """Write the received data to the tun socket"""
        self._logger.debug("Sending packet...")
        self._tun.send(data)

    def set_rx_handler(self, handler):
        """Set the receiving handler"""
        self._handler = handler


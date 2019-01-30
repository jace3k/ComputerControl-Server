import getpass
import logging as log
from socket import *
from threading import Thread

GRPC_PORT = 12344
BROADCAST_PORT = 12342
RECEIVER_PORT = 12343

KEY = 'pl.jacekpiszczek.remoteapp.client'


class BroadcastReceiver(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.name = 'BroadcastReceiver'
        self.r = socket(AF_INET, SOCK_DGRAM)
        self.r.bind(('', BROADCAST_PORT))
        self.r.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        log.info('{} started on port {}'.format(self.name, BROADCAST_PORT))

    def run(self):
        while 1:
            received = self.r.recvfrom(150)
            log.info('{} receive: {}'.format(self.name, received))
            if received[0].decode('utf-8') == KEY:
                ResponseSocket((received[1][0], RECEIVER_PORT)).start()


class ResponseSocket(Thread):
    def __init__(self, address):
        Thread.__init__(self)
        self.name = 'ResponseSocket'
        self.s = socket()
        self.address = address

    def run(self):
        self.s.connect(self.address)
        self.s.send(getpass.getuser().encode())
        log.debug('{} has sent response'.format(self.name))
        self.s.close()


def start_broadcast_receiver():
    BroadcastReceiver().start()

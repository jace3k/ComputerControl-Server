import logging
from concurrent import futures

import grpc

import gui
from networking import start_broadcast_receiver, GRPC_PORT
from service import sleep, setup_service


def serve(pin):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=15))
    setup_service(server, pin)
    server.add_insecure_port('[::]:{}'.format(GRPC_PORT))
    server.start()
    logging.info('GRPC started on port {}'.format(GRPC_PORT))

    start_broadcast_receiver()

    sleep()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    p = gui.get_pin()
    if p is not 0:
        serve(p)

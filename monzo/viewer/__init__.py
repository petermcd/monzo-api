import logging

from monzo.viewer.server import Server

HOST = 'localhost'
PORT = 8080


def start_server():
    try:
        Server(host=HOST, port=PORT)
    except KeyboardInterrupt:
        print('Server Closed')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    start_server()

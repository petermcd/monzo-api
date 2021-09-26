from monzo.viewer.server import Server


def start_server():
    try:
        Server(8764)
    except KeyboardInterrupt:
        print('Server Closed')


if __name__ == '__main__':
    start_server()

from http.server import HTTPServer
from typing import Optional

from monzo.viewer.handler import Handler


class Server(object):
    """
    Create and run a server.
    """
    __slots__ = (
        '_handler',
        '_server',
        '_port'
    )

    def __init__(self, port: int):
        """
        Set up the server.

        Args:
            port: Port number server should listen on
        """
        self._port: int = port
        self._handler = Handler
        self._server: Optional[HTTPServer] = None
        self.run()

    def run(self) -> None:
        """
        Start the server daemon.
        """
        server_address = ('127.0.0.1', self._port)
        self._server = HTTPServer(server_address, self._handler)
        if self._server:
            print(f'Server started, visit http://{server_address[0]}:{server_address[1]}/index.html')
            self._server.serve_forever()

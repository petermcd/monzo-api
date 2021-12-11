import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from typing import Tuple
from jinja2 import Environment, PackageLoader, select_autoescape

HOST = 'localhost'
PORT = 8080


class MonzoHandler(BaseHTTPRequestHandler):
    _paths = {
        '/': 'req_index',
        '/auth': 'req_monzo_auth',
    }

    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        super().__init__(request, client_address, server)
        self._template = Environment(
            loader=PackageLoader('monzo-server', 'templates'),
            autoescape=select_autoescape()
        )

    def do_GET(self):
        url_parse = urlparse(self.path)
        method = self._paths.get(url_parse.path, 'req_404')
        self.__getattribute__(method)()

    def do_POST(self):
        pass

    def _get(self):
        url_parse = urlparse(self.path)
        return parse_qs(url_parse.query)

    def _post(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        _post_tmp = parse_qs(post_body)
        return {
            key.decode('UTF-8'): _post_tmp[key][0].decode('UTF-8')
            for key in _post_tmp.keys()
        }

    def req_index(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Index</title></head></html>", "utf-8"))

    def req_monzo_auth(self):
        url_parse = urlparse(self.path)
        params = parse_qs(url_parse.query)
        print(params)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Index</title></head></html>", "utf-8"))

    def req_404(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Page Not Found</title></head></html>", "utf-8"))


if __name__ == '__main__':
    webserver = HTTPServer(server_address=(HOST, PORT), RequestHandlerClass=MonzoHandler)
    try:
        webserver.serve_forever()
    except KeyboardInterrupt:
        pass

    webserver.server_close()

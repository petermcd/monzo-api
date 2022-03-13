"""Standard init for viewer2."""
import logging
import socketserver
from http import server

HOST = "localhost"
PORT = 8080

logging.basicConfig(level=logging.DEBUG)
handler = server.SimpleHTTPRequestHandler

with socketserver.TCPServer(
    server_address=(HOST, PORT), RequestHandlerClass=handler
) as httpd:
    logging.debug(f"STarting server on http://{HOST}:{PORT}")
    httpd.serve_forever()

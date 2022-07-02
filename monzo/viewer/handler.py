"""HTTP Request handler."""
import logging
from http.server import BaseHTTPRequestHandler

from monzo.viewer.controller import Controller


class Handler(BaseHTTPRequestHandler):
    """Handler for requests."""

    def do_GET(self):
        """Handle GET requests."""
        logging.debug('Processing GET request')
        self._process_request()

    def do_POST(self):
        """Handle GET requests."""
        logging.debug('Processing POST request')
        self._process_request()

    def _process_request(self):
        """Process a generic request."""
        mon = Controller()
        try:
            response = mon.process_request(request=self)
            self.send_response(response['code'], response['message'])
            self.end_headers()
            self.wfile.write(response['content'])
        except ConnectionAbortedError:
            logging.debug('End aborted connection')

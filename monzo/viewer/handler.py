from http.server import BaseHTTPRequestHandler

from monzo.viewer.controller import Controller


class Handler(BaseHTTPRequestHandler):
    """
    Handler for requests.
    """

    def do_GET(self):
        """
        Handle GET requests.
        """
        mon = Controller()
        response = mon.process_request(request=self)
        self.send_response(response['code'], response['message'])
        self.end_headers()
        self.wfile.write(response['content'])

    def do_POST(self):
        """
        Handle GET requests.
        """
        mon = Controller()
        response = mon.process_request(request=self)
        self.send_response(response['code'], response['message'])
        self.end_headers()
        self.wfile.write(response['content'])

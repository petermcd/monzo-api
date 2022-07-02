"""Controller to handle requests."""
import logging
from json import dumps, loads
from typing import Dict, List, Optional, Tuple, Union
from urllib import parse

from jinja2 import Environment, PackageLoader, select_autoescape

from monzo.authentication import Authentication
from monzo.exceptions import MonzoAuthenticationError
from monzo.viewer.filesystem import FileSystem
from monzo.viewer.monzo_data import MonzoData

logging.basicConfig(level=logging.DEBUG)
SCRIPT_MAP = {
    '/': 'index',
    '/auth_step_one.html': 'auth_step_one',
    '/auth_step_two.html': 'auth_step_two',
    '/index.html': 'index',
    '/monzo': 'fetch_token',
    '/raw_request.html': 'raw_request',
}

IGNORE_PATHS = (
    'favicon.ico'
)

MONZO_HANDLER = FileSystem('monzo.json')
MONZO_DATA = MonzoData()


class Controller(object):
    """Controller to process the request."""

    __slots__ = [
        '_AUTH',
        '_TEMPLATE_ENV'
    ]
    _REDIRECT_URL: Optional[str] = None

    def __init__(self):
        """Initialize Controller."""
        self._TEMPLATE_ENV = Environment(
            loader=PackageLoader('monzo.viewer', 'html'),
            autoescape=select_autoescape()
        )
        self._AUTH = None
        if MONZO_HANDLER.is_configured:
            self._AUTH = Authentication(
                access_token=MONZO_HANDLER.access_token,
                access_token_expiry=MONZO_HANDLER.expiry,
                client_id=MONZO_HANDLER.client_id,
                client_secret=MONZO_HANDLER.client_secret,
                redirect_url=Controller._REDIRECT_URL,
                refresh_token=MONZO_HANDLER.refresh_token,
            )

    def process_request(self, request) -> Dict[str, Union[bytes, int, str]]:
        """
        Process a given request.

        Args:
            request: Request handler

        Returns:
            Dictionary containing the response
        """
        logging.debug('Processing received request')
        if not Controller._REDIRECT_URL:
            Controller._REDIRECT_URL =\
                f'http://{request.server.server_address[0]}:{request.server.server_address[1]}/monzo'
        path, parameters = Controller._parse_request_path(request=request)
        parameters = {**parameters, **Controller._parse_request_body(request=request)}
        if path in IGNORE_PATHS or path not in SCRIPT_MAP:
            logging.debug(f'{path} points to a 404')
            return self._404(request=request, parameters=parameters)
        method = self.__getattribute__(SCRIPT_MAP.get(path, 'index'))
        return method(request=request, parameters=parameters)

    def _404(self, request, parameters: Dict[str, List[str]]) -> Dict[str, Union[bytes, int, str]]:
        """
        Output a 404 error page.

        Returns:
            Dictionary containing the response
        """
        logging.debug('Outputting 404 page')
        return {
            'code': 404,
            'message': 'Page Not Found',
            'content': self._fetch_template(template_name='404.html', variables={}).encode('utf-8'),
        }

    def auth_step_one(self, request, parameters: Dict[str, List[str]]) -> Dict[str, Union[bytes, int, str]]:
        """
        Create the ath step one page.

        Returns:
            Dictionary containing the response
        """
        logging.debug('Outputting Monzo form to capture client id and secret')
        redirect_url = f'http://{request.server.server_address[0]}:{request.server.server_address[1]}/monzo'
        variables: Dict[str, Union[int, object, str]] = {
            'REDIRECT_URL_VALUE': redirect_url,
        }
        return {
            'code': 200,
            'message': 'OK',
            'content': self._fetch_template(template_name='auth_step_one.html', variables=variables).encode('utf-8'),
        }

    def auth_step_two(self, request, parameters: Dict[str, List[str]]) -> Dict[str, Union[bytes, int, str]]:
        """
        Create the ath step two page.

        Returns:
            Dictionary containing the response
        """
        redirect_url = f'http://{request.server.server_address[0]}:{request.server.server_address[1]}/monzo'
        template = 'auth_step_two.html'
        variables: Dict[str, Union[int, object, str]] = {}
        if 'client_id' not in parameters or 'client_secret' not in parameters:
            logging.debug('Missing client_id or client_secret, re-requesting details')
            variables = {
                'ERROR_MESSAGE': 'Please enter all fields',
                'CLIENT_ID_VALUE': parameters.get('client_id', [''])[0],
                'CLIENT_SECRET_VALUE': parameters.get('client_secret', [''])[0],
                'REDIRECT_URL_VALUE': redirect_url,
            }
            template = 'auth_step_one.html'
        else:
            MONZO_HANDLER.client_id = parameters['client_id'][0]
            MONZO_HANDLER.client_secret = parameters['client_secret'][0]
            self._AUTH = Authentication(
                client_id=MONZO_HANDLER.client_id,
                client_secret=MONZO_HANDLER.client_secret,
                redirect_url=redirect_url,
            )
            variables = {
                'AUTHENTICATION_URL': self._AUTH.authentication_url or '',
            }
            logging.debug('Outputting Monzo authentication URL')
        return {
            'code': 200,
            'message': 'OK',
            'content': self._fetch_template(template_name=template, variables=variables).encode('utf-8'),
        }

    def fetch_token(self, request, parameters: Dict[str, List[str]]) -> Dict[str, Union[bytes, int, str]]:
        """
        Fetch the token from Monzo.

        Returns:
            Dictionary containing the response
        """
        logging.debug('Fetching token from Monzo')
        redirect_url = f'http://{request.server.server_address[0]}:{request.server.server_address[1]}/monzo'
        code = parameters.get('code', [''])[0]
        state = parameters.get('state', [''])[0]
        if not any([code, state]):
            logging.debug('Missing code or state parameters')
            return self._404(request=request, parameters=parameters)
        self._AUTH = Authentication(
            client_id=MONZO_HANDLER.client_id,
            client_secret=MONZO_HANDLER.client_secret,
            redirect_url=redirect_url,
        )
        self._AUTH.register_callback_handler(MONZO_HANDLER)
        try:
            self._AUTH.authenticate(authorization_token=code, state_token=state)
        except MonzoAuthenticationError:
            logging.debug('Received a monzo authentication error when trying to fetch token')
            return self._404(request=request, parameters=parameters)
        variables: Dict[str, Union[int, object, str]] = {
            'CLIENT_ID': MONZO_HANDLER.client_id,
            'CLIENT_SECRET': MONZO_HANDLER.client_secret,
            'REDIRECT_URL': redirect_url,
            'ACCESS_TOKEN': MONZO_HANDLER.access_token,
            'TOKEN_EXPIRY': MONZO_HANDLER.expiry,
            'REFRESH_TOKEN': MONZO_HANDLER.refresh_token,
        }
        return {
            'code': 200,
            'message': 'OK',
            'content': self._fetch_template(template_name='auth_tokens.html', variables=variables).encode('utf-8'),
        }

    def index(self, request, parameters: Dict[str, List[str]]) -> Dict[str, Union[bytes, int, str]]:
        """
        Create the starting page.

        Returns:
            Dictionary containing the response
        """
        logging.debug('Outputting index page')
        variables: Dict[str, Union[bool, int, object, str]] = {
            'configured': MONZO_HANDLER.is_configured,
        }
        if MONZO_HANDLER.is_configured:
            variables['accounts'] = MONZO_DATA.get_accounts(auth=self._AUTH)

        if 'transactions' in parameters and 'accounts' in parameters:
            variables['transactions'] = MONZO_DATA.get_transactions(self._AUTH, parameters['accounts'][0])

        return {
            'code': 200,
            'message': 'OK',
            'content': self._fetch_template(template_name='index.html', variables=variables).encode('utf-8'),
        }

    def raw_request(self, request, parameters: Dict[str, List[str]]) -> Dict[str, Union[bytes, int, str]]:
        """
        Create the raw request page.

        Returns:
            Dictionary containing the response
        """
        logging.debug('Outputting raw request page')
        variables: Dict[str, Union[bool, int, object, str]] = {
            'configured': MONZO_HANDLER.is_configured,
        }
        if 'submit' in parameters:
            authenticated = bool(parameters.get('authenticated', True))
            request_type = parameters.get('authenticated', ['get'])[0]
            headers = loads(parameters['headers'][0]) if 'headers' in parameters else {}
            monzo_parameters = {}
            if 'parameters' in parameters:
                monzo_parameters = loads(parameters['parameters'][0])

            records = MONZO_DATA.get_raw_request(
                auth=self._AUTH,
                path=parameters.get('path', ['/'])[0],
                authenticated=authenticated,
                request_type=request_type,
                headers=headers,
                parameters=monzo_parameters
            )
            variables['records'] = dumps(records, indent=4, sort_keys=True)
        return {
            'code': 200,
            'message': 'OK',
            'content': self._fetch_template(template_name='raw_request.html', variables=variables).encode('utf-8'),
        }

    @staticmethod
    def _parse_request_body(request) -> Dict[str, List[str]]:
        """
        Obtain query parameters from the URL.

        Returns:
             Dictionary of parameters
        """
        if 'Content-Length' in request.headers and int(request.headers['Content-Length']) > 0:
            content_len = int(request.headers.get('Content-Length', 0))
            post_body = request.rfile.read(content_len).decode('utf-8')
            return parse.parse_qs(post_body)
        return {}

    @staticmethod
    def _parse_request_path(request) -> Tuple[str, Dict[str, List[str]]]:
        """
        Obtain query parameters from the URL.

        Returns:
             Tuple of (path, Dictionary of parameters)
        """
        query_string = parse.urlparse(request.path)
        return query_string.path, parse.parse_qs(query_string.query)

    def _fetch_template(self, template_name: str, variables: Dict[str, Union[bool, int, object, str]]) -> str:
        """
        Fetch a template and replace the variable placeholders.

        Args:
            template_name: Template name
            variables: Dictionary of variables and their values

        Returns:
            Processed template
        """
        template = self._TEMPLATE_ENV.get_template(template_name)
        return template.render(variables)

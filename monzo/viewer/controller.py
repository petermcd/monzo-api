from os.path import join
from re import sub
from typing import Dict, List, Optional, Tuple, Union
from urllib import parse

from monzo.authentication import Authentication
from monzo.exceptions import MonzoAuthenticationError

SCRIPT_MAP = {
    '/': 'index',
    '/auth_step_one.html': 'auth_step_one',
    '/auth_step_two.html': 'auth_step_two',
    '/index.html': 'index',
    '/monzo': 'fetch_token',
}

IGNORE_PATHS = (
    'favicon.ico'
)


class Controller(object):
    """
    Controller to process the request.
    """
    _AUTH: Optional[Authentication] = None
    _CLIENT_ID: str = ''
    _CLIENT_SECRET: str = ''
    _ACCESS_TOKEN: str = ''
    _TOKEN_EXPIRY: int = 0
    _REFRESH_TOKEN: str = ''
    _REDIRECT_URL: str = ''

    def process_request(self, request) -> Dict[str, Union[bytes, int, str]]:
        """
        Process a given request.

        Args:
            request: Request handler

        Returns:
            Dictionary containing the response
        """
        if not Controller._REDIRECT_URL:
            Controller._REDIRECT_URL =\
                f'http://{request.server.server_address[0]}:{request.server.server_address[1]}/monzo'
        path, parameters = self._parse_request_path(request)
        if path in IGNORE_PATHS or path not in SCRIPT_MAP:
            return self._404(request=request, parameters=parameters)
        method = self.__getattribute__(SCRIPT_MAP.get(path, 'index'))
        return method(request=request, parameters=parameters)

    def _404(self, request, parameters: Dict[str, List[str]]) -> Dict[str, Union[bytes, int, str]]:
        """
        Output a 404 error page.

        Returns:
            Dictionary containing the response
        """
        return {
            'code': 404,
            'message': 'Page Not Found',
            'content': self._fetch_template(template='404.html', variables={}).encode('utf-8'),
        }

    def index(self, request, parameters: Dict[str, List[str]]) -> Dict[str, Union[bytes, int, str]]:
        """
        Create the starting page.

        Returns:
            Dictionary containing the response
        """
        return {
            'code': 200,
            'message': 'OK',
            'content': self._fetch_template(template='index.html', variables={}).encode('utf-8'),
        }

    def auth_step_one(self, request, parameters: Dict[str, List[str]]) -> Dict[str, Union[bytes, int, str]]:
        """
        Create the ath step one page.

        Returns:
            Dictionary containing the response
        """
        variables: Dict[str, Union[int, str]] = {
            'REDIRECT_URL_VALUE': Controller._REDIRECT_URL,
        }
        return {
            'code': 200,
            'message': 'OK',
            'content': self._fetch_template(template='auth_step_one.html', variables=variables).encode('utf-8'),
        }

    def auth_step_two(self, request, parameters: Dict[str, List[str]]) -> Dict[str, Union[bytes, int, str]]:
        """
        Create the ath step two page.

        Returns:
            Dictionary containing the response
        """
        parameters = self._parse_request_body(request=request)
        template = 'auth_step_two.html'
        variables: Dict[str, Union[int, str]] = {}
        if not any([parameters['client_id'], parameters['client_secret']]):
            variables = {
                'ERROR_MESSAGE': 'Please enter all fields',
                'CLIENT_ID_VALUE': parameters['client_id'][0],
                'CLIENT_SECRET_VALUE': parameters['client_secret'][0],
                'REDIRECT_URL_VALUE': Controller._REDIRECT_URL,
            }
            template = 'auth_step_one.html'
        else:
            Controller._CLIENT_ID = parameters['client_id'][0]
            Controller._CLIENT_SECRET = parameters['client_secret'][0]
            auth = Authentication(
                client_id=Controller._CLIENT_ID,
                client_secret=Controller._CLIENT_SECRET,
                redirect_url=Controller._REDIRECT_URL,
            )
            variables = {
                'AUTHENTICATION_URL': auth.authentication_url,
            }
        return {
            'code': 200,
            'message': 'OK',
            'content': self._fetch_template(template=template, variables=variables).encode('utf-8'),
        }

    def fetch_token(self, request, parameters: Dict[str, List[str]]) -> Dict[str, Union[bytes, int, str]]:
        """
        Fetch the token from Monzo.

        Returns:
            Dictionary containing the response
        """
        if not any([parameters['code'], parameters['state']]):
            return self._404(request=request, parameters=parameters)
        auth = Authentication(
            client_id=Controller._CLIENT_ID,
            client_secret=Controller._CLIENT_SECRET,
            redirect_url=Controller._REDIRECT_URL,
        )
        try:
            auth.authenticate(authorization_token=parameters['code'][0], state_token=parameters['state'][0])
            Controller._ACCESS_TOKEN = auth.access_token
            Controller._TOKEN_EXPIRY = auth.access_token_expiry
            Controller._REFRESH_TOKEN = auth.refresh_token
        except MonzoAuthenticationError:
            return self._404(request=request, parameters=parameters)
        variables: Dict[str, Union[int, str]] = {
            'CLIENT_ID': Controller._CLIENT_ID,
            'CLIENT_SECRET': Controller._CLIENT_SECRET,
            'REDIRECT_URL': Controller._REDIRECT_URL,
            'ACCESS_TOKEN': Controller._ACCESS_TOKEN,
            'TOKEN_EXPIRY': Controller._TOKEN_EXPIRY,
            'REFRESH_TOKEN': Controller._REFRESH_TOKEN,
        }
        return {
            'code': 200,
            'message': 'OK',
            'content': self._fetch_template(template='auth_tokens.html', variables=variables).encode('utf-8'),
        }

    def _parse_request_body(self, request) -> Dict[str, List[str]]:
        """
        Obtain query parameters from the URL.

        Returns:
             Dictionary of parameters
        """
        content_len = int(request.headers.get('Content-Length'))
        post_body = request.rfile.read(content_len).decode('utf-8')
        return parse.parse_qs(post_body)

    def _parse_request_path(self, request) -> Tuple[str, Dict[str, List[str]]]:
        """
        Obtain query parameters from the URL.

        Returns:
             Tuple of (path, Dictionary of parameters)
        """
        query_string = parse.urlparse(request.path)
        return query_string.path, parse.parse_qs(query_string.query)

    @staticmethod
    def _fetch_template(template: str, variables: Dict[str, Union[int, str]]) -> str:
        """
        Fetch a template and replace the variable placeholders.

        Args:
            template: Template name
            variables: Dictionary of variables and their values

        Returns:
            Processed templates
        """
        path = join('html', template)
        with open(path, 'r') as html_file:
            html = html_file.read()
        for variable_key, value in variables.items():
            html = html.replace('{{ ' + variable_key + ' }}', str(value))
        regex = r'{{[ ]?[A-Za-z0-9_]+[ ]?}}'
        html = sub(regex, '', html)
        return html

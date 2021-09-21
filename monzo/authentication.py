import os
from pathlib import Path, PurePath
from tempfile import gettempdir
from time import time

from monzo import helpers
from monzo.exceptions import MonzoAuthenticationError
from monzo.httpio import DEFAULT_TIMEOUT, REQUEST_RESPONSE_TYPE, HttpIO

MONZO_AUTH_URL = 'https://auth.monzo.com'
MONZO_API_URL = 'https://api.monzo.com'


class Authentication:

    __slots__ = [
        '_access_token',
        '_access_token_expiry',
        '_client_id',
        '_client_secret',
        '_redirect_url',
        '_refresh_token',
    ]

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            redirect_url: str = '',
            access_token: str = '',
            access_token_expiry: int = 0,
            refresh_token: str = ''
    ):
        """
        Standard init.

        Args:
            client_id: Client ID generated at https://developers.monzo.com
            redirect_url: Redirect URL for authentication
            access_token: Pre existing access token
        """
        self._access_token: str = access_token
        self._access_token_expiry: int = access_token_expiry
        self._client_id: str = client_id
        self._client_secret: str = client_secret
        self._redirect_url: str = redirect_url
        self._refresh_token: str = refresh_token

    def authenticate(self, authorization_token: str, state_token: str) -> None:
        """
        Completes authentication once the authentication URL has been visited.

        Args:
            authorization_token: Authorization code provided by Monzo
            state_token: Pre agreed state token to validate against
        """
        if not authorization_token:
            raise MonzoAuthenticationError('Code missing from response')
        if state_token != self.state_token:
            raise MonzoAuthenticationError('State tokens do not match')
        tmp_file_name = 'monzo'
        tmp_file_path = PurePath(gettempdir(), tmp_file_name)
        os.remove(tmp_file_path)
        self._exchange_token(authorization_token=authorization_token)

    def logout(self) -> None:
        """
        Invalidates the access token.
        """
        self.make_request(path='/oauth2/logout')

    def make_request(
            self,
            path: str,
            authenticated: bool = True,
            method: str = 'GET',
            data=None,
            headers=None,
            timeout: int = DEFAULT_TIMEOUT
    ) -> REQUEST_RESPONSE_TYPE:
        """
        Makes an API call to Monzo.

        Args:
            path: Path for the API call
            authenticated: True if authenticated request should be made otherwise False
            method: Method for the API call (DELETE, GET, POST, PUT)
            data: Dictionary of data to be posted as form data or URL parameters
            headers: Dictionary of headers for the request
            timeout: Timeout in seconds for the request

        Returns:
        """
        if self._access_token and self._access_token_expiry - time() < 0:
            self.refresh_access()
        if data is None:
            data = {}
        if headers is None:
            headers = {}
        conn = HttpIO(MONZO_API_URL)
        connection = conn.get
        method = method.lower()
        if method == 'delete':
            connection = conn.delete
        elif method == 'post':
            connection = conn.post
        elif method == 'put':
            connection = conn.put
        if authenticated:
            headers['Authorization'] = f'Bearer {self.access_token}'
        return connection(path=path, data=data, headers=headers, timeout=timeout)

    def refresh_access(self) -> None:
        """
        Fetch a new access token using a refresh token.

        Does not use make_request to avoid circular calls.

        Raises:
            MonzoAuthenticationError: On lack of refresh token
        """
        if not self.refresh_token:
            raise MonzoAuthenticationError('Unable to refresh without a refresh token')
        data = {
            'grant_type': 'refresh_token',
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'refresh_token': self.refresh_token,
        }
        conn = HttpIO(MONZO_API_URL)
        res = conn.post(path='/oauth2/token', data=data)
        self._populate_tokens(res)

    @property
    def access_token(self) -> str:
        """
        Property for access token.

        Returns:
            Access token if one exists, otherwise an empty string
        """
        return self._access_token or ''

    @property
    def access_token_expiry(self) -> int:
        """
        Property for access token expiry.

        Returns:
            Access token expiry as an epoch
        """
        return self._access_token_expiry or 0

    @access_token_expiry.setter
    def access_token_expiry(self, expires_in: int) -> None:
        """
        Setter for access token expiry property.

        Args:
            expires_in: number of seconds until the token expires
        """
        self._access_token_expiry = int(time()) + expires_in

    @property
    def authentication_url(self) -> str:
        """
        Create and return the authentication URL for the Monzo API.

        Returns:
            URL for Monzo authentication
        """
        return f'{MONZO_AUTH_URL}?client_id={self._client_id}&redirect_uri={self._redirect_url}' \
               f'&response_type=code&state={self.state_token}'

    @property
    def refresh_token(self) -> str:
        """
        Property for access refresh token.

        Returns:
            Access token refresh token
        """
        return self._refresh_token

    @property
    def state_token(self) -> str:
        """
        Generates or returns a previously generated state token.

        Returns:
            A state token used for authentication requests.
        """
        tmp_file_name = 'monzo'
        tmp_file_path = PurePath(gettempdir(), tmp_file_name)
        if not Path(tmp_file_path).is_file():
            with open(tmp_file_path, 'w') as fh:
                state_token = helpers.generate_random_token(length=64)
                fh.write(state_token)
                fh.flush()
        with open(tmp_file_path, 'r') as fh:
            state_token = fh.read()
        return state_token

    def _exchange_token(self, authorization_token: str) -> None:
        """
        Exchange an authorization code for an access token.

        Args
            authorization_token: Authorization token as received from Monzo
        """
        data = {
            'grant_type': 'authorization_code',
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'redirect_uri': self._redirect_url,
            'code': authorization_token,
        }
        res = self.make_request('/oauth2/token', authenticated=False, method='post', data=data)
        self._populate_tokens(res)

    def _populate_tokens(self, response: REQUEST_RESPONSE_TYPE) -> None:
        """
        Populates tokens after a token request.

        Args:
            response: Response from an auth request.
        """
        if response['code'] != 200:
            raise MonzoAuthenticationError('Could not fetch a valid access token')

        self._access_token = response['data']['access_token']
        self.access_token_expiry = response['data']['expires_in']
        if 'refresh_token' in response['data']:
            self._refresh_token = response['data']['refresh_token']

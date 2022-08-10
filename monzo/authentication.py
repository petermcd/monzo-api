"""Class to allow authentication on the Monzo API."""
import logging
import os
from pathlib import Path, PurePath
from tempfile import gettempdir
from time import time
from typing import List

from monzo import helpers
from monzo.exceptions import MonzoAuthenticationError, MonzoError
from monzo.handlers.storage import Storage
from monzo.httpio import DEFAULT_TIMEOUT, REQUEST_RESPONSE_TYPE, HttpIO

MONZO_AUTH_URL = 'https://auth.monzo.com'
MONZO_API_URL = 'https://api.monzo.com'


class Authentication(object):
    """
    Class to manage authentication.

    Class provides methods to authenticate to the Monzo API and to make relevant queries. An instantiated
    copy of this class is usually passed to each action
    """

    __slots__ = [
        '_access_token',
        '_access_token_expiry',
        '_client_id',
        '_client_secret',
        '_handlers',
        '_redirect_url',
        '_refresh_token',
    ]

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            redirect_url: str,
            access_token: str = '',
            access_token_expiry: int = 0,
            refresh_token: str = ''
    ):
        """
        Initialize Authentication.

        Args:
            client_id: Client ID generated at https://developers.monzo.com
            client_secret: Client Secret generated at https://developers.monzo.com
            redirect_url: Redirect URL for authentication
            access_token: Pre existing access token
            access_token_expiry: Token expiry as a unix timestamp
            refresh_token: Refresh token to renew access tokens
        """
        self._access_token: str = access_token
        self._access_token_expiry: int = access_token_expiry
        self._client_id: str = client_id
        self._client_secret: str = client_secret
        self._handlers: List[Storage] = []
        self._redirect_url: str = redirect_url
        self._refresh_token: str = refresh_token

    def authenticate(self, authorization_token: str, state_token: str) -> None:
        """
        Completes authentication once the authentication URL has been visited.

        Args:
            authorization_token: Authorization code provided by Monzo
            state_token: Pre agreed state token to validate against

        Raises:
            MonzoAuthenticationError On missing authorization token or mismatching state tokens
        """
        logging.debug('Attempting authentication')
        if not authorization_token:
            logging.debug('Authentication - Missing token')
            raise MonzoAuthenticationError('Code missing from response')
        if state_token != self.state_token:
            logging.debug('Authentication - state token mismatch')
            raise MonzoAuthenticationError('State tokens do not match')
        tmp_file_name = 'monzo'
        tmp_file_path = PurePath(gettempdir(), tmp_file_name)
        os.remove(tmp_file_path)
        self._exchange_token(authorization_token=authorization_token)

    def logout(self) -> None:
        """Invalidate the access token."""
        logging.debug('Invalidating token')
        self.make_request(path='/oauth2/logout', method='post')

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
        Make an API call to Monzo.

        Args:
            path: Path for the API call
            authenticated: True if authenticated request should be made otherwise False
            method: Method for the API call (DELETE, GET, POST, PUT)
            data: Dictionary of data to be posted as form data or URL parameters
            headers: Dictionary of headers for the request
            timeout: Timeout in seconds for the request

        Returns:
            Dictionary containing headers and data from query response
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
        elif method == 'patch':
            connection = conn.patch
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
            MonzoAuthenticationError: On lack of refresh token or failure to refresh a token
        """
        logging.debug('Fetching new token')
        if not self.refresh_token:
            logging.debug('Unable to fetch new token without a refresh token')
            raise MonzoAuthenticationError('Unable to refresh without a refresh token')
        data = {
            'grant_type': 'refresh_token',
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'refresh_token': self.refresh_token,
        }
        conn = HttpIO(MONZO_API_URL)
        try:
            res = conn.post(path='/oauth2/token', data=data)
            self._populate_tokens(res)
        except MonzoError as exc:
            logging.debug('Failed to fetch new token')
            raise MonzoAuthenticationError('Could not refresh the access token') from exc

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
        Generate or returns a previously generated state token.

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

        Raises:
            MonzoAuthenticationError On failure to create a token
        """
        logging.debug('Authentication - swapping authorization token for an access token')
        data = {
            'grant_type': 'authorization_code',
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'redirect_uri': self._redirect_url,
            'code': authorization_token,
        }
        try:
            res = self.make_request('/oauth2/token', authenticated=False, method='post', data=data)
            self._populate_tokens(res)
        except MonzoError as exc:
            logging.debug(f'Could not fetch access token {exc}')
            raise MonzoAuthenticationError('Could not fetch a valid access token') from exc

    def _populate_tokens(self, response: REQUEST_RESPONSE_TYPE) -> None:
        """
        Populate tokens after a token request.

        Args:
            response: Response from an auth request.
        """
        logging.debug('Populating tokens')
        self._access_token = response['data']['access_token']
        self.access_token_expiry = response['data']['expires_in']
        self._refresh_token = ''
        if 'refresh_token' in response['data']:
            self._refresh_token = response['data']['refresh_token']

        for handler in self._handlers:
            handler.store(
                access_token=self._access_token,
                client_id=self._client_id,
                client_secret=self._client_secret,
                expiry=self._access_token_expiry,
                refresh_token=self._refresh_token
            )

    def register_callback_handler(self, handler: Storage) -> None:
        """
        Register a new callback handler for handling new token details.

        Args:
            handler: Credential handler implementing Storage
        """
        logging.debug('Registered a new callback handler')
        self._handlers.append(handler)

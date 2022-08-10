"""Helper functions and classes for testing."""
from datetime import datetime, timedelta
from json import loads
from typing import Dict, Union

from monzo.handlers.storage import Storage


def load_data(path: str, filename: str):
    """
    Load the content and prepare the output as HttpIO would provide.

    Args:
        path: The path to the file to load
        filename: The filename to load

    Returns:
        JSON Content
    """
    with open(f'tests/{path}/{filename}.json') as fh:
        content = fh.read()
    return loads(content)


class Handler(Storage):
    """Class to use as a handler for testing."""

    __slots__ = (
        '_access_token',
        '_client_id',
        '_client_secret',
        '_expiry',
        '_refresh_token'
    )

    def __init__(self):
        """Initialise Handler."""
        expiry = int((datetime.now() + timedelta(days=1)).timestamp())

        self._access_token = 'abc123'
        self._client_id = 'cde456'
        self._client_secret = 'fgh789'
        self._expiry = expiry
        self._refresh_token = 'ijk012'

    def store(
        self,
        access_token: str,
        client_id: str,
        client_secret: str,
        expiry: int,
        refresh_token: str = ''
    ) -> None:
        """
        Store the Monzo credentials.

        Args:
            access_token: New access token
            client_id: Monzo client ID
            client_secret: Monzo client secret
            expiry: Access token expiry as a unix timestamp
            refresh_token: Refresh token that can be used to renew an access token
        """
        self._access_token = access_token
        self._client_id = client_id
        self._client_secret = client_secret
        self._expiry = expiry
        self._refresh_token = refresh_token

    def fetch(self) -> Dict[str, Union[int, str]]:
        """
        Fetch Monzo credentials previously stored.

        Returns:
            Dictionary containing access token, expiry and refresh token
        """
        return {
            'access_token': self._access_token,
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'expiry': self._expiry,
            'refresh_token': self._refresh_token
        }

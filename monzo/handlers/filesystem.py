"""Class to store credentials on the file system."""
from json import dumps, loads
from typing import Dict, Union

from monzo.handlers.storage import Storage


class FileSystem(Storage):
    """Class that will store credentials on the file system."""

    __slots__ = ['_file']

    def __init__(self, file: str):
        """
        Initialize FileSystem.

        Args:
            file: THe full path (including filename) to the storage file
        """
        self._file = file

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
        content = {
            'access_token': access_token,
            'client_id': client_id,
            'client_secret': client_secret,
            'expiry': expiry,
            'refresh_token': refresh_token
        }
        with open(self._file, 'w') as handler:
            handler.write(dumps(content))

    def fetch(self) -> Dict[str, Union[int, str]]:
        """
        Fetch Monzo credentials previously stored.

        Returns:
            Dictionary containing access token, expiry and refresh token
        """
        try:
            with open(self._file, 'r') as handler:
                content = loads(handler.read())
        except FileNotFoundError:
            content = {}

        return content

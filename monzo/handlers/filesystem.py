"""Class to store credentials on the file system."""

import os
from json import dumps, loads
from typing import Dict, Union

from monzo.handlers.storage import Storage


class FileSystem(Storage):
    """Class that will store credentials on the file system."""

    __slots__ = ["_file"]

    def __init__(self, file: str):
        """
        Initialize FileSystem.

        Args:
            file: THe full path (including filename) to the storage file
        """
        self._file = file

    def fetch(self) -> Dict[str, Union[int, str]]:
        """
        Fetch Monzo credentials previously stored.

        Returns:
            Dictionary containing access token, expiry and refresh token
        """
        try:
            with open(self._file, "r") as handler:
                content = loads(handler.read())
        except FileNotFoundError:
            content = {}

        return content

    def store(
        self,
        access_token: str,
        expiry: int,
        refresh_token: str = "",
    ) -> None:
        """
        Store the Monzo credentials.

        Args:
            access_token: New access token
            expiry: Access token expiry as a unix timestamp
            refresh_token: Refresh token that can be used to renew an access token
        """
        content = {
            "access_token": access_token,
            "expiry": expiry,
            "refresh_token": refresh_token,
        }
        fd = os.open(self._file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as handler:
            handler.write(dumps(content))
        os.chmod(self._file, 0o600)

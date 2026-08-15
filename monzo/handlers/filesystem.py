"""Class to store credentials on the file system."""

import os
from json import dumps, loads

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

    def fetch(self) -> dict[str, int | str]:
        """
        Fetch Monzo credentials previously stored.

        Returns:
            Dictionary containing access token, expiry and refresh token
        """
        try:
            with open(self._file, mode="r") as handler:
                content = loads(handler.read())
        except FileNotFoundError:
            content: dict[str, int | str] = {}

        return content

    def store(
        self,
        access_token: str,
        client_id: str,
        client_secret: str,
        expiry: int,
        refresh_token: str = "",
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
        content: dict[str, int | str] = {
            "access_token": access_token,
            "client_id": client_id,
            "client_secret": client_secret,
            "expiry": expiry,
            "refresh_token": refresh_token,
        }
        fd: int = os.open(path=self._file, flags=os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode=0o600)
        with os.fdopen(fd, mode="w") as handler:
            handler.write(dumps(obj=content))
        os.chmod(path=self._file, mode=0o600)

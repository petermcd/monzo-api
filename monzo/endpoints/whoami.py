"""Class to manage the whoami request."""
from __future__ import annotations

from monzo.authentication import Authentication
from monzo.endpoints.monzo import Monzo


class WhoAmI(Monzo):
    """
    Class to manage WhoAmI.

    Class provides access to the whoami endpoint. This is usually used to test connectivity to the
    API
    """

    __slots__ = ['_authenticated', '_client_id', '_user_id']

    def __init__(self, auth: Authentication, authenticated: bool, client_id: str, user_id: str):
        """
        Initialize WhoAmI.

        Args:
            auth: Monzo authentication object
            authenticated: True if user is authenticated on Monzo, otherwise False
            client_id: API client ID for the user
            user_id: API user ID for the user
        """
        self._authenticated = authenticated
        self._client_id = client_id
        self._user_id = user_id
        super().__init__(auth=auth)

    @property
    def authenticated(self) -> bool:
        """
        Property for authenticated.

        Returns:
            True if authenticated otherwise False
        """
        return self._authenticated

    @property
    def client_id(self) -> str:
        """
        Property for client_id.

        Returns:
            Client ID for the user making the request
        """
        return self._client_id

    @property
    def user_id(self) -> str:
        """
        Property for user_id.

        Returns:
            User ID for the user making the request
        """
        return self._user_id

    @classmethod
    def fetch(cls, auth: Authentication) -> WhoAmI:
        """
        Implement and instantiates a WhoAmI object.

        Args:
             auth: Monzo authentication object

        Returns:
            Instantiated WhoAmI object
        """
        res = auth.make_request(path='/ping/whoami')
        return cls(
            auth=auth,
            authenticated=res['data']['authenticated'],
            client_id=res['data']['client_id'],
            user_id=res['data']['user_id'],
        )

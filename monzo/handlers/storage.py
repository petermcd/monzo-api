"""Abstract class for credential storage."""
from abc import ABC, abstractmethod


class Storage(ABC):
    """
    Abstract class that must be implemented if setting up a credential listener.

    Abstract class specifying the methods that need to be implemented to make use of
    the credential listener functionality.
    """

    @abstractmethod
    def store(
        self,
        access_token: str,
        client_id: str,
        client_secret: str,
        expiry: int,
        refresh_token: str = ''
    ) -> None:
        """
        Abstract method that needs to be implemented to receive new credentials from Monzo.

        Args:
            access_token: New access token
            client_id: Monzo client ID
            client_secret: Monzo client secret
            expiry: Access token expiry as a unix timestamp
            refresh_token: Refresh token that can be used to renew an access token
        """
        pass

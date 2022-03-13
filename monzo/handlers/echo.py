"""Class to echo credentials."""
from monzo.handlers.storage import Storage


class Echo(Storage):
    """Class that will echo out credentials."""

    def store(
        self,
        access_token: str,
        client_id: str,
        client_secret: str,
        expiry: int,
        refresh_token: str = ''
    ) -> None:
        """
        Echo the Monzo credentials.

        Args:
            access_token: New access token
            client_id: Monzo client ID
            client_secret: Monzo client secret
            expiry: Access token expiry as a unix timestamp
            refresh_token: Refresh token that can be used to renew an access token
        """
        print(f"client_id = '{client_id}'")
        print(f"client_secret = '{client_secret}'")
        print(f"access_token = '{access_token}'")
        print(f'expiry = {expiry}')
        print(f"refresh_token = '{refresh_token}'")

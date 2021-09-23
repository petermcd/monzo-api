from monzo.handlers.storage import Storage


class Echo(Storage):
    """
    Class that will echo out credentials.
    """
    def store(self, access_token: str, expiry: int, refresh_token: str = '') -> None:
        """
        Method to echo the Monzo credentials.

        Args:
            access_token: New access token
            expiry: Access token expiry as a unix timestamp
            refresh_token: Refresh token that can be used to renew an access token
        """
        print(f"access_token = '{access_token}'")
        print(f'expiry = {expiry}')
        print(f"refresh_token = '{refresh_token}'")

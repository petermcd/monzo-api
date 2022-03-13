"""Example code to authenticate against the Monzo API."""
from monzo.authentication import Authentication

client_id = ''  # Client ID obtained when creating Monzo client
client_secret = ''  # Client secret obtained when creating Monzo client
redirect_uri = 'http://127.0.0.1/monzo'  # URL requests via Monzo will be redirected in a browser

monzo = Authentication(client_id=client_id, client_secret=client_secret, redirect_url=redirect_uri)

# The user should visit this url
print(monzo.authentication_url)

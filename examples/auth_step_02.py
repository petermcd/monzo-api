"""Code to handle the seconds stage of authentication."""
from monzo.authentication import Authentication
from monzo.exceptions import MonzoAuthenticationError, MonzoServerError

client_id = ''  # Client ID obtained when creating Monzo client
client_secret = ''  # Client secret obtained when creating Monzo client
redirect_uri = 'http://127.0.0.1/monzo'  # URL requests via Monzo will be redirected in a browser
state = ''  # State random string created when creating the Monzo URL (generated in step 1 and appended to the URL)
code = ''  # Authorization code from Monzo (this will be in the redirected URL after clicking the link from step 1)

monzo = Authentication(client_id=client_id, client_secret=client_secret, redirect_url=redirect_uri)
try:
    monzo.authenticate(authorization_token=code, state_token=state)
except MonzoAuthenticationError:
    print('State code does not match')
    exit(1)
except MonzoServerError:
    print('Monzo Server Error')
    exit(1)

# The following 3 items should be stored for future requests
print(f"access_token = '{monzo.access_token}'")
print(f'expiry = {monzo.access_token_expiry}')
print(f"refresh_token = '{monzo.refresh_token}'")

# Now authorise access in the Monzo app

"""Example code for showing who is logged into the Monzo API."""
from monzo.authentication import Authentication
from monzo.endpoints.whoami import WhoAmI
from monzo.exceptions import MonzoError

client_id = ''  # Client ID obtained when creating Monzo client
client_secret = ''  # Client secret obtained when creating Monzo client
redirect_uri = 'http://127.0.0.1/monzo'  # URL requests via Monzo will be redirected in a browser
access_token = ''  # access_token retrieved in step 2
expiry = 0  # access_token_expiry retrieved in step 2
refresh_token = ''  # refresh_token retrieved in step 2

monzo = Authentication(
    client_id=client_id,
    client_secret=client_secret,
    redirect_url=redirect_uri,
    access_token=access_token,
    access_token_expiry=expiry,
    refresh_token=refresh_token
)

try:
    who = WhoAmI.fetch(monzo)
    print(who.user_id)
    print(who.client_id)
    print(who.authenticated)
except MonzoError:
    print('failed to fetch whoami endpoint')

"""Example code to fetch accounts."""
from monzo.authentication import Authentication
from monzo.endpoints.account import Account
from monzo.exceptions import MonzoError

client_id = ''  # Client ID obtained when creating a Monzo client
client_secret = ''  # Client secret obtained when creating a Monzo client
redirect_uri = 'http://127.0.0.1/monzo'  # URL requests via Monzo will be redirected in a browser
access_token = ''  # access_token retrieved in step 2
expiry = 0  # access_token_expiry retrieved in step 2
refresh_token = ''  # refresh_token retrieved in step 2\

monzo = Authentication(
    client_id=client_id,
    client_secret=client_secret,
    redirect_url=redirect_uri,
    access_token=access_token,
    access_token_expiry=expiry,
    refresh_token=refresh_token
)

try:
    accounts = Account.fetch(monzo)
    for account in accounts:
        print(
            f'Account ID: {account.account_type()} - '
            f'Balance: {account.balance.total_balance if account.balance else 0}'
        )
except MonzoError:
    print('Failed to retrieve accounts')

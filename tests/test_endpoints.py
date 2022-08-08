"""Tests for endpoints."""
import pytest

from monzo import authentication
from monzo.endpoints.account import Account
from monzo.endpoints.balance import Balance
from monzo.endpoints.whoami import WhoAmI
from tests.helpers import Handler, load_data


class TestEndPoints(object):
    """Tests for the endpoints."""

    @pytest.mark.parametrize(
        'mock_file,expected_account_id,expected_account_type,expected_description',
        [
            ('Accounts', 'acc_123ABC', 'Current Account', 'user_123ABC'),
            ('Accounts_Flex_Type', 'acc_123ABC', 'Flex', 'monzoflex_123ABC'),
            ('Accounts_Flex_Loan_Type', 'acc_123ABC', 'Loan (Flex)', 'monzoflexbackingloan_123ABC'),
            ('Accounts_Loan_Type', 'acc_123ABC', 'Loan', 'loan_123ABC'),
            ('Accounts_Unknown_Type', 'acc_123ABC', 'UNKNOWN', 'random_123ABC'),
        ],
    )
    def test_account(
            self,
            mock_file: str,
            expected_account_id: str,
            expected_account_type: str,
            expected_description: str,
            mocker
    ):
        """
        Test Account endpoint.

        Args:
            mock_file: File to fetch the mock response from
            expected_account_id: Expected account ID
            expected_account_type: Expected account type
            expected_description: str: Expected account description
        """
        mocker.patch.object(
            authentication.HttpIO,
            'get',
            return_value=load_data(path='mock_responses', filename=mock_file)
        )

        handler = Handler()

        credentials = handler.fetch()

        auth = authentication.Authentication(
            client_id=credentials['client_id'],
            client_secret=credentials['client_secret'],
            redirect_url='',
            access_token=credentials['access_token'],
            access_token_expiry=credentials['expiry'],
            refresh_token=credentials['refresh_token'],
        )

        auth.register_callback_handler(handler)

        accounts = Account.fetch(auth=auth)

        assert len(accounts) == 1
        assert accounts[0].account_id == expected_account_id
        assert accounts[0].account_type() == expected_account_type
        assert accounts[0].description == expected_description

    @pytest.mark.parametrize(
        'mock_file,expected_balance,expected_currency,expected_spend_today,expected_total_balance',
        [
            ('Balance', 40000, 'GBP', -3000, 60000),
        ],
    )
    def test_balance(
            self,
            mock_file: str,
            expected_balance: int,
            expected_currency: str,
            expected_spend_today: int,
            expected_total_balance: int,
            mocker
    ):
        """
        Test Balance endpoint.

        Args:
            mock_file: File to fetch the mock response from
            expected_balance: Expected account balance
            expected_currency: Expected account currency
            expected_spend_today: Expected account spend today
            expected_total_balance: Expected account balance total
        """
        mocker.patch.object(
            authentication.HttpIO,
            'get',
            return_value=load_data(path='mock_responses', filename=mock_file)
        )

        handler = Handler()

        credentials = handler.fetch()

        auth = authentication.Authentication(
            client_id=credentials['client_id'],
            client_secret=credentials['client_secret'],
            redirect_url='',
            access_token=credentials['access_token'],
            access_token_expiry=credentials['expiry'],
            refresh_token=credentials['refresh_token'],
        )

        auth.register_callback_handler(handler)

        balance = Balance.fetch(auth=auth, account_id='123ABC')

        assert balance.balance == expected_balance
        assert balance.total_balance == expected_total_balance
        assert balance.currency == expected_currency
        assert balance.spend_today == expected_spend_today

    @pytest.mark.parametrize(
        'mock_file, expected_authenticated, expected_client_id, expected_user_id',
        [
            ('WhoAmI', True, 'client123', 'user123')
        ],
    )
    def test_whoami(
            self,
            mock_file: str,
            expected_authenticated: str,
            expected_client_id: str,
            expected_user_id: str,
            mocker
    ):
        """
        Test WhoAmI endpoint.

        Args:
            mock_file: File to fetch the mock response from
            expected_authenticated: Expected value for authenticated
            expected_client_id: expected client id
            expected_user_id expected user id
            mocker: mocker fixture
        """
        mocker.patch.object(
            authentication.HttpIO,
            'get',
            return_value=load_data(path='mock_responses', filename=mock_file)
        )

        handler = Handler()

        credentials = handler.fetch()

        auth = authentication.Authentication(
            client_id=credentials['client_id'],
            client_secret=credentials['client_secret'],
            redirect_url='',
            access_token=credentials['access_token'],
            access_token_expiry=credentials['expiry'],
            refresh_token=credentials['refresh_token'],
        )

        auth.register_callback_handler(handler)

        whoami = WhoAmI.fetch(auth=auth)

        assert whoami.authenticated == expected_authenticated
        assert whoami.client_id == expected_client_id
        assert whoami.user_id == expected_user_id

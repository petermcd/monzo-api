"""Tests for endpoints."""
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import pytest

from monzo import authentication
from monzo.endpoints.account import Account
from monzo.endpoints.balance import Balance
from monzo.endpoints.receipt import MERCHANT_TYPE, PAYMENT_TYPE, TAX_TYPE, Receipt
from monzo.endpoints.transaction import Transaction
from monzo.endpoints.webhooks import Webhook
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
        'mock_file,expected_external_id,expected_receipt_currency,expected_receipt_merchant,expected_receipt_payments,'
        + 'expected_receipt_taxes,expected_receipt_total,expected_transaction_id,',
        [
            (
                'Receipt',
                '123ABC',
                'GBP',
                {},
                [],
                [],
                665,
                'tx_123ABC'
            ),
        ],
    )
    def test_create_receipt(
            self,
            mock_file: str,
            expected_external_id: str,
            expected_receipt_currency: str,
            expected_receipt_merchant: MERCHANT_TYPE,
            expected_receipt_payments: List[PAYMENT_TYPE],
            expected_receipt_taxes: List[TAX_TYPE],
            expected_receipt_total: int,
            expected_transaction_id: str,
            mocker
    ):
        """
        Test Receipt endpoint.

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

        receipt = Receipt.fetch(auth=auth, external_id='123ABC')

        assert len(receipt) == 1
        assert len(receipt[0].receipt_items) == 1

        assert receipt[0].external_id == expected_external_id
        assert receipt[0].receipt_currency == expected_receipt_currency
        assert receipt[0].receipt_merchant == expected_receipt_merchant
        assert receipt[0].receipt_payments == expected_receipt_payments
        assert receipt[0].receipt_taxes == expected_receipt_taxes
        assert receipt[0].receipt_total == expected_receipt_total
        assert receipt[0].transaction_id == expected_transaction_id

    @pytest.mark.parametrize(
        'mock_file,multi,expected_account_id,expected_amount,expected_amount_is_pending,expected_atm_fees_detailed,'
        + 'expected_attachments,expected_can_add_to_tab,expected_can_be_excluded_from_breakdown,'
        + 'expected_can_be_made_subscription,expected_can_match_transactions_in_categorization,'
        + 'expected_can_split_the_bill,expected_categories,expected_category,expected_counterparty,expected_created,'
        + 'expected_currency,expected_dedupe_id,expected_decline_reason,expected_description,expected_fees,'
        + 'expected_include_in_spending,expected_international,expected_is_load,expected_labels,expected_local_amount,'
        + 'expected_local_currency,expected_merchant,expected_metadata,expected_notes,expected_originator,'
        + 'expected_scheme,expected_settled,expected_transaction_id,expected_updated,expected_user_id',
        [
            (
                'Transaction',
                True,
                'acc_123ABC',
                -2775,
                False,
                None,
                None,
                True,
                True,
                True,
                True,
                True,
                {
                    'bills': -2775
                },
                'bills',
                {},
                datetime(2022, 8, 9, 14, 15, 1),
                'GBP',
                '123ABC',
                '',
                'Company                   INTERNET      GBR',
                {},
                True,
                None,
                False,
                None,
                -2775,
                'GBP',
                'merch_123ABC',
                {
                    "coin_jar_transaction": "tx_123ABC",
                    "ledger_insertion_id": "entryset_123ABC",
                    "mastercard_approval_type": "full",
                    "mastercard_auth_message_id": "mcauthmsg_123ABC",
                    "mastercard_card_id": "mccard_123ABC",
                    "mastercard_lifecycle_id": "mclifecycle_123ABC", "mcc": "1234"
                },
                '',
                False,
                'mastercard',
                datetime(2022, 8, 10, 0, 30, 40),
                'tx_123ABC1',
                datetime(2022, 8, 10, 0, 30, 40),
                'user_ABC123',
            ),
        ],
    )
    def test_transaction(
            self,
            mock_file: str,
            multi: bool,
            expected_account_id: str,
            expected_amount: int,
            expected_amount_is_pending: bool,
            expected_atm_fees_detailed: str,
            expected_attachments: str,
            expected_can_add_to_tab: bool,
            expected_can_be_excluded_from_breakdown: bool,
            expected_can_be_made_subscription: bool,
            expected_can_match_transactions_in_categorization: bool,
            expected_can_split_the_bill: bool,
            expected_categories: Dict[str, Union[int, str]],
            expected_category: str,
            expected_counterparty: str,
            expected_created: datetime,
            expected_currency: str,
            expected_dedupe_id: str,
            expected_decline_reason: str,
            expected_description: str,
            expected_fees: Dict[str, Any],
            expected_include_in_spending: bool,
            expected_international: Optional[str],
            expected_is_load: bool,
            expected_labels: str,
            expected_local_amount: int,
            expected_local_currency: str,
            expected_merchant: str,
            expected_metadata: Dict[str, str],
            expected_notes: str,
            expected_originator: bool,
            expected_scheme: str,
            expected_settled: Optional[datetime],
            expected_transaction_id: str,
            expected_updated: Optional[datetime],
            expected_user_id: bool,
            mocker
    ):
        """
        Test Transaction endpoint.

        Args:
            mock_file: File to fetch the mock response from
            multi: True if using fetch False if using fetch_single
            expected_account_id: Expected account ID
            expected_amount: Expected amount
            expected_amount_is_pending: Expected amount is pending
            expected_atm_fees_detailed: Expected ATM fee details
            expected_attachments: Expected attachment
            expected_can_add_to_tab: Expected can add to tab
            expected_can_be_excluded_from_breakdown: Expected can be excluded from breakdown
            expected_can_be_made_subscription: Expected can be made a subscription
            expected_can_match_transactions_in_categorization: Expected can match transaction in categorization
            expected_can_split_the_bill: Expected can split bill
            expected_categories: Expected categories
            expected_category: Expected category
            expected_counterparty: Expected counterparty
            expected_created: Expected created
            expected_currency: Expected currency
            expected_dedupe_id: Expected dedupe ID
            expected_decline_reason: Expected decline reason
            expected_description: Expected description
            expected_fees: Expected fees
            expected_include_in_spending: Expected include in spending
            expected_international: Expected international
            expected_is_load: Expected is load
            expected_labels: expected labels
            expected_local_amount: expected local amount
            expected_local_currency: expected currency
            expected_merchant: expected merchant
            expected_metadata: Expected metadata
            expected_notes: Expected notes
            expected_originator: Expected originator
            expected_scheme: Expected scheme
            expected_settled: Expected settled
            expected_transaction_id: Expected transaction ID
            expected_updated: Expected updated
            expected_user_id: Expected user ID
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

        if multi:
            transactions = Transaction.fetch(auth=auth, account_id=expected_account_id, since=datetime.now())
            assert len(transactions) == 1
            transaction = transactions[0]
        else:
            transaction = Transaction.fetch_single(auth=auth, transaction_id=expected_transaction_id)

        assert transaction.account_id == expected_account_id
        assert transaction.amount == expected_amount
        assert transaction.amount_is_pending == expected_amount_is_pending
        assert transaction.atm_fees_detailed == expected_atm_fees_detailed
        assert transaction.attachments == expected_attachments
        assert transaction.can_add_to_tab == expected_can_add_to_tab
        assert transaction.can_be_excluded_from_breakdown == expected_can_be_excluded_from_breakdown
        assert transaction.can_be_made_subscription == expected_can_be_made_subscription
        assert transaction.can_match_transactions_in_categorization == expected_can_match_transactions_in_categorization
        assert transaction.can_split_the_bill == expected_can_split_the_bill
        assert transaction.categories == expected_categories
        assert transaction.category == expected_category
        assert transaction.counterparty == expected_counterparty
        assert transaction.created == expected_created
        assert transaction.currency == expected_currency
        assert transaction.dedupe_id == expected_dedupe_id
        assert transaction.decline_reason == expected_decline_reason
        assert transaction.description == expected_description
        assert transaction.fees == expected_fees
        assert transaction.include_in_spending == expected_include_in_spending
        assert transaction.international == expected_international
        assert transaction.is_load == expected_is_load
        assert transaction.labels == expected_labels
        assert transaction.local_amount == expected_local_amount
        assert transaction.local_currency == expected_local_currency
        assert transaction.merchant == expected_merchant
        assert transaction.metadata == expected_metadata
        assert transaction.notes == expected_notes
        assert transaction.originator == expected_originator
        assert transaction.scheme == expected_scheme
        assert transaction.settled == expected_settled
        assert transaction.transaction_id == expected_transaction_id
        assert transaction.updated == expected_updated
        assert transaction.user_id == expected_user_id

    @pytest.mark.parametrize(
        'mock_file,expected_account_id,expected_url,expected_webhook_id,expected_count',
        [
            ('WebhooksNone', 'acc_123ABC', None, None, 0),
            ('WebhooksOne', 'acc_123ABC', 'https://some-url.co.uk', 'webhook_123ABC', 1),
        ],
    )
    def test_webhooks(
            self,
            mock_file: str,
            expected_account_id: str,
            expected_url: Optional[str],
            expected_webhook_id: Optional[str],
            expected_count: int,
            mocker
    ):
        """
        Test Webhook endpoint.

        Args:
            mock_file: File to fetch the mock response from
            expected_account_id: Expected account ID
            expected_url: Expected URL
            expected_webhook_id: Expected webhook ID
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

        webhook = Webhook.fetch(auth=auth, account_id=expected_account_id)

        assert len(webhook) == expected_count

        if webhook:
            assert webhook[0].account_id == expected_account_id
            assert webhook[0].webhook_id == expected_webhook_id
            assert webhook[0].url == expected_url

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

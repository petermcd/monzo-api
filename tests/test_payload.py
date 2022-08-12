"""Tests for HttpIO."""
from json import dumps
from typing import Dict

import pytest

from monzo import authentication
from monzo.endpoints.account import Account
from monzo.endpoints.balance import Balance
from monzo.endpoints.feed_item import FeedItem
from monzo.endpoints.receipt import Receipt, ReceiptItem
from monzo.endpoints.transaction import Transaction
from monzo.endpoints.webhooks import Webhook
from monzo.endpoints.whoami import WhoAmI
from tests.helpers import Handler, load_data


class TestHttpIO(object):
    """Tests for the HttpIO class."""

    @pytest.mark.parametrize("endpoint,http_method,data_filename,response_filename,extra_data", [
        (
            FeedItem,
            'post',
            'FeedItem',
            'FeedItem',
            {
                'account_id': 'acc_123ABC',
                'feed_type': 'basic',
                'params': {'title': 'My Alert', 'image_url': 'https://some-url.co.uk/image.jpg'},
            }
        ),
        (
            Webhook,
            'post',
            'WebhooksCreate',
            'WebhooksCreated',
            {
                'account_id': 'acc_123ABC',
                "url": 'https://some-url.co.uk',
            },
        )
    ])
    def test_create_payload(
            self,
            endpoint,
            http_method: str,
            data_filename: str,
            response_filename: str,
            extra_data: Dict[str, str],
            mocker
    ):
        """
        Test the payload httpio would send.

        Args:
            endpoint: Endpoint object being tested
            http_method: HTTP method the request uses
            data_filename: Filename of the request data
            response_filename: Filename of the response data
            extra_data: Extra parameters for the fetch request
        """
        httpio_capture = mocker.patch.object(
            authentication.HttpIO,
            http_method,
            return_value=load_data(path='mock_responses', filename=response_filename)
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

        endpoint.create(auth=auth, **extra_data)

        expected_data = load_data(path='mock_payloads', filename=data_filename)

        httpio_capture.assert_called_with(
            data=expected_data['data'],
            headers=expected_data['headers'],
            path=expected_data['path'],
            timeout=expected_data['timeout']
        )

    @pytest.mark.parametrize("endpoint,http_method,data_filename,response_filename,webhook_id", [
        (
            Webhook,
            'delete',
            'WebhooksDelete',
            'WebhooksDeleted',
            'webhook_123ABC',
        )
    ])
    def test_delete_webhook_payload(
            self,
            endpoint,
            http_method: str,
            data_filename: str,
            response_filename: str,
            webhook_id: str,
            mocker
    ):
        """
        Test the payload httpio would send.

        Args:
            endpoint: Endpoint object being tested
            http_method: HTTP method the request uses
            data_filename: Filename of the request data
            response_filename: Filename of the response data
            webhook_id: ID of the webhook to delete
        """
        httpio_capture = mocker.patch.object(
            authentication.HttpIO,
            http_method,
            return_value=load_data(path='mock_responses', filename=response_filename)
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

        webhook = Webhook(auth=auth, account_id='acc_123ABC', url='https://some-url.co.uk', webhook_id=webhook_id)

        endpoint.delete(webhook=webhook)

        expected_data = load_data(path='mock_payloads', filename=data_filename)

        httpio_capture.assert_called_with(
            data=expected_data['data'],
            headers=expected_data['headers'],
            path=expected_data['path'],
            timeout=expected_data['timeout']
        )

    @pytest.mark.parametrize("endpoint,http_method,data_filename,response_filename,extra_data", [
        (Account, 'get', 'Accounts', 'Accounts', {}),
        (Balance, 'get', 'Balance', 'Balance', {'account_id': 'acc_123ABC'}),
        (Transaction, 'get', 'Transaction', 'Transaction', {'account_id': 'acc_123ABC'}),
        (Webhook, 'get', 'Webhooks', 'WebhooksNone', {'account_id': 'acc_123ABC'}),
        (Webhook, 'get', 'Webhooks', 'WebhooksOne', {'account_id': 'acc_123ABC'}),
        (WhoAmI, 'get', 'WhoAmI', 'WhoAmI', {}),
    ])
    def test_fetch_payload(
            self,
            endpoint,
            http_method: str,
            data_filename: str,
            response_filename: str,
            extra_data: Dict[str, str],
            mocker
    ):
        """
        Test the payload httpio would send.

        Args:
            endpoint: Endpoint object being tested
            http_method: HTTP method the request uses
            data_filename: Filename of the request data
            response_filename: Filename of the response data
            extra_data: Extra parameters for the fetch request
        """
        httpio_capture = mocker.patch.object(
            authentication.HttpIO,
            http_method,
            return_value=load_data(path='mock_responses', filename=response_filename)
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

        endpoint.fetch(auth=auth, **extra_data)

        expected_data = load_data(path='mock_payloads', filename=data_filename)

        httpio_capture.assert_called_with(
            data=expected_data['data'],
            headers=expected_data['headers'],
            path=expected_data['path'],
            timeout=expected_data['timeout']
        )

    @pytest.mark.parametrize("endpoint,http_method,data_filename,response_filename,extra_data", [
        (Transaction, 'patch', 'Annotate', 'Annotate', {'key': 'notes', 'value': 'Test Note'}),
    ])
    def test_patch_annotate_payload(
            self,
            endpoint,
            http_method: str,
            data_filename: str,
            response_filename: str,
            extra_data: Dict[str, str],
            mocker
    ):
        """
        Test the payload HttpIO would send for patching annotate.

        Args:
            endpoint: Endpoint object being tested
            http_method: HTTP method the request uses
            data_filename: Filename of the request data
            response_filename: Filename of the response data
            extra_data: Extra parameters for the fetch request
        """
        httpio_capture = mocker.patch.object(
            authentication.HttpIO,
            http_method,
            return_value=load_data(path='mock_responses', filename=response_filename)
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

        transaction = Transaction(
            auth=auth,
            transaction_data=load_data(path='mock_responses', filename='Transaction')['data']['transactions'][0]
        )
        transaction.annotate(**extra_data)

        expected_data = load_data(path='mock_payloads', filename=data_filename)

        httpio_capture.assert_called_with(
            data=expected_data['data'],
            headers=expected_data['headers'],
            path=expected_data['path'],
            timeout=expected_data['timeout']
        )

    @pytest.mark.parametrize(
        'endpoint,http_method,data_filename,response_filename,transaction_id,external_id,transaction_total,'
        + 'transaction_currency,extra_data', [
            (
                Receipt,
                'put',
                'ReceiptCreate',
                'ReceiptCreated',
                'tx_123ABC',
                '123ABC',
                665,
                'GBP',
                {
                    'items': [
                        ReceiptItem(description='testing receipts', amount=665, currency='GBP', quantity=1),
                    ],
                },
            ),
        ]
    )
    def test_put_receipt_payload(
            self,
            endpoint,
            http_method: str,
            data_filename: str,
            response_filename: str,
            transaction_id: str,
            external_id: str,
            transaction_total: int,
            transaction_currency: str,
            extra_data: Dict[str, str],
            mocker
    ):
        """
        Test the payload HttpIO would send for patching annotate.

        Args:
            endpoint: Endpoint object being tested
            http_method: HTTP method the request uses
            data_filename: Filename of the request data
            response_filename: Filename of the response data
            extra_data: Extra parameters for the fetch request
        """
        httpio_capture = mocker.patch.object(
            authentication.HttpIO,
            http_method,
            return_value=load_data(path='mock_responses', filename=response_filename)
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

        receipt = Receipt(
            auth=auth,
            transaction_id=transaction_id,
            external_id=external_id,
            transaction_total=transaction_total,
            transaction_currency=transaction_currency,
            **extra_data,
        )
        receipt.create(auth=auth, receipt=receipt)

        expected_data = load_data(path='mock_payloads', filename=data_filename)

        httpio_capture.assert_called_with(
            data=dumps(expected_data['data']),
            headers=expected_data['headers'],
            path=expected_data['path'],
            timeout=expected_data['timeout']
        )

"""Tests for HttpIO."""
from typing import Dict

import pytest

from monzo import authentication
from monzo.endpoints.account import Account
from monzo.endpoints.balance import Balance
from monzo.endpoints.feed_item import FeedItem
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
                'params': {'title': 'My Alert', 'image_url': 'https://some-url.co.uk/image.jpg'}
            }
        ),
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
            data_filename: Filename of the request data
            http_method: HTTP method the request uses
            response_filename: Filename of the response data
            extra_data: Extra parameters for the fetch request
        """
        httpio_get = mocker.patch.object(
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

        httpio_get.assert_called_with(
            data=expected_data['data'],
            headers=expected_data['headers'],
            path=expected_data['path'],
            timeout=expected_data['timeout']
        )

    @pytest.mark.parametrize("endpoint,http_method,data_filename,response_filename,extra_data", [
        (Account, 'get', 'Accounts', 'Accounts', {}),
        (Balance, 'get', 'Balance', 'Balance', {'account_id': 'acc_123ABC'}),
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
            data_filename: Filename of the request data
            http_method: HTTP method the request uses
            response_filename: Filename of the response data
            extra_data: Extra parameters for the fetch request
        """
        httpio_get = mocker.patch.object(
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

        httpio_get.assert_called_with(
            data=expected_data['data'],
            headers=expected_data['headers'],
            path=expected_data['path'],
            timeout=expected_data['timeout']
        )

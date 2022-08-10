"""Tests for authentication."""
from monzo import authentication
from tests.helpers import Handler, load_data


class TestEndPoints(object):
    """Tests for the authentication."""

    def test_logout(self, mocker):
        """
        Test the logout functionality.

        Args:
            mocker: mocker fixture
        """
        httpio_capture = mocker.patch.object(
            authentication.HttpIO,
            'post',
            return_value=load_data(path='mock_responses', filename='Logout')
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

        auth.logout()

        expected_data = load_data(path='mock_payloads', filename='Logout')

        httpio_capture.assert_called_with(
            data=expected_data['data'],
            headers=expected_data['headers'],
            path=expected_data['path'],
            timeout=expected_data['timeout']
        )

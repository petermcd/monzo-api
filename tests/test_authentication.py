"""Tests for authentication."""
from tests.helpers import httpio, load_data


class TestEndPoints(object):
    """Tests for the authentication."""

    def test_logout(self, mocker):
        """
        Test the logout functionality.

        Args:
            mocker: mocker fixture
        """
        httpio_capture, auth = httpio(mocker, http_method='post', response_filename='Logout')

        auth.logout()

        expected_data = load_data(path='mock_payloads', filename='Logout')

        httpio_capture.assert_called_with(
            data=expected_data['data'],
            headers=expected_data['headers'],
            path=expected_data['path'],
            timeout=expected_data['timeout']
        )

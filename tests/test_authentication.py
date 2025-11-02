"""Tests for authentication."""

import pytest

from monzo import authentication
from monzo.exceptions import MonzoAuthenticationError
from tests.helpers import Handler, load_data


class TestEndPoints(object):
    """Tests for the authentication."""

    def test_logout(self, mocker):
        """
        Test the logout functionality.

        Args:
            mocker: Pytest mocker fixture
        """
        httpio_capture = mocker.patch.object(
            authentication.HttpIO,
            "post",
            return_value=load_data(path="mock_responses", filename="Logout"),
        )

        handler = Handler()

        credentials = handler.fetch()

        auth = authentication.Authentication(
            client_id=str(credentials["client_id"]),
            client_secret=str(credentials["client_secret"]),
            redirect_url="",
            access_token=str(credentials["access_token"]),
            access_token_expiry=int(credentials["expiry"]),
            refresh_token=str(credentials["refresh_token"]),
        )

        auth.register_callback_handler(handler)

        auth.logout()

        expected_data = load_data(path="mock_payloads", filename="Logout")

        httpio_capture.assert_called_with(
            data=expected_data["data"],
            headers=expected_data["headers"],
            path=expected_data["path"],
            timeout=expected_data["timeout"],
        )

    def test_authenticate_with_empty_token(self):
        """
        Test authenticate raises an error when the authorization token is empty.
        """
        auth = authentication.Authentication(
            client_id="client_id",
            client_secret="client_secret",
            redirect_url="",
        )

        with pytest.raises(MonzoAuthenticationError):
            auth.authenticate(authorization_token="", state_token="state_token")

    def test_authenticate_state_token_mismatch(self, tmp_path, mocker):
        """
        Test authenticate raises an error when the provided state token does not match.

        Args:
            tmp_path: Pytest fixture for temporary directory.
            mocker: Pytest mocker fixture.
        """
        mocker.patch("monzo.authentication.gettempdir", return_value=str(tmp_path))
        auth = authentication.Authentication(
            client_id="client_id",
            client_secret="client_secret",
            redirect_url="",
        )
        state_token = auth.state_token

        with pytest.raises(MonzoAuthenticationError):
            auth.authenticate(
                authorization_token="auth_token",
                state_token=f"{state_token}invalid",
            )

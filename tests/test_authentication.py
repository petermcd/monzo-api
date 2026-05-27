"""Tests for authentication."""

import pytest

from monzo import authentication
from monzo.exceptions import MonzoArgumentError, MonzoAuthenticationError
from tests.helpers import Handler, load_data


class TestEndPoints(object):
    """Tests for the authentication."""

    def test_redirect_url_https_accepted(self):
        """Test that a valid HTTPS redirect URL is accepted."""
        auth = authentication.Authentication(
            client_id="client_id",
            client_secret="client_secret",
            redirect_url="https://example.com/callback",
        )
        assert auth._redirect_url == "https://example.com/callback"

    def test_redirect_url_localhost_http_accepted(self):
        """Test that HTTP is accepted for localhost redirect URLs."""
        for host in ("http://localhost/callback", "http://127.0.0.1/callback"):
            auth = authentication.Authentication(
                client_id="client_id",
                client_secret="client_secret",
                redirect_url=host,
            )
            assert auth._redirect_url == host

    def test_redirect_url_http_non_localhost_rejected(self):
        """Test that HTTP is rejected for non-localhost redirect URLs."""
        with pytest.raises(MonzoArgumentError):
            authentication.Authentication(
                client_id="client_id",
                client_secret="client_secret",
                redirect_url="http://example.com/callback",
            )

    def test_redirect_url_invalid_rejected(self):
        """Test that a malformed redirect URL is rejected."""
        with pytest.raises(MonzoArgumentError):
            authentication.Authentication(
                client_id="client_id",
                client_secret="client_secret",
                redirect_url="not-a-url",
            )

    def test_redirect_url_empty_accepted(self):
        """Test that an empty redirect URL is accepted (token-only usage)."""
        auth = authentication.Authentication(
            client_id="client_id",
            client_secret="client_secret",
            redirect_url="",
        )
        assert auth._redirect_url == ""

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
            client_id="cde456",
            client_secret="fgh789",
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

    def test_is_authenticated_with_valid_token(self):
        """Test is_authenticated returns True when a token exists and has not expired."""
        from time import time

        auth = authentication.Authentication(
            client_id="client_id",
            client_secret="client_secret",
            redirect_url="",
            access_token="valid_token",
            access_token_expiry=int(time()) + 3600,
        )

        assert auth.is_authenticated is True

    def test_is_authenticated_with_expired_token(self):
        """Test is_authenticated returns False when the token has expired."""
        from time import time

        auth = authentication.Authentication(
            client_id="client_id",
            client_secret="client_secret",
            redirect_url="",
            access_token="expired_token",
            access_token_expiry=int(time()) - 1,
        )

        assert auth.is_authenticated is False

    def test_is_authenticated_with_no_token(self):
        """Test is_authenticated returns False when no access token is set."""
        auth = authentication.Authentication(
            client_id="client_id",
            client_secret="client_secret",
            redirect_url="",
        )

        assert auth.is_authenticated is False

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

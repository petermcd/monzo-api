import pytest

from monzo.authentication import Authentication
from monzo.endpoints.monzo import Monzo
from monzo.exceptions import MonzoAuthenticationError


class TestMonzo:
    @pytest.mark.parametrize(
        "expected_exception, expected_message",
        [
            (MonzoAuthenticationError, "Endpoint cannot be instantiated without a valid access token"),
        ],
    )
    def test_missing_access_token(self, expected_exception, expected_message):
        """
        Test that Monzo raises a ValueError when instantiated without an access token.

        Args:
            expected_exception: The expected exception type
            expected_message: The expected exception message
        """

        auth = Authentication(
            client_id="mock_client_id",
            client_secret="mock_client_secret",
            redirect_url="http://localhost",
        )
        with pytest.raises(expected_exception) as exc_info:
            Monzo(auth)

        assert str(exc_info.value) == expected_message

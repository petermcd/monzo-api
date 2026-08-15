from email.message import Message
from unittest.mock import patch
from urllib.error import HTTPError, URLError

import pytest

from monzo.exceptions import (
    MonzoAuthenticationError,
    MonzoGeneralError,
    MonzoHTTPError,
    MonzoPermissionsError,
    MonzoServerError,
)
from monzo.httpio import HttpIO


class TestHttpIO:
    """Test cases for the HttpIO class."""

    @pytest.mark.parametrize(
        "url, path, code, expected_exception, message",
        [
            ("https://example.com", "/test", 400, MonzoHTTPError, "Bad Request"),
            ("https://example.com", "/test", 401, MonzoAuthenticationError, "Unauthorized"),
            ("https://example.com", "/test", 403, MonzoPermissionsError, "Forbidden"),
            ("https://example.com", "/test", 418, MonzoGeneralError, "teapot"),
            ("https://example.com", "/test", 500, MonzoServerError, "Internal Server Error"),
        ],
    )
    def test_status_code_raises_exception(self, url, path, code, expected_exception, message):
        """Test that specific HTTP status codes raise the expected exceptions."""
        http = HttpIO(url=url)
        error = HTTPError(url=f"{url}{path}", code=code, msg=message, hdrs=Message(), fp=None)
        with (
            patch(target="monzo.httpio.urlopen", side_effect=error),
            pytest.raises(expected_exception=expected_exception),
        ):
            http.get(path=path)

    def test_url_error_raises_monzogeneralerror(self):
        """Test that a URLError raises a MonzoGeneralError."""
        http = HttpIO(url="https://example.com")
        with (
            patch(target="monzo.httpio.urlopen", side_effect=URLError("connection refused")),
            pytest.raises(expected_exception=MonzoGeneralError),
        ):
            http.get(path="/test")

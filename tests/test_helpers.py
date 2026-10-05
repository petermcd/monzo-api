from datetime import UTC, datetime

import pytest

from monzo.helpers import create_date, format_date


class TestHelpers:
    """Test cases for the create_date and format_date functions."""

    @pytest.mark.parametrize(
        "date_str, expected_datetime",
        [
            (
                "2024-06-01T12:34:56.789Z",
                datetime(year=2024, month=6, day=1, hour=12, minute=34, second=56, tzinfo=UTC),
            ),
            ("2023-01-15T00:00:00.000Z", datetime(year=2023, month=1, day=15, hour=0, minute=0, second=0, tzinfo=UTC)),
            (
                "2022-12-31T23:59:59.999Z",
                datetime(year=2022, month=12, day=31, hour=23, minute=59, second=59, tzinfo=UTC),
            ),
        ],
    )
    def test_create_date(self, date_str: str, expected_datetime: datetime):
        """
        Test that create_date correctly converts a date string to a datetime object.

        Args:
            date_str: The date string to convert.
            expected_datetime: The expected datetime object after conversion.
        """
        assert create_date(date_str) == expected_datetime

    @pytest.mark.parametrize(
        "date, expected_date_str",
        [
            (datetime(year=2024, month=6, day=1, hour=12, minute=34, second=56, tzinfo=UTC), "2024-06-01T12:34:56Z"),
            (datetime(year=2023, month=1, day=15, hour=0, minute=0, second=0, tzinfo=UTC), "2023-01-15T00:00:00Z"),
            (datetime(year=2022, month=12, day=31, hour=23, minute=59, second=59, tzinfo=UTC), "2022-12-31T23:59:59Z"),
        ],
    )
    def test_format_date(self, date: datetime, expected_date_str: str):
        """
        Test that format_date correctly converts a datetime object to a date string.

        This test checks that the format_date function returns the expected string representation
        of a given datetime object in the format Monzo expects.

        Args:
            date: The datetime object to convert.
            expected_date_str: The expected string representation of the datetime object.
        """
        date = datetime(year=2024, month=6, day=1, hour=12, minute=34, second=56, tzinfo=UTC)
        expected_date_str = "2024-06-01T12:34:56Z"
        assert format_date(date) == expected_date_str

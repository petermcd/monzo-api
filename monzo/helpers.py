"""Helper functions."""
from datetime import datetime


def create_date(date_str: str) -> datetime:
    """
    Convert a date and time received from Monzo into a DateTime object.

    Args:
        date_str: Date and time as a string

    Returns:
        Converted date and time
    """
    return datetime.strptime(date_str[:19], '%Y-%m-%dT%H:%M:%S')


def format_date(date: datetime) -> str:
    """
    Convert a datetime object to a format Monzo expects.

    Args:
        date: Date and time as a string

    Returns:
        Converted date and time
    """
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')

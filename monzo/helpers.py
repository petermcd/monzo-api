"""Helper functions."""
import random
import string
from datetime import datetime


def generate_random_token(length: int = 64, include_punctuation: bool = False) -> str:
    """
    Create a random token of the given length.

    Args:
        length: The length of the required random string
        include_punctuation: True if punctuation should be included

    Returns:
        Random string of the given length
    """
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    if include_punctuation:
        letters += string.punctuation
    return ''.join(random.choice(letters) for _ in range(length))


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

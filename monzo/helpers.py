import random
import string


def generate_random_token(length: int = 64, include_punctuation: bool = False) -> str:
    """
    Creates a random token of the given length.

    Args:
        length: The length of the rquired random string
        include_punctuation: True if punctuation should be included

    Returns:
        Random string of the given length
    """
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    if include_punctuation:
        letters += string.punctuation
    return ''.join(random.choice(letters) for _ in range(length))

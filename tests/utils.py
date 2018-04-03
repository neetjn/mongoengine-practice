import random
import string
from falcon.testing import TestCase
from blog.db import client


def drop_database():
    """Drop all collections in database"""
    db_name = client.get_database().name
    client.drop_database(db_name)


def random_string(length: int) -> str:
    """
    Generate random string using ascii letters.

    :param length: Length of random string to generate.
    :type length: int
    :return: str
    """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def random_email() -> str:
    """Generate random email address."""
    return f'{random_string(10)}@{random_string(3)}.{random_string(3)}'


def normalize_href(href: str) -> str:
    return href.replace('falconframework.org', '')

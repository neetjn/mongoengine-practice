import random
import string
from falcon.testing import TestCase
from redis import StrictRedis
from blog.constants import BLOG_REDIS_HOST, BLOG_REDIS_PORT
from blog.db import client


def drop_database():
    """Drop all collections in database"""
    db_name = client.get_database().name
    client.drop_database(db_name)
    redis = StrictRedis(host=BLOG_REDIS_PORT, port=BLOG_REDIS_PORT)
    redis.flushdb()


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


def find_link_href(links: list, rel: str) -> str:
    """Extract link href by rel for linkdto instances."""
    return next(l for l in links if l.rel == rel).href


def find_link_href_json(links: list, rel: str) -> str:
    """Extract link href by rel for non serialized json."""
    return next(l for l in links if l.get('rel') == rel).get('href')

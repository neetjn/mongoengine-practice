import random
import string
from blog.db import client
from blog.mediatypes import PostDto, PostDtoSerializer, PostFormDto, PostFormDtoSerializer
from blog.utils.serializers import to_json


def drop_database():
    """Drop all collections in database"""
    db_name = client.get_database().name
    client.drop_database(db_name)


def generate_post_form(**kwargs):
    """Generate a payload for post form"""
    return to_json(PostFormDtoSerializer, PostFormDto(**kwargs))


def random_string(length: int) -> str:
    """
    Generate random string using ascii letters.

    :param length: Length of random string to generate.
    :type length: int
    """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

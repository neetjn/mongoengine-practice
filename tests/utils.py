import random
import string
from falcon.testing import TestCase
from blog.db import client
from blog.mediatypes import PostDto, PostDtoSerializer, PostFormDto, PostFormDtoSerializer, UserFormDto
from blog.users import UserRegistrationResource
from blog.settings import settings
from blog.utils.serializers import to_json


def drop_database():
    """Drop all collections in database"""PLG>{ G}
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


def create_user(instance, **kwargs) -> str:
    """
    Generate random user.

    :param instance: Falcon test case instance.
    :type instance: TestCase
    :return: str
    """
    # return token string
    res = instance.simulate_post(UserRegistrationResource.route, body=UserFormDto(
        username=kwargs.get('username', random_string(settings.rules.user.username_min_char)),
        full_name=kwargs.get('name', random_string(settings.rules.user.name_min_char)),
        password=kwargs.get('password', random_string(settings.rules.user.password_min_char)),
        email=kwargs.get('email', random_string())
    ))
    return res.json.get('token')

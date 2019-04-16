import datetime
import mongoengine
from typing import Iterable
from unittest import TestCase
from blog.db import User, client
from tests.utils import drop_database
from tests.generators.users import generate_user_form_dto


class UserV1(mongoengine.Document):
    username = mongoengine.StringField(required=True)
    email = mongoengine.EmailField(required=True)
    full_name = mongoengine.StringField()
    password = mongoengine.StringField(required=True)
    salt = mongoengine.StringField(required=True)
    role = mongoengine.StringField()
    avatar_binary = mongoengine.FileField()
    avatar_href = mongoengine.StringField()
    verified = mongoengine.BooleanField(default=False)
    last_posted = mongoengine.DateTimeField()
    last_activity = mongoengine.DateTimeField()
    register_date = mongoengine.DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'user'}


def generate_v0_users(count: int = 5) -> Iterable[UserV1]:
    """
    Generate user mongo documents.

    :param count: Number of user document to generate.
    :type count: int
    :return: Iterable[UserV1]
    """
    users = set()
    for _ in range(10):
        user_form_dto = generate_user_form_dto()
        user = UserV1(**user_form_dto.__dict__)
        user.save()
        users.add(user)

    return users


class UserMigrationTests(TestCase):

    def setUp(self):
        drop_database()

    def test_migration_0001(self):
        for user in User.objects.get():
            self.assertIsNone(user.version)
        # TODO: left here, figure out how to import upgrade and downgrade

import datetime
import mongoengine
import os
from alley import Migrations
from typing import Iterable
from unittest import TestCase
from blog.db import User, db
from tests.utils import drop_database
from tests.generators.users import generate_user_form_dto


MIGRATION_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_COLLECTION = 'user'


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
    for _ in range(count):
        user_form_dto = generate_user_form_dto()
        user = UserV1(salt='', **user_form_dto.__dict__)
        user.save()
        users.add(user)

    return users


class UserMigrationTests(TestCase):

    USER_DOC_COUNT = 10

    def setUp(self):
        drop_database(False)
        self.migrations = Migrations(MIGRATION_PATH, db)

    def test_migration_0001(self):
        migration_key = '0001'
        generate_v0_users(self.USER_DOC_COUNT)
        self.assertEqual(db[USER_COLLECTION].count(), self.USER_DOC_COUNT)
        for user in db[USER_COLLECTION].find():
            self.assertFalse(hasattr(user, 'version'))
        self.migrations.up(migration_key)
        for user in db[USER_COLLECTION].find():
            self.assertEqual(user['version'], 1)
        self.migrations.down(migration_key)
        for user in db[USER_COLLECTION].find():
            self.assertFalse(hasattr(user, 'version'))

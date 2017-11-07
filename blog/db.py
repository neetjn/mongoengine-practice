from mongoengine import *


class User(Document):

    username = StringField()
    full_name = StringField()
    posts = fields.ListField(fields.StringField)
    total_likes = IntField()
    last_posted = DateTimeField()
    last_activity = DateTimeField()



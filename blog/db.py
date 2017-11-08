from datetime import datetime
from mongoengine import *


class User(Document):

    username = StringField()
    full_name = StringField()
    posts = ListField(StringField)
    comments = ListField(StringField)
    total_likes = IntField()
    last_posted = DateTimeField()
    last_activity = DateTimeField()


class Comment(EmbeddedDocument):

    author = StringField(required=True)
    content = StringField(required=True)
    tags = ListField(StringField)
    created = DateTimeField(default=datetime.now())
    edited = DateTimeField()
    comments = ListField(StringField)
    likes = IntField(default=0)
    views = IntField(default=0)


class PostView(EmbeddedDocument):

    ip_address = StringField(required=True)
    view_time = DateTimeField(default=datetime.now())


class Post(Document):

    title = StringField(required=True)
    author = StringField(required=True)
    content = StringField(required=True)
    tags = ListField(StringField())
    created = DateTimeField(default=datetime.now())
    edited = DateTimeField()
    comments = ListField(StringField)
    likes = IntField(default=0)
    views = IntField(default=0)

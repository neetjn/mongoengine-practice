from datetime import datetime
from mongoengine import *


class User(Document):

    username = StringField(required=True)
    email = EmailField(required=True)
    full_name = StringField()
    password = StringField(required=True)
    salt = StringField(required=True)
    avatar_href = StringField()
    last_posted = DateTimeField()
    last_activity = DateTimeField()


class CommentLike(EmbeddedDocument):

    user_id = StringField(required=True)
    time = DateTimeField(default=datetime.now())


class Comment(EmbeddedDocument):

    author = StringField(required=True)
    content = StringField(required=True)
    created = DateTimeField(default=datetime.now())
    edited = DateTimeField()
    likes = ListField(EmbeddedDocumentField(CommentLike))


class PostLike(EmbeddedDocument):

    user_id = StringField(required=True)
    time = DateTimeField(default=datetime.now())


class PostView(EmbeddedDocument):

    ip_address = StringField(required=True)
    seen = DateTimeField(default=datetime.now())


class Post(Document):

    title = StringField(required=True)
    author = StringField(required=True)
    content = StringField(required=True)
    tags = ListField(StringField())
    created = DateTimeField(default=datetime.now())
    edited = DateTimeField()
    likes = ListField(EmbeddedDocumentField(PostLike))
    views = ListField(EmbeddedDocumentField(PostView))

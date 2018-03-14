from datetime import datetime
import mongoengine


class UserValidation(mongoengine.Document):

    user_id = mongoengine.StringField(required=True)
    code = mongoengine.StringField()
    requested = mongoengine.DateTimeField(default=datetime.datetime.utcnow)


class User(mongoengine.Document):

    username = mongoengine.StringField(required=True)
    email = mongoengine.EmailField(required=True)
    full_name = mongoengine.StringField()
    password = mongoengine.StringField(required=True)
    salt = mongoengine.StringField(required=True)
    role = mongoengine.StringField()
    avatar_href = mongoengine.StringField()
    verified = mongoengine.BooleanField(default=False)
    last_posted = mongoengine.DateTimeField()
    last_activity = mongoengine.DateTimeField()
    register_date = mongoengine.DateTimeField(default=datetime.datetime.utcnow)


class PostLike(mongoengine.EmbeddedDocument):

    user_id = mongoengine.StringField(required=True)
    time = mongoengine.DateTimeField(default=datetime.datetime.utcnow)


class PostView(mongoengine.EmbeddedDocument):

    ip_address = mongoengine.StringField(required=True)
    seen = mongoengine.DateTimeField(default=datetime.datetime.utcnow)


class Post(mongoengine.Document):

    title = mongoengine.StringField(required=True)
    description = mongoengine.StringField()
    author = mongoengine.StringField(required=True)
    content = mongoengine.StringField(required=True)
    tags = mongoengine.ListField(mongoengine.StringField())
    created = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    edited = mongoengine.DateTimeField()
    likes = mongoengine.ListField(mongoengine.EmbeddedDocumentField(PostLike))
    views = mongoengine.ListField(mongoengine.EmbeddedDocumentField(PostView))


class CommentLike(mongoengine.EmbeddedDocument):

    user_id = mongoengine.StringField(required=True)
    time = mongoengine.DateTimeField(default=datetime.datetime.utcnow)


class Comment(mongoengine.EmbeddedDocument):

    post_id = mongoengine.StringField(required=True)
    author = mongoengine.StringField(required=True)
    content = mongoengine.StringField(required=True)
    created = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    edited = mongoengine.DateTimeField()
    likes = mongoengine.ListField(mongoengine.EmbeddedDocumentField(CommentLike))

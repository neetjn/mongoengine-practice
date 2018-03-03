from datetime import datetime
import mongoengine


class User(mongoengine.Document):

    username = mongoengine.StringField(required=True)
    email = mongoengine.EmailField(required=True)
    full_name = mongoengine.StringField()
    password = mongoengine.StringField(required=True)
    salt = mongoengine.StringField(required=True)
    role = mongoengine.StringField()
    avatar_href = mongoengine.StringField()
    last_posted = mongoengine.DateTimeField()
    last_activity = mongoengine.DateTimeField()
    register_date = mongoengine.DateTimeField(default=datetime.datetime.utcnow)


class CommentLike(mongoengine.EmbeddedDocument):

    user_id = mongoengine.StringField(required=True)
    time = mongoengine.DateTimeField(default=datetime.now())


class Comment(mongoengine.EmbeddedDocument):

    author = mongoengine.StringField(required=True)
    content = mongoengine.StringField(required=True)
    created = mongoengine.DateTimeField(default=datetime.now())
    edited = mongoengine.DateTimeField()
    likes = mongoengine.ListField(mongoengine.EmbeddedDocumentField(CommentLike))


class PostLike(mongoengine.EmbeddedDocument):

    user_id = mongoengine.StringField(required=True)
    time = mongoengine.DateTimeField(default=datetime.now())


class PostView(mongoengine.EmbeddedDocument):

    ip_address = mongoengine.StringField(required=True)
    seen = mongoengine.DateTimeField(default=datetime.now())


class Post(mongoengine.Document):

    title = mongoengine.StringField(required=True)
    author = mongoengine.StringField(required=True)
    content = mongoengine.StringField(required=True)
    tags = mongoengine.ListField(mongoengine.StringField())
    created = mongoengine.DateTimeField(default=datetime.now())
    edited = mongoengine.DateTimeField()
    likes = mongoengine.ListField(mongoengine.EmbeddedDocumentField(PostLike))
    views = mongoengine.ListField(mongoengine.EmbeddedDocumentField(PostView))

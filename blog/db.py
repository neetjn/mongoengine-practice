import datetime
import mongoengine
from blog.constants import BLOG_DB_URI


client = mongoengine.connect(host=BLOG_DB_URI)


class FailedLogin(mongoengine.Document):

    username = mongoengine.StringField()
    ip_address = mongoengine.StringField()
    time = mongoengine.DateTimeField(default=datetime.datetime.utcnow)


class UserValidation(mongoengine.Document):

    user_id = mongoengine.StringField(required=True)
    code = mongoengine.StringField()
    requested = mongoengine.DateTimeField(default=datetime.datetime.utcnow)


class User(mongoengine.Document):

    _version = 1
    version = mongoengine.IntField(default=_version)

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


class PostLike(mongoengine.Document):

    post_id = mongoengine.StringField(required=True)
    user_id = mongoengine.StringField(required=True)
    time = mongoengine.DateTimeField(default=datetime.datetime.utcnow)


class PostView(mongoengine.Document):

    post_id = mongoengine.StringField(required=True)
    user_id = mongoengine.StringField(required=True)
    ip_address = mongoengine.StringField(required=True)
    seen = mongoengine.DateTimeField(default=datetime.datetime.utcnow)


class PostSearchRequest(mongoengine.Document):

    user_id = mongoengine.StringField(required=True)
    query = mongoengine.StringField(required=True)
    options = mongoengine.ListField(mongoengine.StringField(), required=True)
    time = mongoengine.DateTimeField(default=datetime.datetime.utcnow)


class PostQuerySet(mongoengine.QuerySet):

    def get_public(self):
        return self.filter(private=False)


class Post(mongoengine.Document):

    author = mongoengine.StringField(required=True)
    title = mongoengine.StringField(required=True)
    description = mongoengine.StringField()
    content = mongoengine.StringField(required=True)
    tags = mongoengine.ListField(mongoengine.StringField())
    private = mongoengine.BooleanField(default=False)
    featured = mongoengine.BooleanField(default=False)
    created = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    edited = mongoengine.DateTimeField()

    meta = {'queryset_class': PostQuerySet}


class CommentLike(mongoengine.Document):

    comment_id = mongoengine.StringField(required=True)
    user_id = mongoengine.StringField(required=True)
    time = mongoengine.DateTimeField(default=datetime.datetime.utcnow)


class Comment(mongoengine.Document):

    post_id = mongoengine.StringField(required=True)
    author = mongoengine.StringField(required=True)
    content = mongoengine.StringField(required=True)
    created = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    edited = mongoengine.DateTimeField()

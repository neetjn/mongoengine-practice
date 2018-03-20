import datetime
import mongoengine


class FailedLogin(mongoengine.Document):

    username = mongoengine.StringField()
    ip_address = mongoengine.StringField()
    time = mongoengine.DateTimeField(default=datetime.datetime.utcnow)


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


class PostLike(mongoengine.Document):

    post_id = mongoengine.StringField(required=True)
    user_id = mongoengine.StringField(required=True)
    time = mongoengine.DateTimeField(default=datetime.datetime.utcnow)


class PostView(mongoengine.Document):

    post_id = mongoengine.StringField(required=True)
    user_id = mongoengine.StringField(required=True)
    ip_address = mongoengine.StringField(required=True)
    seen = mongoengine.DateTimeField(default=datetime.datetime.utcnow)


class PostQuerySet(mongoengine.QuerySet):

    def get_public(self):
        return self.filter(private=True)


class Post(mongoengine.Document):

    title = mongoengine.StringField(required=True)
    description = mongoengine.StringField()
    author = mongoengine.StringField(required=True)
    content = mongoengine.StringField(required=True)
    tags = mongoengine.ListField(mongoengine.StringField())
    private = mongoengine.BooleanField(default=False)
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

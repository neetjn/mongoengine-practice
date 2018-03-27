import re
from r2dto import fields, validators, Serializer, ValidationError
from blog.constants import USERNAME_PATTERN
from blog.settings import settings
from blog.utils.serializers import CharLenValidator, EmailValidator, RegexValidator, \
    NotEmptyValidator


class UserRoles(object):

    admin = 'ADMIN'
    moderator = 'MODERATOR'
    blogger = 'BLOGGER'


class SearchOption(object):

    title = 'TITLE'
    content = 'CONTENT'
    author = 'AUTHOR'


class LinkDto(object):

    def __init__(self, rel=None, href=None):
        self.rel = rel
        self.href = href


class LinkDtoSerializer(Serializer):

    rel = fields.StringField()
    href = fields.StringField()

    class Meta(object):
        model = LinkDto


class ServiceDescriptionDto(object):

    def __init__(self, **kwargs):
        self.links = kwargs.get('links', [])


class ServiceDescriptionDtoSerializer(Serializer):

    links = fields.ListField(fields.ObjectField(LinkDtoSerializer))

    class Meta(object):

        model = ServiceDescriptionDto


class TokenDto(object):

    def __init__(self, **kwargs):
        self.token = kwargs.get('token', '')


class TokenDtoSerializer(Serializer):

    token = fields.StringField()

    class Meta(object):
        model = TokenDto


class CommentDto(object):

    def __init__(self, **kwargs):
        self.href = kwargs.get('href', '')
        self.author = kwargs.get('author', '')
        self.content = kwargs.get('content', '')
        self.created = kwargs.get('created', None)
        self.edited = kwargs.get('edited', None)
        self.likes = kwargs.get('likes', 0)
        self.views = kwargs.get('views', 0)
        self.links = kwargs.get('links', [])


class CommentDtoSerializer(Serializer):

    href = fields.StringField()
    author = fields.StringField()
    content = fields.StringField(validators=[
        NotEmptyValidator(),
        CharLenValidator(
            min=settings.rules.comment.content_min_char,
            max=settings.rules.comment.content_max_char
        )
    ])
    created = fields.DateTimeField()
    edited = fields.DateTimeField()
    likes = fields.IntegerField()
    links = fields.ListField(fields.ObjectField(LinkDtoSerializer))

    class Meta(object):

        model = CommentDto


class CommentCollectionDto(object):

    def __init__(self, **kwargs):
        self.comments = kwargs.get('comments', [])


class CommentCollectionDtoSerializer(Serializer):

    comments = fields.ListField(fields.ObjectField(CommentDtoSerializer))


class CommentFormDto(object):

    def __init__(self, **kwargs):
        self.content = kwargs.get('content', '')


class CommentFormDtoSerializer(Serializer):

    content = fields.StringField(validators=[
        NotEmptyValidator(),
        CharLenValidator(
            min=settings.rules.post.content_min_char,
            max=settings.rules.post.content_max_char
        )
    ])

    class Meta(object):

        model = CommentFormDto


class PostViewDto(object):

    def __init__(self, **kwargs):
        self.ip_address = kwargs.get('ip_address', None)
        self.view_time = kwargs.get('view_time', None)


class PostViewDtoSerializer(Serializer):

    ip_address = fields.StringField(name='ipAddress', required=True)
    view_time = fields.DateTimeField(name='viewTime', required=True)

    class Meta(object):

        model = PostViewDto


class PostSearchSettings(object):

    def __init__(self, **kwargs):
        self.options = kwargs.get('method', [])


class PostSearchSettingsSerializer(Serializer):

    options = fields.ListField(fields.ObjectField(fields.StringField))


class PostDto(object):

    def __init__(self, **kwargs):
        self.href = kwargs.get('href', '')
        self.author = kwargs.get('author', '')
        self.title = kwargs.get('title', '')
        self.description = kwargs.get('description', '')
        self.content = kwargs.get('content', '')
        self.tags = kwargs.get('tags', [])
        self.private = kwargs.get('private', False)
        self.created = kwargs.get('created', None)
        self.edited = kwargs.get('edited', None)
        self.comments = kwargs.get('comments', [])
        self.likes = kwargs.get('likes', 0)
        self.views = kwargs.get('views', 0)
        self.links = kwargs.get('links', [])


class PostDtoSerializer(Serializer):

    href = fields.StringField()
    author = fields.StringField()
    title = fields.StringField(validators=[
        NotEmptyValidator(),
        CharLenValidator(
            min=settings.rules.post.title_min_char,
            max=settings.rules.post.title_max_char
        )
    ])
    description = fields.StringField(validators=[
        NotEmptyValidator(),
        CharLenValidator(
            min=settings.rules.post.title_min_char,
            max=settings.rules.post.title_max_char
        )
    ])
    content = fields.StringField(validators=[NotEmptyValidator()])
    tags = fields.ListField(fields.ObjectField(fields.StringField))
    created = fields.DateTimeField()
    edited = fields.DateTimeField()
    comments = fields.ListField(fields.ObjectField(CommentDtoSerializer))
    likes = fields.IntegerField()
    views = fields.IntegerField()
    links = fields.ListField(fields.ObjectField(LinkDtoSerializer))

    class Meta(object):

        model = PostDto


class PostCollectionDto(object):

    def __init__(self, **kwargs):
        self.posts = kwargs.get('posts', [])


class PostCollectionDtoSerializer(Serializer):

    posts = fields.ListField(fields.ObjectField(PostDtoSerializer))

    class Model(object):

        model = PostCollectionDto

class PostFormDto(object):

    def __init__(self, **kwargs):
        self.title = kwargs.get('title', '')
        self.description = kwargs.get('description', '')
        self.content = kwargs.get('content', '')
        self.tags = kwargs.get('tags', [])
        self.private = kwargs.get('private', False)


class PostFormDtoSerializer(Serializer):

    title = fields.StringField(validators=[
        NotEmptyValidator(),
        CharLenValidator(
            min=settings.rules.post.title_min_char,
            max=settings.rules.post.title_max_char
        )
    ])
    description = fields.StringField(validators=[
        NotEmptyValidator(),
        CharLenValidator(
            min=settings.rules.post.title_min_char,
            max=settings.rules.post.title_max_char
        )
    ])
    content = fields.StringField(validators=[NotEmptyValidator()])
    tags = fields.ListField(fields.ObjectField(fields.StringField))
    private = fields.BooleanField()

    class Meta(object):

        model = PostFormDto


class UserProfileDto(object):

    def __init__(self, **kwargs):
        self.href = kwargs.get('href', '')
        self.username = kwargs.get('username', '')
        self.email = kwargs.get('email', '')
        self.full_name = kwargs.get('full_name', '')
        self.posts = kwargs.get('posts', [])
        self.comments = kwargs.get('comments', [])
        self.liked_posts = kwargs.get('liked_posts', [])
        self.last_posted = kwargs.get('last_posted', None)
        self.last_activity = kwargs.get('last_activity', None)
        self.register_date = kwargs.get('register_date', None)
        self.links = kwargs.get('links', [])


class UserProfileDtoSerializer(Serializer):

    href = fields.StringField()
    username = fields.StringField(validators=[
        NotEmptyValidator(),
        CharLenValidator(
            min=settings.rules.user.username_min_char,
            max=settings.rules.user.username_max_char
        ),
        RegexValidator(pattern=USERNAME_PATTERN)
    ])
    full_name = fields.StringField(name='fullName', validators=[
        NotEmptyValidator(),
        CharLenValidator(
            min=settings.rules.user.name_min_char,
            max=settings.rules.user.name_max_char
        )
    ])
    email = fields.StringField(validators=[NotEmptyValidator(), EmailValidator()])
    posts = fields.ListField(fields.ObjectField(PostDtoSerializer))
    comments = fields.ListField(fields.ObjectField(CommentDtoSerializer))
    liked_posts = fields.ListField(fields.ObjectField(PostDtoSerializer), name='likedPosts')
    last_posted = fields.DateTimeField(name='lastPosted')
    last_activity = fields.DateTimeField(name='lastActivity')
    register_date = fields.DateTimeField(name='registerDate')
    links = fields.ListField(fields.ObjectField(LinkDtoSerializer))

    class Meta(object):
        model = UserProfileDto


class UserFormDto(object):

    def __init__(self, **kwargs):
        self.username = kwargs.get('username', '')
        self.avatar_href = kwargs.get('avatar_href', '')
        self.password = kwargs.get('password', '')
        self.email = kwargs.get('email', '')
        self.full_name = kwargs.get('full_name', '')


class UserFormDtoSerializer(Serializer):

    username = fields.StringField(validators=[
        NotEmptyValidator(),
        CharLenValidator(
            min=settings.rules.user.username_min_char,
            max=settings.rules.user.username_max_char
        ),
        RegexValidator(pattern=USERNAME_PATTERN)
    ])
    full_name = fields.StringField(name='fullName', validators=[
        NotEmptyValidator(),
        CharLenValidator(
            min=settings.rules.user.name_min_char,
            max=settings.rules.user.name_max_char
        )
    ])
    email = fields.StringField(validators=[EmailValidator()])
    password = fields.StringField()
    avatar_href = fields.StringField(name='avatarHref')

    class Meta(object):

        model = UserFormDto


class UserAuthDto(object):

    def __init__(self, **kwargs):
        self.username = kwargs.get('username', '')
        self.password = kwargs.get('password', '')


class UserAuthDtoSerializer(Serializer):

    username = fields.StringField(validators=[
        NotEmptyValidator(),
        CharLenValidator(
            min=settings.rules.user.username_min_char,
            max=settings.rules.user.username_max_char
        ),
        RegexValidator(pattern=USERNAME_PATTERN)
    ])
    password = fields.StringField()

    class Meta(object):

        model = UserAuthDto

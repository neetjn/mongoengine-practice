import re
from r2dto import fields, validators, Serializer, ValidationError
from blog.constants import USERNAME_PATTERN
from blog.settings import settings
from blog.utils.serializers import CharLenValidator, EmailValidator, RegexValidator, \
    NotEmptyValidator, LengthValidator


class HttpMethods(object):

    GET = 'GET'
    PUT = 'PUT'
    POST = 'POST'
    DELETE = 'DELETE'
    PATCH = 'PATCH'


class UserRoles(object):

    ADMIN = 'ADMIN'
    MODERATOR = 'MODERATOR'
    BLOGGER = 'BLOGGER'


class PostSearchOptions(object):

    TITLE = 'title'
    CONTENT = 'content'
    DESCRIPTION = 'description'
    TAGS = 'tags'
    AUTHOR = 'author'


class LinkDto(object):

    def __init__(self, rel=None, href=None, accepted_methods=None):
        self.rel = rel
        self.href = href
        self.accepted_methods = accepted_methods or []


class LinkDtoSerializer(Serializer):

    rel = fields.StringField(required=True)
    href = fields.StringField(required=True)
    accepted_methods = fields.ListField(fields.StringField(), name='acceptedMethods')
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

    token = fields.StringField(required=True)

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

    content = fields.StringField(required=True, validators=[
        NotEmptyValidator(),
        CharLenValidator(
            min=settings.rules.comment.content_min_char,
            max=settings.rules.comment.content_max_char
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


class PostSearchSettingsDto(object):

    def __init__(self, **kwargs):
        self.query = kwargs.get('query', '')
        self.options = kwargs.get('options', [])


class PostSearchSettingsDtoSerializer(Serializer):

    query = fields.StringField(required=True, validators=[
        NotEmptyValidator()
    ])
    options = fields.ListField(fields.StringField())

    class Meta(object):

        model = PostSearchSettingsDto


class PostDto(object):

    def __init__(self, **kwargs):
        self.href = kwargs.get('href', '')
        self.author = kwargs.get('author', '')
        self.title = kwargs.get('title', '')
        self.description = kwargs.get('description', '')
        self.content = kwargs.get('content', '')
        self.tags = kwargs.get('tags', [])
        self.private = kwargs.get('private', False)
        self.featured = kwargs.get('featured', False)
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
    tags = fields.ListField(fields.StringField(validators=[NotEmptyValidator(),
                                                           CharLenValidator(
                                                               min=settings.rules.post.tag_min_char,
                                                               max=settings.rules.post.tag_max_char
                                                           )]))
    private = fields.BooleanField()
    featured = fields.BooleanField()
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


class PostV2Dto(object):

    def __init__(self, **kwargs):
        self.href = kwargs.get('href', '')
        self.author = kwargs.get('author', '')
        self.title = kwargs.get('title', '')
        self.description = kwargs.get('description', '')
        self.content = kwargs.get('content', '')
        self.tags = kwargs.get('tags', [])
        self.private = kwargs.get('private', False)
        self.featured = kwargs.get('featured', False)
        self.created = kwargs.get('created', None)
        self.edited = kwargs.get('edited', None)
        self.comments = kwargs.get('comments', 0)
        self.likes = kwargs.get('likes', 0)
        self.views = kwargs.get('views', 0)
        self.links = kwargs.get('links', [])


class PostV2DtoSerializer(Serializer):

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
    tags = fields.ListField(fields.StringField(validators=[NotEmptyValidator(),
                                                           CharLenValidator(
                                                               min=settings.rules.post.tag_min_char,
                                                               max=settings.rules.post.tag_max_char
                                                           )]),
                            validators=[LengthValidator(min=0, max=settings.rules.post.tag_max_count)])
    private = fields.BooleanField()
    featured = fields.BooleanField()
    created = fields.DateTimeField()
    edited = fields.DateTimeField()
    comments = fields.IntegerField()
    likes = fields.IntegerField()
    views = fields.IntegerField()
    links = fields.ListField(fields.ObjectField(LinkDtoSerializer))

    class Meta(object):

        model = PostV2Dto


class PostCollectionV2Dto(object):

    def __init__(self, **kwargs):
        self.posts = kwargs.get('posts', [])


class PostCollectionV2DtoSerializer(Serializer):

    posts = fields.ListField(fields.ObjectField(PostV2DtoSerializer))

    class Model(object):

        model = PostCollectionV2Dto


class PostFormDto(object):

    def __init__(self, **kwargs):
        self.title = kwargs.get('title', '')
        self.description = kwargs.get('description', '')
        self.content = kwargs.get('content', '')
        self.tags = kwargs.get('tags', [])
        self.private = kwargs.get('private', False)
        self.featured = kwargs.get('featured', False)


class PostFormDtoSerializer(Serializer):

    title = fields.StringField(required=True, validators=[
        NotEmptyValidator(),
        CharLenValidator(
            min=settings.rules.post.title_min_char,
            max=settings.rules.post.title_max_char
        )
    ])
    description = fields.StringField(required=True, validators=[
        NotEmptyValidator(),
        CharLenValidator(
            min=settings.rules.post.title_min_char,
            max=settings.rules.post.title_max_char
        )
    ])
    content = fields.StringField(required=True, validators=[NotEmptyValidator()])
    tags = fields.ListField(fields.StringField())
    private = fields.BooleanField()
    featured = fields.BooleanField()

    class Meta(object):

        model = PostFormDto


class UserProfileDto(object):

    def __init__(self, **kwargs):
        self.href = kwargs.get('href', '')
        self.username = kwargs.get('username', '')
        self.email = kwargs.get('email', '')
        self.full_name = kwargs.get('full_name', '')
        self.avatar_href = kwargs.get('avatar_href', '')
        self.posts = kwargs.get('posts', [])
        self.comments = kwargs.get('comments', [])
        self.liked_posts = kwargs.get('liked_posts', [])
        self.last_posted = kwargs.get('last_posted', None)
        self.last_activity = kwargs.get('last_activity', None)
        self.register_date = kwargs.get('register_date', None)
        self.links = kwargs.get('links', [])


class UserProfileDtoSerializer(Serializer):

    href = fields.StringField(required=True)
    username = fields.StringField(required=True, validators=[
        NotEmptyValidator(),
        CharLenValidator(
            min=settings.rules.user.username_min_char,
            max=settings.rules.user.username_max_char
        ),
        RegexValidator(pattern=USERNAME_PATTERN)
    ])
    full_name = fields.StringField(required=True, name='fullName', validators=[
        NotEmptyValidator(),
        CharLenValidator(
            min=settings.rules.user.name_min_char,
            max=settings.rules.user.name_max_char
        )
    ])
    avatar_href = fields.StringField(name='avatarHref')
    email = fields.StringField(required=True, validators=[NotEmptyValidator(), EmailValidator()])
    posts = fields.ListField(fields.ObjectField(PostDtoSerializer))
    comments = fields.ListField(fields.ObjectField(CommentDtoSerializer))
    liked_posts = fields.ListField(fields.ObjectField(PostDtoSerializer), name='likedPosts')
    last_posted = fields.DateTimeField(name='lastPosted')
    last_activity = fields.DateTimeField(name='lastActivity')
    register_date = fields.DateTimeField(required=True, name='registerDate')
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

    username = fields.StringField(required=True, validators=[
        NotEmptyValidator(),
        CharLenValidator(
            min=settings.rules.user.username_min_char,
            max=settings.rules.user.username_max_char
        ),
        RegexValidator(pattern=USERNAME_PATTERN)
    ])
    full_name = fields.StringField(required=True, name='fullName', validators=[
        NotEmptyValidator(),
        CharLenValidator(
            min=settings.rules.user.name_min_char,
            max=settings.rules.user.name_max_char
        )
    ])
    email = fields.StringField(required=True, validators=[EmailValidator()])
    password = fields.StringField(required=True, validators=[
        NotEmptyValidator(),
        CharLenValidator(
            min=settings.rules.user.password_min_char,
            max=settings.rules.user.password_max_char
        )
    ])
    avatar_href = fields.StringField(name='avatarHref')

    class Meta(object):

        model = UserFormDto


class UserUpdateFormDto(object):

    def __init__(self, **kwargs):
        self.avatar_href = kwargs.get('avatar_href', '')
        self.password = kwargs.get('password', '')
        self.email = kwargs.get('email', '')
        self.full_name = kwargs.get('full_name', '')


class UserUpdateFormDtoSerializer(Serializer):

    full_name = fields.StringField(name='fullName', validators=[
        CharLenValidator(
            min=settings.rules.user.name_min_char,
            max=settings.rules.user.name_max_char
        )
    ])
    email = fields.StringField(validators=[EmailValidator()])
    password = fields.StringField(validators=[
        CharLenValidator(
            min=settings.rules.user.password_min_char,
            max=settings.rules.user.password_max_char
        )
    ])
    avatar_href = fields.StringField(name='avatarHref')

    class Meta(object):

        model = UserUpdateFormDto


class UserAuthDto(object):

    def __init__(self, **kwargs):
        self.username = kwargs.get('username', '')
        self.password = kwargs.get('password', '')


class UserAuthDtoSerializer(Serializer):

    username = fields.StringField(required=True, validators=[
        NotEmptyValidator(),
        CharLenValidator(
            min=settings.rules.user.username_min_char,
            max=settings.rules.user.username_max_char
        ),
        RegexValidator(pattern=USERNAME_PATTERN)
    ])
    password = fields.StringField(required=True)

    class Meta(object):

        model = UserAuthDto

from r2dto import fields, validators, Serializer


class User(object):

    def __init__(self, **kwargs):

        self.username = kwargs.get('username', '')
        self.full_name = kwargs.get('full_name', '')
        self.posts = kwargs.get('posts', [])
        self.total_likes = kwargs.get('total_links', 0)
        self.last_posted = kwargs.get('last_posted', None)
        self.last_activity = kwargs.get('last_activity', None)


class UserSerializer(object):

    username = fields.StringField()
    full_name = fields.StringField(name='fullName')
    posts = fields.ListField(fields.StringField)
    total_likes = fields.IntegerField(name='totalLikes')
    last_posted = fields.DateTimeField(name='lastPosted')
    last_activity = fields.DateTimeField(name='lastActivity')


class Comment(object):

    def __init__(self, **kwargs):

        self.id = kwargs.get('id', '')
        self.author = kwargs.get('author', '')
        self.content = kwargs.get('content', '')
        self.tags = kwargs.get('tags', [])
        self.created = kwargs.get('created', None)
        self.edited = kwargs.get('edited', None)
        self.comments = kwargs.get('comments', [])
        self.likes = kwargs.get('likes', 0)


class CommentSerializer(Serializer):
    
    id = fields.StringField()
    author = fields.StringField()
    content = fields.StringField()
    created = fields.DateTimeField()
    edited = fields.DateTimeField()
    likes = fields.IntegerField()
    views = fields.IntegerField()

    class Meta(object):

        model = Comment


class Post(object):

    def __init__(self, **kwargs):

        self.id = kwargs.get('id', '')
        self.title = kwargs.get('title', '')
        self.author = kwargs.get('author', '')
        self.content = kwargs.get('content', '')
        self.tags = kwargs.get('tags', [])
        self.created = kwargs.get('created', None)
        self.edited = kwargs.get('edit', None)
        self.comments = kwargs.get('comments', [])
        self.likes = kwargs.get('likes', 0)
        self.views = kwargs.get('views', 0)


class PostSerializer(Serializer):
    
    id = fields.StringField()
    title = fields.StringField()
    author = fields.StringField()
    content = fields.StringField()
    created = fields.DateTimeField()
    edited = fields.DateTimeField()
    comments = fields.ListField(CommentSerializer)
    likes = fields.IntegerField()
    views = fields.IntegerField()

    class Meta(object):

        model = Post

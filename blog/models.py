from r2dto import fields, validators, Serializer


class Profile


class Comment(object):

    def __init__(self, **kwargs):

        self.author = kwargs.get('author', '')
        self.content = kwargs.get('content', '')
        self.tags = kwargs.get('tags', [])
        self.created = kwargs.get('created', None)
        self.edited = kwargs.get('edited', None)
        self.comments = kwargs.get('comments', [])
        self.likes = kwargs.get('likes', 0)


class CommentSerializer(Serializer):
    
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

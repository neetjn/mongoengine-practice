"""
sdfs
"""

from r2dto import fields, validators, Serializer


class Post(object):

    def __init__(self, title='', author='', content='', created=None, edited=None, likes=0, views=0):
        self.title = title
        self.author = author
        self.content = content
        self.created = created
        self.edited = edited
        self.views = views


class PostSerializer(Serializer):
    
    title = fields.StringField()
    author = fields.StringField()
    content = fields.StringField()
    created = fields.DateTimeField()
    edited = fields.DateTimeField()
    likes = fields.IntegerField()
    views = fields.IntegerField()

    class Meta:
        model = Post

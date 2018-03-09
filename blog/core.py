from mongoengine import DoesNotExist, ValidationError, MultipleObjectsReturned, NotUniqueError

from blog.db import User, CommentLike, Comment, PostLike, PostView, Post
from blog.errors import ResourceNotFound
from blog.mediatypes import LinkDto, UserDto, UserWithPasswordDto, UserAuthDto, CommentDto, PostViewDto, \
    PostDto


def get_posts(start=None, count=None):
    """
    Fetches collection of post resources.

    :param start: Used for pagination, specify where to start.
    :type start: int
    :param count: Used for pagination, specify number of posts to find.
    :type count: int
    :return: [Post, ...]
    """
    return Post.objects[start:count]


def create_post(author, post_form_dto):
    """
    Creates a new post resource.

    :param author: Post author.
    :type author: User
    :param post_form_dto: Data transfer object with post details.
    :type post_form_dto: PostFormDto
    """
    post = Post()
    post.author = author.author_id
    post.title = post_form_dto.title
    post.content = post_form_dto.title
    post.tags = post_form_dto.tags
    post.save()


def get_post(post_id):
    """
    Fetch existing post resource.

    :param post_id: Identifier of post to fetch.
    :type post_id: str
    :return: Post
    """
    try:
        return Post.objects.get(pk=post_id)
    except (DoesNotExist, ValidationError):
        raise ResourceNotFound()


def edit_post(post_id, post_dto):
    """
    Fetch existing post resource.

    :param post_id: Identifier of post to fetch.
    :type post_id: str
    """
    # TODO: left here
    post = get_post(post_id)
    post.save()


def get_comment(id):
    pass

import datetime
from mongoengine import DoesNotExist, ValidationError, MultipleObjectsReturned, NotUniqueError
from blog.core.users import get_user
from blog.db import Post
from blog.errors import PostNotFoundError
from blog.mediatypes import LinkDto, PostViewDto, PostDto, PostFormDto


# TODO: add method to delete post resources to core utilities

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


def create_post(author_id: str, post_form_dto: PostFormDto):
    """
    Creates a new post resource.

    :param author_id: Post author identifier.
    :type author_id: User
    :param post_form_dto: Data transfer object with post details.
    :type post_form_dto: PostFormDto
    """
    author = get_user(author_id)
    post_time = datetime.datetime.utcnow()
    author.last_activity = post_time
    author.last_posted = post_time
    # create post resource
    post = Post()
    post.author = author.author_id
    post.title = post_form_dto.title
    post.content = post_form_dto.title
    post.tags = post_form_dto.tags
    post.save()


def get_post(post_id: str):
    """
    Fetch existing post resource.

    :param post_id: Identifier of post to fetch.
    :type post_id: str
    :return: Post
    """
    try:
        return Post.objects.get(pk=post_id)
    except (DoesNotExist, ValidationError):
        raise PostNotFoundError()


def edit_post(post_id: str, post_form_dto: PostFormDto):
    """
    Edit existing post resource.

    :param post_id: Identifier of post to edit.
    :type post_id: str
    """
    post = get_post(post_id)
    post.title = post_form_dto.title
    post.description = post_form_dto.description
    post.content = post_form_dto.content
    post.tags = post_form_dto.tags
    post.edited = datetime.datetime.utcnow()
    post.save()

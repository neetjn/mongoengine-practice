import datetime
from mongoengine import DoesNotExist, ValidationError, MultipleObjectsReturned, NotUniqueError
from blog.core.comments import get_post_comments
from blog.core.users import get_user
from blog.db import Post
from blog.errors import PostNotFoundError
from blog.mediatypes import LinkDto, PostViewDto, PostDto, PostFormDto
from blog.utils.crypto import encrypt_content, decrypt_content


def get_posts(start=None, count=None):
    """
    Fetches collection of post resources.

    :param start: Used for pagination, specify where to start.
    :type start: int
    :param count: Used for pagination, specify number of posts to find.
    :type count: int
    :return: [Post, ...]
    """
    posts = Post.objects.get_public()[start:count]
    for post in posts:
        post.description = decrypt_content(post.description)
        post.content = decrypt_content(post.content)
    return posts


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
    post.description = encrypt_content(post_form_dto.description)
    post.content = encrypt_content(post_form_dto.content)
    post.tags = post_form_dto.tags
    post.save()


def get_post(post_id: str) -> Post:
    """
    Fetch existing post resource.

    :param post_id: Identifier of post to fetch.
    :type post_id: str
    :return: Post
    """
    try:
        post = Post.objects.get(pk=post_id)
        post.description = decrypt_content(post.description)
        post.content = decrypt_content(post.content)
        return post
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
    post.description = encrypt_content(post_form_dto.description)
    post.content = encrypt_content(post_form_dto.content)
    post.tags = post_form_dto.tags
    post.private = post_form_dto.private
    post.edited = datetime.datetime.utcnow()
    post.save()


def delete_post(post_id: str):
    """
    Delete existing post resource.

    :param post_id: Identifier of post to delete.
    :type post_id: str
    """
    get_post(post_id).delete()


def post_to_dto(post: Post, href: str = None, comments: bool = True) -> PostDto:
    """
    Converts post resource into data transfer object.

    :param post: Post resource to convert.
    :type post: Post
    :param href: Post resource href link.
    :type href: str
    :param comments: Include post comments.
    :type comments: bool
    :return: PostDto
    """
    return PostDto(
        href=href,
        title=post.title,
        author=get_user(post.author).username,
        content=post.content,
        tags=post.tags,
        private=post.private,
        created=post.created,
        edited=post.edited,
        comments=get_post_comments(post.post_id) if comments else [],
        likes=len(post.likes),
        views=len(post.views))

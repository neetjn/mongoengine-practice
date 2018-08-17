import datetime
import time
from mongoengine import DoesNotExist, ValidationError, MultipleObjectsReturned, NotUniqueError, \
    InvalidQueryError, Q
from blog.core.users import get_user, get_user_comments
from blog.db import Post, PostLike, PostView, PostSearchRequest, Comment, User
from blog.errors import PostNotFoundError, ResourceNotAvailableError
from blog.mediatypes import LinkDto, PostViewDto, PostDto, PostFormDto, CommentFormDto, \
    PostSearchSettingsDto, PostSearchOptions, PostV2Dto
from blog.settings import settings
from blog.utils.crypto import encrypt_content, decrypt_content


def search_posts(post_search_settings: PostSearchSettingsDto, user_id, start: int = None, count: int = None) -> list:
    """
    Search for an existing post resource.

    :param post_search_settings: Post search settings
    :type post_search_settings: PostSearchSettingsDto
    :param user_id: Identifier of user creating search request.
    :type user_id: str
    :param start: Used for pagination, specify where to start.
    :type start: int
    :param count: Used for pagination, specify number of posts to find.
    :type count: int
    """
    post_search_requests = PostSearchRequest.objects(user_id=user_id).order_by('-time')

    # verify post request hasn't been made within provided parameters
    if post_search_requests:
        now = datetime.datetime.utcnow().timestamp()
        if now - post_search_requests[0].time.timestamp() <= settings.post.search_time_delay:
            raise ResourceNotAvailableError()

    # log post search request
    PostSearchRequest(
        user_id=user_id,
        query=post_search_settings.query,
        options=post_search_settings.options).save()

    queries = {}

    if PostSearchOptions.TITLE in post_search_settings.options:
        queries['title__contains'] = post_search_settings.query

    if PostSearchOptions.TAGS in post_search_settings.options:
        queries['tags__contains'] = post_search_settings.query

    try:
        posts = Post.objects(Q(**queries))
    except InvalidQueryError:
        posts = Post.objects()

    # TODO: research how to optimize search queries for encrypted content

    for post in posts:
        post.description = decrypt_content(post.description)
        post.content = decrypt_content(post.content)

    if PostSearchOptions.CONTENT in post_search_settings.options:
        posts = [post for post in posts if post_search_settings.query in post.content]

    if PostSearchOptions.DESCRIPTION in post_search_settings.options:
        posts = [post for post in posts if post_search_settings.query in post.description]

    if PostSearchOptions.AUTHOR in post_search_settings.options:
        try:
            author = User.objects.get(username=post_search_settings.query)
            # filter posts by author username
            posts = [post for post in posts if post.author == str(author.id)]
        except DoesNotExist:
            posts = []

    return posts[start:count]


def get_posts(start=None, count=None) -> list:
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


def create_post(user_id: str, post_form_dto: PostFormDto):
    """
    Creates a new post resource.

    :param user_id: Post author identifier.
    :type user_id: User
    :param post_form_dto: Data transfer object with post details.
    :type post_form_dto: PostFormDto
    """
    author = get_user(user_id)
    post_time = datetime.datetime.utcnow()
    author.last_activity = post_time
    author.last_posted = post_time
    # create post resource
    post = Post()
    post.author = str(author.id)
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
    post.title = post_form_dto.title or post.title
    post.description = encrypt_content(post_form_dto.description) or post.description
    post.content = encrypt_content(post_form_dto.content) or post.content
    post.tags = list(set(post.tags + post_form_dto.tags))
    post.private = post_form_dto.private or post.private
    post.featured = post_form_dto.featured or post.featured
    post.edited = datetime.datetime.utcnow()
    post.save()


def create_post_comment(post_id: str, user_id: str, comment_form_dto: CommentFormDto):
    """
    Create a new comment resource.

    :param post_id: Identifier of post to create new comment for.
    :type post_id: str
    :param user_id: Identifier of user creating comment resource.
    :type user_id: str
    :param comment_form_dto: Comment data transfer object.
    :type comment_form_dto: CommentFormDto
    """
    get_post(post_id) # ensure post exists
    comment = Comment()
    comment.post_id = post_id
    comment.author = user_id
    comment.content = encrypt_content(comment_form_dto.content)
    comment.save()


def view_post(post_id: str, user_id: str, host: str):
    """
    View existing post resource.

    :param post_id:  Identifier of post to view.
    :type post_id: str
    :param user_id: Identifier of user to view post.
    :type user_id: str
    :param host: Host location post was viewed at.
    :type host: str
    """
    get_post(post_id) # ensure post exists
    post_view = PostView.objects(post_id=post_id, user_id=user_id, ip_address=host).order_by('-id').first()
    now = datetime.datetime.utcnow().timestamp()
    if not post_view or now - post_view.seen.timestamp() >= settings.post.view_time_delay:
        PostView(post_id=post_id, user_id=user_id, ip_address=host).save()


def like_post(post_id: str, user_id: str):
    """
    Like or dislike existing post resource.

    :param post_id:  Identifier of post to like or dislike.
    :type post_id: str
    :param user_id: Identifier of user to like or dislike post.
    :type user_id: str
    """
    get_post(post_id) # ensure post exists
    try:
        post_like = PostLike.objects.get(post_id=post_id, user_id=user_id)
    except DoesNotExist:
        PostLike(post_id=post_id, user_id=user_id).save()
    else:
        post_like.delete()


def delete_post(post_id: str):
    """
    Delete existing post resource.

    :param post_id: Identifier of post to delete.
    :type post_id: str
    """
    get_post(post_id).delete()


def get_post_comment_count(post_id: str) -> int:
    """
    Get total number of comments for existing post.

    :param post_id: Identifier of post to pull comments from.
    :type post_id: str
    """
    return Comment.objects(post_id=post_id).count()


def get_post_comments(post_id: str, start: int = None, count: int = None) -> list:
    """
    Fetch collection of comments given post.

    :param post_id: Identifier of post to target.
    :type post_id: str
    :param start: Used for pagination, specify where to start.
    :type start: int
    :param count: Used for pagination, specify number of posts to find.
    :type count: int
    :return: [Comment, ...]
    """
    comments = Comment.objects(post_id=post_id)[start:count]
    for comment in comments:
        comment.content = decrypt_content(comment.content)
    return comments


def get_user_posts(user_id: str, start: int = None, count: int = None) -> list:
    """
    Find all posts by given user.

    :param user_id: Identifier of user.
    :type user_id: str
    :param start: Used for pagination, specify where to start.
    :type start: int
    :param count: Used for pagination, specify number of posts to find.
    :type count: int
    :return: [Post, ...]
    """
    return Post.objects.get(author=user_id)[start:count]


def get_user_liked_posts(user_id: str, start: int = None, count: int = None) -> list:
    """
    Find all posts liked by given user.

    :param user_id: Identifier of user.
    :type user_id: str
    :param start: Used for pagination, specify where to start.
    :type start: int
    :param count: Used for pagination, specify number of posts to find.
    :type count: int
    :return: [Post, ...]
    """
    post_likes = PostLike.objects(user_id=user_id)[start:count]
    return [Post.objects.get(post_id=pl.post_id) for pl in post_likes]


def post_to_dto(post: Post, href: str = None, links: list = None) -> PostDto:
    """
    Converts post resource into data transfer object.

    :param post: Post resource to convert.
    :type post: Post
    :param href: Post resource href link.
    :type href: str
    :param links: Post resource links.
    :type links: list
    :return: PostDto
    """
    post_id = str(post.id)
    likes = PostLike.objects(post_id=post_id).count()
    views = PostView.objects(post_id=post_id).count()
    return PostDto(
        href=href,
        links=links or [],
        author=get_user(post.author).full_name,
        title=post.title,
        description=post.description,
        content=post.content,
        tags=post.tags,
        private=post.private,
        featured=post.featured,
        created=post.created,
        edited=post.edited,
        likes=likes,
        views=views)


def post_to_v2_dto(post: Post, href: str = None, links: list = None) -> PostDto:
    """
    Converts post resource into data transfer object.

    :param post: Post resource to convert.
    :type post: Post
    :param href: Post resource href link.
    :type href: str
    :param links: Post resource links.
    :type links: list
    :return: PostV2Dto
    """
    post_id = str(post.id)
    likes = PostLike.objects(post_id=post_id).count()
    views = PostView.objects(post_id=post_id).count()
    comments = Comment.objects(post_id=post_id).count()
    return PostV2Dto(
        href=href,
        links=links or [],
        author=get_user(post.author).full_name,
        title=post.title,
        description=post.description,
        content=post.content,
        comments=comments,
        tags=post.tags,
        private=post.private,
        featured=post.featured,
        created=post.created,
        edited=post.edited,
        likes=likes,
        views=views)

import boto3
import datetime
import io
import time
from mongoengine import DoesNotExist, ValidationError, MultipleObjectsReturned, NotUniqueError
from mongoengine.queryset.visitor import Q
from blog.constants BLOG_AWS_ACCESS_KEY_ID, BLOG_AWS_SECRET_ACCESS_KEY, BLOG_AWS_S3_BUCKET
from blog.db import User, FailedLogin, Comment, Post
from blog.errors import UserNotFoundError, UserExistsError, UserForbiddenRequestError
from blog.mediatypes import UserProfileDto, UserAuthDto, UserFormDto, UserRoles
from blog.settings import settings
from blog.utils.crypto import hash_password, compare_passwords, encrypt_content, decrypt_content


def authenticate(user_auth_dto: UserAuthDto, client: str) -> User:
    """
    Validates user login credentials.

    :param user_auth_dto: User login credentials.
    :type user_auth_dto: UserAuthDto
    :param client: Access route from client (ip address).
    :type client: str
    :return: User
    """
    try:
        user = User.objects.get(username=user_auth_dto.username)
        rfl = FailedLogin.objects(username=user_auth_dto.username, ip_address=client).order_by('-time')[5:]
        now = datetime.datetime.utcnow().timestamp()
        failed_logins = [
            fl for fl in rfl if now - fl.time.timestamp() <= settings.login.failed_login_timeout]
        if len(failed_logins) >= 5:
            raise UserForbiddenRequestError()
        if compare_passwords(user.password, user_auth_dto.password, user.salt):
            return user
        # create new failed login document
        FailedLogin(username=user_auth_dto.username, ip_address=client).save()
        return None
    except (DoesNotExist):
        raise UserNotFoundError()


def get_users(start=None, count=None):
    """
    Fetch collection of user resources.

    :param start: Used for pagination, specify where to start.
    :type start: int
    :param count: Used for pagination, specify number of posts to find.
    :type count: int
    :return: [User, ...]
    """
    return User.objects[start:count]


def create_user(user_form_dto: UserFormDto) -> User:
    """
    Creates a new user resource.

    :param user_form_dto: Data transfer object with user details.
    :type user_form_dto: UserFormDto
    :return: User
    """
    try:
        User.objects.get(Q(username=user_form_dto.username) | Q(email=user_form_dto.email))
    except DoesNotExist:
        user = User()
        user.username = user_form_dto.username
        user.avatar_href = user_form_dto.avatar_href
        password, salt = hash_password(user_form_dto.password)
        user.password = password
        user.salt = salt
        user.full_name = user_form_dto.full_name
        user.email = user_form_dto.email
        user.role = UserRoles.BLOGGER
        user.save()
        return user
    else:
        raise UserExistsError()


def get_user(user_id: str) -> User:
    """
    Fetches existing user resource.

    :param user_id: Identifier of user to fetch.
    :type user_id: str
    """
    try:
        return User.objects.get(pk=user_id)
    except (DoesNotExist, ValidationError):
        raise UserNotFoundError()


def edit_user(user_id: str, user_form_dto: UserFormDto):
    """
    Edit existing user resource.

    :param user_id: Identifier of user to edit.
    :type user_id: str
    :param user_form_dto: Data transfer object wirh user details.
    :type user_form_dto: UserFormDto
    """
    user = get_user(user_id)
    if user_form_dto.password:
        password, salt = hash_password(user_form_dto.password)
        user.password = password
        user.salt = salt
    user.full_name = user_form_dto.full_name or user.full_name
    user.email = user_form_dto.email or user.email
    if user_form_dto.avatar_href and user_form_dto.avatar_href != user.avatar_href:
        user.avatar_href = user_form_dto.avatar_href
        user.avatar_binary = user.avatar_binary.delete()
    user.save()


def store_user_avatar(user_id: str, file: io.BufferedReader, content_type: str):
    """
    Store user avatar image.

    :param user_id: Identifier of target user.
    :type user_id: str
    :param file: Avatar to store.
    :type file: BufferReader
    :param content_type: Avatar filetype.
    :type content_type: str
    """
    user = get_user(user_id)
    if user.avatar_href:
        user.avatar_href = None
    user.avatar_binary.delete()
    user.avatar_binary.put(file, content_type=content_type)
    user.save()


def delete_user_avatar(user_id: str):
    """
    Delete user avatar.

    :param user_id: Identifier of target user.
    :type user_id: str
    """
    user = get_user(user_id)
    if user.avatar_href:
        user.avatar_href = None
    if user.avatar_binary:
        user.avatar_binary.delete()
    user.save()


def get_user_posts(user_id: str, start: int = None, count: int = None):
    """
    Find all posts belonging to given user.

    :param user_id: Identifier of author.
    :type user_id: str
    :param start: Used for pagination, specify where to start.
    :type start: int
    :param count: Used for pagination, specify number of posts to find.
    :type count: int
    :return: [Post, ...]
    """
    posts = Post.objects(author=user_id)[start:count]
    for post in posts:
        post.description = decrypt_content(post.description)
        post.content = decrypt_content(post.content)
    return posts


def get_user_comments(user_id: str, start: int = None, count: int = None):
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
    comments = Comment.objects(author=user_id)[start:count]
    for comment in comments:
        comment.content = decrypt_content(comment.content)
    return comments


def user_to_dto(user: User, comments: bool = True) -> UserProfileDto:
    """
    Converts user resource to data transfer object.

    :param user: User resource to convert.
    :type user: User
    :param comments: Include user comments.
    :type comments: bool
    :return: UserProfileDto
    """
    return UserProfileDto(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        last_posted=user.last_posted,
        last_activity=user.last_activity,
        register_date=user.register_date)

import datetime
import time
from mongoengine import DoesNotExist, ValidationError, MultipleObjectsReturned, NotUniqueError
from mongoengine.queryset.visitor import Q
from blog.constants import BLOG_MAX_FAILED_LOGIN, BLOG_FAILED_LOGIN_TIMEOUT
from blog.core.comments import get_user_comments
from blog.db import User, FailedLogin
from blog.errors import UserNotFoundError, UserExistsError, UserForbiddenRequest
from blog.mediatypes import UserProfileDto, UserAuthDto, UserFormDto, UserRoles
from blog.utils.crypto import hash_password, compare_passwords


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
        user = User.objects.get(username=user_auth_dto.username, ip_address=client)
        rfl = FailedLogin.objects(username=user_auth_dto.username)[-1 * BLOG_MAX_FAILED_LOGIN:None]
        now = int(time.time())
        failed_logins = [fl for fl in rfl if now - time.mktime(fl.time.timetuple()) > BLOG_FAILED_LOGIN_TIMEOUT]
        if len(failed_logins) >= 5:
            raise UserForbiddenRequest()
        if compare_passwords(user.password, user_auth_dto.password, user.salt):
            return user
        # create new failed login document
        FailedLogin(username=user_auth_dto.username, ip_address=client).save()
        return None
    except (DoesNotExist, ValidationError):
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
        user.passord = password
        user.salt = salt
        user.full_name = user_form_dto.full_name
        user.email = user_form_dto.email
        user.role = UserRoles.blogger
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
    user.full_name = user_form_dto.full_name
    user.email = user_form_dto.email
    user.save()


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

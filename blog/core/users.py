import datetime
from mongoengine import DoesNotExist, ValidationError, MultipleObjectsReturned, NotUniqueError
from mongoengine.queryset.visitor import Q
from blog.db import User
from blog.errors import UserNotFoundError, UserExistsError
from blog.mediatypes import UserDto, UserFormDto, UserRoles
from blog.utils import hash_password


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


def create_user(user_form_dto):
    """
    Creates a new user resource.

    :param user_form_dto: Data transfer object with user details.
    :type user_form_dto: UserFormDto
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
    else:
        raise UserExistsError()


def get_user(user_id):
    """
    Fetches existing user resource.

    :param user_id: Identifier of user to fetch.
    :type user_id: str
    """
    try:
        return User.objects.get(pk=user_id)
    except (DoesNotExist, ValidationError):
        raise UserNotFoundError()


def edit_user(user_id, user_form_dto):
    """
    Edit existing user resource.

    :param user_id: Identifier of user to edit.
    :type user_id: str
    :param user_form_dto: Data transfer object wirh user details.
    :type user_form_dto: UserFormDto
    """
    user = get_user(user_id)
    user.save()

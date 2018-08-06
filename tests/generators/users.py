from blog.mediatypes import UserFormDto
from blog.settings import settings
from tests.utils import random_string, random_email


def generate_user_form_dto(**kwargs) -> UserFormDto:
    """Generate a user form"""
    return UserFormDto(
        username=kwargs.get('username', random_string(settings.rules.user.username_min_char)),
        full_name=kwargs.get('name', random_string(settings.rules.user.name_min_char)),
        avatar_href=kwargs.get('avatar_href', random_string(10)),
        password=kwargs.get('password', random_string(settings.rules.user.password_min_char)),
        email=kwargs.get('email', random_email()))

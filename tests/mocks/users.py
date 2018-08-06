import copy
import datetime
import jwt
from blog.constants import BLOG_JWT_SECRET_KEY
from blog.mediatypes import UserFormDtoSerializer
from blog.resources.users import UserRegistrationResource
from blog.settings import settings, save_settings
from blog.utils.serializers import to_json
from tests.generators.users import generate_user_form_dto


def create_auth_token(user_id: str, time_of_creation: str, host: str) -> str:
    """
    Construct jwt for authentication.

    :param user_id: User identifier for authentication token.
    :type user_id: str
    :param time_of_creation: Time of token's creation to serialize.
    :type time_of_creation: int
    :param host: Remote host to bind token to.
    :type host: str
    """
    return jwt.encode(
        {'user': str(user_id), 'created': time_of_creation, 'host': host},
        BLOG_JWT_SECRET_KEY,
        algorithm='HS256').decode('utf-8')


def create_user(instance, **kwargs) -> str:
    """
    Generate random user.

    :param instance: Falcon test case instance.
    :type instanace: TestCase
    :return: (str, str)
    """
    global settings
    original_settings = copy.deepcopy(settings)
    settings.user.allow_manual_registration = True
    save_settings(settings, False)
    user_form_dto = generate_user_form_dto(**kwargs)
    res = instance.simulate_post(
        UserRegistrationResource.route,
        body=to_json(UserFormDtoSerializer, user_form_dto))
    token = res.json.get('token')
    settings = original_settings
    save_settings(settings)
    return user_form_dto, token

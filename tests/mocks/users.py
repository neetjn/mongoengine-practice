import copy
from blog.mediatypes import UserFormDtoSerializer
from blog.resources.users import UserRegistrationResource
from blog.settings import settings, save_settings
from blog.utils.serializers import to_json
from tests.generators.users import generate_user_form_dto


def create_user(instance, **kwargs) -> str:
    """
    Generate random user.

    :param instance: Falcon test case instance.
    :type instanace: TestCase
    :return: str
    """
    global settings
    original_settings = copy.deepcopy(settings)
    settings.user.allow_manual_registration = True
    save_settings(settings)
    user_form_dto = generate_user_form_dto(**kwargs)
    res = instance.simulate_post(
        UserRegistrationResource.route,
        body=to_json(UserFormDtoSerializer, user_form_dto))
    token = res.json.get('token')
    settings = original_settings
    save_settings(settings)
    return token

import json
import yaml
from r2dto import fields, Serializer
from blog.utils.serializers import from_json, to_json


__all__ = ['Settings', 'SettingsSerializer', 'settings', 'save_settings']


class LoginSettings(object):
    def __init__(self):
        self.max_failed_login = 0
        self.failed_login_timeout = 0
        self.max_session_time = 0


class PostSettings(object):
    def __init__(self):
        self.view_time_delay = 0


class PostSettingsSerializer(Serializer):
    view_time_delay = fields.IntegerField(required=True)

    class Meta(object):
        model = PostSettings


class LoginSettingsSerializer(Serializer):
    max_failed_login = fields.IntegerField(required=True)
    failed_login_timeout = fields.IntegerField(required=True)
    max_session_time = fields.IntegerField(required=True)

    class Meta(object):
        model = LoginSettings


class UserRules(object):
    def __init__(self):
        self.username_min_char = 0
        self.username_max_char = 0
        self.name_min_char = 0
        self.name_max_char = 0


class UserRulesSerializer(Serializer):
    username_min_char = fields.IntegerField(required=True)
    username_max_char = fields.IntegerField(required=True)
    name_min_char = fields.IntegerField(required=True)
    name_max_char = fields.IntegerField(required=True)

    class Meta(object):
        model = UserRules


class PostRules(object):
    def __init__(self):
        self.title_min_char = 0
        self.title_max_char = 0
        self.content_min_char = 0
        self.content_max_char = 0


class PostRulesSerializer(Serializer):
    title_min_char = fields.IntegerField(required=True)
    title_max_char = fields.IntegerField(required=True)
    content_min_char = fields.IntegerField(required=True)
    content_max_char = fields.IntegerField(required=True)

    class Meta(object):
        model = PostRules


class CommentRules(object):
    def __init__(self):
        self.content_min_char = 0
        self.content_max_char = 0


class CommentRulesSerializer(Serializer):
    content_min_char = fields.IntegerField(required=True)
    content_max_char = fields.IntegerField(required=True)

    class Meta(object):
        model = CommentRules


class Rules(object):
    def __init__(self):
        self.user = UserRules()
        self.post = PostRules()
        self.comment = CommentRules()


class RulesSerializer(Serializer):
    user = fields.ObjectField(UserRulesSerializer, required=True)
    post = fields.ObjectField(PostRulesSerializer, required=True)
    comment = fields.ObjectField(CommentRulesSerializer, required=True)

    class Meta(object):
        model = Rules


class Settings(object):
    def __init__(self):
        self.login = LoginSettings()
        self.post = PostSettings()
        self.rules = Rules()


class SettingsSerializer(Serializer):
    login = fields.ObjectField(LoginSettingsSerializer, required=True)
    post = fields.ObjectField(PostSettingsSerializer, required=True)
    rules = fields.ObjectField(RulesSerializer, required=True)

    class Meta(object):
        model = Settings


with open('blog/settings.yml', 'r') as data:
    s = SettingsSerializer(data=yaml.load(data.read()))
    s.validate()
    # settings object will be stored in memory from first import
    # any changes will effect entire api instantly
    # to retain changes, use save_settings
    settings = s.object


def save_settings(settings_dto: Settings):
    """
    Saves local settings given provided settings object.

    :param settings_dto: Settings data transfer object.
    :type settings_dto: Settings
    """
    global settings

    # login settings
    settings.login.max_failed_login = settings_dto.login.max_failed_login
    settings.login.failed_login_timeout = settings_dto.login.failed_login_timeout
    settings.login.max_session_time = settings_dto.login.max_session_time
    # post settings
    settings.post.view_time_delay = settings_dto.post.view_time_delay
    # user rules
    settings.rules.user.username_min_char = settings_dto.rules.user.username_min_char
    settings.rules.user.username_max_char = settings_dto.rules.user.username_max_char
    settings.rules.user.name_min_char = settings_dto.rules.user.name_min_char
    settings.rules.user.name_max_char = settings_dto.rules.user.name_max_char
    # post rules
    settings.rules.post.title_min_char = settings_dto.rules.post.title_min_char
    settings.rules.post.title_max_char = settings_dto.rules.post.title_max_char
    settings.rules.post.content_min_char = settings_dto.rules.post.content_min_char
    settings.rules.post.content_max_char = settings_dto.rules.post.content_max_char
    # comment rules
    settings.rules.comment.content_min_char = settings_dto.rules.comment.content_min_char
    settings.rules.comment.content_max_char = settings_dto.rules.comment.content_max_char

    with open('blog/settings.yml', 'w') as data:
        s = SettingsSerializer(object=settings)
        s.validate()
        data.write(yaml.dump(s.data, default_flow_style=False))

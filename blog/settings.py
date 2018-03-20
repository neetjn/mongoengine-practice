import json
import yaml
from r2dto import fields, Serializer
from blog.utils.serializers import from_json, to_json


__all__ = ['Settings', 'SettingsSerializer', 'get_settings', 'set_settings']


class LoginSettings(object):
    def __init__(self):
        self.max_failed_login = 0
        self.failed_login_timeout = 0


class LoginSettingsSerializer(Serializer):
    max_failed_login = fields.IntegerField()
    failed_login_timeout = fields.IntegerField()

    class Meta(object):
        model = LoginSettings


class UserRules(object):
    def __init__(self):
        self.username_min_char = 0
        self.username_max_char = 0
        self.name_min_char = 0
        self.name_max_char = 0


class UserRulesSerializer(Serializer):
    username_min_char = fields.IntegerField()
    username_max_char = fields.IntegerField()
    name_min_char = fields.IntegerField()
    name_max_char = fields.IntegerField()

    class Meta(object):
        model = UserRules


class PostRules(object):
    def __init__(self):
        self.title_min_char = 0
        self.title_max_char = 0
        self.content_min_char = 0


class PostRulesSerializer(Serializer):
    title_min_char = fields.IntegerField()
    title_max_char = fields.IntegerField()
    content_min_char = fields.IntegerField()

    class Meta(object):
        model = PostRules


class CommentRules(object):
    def __init__(self):
        self.content_min_char = 0
        self.content_max_char = 0


class CommentRulesSerializer(Serializer):
    content_min_char = fields.IntegerField()
    content_max_char = fields.IntegerField()

    class Meta(object):
        model = CommentRules


class Rules(object):
    def __init__(self):
        self.user = UserRules()
        self.post = PostRules()
        self.comment = CommentRules()


class RulesSerializer(Serializer):
    user = fields.ObjectField(UserRulesSerializer)
    post = fields.ObjectField(PostRulesSerializer)
    comment = fields.ObjectField(CommentRulesSerializer)

    class Meta(object):
        model = Rules


class Settings(object):
    def __init__(self):
        self.login = LoginSettings()
        self.rules = Rules()


class SettingsSerializer(Serializer):
    login = fields.ObjectField(LoginSettingsSerializer)
    rules = fields.ObjectField(RulesSerializer)

    class Meta(object):
        model = Settings


def get_settings() -> Settings:
    """Fetches local settings and returns serialized object."""
    with open('blog/settings.yml', 'r') as data:
        raw = yaml.load(data.read())
    settings = SettingsSerializer(data=raw)
    settings.validate()
    return settings.object


def set_settings(settings: Settings):
    """
    Saves local settings given provided settings object.

    :param settings: Settings object to deserialize and save.
    :type settings: Settings
    """
    with open('blog/settings.yml', 'w') as data:
        s = SettingsSerializer(object=settings)
        s.validate()
        data.write(yaml.dump(s.data), default_flow_style=False)
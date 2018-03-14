import re
from r2dto import Serializer, ValidationError
from blog.constants import EMAIL_REGEX


class RegexValidator(object):

    def __init__(self, pattern: str, message=None):
        """
        Regex validator for r2dto serializer fields.

        :param pattern: Regex pattern to use.
        :type pattern: str
        :type message: Custom validation error message.
        :type message: str
        """
        self.pattern = pattern
        self.message = message

    def validate(self, field, data):
        if not re.match(self.pattern, data):
            raise ValidationError(self.message or
                f'Field "{field.name}" value "{data}"'
                ' does not match the provided field constraints.')


class EmailValidator(object):
    """
    Email validator for r2dto serializer fields.
    """
    def validate(self, field, data):
        if not re.match(EMAIL_REGEX, data):
            raise ValidationError('"f{data}" is not a valid email.')


class CharLenValidator(object):

    def __init__(self, min: int, max: int):
        """
        Character length validator for r2dto serializer fields.

        :param min: Minimum character length for field value.
        :type min: int
        :param max: Maximum character length for field value.
        :type max: int
        """
        self.min = min
        self.max = max

    def validate(self, field, data):
        size = len(data)
        if size < self.min or size > self.max:
            raise ValidationError(
                '"{field.name}" must be greater than or equal to {self.min}'
                ' or less than or equal to {self.max} in length.')

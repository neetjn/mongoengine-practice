import hashlib
from uuid import uuid4
from Crypto.Cipher import AES
from r2dto import Serializer
from blog.constants import EMAIL_REGEX, BLOG_CONTENT_KEY


def to_json(serializer: Serializer, dto: object):
    """
    Serializes data transfer object with r2dto.

    :param serialier: r2dto serializer definition.
    :type serializer: Serializer
    :param dto: Data transfer object to serialize.
    :type dto: object
    """
    base = serializer(object=dto)
    base.validate()
    return base.data


def from_json(serializer: Serializer, payload: str):
    """
    Deserializes json into data transfer object.

    :param serialier: r2dto serializer definition.
    :type serializer: Serializer
    :param payload: Payload to deserialize.
    :type payload: str
    """
    base = serializer(data=payload)
    base.validate()
    return base.object


def encrypt_content(content: str):
    pass


def decrypt_content(content: str):
    pass


def hash_password(password: str):
    """
    Hashes password with a randomly generated salt value.

    :param password: Plain text password to hash.
    :type password: str
    :return: (hashed_password, salt)
    """
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha256(password + salt).hexdigest()
    return (hashed_password, salt)


class EmailValidator(object):
    """
    Email validator for r2dto serializer fields.

    :param field:
    :type field:
    :param data:
    :type data:
    """
    def validate(self, field, data):
        if not re.match(EMAIL_REGEX, data):
            raise ValidationError('"f{data}" is not a valid email.')


class CharLenValidator(object):
    """
    Character length validator for r2dto serializer fields.
    """
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def validate(self, field, data):
        size = len(data)
        if size < self.min or size > self.max:
            raise ValidationError(
                '"{field.name}" must be greater than or equal to {self.min}'
                ' or less than or equal to {self.max} in length.')

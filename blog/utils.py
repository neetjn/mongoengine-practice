import hashlib
import re
from uuid import uuid4
from r2dto import Serializer, ValidationError
from blog.constants import EMAIL_REGEX, BLOG_CONTENT_KEY
from blog.crypto import AESCipher


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


def hash_password(password: str):
    """
    Hashes password with a randomly generated salt value.

    :param password: Plain text password to hash.
    :type password: str
    :return: (hashed_password, salt)
    """
    salt = uuid4().hex
    hashed_password = hashlib.sha256(password + salt).hexdigest()
    return (hashed_password, salt)


def encrypt_content(content: str):
    """
    Encrypt blog post and comment content.

    :param content: Blog content to encrypt.
    :type content: str
    """
    return AESCipher(BLOG_CONTENT_KEY).encrypt(content)


def decrypt_content(content: str):
    """
    Decrypt blog post and comment content.

    :param content: Blog content to decrypt.
    :type content: str
    """
    return AESCipher(BLOG_CONTENT_KEY).encrypt(content)


class EmailValidator(object):
    """
    Email validator for r2dto serializer fields.
    """
    def validate(self, field, data):
        if not re.match(EMAIL_REGEX, data):
            raise ValidationError('"f{data}" is not a valid email.')


class CharLenValidator(object):
    """
    Character length validator for r2dto serializer fields.

    :param min: Minimum character length for field value.
    :type min: int
    :param max: Maximum character length for field value.
    :type max: int
    """
    def __init__(self, min: int, max: int):
        self.min = min
        self.max = max

    def validate(self, field, data):
        size = len(data)
        if size < self.min or size > self.max:
            raise ValidationError(
                '"{field.name}" must be greater than or equal to {self.min}'
                ' or less than or equal to {self.max} in length.')

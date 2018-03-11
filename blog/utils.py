from blog.constants import EMAIL_REGEX


def to_json(serializer, dto):
    """
    Serializes data transfer object with r2dto.

    :param serialier: r2dto serializer definition.
    :param dto: Data transfer object to serialize.
    """
    base = serializer(object=dto)
    base.validate()
    return base.data

def from_json(serializer, payload):
    """
    Deserializes json into data transfer object.

    :param serialier: r2dto serializer definition.
    :param payload: Payload to deserialize.
    """
    base = serializer(data=payload)
    base.validate()
    return base.object


class EmailValidator(object):

    def validate(self, field, data):
        if not re.match(EMAIL_REGEX, data):
            raise ValidationError('"f{data}" is not a valid email.')

class CharLengthValidator(object):

    def validate(self, field, data):

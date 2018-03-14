from r2dto import Serializer


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

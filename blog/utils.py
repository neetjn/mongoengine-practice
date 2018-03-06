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

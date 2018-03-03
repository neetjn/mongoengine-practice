def to_json(serializer, dto):
    """
    Serializes data transfer object with r2dto.

    :param serialier: r2dto serializer definition.
    :param dto: Data transfer object to serialize.
    """
    base = serializer(object=dto)
    base.validate()
    return base.data

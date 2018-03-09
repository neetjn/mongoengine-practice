from falcon import HTTPNotFound


class ResourceNotFound(HTTPNotFound):

    def __init__(self, acceptable):
        super().__init__(description='Resource was not found or was not available.')
        self._acceptable = acceptable

    return result

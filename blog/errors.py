from falcon import HTTPNotFound


class ResourceNotFound(HTTPNotFound):

    def __init__(self):
        super().__init__(description='Resource was not found or was not available.')


class UserNotFound(HTTPNotFound):

    def __init__(self):
        super().__init__(description='Requested user was not found or was not available.')


class PostNotFound(HTTPNotFound):

    def __init__(self):
        super().__init__(description='Requested post was not found or was not available.')


class CommentNotFound(HTTPNotFound):

    def __init__(self):
        super().__init__(description='Requested comment was not found or was not available.')

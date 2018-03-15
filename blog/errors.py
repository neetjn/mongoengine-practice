from falcon import HTTPNotFound, HTTPConflict


class ResourceNotFoundError(HTTPNotFound):

    def __init__(self):
        super().__init__(description='Resource was not found or was not available.')


class UserNotFoundError(HTTPNotFound):

    def __init__(self):
        super().__init__(description='Requested user was not found or was not available.')

class UserExistsError(HTTPConflict):

    def __init__(self):
        super().__init__(description='User resource by username or email already exists')


class PostNotFoundError(HTTPNotFound):

    def __init__(self):
        super().__init__(description='Requested post was not found or was not available.')


class CommentNotFoundError(HTTPNotFound):

    def __init__(self):
        super().__init__(description='Requested comment was not found or was not available.')

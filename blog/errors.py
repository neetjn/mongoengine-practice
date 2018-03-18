from falcon import HTTPNotFound, HTTPConflict, HTTPUnauthorized, HTTPForbidden


class UserForbiddenRequest(HTTPForbidden):

    def __init__(self):
        super().__init__(
            description='User has been temporarily disabled due to failed logins.'
                        'Try again at a later time.')


class UnauthorizedRequest(HTTPUnauthorized):

    def __init__(self, user=None):
        super().__init__(
            description=f'User "{user.username}" is not authorized for this resource.' if user else
                         'Requested resource requires user authentication.')


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

import traceback

from blog.utils.logger import critical
from falcon import HTTPNotFound, HTTPConflict, HTTPUnauthorized, HTTPForbidden, \
    HTTPBadRequest, HTTPInternalServerError


class ErrorHandler:

    @staticmethod
    def http(ex, req, resp, params):
        raise

    @staticmethod
    def unexpected(ex, req, resp, params):
        ex_msg = ''.join(traceback.format_tb(ex.__traceback__))
        raise HTTPInternalServerError(ex.__class__.__name__, ex_msg)


class UserForbiddenRequestError(HTTPForbidden):

    def __init__(self):
        super().__init__(
            description='User has been temporarily disabled due to failed logins. '
                        'Try again at a later time.')


class UnauthorizedRequestError(HTTPUnauthorized):

    def __init__(self, user=None):
        super().__init__(
            description=f'User "{user.username}" is not authorized for this resource.' if user else
                         'Requested resource requires user authentication.')


class ResourceNotAvailableError(HTTPForbidden):

    def __init__(self):
        super().__init__(
            description='Resource is not available. '
                        'Try again at a later time.')


class ResourceNotFoundError(HTTPNotFound):

    def __init__(self):
        super().__init__(description='Resource was not found or was not available.')


class UserNotFoundError(HTTPNotFound):

    def __init__(self):
        super().__init__(description='Requested user was not found or was not available.')

class UserExistsError(HTTPConflict):

    def __init__(self):
        super().__init__(description='User resource by username or email already exists.')


class UserAvatarUploadError(HTTPBadRequest):

    def __init__(self):
        super().__init__(description='Provided avatar image does not follow expected contraints.')


class PostNotFoundError(HTTPNotFound):

    def __init__(self):
        super().__init__(description='Requested post was not found or was not available.')


class CommentNotFoundError(HTTPNotFound):

    def __init__(self):
        super().__init__(description='Requested comment was not found or was not available.')

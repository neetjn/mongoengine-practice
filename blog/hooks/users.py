from blog.errors import ResourceNotAvailableError, UnauthorizedRequestError
from blog.mediatypes import UserRoles


def is_logged_out(req, resp, resource, params):
    """Ensure request is being made from an unauthorized user."""
    if req.context.get('user'):
        raise ResourceNotAvailableError()


def is_logged_in(req, resp, resource, params):
    """Ensure request is being made from authorized user."""
    if not req.context.get('user'):
        raise UnauthorizedRequestError()


def is_admin(req, resp, resource, params):
    """Ensure request is being made from authorized user."""
    user = req.context.get('user')
    if not user or user.role != UserRoles.ADMIN:
        raise UnauthorizedRequestError()


def is_moderator(req, resp, resource, params):
    """Ensure request is being made from authorized user."""
    user = req.context.get('user')
    if not user or not (user.role == UserRoles.ADMIN or user.role == UserRoles.MODERATOR):
        raise UnauthorizedRequestError()

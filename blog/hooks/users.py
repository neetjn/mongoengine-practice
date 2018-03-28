from blog.errors import UnauthorizedRequest
from blog.mediatypes import UserRoles


def is_logged_in(req, resp, resource, params):
    """Ensure request is being made from authorized user."""
    if not req.context.get('user'):
        raise UnauthorizedRequest()


def is_admin(req, resp, resource, params):
    """Ensure request is being made from authorized user."""
    user = req.context.get('user')
    if not user or user.role != UserRoles.ADMIN:
        raise UnauthorizedRequest()


def is_moderator(req, resp, resource, params):
    """Ensure request is being made from authorized user."""
    user = req.context.get('user')
    if not user or not (user.role == UserRoles.ADMIN or user.role == UserRoles.MODERATOR):
        raise UnauthorizedRequest()

from blog.errors import UnauthorizedRequest


def require_login(req, resp, resource, params):
    """Ensure request is being made from authorized user."""
    if not req.context.get('user'):
        raise UnauthorizedRequest()

import jwt
from blog.constants import BLOG_JWT_SECRET_KEY
from blog.core.errors import UserNotFoundError
from blog.core.users import get_user
from blog.utils.logger import debug, warning


class UserProcessor(object):

    # Note: RFC6648 recommends application headers prefixed with 'X-'
    # should be depracated
    # Source: https://tools.ietf.org/html/rfc6648

    def process_request(self, req, resp):
        """
        Process the request for user session before routing it.

        param req: Request object that will have user details
        attached to it.
        """
        payload = jwt.decode(req.auth, BLOG_JWT_SECRET_KEY, algorithms=['HS256']) if req.auth else None
        if payload:
            try:
                # add our user to the request context
                req.context.set_default('user', get_user(payload['userId']))
            except UserNotFoundError:
                warning(req, 'JWT payload found with invalid username.')

        req.blog_user = None

import time
import jwt
from blog.constants import BLOG_JWT_SECRET_KEY
from blog.errors import UserNotFoundError, UnauthorizedRequest
from blog.core.users import get_user
from blog.settings import settings
from blog.utils.logger import debug, warning


class UserProcessor(object):

    def process_resource(self, req, resp, resource, params):
        """Process the request for user session before routing it."""

        # Note: RFC6648 recommends application headers prefixed with 'X-'
        # should be depracated
        # Source: https://tools.ietf.org/html/rfc6648

        host = req.access_route[0]
        payload = jwt.decode(req.auth, BLOG_JWT_SECRET_KEY, algorithms=['HS256']) if req.auth else None
        if payload:
            if payload.get('host') != host:
                warning(req, 'JWT host "{}" does not match the requestee "{}"'.format(payload.get('host'), host))
                raise UnauthorizedRequest()
            elif int(payload.get('created')) + (60 * settings.login.max_session_time) <= time.time():
                warning(req, 'JWT created over {} hours ago.'.format(settings.login.max_session_time_hours))
            else:
                user_id = payload.get('user')
                try:
                    # add our user to the request context
                    user = get_user(user_id)
                    req.context.setdefault('user', user)
                except UserNotFoundError:
                    warning(req, f'JWT payload found with invalid user identifier "{user_id}".')
                    raise UnauthorizedRequest()

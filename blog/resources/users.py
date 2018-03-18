import jwt
import falcon
from blog.core.users import authenticate, get_user
from blog.mediatypes import TokenDto, TokenDtoSerializer


class UserLogin(object):

    def on_get(self, req, resp):
        # TODO: finish authentication, add jwt generation and return as serialized token
        resp.status = falcon.HTTP_200


class UserResource(object):

    def on_get(self, req, resp):
        """Fetch single post resource."""
        resp.status = falcon.HTTP_200
        resp.body = ''

    def on_put(self, req, resp):
        """Update single post resource."""
        resp.status = falcon.HTTP_204
        resp.body = ''

    def on_delete(self, req, resp):
        """Delete single post resource."""
        resp.status = falcon.HTTP_204
        resp.body = ''

import jwt
import falcon
from blog.constants import BLOG_JWT_SECRET_KEY
from blog.core.users import authenticate, get_user
from blog.mediatypes import UserAuthDtoSerializer, TokenDto, TokenDtoSerializer
from blog.utils.serializers import from_json, to_json


class UserLogin(object):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        payload = req.stream.read()
        user = authenticate(from_json(UserAuthDtoSerializer, payload), req.access_route)
        if user:
            jwt_token = jwt.encode({'user': ''}, BLOG_JWT_SECRET_KEY, algorithm='HS256')
            resp.body = to_json(TokenDtoSerializer, TokenDto(token=jwt_token))
        else:
            resp.body = 'false'


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

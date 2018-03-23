import time
import jwt
import falcon
from blog.constants import BLOG_JWT_SECRET_KEY
from blog.core.comments import comment_to_dto
from blog.db import User
from blog.core.posts import get_user_liked_posts, post_to_dto
from blog.core.users import authenticate, get_user, create_user, edit_user, \
    user_to_dto, get_user_comments
from blog.hooks.users import require_login
from blog.mediatypes import UserAuthDtoSerializer, UserFormDtoSerializer, TokenDto, \
    TokenDtoSerializer, UserProfileDtoSerializer
from blog.resources.base import BaseResource
from blog.resources.comments import CommentResource
from blog.resources.posts import PostResource
from blog.utils.serializers import from_json, to_json


def get_auth_jwt(user: User) -> str:
    """
    Construct jwt for authentication.

    :param user: User mongo document to pull information from.
    :type user: User
    """
    return jwt.encode({'user': str(user.id), 'created': int(time.time())}, BLOG_JWT_SECRET_KEY, algorithm='HS256').decode('utf-8')


class AuthResource(BaseResource):

    route = '/v1/user/authenticate/'

    def on_post(self, req, resp):
        """Fetch serialized session JWT."""
        resp.status = falcon.HTTP_200
        payload = req.stream.read()
        user = authenticate(from_json(UserAuthDtoSerializer, payload), req.access_route[0])
        resp.body = to_json(TokenDtoSerializer, TokenDto(token=get_auth_jwt(user))) if user else 'false'


class UserResource(BaseResource):

    route = '/v1/user/'

    def on_post(self, req, resp):
        """Creates a new user resource and provides a session JWT."""
        resp.status = falcon.HTTP_201
        payload = req.stream.read()
        user = create_user(from_json(UserFormDtoSerializer, payload))
        resp.body = to_json(TokenDtoSerializer, TokenDto(token=get_auth_jwt(user)))

    @falcon.before(require_login)
    def on_get(self, req, resp):
        """Fetch user information for current session."""
        resp.status = falcon.HTTP_200
        user = req.context.get('user')
        user_dto = user_to_dto(user)
        user_dto.comments = [
            comment_to_dto(comment, href=CommentResource.url_to(req.host, comment_id=comment_id))
            for comment in get_user_comments(user_id)]
        user_dto.liked_posts = [
            post_to_dto(post, href=PostResource.url_to(req.host, post_id=post_id), comments=False)
            for post in get_user_liked_posts(user_id)]
        # no need to construct url, pull from request
        user.href = req.uri
        resp.body = to_json(UserProfileDtoSerializer, user_dto)

    @falcon.before(require_login)
    def on_put(self, req, resp):
        """Updates user resource for current session."""
        resp.status = falcon.HTTP_204
        payload = req.stream.read()
        edit_user(req.context.get('user'), from_json(UserFormDtoSerializer, payload))

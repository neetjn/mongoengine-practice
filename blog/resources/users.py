import datetime
import jwt
import falcon
from blog.constants import BLOG_JWT_SECRET_KEY
from blog.core.comments import comment_to_dto
from blog.core.posts import get_user_liked_posts, post_to_dto
from blog.core.users import authenticate, get_user, create_user, edit_user, \
    user_to_dto, get_user_comments, get_user_posts
from blog.db import User
from blog.errors import ResourceNotAvailableError
from blog.hooks.users import is_logged_in
from blog.mediatypes import UserAuthDtoSerializer, UserFormDtoSerializer, TokenDto, \
    TokenDtoSerializer, UserProfileDtoSerializer
from blog.resources.base import BaseResource
from blog.resources.comments import CommentResource
from blog.resources.posts import PostResource
from blog.settings import settings
from blog.utils.serializers import from_json, to_json


def get_auth_jwt(user: User, host: str) -> str:
    """
    Construct jwt for authentication.

    :param user: User mongo document to pull information from.
    :type user: User
    :param host: Remote host to bind token to.
    :type host: str
    """
    return jwt.encode(
        {'user': str(user.id), 'created': datetime.datetime.utcnow().timestamp(), 'host': host},
        BLOG_JWT_SECRET_KEY,
        algorithm='HS256').decode('utf-8')


class UserAuthenticationResource(BaseResource):

    route = '/v1/user/authenticate/'

    def on_post(self, req, resp):
        """Fetch serialized session token."""
        resp.status = falcon.HTTP_200
        payload = req.stream.read()
        host = req.access_route[0]
        user = authenticate(from_json(UserAuthDtoSerializer, payload), host)
        resp.body = to_json(TokenDtoSerializer, TokenDto(token=get_auth_jwt(user, host))) if user else 'false'


class UserRegistrationResource(BaseResource):

    route = '/v1/user/register/'

    def on_post(self, req, resp):
        """Creates a new user resource and provides a session token."""
        resp.status = falcon.HTTP_201
        if not settings.user.allow_manual_registration:
            raise ResourceNotAvailableError()
        host = req.access_route[0]
        payload = req.stream.read()
        user = create_user(from_json(UserFormDtoSerializer, payload))
        resp.body = to_json(TokenDtoSerializer, TokenDto(token=get_auth_jwt(user, host)))


class UserResource(BaseResource):

    route = '/v1/user/'

    @falcon.before(is_logged_in)
    def on_get(self, req, resp):
        """Fetch user information for current session."""
        resp.status = falcon.HTTP_200
        user = req.context.get('user')
        user_dto = user_to_dto(user)
        user_dto.posts = [
            post_to_dto(post, href=PostResource.url_to(req.netloc, post_id=post.id))
            for post in get_user_posts(user.id)]
        user_dto.comments = [
            comment_to_dto(comment, href=CommentResource.url_to(req.netloc, comment_id=comment.id))
            for comment in get_user_comments(user.id)]
        user_dto.liked_posts = [
            post_to_dto(post, href=PostResource.url_to(req.netloc, post_id=post.id))
            for post in get_user_liked_posts(user.id)]
        # no need to construct url, pull from request
        user.href = req.uri
        resp.body = to_json(UserProfileDtoSerializer, user_dto)

    @falcon.before(is_logged_in)
    def on_put(self, req, resp):
        """Updates user resource for current session."""
        resp.status = falcon.HTTP_204
        payload = req.stream.read()
        user = req.context.get('user')
        edit_user(user.id, from_json(UserFormDtoSerializer, payload))

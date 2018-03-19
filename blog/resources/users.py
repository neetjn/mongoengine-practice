import jwt
import falcon
from blog.constants import BLOG_JWT_SECRET_KEY
from blog.core.comments import get_user_comments, comment_to_dto
from blog.core.posts import get_user_liked_posts, post_to_dto
from blog.core.users import authenticate, get_user, create_user, edit_user, \
    user_to_dto
from blog.hooks.users import require_login
from blog.mediatypes import UserAuthDtoSerializer, UserFormDtoSerializer, TokenDto, \
    TokenDtoSerializer, UserProfileDtoSerializer
from blog.resources.base import BaseResource
from blog.resources.comments import CommentResource
from blog.resources.posts import PostResource
from blog.utils.serializers import from_json, to_json


# TODO: add user posts to userprofiledto

class UserLogin(BaseResource):

    route = '/v1/user/authenticate'

    def on_get(self, req, resp):
        """Fetch serialized session JWT."""
        resp.status = falcon.HTTP_200
        payload = req.stream.read()
        user = authenticate(from_json(UserAuthDtoSerializer, payload), req.access_route)
        if user:
            jwt_token = jwt.encode({'user': user._id}, BLOG_JWT_SECRET_KEY, algorithm='HS256')
            resp.body = to_json(TokenDtoSerializer, TokenDto(token=jwt_token))
        else:
            resp.body = 'false'


class UserResource(BaseResource):

    route = '/v1/user/'

    def on_post(self, req, resp):
        """Creates a new user resource and provides a session JWT."""
        resp.status = falcon.HTTP_201
        payload = req.stream.read()
        user = create_user(from_json(UserFormDtoSerializer, payload))
        jwt_token = jwt.encode({'user': user._id}, BLOG_JWT_SECRET_KEY, algorithm='HS256')
        resp.body = to_json(TokenDtoSerializer, TokenDto(token=jwt_token))

    @falcon.before(require_login)
    def on_get(self, req, resp):
        """Fetch user information for current session."""
        resp.status = falcon.HTTP_200
        user = req.context.get('user')
        user_dto = user_to_dto(user)
        user_dto.comments = [
            comment_to_dto(comment, href=CommentResource.url_to(req.host, comment_id=comment._id))
            for comment in get_user_comments(user._id)]
        user_dto.liked_posts = [
            post_to_dto(post, href=PostResource.url_to(req.host, post_id=post._id), comments=False)
            for post in get_user_liked_posts(user._id)]
        # no need to construct url, pull from request
        user.href = req.uri
        resp.body = to_json(UserProfileDtoSerializer, user_dto)

    @falcon.before(require_login)
    def on_put(self, req, resp):
        """Updates user resource for current session."""
        resp.status = falcon.HTTP_204
        payload = req.stream.read()
        edit_user(req.context.get('user'), from_json(UserFormDtoSerializer, payload))

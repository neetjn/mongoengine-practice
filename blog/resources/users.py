import datetime
import io
import jwt
import magic
import os
import falcon
from blog.constants import BLOG_JWT_SECRET_KEY
from blog.core.comments import comment_to_dto
from blog.core.posts import get_user_liked_posts, post_to_dto
from blog.core.users import authenticate, get_user, create_user, edit_user, \
    user_to_dto, get_user_comments, get_user_posts, store_user_avatar, delete_user_avatar
from blog.db import User
from blog.errors import ResourceNotAvailableError, UserAvatarUploadError
from blog.hooks.responders import auto_respond, request_body, response_body, Cache
from blog.hooks.users import is_logged_in, is_logged_out
from blog.mediatypes import UserAuthDtoSerializer, UserFormDtoSerializer, TokenDto, \
    TokenDtoSerializer, UserProfileDtoSerializer, LinkDto, HttpMethods, \
    UserUpdateFormDtoSerializer
from blog.resources.base import BaseResource
from blog.resources.comments import CommentResource
from blog.resources.posts import PostResource
from blog.settings import settings
from blog.utils.serializers import to_json


class BLOG_USER_RESOURCE_HREF_REL(object):

    SELF = 'self'
    USER_AVATAR_UPLOAD = 'user-avatar-upload'
    USER_AVATAR_DELETE = 'user-avatar-delete'


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
    use_cache = False

    @falcon.before(auto_respond)
    @falcon.before(request_body, UserAuthDtoSerializer)
    def on_post(self, req, resp):
        """Fetch serialized session token."""
        host = req.access_route[0]
        raise RuntimeError(req.payload)
        user = authenticate(req.payload, host)
        resp.body = to_json(TokenDtoSerializer, TokenDto(token=get_auth_jwt(user, host))) if user else 'false'


class UserRegistrationResource(BaseResource):

    route = '/v1/user/register/'
    use_cache = False

    @falcon.before(auto_respond)
    @falcon.before(request_body, UserFormDtoSerializer)
    @falcon.before(is_logged_out)
    @falcon.after(response_body, TokenDtoSerializer)
    def on_post(self, req, resp):
        """Creates a new user resource and provides a session token."""
        if not settings.user.allow_manual_registration:
            raise ResourceNotAvailableError()
        host = req.access_route[0]
        user = create_user(req.payload)
        resp.body = TokenDto(token=get_auth_jwt(user, host))


class UserAvatarResource(BaseResource):

    route = '/v1/user/{user_id}/avatar/'
    use_cache = False

    @falcon.before(auto_respond)
    def on_get(self, req, resp, user_id):
        """Fetch and serve avatar for requested user."""
        if not settings.user.allow_avatar_capability:
            raise ResourceNotAvailableError()
        user = get_user(user_id)
        if user.avatar_href:
            # redirect to source
            raise falcon.HTTPMovedPermanently(user.avatar_href)
        elif user.avatar_binary:
            # serve binary
            resp.content_type = user.avatar_binary.content_type
            avatar_stream = user.avatar_binary.gridout.read()
            resp.stream = io.BytesIO(avatar_stream)
            resp.stream_len = len(avatar_stream)
        else:
            # serve default avatar image
            resp.content_type = 'image/png'
            avatar_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static/default-avatar.png'))
            resp.stream = open(avatar_path, 'rb')
            resp.stream_len = os.path.getsize(avatar_path)


class UserAvatarMediaResource(BaseResource):

    route = '/v1/user/avatar/'
    unique_cache = True

    @falcon.before(auto_respond)
    @falcon.before(is_logged_in)
    def on_post(self, req, resp):
        """Consumes and stores avatar for user in current session."""
        if not settings.user.allow_avatar_capability:
            raise ResourceNotAvailableError()
        user = req.context.get('user')
        user_id = str(user.id)
        if 'image' not in req.params:
            raise UserAvatarUploadError()
        avatar = req.params.get('image').file
        avatar_stream = avatar.read()
        # checking avatar stream kb against max size
        if len(avatar_stream) / 1024 > settings.rules.user.avatar_size:
            raise UserAvatarUploadError()
        mime = magic.Magic(mime=True)
        store_user_avatar(user_id, avatar_stream, mime.from_buffer(avatar_stream))

    @falcon.before(auto_respond)
    @falcon.before(is_logged_in)
    def on_delete(self, req, resp):
        """Delete existing user avatar, will reference default."""
        if not settings.user.allow_avatar_capability:
            raise ResourceNotAvailableError()
        user = req.context.get('user')
        user_id = str(user.id)
        delete_user_avatar(user_id)


class UserResource(BaseResource):

    route = '/v1/user/'
    unique_cache = True

    @Cache.from_cache
    @falcon.before(auto_respond)
    @falcon.before(is_logged_in)
    @falcon.after(response_body, UserProfileDtoSerializer)
    def on_get(self, req, resp):
        """Fetch user information for current session."""
        user = req.context.get('user')
        user_id = str(user.id)
        user_dto = user_to_dto(user)
        user_dto.posts = [
            post_to_dto(post, href=PostResource.url_to(req.netloc, post_id=post.id))
            for post in get_user_posts(user_id)]
        user_dto.comments = [
            comment_to_dto(comment, href=CommentResource.url_to(req.netloc, comment_id=comment.id))
            for comment in get_user_comments(user_id)]
        user_dto.liked_posts = [
            post_to_dto(post, href=PostResource.url_to(req.netloc, post_id=post.id))
            for post in get_user_liked_posts(user_id)]
        # no need to construct url, pull from request
        user.href = req.uri
        user_dto.links = [
            LinkDto(rel=BLOG_USER_RESOURCE_HREF_REL.SELF,
                    href=UserResource.url_to(req.netloc),
                    accepted_methods=[HttpMethods.GET, HttpMethods.PUT]),
            LinkDto(rel=BLOG_USER_RESOURCE_HREF_REL.USER_AVATAR_UPLOAD,
                    href=UserAvatarMediaResource.url_to(req.netloc),
                    accepted_methods=[HttpMethods.POST]),
            LinkDto(rel=BLOG_USER_RESOURCE_HREF_REL.USER_AVATAR_DELETE,
                    href=UserAvatarMediaResource.url_to(req.netloc),
                    accepted_methods=[HttpMethods.DELETE])]
        # if user avatar capabilities present, provide avatar image
        if settings.user.allow_avatar_capability:
            user_dto.avatar_href = user.avatar_href or UserAvatarResource.url_to(req.netloc, user_id=user.id)
        resp.body = user_dto

    @falcon.before(auto_respond)
    @falcon.before(request_body, UserUpdateFormDtoSerializer)
    @falcon.before(is_logged_in)
    def on_put(self, req, resp):
        """Updates user resource for current session."""
        user = req.context.get('user')
        user_id = str(user.id)
        edit_user(user_id, req.payload)


# override resource binded cache with later defined resources
UserAvatarMediaResource.cached_resources = [UserResource]

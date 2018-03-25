import falcon
from blog.core.posts import get_posts, get_post, create_post, edit_post, delete_post, \
    post_to_dto, like_post, view_post
from blog.db import User
from blog.errors import UnauthorizedRequest
from blog.hooks.users import require_login
from blog.mediatypes import PostDtoSerializer, PostCollectionDtoSerializer, \
    PostFormDtoSerializer, PostCollectionDto, UserRoles, LinkDto
from blog.resources.base import BaseResource
from blog.utils.serializers import from_json, to_json

# TODO: include functionality and endpoint for liking post
# can include like endpoint in post link


def user_has_post_access(user: User, post_id: str) -> bool:
    return get_post(post_id).author != user.id and \
        user.role not in (UserRoles.admin, UserRoles.moderator)


class PostViewResource(BaseResource):

    route = '/v1/post/{post_id}/view'

    @falcon.before(require_login)
    def on_put(self, req, resp, post_id):
        """View an existing post resource"""
        resp.status = falcon.HTTP_204
        user = req.context.get('user')
        view_post(post_id, str(user.id), req.access_route[0])


class PostLikeResource(BaseResource):

    route = '/v1/post/{post_id}/like'

    @falcon.before(require_login)
    def on_put(self, req, resp, post_id):
        """Like an existing post resource"""
        resp.status = falcon.HTTP_204
        user = req.context.get('user')
        like_post(post_id, str(user.id))


class PostResource(BaseResource):

    route = '/v1/post/{post_id}/'

    def on_get(self, req, resp, post_id):
        """Fetch single post resource."""
        resp.status = falcon.HTTP_200
        post = get_post(post_id)
        post_dto = post_to_dto(post, href=req.uri, links=[
            LinkDto(rel='like-post', href=PostLikeResource.url_to(req.netloc, post_id=post.id)),
            LinkDto(rel='view-post', href=PostViewResource.url_to(req.netloc, post_id=post.id))])
        resp.body = to_json(PostDtoSerializer, post_dto)

    @falcon.before(require_login)
    def on_put(self, req, resp, post_id):
        """Update single post resource."""
        resp.status = falcon.HTTP_204
        user = req.context.get('user')
        if not user_has_post_access(user, post_id):
            raise UnauthorizedRequest(user)
        payload = req.stream.read()
        edit_post(post_id, from_json(PostFormDtoSerializer, payload))

    @falcon.before(require_login)
    def on_delete(self, req, resp, post_id):
        """Delete single post resource."""
        resp.status = falcon.HTTP_204
        user = req.context.get('user')
        if not user_has_post_access(user, post_id):
            raise UnauthorizedRequest(user)
        delete_post(post_id)


class PostCollectionResource(BaseResource):

    route = '/v1/posts/'

    def on_get(self, req, resp):
        """
        Fetch grid view for all post resources.

        Note: This endpoint support pagination, pagination arguments must be provided via query args.
        """
        resp.status = falcon.HTTP_200
        post_collection_dto = PostCollectionDto(posts=[
            post_to_dto(post, href=PostResource.url_to(req.netloc, post_id=post.id), links=[
                LinkDto(rel='like-post', href=PostLikeResource.url_to(req.netloc, post_id=post.id)),
                LinkDto(rel='view-post', href=PostViewResource.url_to(req.netloc, post_id=post.id))], comments=False)
            for post in get_posts(start=req.params.get('start'), count=req.params.get('count'))])
        resp.body = to_json(PostCollectionDtoSerializer, post_collection_dto)

    @falcon.before(require_login)
    def on_post(self, req, resp):
        """Create a new post resource."""
        resp.status = falcon.HTTP_201
        payload = req.stream.read()
        user = req.context.get('user')
        create_post(user.id, from_json(PostFormDtoSerializer, payload))
        # link to grid view
        resp.set_header('Location', req.uri)

import falcon
from blog.core.posts import get_posts, get_post, create_post, edit_post, delete_post, \
    post_to_dto, like_post, view_post, get_post_comments, create_post_comment
from blog.core.comments import comment_to_dto
from blog.db import User
from blog.errors import UnauthorizedRequest
from blog.hooks.users import require_login
from blog.mediatypes import PostDtoSerializer, PostCollectionDtoSerializer, \
    PostFormDtoSerializer, PostCollectionDto, UserRoles, LinkDto, \
    CommentFormDtoSerializer
from blog.resources.base import BaseResource
from blog.resources.comments import CommentResource, CommentLikeResource, \
    BLOG_COMMENT_RESOURCE_HREF_REL
from blog.utils.serializers import from_json, to_json


class BLOG_POST_RESOURCE_HREF_REL(object):

    POST_LIKE = 'post-like'
    POST_VIEW = 'post-view'
    POST_COMMENT = 'post-comment'


def user_has_post_access(user: User, post_id: str) -> bool:
    return get_post(post_id).author != user.id and \
        user.role not in (UserRoles.ADMIN, UserRoles.MODERATOR)


class PostCommentResource(BaseResource):

    route = '/v1/post/{post_id}/comment'

    @falcon.before(require_login)
    def on_post(self, req, resp, post_id):
        """Create comment for existing post resource"""
        resp.status = falcon.HTTP_201
        payload = req.stream.read()
        user = req.context.get('user')
        create_post_comment(post_id, str(user.id), from_json(CommentFormDtoSerializer, payload))


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
            LinkDto(rel=BLOG_POST_RESOURCE_HREF_REL.POST_COMMENT,
                    href=PostCommentResource.url_to(req.netloc, post_id=post.id)),
            LinkDto(rel=BLOG_POST_RESOURCE_HREF_REL.POST_LIKE,
                    href=PostLikeResource.url_to(req.netloc, post_id=post.id)),
            LinkDto(rel=BLOG_POST_RESOURCE_HREF_REL.POST_VIEW,
                    href=PostViewResource.url_to(req.netloc, post_id=post.id))])
        comments = get_post_comments(post_id)
        post_dto.comments = [
            comment_to_dto(
                comment,
                href=CommentResource.url_to(req.netloc, comment_id=str(comment.id),
                links=[
                    LinkDto(
                        rel=BLOG_COMMENT_RESOURCE_HREF_REL.COMMENT_LIKE,
                        href=CommentLikeResource.url_to(req.netloc, comment_id=str(comment.id))
                    )
                ])) for comment in comments]

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
                LinkDto(rel='comment', href=PostCommentResource.url_to(req.netloc, post_id=post.id)),
                LinkDto(rel='like', href=PostLikeResource.url_to(req.netloc, post_id=post.id)),
                LinkDto(rel='view', href=PostViewResource.url_to(req.netloc, post_id=post.id))])
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


class PostSearchResource(BaseResource):

    route = '/v1/posts/search'

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_201
        # TODO: complete postsearch resource

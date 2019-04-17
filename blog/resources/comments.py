import falcon
from falcon_redis_cache.hooks import CacheProvider
from falcon_redis_cache.utils import clear_resource_cache
from blog.core.comments import get_comment, edit_comment, delete_comment, comment_to_dto, \
    like_comment
from blog.db import Comment, User
from blog.errors import UnauthorizedRequestError
from blog.hooks.responders import auto_respond, request_body, response_body
from blog.hooks.users import is_logged_in
from blog.mediatypes import UserRoles, CommentDtoSerializer, CommentFormDtoSerializer, \
    LinkDto, HttpMethods
from blog.resources import posts
from blog.resources.base import BaseResource


class BLOG_COMMENT_RESOURCE_HREF_REL(object):

    SELF = 'self'
    COMMENT_LIKE = 'comment-like'


def get_comment_links(req: falcon.Request, comment: Comment) -> list:
    """
    Construct comment resource links.

    :param req: Request object to pull host from.
    :type req: falcon.Request
    :param comment: Comment document to construct links for.
    :type comment: Comment
    """
    return [LinkDto(rel=BLOG_COMMENT_RESOURCE_HREF_REL.SELF,
                    href=CommentResource.url_to(req.netloc, comment_id=comment.id),
                    accepted_methods=[HttpMethods.GET, HttpMethods.PUT, HttpMethods.DELETE]),
            LinkDto(rel=BLOG_COMMENT_RESOURCE_HREF_REL.COMMENT_LIKE,
                    href=CommentLikeResource.url_to(req.netloc, comment_id=comment.id),
                    accepted_methods=[HttpMethods.PUT])]


def user_has_comment_access(user: User, comment_id: str) -> bool:
    """
    Verify user's ability to update or delete comment.

    :param user: User resource to pull information from.
    :type user: User
    :param comment_id: Identifier of comment resource.
    :type comment_id: str
    """
    return get_comment(comment_id).author != user.id and \
        user.role not in (UserRoles.ADMIN, UserRoles.MODERATOR)


class CommentLikeResource(BaseResource):

    route = '/v1/blog/comment/{comment_id}/like'

    @falcon.before(is_logged_in)
    def on_put(self, req, resp, comment_id):
        """Like an existing comment resource."""
        resp.status = falcon.HTTP_204
        user = req.context.get('user')
        like_comment(comment_id, str(user.id))


class CommentResource(BaseResource):

    route = '/v1/blog/comment/{comment_id}/'
    binded_resources = [CommentLikeResource]

    @CacheProvider.from_cache
    @falcon.before(auto_respond)
    @falcon.after(response_body, CommentDtoSerializer)
    def on_get(self, req, resp, comment_id):
        """Fetch single comment resource."""
        comment = get_comment(comment_id)
        comment_dto = comment_to_dto(comment, href=req.uri, links=get_comment_links(req, comment))
        resp.body = comment_dto

    @falcon.before(auto_respond)
    @falcon.before(request_body, CommentDtoSerializer)
    @falcon.before(is_logged_in)
    def on_put(self, req, resp, comment_id):
        """Update single comment resource."""
        user = req.context.get('user')
        if not user_has_comment_access(user, comment_id):
            raise UnauthorizedRequestError()
        edit_comment(comment_id, req.payload)
        comment = get_comment(comment_id)
        # clear postst resource cache to reflect changes to comment
        clear_resource_cache(posts.PostResource, req, post_id=comment.post_id)

    @falcon.before(auto_respond)
    @falcon.before(is_logged_in)
    def on_delete(self, req, resp, comment_id):
        """Delete single comment resource."""
        user = req.context.get('user')
        if not user_has_comment_access(user, comment_id):
            raise UnauthorizedRequestError()
        delete_comment(comment_id)
        # clear post collection/search resource cache to reflect new comment count
        clear_resource_cache(posts.PostCollectionResource, req)
        clear_resource_cache(posts.PostSearchResource, req)


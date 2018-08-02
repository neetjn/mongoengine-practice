import falcon
import redis
from blog.core.comments import get_comment, edit_comment, delete_comment, comment_to_dto, \
    like_comment
from blog.db import Comment, User
from blog.errors import UnauthorizedRequestError
from blog.hooks.users import is_logged_in
from blog.mediatypes import UserRoles, CommentDtoSerializer, CommentFormDtoSerializer, \
    LinkDto
from blog.resources.base import BaseResource
from blog.utils.serializers import from_json, to_json


class BLOG_COMMENT_RESOURCE_HREF_REL(object):

    COMMENT_LIKE = 'comment-like'


def clear_post_comment_cache(client: redis.Redis, comment_id: str=None):
    """
    Emptys post collection and search cache effectively.

    :param client: Redis client to reference.
    :type client: redis.Redis
    :param comment_id: Identifier of individual comment of cache to clear.
    :type comment_id: str
    """
    # delete cached collections
    for key in client.scan_iter('post-collection*'):
        client.delete(key)
    # delete cached searches
    for key in client.scan_iter('post-search*'):
        client.delete(key)
    # delete cached comment by id
    if comment_id:
        client.delete(f'comment-{comment_id}')


def get_comment_links(req: falcon.Request, comment: Comment) -> list:
    """
    Construct comment resource links.

    :param req: Request object to pull host from.
    :type req: falcon.Request
    :param comment: Comment document to construct links for.
    :type comment: Comment
    """
    return [LinkDto(rel=BLOG_COMMENT_RESOURCE_HREF_REL.COMMENT_LIKE,
                    href=CommentLikeResource.url_to(req.netloc, comment_id=comment.id))]


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

    def on_get(self, req, resp, comment_id):
        """Fetch single comment resource."""
        resp.status = falcon.HTTP_200
        cache = req.context.get('cache')
        if cache.get(f'comment-{comment_id}'):
            resp.body = cache.get(f'comment-{comment_id}')
        else:
            comment = get_comment(comment_id)
            comment_dto = comment_to_dto(comment, href=req.uri, links=get_comment_links(req, comment))
            resp.body = to_json(CommentDtoSerializer, comment_dto)
            # store requested comment in redis
            cache.set(f'comment-{comment_id}', resp.body)

    @falcon.before(is_logged_in)
    def on_put(self, req, resp, comment_id):
        """Update single comment resource."""
        resp.status = falcon.HTTP_204
        cache = req.context.get('cache')
        user = req.context.get('user')
        if not user_has_comment_access(user, comment_id):
            raise UnauthorizedRequestError()
        payload = req.stream.read()
        edit_comment(comment_id, from_json(CommentFormDtoSerializer, payload))
        # delete cached comment
        clear_post_comment_cache(cache, comment_id)

    @falcon.before(is_logged_in)
    def on_delete(self, req, resp, comment_id):
        """Delete single comment resource."""
        resp.status = falcon.HTTP_204
        cache = req.context.get('cache')
        user = req.context.get('user')
        if not user_has_comment_access(user, comment_id):
            raise UnauthorizedRequestError()
        delete_comment(comment_id)
        # delete cached comment
        clear_post_comment_cache(cache, comment_id)

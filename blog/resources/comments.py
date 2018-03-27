import falcon
from blog.core.comments import get_comment, edit_comment, delete_comment, comment_to_dto, \
    like_comment
from blog.db import User
from blog.errors import UnauthorizedRequest
from blog.hooks.users import require_login
from blog.mediatypes import UserRoles, CommentDtoSerializer, CommentFormDtoSerializer, \
    LinkDto
from blog.resources.base import BaseResource
from blog.utils.serializers import from_json, to_json


class BLOG_COMMENT_RESOURCE_HREF_REL(object):

    COMMENT_LIKE = 'comment-like'


def user_has_comment_access(user: User, comment_id: str):
    return get_comment(comment_id).author != user.id and \
        user.role not in (UserRoles.ADMIN, UserRoles.MODERATOR)


class CommentLikeResource(BaseResource):

    route = '/v1/blog/comment/{comment_id}/like'

    @falcon.before(require_login)
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
        comment_dto = comment_to_dto(get_comment(comment_id))
        comment_dto.links = [
            LinkDto(rel=BLOG_COMMENT_RESOURCE_HREF_REL.COMMENT_LIKE,
                    href=CommentLikeResource.url_to(req.netloc, comment_id=comment_id))]
        # no need to construct url, pull from request
        comment_dto.href = req.uri
        resp.body = to_json(CommentDtoSerializer, comment_dto)

    @falcon.before(require_login)
    def on_put(self, req, resp, comment_id):
        """Update single comment resource."""
        resp.status = falcon.HTTP_204
        user = req.context.get('user')
        if not user_has_comment_access(user, comment_id):
            raise UnauthorizedRequest()
        payload = req.stream.read()
        edit_comment(comment_id, from_json(CommentFormDtoSerializer, payload))

    @falcon.before(require_login)
    def on_delete(self, req, resp, comment_id):
        """Delete single comment resource."""
        resp.status = falcon.HTTP_204
        user = req.context.get('user')
        if not user_has_comment_access(user, comment_id):
            raise UnauthorizedRequest()
        delete_comment(comment_id)

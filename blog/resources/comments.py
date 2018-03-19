import falcon
from blog.core.comments import get_comment, edit_comment, delete_comment, comment_to_dto
from blog.db import User
from blog.hooks.users import require_login
from blog.mediatypes import UserRoles
from blog.resources.base import BaseResource


def user_has_comment_access(user: User, comment_id: str):
    return get_comment(comment_id).author != user._id and \
        user.role not in (UserRoles.admin, UserRoles.moderator)


class CommentResource(BaseResource):

    route = '/v1/blog/comment/{comment_id}'

    def on_get(self, req, resp, comment_id):
        """Fetch single comment resource."""
        resp.body = ''

    @falcon.before(require_login)
    def on_put(self, req, resp, comment_id):
        """Update single comment resource."""
        resp.body = ''

    @falcon.before(require_login)
    def on_delete(self, req, resp, comment_id):
        """Delete single comment resource."""
        resp.body = ''

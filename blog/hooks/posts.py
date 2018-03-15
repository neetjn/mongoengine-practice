from falcon import Request, Response
from blog.mediatypes import UserRoles


def has_mod_post_access(resource: object, req: Request, resp: Response):
    """
    Check if user has access to edit or delete post resource.
    """
    if req.blog_user.role == UserRoles.admin or UserRoles.moderator:
        return True
    # TODO: complete post mod access hook

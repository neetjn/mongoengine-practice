import datetime
from mongoengine import DoesNotExist, ValidationError, MultipleObjectsReturned, NotUniqueError
from blog.db import Comment
from blog.errors import CommentNotFound
from blog.mediatypes import CommentDto


def get_post_comments(post_id):
    """
    Fetch collection of comments given post.

    :param post_id: Identifier of post to target.
    :type post_id: str
    :return: [Comment, ...]
    """
    return Comment.objects(post_id=post_id)


def get_comment(comment_id):
    """
    Fetch existing comment resource.

    :param comment_id: Identifier of comment to fetch.
    :type comment_id: str
    """
    try:
        return Comment.objects.get(pk=comment_id)
    except (DoesNotExist, ValidationError):
        raise CommentNotFound()


def edit_comment(comment_id, comment_form_dto):
    """
    Edit existing comment resource.

    :param comment_id: Identifier of coment to edit.
    :type comment_id: str
    """
    comment = get_comment(comment_id)
    comment.content = comment_form_dto.content
    comment.editted = datetime.datetime.utcnow()
    comment.save()

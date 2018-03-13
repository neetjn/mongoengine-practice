import datetime
from mongoengine import DoesNotExist, ValidationError, MultipleObjectsReturned, NotUniqueError
from blog.db import Comment
from blog.errors import CommentNotFoundError
from blog.mediatypes import CommentDto, CommentFormDto


# TODO: add method to delete comment resources to core utilities

def get_post_comments(post_id: str):
    """
    Fetch collection of comments given post.

    :param post_id: Identifier of post to target.
    :type post_id: str
    :return: [Comment, ...]
    """
    return Comment.objects(post_id=post_id)


def get_comment(comment_id: str):
    """
    Fetch existing comment resource.

    :param comment_id: Identifier of comment to fetch.
    :type comment_id: str
    """
    try:
        return Comment.objects.get(pk=comment_id)
    except (DoesNotExist, ValidationError):
        raise CommentNotFoundError()


def edit_comment(comment_id: str, comment_form_dto: CommentFormDto):
    """
    Edit existing comment resource.

    :param comment_id: Identifier of coment to edit.
    :type comment_id: str
    """
    comment = get_comment(comment_id)
    comment.content = comment_form_dto.content
    comment.editted = datetime.datetime.utcnow()
    comment.save()

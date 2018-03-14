import datetime
from mongoengine import DoesNotExist, ValidationError, MultipleObjectsReturned, NotUniqueError
from blog.constants import BLOG_CONTENT_KEY
from blog.db import Comment
from blog.errors import CommentNotFoundError
from blog.mediatypes import CommentDto, CommentFormDto
from blog.utils import encrypt_content, decrypt_content


def get_post_comments(post_id: str):
    """
    Fetch collection of comments given post.

    :param post_id: Identifier of post to target.
    :type post_id: str
    :return: [Comment, ...]
    """
    comments = Comment.objects(post_id=post_id)
    for comment in comments:
        comment.content = decrypt_content(comment.content)
    return comments


def get_comment(comment_id: str):
    """
    Fetch existing comment resource.

    :param comment_id: Identifier of comment to fetch.
    :type comment_id: str
    """
    try:
        comment = Comment.objects.get(pk=comment_id)
        comment.content = decrypt_content(comment.content)
        return comment
    except (DoesNotExist, ValidationError):
        raise CommentNotFoundError()


def edit_comment(comment_id: str, comment_form_dto: CommentFormDto):
    """
    Edit existing comment resource.

    :param comment_id: Identifier of comment to edit.
    :type comment_id: str
    """
    comment = get_comment(comment_id)
    comment.content = encrypt_content(comment_form_dto.content)
    comment.editted = datetime.datetime.utcnow()
    comment.save()


def delete_comment(comment_id: str):
    """
    Delete existing post resource.

    :param comment_id: Identifier of comment to delete.
    :type comment_id: str
    """
    get_comment(comment_id).delete()

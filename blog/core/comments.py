import datetime
from mongoengine import DoesNotExist, ValidationError, MultipleObjectsReturned, NotUniqueError
from blog.constants import BLOG_CONTENT_KEY
from blog.core.users import get_user
from blog.db import Comment, CommentLike
from blog.errors import CommentNotFoundError
from blog.mediatypes import CommentDto, CommentFormDto
from blog.utils.crypto import encrypt_content, decrypt_content


def get_comment(comment_id: str) -> Comment:
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


def like_comment(comment_id: str, user_id: str):
    """
    Like or dislike existing comment resource.

    :param comment_id:  Identifier of comment to like or dislike.
    :type comment_id: str
    :param user_id: Identifier of user to like or dislike comment.
    :type user_id: str
    """
    try:
        comment_like = CommentLike.objects.get(comment_id=comment_id, user_id=user_id)
    except DoesNotExist:
        CommentLike(comment_id=comment_id, user_id=user_id).save()
    else:
        comment_like.delete()


def delete_comment(comment_id: str):
    """
    Delete existing post resource.

    :param comment_id: Identifier of comment to delete.
    :type comment_id: str
    """
    get_comment(comment_id).delete()


def comment_to_dto(comment: Comment, href: str = None, links: list = None) -> CommentDto:
    """
    Convert comment resource to data transfer object.

    :param comment: Comment resource to convert.
    :type comment: Comment
    :param href: Post resource href link.
    :type href: str
    :return: CommentDto
    """
    likes = CommentLike.objects(comment_id=comment.id)
    return CommentDto(
        href=href,
        author=get_user(comment.author).username,
        content=comment.content,
        tags=comment.tags,
        created=comment.created,
        edited=comment.edited,
        likes=len(likes))

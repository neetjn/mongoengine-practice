from blog.mediatypes import CommentFormDto
from blog.settings import settings
from tests.utils import random_string


def generate_comment_form_dto(**kwargs) -> CommentFormDto:
    """Generate a comment form"""
    return CommentFormDto(
        content=random_string(settings.rules.comment.content_min_char))

from blog.mediatypes import PostFormDto, PostDto
from blog.settings import settings
from tests.utils import random_string


def generate_post_form_dto(**kwargs) -> PostFormDto:
    """Generate a post form"""
    return PostFormDto(
        title=kwargs.get('title', random_string(settings.rules.post.title_min_char)),
        description=kwargs.get('description', random_string(settings.rules.post.title_min_char)),
        content=kwargs.get('content', random_string(settings.rules.post.content_min_char)),
        tags=kwargs.get('tags', [random_string(settings.rules.post.tag_min_char) for _ in range(settings.rules.post.tag_max_count)]))

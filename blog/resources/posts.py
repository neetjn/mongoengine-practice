import base64
import falcon
import redis
from blog.core.posts import get_posts, get_post, create_post, edit_post, delete_post, \
    post_to_dto, like_post, view_post, get_post_comments, create_post_comment, search_posts
from blog.core.comments import comment_to_dto
from blog.db import Post, User
from blog.errors import UnauthorizedRequestError
from blog.hooks.users import is_logged_in
from blog.mediatypes import PostDtoSerializer, PostCollectionDtoSerializer, \
    PostFormDtoSerializer, PostCollectionDto, UserRoles, LinkDto, \
    CommentFormDtoSerializer, PostSearchSettingsDtoSerializer
from blog.resources.base import BaseResource
from blog.resources.comments import get_comment_links, CommentResource
from blog.utils.serializers import from_json, to_json


class BLOG_POST_RESOURCE_HREF_REL(object):

    POST_LIKE = 'post-like'
    POST_VIEW = 'post-view'
    POST_COMMENT = 'post-comment'


def get_post_links(req: falcon.Request, post: Post) -> list:
    """
    Construct post resource links.

    :param req: Request object to pull host from.
    :type req: falcon.Request
    :param post: Post document to construct links for.
    :type post: Post
    """
    return [
        LinkDto(rel=BLOG_POST_RESOURCE_HREF_REL.POST_COMMENT,
                href=PostCommentResource.url_to(req.netloc, post_id=post.id)),
        LinkDto(rel=BLOG_POST_RESOURCE_HREF_REL.POST_LIKE,
                href=PostLikeResource.url_to(req.netloc, post_id=post.id)),
        LinkDto(rel=BLOG_POST_RESOURCE_HREF_REL.POST_VIEW,
                href=PostViewResource.url_to(req.netloc, post_id=post.id))]


def user_has_post_access(user: User, post_id: str) -> bool:
    """
    Verify user's ability to update or delete post.

    :param user: User resource to pull information from.
    :type user: User
    :param post_id: Identifier of post resource.
    :type post_id: str
    """
    return get_post(post_id).author != user.id and \
        user.role not in (UserRoles.ADMIN, UserRoles.MODERATOR)


def clear_post_cache(client: redis.Redis, post_id: str=None):
    """
    Emptys post collection and search cache effectively.

    :param client: Redis client to reference.
    :type client: redis.Redis
    :param post_id: Identifier of individual post of cache to clear.
    :type post_id: str
    """
    # delete cached collections
    for key in client.scan_iter('post-collection*'):
        client.delete(key)
    # delete cached searches
    for key in client.scan_iter('post-search*'):
        client.delete(key)
    # delete cached post by id
    if post_id:
        client.delete(f'post-{post_id}')


class PostCommentResource(BaseResource):

    route = '/v1/post/{post_id}/comment'

    @falcon.before(is_logged_in)
    def on_post(self, req, resp, post_id):
        """Create comment for existing post resource"""
        resp.status = falcon.HTTP_201
        payload = req.stream.read()
        cache = req.context.get('cache')
        user = req.context.get('user')
        create_post_comment(post_id, str(user.id), from_json(CommentFormDtoSerializer, payload))
        # delete cached payload on change
        clear_post_cache(cache, post_id)


class PostViewResource(BaseResource):

    route = '/v1/post/{post_id}/view'

    @falcon.before(is_logged_in)
    def on_put(self, req, resp, post_id):
        """View an existing post resource"""
        resp.status = falcon.HTTP_204
        cache = req.context.get('cache')
        user = req.context.get('user')
        view_post(post_id, str(user.id), req.access_route[0])
        # delete cached payload on change
        clear_post_cache(cache, post_id)


class PostLikeResource(BaseResource):

    route = '/v1/post/{post_id}/like'

    @falcon.before(is_logged_in)
    def on_put(self, req, resp, post_id):
        """Like an existing post resource"""
        resp.status = falcon.HTTP_204
        cache = req.context.get('cache')
        user = req.context.get('user')
        like_post(post_id, str(user.id))
        # delete cached payload on change
        clear_post_cache(cache, post_id)


class PostResource(BaseResource):

    route = '/v1/post/{post_id}/'

    def on_get(self, req, resp, post_id):
        """Fetch single post resource."""
        resp.status = falcon.HTTP_200
        cache = req.context.get('cache')
        if cache.get(f'post-{post_id}'):
            resp.body = cache.get(f'post-{post_id}')
        else:
            post = get_post(post_id)
            post_dto = post_to_dto(post, href=req.uri, links=get_post_links(req, post))
            comments = get_post_comments(post_id)
            post_dto.comments = [
                comment_to_dto(
                    comment,
                    href=CommentResource.url_to(req.netloc, comment_id=str(comment.id),
                    links=get_comment_links(req, comment))) for comment in comments]

            resp.body = to_json(PostDtoSerializer, post_dto)
            # cache post payload in redis
            cache.set(f'post-{post_id}', resp.body)

    @falcon.before(is_logged_in)
    def on_put(self, req, resp, post_id):
        """Update single post resource."""
        resp.status = falcon.HTTP_204
        cache = req.context.get('cache')
        user = req.context.get('user')
        if not user_has_post_access(user, post_id):
            raise UnauthorizedRequestError(user)
        payload = req.stream.read()
        post_form_dto = from_json(PostFormDtoSerializer, payload)
        # ensure non authorized users cannot set post featured status
        # TODO: create tests for featured post
        if user.role not in (UserRoles.ADMIN, UserRoles.MODERATOR) and post_form_dto.featured:
            post = get_post(post_id)
            if not post.featured:
                raise UnauthorizedRequestError()
        edit_post(post_id, post_form_dto)
        # delete cached payload on change
        clear_post_cache(cache, post_id)

    @falcon.before(is_logged_in)
    def on_delete(self, req, resp, post_id):
        """Delete single post resource."""
        resp.status = falcon.HTTP_204
        cache = req.context.get('cache')
        user = req.context.get('user')
        if not user_has_post_access(user, post_id):
            raise UnauthorizedRequestError(user)
        delete_post(post_id)
        # delete cached payload on delete
        clear_post_cache(cache, post_id)


class PostCollectionResource(BaseResource):

    route = '/v1/posts/'

    def on_get(self, req, resp):
        """
        Fetch grid view for all post resources.

        Note: This endpoint supports pagination, pagination arguments must be provided via query args.
        """
        resp.status = falcon.HTTP_200
        page_start = req.params.get('start')
        page_count = req.params.get('count')
        cache = req.context.get('cache')
        cache_key = f'post-collection;{page_start};{page_count}'
        if cache.get(cache_key):
            resp.body = cache.get(cache_key)
        else:
            post_collection_dto = PostCollectionDto(posts=[
                post_to_dto(post, href=PostResource.url_to(req.netloc, post_id=post.id), links=get_post_links(req, post))
                for post in get_posts(start=page_start, count=page_count)])
            resp.body = to_json(PostCollectionDtoSerializer, post_collection_dto)
            # cache post collection in redis
            cache.set(cache_key, resp.body)

    @falcon.before(is_logged_in)
    def on_post(self, req, resp):
        """Create a new post resource."""
        resp.status = falcon.HTTP_201
        payload = req.stream.read()
        cache = req.context.get('cache')
        user = req.context.get('user')
        create_post(user.id, from_json(PostFormDtoSerializer, payload))
        # link to grid view
        resp.set_header('Location', req.uri)
        # delete cached grid on create
        clear_post_cache(cache)


class PostSearchResource(BaseResource):

    route = '/v1/posts/search'

    @falcon.before(is_logged_in)
    def on_post(self, req, resp):
        """Search for an existing post resource."""
        resp.status = falcon.HTTP_201
        payload = req.stream.read()
        cache = req.context.get('cache')
        page_start = req.params.get('start')
        page_count = req.params.get('count')
        post_search_key = str(base64.encodestring(payload))
        cache_key = f'post-search;{page_start};{page_count};{post_search_key}'
        if cache.get(cache_key):
            resp.body = cache.get(cache_key)
        else:
            user = req.context.get('user')
            post_search_settings = from_json(PostSearchSettingsDtoSerializer, payload)
            post_collection_dto = PostCollectionDto(posts=[
                post_to_dto(post, href=PostResource.url_to(req.netloc, post_id=post.id), links=get_post_links(req, post))
                for post in search_posts(post_search_settings, str(user.id), page_start, page_count)])
            resp.body = to_json(PostCollectionDtoSerializer, post_collection_dto)
            # cache post search in redis
            cache.set(cache_key, resp.body)

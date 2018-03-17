import falcon
from blog.core.posts import get_posts, get_post, create_post, delete_post, post_to_dto
from blog.hooks.users import require_login
from blog.mediatypes import PostDtoSerializer, PostCollectionDtoSerializer, \
    PostFormDtoSerializer, PostCollectionDto
from blog.utils.serializers import from_json, to_json


class PostResource(object):

    def on_get(self, req, resp, post_id):
        """Fetch single post resource."""
        resp.status = falcon.HTTP_200
        post_dto = post_to_dto(get_post(post_id))
        # TODO: find url_to alternative for falcon: specify post resource location
        post_dto.href = ''
        resp.body = to_json(PostDtoSerializer, post_dto)

    def on_put(self, req, resp, post):
        """Update single post resource."""
        resp.status = falcon.HTTP_204
        resp.body = ''

    def on_delete(self, req, resp, post):
        """Delete single post resource."""
        resp.status = falcon.HTTP_204
        resp.body = ''


class PostCollectionResource(object):

    def on_get(self, req, resp):
        """
        Fetch grid view for all post resources.

        Note: This endpoint support pagination, pagination arguments must be provided via query args.
        """
        resp.status = falcon.HTTP_200
        # TODO: add hrefs for each post for end ui
        post_collection_dto = PostCollectionDto(
            posts=[post_to_dto(post, comments=False) for post in get_posts(
                start=req.params.get('start', None), count=req.params.get('count', None)
            )])

        resp.body = to_json(PostCollectionDtoSerializer, post_collection_dto)

    def on_post(self, req, resp):
        """Create a new post resource."""
        resp.status = falcon.HTTP_201
        payload = req.stream.read()
        user = req.context.get('user')
        create_post(user._id, from_json(PostFormDtoSerializer, payload))
        # TODO: find url_to alternative for falcon: redirect to on_get
        resp.set_header('Location', '')

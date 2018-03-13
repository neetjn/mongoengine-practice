import falcon
from blog.core.posts import get_posts, get_post, create_post
from blog.utils import to_json, from_json


class PostResource(object):

    def on_get(self, req, resp):
        """Fetch single post resource."""
        resp.status = falcon.HTTP_200
        resp.body = ''

    def on_put(self, req, resp):
        """Update single post resource."""
        resp.status = falcon.HTTP_204
        resp.body = ''

    def on_delete(self, req, resp):
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
        resp.body = ''

    def on_post(self, req, resp):
        """Create a new post resource."""
        resp.status = falcon.HTTP_201
        resp.body = ''

import falcon
from blog.hooks.users import require_login
from blog.resources.base import BaseResource


class BlogSettingsResource(BaseResource):

    route = '/v1/blog/admin/settings'

    @falcon.before(require_login)
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        # TODO: add ability to get blog settings

    @falcon.before(require_login)
    def on_put(self, req, resp):
        resp.status = falcon.HTTP_204
        # TODO: add ability to update blog settings

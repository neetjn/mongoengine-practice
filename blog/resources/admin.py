import falcon
from blog.hooks.responders import auto_respond, request_body, response_body
from blog.hooks.users import is_admin
from blog.settings import settings, save_settings, SettingsSerializer
from blog.resources.base import BaseResource


class BlogSettingsResource(BaseResource):

    route = '/v1/blog/admin/settings'

    @falcon.before(auto_respond)
    @falcon.before(is_admin)
    @falcon.after(response_body, SettingsSerializer)
    def on_get(self, req, resp):
        """Fetch blog settings."""
        resp.body = settings

    @falcon.before(auto_respond)
    @falcon.before(request_body, SettingsSerializer)
    @falcon.before(is_admin)
    def on_put(self, req, resp):
        """Update and save blog settings."""
        save_settings(req.payload)

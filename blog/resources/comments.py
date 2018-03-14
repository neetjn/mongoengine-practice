import falcon


class CommentResource(object):

    def on_get(self, req, resp):
        """Fetch single comment resource."""
        resp.body = ''

    def on_put(self, req, resp):
        """Update single comment resource."""
        resp.body = ''

    def on_delete(self, req, resp):
        """Delete single comment resource."""
        resp.body = ''

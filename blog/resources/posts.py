from blog.utils import to_json


class PostResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = 'deadass'

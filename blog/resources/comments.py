import falcon
from blog.utils import to_json, from_json


class CommentsResource(object):

    def on_get(self, req, resp):
        resp.body = ''

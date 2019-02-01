import redis
from blog.constants import BLOG_REDIS_HOST, BLOG_REDIS_PORT
from blog.mediatypes import HttpMethods


client = redis.StrictRedis(host=BLOG_REDIS_HOST, port=BLOG_REDIS_PORT)


class CacheProvider(object):

    def process_request(self, req, resp):
        """Provide redis cache with every request."""
        req.context.set('cached', client.get(req.uri, None))

    def process_response(self, req, resp, resource, req_succeeded):
        """Sets or deletes cache for provided resources."""
        if req_succeeded:
            if req.method == HttpMethods.GET:
                client.set(req.uri, resp.body)
            else:
                client.delete(req.uri)

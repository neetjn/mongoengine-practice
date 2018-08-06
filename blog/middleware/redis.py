import redis
from blog.constants import BLOG_REDIS_HOST, BLOG_REDIS_PORT


client = redis.StrictRedis(host=BLOG_REDIS_HOST, port=BLOG_REDIS_PORT)


class CacheProvider(object):

    def process_resource(self, req, resp, resource, params):
        """Provide redis cache with every request."""
        req.context.setdefault('cache', client)

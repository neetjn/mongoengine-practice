import redis
from string import Template
from blog.constants import BLOG_REDIS_HOST, BLOG_REDIS_PORT
from blog.mediatypes import HttpMethods
from blog.utils.logger import warning


client = redis.StrictRedis(host=BLOG_REDIS_HOST, port=BLOG_REDIS_PORT)


def cache_key(req, resource, uri=None) -> str:
    """Provides unique redis cache key."""
    uri = uri or req.uri
    if resource.unique_cache:
        user = req.context.get('user')
        if user:
            return f'{uri}+{str(user.id)}'
        warning(req, f'Could not construct unique key for uri "{uri}"')
    return uri


class CacheProvider(object):

    def process_resource(self, req, resp, resource, params):
        """Provide redis cache with every request."""
        if resource.use_cache:
            resp.cached = client.get(cache_key(req, resource))

    def process_response(self, req, resp, resource, req_succeeded):
        """Sets or deletes cache for provided resources."""
        if req_succeeded and resource.use_cache:
            cache = cache_key(req, resource)
            if req.method == HttpMethods.GET:
                client.set(cache, resp.body)
                if not resp.body:
                    resp.body = resp.cached
            else:
                client.delete(cache)
                for resc in resource.cached_resources:
                    tmpl = resc.route.replace('{', '${')  # interpolate for safe formatting
                    # assumes that binded resources ay have routes with similar params
                    route = Template(tmpl).safe_substitute(**req.params)
                    uri = f'{req.protocol}://{req.netloc}{route}'
                    # delete binded cached resources
                    client.delete(cache_key(req, resc, uri))

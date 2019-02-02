import redis
from string import Template
from blog.constants import BLOG_REDIS_HOST, BLOG_REDIS_PORT
from blog.mediatypes import HttpMethods
from blog.utils.logger import warning


client = redis.StrictRedis(host=BLOG_REDIS_HOST, port=BLOG_REDIS_PORT)


def cache_key(req, resource, uri=None) -> str:
    """Provides unique redis cache key."""
    uri = uri or req.uri
    if uri.endswith('/'):
        uri = uri[:-1]
    if resource.cache_with_params:
        uri += f'?{req.query_string}'
    if resource.unique_cache:
        user = req.context.get('user')
        if user:
            return f'{uri}+{str(user.id)}'
        warning(req, f'Could not construct unique key for uri "{uri}"')
    return uri


class CacheProvider(object):

    # TODO: left here, add processesor for deleting cacge wtg oaransm sjuo reg oarans yse qyery

    def process_resource(self, req, resp, resource, params):
        """Provide redis cache with every request."""
        req.context.setdefault('params', params)
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
                print(f'\nDeleting caches from.. {req.uri}')
                client.delete(cache)
                params = req.context.get('params')
                for resc in resource.cached_resources:
                    # interpolate for safe formatting
                    tmpl = resc.route.replace('{', '${')
                    # assumes that binded resources ay have routes with similar params
                    route = Template(tmpl).safe_substitute(**params)
                    # remove last character, uri has final slash stripped
                    uri = f'{req.scheme}://{req.netloc}{route}'
                    # delete binded cached resources
                    print(cache_key(req, resc, uri))
                    client.delete(cache_key(req, resc, uri))

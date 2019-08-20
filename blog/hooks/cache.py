from blog.constants import BLOG_DISABLE_CACHE


# taken from: https://github.com/neetjn/falcon-redis-cache/blob/master/falcon_redis_cache/hooks.py
class ConditionalCache:
    @staticmethod
    def from_cache(responder):
        def wrapped(*args, **kwargs):
            if not BLOG_DISABLE_CACHE:
                return responder(*args, **kwargs)
            resp = args[2]
            if not resp.context.get('cached'):
                responder(*args, **kwargs)
        return wrapped

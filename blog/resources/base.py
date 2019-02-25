from falcon_redis_cache.resource import CacheCompaitableResource


class BaseResource(CacheCompaitableResource):

    route = ''

    @classmethod
    def url_to(cls, host, **kwargs) -> str:
        """Fetch resource route, supports template pre-processing"""
        return f'{host}{cls.route.format(**kwargs)}'

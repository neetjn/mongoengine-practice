class BaseResource(object):

    route = ''
    use_cache = True
    unique_cache = False
    cache_with_query = False
    cached_resources = []

    @classmethod
    def url_to(cls, host, **kwargs) -> str:
        """Fetch resource route, supports template pre-processing"""
        return f'{host}{cls.route.format(**kwargs)}'

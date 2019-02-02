import falcon
from r2dto import ValidationError
from blog.mediatypes import HttpMethods
from blog.utils.serializers import from_json, to_json

from blog.utils.logger import warning


StatusMethodMap = {
    HttpMethods.GET: falcon.HTTP_200,
    HttpMethods.POST: falcon.HTTP_201,
    HttpMethods.PUT: falcon.HTTP_204,
    HttpMethods.DELETE: falcon.HTTP_204,
}


def auto_respond(req, resp, resource, params):
    """Specify default response status code based on request method."""
    resp.status = StatusMethodMap.get(req.method, StatusMethodMap.get(HttpMethods.GET))


def request_body(req, resp, resource, params, serializer_class):
    """Deserialize request payload into mapped object using defined serializer."""
    req.payload = from_json(serializer_class, req.stream.read())


def response_body(req, resp, resource, serializer_class, content_type="application/json"):
    # make sure not to try and serialize already serialized, cached responses
    if resp.body and resp.body != resp.cached:
        resp.body = to_json(serializer_class, resp.body)
    resp.content_type = content_type


class Cache:

    @staticmethod
    def from_cache(responder):
        def wrapped(*args, **kwargs):
            req = args[1]
            resp = args[2]
            if not resp.cached:
                responder(*args, **kwargs)
        return wrapped

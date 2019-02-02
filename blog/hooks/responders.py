import falcon
from r2dto import ValidationError
from blog.mediatypes import HttpMethods
from blog.utils.serializers import from_json, to_json


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


def response_body(req, resp, resource, params, serializer_class, content_type="application/json"):
    resp.body = to_json(serializer_class, resp.body)
    resp.content_type = content_type

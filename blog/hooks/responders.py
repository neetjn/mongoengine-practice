import falcon
from blog.mediatypes import HttpMethods


StatusMethodMap = {
    HttpMethods.GET: falcon.HTTP_200,
    HttpMethods.POST: falcon.HTTP_201,
    HttpMethods.PUT: falcon.HTTP_204,
    HttpMethods.DELETE: falcon.HTTP_204,
}


def auto_responder(req, resp, resource, params):
    resp.status = StatusMethodMap.get(req.method, StatusMethodMap.get(HttpMethods.GET))

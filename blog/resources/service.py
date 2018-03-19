import falcon
from blog.mediatypes import LinkDto, ServiceDescriptionDto, ServiceDescriptionDtoSerializer
from blog.resources.base import BaseResource
from blog.resources.posts import PostCollectionResource
from blog.resources.users import AuthResource, UserResource
from blog.utils.serializers import from_json, to_json


class ServiceDescriptionResource(BaseResource):

    route = '/'

    def on_get(self, req, resp):
        """Fetch blog service description."""
        resp.status = falcon.HTTP_200
        resp.body = from_json(ServiceDescriptionDtoSerializer, ServiceDescriptionDto(
            links=[
                LinkDto(rel='post-collection', href=PostCollectionResource.url_to(req.host)),
                LinkDto(rel='auth', href=AuthResource.url_to(req.host)),
                LinkDto(rel='user', href=UserResource.url_to(req.host))
            ]))

import falcon
from blog.mediatypes import LinkDto, ServiceDescriptionDto, ServiceDescriptionDtoSerializer, UserRoles
from blog.resources.admin import BlogSettingsResource
from blog.resources.base import BaseResource
from blog.resources.posts import PostCollectionResource, PostSearchResource
from blog.resources.users import AuthResource, UserResource
from blog.utils.serializers import from_json, to_json


class BLOG_HREF_REL(object):

    ADMIN_BLOG_SETTINGS = 'admin-blog-settings'
    POST_COLLECTION = 'post-collection'
    POST_SEARCH = 'post-search'
    USER_AUTHENTICATION = 'user-auth'
    USER = 'user'


class ServiceDescriptionResource(BaseResource):

    route = '/'

    def on_get(self, req, resp):
        """Fetch blog service description."""
        resp.status = falcon.HTTP_200
        service_description = ServiceDescriptionDto(links=[
            LinkDto(rel=BLOG_HREF_REL.POST_COLLECTION, href=PostCollectionResource.url_to(req.netloc)),
            LinkDto(rel=BLOG_HREF_REL.POST_SEARCH, href=PostSearchResource.url_to(req.netloc)),
            LinkDto(rel=BLOG_HREF_REL.USER_AUTHENTICATION, href=AuthResource.url_to(req.netloc)),
            LinkDto(rel=BLOG_HREF_REL.USER, href=UserResource.url_to(req.netloc))])
        user = req.context.get('user')
        if user and user.role == UserRoles.ADMIN:
            service_description.links.append([
                LinkDto(rel=BLOG_HREF_REL.ADMIN_BLOG_SETTINGS, href=BlogSettingsResource.url_to(req.netloc))
            ])
        resp.body = to_json(ServiceDescriptionDtoSerializer, service_description)

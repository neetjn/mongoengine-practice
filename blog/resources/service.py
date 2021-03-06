import falcon
from falcon_redis_cache.hooks import CacheProvider
from blog.hooks.responders import auto_respond, response_body
from blog.mediatypes import LinkDto, ServiceDescriptionDto, ServiceDescriptionDtoSerializer, UserRoles, \
    HttpMethods
from blog.resources.admin import BlogSettingsResource
from blog.resources.base import BaseResource
from blog.resources.posts import PostCollectionResource, PostSearchResource
from blog.resources.users import UserAuthenticationResource, UserRegistrationResource, UserResource
from blog.settings import settings


class BLOG_HREF_REL(object):

    ADMIN_BLOG_SETTINGS = 'admin-blog-settings'
    POST_COLLECTION = 'post-collection'
    POST_SEARCH = 'post-search'
    USER_AUTHENTICATION = 'user-authentication'
    USER_REGISTRATION = 'user-registration'
    USER = 'user'


class ServiceDescriptionResource(BaseResource):

    route = '/'

    @CacheProvider.from_cache
    @falcon.before(auto_respond)
    @falcon.after(response_body, ServiceDescriptionDtoSerializer)
    def on_get(self, req, resp):
        """Fetch blog service description."""
        service_description = ServiceDescriptionDto(links=[
            LinkDto(rel=BLOG_HREF_REL.POST_COLLECTION,
                    href=PostCollectionResource.url_to(req.netloc),
                    accepted_methods=[HttpMethods.GET, HttpMethods.POST]),
            LinkDto(rel=BLOG_HREF_REL.POST_SEARCH,
                    href=PostSearchResource.url_to(req.netloc),
                    accepted_methods=[HttpMethods.POST]),
            LinkDto(rel=BLOG_HREF_REL.USER_AUTHENTICATION,
                    href=UserAuthenticationResource.url_to(req.netloc),
                    accepted_methods=[HttpMethods.POST]),
            LinkDto(rel=BLOG_HREF_REL.USER,
                    href=UserResource.url_to(req.netloc),
                    accepted_methods=[HttpMethods.GET, HttpMethods.PUT])])
        if settings.user.allow_manual_registration:
            service_description.links.append(
                LinkDto(rel=BLOG_HREF_REL.USER_REGISTRATION,
                        href=UserRegistrationResource.url_to(req.netloc),
                        accepted_methods=[HttpMethods.POST]))
        user = req.context.get('user')
        if user and user.role == UserRoles.ADMIN:
            service_description.links.append(
                LinkDto(rel=BLOG_HREF_REL.ADMIN_BLOG_SETTINGS,
                        href=BlogSettingsResource.url_to(req.netloc),
                        accepted_methods=[HttpMethods.GET, HttpMethods.PUT]))
        resp.body = service_description

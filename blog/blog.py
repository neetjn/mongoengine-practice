import falcon
from blog.errors import ErrorHandler
from blog.middleware.pagination import PaginationProcessor
from blog.middleware.users import UserProcessor
from blog.middleware.redis import CacheProvider
from blog.resources.comments import CommentResource
from blog.resources.admin import BlogSettingsResource
from blog.resources.posts import PostCollectionResource, PostResource, PostLikeResource, \
    PostViewResource, PostCommentResource, PostSearchResource
from blog.resources.users import UserAuthenticationResource, UserRegistrationResource, UserResource, \
    UserAvatarMediaResource, UserAvatarResource
from blog.resources.service import ServiceDescriptionResource
from blog.settings import settings

from falcon_multipart.middleware import MultipartMiddleware


api = falcon.API(middleware=[PaginationProcessor(), UserProcessor(), CacheProvider(), MultipartMiddleware()])

api.add_error_handler(Exception, ErrorHandler.unexpected)
api.add_error_handler(falcon.HTTPError, ErrorHandler.http)
api.add_error_handler(falcon.HTTPStatus, ErrorHandler.http)

api.add_route(BlogSettingsResource.route, BlogSettingsResource())
api.add_route(CommentResource.route, CommentResource())
api.add_route(PostResource.route, PostResource())
api.add_route(PostCollectionResource.route, PostCollectionResource())
api.add_route(PostSearchResource.route, PostSearchResource())
api.add_route(PostCommentResource.route, PostCommentResource())
api.add_route(PostLikeResource.route, PostLikeResource())
api.add_route(PostViewResource.route, PostViewResource())
api.add_route(UserAuthenticationResource.route, UserAuthenticationResource())
api.add_route(UserRegistrationResource.route, UserRegistrationResource())
api.add_route(UserResource.route, UserResource())
api.add_route(UserAvatarMediaResource.route, UserAvatarMediaResource())
api.add_route(UserAvatarResource.route, UserAvatarResource())
api.add_route(ServiceDescriptionResource.route, ServiceDescriptionResource())

import inject
import falcon
import redis
from blog.constants import BLOG_REDIS_HOST, BLOG_REDIS_PORT, BLOG_DISABLE_CACHE
from blog.errors import ErrorHandler
from blog.middleware.users import UserProcessor
from blog.resources.comments import CommentResource
from blog.resources.admin import BlogSettingsResource
from blog.resources.posts import PostCollectionResource, PostResource, PostLikeResource, \
    PostViewResource, PostCommentResource, PostSearchResource
from blog.resources.users import UserAuthenticationResource, UserRegistrationResource, UserResource, \
    UserAvatarMediaResource, UserAvatarResource
from blog.resources.service import ServiceDescriptionResource
from blog.settings import settings

from falcon_multipart.middleware import MultipartMiddleware
from falcon_pagination_processor import PaginationProcessor
from falcon_redis_cache.middleware import RedisCacheMiddleware


api_middleware = [PaginationProcessor(),
                  MultipartMiddleware(),
                  UserProcessor()]

api = falcon.API(middleware=api_middleware)

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

if (not BLOG_DISABLE_CACHE):
    api_middleware.append(RedisCacheMiddleware(redis_host=BLOG_REDIS_HOST, redis_port=BLOG_REDIS_PORT))
    # configure DI for resource cache utilities
    inject.configure(lambda binder: binder.bind(redis.Redis, redis.StrictRedis(host=BLOG_REDIS_HOST, port=BLOG_REDIS_PORT)))

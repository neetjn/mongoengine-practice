import falcon
from blog.middleware.users import UserProcessor
from blog.resources.comments import CommentResource
from blog.resources.posts import PostCollectionResource, PostResource, PostLikeResource, \
    PostViewResource, PostCommentResource, PostSearchResource
from blog.resources.users import AuthResource, UserResource
from blog.resources.service import ServiceDescriptionResource


api = falcon.API(middleware=[UserProcessor()])

api.add_route(CommentResource.route, CommentResource())
api.add_route(PostResource.route, PostResource())
api.add_route(PostCollectionResource.route, PostCollectionResource())
api.add_route(PostSearchResource.route, PostResource())
api.add_route(PostCommentResource.route, PostCommentResource())
api.add_route(PostLikeResource.route, PostLikeResource())
api.add_route(PostViewResource.route, PostViewResource())
api.add_route(AuthResource.route, AuthResource())
api.add_route(UserResource.route, UserResource())
api.add_route(ServiceDescriptionResource.route, ServiceDescriptionResource())

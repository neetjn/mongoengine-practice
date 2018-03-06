import falcon
from blog.resources.posts import PostCollectionResource, PostResource

api = falcon.API()
api.add_route('/posts', PostCollectionResource)
api.add_route('posts/{post_id}', PostResource)

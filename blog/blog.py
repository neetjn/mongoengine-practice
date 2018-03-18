import falcon
# from blog.resources.posts import PostCollectionResource, PostResource

# api = falcon.API()
# api.add_route('/posts', PostCollectionResource)
# api.add_route('posts/{post_id}', PostResource)


class TestResource(object):

    def on_get(self, req, resp):
        print(self)
        resp.status = falcon.HTTP_200
        resp.body = 'lol'


api = falcon.API()

api.add_route('/test', TestResource())

print(dir(api))

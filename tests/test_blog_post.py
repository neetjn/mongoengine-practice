from falcon import testing
from blog.blog import api
from blog.resources.posts import PostResource, PostCollectionResource
from blog.settings import settings
from tests.utils import drop_database, generate_post_form, random_string


class BlogPostTests(testing.TestCase):

    def setUp(self):
        super(BlogPostTests, self).setUp()
        # refer to: http://falcon.readthedocs.io/en/stable/api/testing.html
        self.app = api
        # scrub database before each test
        drop_database()

    def test_create_get_post(self):
        res = self.simulate_get(PostCollectionResource.route)
        self.assertEqual(res.status_code, 200)
        # verify no post resources returned in post collection
        self.assertEqual(len(res.json.get('posts')), 0)
        # verify posts are created as intended
        post_form = generate_post_form(
            title=random_string(settings.rules.post.title_min_char),
            description=random_string(settings.rules.post.title_min_char),
            content=random_string(settings.rules.post.content_min_char))
        post_res = self.simulate_post(PostCollectionResource.route, body=post_form)
        # left here, need to provide auth token...
        self.assertEqual(post_res.status_code, 201)
        self.assertEqual(len(res.json.get('posts')), 1)

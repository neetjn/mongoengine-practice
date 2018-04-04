from falcon.testing import TestCase
from blog.blog import api
from blog.mediatypes import PostFormDtoSerializer
from blog.resources.posts import PostResource, PostCollectionResource
from blog.settings import settings
from blog.utils.serializers import to_json
from tests.generators.posts import generate_post_form_dto
from tests.mocks.users import create_user
from tests.utils import drop_database, normalize_href, random_string


class BlogPostTests(TestCase):

    def setUp(self):
        super(BlogPostTests, self).setUp()
        # refer to: http://falcon.readthedocs.io/en/stable/api/testing.html
        self.app = api
        # scrub database before each test
        drop_database()
        # get user credentials
        token = create_user(self)
        # construct request headers
        self.headers = {
            'Authorization': token
        }

    def test_core_post_resource(self):
        """Ensure a post resource can be created, fetched, updated, and deleted."""
        res = self.simulate_get(PostCollectionResource.route)
        self.assertEqual(res.status_code, 200)
        # verify no post resources returned in post collection
        self.assertEqual(len(res.json.get('posts')), 0)
        # verify posts are created as intended
        post_create_res = self.simulate_post(
            PostCollectionResource.route,
            body=to_json(PostFormDtoSerializer, generate_post_form_dto()),
            headers=self.headers)
        self.assertEqual(post_create_res.status_code, 201)
        post_collection_res = self.simulate_get(PostCollectionResource.route)
        self.assertEqual(post_collection_res.status_code, 200)
        self.assertEqual(len(post_collection_res.json.get('posts')), 1)
        # get resource href for created post
        created_post = post_collection_res.json.get('posts')[0]
        post_href = normalize_href(created_post.get('href'))
        # fetch post using extracted href
        post_res = self.simulate_get(post_href)
        self.assertEqual(created_post.get('title'), post_res.json.get('title'))
        self.assertEqual(created_post.get('description'), post_res.json.get('description'))
        self.assertEqual(created_post.get('content'), post_res.json.get('content'))
        self.assertEqual(created_post.get('author'), post_res.json.get('author'))
        # validate links for post in collection and payload from post resource
        expected_links = ('post-comment', 'post-like', 'post-view')
        for rel in expected_links:
            self.assertIsNotNone(
                next((ln for ln in created_post.get('links') if ln.get('rel') == rel), None))
            self.assertIsNotNone(
                next((ln for ln in post_res.json.get('links') if ln.get('rel') == rel), None))
        # update post resource and verify changes
        post_details = generate_post_form_dto()
        post_update_res = self.simulate_put(
            post_href,
            body=to_json(PostFormDtoSerializer, post_details),
            headers=self.headers)
        self.assertEqual(post_update_res.status_code, 204)
        updated_post_res = self.simulate_get(post_href)
        self.assertEqual(updated_post_res.json.get('title'), post_details.title)
        self.assertEqual(updated_post_res.json.get('description'), post_details.description)
        self.assertEqual(updated_post_res.json.get('content'), post_details.content)
        # delete post resource and validate expected behavior
        delete_post_res = self.simulate_delete(post_href, headers=self.headers)
        self.assertEqual(delete_post_res.status_code, 204)
        post_res = self.simulate_get(post_href)
        self.assertEqual(post_res.status_code, 404)
        post_collection_res = self.simulate_get(PostCollectionResource.route)
        self.assertEqual(len(post_collection_res.json.get('posts')), 0)

    def test_like_post(self):
        """Verify post resources can be liked."""
        self.simulate_post(
            PostCollectionResource.route,
            body=to_json(PostFormDtoSerializer, generate_post_form_dto()),
            headers=self.headers)
        post_collection_res = self.simulate_get(PostCollectionResource.route)
        created_post = post_collection_res.json.get('posts')[0]
        post_href = normalize_href(created_post.get('href'))
        self.assertEqual(created_post.get('likes'), 0)
        post_like_href = normalize_href(
            next(ln.get('href') for ln in created_post.get('links') if ln.get('rel') == 'post-like'))
        self.simulate_put(post_like_href, headers=self.headers)
        post_res = self.simulate_get(post_href)
        self.assertEqual(post_res.json.get('likes'), 1)
        self.simulate_put(post_like_href, headers=self.headers)
        post_res = self.simulate_get(post_href)
        self.assertEqual(post_res.json.get('likes'), 0)

import time
from falcon.testing import TestCase
from blog.blog import api
from blog.mediatypes import PostFormDtoSerializer, CommentFormDtoSerializer, \
    PostSearchSettingsDto, PostSearchSettingsDtoSerializer, PostSearchOptions
from blog.resources.posts import PostResource, PostCollectionResource, \
    PostSearchResource
from blog.settings import settings
from blog.utils.serializers import to_json
from tests.generators.comments import generate_comment_form_dto
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
        self.user, self.token = create_user(self)
        # construct request headers
        self.headers = {
            'Authorization': self.token
        }

    def test_core_post_resource(self):
        """Ensure a post resource can be created, fetched, updated, and deleted"""
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
        elapsed_start = time.clock() * 1000
        post_collection_res = self.simulate_get(PostCollectionResource.route)
        elapsed_delta = (time.clock() * 1000) - elapsed_start
        self.assertEqual(post_collection_res.status_code, 200)
        self.assertEqual(len(post_collection_res.json.get('posts')), 1)
        # verify caching works as intended
        elapsed_start = time.clock() * 1000
        self.simulate_get(PostCollectionResource.route)
        cached_delta = (time.clock() * 1000) - elapsed_start
        self.assertGreater(elapsed_delta / 2, cached_delta)
        # measurement subject to change, cached response should take no longer than 3 ms
        self.assertLess(cached_delta, 3.5)
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

    def test_search_post_critera(self):
        """Verify post resources can be searched by critera"""
        post_collection = [generate_post_form_dto() for _ in range(10)]
        for post in post_collection:
            self.simulate_post(
                PostCollectionResource.route,
                body=to_json(PostFormDtoSerializer, post),
                headers=self.headers)
        target_post = post_collection[-1]
        search_settings = PostSearchSettingsDto(
            query=target_post.content,
            options=[PostSearchOptions.CONTENT])
        post_search_res = self.simulate_post(
            PostSearchResource.route,
            body=to_json(PostSearchSettingsDtoSerializer, search_settings),
            headers=self.headers)
        self.assertEqual(post_search_res.status_code, 201)
        self.assertEqual(len(post_search_res.json.get('posts')), 1)
        found_post = post_search_res.json.get('posts')[0]
        self.assertEqual(target_post.title, found_post.get('title'))
        self.assertEqual(target_post.description, found_post.get('description'))
        self.assertEqual(target_post.content, found_post.get('content'))
        self.assertEqual(target_post.private, found_post.get('private'))
        self.assertEqual(target_post.featured, found_post.get('featured'))

    def test_search_post_author(self):
        """Verify post resources can be searched by author"""
        post_collection = [generate_post_form_dto() for _ in range(10)]
        for post in post_collection:
            self.simulate_post(
                PostCollectionResource.route,
                body=to_json(PostFormDtoSerializer, post),
                headers=self.headers)
        search_settings = PostSearchSettingsDto(
            query=self.user.username,
            options=[PostSearchOptions.AUTHOR])
        post_search_res = self.simulate_post(
            PostSearchResource.route,
            body=to_json(PostSearchSettingsDtoSerializer, search_settings),
            headers=self.headers)
        self.assertEqual(post_search_res.status_code, 201)
        self.assertEqual(len(post_search_res.json.get('posts')), 10)

    def test_like_post(self):
        """Verify post resources can be liked"""
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

    def test_view_post(self):
        """Verify post resources can be viewed"""
        self.simulate_post(
            PostCollectionResource.route,
            body=to_json(PostFormDtoSerializer, generate_post_form_dto()),
            headers=self.headers)
        post_collection_res = self.simulate_get(PostCollectionResource.route)
        created_post = post_collection_res.json.get('posts')[0]
        post_href = normalize_href(created_post.get('href'))
        self.assertEqual(created_post.get('views'), 0)
        post_view_href = normalize_href(
            next(ln.get('href') for ln in created_post.get('links') if ln.get('rel') == 'post-view'))
        self.simulate_put(post_view_href, headers=self.headers)
        post_res = self.simulate_get(post_href)
        self.assertEqual(post_res.json.get('views'), 1)

    def test_comment_post(self):
        """Verify comment resources can be created, updated, and deleted"""
        self.simulate_post(
            PostCollectionResource.route,
            body=to_json(PostFormDtoSerializer, generate_post_form_dto()),
            headers=self.headers)
        post_collection_res = self.simulate_get(PostCollectionResource.route)
        created_post = post_collection_res.json.get('posts')[0]
        self.assertEqual(created_post.get('comments'), 0)
        post_href = normalize_href(created_post.get('href'))
        post_res = self.simulate_get(post_href)
        self.assertEqual(len(post_res.json.get('comments')), 0)
        post_comment_href = normalize_href(
            next(ln.get('href') for ln in created_post.get('links') if ln.get('rel') == 'post-comment'))
        comment_form = generate_comment_form_dto()
        # verify comments are created as intended
        create_comment_res = self.simulate_post(
            post_comment_href,
            body=to_json(CommentFormDtoSerializer, comment_form),
            headers=self.headers)
        self.assertEqual(create_comment_res.status_code, 201)
        post_res = self.simulate_get(post_href)
        self.assertEqual(len(post_res.json.get('comments')), 1)
        created_comment = post_res.json.get('comments')[0]
        self.assertEqual(created_comment.get('content'), comment_form.content)
        # verify coment content can be updated
        comment_href = normalize_href(created_comment.get('href'))
        new_comment_form = generate_comment_form_dto()
        update_comment_res = self.simulate_put(
            comment_href,
            body=to_json(CommentFormDtoSerializer, new_comment_form),
            headers=self.headers)
        self.assertEqual(update_comment_res.status_code, 204)
        comment_res = self.simulate_get(comment_href)
        self.assertEqual(comment_res.json.get('content'), new_comment_form.content)
        # verify comment resources can be deleted
        delete_comment_res = self.simulate_delete(comment_href, headers=self.headers)
        self.assertEqual(delete_comment_res.status_code, 204)
        comment_res = self.simulate_get(comment_href)
        self.assertEqual(comment_res.status_code, 404)
        post_res = self.simulate_get(post_href)
        self.assertEqual(len(post_res.json.get('comments')), 0)

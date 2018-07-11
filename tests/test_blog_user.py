from falcon.testing import TestCase
from blog.blog import api
from blog.mediatypes import UserFormDtoSerializer
from blog.resources.users import UserResource
from blog.settings import settings
from blog.utils.serializers import to_json
from tests.generators.users import generate_user_form_dto
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

    def test_core_user_resource(self):
        """Ensure a user resource can be fetched, updated."""
        user_res = self.simulate_get(UserResource.route)
        self.assertEqual(user_res.status_code, 401)
        # verify user profile resurce can be retrieved as expected
        user_res = self.simulate_get(UserResource.route, headers=self.headers)
        self.assertEqual(user_res.status_code, 200)
        # verify user resource can be updated
        user_profile = generate_user_form_dto()
        put_user_res = self.simulate_put(
            UserResource.route,
            body=to_json(UserFormDtoSerializer, user_profile),
            headers=self.headers)
        self.assertEqual(put_user_res.status_code, 204)
        user_profile_res = self.simulate_get(UserResource.route, headers=self.headers)
        self.assertEqual(user_profile_res.json.get('username'), user_res.json.get('username'))
        self.assertEqual(user_profile_res.json.get('email'), user_profile.email)
        self.assertEqual(user_profile_res.json.get('fullName'), user_profile.full_name)
        self.assertEqual(user_profile_res.json.get('avatarHref'), user_profile.avatar_href)

    def test_user_avatar_disabled(self):
        """Verify user avatar functionality disabled with setting."""
        user_res = self.simulate_get(UserResource.route, headers=self.headers)


    def test_user_avatar_resource(self):
        """Ensure a user can upload and delete an avatar."""
        pass

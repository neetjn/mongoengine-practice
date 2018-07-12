import copy
import io
import os
from falcon.testing import TestCase
from blog.blog import api
from blog.mediatypes import UserFormDtoSerializer
from blog.resources.users import UserResource, BLOG_USER_RESOURCE_HREF_REL
from blog.settings import settings, save_settings, SettingsSerializer
from blog.utils.serializers import to_json
from tests.generators.users import generate_user_form_dto
from tests.mocks.users import create_user
from tests.utils import drop_database, normalize_href, random_string, find_link_href_json


# TODO: create tests for s3 avatar upload using fakes3


def create_multipart_form(data: bytes, fieldname: str, filename: str, content_type: str):
    """
    Basic emulation of a browser's multipart file upload
    """
    boundry = '----WebKitFormBoundary' + random_string(16)
    buff = io.BytesIO()
    buff.write(b'--')
    buff.write(boundry.encode())
    buff.write(b'\r\n')
    buff.write(('Content-Disposition: form-data; name="%s"; filename="%s"' % \
               (fieldname, filename)).encode())
    buff.write(b'\r\n')
    buff.write(('Content-Type: %s' % content_type).encode())
    buff.write(b'\r\n')
    buff.write(b'\r\n')
    buff.write(data)
    buff.write(b'\r\n')
    buff.write(boundry.encode())
    buff.write(b'--\r\n')
    headers = {'Content-Type': 'multipart/form-data; boundary=%s' %boundry}
    headers['Content-Length'] = str(buff.tell())
    return buff.getvalue(), headers


class BlogPostTests(TestCase):

    def setUp(self):
        super(BlogPostTests, self).setUp()
        # refer to: http://falcon.readthedocs.io/en/stable/api/testing.html
        self.app = api
        # scrub database before each test
        drop_database()
        # get user credentials
        token = create_user(self, avatar_href=None)
        # construct request headers
        self.headers = {
            'Authorization': token
        }

    def test_core_user_resource(self):
        """Ensure a user resource can be fetched, updated."""
        user_res = self.simulate_get(UserResource.route)
        self.assertEqual(user_res.status_code, 401)
        # verify user profile resurce can be retrieved as expectedUserFormDtoSerializer
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

    def test_user_avatar_disabled(self):
        """Ensure user avatar resources are not accessible when the feature is disabled."""
        global settings
        settings.user.allow_avatar_capability = False
        save_settings(settings, False)
        user_res = self.simulate_get(UserResource.route, headers=self.headers)
        avatar_href = user_res.json.get('avatarHref')
        # verify avatar cannot be fetched
        self.assertEqual(avatar_href, '')
        user_links = user_res.json.get('links')
        # can currently double as both upload and delete, may be subject to change
        user_avatar_resource_href = normalize_href(
            find_link_href_json(user_links, BLOG_USER_RESOURCE_HREF_REL.USER_AVATAR_UPLOAD))
        avatar_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'blog/static/default-avatar.png'))
        avatar_binary = open(avatar_path, 'rb').read()
        body, headers = create_multipart_form(avatar_binary, 'image', avatar_path, 'image/png')
        upload_headers = self.headers.copy()
        upload_headers.update(headers)
        # verify avatar can be uploaded
        avatar_res = self.simulate_post(
            user_avatar_resource_href,
            headers=upload_headers,
            body=body)
        self.assertEqual(avatar_res.status_code, 403)

    def test_user_avatar_resource(self):
        """Ensure a user can upload and delete an avatar."""
        user_res = self.simulate_get(UserResource.route, headers=self.headers)
        avatar_href = normalize_href(user_res.json.get('avatarHref'))
        avatar_res = self.simulate_get(avatar_href)
        # verify default avatar is served as expected
        self.assertEqual(avatar_res.status_code, 200)
        self.assertEqual(avatar_res.headers.get('content-type'), 'image/png')
        self.assertEqual(len(avatar_res.content), 6957)
        user_links = user_res.json.get('links')
        # can currently double as both upload and delete, may be subject to change
        user_avatar_resource_href = normalize_href(
            find_link_href_json(user_links, BLOG_USER_RESOURCE_HREF_REL.USER_AVATAR_UPLOAD))
        avatar_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'blog/static/default-avatar.png'))
        avatar_binary = open(avatar_path, 'rb').read()
        body, headers = create_multipart_form(avatar_binary, 'image', avatar_path, 'image/png')
        upload_headers = self.headers.copy()
        upload_headers.update(headers)
        # verify avatar can be uploaded
        avatar_res = self.simulate_post(
            user_avatar_resource_href,
            headers=upload_headers,
            body=body)
        self.assertEqual(avatar_res.status_code, 201)
        # verify uploaded avatar is served as expected
        avatar_res = self.simulate_get(avatar_href)
        self.assertEqual(avatar_res.status_code, 200)
        self.assertEqual(avatar_res.headers.get('content-type'), 'image/png')
        self.assertEqual(len(avatar_res.content), len(avatar_binary) + 42)
        # verify avatar is deleted as expected
        avatar_res = self.simulate_delete(user_avatar_resource_href, headers=self.headers)
        self.assertEqual(avatar_res.status_code, 204)
        avatar_res = self.simulate_get(avatar_href)
        self.assertEqual(avatar_res.status_code, 200)
        self.assertEqual(avatar_res.headers.get('content-type'), 'image/png')
        self.assertEqual(len(avatar_res.content), 6957)

    def test_user_avatar_resource_s3(self):
        """Ensure a user can upload an avatar via s3 (this test was designed for fakes3)"""
        pass

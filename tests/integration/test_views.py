import json
from http import HTTPStatus
from unittest import mock

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from lapka import get_app
from lapka.models import Animal


json_mime = 'application/json'


class TestViews(AioHTTPTestCase):

    async def get_application(self):
        return get_app()

    @unittest_run_loop
    async def test_animal_profile(self):
        animal_id = 'unique-id'
        valid_data = {
            'id': animal_id,
            'name': 'Name',
            'age': 5,
            'place': 'Wrocław',
            'since': '2017.01.01',
            'category': 'dog',
            'description': [
                'First paragraph',
                'Second paragraph',
            ],
        }
        animal = Animal(**valid_data)
        animal.save()
        req = await self.client.request('GET', '/animal/{}/'.format(animal_id))
        self.assertEqual(req.status, HTTPStatus.OK)
        self.assertEqual(req.content_type, json_mime)
        resp = await req.text()
        self.assertDictEqual(json.loads(resp), animal.to_dict())
        animal.remove()

    @unittest_run_loop
    async def test_animal_profile_invalid_id(self):
        req = await self.client.request('GET', '/animal/INVALID/')
        self.assertEqual(req.status, HTTPStatus.NOT_FOUND)
        resp = await req.text()
        self.assertDictEqual(json.loads(resp), {})

    @unittest_run_loop
    async def test_skip(self):
        req = await self.client.get('/animal/some-id/skip/some-id/')
        self.assertEqual(req.status, HTTPStatus.METHOD_NOT_ALLOWED)

        req = await self.client.post('/animal/some-id/skip/some-id/')
        self.assertEqual(req.status, HTTPStatus.OK)
        self.assertEqual(req.content_type, json_mime)
        self.assertDictEqual(json.loads(await req.text()), {})

    @unittest_run_loop
    async def test_matching(self):
        req = await self.client.get('/animal/matching/user-id/')
        self.assertEqual(req.status, HTTPStatus.OK)
        self.assertEqual(req.content_type, json_mime)


class TestAuth(AioHTTPTestCase):

    async def get_application(self):
        return get_app()

    @unittest_run_loop
    async def test_login_with_google(self):
        headers = {'Content-Type': json_mime}
        data = json.dumps({'idtoken': 'valid_token'})
        user_data = {'avatar': 'http"//example.com/pic', 'name': 'Betty', 'user': '1234567890'}

        async def fake_google():
            return user_data

        with mock.patch('lapka.views.auth_google', return_value=fake_google()) as m_auth:
            req = await self.client.post('/auth/google_token/', headers=headers, data=data)
            resp = await req.json()

            m_auth.assert_called_once()
            self.assertEqual(req.status, HTTPStatus.OK)
            self.assertEqual(req.content_type, json_mime)
            self.assertEqual(resp, user_data)
            # TODO Check if `user_data['user']` in session

    @unittest_run_loop
    async def test_login_with_google_no_token(self):
        headers = {'Content-Type': json_mime}
        data = json.dumps({})
        req = await self.client.post('/auth/google_token/', headers=headers, data=data)

        self.assertEqual(req.status, HTTPStatus.BAD_REQUEST)
        self.assertEqual(req.content_type, json_mime)
        self.assertEqual(await req.text(), data)

    @unittest_run_loop
    async def test_login_with_google_invalid_token(self):
        headers = {'Content-Type': json_mime}
        data = json.dumps({'idtoken': 'invalid_token'})
        user_data = {}

        async def fake_google():
            return user_data

        with mock.patch('lapka.views.auth_google', return_value=fake_google()) as m_auth:
            req = await self.client.post('/auth/google_token/', headers=headers, data=data)
            resp = await req.json()

            m_auth.assert_called_once()
            self.assertEqual(req.status, HTTPStatus.UNAUTHORIZED)
            self.assertEqual(req.content_type, json_mime)
            self.assertEqual(resp, user_data)
            # TODO Check if 'user' not in session

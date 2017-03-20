from http import HTTPStatus
from unittest import mock

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from lapka import get_app


class TestApp(AioHTTPTestCase):

    async def get_application(self):
        return get_app()

    @unittest_run_loop
    async def test_trailing_slash_on_get(self):
        animal_id = 'some-id'
        url = '/animal/{}/'.format(animal_id)

        async def fake_find():
            return {'id': animal_id}

        with mock.patch('lapka.views.find_animal', return_value=fake_find()) as mock_find:
            req = await self.client.get(url, allow_redirects=False)
            self.assertEqual(req.status, HTTPStatus.OK)
            self.assertEqual(req.method, 'GET')
            mock_find.assert_called_once_with(animal_id)

    @unittest_run_loop
    async def test_no_trailing_slash_on_get(self):
        url = '/animal/some-id'
        with mock.patch('lapka.views.find_animal', return_value=None) as mock_find:
            req = await self.client.get(url, allow_redirects=False)
            self.assertEqual(req.status, HTTPStatus.MOVED_PERMANENTLY)
            self.assertEqual(req.method, 'GET')
            self.assertEqual(mock_find.call_count, 0)

    @unittest_run_loop
    async def test_trailing_slash_on_post(self):
        url = '/animal/some-id/skip/some-user/'
        req = await self.client.post(url, allow_redirects=False)
        self.assertEqual(req.method, 'POST')
        self.assertEqual(req.status, HTTPStatus.OK)

    @unittest_run_loop
    async def test_no_trailing_slash_on_post(self):
        url = '/animal/some-id/skip/some-user'

        req = await self.client.post(url, allow_redirects=False)
        self.assertEqual(req.method, 'POST')
        self.assertEqual(req.status, HTTPStatus.MOVED_PERMANENTLY)

        # HTTP does not allow to disable GET request
        req = await self.client.post(url, allow_redirects=True)
        self.assertEqual(req.method, 'GET')
        self.assertEqual(req.status, HTTPStatus.METHOD_NOT_ALLOWED)

    @unittest_run_loop
    async def test_ui(self):
        url = '/ui/index.html'
        req = await self.client.get(url)
        self.assertEqual(req.status, HTTPStatus.OK)

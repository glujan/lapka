from http import HTTPStatus
from unittest import mock

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from lapka import get_app


class TestApp(AioHTTPTestCase):

    async def get_application(self, loop):
        return get_app(loop=loop)

    @unittest_run_loop
    async def test_trailing_slash(self):
        animal_id = 'some-id'
        url = '/animal/{}/'.format(animal_id)

        async def fake_find():
            return {'id': animal_id}

        with mock.patch('lapka.views.find_animal', return_value=fake_find()) as mock_find:
            req = await self.client.get(url, allow_redirects=False)
            self.assertEqual(req.status, HTTPStatus.OK)
            mock_find.assert_called_once_with(animal_id)

    @unittest_run_loop
    async def test_no_trailing_slash(self):
        animal_id = 'some-id'
        url = '/animal/{}'.format(animal_id)

        with mock.patch('lapka.views.find_animal', return_value=None) as mock_find:
            req = await self.client.get(url, allow_redirects=False)
            self.assertEqual(req.status, HTTPStatus.MOVED_PERMANENTLY)
            self.assertEqual(mock_find.call_count, 0)

import json
from http import HTTPStatus

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from lapka import get_app
from lapka.models import Animal


class TestViews(AioHTTPTestCase):

    async def get_application(self, loop):
        return get_app(loop=loop)

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
        resp = await req.text()
        self.assertDictEqual(json.loads(resp), animal.to_dict())
        animal.remove()

    @unittest_run_loop
    async def test_animal_profile_invalid_id(self):
        req = await self.client.request('GET', '/animal/INVALID/')
        self.assertEqual(req.status, HTTPStatus.NOT_FOUND)
        resp = await req.text()
        self.assertDictEqual(json.loads(resp), {})

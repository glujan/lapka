import unittest

from unittest import mock

from lapka import models, views
from tests.utils import AsyncMeta, fake_response as f_resp


class TestLogic(unittest.TestCase, metaclass=AsyncMeta):

    def setUp(self):
        animal_data = {
            'id': 'unique-id',
            'name': 'Name',
            'age': 5,
            'place': 'Wrocław',
            'description': [
                'First paragraph',
                'Second paragraph',
            ],
        }
        self.animal = models.Animal(**animal_data)

    async def test_find_animal(self):
        a_id = self.animal.a_id
        with mock.patch('lapka.models.Animal.find', return_value=self.animal):
            data = await views.find_animal(a_id)
            self.assertDictEqual(data, self.animal.to_dict())

    async def test_find_animal_invalid_id(self):
        a_id = self.animal.a_id + 'INVALID'
        with mock.patch('lapka.models.Animal.find', return_value=None):
            data = await views.find_animal(a_id)
            self.assertDictEqual(data, {})


class TestAuth(unittest.TestCase, metaclass=AsyncMeta):
    async def test_auth_google(self):
        id_token = 'valid_token'
        data = {
            'picture': 'http://example.com/pic',
            'given_name': 'John',
            'sub': '0123456789'
        }

        with mock.patch('lapka.views.aio_req', return_value=f_resp(data)) as mock_get:
            user = await views.auth_google(id_token)
            self.assertEqual(data['sub'], user['user'])
            self.assertEqual(data['picture'], user['avatar'])
            self.assertEqual(data['given_name'], user['name'])
            mock_get.assert_called_once()

    async def test_auth_google_invalid(self):
        id_token = 'invalid_token'
        data = {}

        with mock.patch('lapka.views.aio_req', return_value=f_resp(data, status=404)) as mock_get:
            user = await views.auth_google(id_token)
            self.assertDictEqual(user, {})
            mock_get.assert_called_once()

import unittest

from unittest import mock

from lapka import models, views
from tests.utils import AsyncMeta


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

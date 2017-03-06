import unittest

from lapka import views
from tests.utils import AsyncMeta


class TestLogic(unittest.TestCase, metaclass=AsyncMeta):

    def setUp(self):
        self.animal_data = {
            'id': 'unique-id',
            'name': 'Name',
            'age': 5,
            'place': 'Wrocław',
            'description': [
                'First paragraph',
                'Second paragraph',
            ],
        }

    async def test_find_animal(self):
        a_id = self.animal_data['id']
        data = await views.find_animal(a_id)
        self.assertDictEqual(data, self.animal_data)

    async def test_find_animal_invalid_id(self):
        a_id = self.animal_data['id'] + 'INVALID'
        data = await views.find_animal(a_id)
        self.assertDictEqual(data, {})

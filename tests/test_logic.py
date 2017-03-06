import unittest
from unittest import mock

from aiohttp import web

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


class TestAppCreation(unittest.TestCase, metaclass=AsyncMeta):

    def test_get_app(self):
        with mock.patch('asyncio.get_event_loop', return_value=self.loop):
            app = views.get_app()
            self.assertIsInstance(app, web.Application)
            self.assertIs(app.loop, self.loop)

    def test_get_app_with_loop(self):
        loop = mock.Mock()
        app = views.get_app(loop=loop)
        self.assertIsInstance(app, web.Application)
        self.assertIs(app.loop, loop)

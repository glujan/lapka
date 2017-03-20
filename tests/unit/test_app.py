import unittest

from aiohttp import web

from lapka import get_app
from tests.utils import AsyncMeta


class TestApp(unittest.TestCase, metaclass=AsyncMeta):

    def test_get_app(self):
        app = get_app()
        self.assertIsInstance(app, web.Application)
        self.assertEqual(app.loop, None, 'Passing a loop is depracated')

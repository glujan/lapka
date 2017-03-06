import unittest
from unittest import mock

from aiohttp import web

from lapka import get_app
from tests.utils import AsyncMeta


class TestApp(unittest.TestCase, metaclass=AsyncMeta):

    def test_get_app(self):
        with mock.patch('asyncio.get_event_loop', return_value=self.loop):
            app = get_app()
            self.assertIsInstance(app, web.Application)
            self.assertIs(app.loop, self.loop)

    def test_get_app_with_loop(self):
        loop = mock.Mock()
        app = get_app(loop=loop)
        self.assertIsInstance(app, web.Application)
        self.assertIs(app.loop, loop)

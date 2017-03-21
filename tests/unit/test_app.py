import unittest

from aiohttp import web

from lapka import get_app
from tests.utils import AsyncMeta


class TestGetApp(unittest.TestCase):

    def test_get_app(self):
        app = get_app()
        self.assertIsInstance(app, web.Application)
        self.assertEqual(app.loop, None, 'Passing a loop is depracated')

    def test_session(self):
        with unittest.mock.patch('lapka.aios_setup') as m_setup:
            _ = get_app()
            m_setup.assert_called_once()

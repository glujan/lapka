import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlparse

from aiohttp import ClientSession
from lxml.etree import XPath, XPathSyntaxError

from tests.utils import AsyncMeta, fake_response as f_resp
from lapka import fetch


class TestShelter(unittest.TestCase, metaclass=AsyncMeta):
    @classmethod
    def setUpClass(cls):
        fp = Path(__file__).parent / 'assets' / 'animals_list_01.html'
        with open(fp, 'r') as f:
            cls.animals_list = f.read()

    def setUp(self):
        self.shelter = fetch.Shelter()

    async def test_parse(self):
        urls = ['1', '2', '3']

        async def dummy_urls(*args):
            for u in urls:
                yield u

        mock_parse = patch.object(self.shelter, '_parse', return_value={}).start()
        mock_urls = patch.object(self.shelter, '_animals_urls', side_effect=dummy_urls).start()

        with patch.object(ClientSession, 'get', return_value=f_resp(self.animals_list)) as mock_get:
            async with ClientSession() as session:
                resp = await self.shelter.parse(session)

        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), len(urls))
        self.assertEqual(mock_get.call_count, len(urls))
        self.assertEqual(mock_parse.call_count, len(urls))
        for r in resp:
            self.assertIn(r['url'], urls)

        mock_urls.assert_called_once()

        mock_parse.stop()
        mock_urls.stop()

    async def test__animals_urls(self):
        animals = ['http://schroniskowroclaw.pl/displaywp_project/burbon-22117/',
                   'http://schroniskowroclaw.pl/displaywp_project/nelson-10117/',
                   'http://schroniskowroclaw.pl/displaywp_project/burbon-22117/',
                   'http://schroniskowroclaw.pl/displaywp_project/nelson-10117/']
        urls = []

        self.shelter.animal_url = fetch.SchroniskoWroclawPl.animal_url
        self.shelter.next_url = fetch.SchroniskoWroclawPl.next_url
        self.shelter.start_url = 'http://example.com'

        with patch.object(ClientSession, 'get', return_value=f_resp(self.animals_list)) as mock_get:
            async with ClientSession() as session:
                self.shelter.session = session
                # TODO Pyflakes doesn't support async comprehension
                async for url in self.shelter._animals_urls():
                    urls.append(url)

            self.assertListEqual(urls, animals)
            self.assertEqual(mock_get.call_count, 2)

            mock_get.assert_any_call(self.shelter.start_url)
            mock_get.assert_any_call('http://schroniskowroclaw.pl/zwierzeta-do-adopcji/?page=2')

    async def test__animals_urls_invalid_html(self):
        urls = []

        self.shelter.animal_url = fetch.SchroniskoWroclawPl.animal_url
        self.shelter.next_url = fetch.SchroniskoWroclawPl.next_url
        self.shelter.start_url = 'http://example.com'

        with patch.object(ClientSession, 'get', return_value=f_resp('Invalid')) as mock_get:
            async with ClientSession() as session:
                self.shelter.session = session
                # TODO Pyflakes doesn't support async comprehension
                async for url in self.shelter._animals_urls():
                    urls.append(url)

            mock_get.assert_called_once_with(self.shelter.start_url)
            self.assertListEqual([], urls)


class TestSchroniskoWroclawPl(unittest.TestCase, metaclass=AsyncMeta):
    @classmethod
    def setUpClass(cls):
        fp = Path(__file__).parent / 'assets' / 'animal_01.html'
        with open(fp, 'r') as f:
            cls.animal = f.read()

    def setUp(self):
        self.shelter = fetch.SchroniskoWroclawPl()

    def test_class_attributes(self):
        try:
            XPath(self.shelter.animal_url)
            XPath(self.shelter.next_url)
        except XPathSyntaxError as e:
            self.fail(e.msg)

        url = urlparse(self.shelter.start_url)
        self.assertIn(url.scheme, ('http', 'https'))
        self.assertTrue(url.netloc)

    def test__parse(self):
        valid_data = {
            'name': 'Nelson',
            'id': '101/17',
            'photos': ['http://schroniskowroclaw.pl/wp-content/uploads/2017/02/DSCF9115.jpg',
                       'http://schroniskowroclaw.pl/wp-content/uploads/2017/02/DSCF9120.jpg'],
            'since': '18.02.2017',
            'category': 'Koty',  # TODO i18n
            'description': ['Nelson ma 4-lata, został oddany. Duży, gruby, piękny kocur. Wykastrowany.',
                            'Będzie do adopcji od: 4.03.2017']
        }
        data = self.shelter._parse(self.animal)
        self.assertDictEqual(data, valid_data)

    def test__parse_invalid_html(self):
        data = self.shelter._parse('')
        self.assertDictEqual(data, {})

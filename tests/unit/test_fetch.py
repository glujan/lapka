import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urljoin, urlparse

from aiohttp import ClientSession
from lxml.etree import XPath, XPathSyntaxError

from tests.utils import AsyncMeta, fake_response as f_resp
from lapka import fetch


class TestShelter(unittest.TestCase, metaclass=AsyncMeta):
    @classmethod
    def setUpClass(cls):
        cls.animals_list = """
            <a class='animal' href="/animal01">Animal 01</a>
            <a class="animal" href="http://example.com/animal02">Animal 02</a>
            <a class="next" href="http://example.com/?p=2">Next</a>
        """

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

    async def test_parse_not_overwrite_session(self):
        async def dummy_urls(*args):
            for u in []:
                yield u

        mock_parse = patch.object(self.shelter, '_parse', return_value={}).start()
        mock_urls = patch.object(self.shelter, '_animals_urls', side_effect=dummy_urls).start()

        with patch.object(ClientSession, 'get', return_value=f_resp(self.animals_list)):
            async with ClientSession() as session:
                self.shelter.session = session
                await self.shelter.parse(None)
                self.assertIs(self.shelter.session, session)

        mock_parse.stop()
        mock_urls.stop()

    async def test__animals_urls(self):
        animals = ["http://example.com/animal01", "http://example.com/animal02"] * 2

        urls = []
        base = 'http://example.com'

        orig_start_url = fetch.Shelter.start_url
        fetch.Shelter.start_url = base
        self.shelter = fetch.Shelter()
        self.shelter.animal_url = "//a[@class='animal']/@href"
        self.shelter.next_url = "//a[@class='next']/@href"
        self.assertEqual(self.shelter.start_url, base)

        with patch.object(ClientSession, 'get', return_value=f_resp(self.animals_list)) as mock_get:
            async with ClientSession() as session:
                self.shelter.session = session
                # TODO Pyflakes doesn't support async comprehension
                async for url in self.shelter._animals_urls():
                    urls.append(url)

            self.assertListEqual(urls, animals)
            self.assertEqual(mock_get.call_count, 2)

            mock_get.assert_any_call(self.shelter.start_url)
            mock_get.assert_any_call("http://example.com/?p=2")

        fetch.Shelter.start_url = orig_start_url

    async def test__animals_urls_invalid_html(self):
        urls = []

        self.shelter.animal_url = "//a[@class='animal']/@href"
        self.shelter.next_url = "//a[@class='next']/@href"
        self.shelter.start_url = 'http://example.com'

        with patch.object(ClientSession, 'get', return_value=f_resp('Invalid')) as mock_get:
            async with ClientSession() as session:
                self.shelter.session = session
                # TODO Pyflakes doesn't support async comprehension
                async for url in self.shelter._animals_urls():
                    urls.append(url)

            mock_get.assert_called_once_with(self.shelter.start_url)
            self.assertListEqual([], urls)


class TestConcreteShelter:

    shelter_class = None
    animals_urls = {"animals": [], "next_page": ""}

    def setUp(self):
        self.shelter = self.shelter_class()

    def test_class_attributes(self):
        try:
            XPath(self.shelter.animal_url)
            XPath(self.shelter.next_url)
        except XPathSyntaxError as e:
            self.fail(e.msg)

        url = urlparse(self.shelter.start_url)
        self.assertIn(url.scheme, ('http', 'https'))
        self.assertTrue(url.netloc)

    def test__parse_invalid_html(self):
        with self.subTest("Empty html"):
            data = self.shelter._parse("")
            self.assertDictEqual(data, {})

        with self.subTest("Invalid HTML"):
            data = self.shelter._parse("<html><p>Invalid</p></html>")
            self.assertDictEqual(data, {})

    async def test__animals_urls(self):
        animals = self.animals_urls["animals"]
        urls = []

        with patch.object(ClientSession, 'get', return_value=f_resp(self.animals_list)) as mock_get:
            async with ClientSession() as session:
                self.shelter.session = session
                # TODO Pyflakes doesn't support async comprehension
                async for url in self.shelter._animals_urls():
                    urls.append(url)

            self.assertListEqual(urls, animals)
            self.assertEqual(mock_get.call_count, 2)

            mock_get.assert_any_call(self.shelter.start_url)
            mock_get.assert_any_call(self.animals_urls["next_page"])


class TestSchroniskoWroclawPl(TestConcreteShelter, unittest.TestCase, metaclass=AsyncMeta):
    shelter_class = fetch.SchroniskoWroclawPl
    animals_urls = {
        "animals": [
            "http://schroniskowroclaw.pl/displaywp_project/burbon-22117/",
            "http://schroniskowroclaw.pl/displaywp_project/nelson-10117/",
        ] * 2,
        "next_page": "http://schroniskowroclaw.pl/zwierzeta-do-adopcji/?page=2",
    }

    @classmethod
    def setUpClass(cls):
        fp = Path(__file__).parent / 'assets' / 'animal_01.html'
        with open(fp, 'r') as f:
            cls.animal = f.read()

        fp = Path(__file__).parent / 'assets' / 'animals_list_01.html'
        with open(fp, 'r') as f:
            cls.animals_list = f.read()

    def test__full_url(self):
        for url in ("/partial-url", "other-relative", "/another?p=1", "http://example.org/remote"):
            with self.subTest(url=url):
                full = self.shelter._full_url(url)
                base = '{url.scheme}://{url.netloc}/'.format(url=urlparse(self.shelter.start_url))
                valid_full = urljoin(base, url)
                self.assertEqual(valid_full, full)

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


class TestNaPaluchuWawPl(TestConcreteShelter, unittest.TestCase, metaclass=AsyncMeta):

    shelter_class = fetch.NaPaluchuWawPl
    animals_urls = {
        "animals": [
            "http://www.napaluchu.waw.pl/czekam_na_ciebie/wszystkie_zwierzeta_do_adopcji/011100429",
            "http://www.napaluchu.waw.pl/czekam_na_ciebie/wszystkie_zwierzeta_do_adopcji/000801535",
        ] * 2,
        "next_page": "http://www.napaluchu.waw.pl/czekam_na_ciebie/wszystkie_zwierzeta_do_adopcji:2",
    }

    @classmethod
    def setUpClass(cls):
        fp = Path(__file__).parent / 'assets' / 'animal_11.html'
        with open(fp, 'r') as f:
            cls.animal = f.read()

        fp = Path(__file__).parent / 'assets' / 'animals_list_11.html'
        with open(fp, 'r') as f:
            cls.animals_list = f.read()

    def test__parse(self):
        valid_data = {
            'name': 'Rambo',
            'id': '1833/16',
            'photos': [
                'http://www.napaluchu.waw.pl/files/animals_napaluchu/big/170117065222.jpg',
                'http://www.napaluchu.waw.pl/files/animals_napaluchu/big/170117065223.jpg'],
            'since': '02.10.2016',
            'category': 'Pies',  # TODO i18n
            'description': ['Rambo to wyjątkowy pies dla wyjątkowego opiekuna.',
                            'Ma zaledwie rok, wciąż rośnie, poznaje świat, wszystko go interesuje.',
                            'Ze względu na domieszkę krwi charta angielskiego potrzebuje bardzo dużo ruchu.',
                            'Skąd: Warszawa,  ul.Bokserska'],
        }
        data = self.shelter._parse(self.animal)
        self.assertDictEqual(data, valid_data)

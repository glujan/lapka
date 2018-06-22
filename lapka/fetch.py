"""Fetch and parse data from shelters' websites to a common format."""
import asyncio
from functools import partial
from urllib.parse import urljoin, urlparse

import aiohttp

from lxml import etree


class Shelter:
    """Base class for extracting data about from shelters websites."""

    animal_url = ""
    """"XPath expression to find URLs to animals profiles"""

    next_url = ""
    """XPath expression to find next website in pagination"""

    start_url = ""
    """URL to the beginning of animals list"""

    def __init__(self, session=None):
        """Initialize a new SchroniskoWroclawPl instance."""
        self.session = session
        url = urlparse(self.start_url)
        self._full_url = partial(urljoin, f"{url.scheme}://{url.netloc}/")
        """Transform partial URL to a full one. Use with instance of this class."""

    async def parse(self, session=None):
        """Crawl shelter's website and return data in an unified format."""
        if session:
            self.session = session

        async def task(url):
            async with self.session.get(url) as resp:
                content = await resp.text()
            data = self._parse(content)
            data['url'] = url
            return data

        coros = [task(a_url) async for a_url in self._animals_urls()]
        return await asyncio.gather(*coros)

    async def _animals_urls(self):
        url = self.start_url

        while url:
            async with self.session.get(url) as resp:
                content = await resp.read()

            doc = etree.HTML(content)
            for a_url in doc.xpath(self.animal_url):
                yield self._full_url(a_url)

            try:
                new_url = self._full_url(doc.xpath(self.next_url)[0])
                url = new_url if new_url != url else None
            except IndexError:
                url = None

    def _parse(self, content: str) -> dict:
        """Extract data from animal's page."""
        raise NotImplementedError


class SchroniskoWroclawPl(Shelter):
    """Extract data about animals from schroniskowroclaw.pl website."""

    animal_url = "//div[@class='filter-item']//h5/a/@href"
    next_url = "//ul[@class='page-numbers']//a[@class='next page-numbers']/@href"
    start_url = "http://schroniskowroclaw.pl/zwierzeta-do-adopcji/"

    def _parse(self, content):
        html = etree.HTML(content)
        if html is None:
            return {}

        try:
            doc = html.xpath("//div[@class='project']")[0]
            name = doc.xpath("//div[@class='project-details']//h1/text()")[0].split(' ')[0]
            a_id, since, *other = doc.xpath("//*[@class='project-info']//span/text()")
            category = other[0] if other else None  # FIXME Normalize categories
            photos = map(self._full_url, doc.xpath("//div[@class='project-slider']//img/@src"))

            data = {
                'name': name.strip().title(),
                'id': a_id,
                'since': since,
                'category': category,
                'photos': list(photos),
                'description': doc.xpath("//div[@class='project-details']/p/text()"),
            }
        except (IndexError, etree.XMLSyntaxError):
            # TODO Add logging that couldn't parse website
            data = {}

        return data


class NaPaluchuWawPl(Shelter):
    """Extract data about animals from schroniskowroclaw.pl website."""

    animal_url = "//div[@id='ani_search_result_cont']//a[@class='animals_btn_list_more']/@href"
    next_url = "//div[@class='pagination']/a[@class='next']/@href"
    start_url = "http://www.napaluchu.waw.pl/czekam_na_ciebie/wszystkie_zwierzeta_do_adopcji"

    def _parse(self, content):
        html = etree.HTML(content)
        if html is None:
            return {}

        try:
            doc = html.xpath("//div[@class='ani_one_container']")[0]
            name = doc.xpath("//h5/text()")[0]
            category, *_, since, a_id = doc.xpath("//div[@class='info']//span[not(@class)]/text()")
            photos = map(self._full_url, doc.xpath("//div[@id='main_image_cont']//a/@href"))

            raw_desc = doc.xpath("//div[@class='description']//text()")
            desc = filter(bool, map(lambda s: s.strip(), raw_desc))

            data = {
                'name': name.strip().title(),
                'id': a_id.split(': ')[-1],
                'since': since.strip().split(': ')[-1],
                'category': category.strip().split(': ')[-1],  # TODO Normalize
                'photos': list(photos),
                'description': list(desc),
            }
        except (IndexError, etree.XMLSyntaxError):
            # TODO Add logging that couldn't parse website
            data = {}

        return data


if __name__ == '__main__':

    async def _main():
        import pickle
        from itertools import chain
        from lapka import models

        async with aiohttp.ClientSession() as session:
            tasks = (sh.parse(session) for sh in (SchroniskoWroclawPl(), NaPaluchuWawPl()))
            fetched = await asyncio.gather(*tasks)

        animals = [models.AnimalDummy(**data) for data in chain(*fetched)]
        print('Gathered', len(animals), 'animals')

        with open(models._pickle_path, 'wb') as fp:
            pickle.dump(animals, fp)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main())
    loop.close()

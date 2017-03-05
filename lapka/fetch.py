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
        self._full_url = partial(
            urljoin,
            '{url.scheme}://{url.netloc}/'.format(url=urlparse(self.start_url))
        )
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

        coros = []
        # TODO Pyflakes doesn't support async comprehension
        async for a_url in self._animals_urls():
            coros.append(task(a_url))

        return await asyncio.gather(*coros)

    async def _animals_urls(self):
        url = self.start_url

        while url:
            async with self.session.get(url) as resp:
                content = await resp.read()

            doc = etree.HTML(content)
            for a_url in doc.xpath(self.animal_url):
                yield a_url

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
        try:
            doc = etree.HTML(content).xpath("//*[@class='project']")[0]
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


if __name__ == '__main__':
    async def _main():
        async with aiohttp.ClientSession() as session:
            shelter = SchroniskoWroclawPl()
            animals = await shelter.parse(session)

        print('Gathered {} animals'.format(len(animals)))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main())
    loop.close()

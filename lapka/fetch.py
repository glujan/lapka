"""Fetch and parse data from shelters' websites to a common format."""
import asyncio

import aiohttp
from lxml import etree


class SchroniskoWroclawPl:
    """Extract data about animals from schroniskowroclaw.pl website."""

    animal_url = "//div[@class='filter-item']//h5/a/@href"
    next_url = "//ul[@class='page-numbers']//a[@class='next page-numbers']/@href"
    start_url = 'http://schroniskowroclaw.pl/zwierzeta-do-adopcji/'

    def __init__(self, session=None):
        """Initialize a new SchroniskoWroclawPl instance."""
        self.session = session

    async def parse(self, session=None):
        """Crawl shelter's website and return data in an unified format."""
        if session:
            self.session = session

        async def task(a_url):
            async with self.session.get(a_url) as resp:
                content = await resp.text()
            data = self._parse(content)
            data['url'] = a_url
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
                new_url = doc.xpath(self.next_url)[0]
                url = new_url if new_url != url else None
            except IndexError:
                url = None

    def _parse(self, content):
        name = ''
        try:
            doc = etree.HTML(content).xpath("//*[@class='project']")[0]
            name = doc.xpath("//div[@class='project-details']//h1/text()")[0].split(' ')[0]
            a_id, since, *other = doc.xpath("//*[@class='project-info']//span/text()")
            category = other[0] if other else None  # FIXME Normalize categories

            data = {
                'name': name,
                'id': a_id,
                'since': since,
                'category': category,
                'photos': doc.xpath("//div[@class='project-slider']//img/@src"),
                'description': doc.xpath("//div[@class='project-details']/p/text()"),
            }
        except (IndexError, etree.XMLSyntaxError):
            # TODO Add logging that couldn't parse website
            data = {}

        return data


async def _main():
    async with aiohttp.ClientSession() as session:
        shelter = SchroniskoWroclawPl()
        animals = await shelter.parse(session)

    print('Gathered {} animals'.format(len(animals)))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main())
    loop.close()

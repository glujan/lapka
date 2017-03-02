"""Fetch and parse data from shelters' websites to a common format."""
import asyncio
import json
from http import HTTPStatus
from urllib.parse import unquote

import aiohttp
import aiohttp.web
from lxml import etree


class Fetcher(dict):
    def __init__(self, session=None, *args, **kwargs):
        self._session = session
        self._loop = asyncio.get_event_loop()
        self._sem = asyncio.Semaphore(100)
        super().__init__(*args, **kwargs)

    async def fetch(self, request):
        url = unquote(request.match_info.get('url', ''))

        if not url:
            status, data = HTTPStatus.BAD_REQUEST, None
        else:
            status, data = await self._do_stuff(url)

        return aiohttp.web.Response(status=status, text=json.dumps(data))

    async def _do_stuff(self, url):
        parser = self.get(url, None)
        if not parser:
            return HTTPStatus.NOT_ACCEPTABLE, None

        data = []

        async with self._sem:
            data = await parser.parse()

        status = HTTPStatus.OK  # FIXME Set valid status

        return status, data


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

        animals = []
        async for a_url in self._animals_urls():  # TODO Create tasks and run them at once
            async with self.session.get(a_url) as resp:
                content = await resp.text()
            data = self._parse(content)
            data['url'] = a_url
            animals.append(data)
        return animals

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


def _main():
    with aiohttp.ClientSession() as session:
        handler = Fetcher(session, {
            'schroniskowroclaw.pl': SchroniskoWroclawPl(session),
        })

        app = aiohttp.web.Application()
        app.router.add_get("/fetch/{url}", handler.fetch)
        aiohttp.web.run_app(app)


if __name__ == '__main__':
    _main()

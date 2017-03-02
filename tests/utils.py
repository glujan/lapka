"""Make writing tests easier."""
import asyncio
import functools
import inspect

import aiohttp
import yarl


def _run_in_loop(coro):

    @functools.wraps(coro)
    def inner(self, *args, **kwargs):
        return self.loop.run_until_complete(coro(self, *args, **kwargs))

    return inner


def _init_loop(func):

    @functools.wraps(func)
    def inner(self):
        val = func(self)

        asyncio.set_event_loop(None)
        self.loop = asyncio.new_event_loop()
        return val
    return inner


def _close_loop(func):

    @functools.wraps(func)
    def inner(self):
        val = func(self)

        if not self.loop.is_closed():
            self.loop.call_soon(self.loop.stop)
            self.loop.run_forever()  # FIXME Is this needed?
            self.loop.close()
        return val
    return inner


class AsyncMeta(type):
    """Transform any class member coroutine function to a regular one."""

    def __new__(cls, name, bases, namespace, **kwds):
        """
        Create a modified cls object.

        Decorate `setUp` and `tearDown` methods to open and close an event loop
        properly and decorate all coroutines to make them run in an event loop
        using `asyncio.AbstractEventLoop.run_until_complete` function.
        """
        result = super().__new__(cls, name, bases, namespace, **kwds)
        for name, coro in inspect.getmembers(result, predicate=inspect.iscoroutinefunction):
            setattr(result, name, _run_in_loop(coro))

        if hasattr(result, 'setUp'):
            setattr(result, 'setUp', _init_loop(result.setUp))

        if hasattr(result, 'tearDown'):
            setattr(result, 'tearDown', _init_loop(result.tearDown))

        return result


class _FakeClientResponse(aiohttp.ClientResponse):
    def __init__(self, method, url, content, *args):
        if isinstance(url, str):
            url = yarl.URL(url)
        self._fake_content = content
        super().__init__(method, url, *args)

    async def read(self):
        return self._fake_content.encode('utf8')

    async def text(self):
        return self._fake_content


def fake_response(content, method='', *args):
    """Create a `aiohttp.ClientResponse` instance with fake content."""
    return _FakeClientResponse(method, yarl.URL(''), content, *args)

"""Lapka is an app to help browse and adopt animals from shelters."""

import asyncio

from aiohttp import web

from lapka import views


def get_app(loop=None, **kwargs):
    """Create ready to use `aiohttp.web.Application` instance with Łapka API routes."""
    if loop is None:
        loop = asyncio.get_event_loop()

    middlewares = [
        web.normalize_path_middleware(),
    ]

    app = web.Application(loop=loop, middlewares=middlewares, **kwargs)
    app.router.add_route('GET', r'/animal/{id:[\w-]+}/', views._animal_profile)
    app.router.add_route('GET', r'/animal/matching/{user:[\w-]+}/', views._matching)
    app.router.add_route('POST', r'/animal/skip/{user:[\w-]+}/', views._skip)

    return app

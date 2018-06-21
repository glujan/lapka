"""Lapka is an app to help browse and adopt animals from shelters."""

from pathlib import Path
from secrets import token_bytes

from aiohttp import web

from aiohttp_session import setup as aios_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from lapka import views


def get_app(**kwargs):
    """Create ready to use `aiohttp.web.Application` instance with Łapka API routes."""
    middlewares = [web.normalize_path_middleware()]

    app = web.Application(middlewares=middlewares, **kwargs)
    app.router.add_get(r'/animal/{id:[\w-]+}/', views._animal_profile)
    app.router.add_get(r'/animal/matching/{user:[\w-]+}/', views._matching)
    app.router.add_post(r'/animal/{id:[\w-]+}/skip/{user:[\w-]+}/', views._skip)
    app.router.add_post(r'/auth/google_token/', views._google_token)
    app.router.add_static('/ui', Path('./ui/dist'))
    app.router.add_static('/static', Path('./ui/dist/static'))
    secret_key = token_bytes(32)
    aios_setup(app, EncryptedCookieStorage(secret_key))

    return app

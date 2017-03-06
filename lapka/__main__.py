"""Start Lapka web server."""


if __name__ == '__main__':
    from aiohttp import web

    from lapka import get_app

    app = get_app()
    web.run_app(app)

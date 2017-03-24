"""Views implementing Lapka API."""

from http import HTTPStatus

from aiohttp import request as aio_req, web

from aiohttp_session import get_session

from lapka.models import AnimalDummy


async def find_animal(a_id: str) -> dict:
    """Find animal with given id and return serialized data."""
    try:
        animal = AnimalDummy.find(a_id)
        data = animal.to_dict()
    except AttributeError:
        data = {}

    return data


async def auth_google(id_token: str) -> dict:
    """
    Verify with Google service if id_token is correct.

    For docs see https://developers.google.com/identity/sign-in/web/backend-auth
    """
    url = 'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={}'.format(id_token)
    async with aio_req('GET', url) as resp:
        status = resp.status
        data = {}
        if status == HTTPStatus.OK:
            user = await resp.json()
            data['avatar'] = user['picture']
            data['name'] = user['given_name']
            data['user'] = user['sub']
    return data


async def _skip(request):
    # TODO Implement _skip function
    #  u_id = request.match_info.get('user', None)
    status = HTTPStatus.OK
    return web.json_response({}, status=status)


async def _matching(request):
    # TODO Implement _matching function
    #  u_id = request.match_info.get('user', None)

    data = ['some-id', 'some-id']
    status = HTTPStatus.OK
    return web.json_response(data, status=status)


async def _animal_profile(request):
    """Return data of animal with given id."""
    animal_id = request.match_info.get('id', None)

    data = await find_animal(animal_id)
    status = HTTPStatus.OK if data else HTTPStatus.NOT_FOUND

    return web.json_response(data, status=status)


async def _google_token(request):
    post_data = await request.json()
    id_token = post_data.get('idtoken', None)

    if id_token is None:
        return web.json_response({}, status=HTTPStatus.BAD_REQUEST)

    data = await auth_google(id_token)
    session = await get_session(request)
    if 'user' in data:
        session['user'] = data.pop('user')
        status = HTTPStatus.OK
    else:
        data.clear()
        session.pop('user', None)
        status = HTTPStatus.UNAUTHORIZED

    return web.json_response(data, status=status)

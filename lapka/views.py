"""Views implementing Lapka API."""

from http import HTTPStatus

from aiohttp import web

from lapka.models import Animal


async def find_animal(a_id: str) -> dict:
    """Find animal with given id and return serialized data."""
    try:
        animal = Animal.find(a_id)[0]
        data = animal.to_dict()
    except IndexError:
        data = {}

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

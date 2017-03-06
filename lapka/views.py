"""Views implementing Lapka API."""

from http import HTTPStatus

from aiohttp import web


async def find_animal(a_id: str) -> dict:
    """Find animal with given id and return serialized data."""
    # TODO Use a storage instead of constants

    if a_id.endswith('INVALID'):
        data = {}
    else:
        data = {
            'id': a_id,
            'name': 'Name',
            'age': 5,
            'place': 'Wrocław',
            'description': [
                'First paragraph',
                'Second paragraph',
            ],
        }

    return data


async def _animal_profile(request):
    """Return data of animal with given id."""
    animal_id = request.match_info.get('id', None)

    data = await find_animal(animal_id)
    status = HTTPStatus.OK if data else HTTPStatus.NOT_FOUND

    return web.json_response(data, status=status)

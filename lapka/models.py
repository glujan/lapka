"""Łapka's persistence layer.

Represent and operate on data stored in a persistence storage (like a database).
"""

import pickle


_pickle_path = 'fetched_data.pickle'


class AnimalBase:
    """Base class for Animals persistence."""

    def __init__(self, **kwargs):
        """Create an animal instance."""
        self.category = kwargs.pop('category', '')
        self.name = kwargs.pop('name', '')
        self.a_id = kwargs.pop('id', '')
        self.since = kwargs.pop('since', '')
        self.photos = kwargs.pop('photos', list())
        self.description = kwargs.pop('description', list())
        self.url = kwargs.pop('url', '')
        self.place = kwargs.pop('place', '')

    def to_dict(self):
        """Serialize an instance to a dictionary format."""
        return {
            'name': self.name,
            'id': self.a_id,
            'since': self.since,
            'category': self.category,
            'photos': self.photos,
            'description': self.description,
            'url': self.url,
            'place': self.place,
        }

    def save(self):
        """Store an instance data in a persistance layer."""
        raise NotImplementedError

    def remove(self):
        """Remove an instance data from persistence layer."""
        raise NotImplementedError

    @classmethod
    def find(cls, animal_id):
        """Find an animal by a given identifier."""
        raise NotImplementedError


class AnimalDummy(AnimalBase):
    """"Animal dummy model using a pickle storage."""

    _data = []

    @staticmethod
    def _load():
        try:
            with open(_pickle_path, 'rb') as fp:
                _data = pickle.load(fp)
        except FileNotFoundError:
            _data = []
        return _data

    def save(self):
        """Store an instance data in a persistance layer."""
        self.remove()
        self._data.append(self)

    def remove(self):
        """Remove an instance data from persistence layer."""
        try:
            self._data.remove(self)
        except ValueError:
            pass

    @classmethod
    def find(cls, animal_id):
        """Find an animal by a given identifier."""
        if not cls._data:
            cls._data = cls._load()

        try:
            animal = next(filter(lambda a: a.a_id == animal_id, cls._data))
        except StopIteration:
            animal = None
        return animal

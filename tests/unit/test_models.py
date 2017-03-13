import pickle
import unittest

from unittest import mock

from lapka.models import Animal, _load


class TestAnimal(unittest.TestCase):

    def setUp(self):
        self.animal_data = {
            'name': 'Doggy',
            'id': 'uniqueid',
            'since': '2017.03.18',
            'category': ['dog', ],
            'photos': ['photo1', 'photo2'],
            'description': ['line1', 'line2'],
            'url': 'http://example.org',
            'place': 'City',
        }
        self.animal = Animal(**self.animal_data)

    def test_save(self):
        result = Animal.find(self.animal.a_id)
        self.assertListEqual(result, [])

        self.animal.save()
        result = Animal.find(self.animal.a_id)
        self.assertListEqual(result, [self.animal, ])

    def test_remove(self):
        self.animal.save()

        result = Animal.find(self.animal.a_id)
        self.assertListEqual(result, [self.animal, ])

        self.animal.remove()
        result = Animal.find(self.animal.a_id)
        self.assertListEqual(result, [])

    def test_to_dict(self):
        data = self.animal.to_dict()
        self.assertDictEqual(data, self.animal_data)


class TestLoad(unittest.TestCase):
    def setUp(self):
        self.data = ['sample', 'data']

    def test__load(self):
        pickled = pickle.dumps(self.data)
        with mock.patch('builtins.open', mock.mock_open(read_data=pickled)) as m_open:
            data = _load()
            self.assertListEqual(data, self.data)
            m_open.assert_called_once()

    def test__load_no_file(self):
        with mock.patch('builtins.open', side_effect=FileNotFoundError()) as m_open:
            data = _load()
            self.assertListEqual(data, list())
            m_open.assert_called_once()

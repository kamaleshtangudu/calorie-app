from django.test import TestCase, tag
from apps.base.utils import ConstantEnum


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class TestClass(ConstantEnum):
    PATIENT = 'patient'
    PROFILE = 'profile'


@tag('ConstantEnum')
class TestConstantEnum(TestCase):
    """ Test cases for ConstantEnum class."""

    def test_new__normal(self):
        self.assertEqual(TestClass.PATIENT, 'patient')

    def test_get_item(self):
        self.assertEqual(TestClass["PATIENT"], 'patient')

    def test_next_item(self):
        test_iter = iter(TestClass)

        self.assertEqual(next(test_iter), ('patient', 'PATIENT'))
        self.assertEqual(next(test_iter), ('profile', 'PROFILE'))

    def test_next_item__exception(self):
        self.assertRaises(StopIteration, next, TestClass)

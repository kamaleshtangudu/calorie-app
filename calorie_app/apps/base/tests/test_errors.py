from django.test import TestCase, tag

from apps.base.errors import get_error_code, get_error_message


@tag('BaseErrors')
class TestBaseErrors(TestCase):
    """ Test cases for base errors"""

    def test_get_error_code__default_key(self):
        self.assertEqual(get_error_code(''), 8999)

    def test_get_error_message__default_key(self):
        self.assertEqual(get_error_message(''),
                         'Something went wrong! Please try again later.')

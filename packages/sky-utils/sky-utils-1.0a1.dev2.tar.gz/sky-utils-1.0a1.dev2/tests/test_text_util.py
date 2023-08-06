import unittest

from sky.utils.text import camel_case_to_spaces, camel_case_to_underscore


class TextUtilTestCase(unittest.TestCase):
    def test_camel_case_to_spaces(self):
        self.assertEqual('device type', camel_case_to_spaces('Device Type'))

    def test_camel_case_to_underscore(self):
        self.assertEqual('device_type', camel_case_to_underscore('Device Type'))


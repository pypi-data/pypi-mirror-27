import unittest


class BaseUtilTestCase(unittest.TestCase):
    """
    base util tests
    """
    def test_import_module(self):
        """
        simple test to see if import_module works as expected :)
        """
        from sky.utils.base import import_module
        from datetime import datetime

        func_str_correct = 'datetime.datetime'
        func_str_wrong = 'datetime.datetime.nope'

        func_correct = import_module(func_str_correct)
        self.assertEqual(func_correct, datetime)

        # test if raise exception false returns None as expected
        func_wrong = import_module(func_str_wrong, raise_exception=False)
        self.assertEqual(func_wrong, None)

        with self.assertRaises(ImportError):
            import_module(func_str_wrong)



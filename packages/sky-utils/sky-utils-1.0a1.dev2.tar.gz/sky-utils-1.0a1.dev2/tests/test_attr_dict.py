import unittest


class AttrDictTestCase(unittest.TestCase):
    """
    attrdict tests
    """
    def setUp(self):
        from sky.utils.attr_dict import AttrDict
        self.attr_dict = AttrDict(
            x=15,
            y=30
        )

    def test_attr_dict_iteration(self):
        for k, v in self.attr_dict.items():
            if k not in ['x', 'y'] and v not in [15, 30]:
                self.assertTrue(False, "Key/Values doesn't match!")
        self.assertTrue(True, "Iterated AttrDict successfully!")

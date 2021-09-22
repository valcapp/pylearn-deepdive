import unittest

from helpers import InsufficientResource, check_natural, check_sufficient

class TestChecks(unittest.TestCase):
    def test_check_natural(self):
        self.assertIsNone(
            check_natural(4)
        )
        with self.assertRaises(TypeError):
            check_natural('hello')
        with self.assertRaises(TypeError):
            check_natural(4.3)
    
    def test_check_sufficient(self):
        self.assertIsNone(
            check_sufficient(10,10)
        )
        self.assertIsNone(
            check_sufficient(10,9)
        )
        with self.assertRaises(InsufficientResource):
            check_sufficient(4,5)
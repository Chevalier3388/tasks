from modul_with_tests.divide_by_zero_unittest import divide
import unittest


class TestDivide(unittest.TestCase):
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(10, 0)

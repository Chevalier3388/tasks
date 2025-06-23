import unittest

from modul_with_tests.social_age import get_social_status

class TestSocialAge(unittest.TestCase):

    def test_can_get_child_age(self):
        age = 8
        target_res = "ребёнок"
        func_res = get_social_status(age)
        self.assertEqual(target_res, func_res)

    def test_cannot_pass_str_as_age(self):
        age = "old"
        with self.assertRaises(ValueError):
            get_social_status(age)
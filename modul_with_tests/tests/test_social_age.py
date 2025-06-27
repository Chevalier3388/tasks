import unittest

import pytest

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



@pytest.mark.parametrize("age, status", [
    (10, "ребёнок"),
    (17, "подросток"),
    (19, "взрослый"),
    (55, "пожилой"),
    (69, "пенсионер")
])
def test_social_age(age, status):
    assert get_social_status(age) == status


def test_negative():
    with pytest.raises(ValueError):
        get_social_status(-1)

def test_vlue_error():
    with pytest.raises(ValueError):
        get_social_status("abc")
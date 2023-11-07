import unittest
from pixian_ai.utils import (
    enforce_types,
    param_exists,
    validate_param,
    validate_hex,
    validate_css,
    validate_wh,
)


class EnforceTypesDecoratorTest(unittest.TestCase):
    def test_enforce_types(self):
        @enforce_types
        def test_func(self, a: int, b: str):
            return True

        self.assertTrue(test_func(None, 1, "test"))
        with self.assertRaises(TypeError):
            test_func(None, "1", "test")


class ParamExistsTest(unittest.TestCase):
    def test_param_exists(self):
        with self.assertRaises(ValueError):
            param_exists(["test1", "test2", "test"], [None, None, None])
        self.assertIsNone(param_exists(["test1", "test2", "test"], [1, None, None]))


class ValidateParamTest(unittest.TestCase):
    def test_validate_param(self):
        with self.assertRaises(ValueError):
            validate_param("test_range", 5, (1, 3))
        with self.assertRaises(ValueError):
            validate_param("test_option", "a", ["b", "c", "d"])
        with self.assertRaises(ValueError):
            validate_param("test_option", "a", ("b", "c", "d"))
        self.assertIsNone(validate_param("test_range", 2, (1, 3)))
        self.assertIsNone(validate_param("test_option", "b", ["b", "c", "d"]))


class ValidateHexTest(unittest.TestCase):
    def test_validate_hex(self):
        with self.assertRaises(ValueError):
            validate_hex("test_hex", "invalid")
        with self.assertRaises(ValueError):
            validate_hex("test_hex", "#ZZZZZZ")
        self.assertIsNone(validate_hex("test_hex", "#FFFFFF"))


class ValidateCSSTest(unittest.TestCase):
    def test_validate_css(self):
        with self.assertRaises(ValueError):
            validate_css("test_css", "invalid")
        with self.assertRaises(ValueError):
            validate_css("test_css", "1px 2px 3px 4px 5px")
        self.assertIsNone(validate_css("test_css", "1px 2px 3px 4px"))


class ValidateWHTest(unittest.TestCase):
    def test_validate_wh(self):
        with self.assertRaises(ValueError):
            validate_wh("test_wh", "invalid")
        with self.assertRaises(ValueError):
            validate_wh("test_wh", "10 20 30")
        with self.assertRaises(ValueError):
            validate_wh("test_wh", "10px 20px")
        self.assertIsNone(validate_wh("test_wh", "1920 1080"))

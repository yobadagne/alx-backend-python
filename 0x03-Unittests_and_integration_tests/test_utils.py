#!/usr/bin/env python3
"""
    unit test for nestedmap
"""
import unittest
from typing import Dict, Tuple, Union
from parameterized import parameterized
from unittest.mock import Mock, patch
from utils import (access_nested_map , get_json, memoize)

class TestAccessNestedMap(unittest.TestCase):
    """Tests the `access_nested_map` function."""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Dict, path: Tuple[str], expected: Union[Dict, int]) -> None:
        """Tests `access_nested_map`'s output."""
        self.assertEqual(access_nested_map(nested_map, path), expected)
    @parameterized.expand([
        ({}, ("a", ),KeyError),
        ({"a": 1}, ("a","b"), KeyError),
        ])
    def test_access_nested_map_exception(self, nested_map:Dict, path: Tuple[str], exception: Exception) -> None:
        """ Test for Exception"""
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)
class TestGetJson(unittest.TestCase):
    """ Test the get json function"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
        ])
    def test_get_json(self, test_url:str, test_payload:Dict) -> None:
        """ Test for json output"""
        formock = {'json.return_value' : test_payload}
        with patch("requests.get", return_value = Mock(**formock)) as req_get:
            self.assertEqual(get_json(test_url),test_payload)
            req_get.assert_called_once_with(test_url)
class TestMemoize(unittest.TestCase):
    """ Test for memoize"""
    def test_memoize(self) -> None:
        """ Test memoize"""
        class TestClass:
            def a_method(self):
                return 42
            @memoize
            def a_property(self):
                return self.a_method()
        with patch.object(TestClass,"a_method",return_value=lambda: 42) as memo:
            test_class = TestClass()
            self.assertEqual(test_class.a_property(), 42)
            self.assertEqual(test_class.a_property(), 42)
            memo.assert_called_once()
if __name__ == '__main__':
    unittest.main()

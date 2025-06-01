#!/usr/bin/env python3
"""
A module for testing the utils module.

"""
from parameterized import parameterized
import unittest
import requests
from unittest.mock import (Mock, patch)
from utils import (access_nested_map, get_json, memoize)
from typing import (Dict, Tuple, Any)


class TestAccessNestedMap(unittest.TestCase):
    """Tests the `access_nested_map` function."""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
   ])
    def test_access_nested_map(self, nested_map: Dict, path: Tuple[str], expected: Any) -> None:
        """Test `access_nested_map`'s output when with input cases."""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
   ])
    def test_access_nested_map_exception(self, nested_map: Dict, path: Tuple[str]) -> None:
        """Test `access_nested_map`'s output to see that a KeyError is raised."""
        with self.assertRaises(KeyError):
           access_nested_map(nested_map, path) 


class TestGetJson(unittest.TestCase):
    "Tests the `get_json` function."

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('requests.get')
    def test_get_json(self, test_url: str, test_payload: Dict, mock_get: Mock) -> None:
        "Tests that the `get_json` function returns expected result and is called only once with url."
        mock_get.return_value.json.return_value = test_payload
        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)

class TestMemoize(unittest.TestCase):
    """Tests the `memoize` decorator"""
    
    def test_memoize(self):
        """Tests that the `memoize` function returns the expected output and is called only once"""
        
        class TestClass():
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
        
        with patch.object(TestClass, 'a_method', return_value = 42) as mock_method:
            test_obj = TestClass()
            result1 = test_obj.a_property
            result2 = test_obj.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()
#!/usr/bin/env python3
"""
A module for testing the utils module.

"""
from parameterized import parameterized, parameterized_class

import unittest
from utils import access_nested_map
from typing import (Dict, Tuple, Any)

class TestAccessNestedMap(unittest.TestCase):
    """Tests the `access_nested_map` function."""
    @parameterized.expand([
        ("no_nest", {"a": 1}, ("a",), 1),
        ("one_nest", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("two_nest", {"a": {"b": 2}}, ("a", "b"), 2)
   ])
    
    def test_access_nested_map(self, name: str, nested_map: Dict, path: Tuple[str], expected: Any) -> None:
        """Test `access_nested_map` output."""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

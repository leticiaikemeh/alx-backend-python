#!/usr/bin/env python3
from parameterized import parameterized, parameterized_class

import unittest
from utils import access_nested_map
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ("no_nest", {"a": 1}, ("a",), 1),
        ("one_nest", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("two_nest", {"a": {"b": 2}}, ("a", "b"), 2)
   ])
    def test_access_nested_map(self, name: str, nested_map: Mapping, path: Sequence, expected: Any):
        """Test valid nested map cases"""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)


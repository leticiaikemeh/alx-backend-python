#!/usr/bin/env python3
"""
A module for testing the client module.
"""

from parameterized import parameterized, parameterized_class
import unittest
from unittest.mock import Mock, PropertyMock, patch
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from utils import access_nested_map, get_json, memoize
from typing import Dict


class TestGithubOrgClient(unittest.TestCase):
    """Test the `GithubOrgClient` class."""

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"})
    ])
    @patch('client.get_json')
    def test_org(self, test_org_name: str, expected: Dict,
                 mock_get_json: Mock) -> None:
        """Test that GithubOrgClient.org returns the correct value."""
        mock_get_json.return_value = expected
        test_client = GithubOrgClient(test_org_name)
        result = test_client.org
        self.assertEqual(result, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{test_org_name}"
        )

    def test_public_repos_url(self) -> None:
        """Test that `_public_repos_url` returns the expected URL."""
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/test/repos"
            }
            test_client = GithubOrgClient("test")
            result = test_client._public_repos_url
            self.assertEqual(result, "https://api.github.com/orgs/test/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """Test that `public_repos` returns expected repository names."""
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = \
                "https://api.github.com/orgs/unakraft/repos"
            mock_get_json.return_value = [
                {"name": "repo1"},
                {"name": "repo2"}
            ]
            test_client = GithubOrgClient("unakraft")
            result = test_client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/unakraft/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo: Dict, license_key: str,
                         expected: bool) -> None:
        """Test that `has_license` returns the correct boolean."""
        test_client = GithubOrgClient("test")
        result = test_client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(('org_payload', 'repos_payload',
                      'expected_repos', 'apache2_repos'), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient."""

    @classmethod
    def setUpClass(cls) -> None:
        """Patch `requests.get` before all tests."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = [
            Mock(json=lambda: cls.org_payload),
            Mock(json=lambda: cls.repos_payload)
        ]

    def test_public_repos(self) -> None:
        """Test `public_repos` integration with all repos."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Test `public_repos` filtered by license."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"),
                         self.apache2_repos)

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop patcher after all tests."""
        cls.get_patcher.stop()

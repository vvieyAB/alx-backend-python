#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class."""

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        # Create test payload
        test_payload = {"org": org_name, "data": "test_data"}
        
        # Configure the mock to return test payload
        mock_get_json.return_value = test_payload

        # Create client instance
        client = GithubOrgClient(org_name)

        # Call the org property
        result = client.org

        # Assert that get_json was called once with expected URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        
        # Assert that the result equals the test payload
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test that GithubOrgClient._public_repos_url returns expected URL."""
        # Test payload with repos_url
        test_payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
        
        # Patch the org property to return our test payload
        with patch('client.GithubOrgClient.org', 
                  new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            
            # Create client instance
            client = GithubOrgClient("testorg")
            
            # Get the public repos URL
            result = client._public_repos_url
            
            # Assert the result is correct
            self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that GithubOrgClient.public_repos returns expected repos."""
        # Mock the _public_repos_url property
        test_repos_url = "https://api.github.com/orgs/testorg/repos"
        test_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "gpl"}},
        ]
        
        # Mock get_json to return test repos payload
        mock_get_json.return_value = test_repos_payload
        
        # Create client instance and mock _public_repos_url
        client = GithubOrgClient("testorg")
        with patch('client.GithubOrgClient._public_repos_url',
                  new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = test_repos_url
            
            # Call public_repos method
            result = client.public_repos()
            
            # Assert the result is correct (list of repo names)
            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected_repos)
            
            # Assert that _public_repos_url was called once
            mock_repos_url.assert_called_once()
            
            # Assert that get_json was called once with correct URL
            mock_get_json.assert_called_once_with(test_repos_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that GithubOrgClient.has_license returns expected result."""
        # Create client instance (org name doesn't matter for this test)
        client = GithubOrgClient("testorg")
        
        # Call has_license method
        result = client.has_license(repo, license_key)
        
        # Assert the result is correct
        self.assertEqual(result, expected)


@parameterized_class([
    {
        'org_payload': org_payload,
        'repos_payload': repos_payload,
        'expected_repos': expected_repos,
        'apache2_repos': apache2_repos
    }
    for org_payload, repos_payload, expected_repos, apache2_repos in [
        # This would be populated with actual fixtures from fixtures.py
        # For now, we'll use placeholder variables
        (org_payload, repos_payload, expected_repos, apache2_repos)
    ]
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Set up class method to mock requests.get."""
        # Create a patcher for requests.get
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        
        # Configure side_effect to return different payloads based on URL
        def side_effect(url):
            mock_response = Mock()
            if "orgs/testorg" in url:
                mock_response.json.return_value = cls.org_payload
            elif "repos" in url:
                mock_response.json.return_value = cls.repos_payload
            return mock_response
        
        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down class method to stop the patcher."""
        cls.get_patcher.stop()

    def test_public_repos_integration(self):
        """Integration test for public_repos method."""
        # Create client instance
        client = GithubOrgClient("testorg")
        
        # Call public_repos method
        result = client.public_repos()
        
        # Assert the result matches expected_repos
        self.assertEqual(result, self.expected_repos)
        
        # Assert requests.get was called twice (org + repos)
        self.assertEqual(self.mock_get.call_count, 2)

    def test_public_repos_with_license_integration(self):
        """Integration test for public_repos with license filter."""
        # Create client instance
        client = GithubOrgClient("testorg")
        
        # Call public_repos method with license filter
        result = client.public_repos(license="apache-2.0")
        
        # Assert the result matches apache2_repos
        self.assertEqual(result, self.apache2_repos)
        
        # Assert requests.get was called twice (org + repos)
        self.assertEqual(self.mock_get.call_count, 2)


if __name__ == '__main__':
    unittest.main()
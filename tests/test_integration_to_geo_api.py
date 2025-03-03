import unittest
from unittest.mock import patch, Mock
import requests
from src.GeoLocationData import (
    GeoLocationData,
    ConnectionError,
    RateLimitError,
    UnauthorizedError,
)


class TestGeoLocationDataErrors(unittest.TestCase):
    """Integration tests for error handling in GeoLocationData class"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.geo_locator = GeoLocationData()
        self.test_zip = "90210"
        self.test_city_state = "Los Angeles, CA"
        self.invalid_format = "InvalidLocation"

    @patch("src.GeoLocationData.requests.get")
    def test_connection_error(self, mock_get):
        """Test that ConnectionError is raised when connection fails."""
        # Configure the mock to raise a ConnectionError
        mock_get.side_effect = requests.ConnectionError("Connection failed")

        # Verify that our custom ConnectionError is raised
        with self.assertRaises(ConnectionError) as context:
            self.geo_locator.get_geoloc_data(self.test_zip)

        # Verify the error message
        self.assertIn("CONNECTION ERROR", str(context.exception))

    @patch("src.GeoLocationData.requests.get")
    def test_rate_limit_error(self, mock_get):
        """Test that RateLimitError is raised when rate limit is exceeded."""
        # Create a mock response with 429 status code
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.json.return_value = {"message": "Rate limit exceeded"}
        mock_get.return_value = mock_response

        # Verify that our custom RateLimitError is raised
        with self.assertRaises(RateLimitError) as context:
            self.geo_locator.get_geoloc_data(self.test_zip)

        # Verify the error message
        self.assertIn("RATE LIMIT ERROR", str(context.exception))
        self.assertIn(self.test_zip, str(context.exception))

    @patch("src.GeoLocationData.requests.get")
    def test_unauthorized_error(self, mock_get):
        """Test that UnauthorizedError is raised when API key is invalid."""
        # Create a mock response with 401 status code
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"message": "Invalid API key"}
        mock_get.return_value = mock_response

        # Verify that our custom UnauthorizedError is raised
        with self.assertRaises(UnauthorizedError) as context:
            self.geo_locator.get_geoloc_data(self.test_zip)

        # Verify the error message
        self.assertIn("UNAUTHORIZED ERROR", str(context.exception))

    @patch("src.GeoLocationData.requests.get")
    def test_not_found_error(self, mock_get):
        """Test error handling for location not found."""
        # Create a mock response with 404 status code
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Get geolocation data for non-existent location
        results = self.geo_locator.get_geoloc_data(self.test_zip)

        # Verify that the result is empty and an error message was recorded
        self.assertEqual(len(results), 0)
        self.assertEqual(len(self.geo_locator.errors), 1)
        self.assertIn("NOTFOUND", self.geo_locator.errors[0])
        self.assertIn(self.test_zip, self.geo_locator.errors[0])

    @patch("src.GeoLocationData.requests.get")
    def test_read_timeout_with_retry(self, mock_get):
        """Test read timeout with retry mechanism."""
        # First call raises ReadTimeout, second call succeeds
        mock_get.side_effect = [
            requests.ReadTimeout("Read timed out"),
            Mock(
                status_code=200,
                json=lambda: [
                    {"name": "Beverly Hills", "lat": 34.0736, "lon": -118.4004}
                ],
            ),
        ]

        # Should succeed on retry
        results = self.geo_locator.get_geoloc_data(self.test_zip)

        # Verify that we got the result after retry
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Beverly Hills")

    @patch("src.GeoLocationData.requests.get")
    def test_read_timeout_max_retries_exceeded(self, mock_get):
        """Test read timeout when max retries are exceeded."""
        # Configure mock to always raise ReadTimeout
        mock_get.side_effect = requests.ReadTimeout("Read timed out")

        # Should fail after max retries
        with self.assertRaises(TimeoutError) as context:
            self.geo_locator.get_geoloc_data(self.test_zip)

        # Verify error message
        self.assertIn("Read timeout after", str(context.exception))

    def test_invalid_format_error(self):
        """Test error handling for invalid location format."""
        # Get geolocation data for location with invalid format
        results = self.geo_locator.get_geoloc_data(self.invalid_format)

        # Verify that the result is empty and an error message was recorded
        self.assertEqual(len(results), 0)
        self.assertEqual(len(self.geo_locator.errors), 1)
        self.assertIn("INVALID FORMAT", self.geo_locator.errors[0])
        self.assertIn(self.invalid_format, self.geo_locator.errors[0])

    @patch("src.GeoLocationData.requests.get")
    def test_general_http_error(self, mock_get):
        """Test error handling for general HTTP errors."""
        # Create a mock response with 500 status code
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.url = "http://test.com"
        mock_response.json.return_value = {"message": "Internal server error"}
        mock_get.return_value = mock_response

        # Get geolocation data
        results = self.geo_locator.get_geoloc_data(self.test_zip)

        # Verify that the result is empty and an error message was recorded
        self.assertEqual(len(results), 0)
        self.assertEqual(len(self.geo_locator.errors), 1)
        self.assertIn("ERROR", self.geo_locator.errors[0])
        self.assertIn("500", self.geo_locator.errors[0])

    @patch("src.GeoLocationData.requests.get")
    def test_json_decode_error(self, mock_get):
        """Test error handling when response is not valid JSON."""
        # Create a mock response that raises JSONDecodeError
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.url = "http://test.com"
        mock_response.json.side_effect = requests.JSONDecodeError("Invalid JSON", "", 0)
        mock_response.text = "Not JSON"
        mock_get.return_value = mock_response

        # Get geolocation data
        results = self.geo_locator.get_geoloc_data(self.test_zip)

        # Verify that the result is empty and an error message was recorded
        self.assertEqual(len(results), 0)
        self.assertEqual(len(self.geo_locator.errors), 1)
        # The error handler should use response.text when json() fails
        self.assertIn("Not JSON", self.geo_locator.errors[0])

    @patch("src.GeoLocationData.requests.get")
    def test_unhandled_exception(self, mock_get):
        """Test error handling for unhandled exceptions."""
        # Configure mock to raise an unexpected exception
        mock_get.side_effect = Exception("Unexpected error")

        # Testing system exit is a bit tricky with unittest
        with self.assertRaises(SystemExit):
            self.geo_locator.get_geoloc_data(self.test_zip)

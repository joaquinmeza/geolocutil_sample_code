from tests.values import (
    VALID_10001,
    VALID_NY_NY,
    NO_VALIDS,
    HELP_MESSAGE,
    SKIPPED_MESSAGE,
)
from tests.base_test_class import BaseTestClass


class TestGeolocationUtilNoFlags(BaseTestClass):

    def test_help_message(self):
        stdout, stderr, return_code = self.get_stdout_output("--help")
        self.validate_stdout(stdout, stderr, return_code, HELP_MESSAGE)

    def test_with_valid_zip_code(self):
        stdout, stderr, return_code = self.get_stdout_output("10001")
        expected = self._get_expected_output("10001", VALID_10001)
        self.validate_stdout(stdout, stderr, return_code, expected)

    def test_with_valid_city_state(self):
        stdout, stderr, return_code = self.get_stdout_output("New York, NY")
        expected = self._get_expected_output("New York, NY", VALID_NY_NY)
        self.validate_stdout(stdout, stderr, return_code, expected)

    def test_with_invalid_zip_code(self):
        stdout, stderr, return_code = self.get_stdout_output("00033")
        self.validate_stdout(
            stdout, stderr, return_code, f"{NO_VALIDS}\n{SKIPPED_MESSAGE}\n"
        )

    def test_with_invalid_city_state(self):
        stdout, stderr, return_code = self.get_stdout_output("faketown, CA")
        self.validate_stdout(
            stdout, stderr, return_code, f"{NO_VALIDS}\n{SKIPPED_MESSAGE}\n"
        )

    def test_valid_zip_code_with_invalid_city_state(self):
        stdout, stderr, return_code = self.get_stdout_output("10001", "faketown, CA")
        expected = self._get_expected_output("10001", VALID_10001)
        self.validate_stdout(stdout, stderr, return_code, expected)

    def test_valid_city_state_with_invalid_zip_code(self):
        stdout, stderr, return_code = self.get_stdout_output("00033", "New York, NY")
        expected = self._get_expected_output("New York, NY", VALID_NY_NY)
        self.validate_stdout(stdout, stderr, return_code, expected)

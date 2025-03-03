from tests.values import VALID_00501, VALID_HAGATNA, NO_VALIDS, SKIPPED_MESSAGE
from tests.base_test_class import BaseTestClass


class TestGeolocationUtilWithJFlag(BaseTestClass):

    def test_with_valid_zip_code(self):
        stdout, stderr, return_code = self.get_stdout_output("-j", "00501")
        expected = self._get_expected_output("00501", VALID_00501, ensure_ascii=True)
        self.validate_stdout(stdout, stderr, return_code, expected)

    def test_with_valid_city_state(self):
        stdout, stderr, return_code = self.get_stdout_output("-j", "Hagatna, GU")
        expected = self._get_expected_output(
            "Hagatna, GU", VALID_HAGATNA, ensure_ascii=True
        )
        self.validate_stdout(stdout, stderr, return_code, expected)

    def test_with_invalid_zip_code(self):
        stdout, stderr, return_code = self.get_stdout_output("-j", "00033")
        self.validate_stdout(
            stdout, stderr, return_code, f"{NO_VALIDS}\n{SKIPPED_MESSAGE}\n"
        )

    def test_with_invalid_city_state(self):
        stdout, stderr, return_code = self.get_stdout_output("-j", "faketown, CA")
        self.validate_stdout(
            stdout, stderr, return_code, f"{NO_VALIDS}\n{SKIPPED_MESSAGE}\n"
        )

    def test_valid_zip_code_with_invalid_city_state(self):
        stdout, stderr, return_code = self.get_stdout_output(
            "-j", "00501", "faketown, CA"
        )
        expected = self._get_expected_output("00501", VALID_00501, ensure_ascii=True)
        self.validate_stdout(stdout, stderr, return_code, expected)

    def test_valid_city_state_with_invalid_zip_code(self):
        stdout, stderr, return_code = self.get_stdout_output(
            "-j", "00033", "Hagatna, GU"
        )
        expected = self._get_expected_output(
            "Hagatna, GU", VALID_HAGATNA, ensure_ascii=True
        )
        self.validate_stdout(stdout, stderr, return_code, expected)

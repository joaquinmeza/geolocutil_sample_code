from tests.values import (
    VALID_MADISON_WI_P_FLAG,
    VALID_12345_P_FLAG,
    SKIPPED_MESSAGE,
    LINE_SPLIT,
    HEADER,
    VALID_MULTIPLE_P_FLAG,
)
from tests.base_test_class import BaseTestClass


class TestGeolocationUtilWithPFlag(BaseTestClass):

    @staticmethod
    def _get_expected_output_for_p_flag(*messages):
        _list = [LINE_SPLIT, HEADER, LINE_SPLIT]
        for message in messages:
            _list.append(message)
        _list.append(LINE_SPLIT)
        _list.append(SKIPPED_MESSAGE)
        return "\n".join(_list) + "\n"

    def test_with_valid_zip_code(self):
        stdout, stderr, return_code = self.get_stdout_output("-p", "12345")
        expected = self._get_expected_output_for_p_flag(VALID_12345_P_FLAG)
        self.validate_stdout(stdout, stderr, return_code, expected)

    def test_with_valid_city_state(self):
        stdout, stderr, return_code = self.get_stdout_output("-p", "Madison, WI")
        expected = self._get_expected_output_for_p_flag(VALID_MADISON_WI_P_FLAG)
        self.validate_stdout(stdout, stderr, return_code, expected)

    def test_with_invalid_zip_code(self):
        stdout, stderr, return_code = self.get_stdout_output("-p", "00033")
        expected = self._get_expected_output_for_p_flag()
        self.validate_stdout(stdout, stderr, return_code, expected)

    def test_with_invalid_city_state(self):
        stdout, stderr, return_code = self.get_stdout_output("-p", "faketown, CA")
        expected = self._get_expected_output_for_p_flag()
        self.validate_stdout(stdout, stderr, return_code, expected)

    def test_valid_zip_code_with_invalid_city_state(self):
        stdout, stderr, return_code = self.get_stdout_output(
            "-p", "12345", "faketown, CA"
        )
        expected = self._get_expected_output_for_p_flag(VALID_12345_P_FLAG)
        self.validate_stdout(stdout, stderr, return_code, expected)

    def test_valid_city_state_with_invalid_zip_code(self):
        stdout, stderr, return_code = self.get_stdout_output(
            "-p", "00033", "Madison, WI"
        )
        expected = self._get_expected_output_for_p_flag(VALID_MADISON_WI_P_FLAG)
        self.validate_stdout(stdout, stderr, return_code, expected)

    def test_with_multiple_valid(self):
        stdout, stderr, return_code = self.get_stdout_output(
            "-p", "12345", "Madison, WI"
        )
        expected = self._get_expected_output_for_p_flag(
            VALID_12345_P_FLAG, VALID_MADISON_WI_P_FLAG
        )
        self.validate_stdout(stdout, stderr, return_code, expected)

    def test_with_many(self):
        stdout, stderr, return_code = self.get_stdout_output(
            "-p",
            "Madison WI",
            "12345",
            "Chicago, IL",
            "10001",
            "faketown",
            "not faketown, ca",
            "Los Angeles, ca",
            "00501",
            "00000",
            "0005012",
            "san juan, pr",
            "00901",
            "96913",
            "Hagatna, GU",
            "New York, NY",
        )
        self.validate_stdout(stdout, stderr, return_code, VALID_MULTIPLE_P_FLAG)

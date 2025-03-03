import unittest
import subprocess
import json
import os
from tests.values import geoloc_util_location, SKIPPED_MESSAGE


class BaseTestClass(unittest.TestCase):

    def setUp(self):
        self.api_key = os.getenv("GEOLOC_API_KEY")

    @staticmethod
    def get_stdout_output(*query):
        process = subprocess.Popen(
            ["python", geoloc_util_location, *query], stdout=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        return_code = process.returncode
        stdout = stdout.decode("utf-8")
        return stdout, stderr, return_code

    @staticmethod
    def _get_expected_output(search_term, result, ensure_ascii=False):
        json_string = json.dumps(
            [{"search_term": search_term, **result}],
            indent=4,
            ensure_ascii=ensure_ascii,
        )
        json_string += f"\n{SKIPPED_MESSAGE}\n"
        return json_string

    def validate_stdout(
        self,
        stdout,
        stderr,
        return_code,
        expected_stdout,
        convert_to_json=False,
        is_help_message=False,
    ):
        if convert_to_json:
            self.assertIn(SKIPPED_MESSAGE, stdout)
            stdout = stdout.replace(SKIPPED_MESSAGE, "")
            stdout = json.loads(stdout)
            expected_stdout = json.loads(expected_stdout)
        else:
            if is_help_message:
                expected_stdout += f"\n{SKIPPED_MESSAGE}\n"
        self.assertEqual(expected_stdout, stdout)
        self.assertIsNone(stderr)
        self.assertEqual(return_code, 0)

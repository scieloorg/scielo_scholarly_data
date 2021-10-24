import unittest

from scielo_scholarly_data.helpers import is_valid_issn


class TestHelpers(unittest.TestCase):

    def test_is_valid_issn(self):
        issns = {
            '2090-424X': True,
            '2090-4241': False,
            '2090-4242': False,
            '2090-4243': False,
            '2090-4244': False,
            '9777-2920': False,
            '9777-2921': False,
            '9777-2922': False,
            '9777-2923': False,
            '9777-2924': False,
            '9777-2925': True,
            '9777-2926': False,
            '9777-2927': False,
            '9777-2928': False,
            '9777-2929': False,
            '9777-292X': False,
        }

        expected_values = list(issns.values())
        obtained_values = [is_valid_issn(i) for i in issns]

        self.assertListEqual(expected_values, obtained_values)
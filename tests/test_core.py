from scielo_scholarly_data.core import (
    convert_to_iso_date,
    keep_alpha_num_space,
    remove_accents,
    remove_double_spaces,
    remove_non_printable_chars,
    remove_parenthesis,
    remove_end_punctuation_chars,
    remove_words,
    unescape,
    roman_to_int,
)

import unittest
from dateutil.parser import parse


class TestCore(unittest.TestCase):

    def test_keep_alpha_num_space(self):
        self.assertEqual(
            keep_alpha_num_space('This$ ° [is]+- a´ (sentence) that contains numbers 1, 2, 3'),
            'This     is    a   sentence  that contains numbers 1  2  3'
        )

        self.assertEqual(
            keep_alpha_num_space('This$ ° [is]+- a´ (sentence) that contains numbers 1, 2, 3', replace_with='?'),
            'This? ? ?is??? a? ?sentence? that contains numbers 1? 2? 3'
        )

        self.assertEqual(
            keep_alpha_num_space('This$ ° [is]+- a´ (sentence) that contains numbers 1, 2, 3', replace_with=''),
            'This  is a sentence that contains numbers 1 2 3'
        )

    def test_remove_accents(self):
        self.assertEqual(
            remove_accents('Esta é uma sentença'), 
            'Esta e uma sentenca'
        )

    def test_remove_double_spaces(self):
        self.assertEqual(
            remove_double_spaces('This is  a  sentence'), 
            'This is a sentence'
        )

    def test_remove_end_punctuation_chars(self):
        self.assertEqual(
            remove_end_punctuation_chars('Ciência e Mundo .'),
            'Ciência e Mundo'
        )

    def test_remove_non_printable_chars(self):
        for i in range(0, 32):
            self.assertEqual(
                remove_non_printable_chars('Hello world without non ' + chr(i) + 'printable chars'), 
                'Hello world without non printable chars'
            )

        self.assertEqual(
            remove_non_printable_chars('Hello world without non ' + chr(127) + 'printable chars'), 
            'Hello world without non printable chars'
        )

    def test_unescape(self):
        for i in [
            ('&gt;', '>'), 
            ('&#62;', '>'), 
            ('&#x3e;', '>')
        ]:
            self.assertEqual(
                unescape(i[0]), 
                i[1]
            )

    def test_remove_parenthesis(self):
        self.assertEqual(
            remove_parenthesis('This is a text with (parenthesis) to remove'),
            'This is a text with to remove'
        )

    def test_remove_words(self):
        self.assertEqual(
            remove_words('21 de setembro de 2021', words_to_remove=['de']),
            '21 setembro 2021'
        )

    def test_convert_to_iso_date_without_separators(self):
        self.assertEqual(
            str(convert_to_iso_date('20210921')),
            '2021-09-21'
        )

    def test_convert_to_iso_date_with_separators(self):
        test_date = '2021-09-21'
        dates = {
            '2021-09-21': test_date,
            '2021/09/21': test_date,
            '2021.09.21': test_date,
            '2021 09 21': test_date
        }
        expected_values = list(dates.values())
        obtained_values = [str(convert_to_iso_date(dt)) for dt in dates]

        self.assertListEqual(expected_values, obtained_values)

    def test_convert_to_iso_date_with_separators_different_orderings(self):
        test_date = '2021-09-21'
        dates = {
            '21-09-2021': test_date,
            '21/09/2021': test_date,
            '21.09.2021': test_date,
            '21 09 2021': test_date
        }
        expected_values = list(dates.values())
        obtained_values = [str(convert_to_iso_date(dt)) for dt in dates]

        self.assertListEqual(expected_values, obtained_values)

    def test_convert_to_iso_date_just_year_received(self):
        self.assertEqual(
            str(convert_to_iso_date('2021')),
            '2021-01-01'
        )

    def test_convert_to_iso_date_just_year_delivered(self):
        self.assertEqual(
            str(convert_to_iso_date('2021-06-15', only_year=True )),
            '2021'
        )

    def test_convert_to_iso_date_just_year_user_decision(self):
        self.assertEqual(
            str(convert_to_iso_date('2021', day='1', month='1')),
            '2021-01-01'
        )

    def test_convert_to_iso_date_invalid_month(self):
        self.assertEqual(
            convert_to_iso_date('2021-13-09'),
            None
        )

    def test_convert_to_iso_date_invalid_day(self):
        self.assertEqual(
            convert_to_iso_date('2021-12-35'),
            None
        )

    def test_convert_to_iso_date_invalid_date(self):
        self.assertEqual(
            convert_to_iso_date('2021-02-31'),
            None
        )

    def test_convert_to_iso_date_re_unmatch(self):
        self.assertEqual(
            convert_to_iso_date('abc-01-01'),
            None
        )

    def test_roman_to_int(self):
        nums = {
            'XX': 20,
            'MCMXXII': 1922,
            'MMXXII': 2022,
            'MDLIV': 1554,
        }
        expected_values = list(nums.values())
        obtained_values = [roman_to_int(ints) for ints in nums]

        self.assertListEqual(expected_values, obtained_values)

from scielo_scholarly_data.core import (
    convert_to_alpha_num_space,
    defaults_date_to_ISO_format,
    remove_accents,
    remove_double_spaces,
    remove_non_printable_chars,
    remove_parenthesis,
    unescape
)

import unittest
from dateutil.parser import parse


class TestCore(unittest.TestCase):

    def test_convert_to_alpha_num_space(self):
        self.assertEqual(
            convert_to_alpha_num_space('This$ ° [is]+- a´ (sentence) that contains numbers 1, 2, 3'), 
            'This     is    a   sentence  that contains numbers 1  2  3'
        )

        self.assertEqual(
            convert_to_alpha_num_space('This$ ° [is]+- a´ (sentence) that contains numbers 1, 2, 3', replace_with='?'),
            'This? ? ?is??? a? ?sentence? that contains numbers 1? 2? 3'
        )

        self.assertEqual(
            convert_to_alpha_num_space('This$ ° [is]+- a´ (sentence) that contains numbers 1, 2, 3', replace_with=''),
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

    def test_defaults_date_to_ISO_format_without_separators(self):
        self.assertEqual(
            defaults_date_to_ISO_format('20210921'),
            parse('2021-09-21').date()
        )

    def test_defaults_date_to_ISO_format_with_separators(self):
        test_date = parse('2021-09-21').date()
        dates = {
            '2021-09-21': test_date,
            '2021/09/21': test_date,
            '2021.09.21': test_date,
            '2021 09 21': test_date
        }
        expected_values = list(dates.values())
        obtained_values = [defaults_date_to_ISO_format(dt) for dt in dates]

        self.assertListEqual(expected_values, obtained_values)

    def test_defaults_date_to_ISO_format_with_separators_different_orderings(self):
        test_date = parse('2021-09-21').date()
        dates = {
            '21-09-2021': test_date,
            '21/09/2021': test_date,
            '21.09.2021': test_date,
            '21 09 2021': test_date
        }
        expected_values = list(dates.values())
        obtained_values = [defaults_date_to_ISO_format(dt) for dt in dates]

        self.assertListEqual(expected_values, obtained_values)

    def test_defaults_date_to_ISO_format_just_year_received(self):
        self.assertEqual(
            defaults_date_to_ISO_format('2021'),
            parse('2021-06-15').date()
        )

    def test_defaults_date_to_ISO_format_just_year_delivered(self):
        self.assertEqual(
            defaults_date_to_ISO_format('2021-06-15', just_year=True ),
            parse('2021').date().year
        )

    def test_defaults_date_to_ISO_format_just_year_user_decision(self):
        self.assertEqual(
            defaults_date_to_ISO_format('2021', day='1', month='1'),
            parse('2021-01-01').date()
        )

    def test_defaults_date_to_ISO_format_invalid_month(self):
        self.assertEqual(
            defaults_date_to_ISO_format('2021-13-09'),
            None
        )

    def test_defaults_date_to_ISO_format_invalid_day(self):
        self.assertEqual(
            defaults_date_to_ISO_format('2021-12-35'),
            None
        )

    def test_defaults_date_to_ISO_format_invalid_date(self):
        self.assertEqual(
            defaults_date_to_ISO_format('2021-02-31'),
            None
        )

    def test_defaults_date_to_ISO_format_invalid_char(self):
        self.assertEqual(
            defaults_date_to_ISO_format('20*21)10(19'),
            parse('2021-10-19').date()
        )

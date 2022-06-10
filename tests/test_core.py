from scielo_scholarly_data.core import (
    check_sum_orcid,
    keep_alpha_num_space,
    remove_accents,
    remove_double_spaces,
    remove_non_printable_chars,
    remove_parenthesis,
    remove_end_punctuation_chars,
    remove_chars,
    remove_words,
    unescape
)

from scielo_scholarly_data.dates import (
    convert_to_iso_date,
)

import unittest


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

    def test_remove_chars(self):
        self.assertEqual(
            remove_chars('This is a text with chars to remove', [' ']),
            'Thisisatextwithcharstoremove'
        )

    def test_remove_words(self):
        self.assertEqual(
            remove_words('21 de setembro de 2021', words_to_remove=['de']),
            '21 setembro 2021'
        )

    def test_check_sum_orcid(self):
        orcids = {
            '0000000925158361': True,
            '0000000955138362': False,
            '000000071302576X': True,
            '0000000157937897': False
        }
        expected_values = list(orcids.values())
        obtained_values = [check_sum_orcid(register) for register in orcids]

        self.assertListEqual(expected_values, obtained_values)

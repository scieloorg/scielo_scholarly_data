from scielo_scholarly_data.core import (
    convert_to_alpha_num_space,
    remove_accents,
    remove_double_spaces,
    remove_non_printable_chars,
    remove_parenthesis,
    unescape
)

import unittest


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

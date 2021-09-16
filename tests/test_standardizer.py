from scielo_scholarly_data.standardizer import (
    document_author,
    document_doi,
    journal_issn,
    journal_title,
    journal_number
)

import unittest


class TestStandardizer(unittest.TestCase):

    def test_journal_title(self):
        self.assertEqual(
            journal_title('Agrociencia (Uruguay)', keep_parenthesis_content=False), 
            'Agrociencia'
        )

        self.assertEqual(
            journal_title('Agrociencia (Uruguay)'), 
            'Agrociencia Uruguay'
        )

        self.assertEqual(
            journal_title('African Journal of Disability (Online)', keep_parenthesis_content=False),
            'African Journal of Disability'
            )

        self.assertEqual(
            journal_title('Anagramas -Rumbos y sentidos de la comunicación-'), 
            'Anagramas Rumbos y sentidos de la comunicacion'
        )

    def test_journal_issn_without_hyphen(self):
        issns = {
            '15856280': '1585-6280',
            '85856281': '8585-6281'
        }

        expected_values = list(issns.values())
        obtained_values = [journal_issn(i) for i in issns]

        self.assertListEqual(expected_values, obtained_values)

    def test_journal_issn_correct(self):
        issns = {
            '1585-6280': '1585-6280',
            '8585-6281': '8585-6281'
        }

        expected_values = list(issns.values())
        obtained_values = [journal_issn(i) for i in issns]

        self.assertListEqual(expected_values, obtained_values)

    def test_journal_issn_with_char(self):
        issns = {
            '1585x6280': None,
            '85856281a': None,
            '8585-62s81': None,
            'x8585-6281': None,
            '85X856281': None
        }

        expected_values = list(issns.values())
        obtained_values = [journal_issn(i) for i in issns]

        self.assertListEqual(expected_values, obtained_values)

    def test_journal_issn_with_space(self):
        issns = {
            '1585 6280': None,
            '85856281 ': None,
            ' 8585-6281': None,
            '85 85-6281': None,
            '8585 6281 ': None
        }

        expected_values = list(issns.values())
        obtained_values = [journal_issn(i) for i in issns]

        self.assertListEqual(expected_values, obtained_values)

    def test_journal_issn_with_less_or_more_positions(self):
        issns = {
            '185-6280': None,
            '8585-281': None,
            '8585-628': None,
            '8685-62833': None,
            '85835-6282': None,
            '808-63286': None
        }

        expected_values = list(issns.values())
        obtained_values = [journal_issn(i) for i in issns]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_doi(self):
        dois = {
            'https://10.1016/J.SCITOTENV.2019.02.108': '10.1016/J.SCITOTENV.2019.02.108',
            'http://10.1007/S13157-019-01161-Y': '10.1007/S13157-019-01161-Y',
            '10.4257/OECO.2020.2401.05': '10.4257/OECO.2020.2401.05',
            'ftp://10.1111/EFF.12536': '10.1111/EFF.12536',
            'axc; 10.1007/S10452-020-09782-W': '10.1007/S10452-020-09782-W',
            '&referrer=google*url=10.1590/1678-4766E2016006': '10.1590/1678-4766E2016006',
        }

        expected_values = list(dois.values())
        obtained_values = [document_doi(d) for d in dois]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_author(self):
        authors = {
            'Silva, Joao  J. P.. &': 'Silva Joao J P',
            'Santos;=;] R': 'Santos R',
            'Joao...Paulo': 'Joao Paulo',
            '3ø Elton Jonas': 'Elton Jonas',
            'Elvis-Presley': 'Elvis Presley'
        }

        expected_values = list(authors.values())
        obtained_values = [document_author(da) for da in authors]

        self.assertListEqual(expected_values, obtained_values)

    def test_journal_number(self):
        original_journal_number = "(32d)"
        expected_journal_number = "32d"
        obtained_journal_number = journal_number(original_journal_number)
        self.assertEqual(expected_journal_number, obtained_journal_number)

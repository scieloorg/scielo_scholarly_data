from scielo_scholarly_data.standardizer import document_author, document_doi, journal_issn, journal_title

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

    def test_journal_issn(self):
        issns = {
            '15856280': '1585-6280',
            '8585-6281': '8585-6281',
            '8585x6282': None,
            '8685-6283a': None,
            '85856282': '8585-6282',
            '  8085-6285': None,
            '8-85-6286': None,
            '85856287': '8585-6287',
            '8x85-6288': None,
            '8m85-6289': None,
            '858628X': None
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

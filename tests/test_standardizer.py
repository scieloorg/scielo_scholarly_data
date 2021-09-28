from scielo_scholarly_data.standardizer import (
    document_author,
    document_doi,
    document_title,
    journal_issn,
    journal_title,
    journal_title_for_deduplication,
    issue_number
)

import unittest


class TestStandardizer(unittest.TestCase):

    def test_journal_title_for_deduplication_html_code_to_unicode(self):
        self.assertEqual(
            journal_title_for_deduplication('Agrociencia &amp; (Uruguay)'),
            'agrociencia & uruguay'
        )


    def test_journal_title_for_deduplication_remove_nonprintable_char(self):
        self.assertEqual(
            journal_title_for_deduplication('Agrociencia (Uruguay)\n'),
            'agrociencia uruguay'
        )

    def test_journal_title_for_deduplication_remove_parentheses_and_content(self):
        self.assertEqual(
            journal_title_for_deduplication('Agrociencia (Uruguay)', keep_parenthesis_content=False),
            'agrociencia'
        )

    def test_journal_title_for_deduplication_remove_accentuation(self):
        self.assertEqual(
            journal_title_for_deduplication('Agrociência (Uruguay)'),
            'agrociencia uruguay'
        )

    def test_journal_title_for_deduplication_convert_to_alphanumeric_char(self):
        self.assertEqual(
            journal_title_for_deduplication('Agrociencia + (Uruguay)'),
            'agrociencia uruguay'
        )

    def test_journal_title_for_deduplication_remove_double_space(self):
        self.assertEqual(
            journal_title_for_deduplication('Agrociencia    (Uruguay)'),
            'agrociencia uruguay'
        )

    def test_journal_title_for_deduplication_remove_special_words(self):
        self.assertEqual(
            journal_title_for_deduplication('Agrociencia (Uruguay) online'),
            'agrociencia uruguay'
        )

    def test_journal_title_for_deduplication_to_lowercase_char(self):
        self.assertEqual(
            journal_title_for_deduplication('Agrociencia (URUGUAY)'),
            'agrociencia uruguay'
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

    def test_issue_number_special_char(self):
        issues = {
            '&96':'96',
            '$96':'96',
            '@96a':'96a',
            '!96a':'96a'
        }
        expected_values = list(issues.values())
        obtained_values = [issue_number(num) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_number_non_printable(self):
        issues = {
            '\n96':'96',
            '96\t':'96',
            '96\aa':'96a',
            '9\n6a':'96a'
        }
        expected_values = list(issues.values())
        obtained_values = [issue_number(num) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_number_with_spaces(self):
        issues = {
            '96':'96',
            '96  ':'96',
            '96a ':'96a',
            ' 96 a':'96a'
        }
        expected_values = list(issues.values())
        obtained_values = [issue_number(num) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_number_with_parenthesis(self):
        issues = {
            '(96)':'96',
            '9(6)':'96',
            '96(a)':'96a',
            '(96)a':'96a'
        }
        expected_values = list(issues.values())
        obtained_values = [issue_number(num) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_title_references(self):
        titles = {
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE &#38; PROBLEMÁTICAS':
                'INNOVACION TECNOLOGICA EN LA RESOLUCION DE PROBLEMATICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE &#338; PROBLEMÁTICAS':
                'INNOVACION TECNOLOGICA EN LA RESOLUCION DE PROBLEMATICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE &#x2030; PROBLEMÁTICAS':
                'INNOVACION TECNOLOGICA EN LA RESOLUCION DE PROBLEMATICAS'
        }
        expected_values = list(titles.values())
        obtained_values = [document_title(dt) for dt in titles]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_title_non_printable(self):
        titles = {
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE \n PROBLEMÁTICAS':
                'INNOVACION TECNOLOGICA EN LA RESOLUCION DE PROBLEMATICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE \t PROBLEMÁTICAS':
                'INNOVACION TECNOLOGICA EN LA RESOLUCION DE PROBLEMATICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE \a PROBLEMÁTICAS':
                'INNOVACION TECNOLOGICA EN LA RESOLUCION DE PROBLEMATICAS'
        }
        expected_values = list(titles.values())
        obtained_values = [document_title(dt) for dt in titles]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_title_accents(self):
        titles = {
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÊ PROBLEMÁTICAS':
                'INNOVACION TECNOLOGICA EN LA RESOLUCION DE PROBLEMATICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DẼ PROBLEMÁTICAS':
                'INNOVACION TECNOLOGICA EN LA RESOLUCION DE PROBLEMATICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÈ PROBLEMÁTICAS':
                'INNOVACION TECNOLOGICA EN LA RESOLUCION DE PROBLEMATICAS'
        }
        expected_values = list(titles.values())
        obtained_values = [document_title(dt) for dt in titles]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_title_alpha_num_spaces(self):
        titles = {
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÊ: PROBLEMÁTICAS':
                'INNOVACION TECNOLOGICA EN LA RESOLUCION DE PROBLEMATICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DẼ* PROBLEMÁTICAS':
                'INNOVACION TECNOLOGICA EN LA RESOLUCION DE PROBLEMATICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÈ& PROBLEMÁTICAS':
                'INNOVACION TECNOLOGICA EN LA RESOLUCION DE PROBLEMATICAS'
        }
        expected_values = list(titles.values())
        obtained_values = [document_title(dt) for dt in titles]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_title_double_spaces(self):
        titles = {
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÊ  PROBLEMÁTICAS':
                'INNOVACION TECNOLOGICA EN LA RESOLUCION DE PROBLEMATICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DẼ   PROBLEMÁTICAS':
                'INNOVACION TECNOLOGICA EN LA RESOLUCION DE PROBLEMATICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÈ    PROBLEMÁTICAS':
                'INNOVACION TECNOLOGICA EN LA RESOLUCION DE PROBLEMATICAS'
        }
        expected_values = list(titles.values())
        obtained_values = [document_title(dt) for dt in titles]

        self.assertListEqual(expected_values, obtained_values)

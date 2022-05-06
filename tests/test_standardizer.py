from scielo_scholarly_data.standardizer import (
    document_author_for_visualization,
    document_author_for_deduplication,
    document_doi,
    document_elocation,
    document_first_page,
    document_publication_date,
    document_last_page,
    document_title_for_deduplication,
    document_title_for_visualization,
    journal_issn,
    journal_title_for_deduplication,
    journal_title_for_visualization,
    issue_number,
    issue_volume
)

import unittest
from dateutil.parser import parse


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

    def test_journal_title_for_visualization_html_code_to_unicode(self):
        self.assertEqual(
            journal_title_for_visualization('Agrociencia &amp; (Uruguay)'),
            'Agrociencia & (Uruguay)'
        )

    def test_journal_title_for_visualization_remove_nonprintable_char(self):
        self.assertEqual(
            journal_title_for_visualization('Agrociencia (Uruguay)\n'),
            'Agrociencia (Uruguay)'
        )

    def test_journal_title_for_visualization_remove_double_space(self):
        self.assertEqual(
            journal_title_for_visualization('Agrociencia    (Uruguay)'),
            'Agrociencia (Uruguay)'
        )

    def test_journal_title_for_visualization_remove_pointing_at_end(self):
        self.assertEqual(
            journal_title_for_visualization('Agrociencia (Uruguay).,;'),
            'Agrociencia (Uruguay)'
        )

    def test_journal_issn_without_hyphen(self):
        issns = {
            '15856280': '1585-6280',
            '85856281': '8585-6281',
            '1387666X': '1387-666X',
        }

        expected_values = list(issns.values())
        obtained_values = [journal_issn(i) for i in issns]

        self.assertListEqual(expected_values, obtained_values)

    def test_journal_issn_validator_true_correct_issn(self):
        correct_issn_upper_case_x = '1387-666X'
        self.assertEqual(journal_issn(correct_issn_upper_case_x, use_issn_validator=True), '1387-666X')

        correct_issn_lower_case_x = '1387-666x'
        self.assertEqual(journal_issn(correct_issn_lower_case_x, use_issn_validator=True), '1387-666X')

        correct_issn_lower_case_x_no_hyphen = '1387666x'
        self.assertEqual(journal_issn(correct_issn_lower_case_x_no_hyphen, use_issn_validator=True), '1387-666X')

    def test_journal_issn_validator_true_wrong_issn(self):
        wrong_issns = ['1585-6280', '15856280', '15856281', '8585-6281', '1387-6660']
        obtained_values = [journal_issn(i, use_issn_validator=True) for i in wrong_issns]

        self.assertListEqual([None for x in range(len(wrong_issns))], obtained_values)

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

    def test_document_author_for_visualization_alpha_space_surname_first(self):
        names = {
            'Silva, João & J* P': 'Silva, João J P',
            'João & J* P Silva': 'Silva, João J P'
        }
        expected_values = list(names.values())
        obtained_values = [document_author_for_visualization(name) for name in names]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_author_for_visualization_alpha_space_surname_last(self):
        names = {
            'Silva, João & J* P': 'João J P Silva',
            'João & J* P Silva': 'João J P Silva'
        }
        expected_values = list(names.values())
        obtained_values = [document_author_for_visualization(name, surname_first=False) for name in names]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_author_for_visualization_double_space_surname_first(self):
        names = {
            'Silva, João  J  P': 'Silva, João J P',
            'João  J  P Silva': 'Silva, João J P'
        }
        expected_values = list(names.values())
        obtained_values = [document_author_for_visualization(name) for name in names]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_author_for_visualization_double_space_surname_last(self):
        names = {
            'Silva, João  J  P': 'João J P Silva',
            'João  J  P Silva': 'João J P Silva'
        }
        expected_values = list(names.values())
        obtained_values = [document_author_for_visualization(name, surname_first=False) for name in names]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_author_for_visualization_single_name_author(self):
        names = {
            'João': 'João',
            ',João': 'João',
            'João,': 'João'
        }
        expected_values = list(names.values())
        obtained_values = [document_author_for_visualization(name) for name in names]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_author_for_deduplication_remove_accents_surname_first(self):
        names = {
            'Sílva, João  J  P': 'silva, joao j p',
            'João  J  P Silva': 'silva, joao j p'
        }
        expected_values = list(names.values())
        obtained_values = [document_author_for_deduplication(name) for name in names]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_author_for_deduplication_lower_case_surname_last(self):
        names = {
            'Silva, João  J  P': 'joao j p silva',
            'João  J  P Silva': 'joao j p silva'
        }
        expected_values = list(names.values())
        obtained_values = [document_author_for_deduplication(name, surname_first=False) for name in names]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_author_for_deduplication_single_name_author(self):
        names = {
            'João': 'joao',
            ',João': 'joao',
            'João,': 'joao'
        }
        expected_values = list(names.values())
        obtained_values = [document_author_for_deduplication(name) for name in names]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_elocation_non_printable_chars(self):
        self.assertEqual(
            document_elocation('e\n277\t21'),
            'e27721'
        )

    def test_document_elocation_alpha_num_space(self):
        self.assertEqual(
            document_elocation('e*277$2%1@'),
            'e27721'
        )

    def test_document_elocation_double_spaces(self):
        self.assertEqual(
            document_elocation('e  27721  '),
            'e27721'
        )

    def test_document_elocation_end_punctuation_chars(self):
        self.assertEqual(
            document_elocation('e27721.,; '),
            'e27721'
        )

    def test_document_first_page_unescape(self):
        self.assertEqual(
            document_first_page('12&#60;8'),
            '128'
        )

    def test_document_first_page_non_printable_chars(self):
        self.assertEqual(
            document_first_page('12\n8'),
            '128'
        )

    def test_document_first_page_alpha_num_space(self):
        self.assertEqual(
            document_first_page('12&8'),
            '128'
        )

    def test_document_first_page_double_spaces(self):
        self.assertEqual(
            document_first_page('  12  8'),
            '128'
        )

    def test_document_first_page_end_punctuation_chars(self):
        self.assertEqual(
            document_first_page('128.,; .'),
            '128'
        )

    def test_document_first_page_re_unmatch(self):
        self.assertEqual(
            document_first_page('abc-128'),
            None
        )

    def test_document_publication_date_non_printable_char(self):
        test_date = '2021-09-21'
        dates = {
            '2021-\t09-21': test_date,
            '2021/\n09/21': test_date,
            '2021.setembro\n.21': test_date,
            '21setembro2021\n': test_date,
            '21 de set de 2021\n': test_date,
            '21 of sept 2021\n': test_date
        }
        expected_values = list(dates.values())
        obtained_values = [str(document_publication_date(dt)) for dt in dates]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_publication_date_special_chars(self):
        test_date = '2021-09-21'
        dates = {
            '2021-09-&21': test_date,
            '2021/%09/21': test_date,
            '2021.setembro#.21': test_date,
            '21 de setembro de 2021()': test_date
        }
        expected_values = list(dates.values())
        obtained_values = [str(document_publication_date(dt)) for dt in dates]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_publication_date_double_spaces(self):
        test_date = '2021-09-21'
        dates = {
            '2021-09-  21': test_date,
            '2021/  09/21': test_date,
            '2021.setembro  .21': test_date,
            '2021setembro21  ': test_date
        }
        expected_values = list(dates.values())
        obtained_values = [str(document_publication_date(dt)) for dt in dates]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_publication_date_special_date_formats(self):
        test_date = '2021-09-21'
        dates = {
            '20210921': test_date,
            '2021/09/21': test_date,
            '2021.setembro.21': test_date,
            '2021set21': test_date,
            '2021september21': test_date,
            '2021septiembre21': test_date
        }
        expected_values = list(dates.values())
        obtained_values = [str(document_publication_date(dt)) for dt in dates]
        self.assertListEqual(expected_values, obtained_values)

    def test_document_publication_date_complete_format(self):
        test_date = '2021-09-21'
        dates = {
            '2021-09-21T21:31:00Z': test_date,
            ' 2021-09-21T21:31:00Z ': test_date,
            '2021 09 21T21:31:00Z': test_date,
            '2021/09/21T21:31:00Z': test_date,
            '/2021-09-21T21:31:00Z': test_date,
            '2021.09.21T21:31:00Z': test_date
        }
        expected_values = list(dates.values())
        obtained_values = [str(document_publication_date(dt)) for dt in dates]
        self.assertListEqual(expected_values, obtained_values)

    def test_document_publication_date_just_year(self):
        test_date = parse('2021').date().year
        dates = {
            '20210921': test_date,
            '2021/09/21': test_date,
            '2021.setembro.21': test_date,
            '2021set21': test_date,
            '2021september21': test_date,
            '2021septiembre21': test_date
        }
        expected_values = list(dates.values())
        obtained_values = [document_publication_date(dt, only_year=True) for dt in dates]
        self.assertListEqual(expected_values, obtained_values)

    def test_document_publication_date_just_year_received(self):
        test_date = parse('2021-06-15').date()
        dates = {
            '2021': test_date,
            '2021 ': test_date,
            ' 2021': test_date
        }
        expected_values = list(dates.values())
        obtained_values = [document_publication_date(dt, day='15', month='06') for dt in dates]
        self.assertListEqual(expected_values, obtained_values)

    def test_document_last_page_unescape(self):
        self.assertEqual(
            document_last_page('12&#38;8'),
            '128'
        )

    def test_document_last_page_non_printable_chars(self):
        self.assertEqual(
            document_last_page('12\n8'),
            '128'
        )

    def test_document_last_page_alpha_num_space(self):
        self.assertEqual(
            document_last_page('12&8'),
            '128'
        )

    def test_document_last_page_double_spaces(self):
        self.assertEqual(
            document_last_page('  12  8'),
            '128'
        )

    def test_document_last_page_end_punctuation_chars(self):
        self.assertEqual(
            document_last_page('128.,; .'),
            '128'
        )

    def test_document_last_page_range(self):
        range = {
            '128-140':'140',
            '128_140':'140',
            '128:140':'140',
            '128;140':'140',
            '128,140':'140',
            '128.140':'140',
            '128-30':'158'
        }
        expected_values = list(range.values())
        obtained_values = [document_last_page(page) for page in range]
        
        self.assertListEqual(expected_values, obtained_values)

    def test_document_last_page_re_unmatch(self):
        self.assertEqual(
            document_last_page('abc-128'),
            None
        )

    def test_document_first_page_range(self):
        range = {
            '128-140': '128',
            '128_140': '128',
            '128:140': '128',
            '128;140': '128',
            '128,140': '128',
            '128.140': '128'
        }
        expected_values = list(range.values())
        obtained_values = [document_first_page(page) for page in range]

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
            ' 96':'96',
            '96  ':'96',
            '96 a ':'96 a',
            ' 96 a':'96 a'
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

    def test_issue_volume_special_char(self):
        issues = {
            '&96':'96',
            '$96':'96',
            '@96a':'96a',
            '!96a':'96a'
        }
        expected_values = list(issues.values())
        obtained_values = [issue_volume(num, force_integer=False) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_volume_non_printable(self):
        issues = {
            '\n96':'96',
            '96\t':'96',
            '96\aa':'96a',
            '9\n6a':'96a'
        }
        expected_values = list(issues.values())
        obtained_values = [issue_volume(num, force_integer=False) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_volume_with_spaces(self):
        issues = {
            ' 96':'96',
            '96  ':'96',
            '96 a ':'96 a',
            ' 96 a':'96 a'
        }
        expected_values = list(issues.values())
        obtained_values = [issue_volume(num, force_integer=False) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_volume_with_parenthesis(self):
        issues = {
            '(96)':'96',
            '9(6)':'96',
            '96(a)':'96a',
            '(96)a':'96a'
        }
        expected_values = list(issues.values())
        obtained_values = [issue_volume(num, force_integer=False) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_volume_remove_points_at_end(self):
        issues = {
            '(96).':'96',
            '9(6);':'96',
            '96(a),':'96a',
            '(96)a .':'96a'
        }
        expected_values = list(issues.values())
        obtained_values = [issue_volume(num, force_integer=False) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_volume_with_alpha_chars(self):
        issues = {
            'v. 12': '12',
            'vol.: 12': '12',
            '12 v.': '12',
            'Volume  12': '12',
        }
        expected_values = list(issues.values())
        obtained_values = [issue_volume(num) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_volume_with_romans(self):
        issues = {
            'vol.: V': 'vol 5',
            'vol.: XXc': 'vol 20c',
            'XII v.': '12 v',
            'volume  XIIv': 'volume 12v',
        }
        expected_values = list(issues.values())
        obtained_values = [issue_volume(num, force_integer=False, convert_romans=True) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_title_for_deduplication_html_entities_keeps(self):
        self.assertEqual(
            document_title_for_deduplication('INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE &#60; PROBLEMÁTICAS', remove_special_char=False),
            'innovacion tecnologica en la resolucion de < problematicas'
        )

    def test_document_title_for_deduplication_keep_alpha_num_space(self):
        self.assertEqual(
            document_title_for_deduplication('INNOVACIÓN & TECNOLÓGICA EN LA RESOLUCIÓN DE &#60; PROBLEMÁTICAS'),
            'innovacion tecnologica en la resolucion de problematicas'
        )

    def test_document_title_for_deduplication_remove_non_printable_chars(self):
        self.assertEqual(
            document_title_for_deduplication('INNOVACIÓN \n TECNOLÓGICA EN LA RESOLUCIÓN DE \t PROBLEMÁTICAS'),
            'innovacion tecnologica en la resolucion de problematicas'
        )

    def test_document_title_for_deduplication_remove_double_spaces(self):
        self.assertEqual(
            document_title_for_deduplication('  INNOVACIÓN  TECNOLÓGICA  EN  LA  RESOLUCIÓN  DE  PROBLEMÁTICAS  '),
            'innovacion tecnologica en la resolucion de problematicas'
        )

    def test_document_title_for_deduplication_remove_end_punctuation_chars(self):
        self.assertEqual(
            document_title_for_deduplication('INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE PROBLEMÁTICAS,.;'),
            'innovacion tecnologica en la resolucion de problematicas'
        )

    def test_document_title_for_deduplication_text_strip(self):
        self.assertEqual(
            document_title_for_deduplication(' INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE PROBLEMÁTICAS '),
            'innovacion tecnologica en la resolucion de problematicas'
        )

    def test_document_title_for_deduplication_remove_accents(self):
        self.assertEqual(
            document_title_for_deduplication('INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE PROBLEMÁTICAS'),
            'innovacion tecnologica en la resolucion de problematicas'
        )

    def test_document_title_for_deduplication_text_lower(self):
        self.assertEqual(
            document_title_for_deduplication('INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE PROBLEMÁTICAS'),
            'innovacion tecnologica en la resolucion de problematicas'
        )

    def test_document_title_for_visualization_html_entities_keeps(self):
        titles = {
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE &#60; PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE < PROBLEMÁTICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE &#163; PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE £ PROBLEMÁTICAS'
        }
        expected_values = list(titles.values())
        obtained_values = [document_title_for_visualization(dt, remove_special_char=False) for dt in titles]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_title_for_visualization_non_printable(self):
        titles = {
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE \n PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE PROBLEMÁTICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE \t PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE PROBLEMÁTICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE \a PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE PROBLEMÁTICAS'
        }
        expected_values = list(titles.values())
        obtained_values = [document_title_for_visualization(dt) for dt in titles]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_title_for_visualization_alpha_num_spaces(self):
        titles = {
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÊ: PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÊ PROBLEMÁTICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DẼ* PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DẼ PROBLEMÁTICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÈ& PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÈ PROBLEMÁTICAS'
        }
        expected_values = list(titles.values())
        obtained_values = [document_title_for_visualization(dt) for dt in titles]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_title_for_visualization_double_spaces(self):
        titles = {
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÊ  PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÊ PROBLEMÁTICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DẼ   PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DẼ PROBLEMÁTICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÈ    PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÈ PROBLEMÁTICAS'
        }
        expected_values = list(titles.values())
        obtained_values = [document_title_for_visualization(dt) for dt in titles]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_title_for_visualization_remove_pointing_at_end(self):
        titles = {
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÊ PROBLEMÁTICAS..':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÊ PROBLEMÁTICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DẼ PROBLEMÁTICAS.,;':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DẼ PROBLEMÁTICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÈ PROBLEMÁTICAS,,,,':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÈ PROBLEMÁTICAS'
        }
        expected_values = list(titles.values())
        obtained_values = [document_title_for_visualization(dt) for dt in titles]

        self.assertListEqual(expected_values, obtained_values)

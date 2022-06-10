from scielo_scholarly_data.standardizer import (
    book_editor_name_for_visualization,
    book_editor_name_for_deduplication,
    book_title_for_deduplication,
    book_title_for_visualization,
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
    issue_volume,
    InvalidRomanNumeralError,
    orcid_validator,
    ImpossibleConvertionToIntError,
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

    def test_journal_title_for_deduplication_remove_specific_chars(self):
        self.assertEqual(
            journal_title_for_deduplication('Agrociencia (URUGUAY)', chars_to_remove=[' ']),
            'agrocienciauruguay'
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

    def test_document_doi_return_mode_path(self):
        dois = {
            'https://10.1016/J.SCITOTENV.2019.02.108': '10.1016/J.SCITOTENV.2019.02.108',
            'http://10.1007/S13157-019-01161-Y': '10.1007/S13157-019-01161-Y',
            '10.4257/OECO.2020.2401.05': '10.4257/OECO.2020.2401.05',
            'ftp://10.1111/EFF.12536': '10.1111/EFF.12536',
            'axc; 10.1007/S10452-020-09782-W': '10.1007/S10452-020-09782-W',
            '&referrer=google*url=10.1590/1678-4766E2016006': '10.1590/1678-4766E2016006',
        }

        expected_values = list(dois.values())
        obtained_values = [document_doi(d, return_mode='path') for d in dois]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_doi_return_mode_uri(self):
        dois = {
            'https://10.1016/J.SCITOTENV.2019.02.108': 'http://doi.org/10.1016/J.SCITOTENV.2019.02.108',
            'http://10.1007/S13157-019-01161-Y': 'http://doi.org/10.1007/S13157-019-01161-Y',
            '10.4257/OECO.2020.2401.05': 'http://doi.org/10.4257/OECO.2020.2401.05',
            'ftp://10.1111/EFF.12536': 'http://doi.org/10.1111/EFF.12536',
            'axc; 10.1007/S10452-020-09782-W': 'http://doi.org/10.1007/S10452-020-09782-W',
            '&referrer=google*url=10.1590/1678-4766E2016006': 'http://doi.org/10.1590/1678-4766E2016006',
        }

        expected_values = list(dois.values())
        obtained_values = [document_doi(d, return_mode='uri') for d in dois]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_doi_return_mode_host(self):
        dois = {
            'https://10.1016/J.SCITOTENV.2019.02.108': 'doi.org',
            'http://10.1007/S13157-019-01161-Y': 'doi.org',
            '10.4257/OECO.2020.2401.05': 'doi.org',
            'ftp://10.1111/EFF.12536': 'doi.org',
            'axc; 10.1007/S10452-020-09782-W': 'doi.org',
            '&referrer=google*url=10.1590/1678-4766E2016006': 'doi.org',
        }

        expected_values = list(dois.values())
        obtained_values = [document_doi(d, return_mode='host') for d in dois]

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

    def test_document_author_for_deduplication_remove_specific_chars(self):
        names = {
            'Silva, João  J  P': 'joaojpsilva',
            'João  J  P Silva': 'joaojpsilva'
        }
        expected_values = list(names.values())
        obtained_values = [document_author_for_deduplication(name, surname_first=False, chars_to_remove=[' ']) for name in names]

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
            '9(6)':'9 6',
            '96(a)':'96 a',
            '(96)a':'96 a'
        }
        expected_values = list(issues.values())
        obtained_values = [issue_volume(num, force_integer=False) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_volume_remove_points_at_end(self):
        issues = {
            '(96).':'96',
            '9(6);':'9 6',
            '96(a),':'96 a',
            '(96)a .':'96 a'
        }
        expected_values = list(issues.values())
        obtained_values = [issue_volume(num, force_integer=False) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_volume_with_alpha_chars(self):
        issues = {
            '& Cognition, 34': '34',
            '&#8239;v.50': '50',
            '( Suppl)78': '78',
            '(1-2)': '1',
            '(11)suppl.16': '11',
            '(2)8(4)1875[1876]': '2',
            ', 13(1)': '13',
            ', Campinas, 13': '13',
        }
        expected_values = list(issues.values())
        obtained_values = [issue_volume(num) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_volume_with_romans(self):
        issues = {
            'vol.: V': '5',
            'XII v.': '12',
            'volume  XII v': '12',
            ', II, III, IV e IV': '2',
            '122(16 Suppl 2)': '122',
            'Basel), 39': '39',
            'C 42C 42': '42',
            'CXXVIII-CXXIX': '128',
            'Coleção Ehila v. 34': '34',
        }
        expected_values = list(issues.values())
        obtained_values = [issue_volume(num) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_volume_with_romans_return_error(self):
        self.assertRaises(
            InvalidRomanNumeralError,
            issue_volume, 'vol.: XXc'
        )

    def test_issue_volume_impossible_convertion_error(self):
        self.assertRaises(
            ImpossibleConvertionToIntError,
            issue_volume, '&#8226;&#8226;&#8226;'
        )

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

    def test_document_title_for_deduplication_remove_specific_chars(self):
        self.assertEqual(
            document_title_for_deduplication('INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE PROBLEMÁTICAS',
                                             chars_to_remove=[' ']),
            'innovaciontecnologicaenlaresoluciondeproblematicas'
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

    def test_orcid_validator_return_uri(self):
        orcids = {
            'https://orcid.org/0000-0002-1825-0097' : 'https://orcid.org/0000-0002-1825-0097',
            '0000-0001-5109-3700' : 'https://orcid.org/0000-0001-5109-3700',
            'orcid.org/0000-0002-1694-233X' : 'https://orcid.org/0000-0002-1694-233X'
        }
        expected_values = list(orcids.values())
        obtained_values = [orcid_validator(register) for register in orcids]

        self.assertListEqual(expected_values, obtained_values)

    def test_orcid_validator_return_hostname(self):
        orcids = {
            'https://orcid.org/0000-0002-1825-0097' : 'orcid.org',
            '0000-0001-5109-3701' : {'error' : 'invalid checksum'},
            'orcid.org/0000-0002-1694-2339' : {'error' : 'invalid checksum'},
            'orcid.org/000-0002-1825-0097' : {'error' : 'invalid format'}
        }
        expected_values = list(orcids.values())
        obtained_values = [orcid_validator(register, return_mode='host') for register in orcids]

        self.assertListEqual(expected_values, obtained_values)

    def test_orcid_validator_return_path(self):
        orcids = {
            'https://orcid.org/0000-0002-1825-0097' : '0000-0002-1825-0097',
            '0000-0001-5109-3701' : {'error' : 'invalid checksum'},
            'orcid.org/0000-0002-1694-233X' : '0000-0002-1694-233X'
        }
        expected_values = list(orcids.values())
        obtained_values = [orcid_validator(register, return_mode='path') for register in orcids]

        self.assertListEqual(expected_values, obtained_values)

    def test_book_editor_name_for_deduplication_html_entities_keeps(self):
        self.assertEqual(
            book_editor_name_for_deduplication('Editora da Universidade Estadual &#60; de São Paulo', keep_alpha_num_space_only=False),
            'editora da universidade estadual < de sao paulo'
        )

    def test_book_editor_name_for_deduplication_keep_alpha_num_space(self):
        self.assertEqual(
            book_editor_name_for_deduplication('Editora da Universidade Estadual &#60; de São Paulo'),
            'editora da universidade estadual de sao paulo'
        )

    def test_book_editor_name_for_deduplication_remove_non_printable_chars(self):
        self.assertEqual(
            book_editor_name_for_deduplication('Editora da \n Universidade Estadual \t de São Paulo'),
            'editora da universidade estadual de sao paulo'
        )

    def test_book_editor_name_for_deduplication_remove_double_spaces(self):
        self.assertEqual(
            book_editor_name_for_deduplication('  Editora  da   Universidade Estadual   de  São  Paulo'),
            'editora da universidade estadual de sao paulo'
        )

    def test_book_editor_name_for_deduplication_remove_end_punctuation_chars(self):
        self.assertEqual(
            book_editor_name_for_deduplication('Editora da Universidade Estadual de São Paulo,.;'),
            'editora da universidade estadual de sao paulo'
        )

    def test_book_editor_name_for_deduplication_text_strip(self):
        self.assertEqual(
            book_editor_name_for_deduplication(' Editora da Universidade Estadual de São Paulo '),
            'editora da universidade estadual de sao paulo'
        )

    def test_book_editor_name_for_deduplication_remove_accents(self):
        self.assertEqual(
            book_editor_name_for_deduplication('Editora da Universidade Estadual de São Paulo'),
            'editora da universidade estadual de sao paulo'
        )

    def test_book_editor_name_for_deduplication_text_lower(self):
        self.assertEqual(
            book_editor_name_for_deduplication('Editora da Universidade Estadual de São Paulo'),
            'editora da universidade estadual de sao paulo'
        )

    def test_book_editor_name_for_visualization_html_entities_keeps(self):
        self.assertEqual(
            book_editor_name_for_visualization('Editora da Universidade Estadual &#60; de São Paulo', keep_alpha_num_space_only=False),
            'Editora da Universidade Estadual < de São Paulo'
        )

    def test_book_editor_name_for_visualization_non_printable(self):
        self.assertEqual(
            book_editor_name_for_visualization('Editora da Universidade Estadual \n de São Paulo'),
            'Editora da Universidade Estadual de São Paulo'
        )

    def test_book_editor_name_for_visualization_alpha_num_spaces(self):
        self.assertEqual(
            book_editor_name_for_visualization('Editora da $ Universidade % Estadual * de São Paulo'),
            'Editora da Universidade Estadual de São Paulo'
        )

    def test_book_editor_name_for_visualization_double_spaces(self):
        self.assertEqual(
            book_editor_name_for_visualization(' Editora  da  Universidade   Estadual  de  São  Paulo '),
            'Editora da Universidade Estadual de São Paulo'
        )

    def test_book_editor_name_for_visualization_remove_pointing_at_end(self):
        self.assertEqual(
            book_editor_name_for_visualization('Editora da Universidade Estadual de São Paulo.,;.;'),
            'Editora da Universidade Estadual de São Paulo'
        )

    def test_book_title_for_deduplication_html_entities_keeps(self):
        self.assertEqual(
            book_title_for_deduplication(
                'O MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI: &#60; APORTES PARA O DEBATE',
            keep_alpha_num_space_chars_only=False),
            'o modelo de desenvolvimento brasileiro das primeiras decadas do seculo xxi: < aportes para o debate'
        )

    def test_book_title_for_deduplication_keep_alpha_num_space(self):
        self.assertEqual(
            book_title_for_deduplication(
                'O MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI: &#60; APORTES PARA O DEBATE'),
            'o modelo de desenvolvimento brasileiro das primeiras decadas do seculo xxi aportes para o debate'
        )

    def test_book_title_for_deduplication_remove_non_printable_chars(self):
        self.assertEqual(
            book_title_for_deduplication(
                '\tO MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI:\n APORTES PARA O DEBATE'),
            'o modelo de desenvolvimento brasileiro das primeiras decadas do seculo xxi aportes para o debate'
        )

    def test_book_title_for_deduplication_remove_double_spaces(self):
        self.assertEqual(
            book_title_for_deduplication(
                '  O  MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS   DÉCADAS DO SÉCULO XXI:  APORTES PARA O  DEBATE'),
            'o modelo de desenvolvimento brasileiro das primeiras decadas do seculo xxi aportes para o debate'
        )

    def test_book_title_for_deduplication_remove_end_punctuation_chars(self):
        self.assertEqual(
            book_title_for_deduplication(
                'O MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI: APORTES PARA O DEBATE,.;'),
            'o modelo de desenvolvimento brasileiro das primeiras decadas do seculo xxi aportes para o debate'
        )

    def test_book_title_for_deduplication_text_strip(self):
        self.assertEqual(
            book_title_for_deduplication(
                ' O MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI: APORTES PARA O DEBATE '),
            'o modelo de desenvolvimento brasileiro das primeiras decadas do seculo xxi aportes para o debate'
        )

    def test_book_title_for_deduplication_remove_accents(self):
        self.assertEqual(
            book_title_for_deduplication(
                'O MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI: APORTES PARA O DEBATE'),
            'o modelo de desenvolvimento brasileiro das primeiras decadas do seculo xxi aportes para o debate'
        )

    def test_book_title_for_deduplication_text_lower(self):
        self.assertEqual(
            book_title_for_deduplication(
                'O MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI: APORTES PARA O DEBATE'),
            'o modelo de desenvolvimento brasileiro das primeiras decadas do seculo xxi aportes para o debate'
        )

    def test_book_title_for_deduplication_remove_specific_chars(self):
        self.assertEqual(
            book_title_for_deduplication(
                'O MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI: APORTES PARA O DEBATE',
            chars_to_remove=[' ']),
            'omodelodedesenvolvimentobrasileirodasprimeirasdecadasdoseculoxxiaportesparaodebate'
        )

    def test_book_title_for_visualization_html_entities_keeps(self):
        self.assertEqual(
            book_title_for_visualization(
                'O MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI: &#60; APORTES PARA O DEBATE',
            keep_alpha_num_space_chars_only=False),
            'O MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI: < APORTES PARA O DEBATE'
        )

    def test_book_title_for_visualization_non_printable(self):
        self.assertEqual(
            book_title_for_visualization(
                '\tO MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI:\n APORTES PARA O DEBATE'),
            'O MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI APORTES PARA O DEBATE'
        )

    def test_book_title_for_visualization_alpha_num_spaces(self):
        self.assertEqual(
            book_title_for_visualization(
                'O MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI: &#60; APORTES PARA O DEBATE'),
            'O MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI APORTES PARA O DEBATE'
        )

    def test_book_title_for_visualization_double_spaces(self):
        self.assertEqual(
            book_title_for_visualization(
                '  O  MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS   DÉCADAS DO SÉCULO XXI:  APORTES PARA O  DEBATE'),
            'O MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI APORTES PARA O DEBATE'
        )

    def test_book_title_for_visualization_remove_pointing_at_end(self):
        self.assertEqual(
            book_title_for_visualization(
                'O MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI: APORTES PARA O DEBATE,.;'),
            'O MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI APORTES PARA O DEBATE'
        )

    def test_book_title_for_visualization_remove_specific_chars(self):
        self.assertEqual(
            book_title_for_visualization(
                'O MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI: APORTES PARA O DEBATE',
                chars_to_remove=[' ']),
            'OMODELODEDESENVOLVIMENTOBRASILEIRODASPRIMEIRASDÉCADASDOSÉCULOXXIAPORTESPARAODEBATE'
        )
          
    def test_document_sponsors_html_entities_keeps(self):
        self.assertEqual(
            document_title_for_deduplication('Fundação de Amparo a Pesquisa do Estado de São Paulo &#60; Biota Program', remove_special_char=False),
            'fundacao de amparo a pesquisa do estado de sao paulo < biota program'
        )

    def test_document_sponsors_keep_alpha_num_space(self):
        self.assertEqual(
            document_title_for_deduplication('Fundação de Amparo a Pesquisa do Estado de São Paulo &#60; Biota Program'),
            'fundacao de amparo a pesquisa do estado de sao paulo biota program'
        )

    def test_document_sponsors_remove_non_printable_chars(self):
        self.assertEqual(
            document_title_for_deduplication('Fundação de Amparo a Pesquisa do \n Estado de São Paulo \t Biota Program'),
            'fundacao de amparo a pesquisa do estado de sao paulo biota program'
        )

    def test_document_sponsors_remove_double_spaces(self):
        self.assertEqual(
            document_title_for_deduplication('Fundação  de   Amparo  a Pesquisa do  Estado de São Paulo  Biota Program'),
            'fundacao de amparo a pesquisa do estado de sao paulo biota program'
        )

    def test_document_sponsors_remove_end_punctuation_chars(self):
        self.assertEqual(
            document_title_for_deduplication('Fundação de Amparo a Pesquisa do Estado de São Paulo Biota Program,.;'),
            'fundacao de amparo a pesquisa do estado de sao paulo biota program'
        )

    def test_document_sponsors_text_strip(self):
        self.assertEqual(
            document_title_for_deduplication(' Fundação de Amparo a Pesquisa do Estado de São Paulo Biota Program '),
            'fundacao de amparo a pesquisa do estado de sao paulo biota program'
        )

    def test_document_sponsors_remove_accents(self):
        self.assertEqual(
            document_title_for_deduplication('Fundação de Amparo à Pesquisa do Estado de São Paulo Biota Program'),
            'fundacao de amparo a pesquisa do estado de sao paulo biota program'
        )

    def test_document_sponsors_text_lower(self):
        self.assertEqual(
            document_title_for_deduplication('Fundação de Amparo a Pesquisa do Estado de São Paulo Biota Program'),
            'fundacao de amparo a pesquisa do estado de sao paulo biota program'
        )

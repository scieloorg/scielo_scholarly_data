from scielo_scholarly_data import dates


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
    def test_convert_to_iso_date_without_separators(self):
        self.assertEqual(
            str(dates.convert_to_iso_date('20210921')),
            '2021-09-21'
        )

    def test_convert_to_iso_date_with_separators_hyphen(self):
        self.assertEqual(
            str(dates.convert_to_iso_date('2021-09-21')),
            '2021-09-21'
        )

    def test_convert_to_iso_date_with_separators_slash(self):
        self.assertEqual(
            str(dates.convert_to_iso_date('2021/09/21')),
            '2021-09-21'
        )

    def test_convert_to_iso_date_with_separators_dot(self):
        self.assertEqual(
            str(dates.convert_to_iso_date('2021.09.21')),
            '2021-09-21'
        )

    def test_convert_to_iso_date_with_separators_space(self):
        self.assertEqual(
            str(dates.convert_to_iso_date('2021 09 21')),
            '2021-09-21'
        )

    def test_convert_to_iso_date_with_separators_different_orderings(self):
        test_date = '2021-09-21'
        dates_ = {
            '21-09-2021': test_date,
            '21/09/2021': test_date,
            '21.09.2021': test_date,
            '21 09 2021': test_date
        }
        expected_values = list(dates_.values())
        obtained_values = [str(dates.convert_to_iso_date(dt)) for dt in dates_]

        self.assertListEqual(expected_values, obtained_values)


    def test_convert_to_iso_date_just_year_received(self):
        self.assertEqual(
            str(dates.convert_to_iso_date('2021')),
            '2021-01-01'
        )

    def test_convert_to_iso_date_just_year_delivered(self):
        self.assertEqual(
            str(dates.convert_to_iso_date('2021-06-15', only_year=True)),
            '2021'
        )

    def test_convert_to_iso_date_just_year_user_decision(self):
        self.assertEqual(
            str(dates.convert_to_iso_date('2021', day='01', month='01')),
            '2021-01-01'
        )

    def test_convert_to_iso_date_invalid_month(self):
        self.assertRaises(
            dates.DateMonthError,
            dates.convert_to_iso_date, '2021-13-09'
        )

    def test_convert_to_iso_date_invalid_day(self):
        self.assertRaises(
            dates.DateDayError,
            dates.convert_to_iso_date, '2021-12-35'
        )

    def test_convert_to_iso_date_invalid_date(self):
        self.assertRaises(
            dates.DateDayError,
            dates.convert_to_iso_date, '2021-02-31'
        )

    def test_convert_to_iso_month_or_day_with_one_digit(self):
        self.assertEqual(
            str(dates.convert_to_iso_date('2021-5-5')),
            '2021-05-05'
        )

    def test_convert_to_iso_full_month_in_spanish(self):
        self.assertEqual(
            str(dates.convert_to_iso_date('2021-Julio-05')),
            '2021-07-05'
        )

    def test_convert_to_iso_full_month_in_portuguese(self):
        self.assertEqual(
            str(dates.convert_to_iso_date('10 de maio de 2022')),
            '2022-05-10'
        )

    def test_convert_to_iso_invalid_format(self):
        self.assertRaises(
            dates.InvalidFormatError,
            dates.convert_to_iso_date, '200W'
        )

    def test_convert_to_iso_invalid_full_month(self):
        self.assertRaises(
            dates.InvalidFormatError,
            dates.convert_to_iso_date, '2021-jlia-30'
        )

    def test_convert_to_iso_start_with_full_month(self):
        self.assertEqual(
            str(dates.convert_to_iso_date('Janeiro 14, 2022')),
            '2022-01-14'
        )
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



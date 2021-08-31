import re

from scielo_scholarly_data.core import (
    convert_to_alpha_num_space,
    convert_to_alpha_space,
    remove_accents,
    remove_double_spaces,
    remove_non_printable_chars,
    unescape
)

from scielo_scholarly_data.values import (
    JOURNAL_TITLE_SPECIAL_CHARS,
    JOURNAL_TITLE_SPECIAL_WORDS,
    PATTERN_PARENTHESIS,
    PATTERNS_DOI
)




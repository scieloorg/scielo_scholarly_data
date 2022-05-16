import html
import unicodedata
import re
from datetime import datetime

from dateutil.parser import parse
from scielo_scholarly_data.values import (
    PATTERN_DATE,
    PATTERN_PARENTHESIS,
    PUNCTUATION_TO_REMOVE_FROM_TITLE_VISUALIZATION,
    MONTHS_DICT,
)

class DateMonthError(Exception):
    ...


class DateDayError(Exception):
    ...


class UnpackError(Exception):
    ...


class InvalidFormatError(Exception):
    ...


class NoneTypeError(Exception):
    ...



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


def standardizes_date(text, day='01', month='01'):
    """
    Função para padronizar uma data para uma string com dia, mês e ano separados por '-'.

    Parameters
    ----------
    text: str
        Data a ser padronizada;
    day: str
        Dia que será considerado quando a data original for apenas o ano;
    month: str
        Mês que será considerado quando a data original for apenas o ano;
    Returns
    -------
    str
        Data como uma string com dia, mês e ano separados por '-'.
    """
    if len(text) == 4 and text.isnumeric():
        return '-'.join([text, month, day])
    if len(text) == 8 and text.isnumeric():
        return text[:4] + '-' + text[4:6] + '-' + text[6:]
    if len(text) == 8 and not text.isnumeric():
        text = text.replace('-','')
        return text[:4] + '-0' + text[4:5] + '-0' + text[5:]
    if len(text) >= 10:
        for conector in [' de ', ' of ', ' del ']:
            text = text.replace(conector, '-')
        for c in ['/', '.', ' ']:
            if '-' in text:
                break
            text = text.replace(c, '-')
        return text


def months_in_full_to_int(month):
    """
    Função para converter um mês, escrito por extenso, em um valor numérico.

    Parameters
    ----------
    month : str
        Mês escrito por extenso.

    Returns
    -------
    int
        Mês numérico.
    """
    if month.lower() in MONTHS_DICT.keys():
        return MONTHS_DICT[month.lower()]



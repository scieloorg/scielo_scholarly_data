from datetime import datetime

from dateutil.parser import parse
from scielo_scholarly_data.values import (
    PATTERN_DATE,
    PATTERN_PARENTHESIS,
    PUNCTUATION_TO_REMOVE_FROM_TITLE_VISUALIZATION,
    TEXT_MONTH_TO_NUMERIC_MONTH,
)

from scielo_scholarly_data import core


class DateMonthError(Exception):
    ...


class DateDayError(Exception):
    ...


class InvalidFormatError(Exception):
    ...


def standardizes_date(text, day, month):
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


def split_date(text):
    """
    Função para fatiar uma data completa em ano, mês e dia.

    Parameters
    ----------
    text : str
        Data a ser fatiada.

    Returns
    -------
    tuple
        Ano (y), mês (m) e dia (d).
    """
    try:
        y, m, d = text.split('-')
    except (ValueError, AttributeError) as exc:
        if "unpack" in str(exc):
            raise UnpackError(f"{exc}")
        if "NoneType" in str(exc):
            raise InvalidFormatError(f"{exc}")
    return y, m, d


def convert_to_iso_date(text, day='01', month='01', only_year=False):
    """
    Função para a padronização de datas no formato ISO YYYY-MM-DD.

    Parameters
    ----------
    text : str
        Data a ser padronizada.
    day : str, default '01'
        Valor para dia no caso de data composta somente pelo ano.
    month : str, default '01'
        Valor para mês no caso de data composta somente pelo ano.
    just_year : bool, default False
        Valor lógico para retornar a data completa ou apenas o ano

    Returns
    -------
    data-type
        Data padronizada, que pode ser apenas o ano ou a data completa.
    """
    text = standardizes_date(text, day, month)

    y, m, d = split_date(text)

    if m.isalpha():
        m = months_in_full_to_int(m)

    if len(y) == 2 and len(d) == 4:
        d, y = y, d

    try:
        text = '-'.join([y, m, d])
    except TypeError as exc:
        raise NoneTypeError(f"{exc}: Não foi possível reconhecer a data")

    try:
        date = datetime.fromisoformat(text)
        if only_year:
            return date.year
        return date.isoformat()[:10]
    except ValueError as exc:
        if "day" in str(exc):
            raise DateDayError(f"{exc}: {y}-{m}-{d}")
        if "month" in str(exc):
            raise DateMonthError(f"{exc}: {y}-{m}-{d}")

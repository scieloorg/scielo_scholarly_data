from datetime import datetime
from scielo_scholarly_data import core

TEXT_MONTH_TO_NUMERIC_MONTH = {
    'janeiro':'01',
    'jan':'01',
    'enero':'01',
    'january':'01',
    'fevereiro':'02',
    'fev':'02',
    'febrero':'02',
    'february':'02',
    'feb':'02',
    'março':'03',
    'mar':'03',
    'marzo':'03',
    'march':'03',
    'abril':'04',
    'abr':'04',
    'april':'04',
    'apr':'04',
    'maio':'05',
    'mai':'05',
    'mayo':'05',
    'may':'05',
    'junho':'06',
    'jun':'06',
    'junio':'06',
    'june':'06',
    'julho':'07',
    'jul':'07',
    'julio':'07',
    'july':'07',
    'agosto':'08',
    'ago':'08',
    'august':'08',
    'aug':'08',
    'setembro':'09',
    'set':'09',
    'septiembre':'09',
    'sept':'09',
    'september':'09',
    'sep': '09',
    'outubro':'10',
    'out':'10',
    'octubre':'10',
    'oct':'10',
    'october':'10',
    'novembro':'11',
    'nov':'11',
    'noviembre':'11',
    'november':'11',
    'dezembro':'12',
    'dez':'12',
    'diciembre':'12',
    'dic':'12',
    'december':'12',
    'dec':'12',
}


WORDS_TO_REMOVE_IN_DATE_STANDARDIZATION = [
    'de',
    'of',
    'del',
    'el',
    'st',
    'th',
    'in',
    'accedido',
    'acceded',
    'accesado',
    'accesed',
    'acces',
    'acceso',
    'accessed',
    'acessado',
    'acesso',
    'citado',
    'cited',
    'consultado',
    'recuperado',
    'the last access',
    'year',
    'month',
    'day',

]


class InvalidStringError(Exception):
    ...


class DateMonthError(Exception):
    ...


class DateDayError(Exception):
    ...


class InvalidFormatError(Exception):
    ...


def _standardizes_date(text, day, month):
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
    text = core.keep_alpha_num_space(text)
    text = core.remove_words(text, WORDS_TO_REMOVE_IN_DATE_STANDARDIZATION)
    text = core.remove_double_spaces(text)
    if text.isnumeric():
        if len(text) == 4:
            return '-'.join([text, month, day])
        if len(text) == 8:
            return text[:4] + '-' + text[4:6] + '-' + text[6:]
    else:
        return text.replace(' ', '-')


def _months_in_full_to_int(month):
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
    if month.lower() in TEXT_MONTH_TO_NUMERIC_MONTH.keys():
        return TEXT_MONTH_TO_NUMERIC_MONTH[month.lower()]


def _split_date(text):
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
        if m.isalpha():
            m = _months_in_full_to_int(m)
        if y.isalpha():
            y = _months_in_full_to_int(y)
            y, m, d = d, y, m
        m = m.zfill(2)
        d = d.zfill(2)
        if len(y) == 2 and len(d) == 4:
            d, y = y, d
    except (ValueError, AttributeError) as exc:
            raise InvalidFormatError(f"{exc}: Não foi possível reconhecer a data")
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
    only_year : bool, default False
        Valor lógico para retornar a data completa ou apenas o ano

    Returns
    -------
    data-type
        Data padronizada, que pode ser apenas o ano ou a data completa.
    """
    text = _standardizes_date(text, day, month)

    y, m, d = _split_date(text)

    try:
        text = '-'.join([y, m, d])
    except TypeError as exc:
        raise InvalidFormatError(f"{exc}: Não foi possível reconhecer a data")

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
        else:
            raise InvalidStringError(f"{exc}: {y}-{m}-{d}")

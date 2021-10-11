import html
import unicodedata
import re
from dateutil.parser import parse
from datetime import date
from scielo_scholarly_data.values import PATTERN_PARENTHESIS

from scielo_scholarly_data.values import (
    PUNCTUATION_TO_REMOVE_FROM_TITLE_VISUALIZATION,
    DATE_SEPARATORS,
    MONTHS_DICT
)

def keep_alpha_num_space(text, keep_chars=None, replace_with=' '):
    """
    Mantém em text apenas caracteres alfanuméricos (letras latinas e algarismos arábicos) e espaços
    Possibilita manter em text caracteres especiais na lista keep_chars

    :param text: texto a ser tratado
    :param keep_chars: set de caracteres a serem mantidos
    :param replace_with: caracte a ser inserido quando não for alfanumérico ou não estiver em keep_chars
    :return: texto com apenas caracteres alphanuméricos e espaço mantidos (e especiais, caso indicado)
    """
    if keep_chars is None:
        keep_chars = []
    new_text = []
    for character in text:
        if character.isalnum() or character.isspace() or (character in keep_chars):
            new_text.append(character)
        else:
            new_text.append(replace_with)
    return ''.join(new_text)


def convert_to_alpha_space(text, keep_chars=None, replace_with=' '):
    """
    Mantém em text apenas caracteres alfa (letras latinas) e espaços
    Possibilita manter em text caracteres especiais na lista keep_chars

    :param text: texto a ser tratado
    :param keep_chars: set de caracteres a serem mantidos
    :param replace_with: caracte a ser inserido quando não for alfa ou não estiver em keep_chars
    :return: texto com apenas caracteres alpha e espaço mantidos (e especiais, caso indicado)
    """
    if keep_chars is None:
        keep_chars = []
    new_text = []
    for character in text:
        if character.isalpha() or character.isspace() or (character in keep_chars):
            new_text.append(character)
        else:
            new_text.append(replace_with)
    return ''.join(new_text)


def remove_accents(text):
    """
    Transforma caracteres acentuados de text em caracteres sem acento.

    :param text: texto a ser tratado
    :return: texto sem caracteres acentuados
    """
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')


def remove_double_spaces(text):
    """
    Remove de text os espaços duplos

    :param text: texto a ser tratado
    :return: texto sem espaços duplos
    """
    return " ".join([w for w in text.split() if w])


def remove_non_printable_chars(text, replace_with=''):
    """
    Remove de text os caracteres non pritable, isto é, que possuem código ASCII de 0 a 31
    Também remove caractere de código ASCII 127, que representa a ação DELETE

    :param text: texto a ser tratada
    :param replace_with: caracte a ser inserido quando for non printable
    :return: texto com caracteres ASCII de 0 a 31 e 127 removidos
    """
    new_text = []
    for t in text:
        if ord(t) >= 32 and ord(t) != 127:
            new_text.append(t)
        else:
            new_text.append(replace_with)
    return ''.join(new_text)


def remove_end_punctuation_chars(text, end_punctuation_chars_to_remove=PUNCTUATION_TO_REMOVE_FROM_TITLE_VISUALIZATION):
    """
    Remove pontuação no final de text, os caracteres que serão removidos devem constar em values.PUNCTUATION_TO_REMOVE_FROM_TITLE_VISUALIZATION

    :param text: text a ser tratado
    :end_punctuation_chars_to_remove: conjunto de caracteres (pontuação) a serem removidos do final de text
    """
    while True in [text.endswith(x) for x in end_punctuation_chars_to_remove]:
        text = text[:-1]
    return text


def unescape(text):
    """
    https://docs.python.org/3/library/html.html

    Convert all named and numeric character references (e.g. &gt;, &#62;, &#x3e;) in the string s to the corresponding Unicode characters
    """
    return html.unescape(text)


def remove_parenthesis(text):
    """
    Função para remoção de parenteses e respectivo conteúdo

    :param text: texto no qual os parenteses e o respectivo conteúdo serão removidos
    :return: texto sem parenteses e sem o respectivo conteúdo
    """
    parenthesis_search = re.search(PATTERN_PARENTHESIS, text)
    while parenthesis_search is not None:
        text = text[:parenthesis_search.start()] + text[parenthesis_search.end():]
        parenthesis_search = re.search(PATTERN_PARENTHESIS, text)
    text = remove_double_spaces(text)
    return text


def defaults_date_to_ISO_format(text, day='01', month='01', just_year=False):
    """
    Função para a padronização de datas no formato ISO YYYY-MM-DD

    :param text: data a ser padronizada
    :param day: valor para dia no caso de data composta somente pelo ano
    :param month: valor para mês no caso de data composta somente pelo ano
    :param just_year: valor lógico para retornar a data completa (default) ou apenas o ano
    :return: data padronizada
    """
    #Verifica se a data é composta apenas pelo ano retornando 'dia' e 'mês' da acordo com os valores recebidos como parâmetros
    if text.isdigit and len(text) <= 4:
        try:
            text = parse(text + '-' + month + '-' + day).date()
        except ValueError:
            return None
    else:
        try:
            #Tenta converter a data sem nenhum tratamento prévio
            text = parse(text).date()
        except ValueError:
            try:
                #Tenta separar 'dia', 'mês' e 'ano' a partir dos separadores de data
                for s in DATE_SEPARATORS:
                    text = text.replace(s,'-')
                year = text.split('-')[0]
                month = text.split('-')[1]
                day = text.split('-')[2]
            except IndexError:
                try:
                    #Tentar separar 'dia', 'mês' e 'ano' a partir da posição em text
                    year = text[:4]
                    month = text[4:-2]
                    day = text[-2:]
                except ValueError:
                    return None
            except ValueError:
                return None
    if just_year:
        return text.year
    else:
        return text

def remove_words(text, words_to_remove=[]):
    """
    Função para a remoção de palavras, pré-definidas em uma lista, em um dado texto

    :param text: texto no qual será realizada a remoção das palavras
    :param words_to_remove: lista de palavras a serem removidas
    :return: texto com as palavras removidas
    """
    text_words = text.split(' ')

    for sw in words_to_remove:
        if sw in text_words:
            text_words.remove(sw)

    return ' '.join(text_words)
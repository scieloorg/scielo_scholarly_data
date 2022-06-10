import html
import unicodedata
import re
import roman

from scielo_scholarly_data.values import (
    PATTERN_DATE,
    PATTERN_PARENTHESIS,
    PUNCTUATION_TO_REMOVE_FROM_TITLE_VISUALIZATION,
)


def keep_alpha_num_space(text, keep_chars=None, replace_with=' '):
    """
    Mantém em text apenas caracteres alfanuméricos (letras latinas e algarismos arábicos) e espaços.
    Possibilita manter em text caracteres especiais na lista keep_chars.

    Parameters
    ----------
    text : str
        Texto a ser tratado.
    keep_chars : list of str, default None
        Conjunto de caracteres a serem mantidos.
    replace_with : str, default ' '
        Caracte a ser inserido quando não for alfanumérico ou não estiver em keep_chars.

    Returns
    -------
    str
        Texto com apenas caracteres alphanuméricos e espaço mantidos (e especiais, caso indicado).
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


def keep_alpha_space(text, keep_chars=None, replace_with=' '):
    """
    Mantém em text apenas caracteres alfa (letras latinas) e espaços.
    Possibilita manter em text caracteres especiais na lista keep_chars.

    Parameters
    ----------
    text : str
        Texto a ser tratado.
    keep_chars : list of str, default None
        Conjunto de caracteres a serem mantidos.
    replace_with : str, default ' '
        Caracte a ser inserido quando não for alfanumérico ou não estiver em keep_chars.

    Returns
    -------
    str
        Texto com apenas caracteres alphanuméricos e espaço mantidos (e especiais, caso indicado).
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

    Parameters
    ----------
    text : str
        Texto a ser tratado.

    Returns
    -------
    str
        Texto sem caracteres acentuados.
    """
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')


def remove_double_spaces(text):
    """
    Remove de text os espaços duplos.

    Parameters
    ----------
    text : str
        Texto a ser tratado.

    Returns
    -------
    str
        Texto sem espaços duplos.
    """
    return " ".join([w for w in text.split() if w])


def remove_non_printable_chars(text, replace_with=''):
    """
    Remove de text os caracteres non pritable, isto é, que possuem código ASCII de 0 a 31.
    Também remove caractere de código ASCII 127, que representa a ação DELETE.

    Parameters
    ----------
    text : str
        Texto a ser tratado.
    replace_with : str, default ''
        Caracte a ser inserido quando for non printable.

    Returns
    -------
    str
        Texto com caracteres ASCII de 0 a 31 e 127 removidos.
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
    Remove pontuação no final de text, os caracteres que serão removidos devem constar em
    values.PUNCTUATION_TO_REMOVE_FROM_TITLE_VISUALIZATION.

    Parameters
    ----------
    text : str
        Texto a ser tratado.
    end_punctuation_chars_to_remove : list of str
        Conjunto de caracteres (pontuação) a serem removidos do final de text.

    Returns
    -------
    str
        Texto com pontuação removida no final.
    """
    while True in [text.endswith(x) for x in end_punctuation_chars_to_remove]:
        text = text[:-1]
    return text


def unescape(text):
    """
    https://docs.python.org/3/library/html.html
    Convert all named and numeric character references (e.g. &gt;, &#62;, &#x3e;) in the string s to the corresponding
    Unicode characters.

    Parameters
    ----------
    text : str
        Texto a ser tratado.

    Returns
    -------
    str
        Texto sem entidades HTML.
    """
    return html.unescape(text)


def remove_parenthesis(text):
    """
    Função para remoção de parênteses e respectivo conteúdo.

    Parameters
    ----------
    text : str
        Texto no qual os parênteses e o respectivo conteúdo serão removidos.

    Returns
    -------
    str
        Texto sem parênteses e sem o respectivo conteúdo.
    """
    parenthesis_search = re.search(PATTERN_PARENTHESIS, text)
    while parenthesis_search is not None:
        text = text[:parenthesis_search.start()] + text[parenthesis_search.end():]
        parenthesis_search = re.search(PATTERN_PARENTHESIS, text)
    text = remove_double_spaces(text)
    return text


def remove_chars(text, chars_to_remove):
    """
        Função para remoção de caracteres específicos, definidos a partir de uma lista.

        Parameters
        ----------
        text : str
            Texto no qual os caracteres específicados serão removidos.
        chars_to_remove : list
            Lista de caracteres a serem removidos do texto.

        Returns
        -------
        str
            Texto com os caracteres especificados removidos.
        """
    text_aux = []
    for c in text:
        if c not in chars_to_remove:
            text_aux.append(c)
    return ''.join(text_aux)


def remove_words(text, words_to_remove=[]):
    """
    Função para a remoção de palavras, pré-definidas em uma lista, em um dado texto.

    Parameters
    ----------
    text : str
        Texto no qual será realizada a remoção das palavras.
    param words_to_remove : list of str
        Lista de palavras a serem removidas.

    Returns
    -------
    str
        Texto com as palavras removidas.
    """
    text_words = text.split(' ')

    for sw in text_words:
        if sw in words_to_remove:
            text_words.remove(sw)

    return ' '.join(text_words)


def order_name_and_surname(text, surname_first=True):
    """
    Função para separar o nome e o sobrenome de uma string que representa um nome completo.
    Parameters
    ----------
    text : str
        Nome completo a ser separado.
    surname_first : bool, default = True
        Valor lógico que determina a ordem do nome e sobrenome na saída.

    Returns
    -------
    str
        Nome completo recomposto de acordo com a ordem estabelecida.
    """
    if ',' not in text:
        t = text.split(' ')
        if len(t) == 1:
            return text
        else:
            surname = t[-1]
            name = ' '.join(t[:-1])
    else:
        t = text.split(',')
        if len(t) == 2 and (t[0] == '' or t[1] == ''):
            return ''.join(t)
        else:
            surname = t[0]
            name = ' '.join(t[1:])
            name = name.strip()

    if surname_first:
        text = ''.join([surname, ', ', name])
    else:
        text = ''.join([name, ' ', surname])
    return text

  
def check_sum_orcid(orcid_number):
    """
    Função para verificar a validade de um regitro ORCID por meio do dígito verificador.
    Parameters
    ----------
    orcid_number : str
        Número de registro a ser verificado.

    Returns
    -------
    bool
        Retorna True caso o registro seja válido ou False caso contrário.
    """
    sub_calculation = 0
    for number in orcid_number[:-1]:
        sub_calculation = (sub_calculation + int(number)) * 2
    verifying_digit = (12 - (sub_calculation % 11)) % 11
    if verifying_digit == 10: verifying_digit = 'X'
    return str(verifying_digit) == orcid_number[-1]


def roman_to_int(roman_number):
    """
    Função para converter um número romano no correspondente indo-arábico.
    Parameters
    ----------
    roman : str
        Número romano.

    Returns
    -------
    int
        Número inteiro.
    """
    return roman.fromRoman(roman_number)
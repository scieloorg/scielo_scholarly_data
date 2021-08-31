import html
import unicodedata


def convert_to_alpha_num_space(text, keep_chars={}, replace_with=' '):
    """
    Mantém em text apenas caracteres alfanuméricos (letras latinas e algarismos arábicos) e espaços
    Possibilita manter em text caracteres especiais na lista keep_chars

    :param text: texto a ser tratado
    :param keep_chars: set de caracteres a serem mantidos
    :param replace_with: caracte a ser inserido quando não for alfanumérico ou não estiver em keep_chars
    :return: texto com apenas caracteres alphanuméricos e espaço mantidos (e especiais, caso indicado)
    """
    new_text = []
    for character in text:
        if character.isalnum() or character.isspace() or (character in keep_chars):
            new_text.append(character)
        else:
            new_text.append(replace_with)
    return ''.join(new_text)


def convert_to_alpha_space(text, keep_chars={}, replace_with=' '):
    """
    Mantém em text apenas caracteres alfa (letras latinas) e espaços
    Possibilita manter em text caracteres especiais na lista keep_chars

    :param text: texto a ser tratado
    :param keep_chars: set de caracteres a serem mantidos
    :param replace_with: caracte a ser inserido quando não for alfa ou não estiver em keep_chars
    :return: texto com apenas caracteres alpha e espaço mantidos (e especiais, caso indicado)
    """
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
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text.strip()


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


def unescape(text):
    """
    https://docs.python.org/3/library/html.html

    Convert all named and numeric character references (e.g. &gt;, &#62;, &#x3e;) in the string s to the corresponding Unicode characters
    """
    return html.unescape(text)

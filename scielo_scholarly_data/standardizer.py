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


def journal_title(text: str, remove_words=JOURNAL_TITLE_SPECIAL_WORDS, keep_parenthesis_content=True):
    """
    Procedimento para padroniza titulo de periódico de acordo com os seguintes métodos, por ordem
        1. Converte códigos HTML para caracteres Unicode
        2. Remove caracteres non printable
        3. Remove parenteses e respectivo conteúdo interno
        4. Remove acentuação
        5. Mantém caracteres alfanuméricos e espaço
        6. Remove espaços duplos
        7. Remove palavras especiais

    :param text: título do periódico a ser tratado
    :param remove_words: set de palavras a serem removidas
    :param keep_parenthesis_content: booleano que indica se deve ou não ser aplicada remoção de conteúdo entre parênteses
    :return: título tratado do periódico
    """
    text = unescape(text)
    text = remove_non_printable_chars(text)

    if not keep_parenthesis_content:
        parenthesis_search = re.search(PATTERN_PARENTHESIS, text)
        while parenthesis_search is not None:
            text = text[:parenthesis_search.start()] + text[parenthesis_search.end():]
            parenthesis_search = re.search(PATTERN_PARENTHESIS, text)

    text = remove_accents(text)
    text = convert_to_alpha_num_space(text, JOURNAL_TITLE_SPECIAL_CHARS)
    text = remove_double_spaces(text)

    text_words = text.split(' ')

    for sw in remove_words:
        if sw in text_words:
            text_words.remove(sw)

    text = ' '.join(text_words)
    text = remove_double_spaces(text)

    return text


def journal_issn(text: str):
    """
    Procedimento que padroniza ISSN de periódico

    :param text: caracteres que representam um código ISSN de um periódico
    :return: código ISSN padronizado ou nada
    """
    if text.isdigit():
        if len(text) == 8:
            return '-'.join([text[:4]] + [text[4:]]).upper()
    elif len(text) == 9:
        if '-' in text and text[:4].isdigit():
            return text.upper()

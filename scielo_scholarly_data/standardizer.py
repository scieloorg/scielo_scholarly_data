import re

from scielo_scholarly_data.core import (
    convert_to_alpha_num_space,
    convert_to_alpha_space,
    remove_accents,
    remove_double_spaces,
    remove_non_printable_chars,
    remove_parenthesis,
    remove_words,
    unescape
)

from scielo_scholarly_data.values import (
    DOCUMENT_TITLE_SPECIAL_CHARS,
    JOURNAL_TITLE_SPECIAL_CHARS,
    JOURNAL_TITLE_SPECIAL_WORDS,
    PATTERNS_DOI
)


def journal_title_for_deduplication(text: str, words_to_remove=JOURNAL_TITLE_SPECIAL_WORDS, keep_parenthesis_content=True):
    """
    Procedimento para padronizar título de periódico de acordo com os seguintes métodos, por ordem
        1. Converte códigos HTML para caracteres Unicode
        2. Remove caracteres non printable
        3. Remove parenteses e respectivo conteúdo interno
        4. Remove acentuação
        5. Mantém caracteres alfanuméricos e espaço
        6. Remove espaços duplos
        7. Remove palavras especiais
        8. Transforma para caracteres minúsculos

    :param text: título do periódico a ser tratado
    :param words_to_remove: set de palavras a serem removidas
    :param keep_parenthesis_content: booleano que indica se deve ou não ser aplicada remoção de conteúdo entre parênteses
    :return: título tratado do periódico
    """
    text = unescape(text)
    text = remove_non_printable_chars(text)
    if not keep_parenthesis_content:
        text = remove_parenthesis(text)
    text = remove_accents(text)
    text = convert_to_alpha_num_space(text, JOURNAL_TITLE_SPECIAL_CHARS)
    text = remove_double_spaces(text)
    text = remove_words(text, words_to_remove)

    return text.lower()


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


def issue_volume(text: str):
    # ToDo
    pass


def issue_number(text: str):
    """
    Procedimento que padroniza número da edição do periódico
    
    :param text: caracteres que representam número da edição
    :return: número de periódico padronizado
    """

    text = remove_non_printable_chars(text)
    text = convert_to_alpha_num_space(text, replace_with='')
    text = text.replace(' ','')
    return text


def document_doi(text: str):
    """
    Procedimento que padroniza DOI de documento

    :param text: caracteres que representam um código DOI de um documento
    :return: código DOI padronizado ou nada
    """
    for pattern_doi in PATTERNS_DOI:
        matched_doi = pattern_doi.search(text)
        if matched_doi:
            return matched_doi.group()


def document_title(text: str):
    """
    Função para padronizar titulos de documentos de acordo com os seguintes métodos, por ordem
        1. Converte códigos HTML para caracteres Unicode
        2. Remove caracteres non printable
        3. Remove acentuação
        4. Mantém caracteres alfanuméricos e espaço
        5. Remove espaços duplos

    :param text: título do documento a ser tratado
    :param remove_words: conjunto de palavras a serem removidas
    :return: título tratado do documento
    """

    text = unescape(text)
    text = remove_non_printable_chars(text)
    text = remove_accents(text)
    text = convert_to_alpha_num_space(text, DOCUMENT_TITLE_SPECIAL_CHARS)
    text = remove_double_spaces(text)

    return text

def document_first_page(text: str):
    pass


def document_last_page(text: str):
    pass


def document_elocation(text: str):
    pass


def document_publication_date(text: str):
    pass


def document_author(text: str):
    """
    Procedimento para padroniza nome de autor de acordo com os seguintes métodos, por ordem
        1. Remove acentos
        2. Mantém letras e espaços
        3. Remove espaços duplos

    :param text: nome do autor a ser tratado
    :return: nome tratado do autor
    """
    text = remove_accents(text)
    text = convert_to_alpha_space(text)
    text = remove_double_spaces(text)

    return text


def book_title(text: str):
    pass


def book_editor_name(text: str):
    pass


def book_editor_address(text: str):
    pass


def chapter_title(text: str):
    pass


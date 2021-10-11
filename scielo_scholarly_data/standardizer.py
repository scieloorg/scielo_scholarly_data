import re

from scielo_scholarly_data.core import (
    convert_to_alpha_space,
    keep_alpha_num_space,
    remove_accents,
    remove_double_spaces,
    remove_non_printable_chars,
    remove_parenthesis,
    remove_end_punctuation_chars,
    remove_words,
    unescape
)

from scielo_scholarly_data.values import (
    DATE_SEPARATORS,
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
    text = keep_alpha_num_space(text, JOURNAL_TITLE_SPECIAL_CHARS)
    #O procedimento keep_alpha_num_space() remove de text caracteres que não são alfanuméricos, mantendo somente
    #letras latinas, algarismos arábicos, espaços e outros caracteres indicados em values.JOURNAL_TITLE_SPECIAL_CHARS.
    text = remove_double_spaces(text)
    text = remove_words(text, words_to_remove)
    return text.lower()


def journal_title_for_visualization(text: str):
    """
    Procedimento para padronizar título de periódico de acordo com os seguintes métodos, por ordem
        1. Converte códigos HTML para caracteres Unicode
        2. Remove caracteres non printable
        3. Remove espaços duplos
        4. Remove pontuação no final do título
        5. Transforma para caracteres minúsculos

    :param text: título do periódico a ser tratado
    :return: título tratado do periódico
    """
    text = unescape(text)
    text = remove_non_printable_chars(text)
    text = remove_double_spaces(text)
    text = remove_end_punctuation_chars(text)
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


def issue_volume(text: str):
    """
    Procedimento que padroniza o número do volume do periódico

    :param text: caracteres que representam o número do volume do periódico
    :return: número do volume do periódico padronizado
    """

    # remove caracteres non printable
    text = remove_non_printable_chars(text)

    # remove caracteres especiais
    text = keep_alpha_num_space(text, replace_with='')

    # remove espaços duplos
    text = remove_double_spaces(text)

    # remove pontuação no final do número
    text = remove_end_punctuation_chars(text)

    #remove espaços nas extremidades do número
    text = text.strip()

    return text


def issue_number(text: str):
    """
    Procedimento que padroniza número da edição do periódico
    
    :param text: caracteres que representam número da edição
    :return: número de periódico padronizado
    """

    text = remove_non_printable_chars(text)
    text = keep_alpha_num_space(text, replace_with='')
    text = text.strip()
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


def document_title_for_deduplication(text: str):
    """
    Função para padronizar títulos de documentos de acordo com os seguinte métodos, por ordem
        1. Converte códigos HTML para caracteres Unicode
        2. Mantém caracteres alfanuméricos e espaço
        3. Remove caracteres non printable
        4. Remove espaços duplos
        5. Remove pontuação no final do título
        6. Remove espaços nas extremidades do título
        7. Remove acentos
        8. Converte os caracteres para caixa baixa

    :param text: título do documento a ser tratado
    :param remove_char: booleano que indica se as entidades HTML e os caracteres especiais devem ser mantidos ou retirados (default)
    :return: título tratado do documento
    """
    #Aplica os métodos de 1 até 6 da mesma forma que document_title_for_visualization
    text = document_title_for_visualization(text)

    #Remove acentos do título do documento
    text = remove_accents(text)

    #Converte os caracteres para caixa baixa
    text = text.lower()

    return text


def document_title_for_visualization(text: str, remove_special_char=True):
    """
    Função para padronizar titulos de documentos de acordo com os seguintes métodos, por ordem
        1. Converte códigos HTML para caracteres Unicode ou remove (default)
        2. Mantém caracteres alfanuméricos e espaço ou remove (default)
        3. Remove caracteres non printable
        4. Remove espaços duplos
        5. Remove pontuação no final do título
        6. Remove espaços nas extremidades do título

    :param text: título do documento a ser tratado
    :param remove_char: booleano que indica se as entidades HTML e os caracteres especiais devem ser mantidos ou retirados (default)
    :return: título tratado do documento
    """
    # o método unescape converte códigos no formato &#38; para seus caracteres correspondentes
    text = unescape(text)

    if remove_special_char:
        # remove caracteres especiais
        text = keep_alpha_num_space(text)

    # remove caracteres non printable
    text = remove_non_printable_chars(text)

    # remove espaços duplos
    text = remove_double_spaces(text)

    # remove ponto final
    text = remove_end_punctuation_chars(text)

    # remove espaços das bordas
    text = text.strip()

    return text


def document_first_page(text: str):
    """
    Função para normalizar o número da página inicial de um documento, considerando os seguintes métodos em ordem:
    1. Converter entidades HTML para caracteres unicode
    2. Remover caracteres não imprimíveis
    3. Remover caracteres especiais, mantendo apenas caracteres alfanuméricos e espaço
    4. Remover espaços duplos
    5. Remover pontuação no final do número
    6. Remover espaços brancos nas extremidades
    :param text: número da página inicial de um documento a ser normalizado
    :return: número da página inicial de um documento normalizado
    """
    # o método unescape converte códigos no formato &#38; para seus caracteres correspondentes
    text = unescape(text)

    # remove caracteres non printable
    text = remove_non_printable_chars(text)

    # remove caracteres especiais
    text = keep_alpha_num_space(text)

    # remove espaços duplos
    text = remove_double_spaces(text)

    # remove ponto final
    text = remove_end_punctuation_chars(text)

    # remove espaços
    text = text.replace(' ','')

    return text


def document_last_page(text: str):
    """
    Função para normalizar o número da página final de um documento, considerando os mesmo métodos da função document_first_page
    :param text: número da página final de um documento a ser normalizado
    :return: número da página final de um documento normalizado
    """
    # aplica os mesmos métodos considerados por document_first_page
    text = document_first_page(text)

    return text


def document_elocation(text: str):
    """
    Função para padronizar o valor do atributo elocation, esse valor identifica uma paginação eletrônica e só deverá
    ser utilizado quando houver um único número de paginação eletrônica. São exemplos de elocation: 0102961 e e27721
    este último considerado para elementos de citação.
    :param text: valor do atributo elocation a ser padronizado
    :return: valor do atributo elocation padronizado
    """
    # remove caracteres non printable
    text = remove_non_printable_chars(text)

    # remove caracteres especiais
    text = keep_alpha_num_space(text, replace_with='')

    # remove espaços duplos
    text = remove_double_spaces(text)

    # remove pontuação no final do número
    text = remove_end_punctuation_chars(text)

    # remove espaços
    text = text.replace(' ','')

    return text

def document_publication_date(text: str):
    """
    Função para padronizar a data da publicação de um documento para o formato ISO
    :param text: data da publicação a ser padronizada
    :return: data da publicação padronizada
    """
    # remove caracteres non printable
    text = remove_non_printable_chars(text)

    # remove caracteres especiais
    text = keep_alpha_num_space(text, keep_chars=DATE_SEPARATORS, replace_with='')

    # remove espaços duplos
    text = remove_double_spaces(text)

    return text


def document_author_for_visualization(text: str):
    """
    Procedimento para padronizar nome de autor de documento.
    :param text: nome do autor a ser tratado
    :return: nome tratado do autor
    """
    # Mantém letras e espaços
    text = convert_to_alpha_space(text)

    # Remove espaços duplos
    text = remove_double_spaces(text)

    return text


def document_author_for_deduplication(text: str):
    """
    Procedimento para padronizar nome de autor de documento.
    :param text: nome do autor a ser tratado
    :return: nome tratado do autor
    """
    # Mantém letras e espaços e remove espaços duplos
    text = document_author_for_visualization(text)

    # Remove acentuação
    text = remove_accents(text)

    # Transforma para caixa baixa
    text = text.lower()

    return text


def book_title(text: str):
    pass


def book_editor_name(text: str):
    pass


def book_editor_address(text: str):
    pass


def chapter_title(text: str):
    pass


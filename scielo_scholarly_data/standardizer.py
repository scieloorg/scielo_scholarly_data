import re

from scielo_scholarly_data.core import (
    convert_to_iso_date,
    convert_to_alpha_space,
    keep_alpha_num_space,
    remove_accents,
    remove_double_spaces,
    remove_non_printable_chars,
    remove_parenthesis,
    remove_end_punctuation_chars,
    remove_words,
    unescape,
)

from scielo_scholarly_data.values import (
    JOURNAL_TITLE_SPECIAL_CHARS,
    JOURNAL_TITLE_SPECIAL_WORDS,
    PATTERN_ISSN_WITH_HYPHEN,
    PATTERN_ISSN_WITHOUT_HYPHEN,
    PATTERNS_DOI,
    PUNCTUATION_TO_KEEP_IN_AUTHOR_VISUALIZATION,
    PATTERN_PAGE_RANGE,
    PUNCTUATION_TO_DEFINE_PAGE_RANGE,
)

from stdnum import (
    issn,
    isbn,
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


def journal_issn(text, use_issn_validator=False):
    '''
    Padroniza ISSN. Por exemplo, de "1387666x" para "1387-666X"

    Parameters
    ----------
    text : str
        Código ISSN a ser padrozinado
    use_issn_validator : bool
        O validador de ISSN deve ser utilizado?

    Returns
    -------
    issn
        Código ISSN padronizado ou None
    '''

    if re.match(PATTERN_ISSN_WITH_HYPHEN, text):
        if use_issn_validator:
            if not issn.is_valid(text):
                return
        return text.upper()

    if re.match(PATTERN_ISSN_WITHOUT_HYPHEN, text):
        text = '-'.join([text[:4], text[4:]])
        if use_issn_validator:
            if not issn.is_valid(text):
                return
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


def document_title_for_deduplication(text: str, remove_special_char=True):
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

    text = unescape(text)
    if remove_special_char:
        text = keep_alpha_num_space(text)
    text = remove_non_printable_chars(text)
    text = remove_double_spaces(text)
    text = remove_end_punctuation_chars(text)
    text = text.strip()
    text = remove_accents(text)
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


def document_first_page(text: str, keep_chars=PUNCTUATION_TO_DEFINE_PAGE_RANGE):
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

    text = unescape(text)
    text = remove_non_printable_chars(text)
    text = keep_alpha_num_space(text, keep_chars)
    text = remove_double_spaces(text)
    text = remove_end_punctuation_chars(text)
    text = text.replace(' ','')
    if not text.isdigit():
        try:
            text = re.match(PATTERN_PAGE_RANGE, text).groups()[0]
        except KeyError:
            return
    return text


def document_last_page(text: str, keep_chars=PUNCTUATION_TO_DEFINE_PAGE_RANGE):
    """
    Função para normalizar o número da página final de um documento, considerando os seguintes métodos em ordem:
    1. Converter entidades HTML para caracteres unicode
    2. Remover caracteres não imprimíveis
    3. Remover caracteres especiais, mantendo apenas caracteres alfanuméricos e espaço
    4. Remover espaços duplos
    5. Remover pontuação no final do número
    6. Remover espaços brancos

    :param text: número da página final de um documento a ser normalizado
    :return: número da página final de um documento normalizado
    """

    text = unescape(text)
    text = remove_non_printable_chars(text)
    text = keep_alpha_num_space(text, keep_chars)
    text = remove_double_spaces(text)
    text = remove_end_punctuation_chars(text)
    text = text.replace(' ', '')
    if not text.isdigit():
        try:
            first_page = int(re.match(PATTERN_PAGE_RANGE, text).groups()[0])
            last_page = int(re.match(PATTERN_PAGE_RANGE, text).groups()[1])
        except KeyError:
            return
        if first_page > last_page:
            text = str(first_page + last_page)
        else:
            text = str(last_page)
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

    text = remove_non_printable_chars(text)
    text = remove_double_spaces(text)
    text = text.strip()
    text = text.lower()
    text = remove_words(text, words_to_remove=['de', 'of'])
    text = convert_to_iso_date(text)

    return text


def document_author_for_visualization(text: str, surname_first=True):
    """
    Procedimento para padronizar nome de autor de documento, considerando os seguintes métodos, em ordem:
    1. Remoção de caracteres não imprimíveis
    2. Remover caracteres especiais, mantendo apenas caracteres alfabéticos e espaço
    3. Remover espaços duplos
    4. Remover espaços nas extremidades

    :param text: nome do autor a ser tratado
    :param surname_first: valor lógico que indica a posição do sobrenome na saída
    :return: nome tratado do autor
    """

    text = remove_non_printable_chars(text)
    text = convert_to_alpha_space(text, keep_chars=PUNCTUATION_TO_KEEP_IN_AUTHOR_VISUALIZATION)
    text = remove_double_spaces(text)
    text = text.strip()

    if ',' not in text:
        t = text.split(' ')
        surname = ''.join(t[-1:])
        name = ' '.join(t[:-1])
    else:
        t = text.split(', ')
        surname = ''.join(t[:1])
        name = ' '.join(t[1:])

    if surname_first:
        text = ''.join([surname, ', ', name])
    else:
        text = ''.join([name, ' ', surname])

    return text


def document_author_for_deduplication(text: str, surname_first=True):
    """
    Procedimento para padronizar nome de autor de documento, considerando os seguintes métodos, em ordem:
    1. Remoção de caracteres não imprimíveis
    2. Remover caracteres especiais, mantendo apenas caracteres alfabéticos e espaço
    3. Remover espaços duplos
    4. Remover espaços nas extremidades
    5. Remover acentos
    6. Converter para caixa baixa

    :param text: nome do autor a ser tratado
    :param surname_first: valor lógico que indica a posição do sobrenome na saída
    :return: nome tratado do autor
    """
    text = remove_non_printable_chars(text)
    text = convert_to_alpha_space(text, keep_chars=PUNCTUATION_TO_KEEP_IN_AUTHOR_VISUALIZATION)
    text = remove_double_spaces(text)
    text = text.strip()
    text = remove_accents(text)
    text = text.lower()

    if ',' not in text:
        t = text.split(' ')
        surname = ''.join(t[-1:])
        name = ' '.join(t[:-1])
    else:
        t = text.split(', ')
        surname = ''.join(t[:1])
        name = ' '.join(t[1:])

    if surname_first:
        text = ''.join([surname, ', ', name])
    else:
        text = ''.join([name, ' ', surname])

    return text


def book_title(text: str):
    pass


def book_editor_name(text: str):
    pass


def book_editor_address(text: str):
    pass


def chapter_title(text: str):
    pass


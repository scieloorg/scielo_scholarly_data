import re

from scielo_scholarly_data.dates import (
    convert_to_iso_date,
)

from scielo_scholarly_data.core import (
    check_sum_orcid,
    keep_alpha_space,
    keep_alpha_num_space,
    remove_accents,
    remove_double_spaces,
    remove_non_printable_chars,
    remove_parenthesis,
    remove_end_punctuation_chars,
    remove_chars,
    remove_words,
    order_name_and_surname,
    unescape,
    roman_to_int,
)

from scielo_scholarly_data.values import (
    JOURNAL_TITLE_SPECIAL_CHARS,
    JOURNAL_TITLE_SPECIAL_WORDS,
    PATTERN_ISSN_WITH_HYPHEN,
    PATTERN_ISSN_WITHOUT_HYPHEN,
    PATTERNS_DOI,
    PATTERN_ORCID,
    PATTERN_PAGE_RANGE,
    PUNCTUATION_TO_DEFINE_PAGE_RANGE,
    PUNCTUATION_TO_KEEP_IN_PERSONS_NAME_VISUALIZATION,
)

from scielo_scholarly_data.helpers import is_valid_issn
from urllib.parse import urlparse


class InvalidRomanNumeralError(Exception):
    ...

class ImpossibleConvertionToIntError(Exception):
    ...


def journal_title_for_deduplication(text: str, words_to_remove=JOURNAL_TITLE_SPECIAL_WORDS,
                                    keep_parenthesis_content=True, chars_to_remove=[]):
    """
    Procedimento para padronizar título de periódico de acordo com os seguintes métodos, por ordem:
        1. Converte códigos HTML para caracteres Unicode;
        2. Remove caracteres non printable;
        3. Remove parenteses e respectivo conteúdo interno;
        4. Remove acentuação;
        5. Mantém caracteres alfanuméricos e espaço;
        6. Remove espaços duplos;
        7. Remove palavras especiais;
        8. Transforma para caracteres minúsculos;
        9. Remove caracteres específicos definidos a partir de uma lista.

    Parameters
    ----------
    text : str
        Título do periódico a ser padronizado.
    words_to_remove : list of str
        Conjunto de palavras a serem removidas.
    keep_parenthesis_content : bool, default True
        Valor lógico que indica se deve ou não ser aplicada remoção de conteúdo entre parênteses.
    chars_to_remove : list, default empty
        Lista de caracteres que devem ser removidos.

    Returns
    -------
    str
        Título padronizado do periódico.
    """
    text = unescape(text)
    text = remove_non_printable_chars(text)
    if not keep_parenthesis_content:
        text = remove_parenthesis(text)
    text = remove_accents(text)
    text = keep_alpha_num_space(text, JOURNAL_TITLE_SPECIAL_CHARS)
    text = remove_double_spaces(text)
    text = remove_words(text, words_to_remove)
    if chars_to_remove:
        text = remove_chars(text, chars_to_remove)
    return text.lower()


def journal_title_for_visualization(text: str):
    """
    Procedimento para padronizar título de periódico de acordo com os seguintes métodos, por ordem:
        1. Converte códigos HTML para caracteres Unicode;
        2. Remove caracteres non printable;
        3. Remove espaços duplos;
        4. Remove pontuação no final do título;
        5. Transforma para caracteres minúsculos.

    Parameters
    ----------
    text : str
        Título do periódico a ser padronizado.

    Returns
    -------
    str
        Título padronizado do periódico.
    """
    text = unescape(text)
    text = remove_non_printable_chars(text)
    text = remove_double_spaces(text)
    text = remove_end_punctuation_chars(text)
    return text


def journal_issn(text, use_issn_validator=False):
    '''
    Padroniza ISSN. Por exemplo, de "1387666x" para "1387-666X".

    Parameters
    ----------
    text : str
        Código ISSN a ser padrozinado.
    use_issn_validator : bool, default False
        O validador de ISSN deve ser utilizado?

    Returns
    -------
    str
        Código ISSN padronizado ou None.
    '''

    if re.match(PATTERN_ISSN_WITH_HYPHEN, text):
        if use_issn_validator:
            if not is_valid_issn(text):
                return
        return text.upper()

    if re.match(PATTERN_ISSN_WITHOUT_HYPHEN, text):
        text = '-'.join([text[:4], text[4:]])
        if use_issn_validator:
            if not is_valid_issn(text):
                return
        return text.upper()


def issue_volume(text: str, force_integer=True):
    """
    Procedimento que padroniza o número do volume do periódico de acordo com os seguintes métodos, por ordem:
        1) Remove caracteres non printable;
        2) Remove caracteres especiais;
        3) Remove espaços duplos;
        4) Remove pontuação no final do número;
        5) Remove espaços nas extremidades do número;
        6) Remove caracteres alfabéticos (opcional);
        7) Transforma números romanos em indo-arábicos (opcional).

    Parameters
    ----------
    text : str
        Caracteres que representam o número do volume do periódico.
    force_integer : bool
        Valor lógico para a manutenção de apenas caracteres numéricos, default True.
    convert_romans : bool
        Valor lógico para a conversão de número romano em indo-arábico, default False.

    Returns
    -------
    str
        Número do volume do periódico padronizado.
    """

    text = unescape(text)
    text = remove_non_printable_chars(text)
    text = keep_alpha_num_space(text, replace_with=' ')
    text = remove_double_spaces(text)
    text = remove_end_punctuation_chars(text)
    text = text.strip()
    #text = remove_words(text, WORDS_TO_REMOVE_VOLUME_NUMBER)

    if force_integer:
        romans = ['M', 'D', 'C', 'L', 'X', 'V', 'I']
        for value in text.split(' '):
            if value.isnumeric():
                return value
        for value in text.split(' '):
            if value.isalpha():
                convert_roman = True
                for char in value:
                    if char.upper() not in romans:
                        convert_roman = False
                        pass
                if convert_roman:
                    try:
                        return str(roman_to_int(value.upper()))
                    except:
                        raise InvalidRomanNumeralError(f"O valor {value} não é um número romano")

        raise ImpossibleConvertionToIntError(f"Não foi possível converter o valor {text} para inteiro")

    return text

def issue_number(text: str):
    """
    Procedimento que padroniza número da edição do periódico de acordo com os seguintes métodos, por ordem:
        1) Remove caracteres non printable;
        2) Remove caracteres especiais;
        3) Remove espaços nas extremidades do número.

    Parameters
    ----------
    text : str
        Caracteres que representam número da edição do periódico.

    Returns
    -------
    str
        Número da edição do periódico padronizado.
    """

    text = remove_non_printable_chars(text)
    text = keep_alpha_num_space(text, replace_with='')
    text = text.strip()
    return text


def document_doi(text: str, return_mode='uri'):
    """
    Procedimento que padroniza DOI de documento.

    Parameters
    ----------
    text : str
        Caracteres que representam um código DOI de um documento.
    return_mode : str
        Define qual a informação que será retornada host, path ou uri (default).

    Returns
    -------
    str ou error.
        Código DOI padronizado de acordo com a demanda ou str vazia ou erro de formato.

    Exemplo:
        uri: http://dx.doi.org/10.1038/nphys1170.
        path: 10.1038/nphys1170.
        host: dx.doi.org.
    """
    matched_doi = False
    for pattern_doi in PATTERNS_DOI:
        matched_doi = pattern_doi.search(text)
        if matched_doi:
            break
    if not matched_doi:
        return {'error' : 'invalid doi'}
    if return_mode == 'uri':
        return f'http://doi.org/{matched_doi.group()}'
    if return_mode == 'host':
        return 'doi.org'
    if return_mode == 'path':
        return matched_doi.group()


def document_title_for_deduplication(text: str, remove_special_char=True, chars_to_remove=[]):
    """
    Função para padronizar títulos de documentos de acordo com os seguinte métodos, por ordem:
        1. Converte códigos HTML para caracteres Unicode;
        2. Mantém caracteres alfanuméricos e espaço;
        3. Remove caracteres non printable;
        4. Remove espaços duplos;
        5. Remove pontuação no final do título;
        6. Remove espaços nas extremidades do título;
        7. Remove acentos;
        8. Remove caracteres específicos definidos a partir de uma lista;
        9. Converte os caracteres para caixa baixa.

    Parameters
    ----------
    text : str
        Título do documento a ser padronizado.
    remove_char : bool, default True
        Valor lógico que indica se as entidades HTML e os caracteres especiais devem ser mantidos ou retirados.
    chars_to_remove : list, default empty
        Lista de caracetres que devem ser removidos.

    Returns
    -------
    str
        Título padronizado do documento.
    """

    text = unescape(text)
    if remove_special_char:
        text = keep_alpha_num_space(text)
    text = remove_non_printable_chars(text)
    text = remove_double_spaces(text)
    text = remove_end_punctuation_chars(text)
    text = text.strip()
    text = remove_accents(text)
    if chars_to_remove:
        text = remove_chars(text, chars_to_remove)
    text = text.lower()
    return text


def document_title_for_visualization(text: str, remove_special_char=True):
    """
    Função para padronizar titulos de documentos de acordo com os seguintes métodos, por ordem:
        1. Converte códigos HTML para caracteres Unicode ou remove (default);
        2. Mantém caracteres alfanuméricos e espaço ou remove (default);
        3. Remove caracteres non printable;
        4. Remove espaços duplos;
        5. Remove pontuação no final do título;
        6. Remove espaços nas extremidades do título.

    Parameters
    ----------
    text : str
        Título do documento a ser padronizado.
    remove_special_char : bool, default True
        Valor lógico que indica se as entidades HTML e os caracteres especiais devem ser mantidos ou retirados (default).

    Returns
    -------
    str
        Título padronizado do documento.
    """

    text = unescape(text)
    if remove_special_char:
        text = keep_alpha_num_space(text)
    text = remove_non_printable_chars(text)
    text = remove_double_spaces(text)
    text = remove_end_punctuation_chars(text)
    text = text.strip()
    return text


def document_first_page(text: str, keep_chars=PUNCTUATION_TO_DEFINE_PAGE_RANGE):
    """
    Função para normalizar o número da página inicial de um documento, considerando os seguintes métodos em ordem:
    1. Converter entidades HTML para caracteres unicode;
    2. Remover caracteres não imprimíveis;
    3. Remover caracteres especiais, mantendo apenas caracteres alfanuméricos e espaço;
    4. Remover espaços duplos;
    5. Remover pontuação no final do número;
    6. Remover espaços brancos nas extremidades.

    Parameters
    ----------
    text : str
        Número da página inicial de um documento a ser padronizado.

    Returns
    -------
    str
        Número da página inicial de um documento padronizado.
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
        except (KeyError, AttributeError):
            return
    return text


def document_last_page(text: str, keep_chars=PUNCTUATION_TO_DEFINE_PAGE_RANGE):
    """
    Função para normalizar o número da página final de um documento, considerando os seguintes métodos em ordem:
    1. Converter entidades HTML para caracteres unicode;
    2. Remover caracteres não imprimíveis;
    3. Remover caracteres especiais, mantendo apenas caracteres alfanuméricos e espaço;
    4. Remover espaços duplos;
    5. Remover pontuação no final do número;
    6. Remover espaços brancos.

    Parameters
    ----------
    text : str
        Número da página final de um documento a ser padronizado.

    Returns
    -------
    str
        Número da página final de um documento padronizado.
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
        except (KeyError, AttributeError):
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
    este último considerado para elementos de citação. Os seguinte métodos são considerados, em ordem:
        1) Remove caracteres non printable;
        2) Remove caracteres especiais;
        3) Remove espaços duplos;
        4) Remove pontuação no final do número;
        5) Remove espaços.

    Parameters
    ----------
    text : str
        Valor do atributo elocation a ser padronizado.

    Returns
    -------
    str
        Valor do atributo elocation padronizado.
    """

    text = remove_non_printable_chars(text)
    text = keep_alpha_num_space(text, replace_with='')
    text = remove_double_spaces(text)
    text = remove_end_punctuation_chars(text)
    text = text.replace(' ','')
    return text


def document_publication_date(text: str, day='01', month='01', only_year=False):
    """
    Função para padronizar a data da publicação de um documento para o formato ISO,
    de acordo com os seguinte métodos, em ordem:
        1) Remove caracteres non printable;
        2) Remove espaços duplos;
        3) Remove espaços nas extremidades da data;
        4) Converte os caracteres para caixa baixa;
        5) Remove palavras de uma lista.

    Parameters
    ----------
    text : str
        Data da publicação a ser padronizada.

    Returns
    -------
    data-type
        Data da publicação padronizada.
    """

    text = remove_non_printable_chars(text)
    text = remove_double_spaces(text)
    text = text.strip()
    text = remove_words(text, words_to_remove=['de', 'of'])
    text = convert_to_iso_date(text, day, month, only_year)

    return text


def document_author_for_visualization(text: str, surname_first=True):
    """
    Procedimento para padronizar nome de autor de documento, considerando os seguintes métodos, em ordem:
    1. Remoção de caracteres não imprimíveis;
    2. Remover caracteres especiais, mantendo apenas caracteres alfabéticos e espaço;
    3. Remover espaços duplos;
    4. Remover espaços nas extremidades.

    Parameters
    ----------
    text : str
        Nome do autor a ser padronizado.
    surname_first : bool, default True
        Valor lógico que indica a posição do sobrenome na saída.

    Returns
    -------
    str
        Nome padronizado do autor.
    """

    text = remove_non_printable_chars(text)
    text = keep_alpha_space(text, keep_chars=PUNCTUATION_TO_KEEP_IN_PERSONS_NAME_VISUALIZATION)
    text = remove_double_spaces(text)
    text = text.strip()
    text = order_name_and_surname(text, surname_first)
    return text


def document_author_for_deduplication(text: str, surname_first=True, chars_to_remove=[]):
    """
    Procedimento para padronizar nome de autor de documento, considerando os seguintes métodos, em ordem:
    1. Remoção de caracteres não imprimíveis;
    2. Remover caracteres especiais, mantendo apenas caracteres alfabéticos e espaço;
    3. Remover espaços duplos;
    4. Remover espaços nas extremidades;
    5. Remover acentos;
    6. Converter para caixa baixa;
    7. Remove caracteres específicos definidos a partir de uma lista.

    Parameters
    ----------
    text : str
        Nome do autor a ser padronizado.
    surname_first : bool, default True
        Valor lógico que indica a posição do sobrenome na saída.
    chars_to_remove : list, default empty
        Lista de caracteres que devem ser removidos.

    Returns
    -------
    str
        Nome padronizado do autor.
    """
    text = remove_non_printable_chars(text)
    text = keep_alpha_space(text, keep_chars=PUNCTUATION_TO_KEEP_IN_PERSONS_NAME_VISUALIZATION)
    text = remove_double_spaces(text)
    text = text.strip()
    text = remove_accents(text)
    text = text.lower()
    text = order_name_and_surname(text, surname_first)
    if chars_to_remove:
        text = remove_chars(text, chars_to_remove)
    return text


def book_title_for_deduplication(text: str, keep_alpha_num_space_chars_only=True, chars_to_remove=[]):
    """
    Função para padronizar títulos de livros de acordo com os seguinte métodos, por ordem:
        1. Converte códigos HTML para caracteres Unicode;
        2. Converte os caracteres para caixa baixa;
        3. Mantém caracteres alfanuméricos e espaço;
        4. Remove caracteres non printable;
        5. Remove espaços duplos;
        6. Remove pontuação no final do título;
        7. Remove espaços nas extremidades do título;
        8. Remove acentos;
        9. Remove caracteres específicos definidos a partir de uma lista.

    Parameters
    ----------
    text : str
        Título do livro a ser padronizado.
    keep_alpha_num_space_chars_only : bool, default True
        Valor lógico que indica se as entidades HTML e os caracteres especiais devem ser mantidos ou retirados.
    chars_to_remove : list, default empty
        Lista de caracteres que devem ser removidos.

    Returns
    -------
    str
        Título padronizado do livro.
    """

    text = unescape(text)
    if keep_alpha_num_space_chars_only:
        text = keep_alpha_num_space(text)
    text = remove_non_printable_chars(text)
    text = remove_double_spaces(text)
    text = remove_end_punctuation_chars(text)
    text = text.strip()
    text = remove_accents(text)
    text = text.lower()
    if chars_to_remove:
        text = remove_chars(text, chars_to_remove)
    return text


def book_title_for_visualization(text: str, keep_alpha_num_space_chars_only=True, chars_to_remove=[]):
    """
    Função para padronizar titulos de livros de acordo com os seguintes métodos, por ordem:
        1. Converte códigos HTML para caracteres Unicode ou remove (default);
        2. Remove espaços nas extremidades do título;
        3. Mantém caracteres alfanuméricos e espaço ou remove (default);
        4. Remove caracteres non printable;
        5. Remove espaços duplos;
        6. Remove pontuação no final do título;
        7. Remove caracteres específicos definidos a partir de uma lista.

    Parameters
    ----------
    text : str
        Título do livro a ser padronizado.
    keep_alpha_num_space_chars_only : bool, default True
        Valor lógico que indica se as entidades HTML e os caracteres especiais devem ser mantidos ou retirados (default).
    chars_to_remove : list, default empty
        Lista de caracteres que devem ser removidos.

    Returns
    -------
    str
        Título padronizado do livro.
    """

    text = unescape(text)
    if keep_alpha_num_space_chars_only:
        text = keep_alpha_num_space(text)
    text = remove_non_printable_chars(text)
    text = remove_double_spaces(text)
    text = remove_end_punctuation_chars(text)
    text = text.strip()
    if chars_to_remove:
        text = remove_chars(text, chars_to_remove)
    return text


def book_editor_name_for_visualization(text: str, keep_alpha_num_space_only=True):
    """
    Função para padronizar nomes de editoras de acordo com os seguintes métodos, por ordem:
        1. Converte códigos HTML para caracteres Unicode ou remove (default);
        2. Mantém caracteres alfanuméricos e espaço ou remove (default);
        3. Remove caracteres non printable;
        4. Remove espaços duplos;
        5. Remove pontuação no final do nome;
        6. Remove espaços nas extremidades do nome.

    Parameters
    ----------
    text : str
        Nome da editora a ser padronizado.
    keep_alpha_num_space_only : bool, default True
        Valor lógico que indica se as entidades HTML e os caracteres especiais devem ser mantidos ou retirados (default).

    Returns
    -------
    str
        Nome padronizado da editora.
    """

    text = unescape(text)
    if keep_alpha_num_space_only:
        text = keep_alpha_num_space(text)
    text = remove_non_printable_chars(text)
    text = remove_double_spaces(text)
    text = remove_end_punctuation_chars(text)
    text = text.strip()
    return text


def book_editor_name_for_deduplication(text: str, keep_alpha_num_space_only=True):
    """
    Função para padronizar nomes de editoras de acordo com os seguinte métodos, por ordem:
        1. Converte códigos HTML para caracteres Unicode;
        2. Mantém caracteres alfanuméricos e espaço;
        3. Remove caracteres non printable;
        4. Remove espaços duplos;
        5. Remove pontuação no final do nome;
        6. Remove espaços nas extremidades do nome;
        7. Remove acentos;
        8. Converte os caracteres para caixa baixa.

    Parameters
    ----------
    text : str
        Nome da editora a ser padronizado.
    keep_alpha_num_space_only : bool, default True
        Valor lógico que indica se as entidades HTML e os caracteres especiais devem ser mantidos ou retirados.

    Returns
    -------
    str
        Nome padronizado da editora.
    """

    text = unescape(text)
    if keep_alpha_num_space_only:
        text = keep_alpha_num_space(text)
    text = remove_non_printable_chars(text)
    text = remove_double_spaces(text)
    text = remove_end_punctuation_chars(text)
    text = text.strip()
    text = remove_accents(text)
    text = text.lower()
    return text

  
def orcid_validator(text: str, return_mode='uri'):
    """
        Função para verificar e padronizar um registro ORCID.

        Parameters
        ----------
        text : str
            Registro ORCID a ser validado e padronizado.
        return_mode : str
            Define qual a informação que será retornada host, path ou uri (default).

        Returns
        -------
        str ou error

        Exemplo:
            uri: https://orcid.org/0000-0002-1825-0097.
            path: 0000-0002-1825-0097.
            host: orcid.org.
        """
    orcid = urlparse(text)
    matched_orcid = re.match(PATTERN_ORCID, orcid.path)
    if not matched_orcid:
        return {'error' : 'invalid format'}
    path = keep_alpha_num_space(matched_orcid.groups()[1], replace_with='')
    if not check_sum_orcid(path):
        return {'error' : 'invalid checksum'}
    if orcid.scheme == '':
        scheme = 'https'
    else:
        scheme = orcid.scheme
    if orcid.netloc == '':
        hostname = 'orcid.org'
    else:
        hostname = orcid.netloc
    if return_mode == 'uri':
        return scheme + '://' + hostname + '/' + matched_orcid.groups()[1]
    if return_mode == 'path':
        return matched_orcid.groups()[1]
    if return_mode == 'host':
        return hostname
  

def document_sponsors(text: str, remove_special_char=True):
    """
    Função para padronizar o nome de patrocinadores de documentos de acordo com os seguinte métodos, por ordem:
        1. Converte códigos HTML para caracteres Unicode;
        2. Mantém caracteres alfanuméricos e espaço;
        3. Remove caracteres non printable;
        4. Remove espaços duplos;
        5. Remove pontuação no final do título;
        6. Remove espaços nas extremidades do título;
        7. Remove acentos;
        8. Converte os caracteres para caixa baixa.

    Parameters
    ----------
    text : str
        Título do documento a ser padronizado.
    remove_char : bool, default True
        Valor lógico que indica se as entidades HTML e os caracteres especiais devem ser mantidos ou retirados.

    Returns
    -------
    str
        Título padronizado do documento.
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


def book_title(text: str):
    pass  

  
def book_editor_address(text: str):
    pass


def chapter_title(text: str):
    pass

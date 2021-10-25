from stdnum import (
    issn,
    isbn,
)

# https://www.issn.org/understanding-the-issn/what-is-an-issn (accessed on 2021/08/31)
def is_valid_issn(text: str):
    """
    Procedimento que verifica se um código ISSN é valido

    Parameters
    ----------
    text : str
        Código ISSN a ser validado.

    Returns
    -------
    bool
        Valor lógica que indica a validade do ISSN.
    """
    return issn.is_valid(text)


def is_valid_isbn(text: str):
    """
    Procedimento que verifica se um código ISBN é valido

    :param isbn: código ISBN padronizado
    :return: True se código é válido, False caso contrário
    """
    pass
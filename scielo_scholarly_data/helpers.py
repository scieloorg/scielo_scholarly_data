# https://www.issn.org/understanding-the-issn/what-is-an-issn (accessed on 2021/08/31)
def is_valid_issn(issn: str):
    """
    Procedimento que verifica se um código ISSN é valido

    :param issn: código ISSN padronizado
    :return: True se código é válido, False caso contrário
    """
    informed_check_digit = issn[8] if issn[8].upper() != 'X' else '10'
    informed_check_digit = int(informed_check_digit)

    sum_digits = 0

    pos = 8
    for i in issn[:4] + issn[5:8]:
        sum_digits += int(i) * pos
        pos -= 1

    modulus = sum_digits % 11
    if modulus == 0:
        computed_check_digit = modulus
    else:
        computed_check_digit = 11 - modulus

    if computed_check_digit == informed_check_digit:
        return True

    return False


def is_valid_isbn(isbn: str):
    """
    Procedimento que verifica se um código ISBN é valido

    :param isbn: código ISBN padronizado
    :return: True se código é válido, False caso contrário
    """
    pass
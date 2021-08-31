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

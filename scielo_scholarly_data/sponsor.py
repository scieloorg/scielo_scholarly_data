# -*- coding: utf-8 -*

import scielo_scholarly_data.standardizer as standardizer
import kshingle as ks


def get_similar(name, standard_names):
    """
    Procedimento para obter o nome completo e o acrônimo do financiador de uma pesquisa.

    Parameters
    ----------
    standard_names : tuple
        Nome completo e acrônimo padronizado.
    name : str
        Texto não padronizado.

    Returns
    -------
    tuple
        1º elemento: texto de entrada tratado
        2º elemento: nome completo padronizado
        3º elemento: acrônimo padronizado
    """
    name = standardizer.document_sponsors(name)
    for standard_name in standard_names:
        if len(name) > 0 and ks.jaccard_strings(standardizer.document_sponsors(standard_name), name, k=2) > 0.75:
            return name, standard_names[0], standard_names[1]
    return name, "", ""


def get_sponsor_names(name, pairs):
    """
    Procedimento para submeter um nome de financiador não padronizado e uma lista de tuplas
    (nome padronizado, acrônimo) para medição de similaridade.

    Parameters
    ----------
    name : str
        Nome do financiador para padronização.
    pairs : list
        Lista de tuplas: nome completo e acrônimo padronizado.

    Returns
    -------
    tuple
        1º elemento: nome completo padronizado
        2º elemento: acrônimo padronizado
    """
    name = standardizer.document_sponsors(name)
    for pair in pairs:
        response = get_similar(name, pair)
        if response[-2:] != ("", ""):
            return response

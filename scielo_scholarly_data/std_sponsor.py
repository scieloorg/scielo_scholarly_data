# -*- coding: utf-8 -*

import scielo_scholarly_data.standardizer as standardizer
import kshingle as ks
from sentence_transformers import SentenceTransformer, util
from operator import itemgetter


model = SentenceTransformer('scielo_scholarly_data/stmodels/paraphrase-multilingual-MiniLM-L12-v2')


def make_standard_sponsor(name, acron):
    """
    Função para montar uma lista de dicionários a partir de uma string que descreve o nome de um financiador e seu acrônimo.

    Parameters
    ----------
    sponsor : str
        Nome e acrônimo padronizados de um financiador.
        Exemplo:
            "Conselho Nacional de Desenvolvimento Científico e Tecnológico,CNPq"

    Returns
    -------
    list
        Uma lista de dicionários nos quais a chave "text" descreve as possíveis combinações de nome e acrônimo.
        [{
            "text": "Conselho Nacional de Desenvolvimento Científico e Tecnológico CNPq",
            "name": "Conselho Nacional de Desenvolvimento Científico",
            "acronym": "CNPq"
        },
        {
            "text": "Conselho Nacional de Desenvolvimento Científico e Tecnológico",
            "name": "Conselho Nacional de Desenvolvimento Científico",
            "acronym": "CNPq"
        },
        {
            "text": "CNPq",
            "name": "Conselho Nacional de Desenvolvimento Científico",
            "acronym": "CNPq"
        }]
    """
    result = [
        {
            "text": name + " " + acron,
            "name": name,
            "acronym": acron
        },
        {
            "text": name,
            "name": name,
            "acronym": acron
        },
        {
            "text": acron,
            "name": name,
            "acronym": acron
        }
    ]
    return result


def search_sponsors_by_jaccard_similarity(name, sponsors):
    """
    Procedimento para obter o nome completo e o acrônimo do financiador de uma pesquisa,
    considerando o coeficiente de similaridade de Jaccard

    Parameters
    ----------
    name : str
        Nome da instituição financiadora, da forma que foi declarada, para padronização.
    sponsors : list
        Uma lista de dicionários nos quais a chave "text" descreve as possíveis combinações de nome e acrônimo.

    Returns
    -------
    list
        Uma lista ordenada de dicionários nos quais os nomes e acrônimos são associados a uma medida de similaridade.
        [{
            "standard_name": "Conselho Nacional de Desenvolvimento Científico e Tecnológico",
            "standard_acronym": "CNPq",
            "score": 1.0
        },
        {
            "standard_name": "Coordenação de Aperfeiçoamento de Pessoal de Nível Superior",
            "standard_acronym": "CAPES",
            "score": 0.01
        },
        {
            "standard_name": "Fundação de Amparo à Pesquisa do Estado de São Paulo",
            "standard_acronym": "FAPESP",
            "score": 0.05
        }]
    """
    name = standardizer.document_sponsors(name)
    if len(name) > 0:
        result = []
        for sponsor in sponsors:
            jaccard_index = ks.jaccard_strings(standardizer.document_sponsors(sponsor["text"]), name, k=2)
            d = {
                "standard_name": sponsor["name"],
                "standard_acronym": sponsor["acronym"],
                "score": jaccard_index
            }
            result.append(d)
        return sorted(result, key=itemgetter('score'), reverse=True)


def search_sponsors_by_semantic_similarity(name, sponsors):
    """
    Procedimento para obter o nome completo e o acrônimo do financiador de uma pesquisa,
    considerando a similaridade baseada em semântica textual.
    (https://www.sbert.net/examples/training/sts/README.html)

    Parameters
    ----------
    name : str
        Nome da instituição financiadora, da forma que foi declarada, para padronização.
    sponsors : list
        Uma lista de dicionários nos quais a chave "text" descreve as possíveis combinações de nome e acrônimo.

    Returns
    -------
    list
        Uma lista ordenada de dicionários nos quais os nomes e acrônimos são associados a uma medida de similaridade.
        [{
            "standard_name": "Conselho Nacional de Desenvolvimento Científico e Tecnológico",
            "standard_acronym": "CNPq",
            "score": 1.0
        },
        {
            "standard_name": "Coordenação de Aperfeiçoamento de Pessoal de Nível Superior",
            "standard_acronym": "CAPES",
            "score": 0.01
        },
        {
            "standard_name": "Fundação de Amparo à Pesquisa do Estado de São Paulo",
            "standard_acronym": "FAPESP",
            "score": 0.05
        }]
    """
    query_embedding = model.encode(name, convert_to_tensor=True)
    texts = [item["text"] for item in sponsors]
    corpus_embeddings = model.encode(texts, convert_to_tensor=True)
    search_hits = util.semantic_search(query_embedding, corpus_embeddings)
    search_hits = search_hits[0]  # Get the hits for the first query

    result = []

    for hit in search_hits:
        related_sponsor = sponsors[hit['corpus_id']]
        d = {
            "standard_name": related_sponsor['name'],
            "standard_acronym": related_sponsor['acronym'],
            "score": hit['score']
        }
        result.append(d)

    return result


def get_sponsor_names_with_score(name, sponsors, method="jaccard"):
    """
    Procedimento para obter o nome completo e o acrônimo do financiador de uma pesquisa,
    a partir da escolha de um método específico (jaccard ou semantic).

    Parameters
    ----------
    name : str
        Nome da instituição financiadora, da forma que foi declarada, para padronização.
    sponsors : list
        Uma lista de dicionários nos quais a chave "text" descreve as possíveis combinações de nome e acrônimo.
    method : str
        "jaccard" - similaridade de Jaccard
        "semantic" - similaridade semântica textual

    Returns
    -------
    list
        Uma lista ordenada de dicionários nos quais os nomes e acrônimos são associados a uma medida de similaridade.
        [{
            "standard_name": "Conselho Nacional de Desenvolvimento Científico e Tecnológico",
            "standard_acronym": "CNPq",
            "score": 1.0
        },
        {
            "standard_name": "Coordenação de Aperfeiçoamento de Pessoal de Nível Superior",
            "standard_acronym": "CAPES",
            "score": 0.01
        },
        {
            "standard_name": "Fundação de Amparo à Pesquisa do Estado de São Paulo",
            "standard_acronym": "FAPESP",
            "score": 0.05
        }]
    """
    if method == 'jaccard':
        return search_sponsors_by_jaccard_similarity(name, sponsors)
    else:
        return search_sponsors_by_semantic_similarity(name, sponsors)


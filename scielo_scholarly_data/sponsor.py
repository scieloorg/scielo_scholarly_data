# -*- coding: utf-8 -*

import scielo_scholarly_data.standardizer as standardizer
import kshingle as ks
import pandas as pd
from pandas import DataFrame
from sentence_transformers import SentenceTransformer, util
from collections import OrderedDict
from operator import itemgetter
from scielo_scholarly_data import std_sponsor


def get_standardized_sponsor_name(name, standard_names, method):
    temp = []

    for std_name, std_acron in standard_names:
        sponsor_standardized = std_sponsor.get_sponsor_names_with_score(
            name,
            std_sponsor.make_standard_sponsor(std_name, std_acron),
            method=method,
        )
        if sponsor_standardized != None:
            temp.append(sponsor_standardized[0])

    temp = sorted(temp, key=itemgetter('score'))
    return temp[-1]


def main():
    names = pd.read_csv('scielo_scholarly_data/example_in.csv', quotechar='"', encoding='latin-1', on_bad_lines='skip', sep=r'\\t', engine='python', header=None)
    sponsors = pd.read_csv('scielo_scholarly_data/standard_sponsors.csv', sep=',', header=None, encoding='utf-8')

    non_standard_names = [(row[1], row[3], row[4]) for index, row in names.iterrows()]
    standard_names = [(row[0], row[1]) for index, row in sponsors.iterrows()]

    sponsors_standardized = []
    sponsors_non_stadardized = []

    control = 0

    for name in non_standard_names:
        # id, non_std_name, project_number
        article_id, non_std_name, project_number = name

        jaccard = get_standardized_sponsor_name(non_std_name, standard_names, 'jaccard')
        semantic = get_standardized_sponsor_name(non_std_name, standard_names, 'semantic')

        if jaccard != None and semantic != None and jaccard["score"] >= 0.8:
            result = [
                article_id,
                non_std_name,
                project_number,
                jaccard["standard_name"],
                jaccard["standard_acronym"],
                jaccard["score"],
                semantic["standard_name"],
                semantic["standard_acronym"],
                semantic["score"]
            ]
            result = tuple(result)
            sponsors_standardized.append(result)
        else:
            sponsors_non_stadardized.append(name)

        df = pd.DataFrame(sponsors_standardized)
        df = df.drop_duplicates()
        df.to_csv('standardized.csv', sep=';', header=False, index=False, index_label=None, quotechar='"', line_terminator='\n', mode='a')

        df2 = pd.DataFrame(sponsors_non_stadardized)
        df2 = df2.drop_duplicates()
        df2.to_csv('non_standardized.csv', sep=';', header=False, index=False, index_label=None, quotechar='"', line_terminator='\n', mode='a')

        sponsors_standardized = []
        sponsors_non_stadardized = []


if __name__ == '__main__':
    main()


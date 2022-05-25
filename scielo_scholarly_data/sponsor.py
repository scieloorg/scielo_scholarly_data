# -*- coding: utf-8 -*

import scielo_scholarly_data.standardizer as standardizer
import kshingle as ks
import pandas as pd
from pandas import DataFrame
from sentence_transformers import SentenceTransformer, util
from collections import OrderedDict
from operator import itemgetter


def select_method_to_get_sponsor_name(name, standard_names, method):
    temp = []
    try:
        for standard_name in standard_names:
            std_name, std_acron = standard_name.split(",")
            sponsor_standardized = tasks.get_sponsor_names(
                name,
                make_standard_sponsor(std_name, std_acron),
                method=method,
                get_result=True,
            )
            if sponsor_standardized != None:
                temp.append(sponsor_standardized[0])

        temp = sorted(temp, key=itemgetter('score'))
        return temp[-1]
    except:
        return


def main():
    names = pd.read_csv('financial_support_date_pid_file_sponsor_number_run.csv', quotechar='"', encoding='latin-1', on_bad_lines='skip', sep=r'\\t', engine='python', header=None)
    sponsors = pd.read_csv('standard_sponsors.csv', sep=',', header=None, encoding='utf-8')

    non_standard_names = [(row[1], row[3], row[4]) for index, row in names.iterrows()]
    standard_names = [row[0] + ',' + row[1] for index, row in sponsors.iterrows()]

    sponsors_standardized = []
    sponsors_non_stadardized = []

    control = 0

    for name in non_standard_names:
        # id, non_std_name, project_number
        article_id, non_std_name, project_number = name

        jaccard = select_method_to_get_sponsor_name(non_std_name, standard_names, 'jaccard')
        semantic = select_method_to_get_sponsor_name(non_std_name, standard_names, 'semantic')

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

        control += 1
        if control % 500 == 0:
            print(f"{control/5868*100:.2f}%")

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



from scielo_scholarly_data import standardizer
from scielo_scholarly_data import sponsor
import unittest

class TestSponsor(unittest.TestCase):
    def test_search_sponsors_by_jaccard_similarity(self):
        standard_name = "Conselho Nacional de Desenvolvimento Científico e Tecnológico,CNPq"
        standard_names = sponsor.make_standard_sponsor(standard_name)
        name = "Conselho Nacional de Desenvolvimento Científico e Tecnológico"
        result = sponsor.search_sponsors_by_jaccard_similarity(name, standard_names)
        self.assertEqual(
            result[0],
            {
                "standard_name": "Conselho Nacional de Desenvolvimento Científico e Tecnológico",
                "standard_acronym": "CNPq",
                "score": 1.0
            }
        )
        self.assertEqual(result[1]['standard_name'], "Conselho Nacional de Desenvolvimento Científico e Tecnológico")

        self.assertEqual(result[2]['standard_name'], "Conselho Nacional de Desenvolvimento Científico e Tecnológico")

        self.assertEqual(result[1]['standard_acronym'], "CNPq")

        self.assertEqual(result[2]['standard_acronym'], "CNPq")

    def test_search_sponsors_by_semantic_similarity(self):
        standard_name = "Conselho Nacional de Desenvolvimento Científico e Tecnológico,CNPq"
        standard_names = sponsor.make_standard_sponsor(standard_name)
        name = "Conselho Nacional de Desenvolvimento Científico e Tecnológico"
        result = sponsor.search_sponsors_by_semantic_similarity(name, standard_names)
        self.assertEqual(
            result[0],
            {
            "standard_name": "Conselho Nacional de Desenvolvimento Científico e Tecnológico",
            "standard_acronym": "CNPq",
            "score": 1.0
            }
        )
        self.assertEqual(result[1]['standard_name'], "Conselho Nacional de Desenvolvimento Científico e Tecnológico")

        self.assertEqual(result[2]['standard_name'], "Conselho Nacional de Desenvolvimento Científico e Tecnológico")

        self.assertEqual(result[1]['standard_acronym'], "CNPq")

        self.assertEqual(result[2]['standard_acronym'], "CNPq")

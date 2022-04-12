from scielo_scholarly_data import standardizer
from scielo_scholarly_data import sponsor
import unittest

class TestSponsor(unittest.TestCase):

    def test_get_similar_full_name(self):
        standard_names = "Conselho Nacional de Desenvolvimento Científico e Tecnológico", "CNPq"
        name = "conselho nacional de desenvolvimento cientifico e tecnologico dprofix"
        self.assertEqual(
            sponsor.get_similar(name, standard_names),
            ("conselho nacional de desenvolvimento cientifico e tecnologico dprofix", "Conselho Nacional de Desenvolvimento Científico e Tecnológico", "CNPq")
        )

    def test_get_similar_acron(self):
        standard_names = "Conselho Nacional de Desenvolvimento Científico e Tecnológico", "CNPq"
        name = "CNPQ"
        self.assertEqual(
            sponsor.get_similar(name, standard_names),
            ("cnpq", "Conselho Nacional de Desenvolvimento Científico e Tecnológico", "CNPq")
        )

    def test_get_similar_without_match(self):
        standard_names = "Conselho Nacional de Desenvolvimento Científico e Tecnológico", "CNPq"
        name = "fapesp cnpq pronex e conselho britanico"
        self.assertEqual(
            sponsor.get_similar(name, standard_names),
            ("fapesp cnpq pronex e conselho britanico", "", "")
        )

    def test_get_sponsor_names_full_name_cnpq(self):
        standard_names = [
	        ('Conselho Nacional de Desenvolvimento Científico e Tecnológico', 'CNPq'),
	        ('Coordenação de Aperfeiçoamento de Pessoal de Nível Superior', 'CAPES'),
	        ('Fundação de Amparo à Pesquisa do Estado de São Paulo', 'FAPESP')
	        ]
        name = "conselho nacional de desenvolvimento cientifico e tecnologico dprofix"
        self.assertEqual(
            sponsor.get_sponsor_names(name, standard_names),
            ("conselho nacional de desenvolvimento cientifico e tecnologico dprofix",
             "Conselho Nacional de Desenvolvimento Científico e Tecnológico", "CNPq")
        )

    def test_get_sponsor_names_full_name_capes(self):
        standard_names = [
            ('Conselho Nacional de Desenvolvimento Científico e Tecnológico', 'CNPq'),
            ('Coordenação de Aperfeiçoamento de Pessoal de Nível Superior', 'CAPES'),
            ('Fundação de Amparo à Pesquisa do Estado de São Paulo', 'FAPESP')
        ]
        name = "coordenacao e pessoal de nivel superior"
        self.assertEqual(
            sponsor.get_sponsor_names(name, standard_names),
            ("coordenacao e pessoal de nivel superior", "Coordenação de Aperfeiçoamento de Pessoal de Nível Superior", "CAPES")
        )

    def test_get_sponsor_names_full_name_fapesp(self):
        standard_names = [
            ('Conselho Nacional de Desenvolvimento Científico e Tecnológico', 'CNPq'),
            ('Coordenação de Aperfeiçoamento de Pessoal de Nível Superior', 'CAPES'),
            ('Fundação de Amparo à Pesquisa do Estado de São Paulo', 'FAPESP')
        ]
        name = "fundacao de amparo a pesquisa do estado de sao"
        self.assertEqual(
            sponsor.get_sponsor_names(name, standard_names),
            ("fundacao de amparo a pesquisa do estado de sao", "Fundação de Amparo à Pesquisa do Estado de São Paulo", "FAPESP")
        )

    def test_get_sponsor_names_acron_cnpq(self):
        standard_names = [
            ('Conselho Nacional de Desenvolvimento Científico e Tecnológico', 'CNPq'),
            ('Coordenação de Aperfeiçoamento de Pessoal de Nível Superior', 'CAPES'),
            ('Fundação de Amparo à Pesquisa do Estado de São Paulo', 'FAPESP')
        ]
        name = "cnPq"
        self.assertEqual(
            sponsor.get_sponsor_names(name, standard_names),
            ("cnpq", "Conselho Nacional de Desenvolvimento Científico e Tecnológico", "CNPq")
        )

    def test_get_sponsor_names_acron_capes(self):
        standard_names = [
            ('Conselho Nacional de Desenvolvimento Científico e Tecnológico', 'CNPq'),
            ('Coordenação de Aperfeiçoamento de Pessoal de Nível Superior', 'CAPES'),
            ('Fundação de Amparo à Pesquisa do Estado de São Paulo', 'FAPESP')
        ]
        name = "Capes"
        self.assertEqual(
            sponsor.get_sponsor_names(name, standard_names),
            ("capes", "Coordenação de Aperfeiçoamento de Pessoal de Nível Superior", "CAPES")
        )

    def test_get_sponsor_names_acron_fapesp(self):
        standard_names = [
            ('Conselho Nacional de Desenvolvimento Científico e Tecnológico', 'CNPq'),
            ('Coordenação de Aperfeiçoamento de Pessoal de Nível Superior', 'CAPES'),
            ('Fundação de Amparo à Pesquisa do Estado de São Paulo', 'FAPESP')
        ]
        name = "fapesp"
        self.assertEqual(
            sponsor.get_sponsor_names(name, standard_names),
            ("fapesp", "Fundação de Amparo à Pesquisa do Estado de São Paulo", "FAPESP")
        )

    def test_get_sponsor_names_without_match(self):
        standard_names = [
            ('Conselho Nacional de Desenvolvimento Científico e Tecnológico', 'CNPq'),
            ('Coordenação de Aperfeiçoamento de Pessoal de Nível Superior', 'CAPES'),
            ('Fundação de Amparo à Pesquisa do Estado de São Paulo', 'FAPESP')
        ]
        name = "fapesp cnpq pronex e conselho britanico"
        self.assertEqual(
            sponsor.get_sponsor_names(name, standard_names),
            None
        )
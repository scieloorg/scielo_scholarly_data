# SciELO Scholarly Data
This repository contains a set of tools responsible for processing scientific publication data (also known, in part, as **scholarly data**). The methods we develop cover standardization, normalization, and deduplication processes.

## Installation

### Installing as a library
```shell
pip install -e git+https://github.com/scieloorg/scielo_scholarly_data#egg=scielo_scholarly_data
```

### Installing as standalone application

_Create a virtual environment and install the application dependencies_
```shell
# Create a virtual environment
virtualenv -p python3 .venv

# Access the virtual environment
source .venv/bin/activated

# Install dependencies
pip install -r requirements.txt

# Install the package
python setup.py install
```

_Run tests_
```
python setup.py test
```


## Usage
This section presents examples of using the standardizer and core libraries.
```python
from scielo_scholarly_data import standardizer

# Standardize a journal title
standardizer.journal_title_for_deduplication('Agrociencia &amp;   (Uruguay)')
> 'agrociencia & uruguay'

standardizer.journal_title_for_visualization('Agrociencia   &amp; (Uruguay)')
> 'Agrociencia & (Uruguay)'

# Standardizer a journal ISSN
standardizer.journal_issn('1387666x')
> '1387-666X'

# Standardizer a issue volume
standardizer.issue_volume(' .15,b ')
> '15b'

# Standardizer a issue number
standardizer.issue_number(' 123 a. ')
> '123 a'

# Standardize a document DOI
standardizer.document_doi('&referrer=google*url=10.1590/1678-4766E2016006')
> '10.1590/1678-4766E2016006'

# Standardizer a document title
standardizer.document_title_for_deduplication(' INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE PROBLEMÁTICAS ')
> 'innovacion tecnologica en la resolucion de problematicas'

standardizer.document_title_for_visualization(' INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE PROBLEMÁTICAS ')
> 'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE PROBLEMÁTICAS'

# Standardizer a document page
standardizer.document_first_page('120-10')
> '120'

standardizer.document_last_page('120-10')
> '130'

# Standardizer a document elocation
standardizer.document_elocation('e*277$2%1@')
> 'e27721'

# Standardizer a document publication date
standardizer.document_publication_date('19 de nov de 2020')
> datetime.date(2020, 11, 19)

standardizer.document_publication_date('19 de nov de 2020', only_year=True)
> datetime.date(2020)

# Standardizer a document author
standardizer.document_author_for_deduplication('John Fitzgerald Kennedy')
> 'kennedy, john fitzgerald'

standardizer.document_author_for_deduplication('John Fitzgerald Kennedy', surname_first=True)
> 'kennedy, john fitzgerald'

standardizer.document_author_for_visualization('John Fitzgerald Kennedy')
> 'Kennedy, John Fitzgerald'

standardizer.document_author_for_visualization('John Fitzgerald Kennedy', surname_first=True)
> 'Kennedy, John Fitzgerald'

standardizer.book_title_for_deduplication('O MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI: &#60; APORTES PARA O DEBATE', remove_special_char=False)
> 'o modelo de desenvolvimento brasileiro das primeiras decadas do seculo xxi: < aportes para o debate'

standardizer.book_title_for_visualization('O MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI: &#60; APORTES PARA O DEBATE', remove_special_char=False)
> 'O MODELO DE DESENVOLVIMENTO BRASILEIRO DAS PRIMEIRAS DÉCADAS DO SÉCULO XXI: APORTES PARA O DEBATE'

from scielo_scholarly_data import core
# Remove accents from a text
core.remove_accents('Olá mundo')
> 'Ola mundo'

# Remove double spaces from a text
core.remove_double_spaces('This  is a  sentence')
> 'This is a sentence'

# Keeps only alphanumeric, numeric and space characters in a text
core.keep_alpha_num_space('This$ ° [is]+- a´ (sentence) that contains numbers 1, 2, 3')
> 'This     is    a   sentence  that contains numbers 1  2  3'

# Keeps only alphanumeric and space characters in a text
core.keep_alpha_space('This     is    a   sentence  that contains numbers 1  2  3')
> 'This     is    a   sentence  that contains numbers        '

# Remove non printable characteres from a text
core.remove_non_printable_chars('\nabc\t123')
> 'abc123'

# Remove end punctuation from a text
core.remove_end_punctuation_chars('abc123.,;')
> 'abc123'

# Remove parenthesis from a text
core.remove_parenthesis('abc (123)')
> 'abc'

# Convert a date to ISO format
core.convert_to_iso_date('20/feb/2021')
> datetime.date(2021, 2, 20)

core.convert_to_iso_date('2021')
> datetime.date(2021, 1, 1)

core.convert_to_iso_date('2021', month='06', day='15')
> datetime.date(2021, 6, 15)

core.check_sum_orcid('000000021694233X')
>True

```

## Documentation
This section aims to provide a scientific explanation about the decisions we made in our processing methods.

### Standardization processes
- book_editor_address
- book_editor_name
- book_title
- chapter_title
- document_author_for_deduplication
- document_author_for_visualization
- document_doi
- document_elocation
- document_first_page
- document_last_page
- document_publication_date
- document_title_for_deduplication
- document_title_for_visualization
- issue_number
- issue_volume
- journal_issn
- journal_number
- journal_title_for_deduplication
- journal_title_for_visualization
- journal_volume
- orcid_validator


### Normalization processes
`To do`

### Deduplication processes
`To do`

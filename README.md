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
# Standardize a journal title
from scielo_scholarly_data import standardizer

standardizer.journal_title('Revista Latino-Americana de Enfermagem')
> 'Revista Latino Americana de Enfermagem'

standardizer.journal_title('Agrociencia (Uruguay)', keep_parenthesis_content=False)
> 'Agrociencia'

# Standardize a document DOI
standardizer.document_doi('&referrer=google*url=10.1590/1678-4766E2016006')
> '10.1590/1678-4766E2016006'

# Remove accents from a text
from scielo_scholarly_data import core

core.remove_accents('Olá mundo')
> 'Ola mundo'

# Remove double spaces from a text
core.remove_double_spaces('This  is a  sentence')
> 'This is a sentence'
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


### Normalization processes
`To do`

### Deduplication processes
`To do`

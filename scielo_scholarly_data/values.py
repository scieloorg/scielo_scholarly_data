import re


PATTERN_PARENTHESIS = re.compile(r'[-a-zA-ZÀ-ÖØ-öø-ÿ|0-9]*\([-a-zA-ZÀ-ÖØ-öø-ÿ|\W|0-9]*\)[-a-zA-ZÀ-ÖØ-öø-ÿ|0-9]*', re.UNICODE)

# https://www.crossref.org/blog/dois-and-matching-regular-expressions/ (accessed on 2021/08/31)
PATTERNS_DOI = [re.compile(pd) for pd in [
    r'10.\d{4,9}/[-._;()/:A-Z0-9]+$',
    r'10.1002/[^\s]+$',
    r'10.\d{4}/\d+-\d+X?(\d+)\d+<[\d\w]+:[\d\w]*>\d+.\d+.\w+;\d$',
    r'10.1207/[\w\d]+\&\d+_\d+$']
]

# https://en.wikipedia.org/wiki/International_Standard_Serial_Number (accessed on 2021/08/31)
PATTERNS_ISSN = [re.compile(pi) for pi in [
    r'^[0-9]{4}[0-9]{3}[0-9xX]$',
    r'^[0-9]{4}-[0-9]{3}[0-9xX]$']
]

JOURNAL_TITLE_SPECIAL_CHARS = {
    '@',
    '&'
}

JOURNAL_TITLE_SPECIAL_WORDS = {
    'impresso',
    'print',
    'impreso',
    'online',
    'eletronico',
    'electronico',
    'cdrom'
}

DOCUMENT_TITLE_SPECIAL_CHARS = {

}

JOURNAL_STANDARDIZER_ARGS_DEDUPLICATION = {

}

PUNCTUATION_TO_REMOVE_FROM_TITLE_VISUALIZATION = {
    ',',
    '.',
    ';',
    ':'
}

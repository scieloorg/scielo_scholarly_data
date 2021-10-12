import re


PATTERN_PARENTHESIS = re.compile(r'[-a-zA-ZÀ-ÖØ-öø-ÿ|0-9]*\([-a-zA-ZÀ-ÖØ-öø-ÿ|\W|0-9]*\)[-a-zA-ZÀ-ÖØ-öø-ÿ|0-9]*', re.UNICODE)

PATTERN_DATE = r'(\d*)([a-zA-Z]*)(\d*)'

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
    ':',
    ' '
}

MONTHS_DICT = {
'janeiro':'01',
'jan':'01',
'fevereiro':'02',
'fev':'02',
'março':'03',
'mar':'03',
'abril':'04',
'abr':'04',
'maio':'05',
'mai':'05',
'junho':'06',
'jun':'06',
'julho':'07',
'jul':'07',
'agosto':'08',
'ago':'08',
'setembro':'09',
'set':'09',
'outubro':'10',
'out':'10',
'novembro':'11',
'nov':'11',
'dezembro':'12',
'dez':'12',
'enero':'01',
'febrero':'02',
'feb':'02',
'marzo':'03',
'mayo':'05',
'junio':'06',
'julio':'07',
'septiembre':'09',
'sept':'09',
'octubre':'10',
'oct':'10',
'noviembre':'11',
'diciembre':'12',
'dic':'12',
'january':'01',
'february':'02',
'march':'03',
'april':'04',
'apr':'04',
'may':'05',
'june':'06',
'july':'07',
'august':'08',
'aug':'08',
'september':'09',
'october':'10',
'november':'11',
'december':'12',
'dec':'12'
}


DATE_SEPARATORS = {
    '/',
    '.',
    ' ',
    '-'
}
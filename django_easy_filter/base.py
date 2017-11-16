HEADER = [
    'SKIP',
    'OFFSET',
    'SIZE',
    'LIMIT',
    'FILTER',
    'SORT'
]
FILTER = [
    '=',
    '==',
    '!=',
    '<',
    '>',
    '<=',
    '>=',
    '~='
]
CONNECT_FILTER = [
    'AND',
    'OR',
    '&&',
    '&',
    '|',
    '||'
]

OPERATION = FILTER + CONNECT_FILTER
from . import Grammar

grammar = Grammar()

s   = 's'
b   = 'b'
SCO  = 'SCO'
SCOR = 'SCOR'

grammar.rules = {
    s : [
        [b, SCOR],
    ],
    b : [
        [SCO, b, SCOR],
        []
    ]
}

grammar.start_symbol = s
grammar.term = frozenset([SCO,SCOR])
grammar.nonterm = frozenset([s, b])
grammar.nullable = [b]

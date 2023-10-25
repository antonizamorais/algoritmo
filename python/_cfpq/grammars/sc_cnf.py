from . import Grammar

grammar = Grammar()

s   = 's'
s1 = 's1'
s2 = 's2'
b = 'b'
b1 = 'b1'
SCO  = 'SCO'
SCOR = 'SCOR'

grammar.rules = {
    s : [
        [b, s2],
    ],
    b : [
        [s1, b1],
        []
    ],
    b1 : [
        [b, s2],
    ],
    s1 : [[SCO]],
    s2 : [[SCOR]],
}

grammar.start_symbol = s
grammar.term = frozenset([SCO,SCOR])
grammar.nonterm = frozenset([s, s1,s2, b,b1])
grammar.nullable = [b]


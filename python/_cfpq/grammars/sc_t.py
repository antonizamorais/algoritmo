#-*- coding:utf-8 -*-
'''
Grammar
--------------
s -> SCO s SCOR
s -> T s TR
s -> SCO SCOR
s -> T TR
'''

from . import Grammar

T  = 'T'
TR = 'TR'
SCO  = 'SCO'
SCOR = 'SCOR'

grammar = Grammar()

s = 's'

grammar.rules = {
    s: [
        [SCO,s,SCOR],
        [T,s,TR],
        [SCO,SCOR],
        [T,TR]
    ]
}

grammar.start_symbol = s
grammar.term = frozenset([T,TR,SCO,SCOR])
grammar.nonterm = [s]
grammar.nullable = []

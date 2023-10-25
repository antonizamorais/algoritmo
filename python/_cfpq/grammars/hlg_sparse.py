#-*- coding:utf-8 -*-
'''
Grammar in CNF
--------------
b -> b a
b -> a b
b -> ''

a -> A

Try this grammar at http://jsmachines.sourceforge.net/machines/ll1.html
'''
from . import Grammar

grammar = Grammar()

a = 'a'
b = 'b'

A = 'A'

grammar.start_symbol = b

grammar.T = {
    b : {
        A : [
            (b,a),
            (a,b)
        ]
    },
}

grammar.cnfrules = [
    [b,b,a],
    [b,a,b],
    [b],
    [a,A],
]

grammar.rules = {
    b : [
        [b,a],
        [a,b],
        []
    ],
    a : [A]
}
grammar.term = set([A])
grammar.nonterm = set([a,b])
grammar.nullable = set([b])

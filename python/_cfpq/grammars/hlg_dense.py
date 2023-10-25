#-*- coding:utf-8 -*-
'''
Grammar in CNF
--------------
a -> a a
a -> A


Try this grammar at http://jsmachines.sourceforge.net/machines/ll1.html
'''
from . import Grammar

grammar = Grammar()

a = 'a'
A = 'A'

grammar.start_symbol = a

grammar.T = {
    a : {
        A : [(a,a)]
    },
}

grammar.brules = {
    a : [a,a]
}

grammar.urules = {
    a : [A]
}

grammar.cnfrules = [
    [a,a,a],
    [a,A]
]

grammar.rules = {
    a : [
        [a,a],
        [A]
    ]
}
grammar.term = set([A])
grammar.nonterm = set([a])
grammar.nullable = set()

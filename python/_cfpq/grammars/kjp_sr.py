#-*- coding:utf-8 -*-
'''
Grammar in CNF
--------------
s -> s a
s -> ''
a -> A

Try this grammar at http://jsmachines.sourceforge.net/machines/ll1.html
'''
from . import Grammar

grammar = Grammar()

s = 's'
a = 'a'
A = 'A'

grammar.T = {
    s : {
        A : [
            (s,a)
        ]
    },
}

grammar.cnfrules = [
    [s,s,a],
    [s],
    [a,A],
]

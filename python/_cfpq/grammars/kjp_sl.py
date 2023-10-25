#-*- coding:utf-8 -*-
'''
Grammar in CNF
--------------
s -> a s
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
            (a,s)
        ]
    },
}

grammar.cnfrules = [
    [s,a,s,],
    [s],
    [a,A]
]

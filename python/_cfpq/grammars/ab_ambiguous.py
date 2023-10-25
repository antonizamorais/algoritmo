#-*- coding:utf-8 -*-
'''
Grammar in CNF
--------------
s -> ''
s -> a s2
s -> s s

s2 -> s b

a -> A
b -> B

Try this grammar at http://jsmachines.sourceforge.net/machines/ll1.html
'''
from . import Grammar

grammar = Grammar()

s = 's'
s2 = 's2'
a = 'a'
b = 'b'

A = 'A'
B = 'B'

grammar.cnfrules = [
    [s,s,s],
    [s,a,s2],
    [s],

    [s2,s,b],

    [a,A],
    [b,B]
]

grammar.T = {
    s : {
        A : [(s,s), (a,s2)],
        B : [(s,s), ]
    },

    s2 : {
        A : [(s,b)],
        B : [(s,b)]
    }
}

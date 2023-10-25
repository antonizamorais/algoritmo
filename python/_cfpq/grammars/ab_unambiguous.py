#-*- coding:utf-8 -*-
'''
Grammar in CNF
--------------
s -> a s2
s -> ''
s2 -> s s3
s3 -> b s

a -> A
b -> B

Try this grammar at http://jsmachines.sourceforge.net/machines/ll1.html
'''
from . import Grammar

grammar = Grammar()

s  = 's'
s2 = 's2'
s3 = 's3'
a = 'a'
b = 'b'
A = 'A'
B = 'B'

grammar.T = {
    s : {
        A : [(a,s2)]
    },
    s2 : {
        A : [(s,s3)],
        B : [(s,s3)],
    },
    s3 : {
        B : [(b,s)]
    },
}

grammar.cnfrules = [
    [s,a,s2],
    [s],

    [s2,s,s3],

    [s3,b,s],

    [a,A],
    [b,B],
]

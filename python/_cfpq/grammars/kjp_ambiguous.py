'''
Grammar in CNF
--------------
s -> s s
s -> A
s -> B
s -> C
s -> D

Try this grammar at http://jsmachines.sourceforge.net/machines/ll1.html
'''
from . import Grammar

grammar = Grammar()

s = 's'
A = 'A'
B = 'B'
C = 'C'
D = 'D'

grammar.cnfrules = [
    [s,s,s],
    [s,A],
    [s,B],
    [s,C],
    [s,D]
]

grammar.T = {
    s : {
        A : [(s,s)],
        B : [(s,s)],
        C : [(s,s)],
        D : [(s,s)],
    },
}

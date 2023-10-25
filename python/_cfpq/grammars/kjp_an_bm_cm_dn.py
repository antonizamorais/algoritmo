'''
Grammar in CNF
--------------
s -> a s2
s -> a s3
s2 -> s d
s3 -> x d

x -> b x2
x -> ''
x2 -> x c

a -> A
b -> B
c -> C
d -> D


Try this grammar at http://jsmachines.sourceforge.net/machines/ll1.html
'''
from . import Grammar

grammar = Grammar()

s = 's'
s2 = 's2'
s3 = 's3'
x = 'x'
x2 = 'x2'
a = 'a'
b = 'b'
c = 'c'
d = 'd'
A = 'A'
B = 'B'
C = 'C'
D = 'D'

grammar.cnfrules = [
    [s,a,s2],
    [s,a,s3],
    [s2,s,d],
    [s3,x,d],

    [x,b,x2],
    [x],
    [x2,x,c],

    [a,A],
    [b,B],
    [c,C],
    [d,D],
]

grammar.T = {
    s : {
        A : [(a,s2),(a,s3)],
    },
    s2 : {
        A : [(s,d)],
        D : [(x,d)]
    },
    s3 : {
        B : [(x,d)],
        D : [(x,d)],
    },
    x : {
        B : [(b,x2)],
    },
    x2 : {
        B : [(x,c)],
        C : [(x,c)],
        D : [(x,c)],
    },
}

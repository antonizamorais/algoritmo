'''
Grammar in CNF
--------------
s -> a s2
s2 -> p ar

p -> a p2
p2 -> p ar
p -> a p3
p3 -> m ar

m -> x m2
m2 -> x m3
m3 -> x x

a -> A
ar -> AR

x -> B
x -> C
x -> D

Try this grammar at http://jsmachines.sourceforge.net/machines/ll1.html
'''
from . import Grammar

grammar = Grammar()

s  = 's'
s2 = 's2'
p  = 'p'
p2 = 'p2'
p3 = 'p3'
m  = 'm'
m2 = 'm2'
m3 = 'm3'
a  = 'a'
ar = 'ar'
x = 'x'

A  = 'A'
AR = 'AR'
B  = 'B'
C  = 'C'
D  = 'D'

grammar.T = {
    s : {
        A : [(a,s2)],
    },
    s2 : {
        A : [(p,ar)],
    },
    p : {
        A : [(a,p2), (a,p3)],
    },
    p2 : {
        A : [(p,ar)],
    },
    p3 : {
        B : [(m,ar)],
        C : [(m,ar)],
        D : [(m,ar)],
    },
    m : {
        B : [(x,m2)],
        C : [(x,m2)],
        D : [(x,m2)],
    },
    m2 : {
        B : [(x,m3)],
        C : [(x,m3)],
        D : [(x,m3)],
    },
    m3 : {
        B : [(x,x)],
        C : [(x,x)],
        D : [(x,x)],
    },
}

grammar.cnfrules = [
    [s,a,s2],
    [s2,p,ar],

    [p,a,p2],
    [p2,p,ar],
    [p,a,p3],
    [p3,m,ar],

    [m,x,m2],
    [m2,x,m3],
    [m3,x,x],

    [a,A],
    [ar,AR],

    [x,B],
    [x,C],
    [x,D],
]

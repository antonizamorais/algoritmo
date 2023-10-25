#-*- coding:utf-8 -*-
'''
Grammar in CNF
--------------
s -> s1 s5
s -> s1 s2
s -> s3 s6
s -> s3 s4

s5 -> s s2
s6 -> s s4

s1 -> SCO
s2 -> SCOR
s3 -> T
s4 -> TR

Try this grammar at http://jsmachines.sourceforge.net/machines/ll1.html
'''

from . import Grammar

T  = 'T'
TR = 'TR'
SCO  = 'SCO'
SCOR = 'SCOR'

grammar = Grammar()

s = 's'
s1 = 's1'
s2 = 's2'
s3 = 's3'
s4 = 's4'
s5 = 's5'
s6 = 's6'

grammar.cnfrules = [
    [s,s1,s5],
    [s,s1,s2],
    [s,s3,s6],
    [s,s3,s4],

    [s5,s,s2],

    [s6,s,s4],

    [s1, SCO],
    [s2, SCOR],
    [s3, T],
    [s4, TR],
]

grammar.T = {
    s : {
        SCO : [(s1,s5),(s1,s2)],
        T :[(s3,s6),(s3,s4)]
    },

    s5 : {
        T : [(s,s2)],
        SCO : [(s,s2)]
    },

    s6 : {
        T : [(s,s4)],
        SCO : [(s,s4)]
    }
}

grammar.rules = {
    s : [
        [s1,s5],
        [s1,s2],
        [s3,s6],
        [s3,s4],
    ],

    s5 : [[s,s2]],

    s6 : [[s,s4]],

    s1 : [[SCO]],
    s2 : [[SCOR]],
    s3 : [[T]],
    s4 : [[TR]],
}

grammar.start_symbol = s
grammar.term = frozenset([T,TR,SCO,SCOR])
grammar.nonterm = frozenset([s,s1,s2,s3,s4,s5,s6])
grammar.nullable = []

#-*- coding:utf-8 -*-
'''
Grammar in CNF
--------------
s -> bt s2
s2 -> s btr
s -> bt btr

bt -> BT
btr -> BTR

Try this grammar at http://jsmachines.sourceforge.net/machines/ll1.html
'''
from . import Grammar

grammar = Grammar()

s   = 's'
s2  = 's2'
bt  = 'bt'
btr = 'btr'

BT  = 'BT'
BTR = 'BTR'

grammar.T = {
    s : {
        BT : [(bt,s2), (bt,btr)]
    },
    s2 : {
        BT : [(s,btr)],
    },
}

grammar.cnfrules = [
    [s,bt,s2],
    [s,bt,btr],
    [s2,s,btr],
    [bt, BT],
    [btr, BTR]
]

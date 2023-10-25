#-*- coding:utf-8 -*-
'''
Grammar in CNF
--------------
S ^result [I] [F] [T] ^mutation S2 mutation [I] [F] [T] result
S ^result [I] [F] [T] ^mutation mutation [I] [F] [T] result
S2 ^result ^mutation S2 mutation result
S2
I index self::1
F from self::A
T to self::B
'''
from . import Grammar

grammar = Grammar()

S  = 'S'
S2 = 'S2'
I = 'I'
F = 'F'
T = 'T'

index = 'index'
index_ = '^index'
mutation = 'mutation'
mutation_ = '^mutation'
result = 'result'
result_ = '^result'
self1 = 'self::1'
fromm = 'from'
selfA = 'self::A'
to = 'to'
selfB = 'self::B'


grammar.rules = {
    S : [[result_, '[I]','[F]','[T]',mutation_, S2, mutation, '[I]', '[F]', '[T]' result],
        [result_, '[I]','[F]','[T]',mutation_, mutation, '[I]', '[F]', '[T]' result]],
    S2 : [[result_, mutation_, S2, mutation, result], []]
    I : [[index, self1]],
    F : [[fromm, selfA]],
    T : [[to, selfB]]
}

grammar.start_symbol = S
grammar.term = set([index, index_, mutation, mutation_, result, result_, self1,
    selfA, selfB, fromm, to])
grammar.nonterm = set([S,S2,I,F,T])
grammar.nullable = set([S2])

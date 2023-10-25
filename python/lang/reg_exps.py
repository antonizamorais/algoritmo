#-*- coding:utf-8 -*-
SPACES = 'SPACES'
NEW_LINE = 'NEW_LINE'
RULE_DEF = 'RULE_DEF'
URI = 'URI'
ID = 'ID'
FLOAT = 'FLOAT'
INTEGER = 'INTEGER'
STRING = 'STRING'
OR = 'OR'
EOI = '$'
DOT = 'DOT'

rules = [
    (r'\.', DOT),
    (r' +', SPACES),
    (r'\n', NEW_LINE),
    (r':\-', RULE_DEF),
    (r'\|', OR),
    (r'[A-z]\w*:\S+', URI), # naive URI pattern
    (r'[A-z]\w*', ID),
    #(r'\d+\.\d+', FLOAT),
    #(r'\d+', INTEGER),
    (r'(?P<quote>[\'"]).*?(?P=quote)', STRING)
]


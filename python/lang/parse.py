#-*- coding:utf-8 -*-
"""
Test this grammar at http://jsmachines.sourceforge.net/machines/ll1.html
R -> ID :- B
R -> ''

B -> URI B
B -> ID B
B -> | B
B -> . R
"""

from reg_exps import *

def parse(tokens):
    p = LLParser(tokens)
    p.R()
    if len(p.tokens) > 0:
        print 'stack not empty'

class UnexpectedTokenError(Exception):
    """ Unexpected token error exception.
        found:
            Token found on input.
        expected:
            List of expected tokens.
    """
    def __init__(self, pos, found, expected):
        self.pos = pos
        self.found = found
        self.expected = expected
    

class UnexpectedEndOfInputError(Exception):
    """ Unexpected end of input error exception.
    """
    pass


class LLParser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok = self.tokens.pop(0)
        print self.tok,

    def eat(self, t):
        if self.tok != None:
            if self.tok.type == t:
                print ',',self.tok,
                if len(self.tokens) > 0:
                    self.tok = self.tokens.pop(0)
                else:
                    self.tok = None
            else:
                self.error(self.tok.pos, self.tok.type, t)
        else:
            self.error_ueoi()

    def R(self):
        '''Rule'''
        if self.tok == None: # end of input
            return
        if self.tok.type == ID:
            self.eat(ID); self.eat(RULE_DEF); self.B()
        else:
            self.error(self.tok.pos, self.tok, [ID, EOI])

    def B(self):
        '''Body of a rule'''
        if self.tok == None:
            self.error_ueoi()
            return
            
        if self.tok.type == URI:
            self.eat(URI); self.B()
        elif self.tok.type == ID:
            self.eat(ID); self.B()
        elif self.tok.type == OR:
            self.eat(OR); self.B()
        elif self.tok.type == DOT:
            self.eat(DOT); self.R()
        else:
            self.error(self.tok.pos, self.tok, [URI, ID, OR, DOT])
    
    def error(self, pos, found, expected):
        '''Unexpected token error
        '''
        raise UnexpectedTokenError(pos, found, expected)
    
    def error_ueoi(self):
        '''Unexpected end of input error.
        '''
        raise UnexpectedEndOfInputError()

if __name__ == '__main__':
    import lex
    tt = lex.tokenize_as_list(open('gram.llq').read())
    try:
        parse(tt)
    except UnexpectedTokenError as err:
        print 'Unexpected token %s at %d (expected %s)' % (err.found, err.pos,
            err.expected)
    except UnexpectedEndOfInputError:
        print 'Unexpected end of input.'
        

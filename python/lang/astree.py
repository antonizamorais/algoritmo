#-*- coding:utf-8 -*-
class ASTree:
    def __init__(self, cargo, children=[]):
        self.cargo = cargo
        self.children = children

    def __str__(self):
        return str(self.cargo)
    
    def add(self, child):
        self.children.append(child)
    
    def show(self):
        print self
        for node in children:
            node.show()
#class Tree:
#    def __init__(self, root=None):
#        self.root = root
        
    

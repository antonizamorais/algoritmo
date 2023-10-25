#-*- coding:utf-8 -*-
class GSS:
    '''Simple GSS'''
    def __init__(self):
        self.roots = []

    def add(self, new):
        self.roots.append(new)

    def show(self):
        for node in self.roots:
            node.show(level=0)

class GSSNode:
    def __init__(self, node, state, parent=None):
        self.parent   = parent
        self.node     = node
        self.state    = state
        self.children = []
        
    def add(self, node, state):
        new = GSSNode(node, state, self)
        self._add_node(new)

    def _add_node(self, gss_node):
        self.children.append(gss_node)

    def show(self,level=0):
        print self.node,self.state,'\t',
        for c in self.children:
            c.show(level+1)
            print (level+1)*'\t',
        print ''

    def up(self, n):
        p = self
        for i in range(n):
            p = p.parent
        return p

    def unpack(self):
        return self.node, self.state

if __name__ == '__main__':
    gss = GSS()
    a = 'a'
    b = 'b'
    c = 'c'
    d = 'd'
    e = 'e'
    f = 'f'
    
    a0 = GSSNode(a,0)
    b2 = GSSNode(b,2,a0)
    c4 = GSSNode(c,4,b2)

    a0._add_node(b2)
    a0.add(a,1)
    b2._add_node(c4)
    b2.add(f,3)
    c4.add(b,4)
    c4.add(d,4)
    
    gss.add(a0)

    gss.show()
    print c4.up(0).node,c4.up(0).state
    print c4.up(1).node,c4.up(1).state
    print c4.up(2).node,c4.up(2).state
    
    
    
    

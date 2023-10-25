#-*- coding:utf-8 -*-
from graphlib import Graph
from gss import *
from experiments.grammars.util import *

DBG_LEVEL = 1

""" Evaluation Algorithm """
def _build_base_graph(graph, grammar):
    '''Builds a graph with edges restricted to the alphabet.'''
    D = Graph() 
    for p in grammar.ALPHABET:
        if p.endswith(OP_INV) == False:
            for s,o in graph.subject_objects(p):
                D.add(s,p,o)
        else:
            for o,_,s in graph.subject_objects(p[:-len(OP_INV)]):
                D.add(s,p,o)
    for s in graph.all_subjects():
        D.add(s,EOF,o)
    return D

def lr_processor(D, G, dscru):
    dscrm = {} # marked pairs (nodo, state)
    res   = Graph() # results set

    while len(dscru) > 0 > 0:
        if len(dscru) > 0:
            gss_node = dscru.pop(); assert type(gss_node) == GSSNode, 'erro de tipos'
            (x,s) = gss_node.unpack()
            _dbg('picked from dscru',(x.split('#')[-1],s))
            attach(dscrm,x,s)
            # 'shift' states
            shifts = G.shifts.get(s,{})
            for p in shifts:
                assert type(p) == str, 'erro de tipos'
                for y in D.objects(x,p):
                    #for ss in shifts[p]:
                        ss = shifts[p]
                        assert type(ss) == int, 'erro de tipos'
                        if ss not in states(dscrm,y):
                            dscru.add((y,ss)); _dbg('added',(y,ss),'to dscru')
                        else:
                            pass #TODO: fazer alguma coisa aqui?
            # 'reduce' states
            #for i in G.reduces.get(s,[]):
            i = G.reduces.get(s,[])
            '''go up in the stack'''
                
                    
                    
            # 'goto' states
            for N in G.gotos.get(s,{}):
                assert type(N) == str, 'erro de tipos'
                for y in res.objects(x,N):
                    #for ss in G.gotos.get(s,{})[N]:
                        ss = G.gotos.get(s,{})[N]
                        assert type(ss) == int, 'erro de tipos'
                        if ss not in states(dscrm,y):
                            dscru.add((y,ss)); _dbg('added',(y,ss),'to dscru')
                        else:
                            '''
                            pra cada tripla (y,X,z) e sss in T(ss,Y):
                                
                                
                            '''
                            _dbg('entrou no else')
    
    for x in dscrm:
        print x.split('#')[-1],': ',
        for s in dscrm[x]:
            print s,
        print ''
             
    for s,p,o in res.subject_objects(G.START_SYMBOL):
        print s.split('#')[-1],p.split('#')[-1],o.split('#')[-1]
    print 'dscru =',dscru
    return res

def attach(dscrm,x,s):
    if x not in dscrm:
        dscrm[x] = set()
    if s not in dscrm[x]:
        dscrm[x].add(s)
    else:
        raise 'duplicated state:'+x+' '+str(s)

def states(dscrm,x):
    return dscrm.get(x,[])

def _dbg(*text):
    if DBG_LEVEL > 0:
        print text

""" MAIN PROGRAM """    
if __name__ == '__main__':
    from itertools import product
    from time import clock
    from experiments.grammars.util import *
    # helper function to get time in milliseconds
    now = lambda: int(round(clock() * 1000))
    
    #~ from experiments.grammars.g2 import grammar
    
    #~ graph = Graph()
    #~ n1 = 'n1'
    #~ n2 = 'n2'
    #~ n3 = 'n3'
    #~ n4 = 'n4'
    #~ n5 = 'n5'

    #~ graph.add(n1,sc,n4)
    #~ graph.add(n2,sc,n4)
    #~ graph.add(n3,sc,n4)
    #~ graph.add(n4,sc,n5)
    #~ D = _build_base_graph(graph, grammar)
    #~ pairs = set(product(set(D.subjects()), [0]))
    #~ res = lr_processor(D,grammar,pairs)
    #~ for s,p,o in res:
        #~ print s,p,o
        
    graph = Graph()
    eld = 'elderly'
    adt = 'adult'
    drv = 'driver'
    per = 'person'
    anm = 'animal'
    shp = 'sheep'
    tbd = 'tabloid'
    nws = 'newspaper'
    pub = 'publication'
    gir = 'giraffe'
    tre = 'tree'
    plt = 'plant'
    grs = 'grass'
    cow = 'cow'
    veg = 'vegetarian'
    brd = 'broadsheet'
    thg = 'thing'
    bra = 'brain'
    vhc = 'vehicle'
    mle = 'male'
    fem = 'female'
    man = 'man'
    wvm = 'white van man'

    #~ graph.add(adt,sc,thg)
    #~ graph.add(mle,sc,thg)
    #~ graph.add(anm,sc,thg)
    graph.add(man,sc,anm)
    #~ graph.add(man,sc,adt)
    #~ graph.add(wvm,sc,man)
    graph.add(man,sc,per)
    graph.add(per,sc,anm)
    #~ graph.add(,sc,)
    #~ graph.add(,sc,)
    #~ graph.add(,sc,)
    #~ graph.add(,sc,)
    #~ graph.add(,sc,)
    #~ graph.add(,sc,)
    #~ graph.add(,sc,)
    #~ graph.add(,sc,)
    #~ graph.add(,sc,)
    #~ graph.add(,sc,)
    #~ graph.add(eld,sc,adt)
    #~ graph.add(drv,sc,adt)
    #~ graph.add(per,sc,anm)
    #~ graph.add(gir,sc,anm)
    #~ graph.add(shp,sc,anm)
    #~ graph.add(cow,sc,veg)
    #~ graph.add(tre,sc,plt)
    #~ graph.add(brd,sc,nws)
    #~ graph.add(nws,sc,pub)
    #~ graph.add(tbd,sc,pub)
    #~ graph.add(grs,sc,plt)
    
    #~ graph.parse('experiments/data/people_pets.rdf')

    #~ from experiments.grammars.g2 import grammar
    
    #~ D = _build_base_graph(graph, grammar)

    #~ from experiments.grammars.g_xyz import grammar
    #~ graph2 = Graph()
    #~ y = 'y'
    #~ z = 'z'
    #~ n1 = 'n1'
    #~ n2 = 'n2'
    #~ n3 = 'n3'
    #~ n4 = 'n4'
    
    #~ graph2.add(n1,y,n3)
    #~ graph2.add(n2,y,n3)
    #~ graph2.add(n3,z,n4)

    
    #~ D = _build_base_graph(graph2, grammar)
    #~ for s,p,o in D:
        #~ print s,p,o

    from experiments.grammars.g0u_lr import grammar
    a = 'a'
    b = 'b'

    n1 = 'n1'
    n2 = 'n2'
    n3 = 'n3'
    n4 = 'n4'

    graph = Graph()
    graph.add(n1,a,n2)
    graph.add(n2,a,n3)
    graph.add(n3,b,n4)

    D = _build_base_graph(graph, grammar)
    for s,p,o in D:
        print s,p,o
    
    pairs = set(product(set(D.all_subjects()), [0]))

    start = now()
    res = lr_processor(D,grammar,pairs)
    count=0
    for s,p,o in res.subject_objects(grammar.START_SYMBOL):
        print s,p,o
        count+=1
    t = now()-start
    print count, 'results'
    print t, 'ms'
    

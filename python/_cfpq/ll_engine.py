#-*- coding:utf-8 -*-
from graph import Graph
from util import _get_memory, _get_time, load_grammar, quick_load_graph,\
    print_exp_data

""" Evaluation Algorithm """
def processor(graph, G, newv):
    start = _get_time()
    res = graph   # _build_base_graph(graph, G)
    sta = {}      # states' hash structure
    vis = set()   # visited vertices
    newr = set()  # new results
    news = set()  # new states

    while len(newr) > 0 or len(newv) > 0 or len(news) > 0:
        if len(newv) > 0:
            (x,N) = newv.pop()
            vis.add((x,N))
            if N.startswith('[') and N.endswith(']') and (x,URIRef(N[1:-1])) not in vis: # N is a nested non-terminal
                newv.add((x,URIRef(N[1:-1]))) # (x, N)
            else: # N is a non-terminal
                if (N in G.nullable) and ((x,N,x) not in res):
                    newr.add((x,N,x))
                for s in G.urules.get(N,{}):
                    for y in res.objects(x,s):
                        newr.add((x,N,y))
                for p in res.predicates(x,None):
                    for rhs in G.T.get(N,{}).get(p,[]):
                        news.add((x,N,rhs,0)) # (x, N-> .MO)
        if len(news) > 0:
            (x,S,rhs,i) = news.pop()
            if (x,rhs[i]) not in vis:
                newv.add((x,rhs[i]))
            save_state(x,S,rhs,i,sta)
            for y in res.objects(x,rhs[i]):

                if i == 1:
                    for w in res.subjects(rhs[i-1], x):
                        if (w,S,y) not in res:
                            newr.add((w,S,y))
                elif i == 0:
                    if (rhs,i+1) in sta.get(y,{}).get(S,[]):
                        for z in res.objects(y,rhs[i+1]):
                            if (x,S,z) not in res:
                                newr.add((x,S,z))
                    else:
                        news.add((y,S,rhs,i+1))
        if len(newr) > 0:
            (x,N,y) = newr.pop()
            res.add(x,N,y)
            if (x,'['+N+']') in vis:
                newr.add((x,'['+N+']',x))
            for (S,rhs,i) in states(x,N,sta):
                if i == 0:
                    if (rhs,i+1) in sta.get(y,{}).get(S,[]):
                        for z in res.objects(y,rhs[i+1]):
                            if (x,S,z) not in res:
                                newr.add((x,S,z))
                    else:
                        news.add((y,S,rhs,i+1))
                elif i == 1:
                    for w in res.subjects(rhs[i-1],x):
                        if (w,S,y) not in res:
                            newr.add((w,S,y))
    duration = _get_time() - start
    return res, duration, _get_memory()

def states(n,X,sta):
    if n in sta:
        temp = sta[n]
        for S in temp:
            for (rhs,i) in temp[S]:
                if X == rhs[i]:
                    yield S,rhs,i

def save_state(n,S,rhs,i,sta):
    if n not in sta:
        sta[n] = {}
    if S not in sta[n]:
        sta[n][S] = []
    if (rhs,i) not in sta[n][S]:
        sta[n][S].append((rhs,i))
    else:
        print('Estado duplicado')
        quit()

""" MAIN PROGRAM """

if __name__ == '__main__':
    # from experiments.grammars.g1 import grammar
    from itertools import product
    import sys

    args = sys.argv[1:]

    assert len(args)==2, 'Usage: '+sys.argv[0]+' <grammar> <path/to/graph>'

    grammar = args[0]
    graph   = args[1]

    G = load_grammar(grammar)
    D = quick_load_graph(graph, Graph(), G)
    Q = set(product(D.all_nodes(), [G.start_symbol]))

    r,t,m = processor(D, G, Q)

    rescount = 0
    for s,o in r.subject_objects(G.start_symbol):
        rescount += 1
    assert rescount == len(list(r.subjct_objects(G.start_symbol))), 'different result counts'

    print(True, grammar, graph, len(set(D.all_nodes())), len(D),
        rescount, t, '%.2f'%(m), sep='\t')

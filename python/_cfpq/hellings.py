#-*- coding:utf-8 -*-
from rdflib import Graph, URIRef, Literal
from experiments.grammars.util import OP_INV

def _build_base_graph(D, G):
    """ Builds the base graph r to run the algorithms. For each rule in
    the form A -> a, if there is an edge (n,a,m) in the original graph,
    the edge (n,A,m) is added to the new graph. Besides that, for each
    nullable non terminal A, the edge (n,A,n) is added to the new graph
    for each resource n.
    :params:
        D: The original graph. An rdflib.Graph.
    :returns:
        r. An rdflib.Graph.
    """
    r = Graph()
    # Adding A -> a edges
    for A in G.urules:
        for a in G.urules[A]:
            if a.endswith(OP_INV) == False:
                for s,o in D.subject_objects(a):
                    r.add((s,A,o))
            else:
                for o,s in D.subject_objects(URIRef(a[:-len(OP_INV)])):
                    r.add((s,A,o))
    # Adding A -> '' edges
    for A in G.nullable:
        for n in D.all_nodes():
            r.add((n,A,n))
    return r


def hellings(D, G):
    """ Completes the graph D.

    :params:
        D: an rdflib.Graph.

    This is an implementation of the algorithm proposed in:
    Jelle Hellings. 2014. Conjunctive Context-Free Path Queries. In
    Proc. 17th International Conference on Database Theory (ICDT),
    Athens, Greece, March 24-28, 2014, Nicole Schweikardt, Vassilis
    Christophides, and Vincent Leroy (Eds.) OpenProceedings.org,
    119-130. DOI: http://dx.doi.org/10.5441/002/icdt.2014.15
    """
    r = _build_base_graph(D, G)

    # Duplicates the triples of 'r'
    New = set(r).copy()
    while len(New) > 0:
        (n,N,m) = New.pop()
        for (nn,M) in r.subject_predicates(n):
            for NN in G.brules:
                if (nn,NN,m) not in r:
                    for (X,Y) in G.brules.get(NN,[]):
                        if (X,Y) == (M,N):
                            New.add((nn,NN,m))
                            r.add((nn,NN,m))
        for (M,mm) in r.predicate_objects(m):
            for MM in G.brules:
                if (n,MM,mm) not in r:
                    for (X,Y) in G.brules.get(MM,[]):
                        if (X,Y) == (N,M):
                            New.add((n,MM,mm))
                            r.add((n,MM,mm))
    return r

""" MAIN PROGRAM """

if __name__ == '__main__':
    from experiments.grammars.g1_yrd import grammar
    import time

    graph = Graph()
    graph.parse('experiments/data/skos.rdf')
    start = time.time()
    r = hellings(graph,grammar)
    print time.time()-start

    c = 0
    for s,p,o in r.triples((None,URIRef('S'),None)):
        c+=1

    print c,'results'

#!/usr/bin/env python3

'''
Context-free path query evaluation module.
Use this script as a CLI program to run CFPQs or import it as a python module.
'''

import gc
from itertools import product
from sys import argv

from _cfpq.grammars import Grammar
from _cfpq.TraceItemsCFPQEngine import TraceItemsCFPQEngine
from graphs import Graph
from provenance import Provenance


if __name__ == '__main__':
    engine = None
    grammar = None
    graph = None
    prov = None 
    try:
        grammar = Grammar.load(argv[1])
        graph = Graph.load(argv[2])
        #Colocar um terceiro argumento: grafo de proveniência
        prov = Provenance.open(argv[3])
        query = set(product(graph.all_nodes(), [grammar.start_symbol]))
        # TODO: receive CFPQEngine class as input
        #Passar o grafo de proveniência para o algoritmo
        engine = TraceItemsCFPQEngine(grammar, graph, prov, query)
    except IndexError:
        # TODO: receive CFPQEngine class as input
        print('Usage:', argv[0],
              'grammar.yrd graph.txt provenance.json')
        quit(-1)
    engine.run_experiment()


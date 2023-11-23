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
    if len(argv) != 5:
        # TODO: receive CFPQEngine class as input
        print('Usage:', argv[0], 'grammar.yrd graph.txt provenance.json requisito.txt')
        quit(-1)

    engine = None
    grammar = None
    graph = None
    provenance = None 

    grammar = Grammar.load(argv[1])
    graph = Graph.load(argv[2])
    # Terceiro argumento: grafo de proveniência .json
    provenance = Provenance.load(argv[3])
    # Quarto argumento: Requisito .txt
    requisito = Provenance.loadReq(argv[4])
    query = set(product(graph.all_nodes(), [grammar.start_symbol]))
    # TODO: receive CFPQEngine class as input
    #Passar o grafo de proveniência para o algoritmo
    engine = TraceItemsCFPQEngine(grammar, graph, provenance, requisito, query)

    engine.run_experiment()


"""
Synthetic database generator functions.
"""

import random
import sys


def complete(n):
    """
    Generates a complete graph with n nodes and a minimum cycle.
    Edge labels are randomly chosen from {A, B, ..., J}.
    Edge weights are randomly chosen from {1, 2, ..., 10}.
    The minimum cycle is a cycle connecting all vertices where all edges have
    weight 1.
    """
    n = int(n)
    predicates = 'A B C D E F G H I J'.split(' ')
    weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    graph = []
    for i in range(1, n+1):
        s = str(i)
        for j in range(1, n+1):
            o = str(j)
            # random.shuffle(weights)
            for k in range(len(predicates)):
                p = predicates[k]
                w = weights[k]
                graph += [[s, p, o, w]]
    _to_file(graph)
    return graph


def _to_file(D):
    for s, p, o, w in D:
        print(str(s)+" "+str(p)+" "+str(o)+" "+str(w))


def sierpinski(degree, predicates='A B C D E', weights=[1, 2, 3, 4, 5]):
    """ Generates a Sierpinski Triangle graph. """

    def gen_sierpinski(t, l, r, deg, g):
        ''' Core function for generating the Sierpinski Triangle. '''
        if deg > 0:
            lt = next(ids)
            tr = next(ids)
            rl = next(ids)
            gen_sierpinski(l,  lt, rl, deg-1, g)
            gen_sierpinski(lt, t,  tr, deg-1, g)
            gen_sierpinski(rl, tr, r,  deg-1, g)
        else:
            add_edges(l, t, g)
            add_edges(t, r, g)
            add_edges(r, l, g)

    def add_edges(u, v, g):
        ''' Adds edges between vertices u and v for all predicates. '''
        for i, p in enumerate(predicates):
            g += [[u, p, v, weights[i]]]
            g += [[v, p, u, weights[i]]]

    def _idgen():
        ''' Generates integer identifiers for vertices. '''
        c = 4
        while True:
            yield c
            c += 1

    ids = _idgen()
    graph = []
    degree = int(degree)
    predicates = predicates.split(' ')
    gen_sierpinski(1, 2, 3, degree, graph)
    _to_file(graph)
    return graph


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 1:
        print('Usage: python3', sys.argv[0], '<generator> [<args...>]')
        exit(1)

    generators = list(filter(callable, locals().values()))
    gen_name = args[0]
    gen = None
    for g in generators:
        if gen_name == g.__name__:
            gen = g
            break
    if not gen:
        print('Bad generator name. Available generators: ', end='')
        for name in [g.__name__ for g in generators]:
            if not name.startswith('_'):
                print(name, end=' ')
        print()
        exit(1)
    gen(*tuple(args[1:]))

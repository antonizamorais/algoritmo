'''
TODO: Write documentation.
'''

import gc
from sys import argv

from behaviors import RandomicBehavior, DeterministicBehavior, NonDeterministicBehavior
from cfpq import Grammar
from _graphmin.regular import RandomRGM
from _graphmin.contextfree import RandomCFGM
from graphs import Graph


def run_experiment(Minimizer, graph, grammar, query, optimum,
                   behavior=RandomicBehavior):
    # gc.disable()
    old = graph.total_weight()
    DMin, stats = Minimizer().minimize(graph, grammar, query, behavior)
    new = DMin.total_weight()
    output = [
        Minimizer.__name__[:10],
        grammar.name[grammar.name.rfind('/')+1:-4],
        graph.name[graph.name.rfind('/')+1:-4],
        len(set(graph.all_subjects())), graph.triples_count,
        '%.2f' % (old), '%.2f' % (new), '%.2f' % (round(new / optimum, 2)),
        '%d' % (stats['pq']['time']), '%d' % stats['gmin']['time'],
        '%.2f' % (stats['pq']['mem']), '%.2f' % (stats['gmin']['mem'])
    ]
    output = [str(x).replace('.', ',') for x in output]
    print(*output, sep='\t')
    # gc.enable()
    # DMin.show()


def _get_class(minimizer_name):
    for m in [RandomRGM, RandomCFGM]:
        if minimizer_name == m.__name__:
            return m
    else:
        raise ValueError('Bad graph minimizer class name.')


if __name__ == '__main__':
    try:
        Minimizer = _get_class(argv[1])
        grammar = Grammar.load(argv[2])
        graph = Graph.load(argv[3], [('weight', float)], grammar)
        optimum = float(argv[4])
    except IndexError:
        print('Usage:', argv[0],
              'minimizer_class graph.txt grammar.yrd optimum')
        quit(-1)
    s = grammar.start_symbol if Minimizer.__name__.endswith('CFGM') else 'q0'
    query = set()
    for v in graph.all_subjects():
        query.add((v, s))
    run_experiment(Minimizer, graph, grammar, query, optimum, behavior=DeterministicBehavior)

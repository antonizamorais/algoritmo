import unittest

from behaviors import (DeterministicBehavior, NonDeterministicBehavior,
                       RandomicBehavior)
from graphs import Graph
from _cfpq.grammars import Grammar


class BaseTestCase(unittest.TestCase):
    def assertEmpty(self, container, msg=None):
        """
        Asserts `container` is empty. Contains an actual default `msg`.
        """
        if msg is None:
            msg = 'Non-empty container %s.' % (container)
        self.assertEqual(len(container), 0, msg)

    def assertContains(self, container, contained):
        """
        Asserts `container` contains `contained`.
        """
        for x in contained:
            self.assertIn(x, container)


class MinimizerTestCase(BaseTestCase):
    test_data = 'tests/test_data/'
    graph_dir = test_data + 'weighted_graphs/'
    grammar_dir = test_data + 'grammars/'

    def _test(self, Minimizer, tests, **kwargs):
        behaviors = [
            DeterministicBehavior,
            NonDeterministicBehavior,
            RandomicBehavior
        ]
        alltests = []
        for behavior in behaviors:
            for t in tests:
                alltests += [(behavior, *t)]
        for behavior, grammarfile, graphfile, query, results, \
                weight in alltests:
            with self.subTest(Minimizer.__name__ + ', ' + grammarfile +
                              ', ' + graphfile + ', ' + behavior.__name__):
                grammar = Grammar.load(self.grammar_dir + grammarfile + '.yrd')
                graph = Graph.load(self.graph_dir + graphfile + '.txt',
                                   [('weight', float)], grammar)
                DMin, _ = Minimizer().minimize(graph, grammar, query,
                                               behavior=behavior, **kwargs)
                if behavior == DeterministicBehavior:
                    got = DMin.total_weight()
                    msg = 'Wrong weight. Want %f, got %f.' % (weight, got)
                    self.assertAlmostEqual(weight, got, msg=msg)
                self.assertNumberOfResults(DMin, grammar, query, results)

    def assertNumberOfResults(self, DMin, grammar, query, results):
        raise NotImplementedError('Abstract method.')

import unittest

from . import MinimizerTestCase
from cfpq import TraceItemsCFPQEngine
from graphmin import RandomCFGM
from graphmin import RandomRGM
from _graphmin.automata import Automaton, ProductAutomaton
from _graphmin.regular import _dfs_paths  # TODO: test _bfs_paths too


class RandomCFGMTest(MinimizerTestCase):
    def test_random_cfgm(self):
        tests = [
            ('aplusbstar', 'graph2', [('v1', 'a')], 4, 8),
            ('aplusbstar', 'graph3', [(x, 'a') for x in ['v1', 'v2', 'v3']],
             9, 9.8),
            ('aplusbstar', 'graph4', [('v1', 'a')], 2, 3.5),
        ]
        self._test(RandomCFGM, tests)

    def assertNumberOfResults(self, DMin, grammar, query, results):
        engine = TraceItemsCFPQEngine(grammar, DMin, query)
        got, _, _, _  = engine.run()
        msg = 'Wrong results. Want %d, got %d.' % (results, got)
        self.assertEqual(results, got, msg=msg)


class RegularGMTest(MinimizerTestCase):
    def test_random_rgm(self):
        tests = [
            ('aplusbstar', 'graph2', [('v1', 'q0')], 4, 5),
            ('aplusbstar', 'graph3', [(x, 'q0') for x in ['v1', 'v2', 'v3']],
             9, 7.7),
            ('aplusbstar', 'graph4', [('v1', 'q0')], 2, 3.5),
        ]
        self._test(RandomRGM, tests)

    def assertNumberOfResults(self, DMin, grammar, query, results):
        pa = ProductAutomaton(graph=DMin,
                              automaton=Automaton(grammar=grammar))
        answers = set()
        for i, (a, q) in enumerate(query):
            for _, b in _dfs_paths(a, q, i+1, pa, DMin, iter):
                answers.add((a, b))
        got = len(answers)
        msg = 'Wrong results. Want %d, got %d.' % (results, got)
        self.assertEqual(results, got, msg=msg)
    # TODO: write unit test for edge lives


if __name__ == '__main__':
    unittest.main()

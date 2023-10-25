from itertools import product
import unittest

from cfpq import TraceItemsCFPQEngine
from graphs import Graph
from cfpq import Grammar

test_data_dir = 'tests/test_data/'


class CFPQEngineTest(unittest.TestCase):
    def test_ontologies(self):
        dir = test_data_dir + 'ontologies/'
        for engine_class in [TraceItemsCFPQEngine]:
            for grammar, graph, expected in [
                ('sc_t', 'atom-primitive', 15454),
                ('sc_t', 'biomedical-mesure-primitive', 15156),
                ('sc_t', 'foaf', 4118),
                ('sc_t', 'funding', 17634),
                ('sc_t', 'generations', 2164),
                ('sc_t', 'people_pets', 9472),
                ('sc_t', 'pizza', 56195),
                ('sc_t', 'skos', 810),
                ('sc_t', 'travel', 2499),
                ('sc_t', 'univ-bench', 2540),
                ('sc_t', 'wine', 66572),
                ('sc', 'atom-primitive', 122),
                ('sc', 'biomedical-mesure-primitive', 2871),
                ('sc', 'foaf', 10),
                ('sc', 'funding', 1158),
                ('sc', 'generations', 0),
                ('sc', 'people_pets', 37),
                ('sc', 'pizza', 1262),
                ('sc', 'skos', 1),
                ('sc', 'travel', 63),
                ('sc', 'univ-bench', 81),
                ('sc', 'wine', 133)
            ]:
                with self.subTest('{engine.__name__}, {grammar}, {graph}'):
                    graph = Graph.load(dir + graph + '.txt')
                    grammar = Grammar.load(dir + grammar + '.yrd')
                    query = set(product(graph.all_nodes(), [grammar.start_symbol]))
                    engine = engine_class(grammar, graph, query)
                    self._test_database(engine, expected)

    def _test_database(self, engine, expected_result_count):
        engine_name = type(engine).__name__
        grammar = engine.G.name
        graph = engine.D.name
        got_result_count, _, _, _ = engine.run()
        errmsg = f'\nFor {engine_name}, {grammar}, {graph}' + \
                 f'\nWant {expected_result_count}, got {got_result_count}.'
        self.assertEqual(expected_result_count, got_result_count, errmsg)


class GrammarTest:
    def setUp(self):
        self.grammar = util.load_grammar(test_data_dir+'sc.yrd')

    def test_start_symbol(self):
        self.assertEqual('s', self.grammar.start_symbol)

    def test_terminals(self):
        self.assertEqual(set(['SCO', 'SCOR']), self.grammar.term)

    def test_nonterminals(self):
        self.assertEqual(set(['s', 'b']), self.grammar.nonterm)

    def test_nullable(self):
        self.assertEqual(set(['b']), self.grammar.nullable)

    def test_rules(self):
        self.assertEqual(1, len(self.grammar.rules['s']))
        self.assertEqual(2, len(self.grammar.rules['b']))
        self.assertIn(['b', 'SCOR'], self.grammar.rules['s'])
        self.assertIn(['SCO', 'b', 'SCOR'], self.grammar.rules['b'])
        self.assertIn([], self.grammar.rules['b'])


if __name__ == '__main__':
    unittest.main()

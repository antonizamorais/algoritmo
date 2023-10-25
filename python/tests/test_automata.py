import unittest
from _graphmin.automata import ProductAutomaton, Automaton
from graphs import Graph


dir = 'tests/test_data/weighted_graphs/'


class AutomatonTest(unittest.TestCase):
    def test_init(self):
        automaton = Automaton()
        self.assertEqual(automaton.initial_states, set())
        self.assertEqual(automaton.final_states, set())

    def test_add(self):
        """
        Check whether graph inherited methods are working.
        """
        automaton = Automaton()
        automaton.add('q0', 'a', 'q1')
        self.assertIn(('q0', 'a', 'q1'), automaton)
        self.assertEqual(len(automaton), 1)


class ProductAutomatonTest(unittest.TestCase):
    def test_empty_init(self):
        pa = ProductAutomaton()
        self.assertEqual(pa.initial_states, set())
        self.assertEqual(pa.final_states,  set())
        self.assertEqual(pa.subj_data, {})
        self.assertEqual(pa.obj_data, {})
        self.assertEqual(len(pa), 0)

    def test_init(self):
        from .test_data.automata.aplusbstar import automaton
        graph = Graph.load(dir+'graph1.txt', [('weight', float)])
        pa = ProductAutomaton(graph, automaton)
        self.assertEqual(pa.initial_states, {('v1', 'q0'), ('v2', 'q0')})
        self.assertEqual(pa.final_states, {('v2', 'q1'), ('v1', 'q1'),
                                           ('v2', 'q2')})
        self.assertEqual(len(pa), 8)
        self.assertIn((('v1', 'q0'), 'A', ('v1', 'q1')), pa)
        self.assertIn((('v1', 'q0'), 'A', ('v2', 'q1')), pa)
        self.assertIn((('v2', 'q0'), 'A', ('v1', 'q1')), pa)
        self.assertIn((('v1', 'q1'), 'A', ('v2', 'q1')), pa)
        self.assertIn((('v2', 'q1'), 'A', ('v1', 'q1')), pa)
        self.assertIn((('v2', 'q1'), 'B', ('v2', 'q2')), pa)
        self.assertIn((('v2', 'q2'), 'B', ('v2', 'q2')), pa)

        self.assertEqual(pa.weight(('v1', 'q0'), 'A', ('v1', 'q1')), 1)
        self.assertEqual(pa.weight(('v1', 'q0'), 'A', ('v2', 'q1')), 2.5)
        self.assertEqual(pa.weight(('v1', 'q1'), 'A', ('v2', 'q1')), 2.5)
        self.assertEqual(pa.weight(('v2', 'q0'), 'A', ('v1', 'q1')), 3.8)
        self.assertEqual(pa.weight(('v2', 'q1'), 'A', ('v1', 'q1')), 3.8)
        self.assertEqual(pa.weight(('v2', 'q1'), 'B', ('v2', 'q2')), 4.9)
        self.assertEqual(pa.weight(('v2', 'q2'), 'B', ('v2', 'q2')), 4.9)

    def test_add(self):
        pa = ProductAutomaton()
        pa.add(('x', 'q0'), 'p', ('y', 'q1'))
        self.assertEqual(len(pa), 1)
        self.assertIn((('x', 'q0'), 'p', ('y', 'q1')), pa)


if __name__ == '__main__':
    unittest.main()

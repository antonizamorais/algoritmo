import unittest
from graphs import Graph

dir = 'tests/test_data/weighted_graphs/'


class GraphTest(unittest.TestCase):
    def test_graph_weight(self):
        graph = Graph.load(dir+'graph1.txt', [('weight', float)])
        self.assertAlmostEqual(graph.total_weight(), 12.2)

# TODO: Write more tests

from graphs import Graph
from behaviors import NonDeterministicBehavior


class Automaton(Graph):
    """
    An Automaton is a Graph with initial and final states.
    """

    def __init__(self, grammar=None, **kwargs):
        super().__init__(**kwargs)
        self.initial_states = set()
        self.final_states = set()
        if grammar is not None:
            # TODO: implement a real automaton builder
            automaton = None
            if grammar.name.endswith('aplusbstar.yrd'):
                from tests.test_data.automata.aplusbstar import automaton
            elif grammar.name.endswith('aorbstar.yrd'):
                from tests.test_data.automata.aorbstar import automaton
            elif grammar.name.endswith('abcdstar.yrd'):
                from tests.test_data.automata.abcdstar import automaton
            elif grammar.name.endswith('astar.yrd'):
                from tests.test_data.automata.astar import automaton
            elif grammar.name.endswith('a-bstar.yrd'):
                from tests.test_data.automata.abstar import automaton
            elif grammar.name.endswith('a-cstar.yrd'):
                from tests.test_data.automata.acstar import automaton
            elif grammar.name.endswith('a-dstar.yrd'):
                from tests.test_data.automata.adstar import automaton
            elif grammar.name.endswith('a-estar.yrd'):
                from tests.test_data.automata.aestar import automaton
            else:
                raise Exception('Bad grammar %s.' % (grammar.name))
            self.initial_states = automaton.initial_states
            self.final_states = automaton.final_states
            for s, p, o, data in automaton:
                self.add(s, p, o, data)

    def show(self):
        print("Initial states:", self.initial_states)
        print("Final states:", self.final_states)
        super().show()


class ProductAutomaton(Automaton):
    """
    A ProductAutomaton represents a product between an Automaton and a Graph.
    Its nodes are (vertex, state) pairs and it contains edges between those
    nodes.
    """

    def __init__(self, graph=None, automaton=None,
                 behavior=NonDeterministicBehavior, **kwargs):
        """
        Creates a new ProductAutomaton object.
        If params graph and automaton are not None, returns the product from
        them.
        """
        super().__init__(**kwargs)
        self.iter = behavior.iter
        self.random = behavior.random
        if (graph is not None) and (automaton is not None):  # compute product
            pairs = set()
            for v in graph.all_nodes():
                for q in automaton.initial_states:
                    pairs.add((v, q))
            visited = set()
            while len(pairs) > 0:
                v1, q1 = pairs.pop()
                node1 = (v1, q1)
                visited.add(node1)
                for label, v2 in graph.predicate_objects(v1):
                    for q2 in automaton.objects(q1, label):
                        node2 = (v2, q2)
                        if q1 in automaton.initial_states:
                            self.initial_states.add(node1)
                        if q2 in automaton.initial_states:
                            self.initial_states.add(node2)
                        if q1 in automaton.final_states:
                            self.final_states.add(node1)
                        if q2 in automaton.final_states:
                            self.final_states.add(node2)
                        self.add(node1, label, node2, graph.data(v1, label,
                                                                 v2))
                        if node2 not in visited:
                            pairs.add(node2)

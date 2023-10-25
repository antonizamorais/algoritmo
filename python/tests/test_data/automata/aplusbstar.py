from _graphmin.automata import Automaton

automaton = Automaton(name='A+B*')
automaton.add('q0', 'A', 'q1')
automaton.add('q1', 'A', 'q1')
automaton.add('q1', 'B', 'q2')
automaton.add('q2', 'B', 'q2')
automaton.initial_states = set(['q0'])
automaton.final_states = set(['q1', 'q2'])

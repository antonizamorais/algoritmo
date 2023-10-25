from _graphmin.automata import Automaton

automaton = Automaton(name='(A|B)*')
automaton.add('q0', 'A', 'q0')
automaton.add('q0', 'B', 'q0')
automaton.initial_states = set(['q0'])
automaton.final_states = set(['q0'])

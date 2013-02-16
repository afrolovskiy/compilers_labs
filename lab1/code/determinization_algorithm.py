from fa import FA, get_alphabet
from tompson_algorithm import TompsonAlgorithm


class DeterminizationAlgorithm:

    def __init__(self, nfa, alphabet):
        self.nfa = nfa    
        self.alphabet = alphabet

    def build_subsets(self):
        last_state = 0
        generalized_states = {}
        transition_table ={}
        initial_state = None
        final_state = []	

        closure = self._closure([self.nfa.initial_state], self.nfa.transition_table)
        generalized_states = {last_state: set(closure)}
        initial_state = last_state
        last_state += 1

        d_states = [set(closure)]
        unmarked = [set(closure)]

        while unmarked:
            T = unmarked.pop()
            transitions = {}
            for a in self.alphabet:   
                mv = self._move(list(T), a, self.nfa.transition_table)
                U = set(self._closure(mv, self.nfa.transition_table))
                if U:
                    if U not in d_states:
                        d_states.append(U)
                        generalized_states[last_state] = U
                        if self.nfa.final_state in U:
				            final_state.append(last_state)
                        last_state += 1
                        unmarked.append(U)
                    transitions.update({a: [self.get_key_by_value(generalized_states, U)]})
            transition_table[self.get_key_by_value(generalized_states, T)] = transitions   
        return FA(transition_table, initial_state, final_state)

    def get_key_by_value(self, dictionary, value):
        for key, item in dictionary.items():
            if item == value:
                return key

    def _closure(self, T, transition_table):
        stack = list(T)
        closure = list(T)
        while stack:
            t = stack.pop()
            for u in transition_table[t].get(FA.EMPTY, []):
                if u not in closure:
                    closure.append(u)
                    stack.append(u)
        return closure

    def _move(self, T, a, transition_table):
        result = set()
        for s in T:
            states = set(transition_table[s].get(a, []))
            result = result.union(states)
        return result

#regexp = "aaabbb"
#regexp = "a(ab)*b"
#regexp = "a(a|b)*b"
#regexp = "a(a*|b)*b"
#regexp = "a|b"
#alg1 = TompsonAlgorithm(regexp)
#fa = alg1.buildNFA()
#fa.draw('graph')

#alg2 = DeterminizationAlgorithm(fa, ['a', 'b'])
#fa2 = alg2.build_subsets()
#fa2.draw('graph2') 


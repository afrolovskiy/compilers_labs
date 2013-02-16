from fa import FA, get_alphabet
from tompson_algorithm import TompsonAlgorithm
from determinization_algorithm import DeterminizationAlgorithm
from minimization_algorithm import MinimizationAlgorithm


class WrongString(Exception):
    pass

class ModellingAlgorithm:
    
    def __init__(self, fa, alphabet):
        self.fa = fa
        self.alphabet = alphabet

    def model(self, source):
        state = self.fa.initial_state
        for symbol in source:
            state = self._move(state, symbol)
        if state in self.fa.final_state:
            return True
        raise WringString()

    def _move(self, state, symbol):
        transitions = self.fa.transition_table.get(state, {}).get(symbol, [])
        if transitions:
            return transitions[0]
        raise WrongString()


regexp = "a(a*|b)*b"
alg1 = TompsonAlgorithm(regexp)
fa = alg1.buildNFA()
fa.draw('graph')

alg2 = DeterminizationAlgorithm(fa, ['a', 'b'])
fa2 = alg2.build_subsets()
fa2.draw('graph2') 

alg3 = MinimizationAlgorithm(fa2, ['a', 'b'])
fa3 = alg3.minimize()
fa3.draw('graph3') 

alg4 = ModellingAlgorithm(fa3, ['a', 'b'])
alg4.model('baaaaab')

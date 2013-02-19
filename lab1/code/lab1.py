# variant 6
from fa import (FA, TompsonAlgorithm, DeterminizationAlgorithm, MinimizationAlgorithm,
		      ModellingAlgorithm)


regexp = "(a|b)*"
s = ''
#s = 'ab'

#regexp = "a(a|bbb)*bab"
#s = 'aabab'
#s = 'abbbabab'
#s = 'abbabab'

#regexp = 'abc*|bbb|a*'
#s = ''
#s = 'aaaaaaaaaa'
#s = 'ab'
#s = 'bb'

alg1 = TompsonAlgorithm(regexp)
fa = alg1.buildNFA()
fa.draw('graph')

alg2 = DeterminizationAlgorithm(fa)
fa2 = alg2.build_subsets()
fa2.draw('graph2') 

alg3 = MinimizationAlgorithm(fa2)
fa3 = alg3.minimize()
fa3.draw('graph3') 

alg4 = ModellingAlgorithm(fa3)
alg4.model(s)

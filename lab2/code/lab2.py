from grammar import (Symbol , EmptySymbol,Terminal,
					 Nonterminal, Rule, Grammar)
from conversion import has_empty_chain, convert_grammar


grammar = Grammar()

S = Nonterminal('S')
A = Nonterminal('A')
B = Nonterminal('B')
grammar.nonterminals.update([A, B, S])

grammar.axiom = S

a = Terminal('a')
b = Terminal('b')
grammar.terminals.update([a, b])

e = EmptySymbol()

grammar.rules.append(Rule([S], [A, B]))
grammar.rules.append(Rule([A], [a, A]))
grammar.rules.append(Rule([A], [e]))
grammar.rules.append(Rule([B], [b, A]))
grammar.rules.append(Rule([B], [e]))

print "grammar:", grammar
print has_empty_chain(grammar)

new_grammar = convert_grammar(grammar)
print "new_grammar:", new_grammar


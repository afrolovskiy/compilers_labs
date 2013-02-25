from grammar import (Symbol , EmptySymbol,Terminal,
					 Nonterminal, Rule, Grammar)
from conversion import (has_empty_chain, convert_grammar, find_disappearing_nonterminals,
				   delete_empty_rules, delete_useless_nonterminals, convert_to_greibach)


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

print "grammar:\n", grammar

#disappearing_nonterminals = find_disappearing_nonterminals(grammar)
#new_grammar = convert_grammar(grammar, disappearing_nonterminals)
#print "new_grammar:\n", new_grammar

#new_grammar2 = delete_empty_rules(grammar)
#print "new_grammar2:"
#print new_grammar2

new_grammar3 = convert_to_greibach(grammar)
print "grammar3:", new_grammar3
###################################################################
#grammar2 = Grammar()

#S = Nonterminal('S')
#A = Nonterminal('A')
#B = Nonterminal('B')
#C = Nonterminal('C')
#D = Nonterminal('D')
#grammar2.nonterminals.update([A, B, C, D, S])

#grammar2.axiom = S

#a = Terminal('a')
#b = Terminal('b')
#grammar2.terminals.update([a, b])

#e = EmptySymbol()

#grammar2.rules.append(Rule([S], [A, C, D]))
#grammar2.rules.append(Rule([A], [e]))
#grammar2.rules.append(Rule([B], [e]))
#grammar2.rules.append(Rule([C], [a, b]))
#grammar2.rules.append(Rule([D], [A, B]))

#print "grammar2:\n", grammar2

#new_grammar2 = delete_useless_nonterminals(grammar2)
#print "new_grammar2:", new_grammar2
#####################################################################


from grammar import Grammar, Rule, Nonterminal, Terminal, EmptySymbol, Symbol
from topdown_parser import Configuration, TopDownParser

grammar = Grammar()

true = Terminal('<true>')
false = Terminal('<false>')
identifier = Terminal('<identifier>')
or_operator  = Terminal('!')
and_operator = Terminal('&')
not_operator = Terminal('~')
grammar.terminals.update([true, false, identifier, or_operator, and_operator, not_operator])

S = Nonterminal('S')
S_new = Nonterminal('SS')
A = Nonterminal('A')
A_new = Nonterminal('AA')
B = Nonterminal('B')
C = Nonterminal('C')
D = Nonterminal('D')
grammar.nonterminals.update([S, S_new, A, A_new, B, C, D])
grammar.axiom = S

grammar.rules.append(Rule([S], [A]))
grammar.rules.append(Rule([S], [A, S_new]))
grammar.rules.append(Rule([S_new], [or_operator, A]))
grammar.rules.append(Rule([S_new], [or_operator, A, S_new]))
grammar.rules.append(Rule([A], [C]))
grammar.rules.append(Rule([A], [C, A_new]))
grammar.rules.append(Rule([A_new], [and_operator, C]))
grammar.rules.append(Rule([A_new], [and_operator, C, A_new]))
grammar.rules.append(Rule([C], [B]))
grammar.rules.append(Rule([C], [not_operator, B]))
grammar.rules.append(Rule([B], [D]))
grammar.rules.append(Rule([B], [identifier]))
grammar.rules.append(Rule([D], [true]))
grammar.rules.append(Rule([D], [false]))

print "grammar:\n", grammar


expr = [true, or_operator, true, and_operator, false, and_operator, identifier, 
           or_operator, true, or_operator]
print "expr: %s\n" % ''.join([str(symbol) for symbol in expr])

parser = TopDownParser(grammar)
parser.parse(expr)

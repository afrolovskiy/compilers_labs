from grammar import (Symbol , EmptySymbol,Terminal, 
					 Nonterminal, Rule, Grammar)


def find_disappearing_nonterminals(grammar):
	# initialize disappearing nonterminals set
	disappearing_nonterminals = set()
	for rule in grammar.rules:
		if (len(rule.right_side) == 1 and
				rule.right_side[0] == EmptySymbol()):
			disappearing_nonterminals.add(rule.left_side[0])		
			
	# find other disappearing nonterminals
	new_disappearing_nonterminals = set(disappearing_nonterminals)
	disappearing_nonterminals = set()
	while disappearing_nonterminals != new_disappearing_nonterminals:
		disappearing_nonterminals = set(new_disappearing_nonterminals)
		for rule in grammar.rules:
			output_symbols = set(rule.right_side)
			if output_symbols.issubset(new_disappearing_nonterminals):
				new_disappearing_nonterminals.add(rule.left_side[0])

	return disappearing_nonterminals


def has_empty_chain(grammar):
	disappearing_nonterminals = find_disappearing_nonterminals(grammar)				
	return grammar.axiom in disappearing_nonterminals 


def convert_grammar(grammar):
	new_grammar = Grammar()

	# build new nonterminals set
	disappearing_nonterminals = find_disappearing_nonterminals(grammar)
	new_grammar.nonterminals = build_new_nonterminals_set(grammar, disappearing_nonterminals)

	# find new axiom
	if grammar.axiom in disappearing_nonterminals:
		# language has empty chain
		new_grammar.axiom = Nonterminal(grammar.axiom.name, False)
		new_grammar.nonterminals.add(new_grammar.axiom)
		new_grammar.nonterminals.remove(grammar.axiom)
	else:
		new_grammar.axiom = grammar.axiom

	# build new rules
	new_grammar.rules = build_new_rules(
		grammar, disappearing_nonterminals, new_grammar.nonterminals)

	# copy terminals	
	new_grammar.terminals = set(grammar.terminals)
	return new_grammar


def build_new_nonterminals_set(grammar, disappearing_nonterminals):
	new_nonterminals = set(grammar.nonterminals)
	for nonterminal in grammar.nonterminals:
		if nonterminal in disappearing_nonterminals:
			new_nonterminals.add(Nonterminal(nonterminal.name, False))
	return new_nonterminals	


def build_new_rules(grammar, disappearing_nonterminals, new_nonterminals):
	new_rules = []
	for rule in grammar.rules:
		if not rule.is_empty():
			idx = find_left_nonnullable_symbol_idx(rule)	

			adding_rules = build_adding_rules(rule, idx)
			new_rules.extend(adding_rules)			

			if rule.left_side[0] in disappearing_nonterminals:
				for adding_rule in adding_rules:
					left_side = [adding_rule.left_side[0].create_nonnullable_nonterminal()]
					right_side = list(adding_rule.right_side)
					new_rules.append(Rule(left_side, right_side))
		else:
			new_rules.append(rule)	

	new_cleared_rules = []
	for rule in new_rules:
		if rule.left_side[0] in new_nonterminals:
			new_cleared_rules.append(rule)

	return new_cleared_rules
	
def find_left_nonnullable_symbol_idx(rule):
	idx = 0
	for symbol in rule.right_side:
		print "symbol:", symbol
		if not symbol.is_nullable:
			return idx
		idx += 1
	return idx


def build_adding_rules(rule, idx):
	adding_rules = []
	for i in range(idx):
		left_side = list(rule.left_side)
		right_side = [rule.right_side[i].create_nonnullable_nonterminal()]
		right_side.extend(rule.right_side[i + 1:])
		adding_rules.append(Rule(left_side, right_side))

	if idx < len(rule.right_side):
		left_side = list(rule.left_side)
		right_side = rule.right_side[idx:]				
		adding_rules.append(Rule(left_side, right_side))
	return adding_rules



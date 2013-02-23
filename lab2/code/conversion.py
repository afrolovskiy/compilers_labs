from grammar import (Symbol , EmptySymbol,Terminal, 
					 Nonterminal, ComplexNonterminal, Rule, Grammar)


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


###############################################################################
def convert_grammar(grammar, disappearing_nonterminals):
	new_grammar = Grammar()

	# build new nonterminals set
	new_grammar.nonterminals = build_new_nonterminals_set(
		grammar, disappearing_nonterminals)

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
###############################################################################


###############################################################################
def delete_empty_rules(grammar):
	disappearing_nonterminals = find_disappearing_nonterminals(grammar)

	converted_grammar = convert_grammar(grammar, disappearing_nonterminals)
	print "converted_grammar:"
	print converted_grammar

	cleared_grammar = delete_useless_nonterminals(converted_grammar)
	print "cleared_grammar:"
	print cleared_grammar

	# build new grammar
	new_grammar = Grammar()
	new_grammar.axiom = ComplexNonterminal(
		[cleared_grammar.axiom], cleared_grammar.axiom.is_nullable)


	return new_grammar


#################################################
def delete_useless_nonterminals(grammar):
	new_rules = list(grammar.rules)
	new_nonterminals = set(grammar.nonterminals)

	while True:
		useless_nonterminals = find_useless_nonterminals(new_rules)
		if not useless_nonterminals:
			break

		new_rules = delete_useless_nonterminals_from_rules(new_rules, useless_nonterminals)
		new_rules = delete_useless_nonterminals_rules(new_rules, useless_nonterminals)
		new_nonterminals.difference_update(useless_nonterminals) 

	new_grammar = Grammar()
	new_grammar.axiom = grammar.axiom
	new_grammar.terminals = set(grammar.terminals)
	new_grammar.nonterminals = new_nonterminals
	new_grammar.rules = new_rules
	return new_grammar


def find_useless_nonterminals(rules):
	useless_nonterminals = set()
	normal_nonterminals = set()

	for rule in rules:
		nonterminal = rule.left_side[0]
		if not rule.is_empty():
			normal_nonterminals.add(nonterminal)
			if nonterminal in useless_nonterminals:
				useless_nonterminals.remove(nonterminal)
		elif nonterminal not in normal_nonterminals:
			useless_nonterminals.add(nonterminal)

	return useless_nonterminals


def delete_useless_nonterminals_from_rules(rules, useless_nonterminals):
	new_cleared_rules = []
	for rule in rules:
		right_side = rule.right_side
		if not rule.is_empty():
			rule = delete_useless_nonterminals_from_rule(rule, useless_nonterminals)
		new_cleared_rules.append(rule)
	return new_cleared_rules
		

def delete_useless_nonterminals_from_rule(rule, useless_nonterminals):
	left_side = list(rule.left_side)
	right_side = list(rule.right_side)
	for nonterminal in useless_nonterminals:
		while nonterminal in right_side:
			right_side.remove(nonterminal)
	if len(right_side) == 0:
		right_side = [EmptySymbol()]
	return Rule(left_side, right_side)
	

def delete_useless_nonterminals_rules(rules, useless_nonterminals):
	new_cleared_rules = []
	for rule in rules:
		nonterminal = rule.left_side[0]
		if nonterminal not in useless_nonterminals:
			new_cleared_rules.append(rule)
	return new_cleared_rules
################################################




###############################################################################


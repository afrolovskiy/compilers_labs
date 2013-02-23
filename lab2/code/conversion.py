# variant 14
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
# Algorithm 8.1
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
# Algorithm 8.2
def delete_empty_rules(grammar):
	disappearing_nonterminals = find_disappearing_nonterminals(grammar)

	converted_grammar = convert_grammar(grammar, disappearing_nonterminals)
	print "converted_grammar:"
	print converted_grammar

	cleared_grammar = delete_useless_nonterminals(converted_grammar)
	print "cleared_grammar:"
	print cleared_grammar

	return build_new_grammar(cleared_grammar)


def find_rules_for_nonterminal(rules, nonterminal):
	selected_rules = []
	for rule in rules:
		if rule.left_side[0] == nonterminal:
			selected_rules.append(rule)
	return selected_rules


def replace_nonterminal(chain, idx, inserted_symbols):
	new_chain = []
	if idx > 0:
		new_chain = chain[:idx]
	new_chain.extend(inserted_symbols)
	if (idx + 1) < len(chain):
		new_chain.extend(chain[idx + 1:])
	return new_chain


def build_new_grammar(grammar):
	new_grammar = Grammar()
	new_grammar.terminals = set(grammar.terminals)
	new_grammar.axiom = ComplexNonterminal(
		[grammar.axiom], grammar.axiom.is_nullable)

	new_rules = []
	unwatched, watched = [new_grammar.axiom], set()
	while unwatched:
		complex_nonterminal = unwatched[0]
		unwatched.remove(complex_nonterminal)
		watched.add(complex_nonterminal)

		if complex_nonterminal.starts_with_nonterminal():
			new_rules.extend(build_rules_starts_with_nonterminal(
				grammar.rules, complex_nonterminal, watched, unwatched))
		elif complex_nonterminal.starts_with_terminal():
			new_rules.extend(build_rules_starts_with_terminal(
				grammar.rules, complex_nonterminal, watched, unwatched))
					
	new_grammar.rules = new_rules
	new_grammar.nonterminals = watched
	return new_grammar


def build_rules_starts_with_nonterminal(rules, complex_nonterminal, watched, unwatched):
	adding_rules = []
	nonterminal_rules = find_rules_for_nonterminal(
		rules, complex_nonterminal.name[0])
	for rule in nonterminal_rules:
		if not rule.is_empty():
			left_side = [complex_nonterminal]

			new_name = replace_nonterminal(complex_nonterminal.name, 0, rule.right_side)
			new_complex_nonterminal = ComplexNonterminal(new_name)
			right_side = [new_complex_nonterminal]
			
			if (new_complex_nonterminal not in watched and
					new_complex_nonterminal not in unwatched):
				unwatched.append(new_complex_nonterminal)				

			new_rule = Rule(left_side, right_side)
			adding_rules.append(new_rule)
	return adding_rules


def build_rules_starts_with_terminal(rules, complex_nonterminal, watched, unwatched):
	adding_rules = []
	symbols = complex_nonterminal.name
	for idx in range(1, len(symbols)):
		symbol = symbols[idx]

		if (isinstance(symbol, Terminal) or 
				(isinstance(symbol, Nonterminal) and not symbol.is_nullable)):
			break

		selected_rules = find_rules_for_nonterminal(rules, symbol)
		for rule  in selected_rules:
			if not rule.is_empty():
				left_side = [complex_nonterminal]

				new_name = list(rule.right_side)
				if (idx + 1) < len(symbols):
					new_name.extend(symbols[idx + 1:])
				new_complex_nonterminal = ComplexNonterminal(new_name)
				right_side = [symbols[0], new_complex_nonterminal]

				if (new_complex_nonterminal not in watched and
						new_complex_nonterminal not in unwatched):
					unwatched.append(new_complex_nonterminal)
			
				adding_rules.append(Rule(left_side, right_side))

	adding_rules.append(Rule([complex_nonterminal], [symbols[0]]))

	return adding_rules
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
# Algorithm 8.3
def convert_to_greibach(grammar):
	converted_grammar = delete_empty_rules(grammar)
	
	new_grammar = Grammar()
	new_grammar.axiom = converted_grammar.axiom	
	new_grammar.terminals = set(converted_grammar.terminals)	

	sorted_nonterminals = sort_nonterminals(
		converted_grammar.nonterminals, converted_grammar.rules)
	new_grammar.nonterminals = set(sorted_nonterminals)

	# rebuild rules
	nonterminal = sorted_nonterminals[-1]
	new_rules = find_rules_for_nonterminal(converted_grammar.rules, nonterminal)
	for idx in range(len(sorted_nonterminals)  - 2, -1, -1):
		nonterminal = sorted_nonterminals[idx]
		rules = find_rules_for_nonterminal(converted_grammar.rules, nonterminal)
		for rule in rules:
			if isinstance(rule.right_side[0], Nonterminal):
				new_rules.extend(replace_rule(new_rules, rule))
			else:
				new_rules.append(rule)

	# add rules for terminals
	for terminal in converted_grammar.terminals:
		new_nonterminal = Nonterminal("X{%s}" % str(terminal))
		new_grammar.nonterminals.add(new_nonterminal)
		new_rules.append(Rule([new_nonterminal], [terminal]))

		# replace nonleft terminal to new nonterminals
		for rule in new_rules:
			rule =replace_nonleft_terminal_to_nonterminal(rule, terminal, new_nonterminal)

	new_grammar.rules = new_rules
	
	print "grammar:", new_grammar
		
	return delete_nonderivable_nonterminals(new_grammar)


def replace_rule(new_rules, rule):
	adding_rules = []

	nonterminal = rule.right_side[0]
	nonterminal_rules = find_rules_for_nonterminal(new_rules, nonterminal)

	if nonterminal_rules:
		left_side = rule.left_side
		for nonterminal_rule in nonterminal_rules:
			right_side = replace_nonterminal(rule.right_side, 0, nonterminal_rule.right_side) 
			adding_rules.append(Rule(left_side, right_side))
	else:
		adding_rules.append(rule)

	return adding_rules


def replace_nonleft_terminal_to_nonterminal(rule, terminal, nonterminal):
	if terminal in rule.right_side[1:]:
		new_right_side = list(rule.right_side)
		for idx in range(1, len(rule.right_side)):
			symbol = rule.right_side[idx]
			if symbol == terminal:
				new_right_side[idx] = nonterminal
	else:
		new_right_side = rule.right_side
	return Rule(rule.left_side, new_right_side)

#########################################################
def delete_nonderivable_nonterminals(grammar):
	new_grammar = Grammar()
	new_grammar.axiom = grammar.axiom
	new_grammar.terminals = grammar.terminals

	unwatched = list([new_grammar.axiom])
	watched = set()
	while unwatched:
		nonterminal = unwatched[0]
		unwatched = unwatched.remove(nonterminal) or []
		watched.add(nonterminal)

		rules = find_rules_for_nonterminal(grammar.rules, nonterminal)
		for rule in rules:
			for symbol in rule.right_side:
				if isinstance(symbol, Nonterminal):
					if symbol not in watched and symbol not in unwatched:
						unwatched.append(symbol)

	new_grammar.nonterminals = watched

	new_rules = []
	for rule in grammar.rules:
		if rule.left_side[0] in watched:
			new_rules.append(rule)

	new_grammar.rules = new_rules

	return new_grammar	 
	

#########################################################
def sort_nonterminals(nonterminals, rules):
	def delete_recursive_rules(rules):
		result_rules = []
		for rule in rules:
			nonterminal = rule.left_side[0]
			if nonterminal not in rule.right_side:	
				result_rules.append(rule)
		return result_rules

	def compare(nonterminal1, nonterminal2):
		if nonterminal1 == nonterminal2:
			return 0

		rules1 = find_rules_for_nonterminal(tuning_rules, nonterminal1)
		for rule in rules1:
			if nonterminal2 in rule.right_side:
				return -1
			for symbol in rule.right_side:
				if isinstance(symbol, Nonterminal):
					return compare(symbol, nonterminal2)

		rules2 = find_rules_for_nonterminal(tuning_rules, nonterminal2)
		for rule in rules2:
			if nonterminal1 in rule.right_side:
				return 1
			for symbol in rule.right_side:
				if isinstance(symbol, Nonterminal):
					return compare(nonterminal1, symbol)

	tuning_rules = delete_recursive_rules(rules)
	return sorted(list(nonterminals), compare)
#########################################################
	

	

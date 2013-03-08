from grammar import Grammar, Rule, Nonterminal, Terminal, EmptySymbol, Symbol

class Configuration:
	NORMAL_STATE = 'q'
	RETURN_STATE = 'b'
	TERMINAL_STATE = 't'
	
	def __init__(self, state, position, history, chain):
		self.state = state
		self.position = position
		self.history = history
		self.chain = chain

	def history2str(self):
		result = ""
		for element in self.history:
			if isinstance(element, Terminal):
				result += str(element)
			else:
				result += '%s%s' % (str(element[0]), element[1])
		return result
	
	def chain2str(self):
		return '%(chain)s$' % {
			'chain': ''.join([str(symbol) for symbol in reversed(self.chain)]),		
		}

	def __str__(self):
		return "(%(state)s, %(position)s, %(history)s, %(chain)s)" % {
			'state': self.state,
			'position': self.position,
			'history': self.history2str(),
			'chain': self.chain2str(),		
		}


class ParseError(Exception):
	pass


class TopDownParser:
	
	def __init__(self, grammar):
		self.grammar = grammar
		self.alternatives = self.order_alternatives(grammar)

	def order_alternatives(self, grammar):
		alternatives = {}
		for rule in grammar.rules:
			nonterminal = rule.left_side[0]
			if nonterminal not in alternatives.keys():
				alternatives[nonterminal] = []
			alternatives[nonterminal].append(rule.right_side)
		return alternatives

	def parse(self, input_chain):
		configuration = self.initial_configuration()
		while True:
			print str(configuration)
			if configuration.chain:
				symbol = configuration.chain.pop()
				if isinstance(symbol, Nonterminal):
					self.expand_tree(configuration, symbol)
				elif isinstance(symbol, Terminal):
					if self.compare_terminal(configuration, symbol, input_chain):
						break
			else:
				self.compare_failed(configuration)			
				
		print str(configuration)
		return configuration.history		

	def initial_configuration(self):
		return Configuration(Configuration.NORMAL_STATE, 0, [], [self.grammar.axiom])

	def expand_tree(self, configuration, nonterminal, idx=0):
		configuration.state = Configuration.NORMAL_STATE

		nonterminal_alternatives = self.alternatives.get(nonterminal, None)
		if not nonterminal_alternatives:
			raise ParseError("Alternatives don't exist")
		alternative_right_side = nonterminal_alternatives[idx]		

		configuration.chain.extend(reversed(alternative_right_side))
		configuration.history.append((nonterminal, idx))

	def compare_terminal(self, configuration, terminal, input_chain):
		if terminal == input_chain[configuration.position]:
			self.compare_success(configuration, terminal)
			if configuration.position == len(input_chain):
				if not configuration.chain:
					configuration.state = Configuration.TERMINAL_STATE
					return True
				else:
					self.compare_failed(configuration)
		else:
			self.compare_failed(configuration, terminal)
		return False

	def compare_success(self, configuration, terminal):
		configuration.state = Configuration.NORMAL_STATE
		configuration.position += 1
		configuration.history.append(terminal)
	
	def compare_failed(self, configuration, terminal=None):
		configuration.state = Configuration.RETURN_STATE
		if terminal:
			configuration.chain.append(terminal)
		self.transform_terminals(configuration)			
		self.try_alternative(configuration)

	def transform_terminals(self, configuration):
		length = len(configuration.history)
		for idx in reversed(range(length)):
			symbol = configuration.history[idx]
			if isinstance(symbol, Terminal):
				configuration.chain.append(symbol)
				configuration.position -= 1
			else:
				configuration.history = configuration.history[:idx + 1]
				break

	def try_alternative(self, configuration):
		print str(configuration)		
		alternative = configuration.history.pop()

		nonterminal, alternative_idx = alternative
		alternative_right_side = self.alternatives[nonterminal][alternative_idx]
		if configuration.chain:		
			length = len(alternative_right_side)
			configuration.chain = configuration.chain[:-length]

		next_alternative = self.get_next_alternative(nonterminal, alternative_idx + 1)
		if next_alternative:
			configuration.state = Configuration.NORMAL_STATE
			next_alternative_idx = alternative_idx + 1
			next_alternative_right_side = self.alternatives[nonterminal][next_alternative_idx]
			configuration.history.append((nonterminal, next_alternative_idx))
			configuration.chain.extend(reversed(next_alternative_right_side))
		else:
			if (nonterminal == self.grammar.axiom and
				configuration.position == 0):
				raise ParseError('Parsing error')

			configuration.chain.append(nonterminal)	
			if isinstance(configuration.history[-1], Terminal):
				self.transform_terminals(configuration)
			self.try_alternative(configuration)		

	def get_next_alternative(self, nonterminal, idx):
		if len(self.alternatives[nonterminal]) > idx:
			return self.alternatives[nonterminal][idx]
		else:
			return None
		

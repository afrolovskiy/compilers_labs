class Symbol:
	def __init__(self, name):
		self.name = name
		self.is_nullable = False
		
	def __eq__(self, other):
		if not isinstance(other, Symbol):
			return False
		if self.name == other.name:
			return True
		return False
	
	def __hash__(self):
		return sum([ord(symbol) for symbol in self.name])

	def __str__(self):
		return self.name


class EmptySymbol(Symbol):
	def __init__(self):
		self.name = None
		self.is_nullable = False
		
	def __eq__(self, other):
		if isinstance(other, EmptySymbol):
			return True
		return False

	def __hash__(self):
		return 0
		
	def __str__(self):
		return "e"


class Terminal(Symbol):

	def __eq__(self, other):
		if not isinstance(other, Terminal):
			return False
		if self.name == other.name:
			return True
		return False

		
class Nonterminal(Symbol):

	def __init__(self, name, is_nullable=True):
		self.name = name
		self.is_nullable = is_nullable

	def __eq__(self, other):
		if not isinstance(other, Nonterminal):
			return False
		if self.name == other.name and self.is_nullable == other.is_nullable:
			return True
		return False

	def __hash__(self):
		result_hash = sum([ord(symbol) for symbol in self.name]) 
		if not self.is_nullable:
			return result_hash + 1000
		return result_hash

	def __str__(self):
		result_str = self.name
		if not self.is_nullable:
			return "nonnullable{%s}" % result_str
		return result_str

	def create_nonnullable_nonterminal(self):
		return Nonterminal(self.name, is_nullable=False)

	
class ComplexNonterminal(Nonterminal):
	def __init__(self, is_nullable=True):
		self.name = []
		self.is_nullable = is_nullable
		
	def __hash__(self):
		return sum([ord(symbol) for symbol in name])
	
	def __eq__(self, other):
		if not isinstance(other, ComplexNonterminal):
			return False
		if self.name == other.name:
			return True
		return False

	def __str__(self):
		result_str = "[%s]" % ''.join([str(symbol) for symbol in name])
		if not self.is_nullable:
			return "nonnullable{%s}" % result_str
		return result_str
		

class Rule:
	def __init__(self, left_side=[], right_side=[]):
		self.left_side = left_side
		self.right_side = right_side
		
	def __str__(self):
		return "%s -> %s" % (''.join([str(symbol) for symbol in self.left_side]),
							  ''.join([str(symbol) for symbol in self.right_side]))

	def is_empty(self):
		if self.right_side == [EmptySymbol()]:
			return True
		return False
							  

class Grammar:
	def __init__(self):
		self.axiom = None
		self.terminals = set()
		self.nonterminals = set()
		self.rules = []

	def __str__(self):
		result_str = "axiom: %s\n" % self.axiom
		result_str += "terminals: [%s]\n" % ','.join(
			[str(terminal) for terminal in self.terminals])
		result_str += "nonterminals: [%s]\n" % ','.join(
			[str(nonterminal) for nonterminal in self.nonterminals])
		result_str += "rules:\n"
		for rule in self.rules:
			result_str += "\t%s\n" % rule
		return result_str


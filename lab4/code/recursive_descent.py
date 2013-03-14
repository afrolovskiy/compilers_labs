
class RecursiveDescent:
	# Grammar rules:
	# S -> trueB			(S0)
	# S -> falseB			(S1)
	# S -> <identisier>B		(S2)
	# S -> ~A				(S3)
	# A -> trueB			(A0)
	# A -> false B			(A1)
	# A -> <identifier>B		(A2)
	# B -> &C				(B0)
	# B -> !C				(B1)
	# B -> empty			(B2)
	# C -> trueB			(C0)
	# C -> falseB			(C1)
	# C -> <identifier>B		(C2)
	# C -> ~A				(C3)

	LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	DIGITS = "0123456789"
	START_SYMBOLS = LETTERS +  '_'
	IDENTIFIER_SYMBOLS = LETTERS + DIGITS + '_'
	
	def __init__(self, chain):
		self.chain = chain	

	def parse(self):
		return self.S(0, [])

	def S(self, position, history):
		if position >= len(self.chain):
			print history
			raise Exception("Wrong string, position: %s" % position)
	
		if self.chain[position] == '~':
			history.append('S3')
			position += 1
			return self.A(position, history)						
		return self.process_identifier(position, history, 'S')

	def A(self, position, history):			
		return self.process_identifier(position, history, 'A')

	def B(self, position, history):
		if position >= len(self.chain):
			history.append('B2')	
			return history
		
		if self.chain[position] == '&':
			history.append('B0')
			position +=1
			return self.C(position, history)
		elif self.chain[position] == '!':
			history.append('B1')
			position +=1
			return self.C(position, history)

		print history
		raise Exception("Wrong string, position: %s" % position)

	def C(self, position, history):
		if position >= len(self.chain):
			print history
			raise Exception("Wrong string, position: %s" % position)

		if self.chain[position] == '~':
			history.append('C3')
			position += 1
			return self.A(position, history)						
	
		return self.process_identifier(position, history, 'C')
							
	def pick_identifier(self, position):
		""" Return next position after identifier"""
		if position >= len(self.chain):
			return position

		if self.chain[position] not in self.START_SYMBOLS:
			return position
		position +=1

		for idx in range(position, len(self.chain)):
			if self.chain[idx] not in self.IDENTIFIER_SYMBOLS:
				return idx		
		return len(self.chain)	

	def process_identifier(self, position, history, nonterminal):
		last_position = self.pick_identifier(position)
		if last_position == position:
			print history
			raise Exception("Wrong string, position: %s" % position)
	
		word = self.chain[position:last_position]
		if word == 'true':
			history.append('%s0' % nonterminal)
		elif word == 'false':
			history.append('%s1' % nonterminal)
		else:
			history.append('%s2' % nonterminal)
		return self.B(last_position, history)	
	
			

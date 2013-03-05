class WrongFileFormat(Exception):
	pass

class Algorithm:
	COMPASS = ['north', 'east', 'south', 'west']
	
	def __init__(self, fin, fout):
		self.compass = None
		self.prev_road = None
		self.fin = fin
		self.fout = fout
		self.ways = []
		
	def find(self):
		while True:
			length = int(self.fin.readline())
			if length == 0:
				return self.print_way()
			if length < 2:
				raise WrongFileFormat()
			self.process_direction(length)

	def process_direction(self, length):
		way = []
		self.process_start_instruction(way)
		self.process_travelling_instruction(way, length)
		self.process_end_instruction(way)
		way.reverse()
		self.ways.append(way)

	def process_start_instruction(self, way):
		s = self.fin.readline()

		if not s.startswith('Head'):
			raise WrongFileFormat()

		from_position = s.rindex(' from ')
		self.compass = s[len('Head '):from_position]
		self.prev_road = s[from_position + 6:]

		way.append('Arrive at %s' % self.prev_road)

	def process_travelling_instruction(self, way, length):
		for idx in range(1, length - 1):
			s = self.fin.readline()

			if s.startswith('Turn '):
				self.process_turn_instruction(way, s)
			elif s.startswith('Continue on '):
				self.process_continue_instruction(way, s)
			else:
				raise WringFileFormat()

	def  process_turn_instruction(self, way, s):
		at_position = s.rindex(' at ')
		lr = s[len('Turn '): at_position]
		road = s[at_position + 4:]

		way.append('Turn %s at %s' % (self.get_opposite_side(lr), self.prev_road))	

		self.prev_road = road
		self.compass = self.get_next_compass(lr)

	def process_continue_instruction(self, way, s):
		road = s[len('Continue on '):]
		way.append('Continue on %s' % self.prev_road)
		self.prev_road = road
		
	def process_end_instruction(self, way):
		s = self.fin.readline()
		if not s.startswith('Arrive at '):
			raise WrongFileFormat()
		road = s[len('Arrive at '):]
		way.append('Head %s from %s' % (self.get_opposite_compass(self.compass), road))

	def get_opposite_side(self, lr):
		if lr == 'left':
			return 'right'
		return 'left'

	def get_next_compass(self, lr):
		compass_idx = self.COMPASS.index(self.compass)
		if lr == 'left':
			return self.COMPASS[compass_idx - 1]
		return self.COMPASS[compass_idx + 1]

	def get_opposite_compass(self, compass):
		compass_idx = self.COMPASS.index(self.compass)
		return self.COMPASS[(compass_idx + 2) % 4]			
		
	def print_way(self):
		direction_idx = 1
		for way in self.ways:
			self.fout.writelines("Direction %s:\n" % direction_idx)
			self.fout.writelines(way)
			self.fout.writelines("\n")
			direction_idx += 1


Algorithm(open('input.txt'), open('output.txt', 'w')).find()
			

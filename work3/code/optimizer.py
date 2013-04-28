class Command(object):
	UNCONDITIONAL_JUMP = ['JUMP', ]
	CONDITIONAL_JUMPS = ['JZ', 'JNZ', 'JC', 'JNC']
	TWO_OPERAND_ARITHMETIC_CMDS = ['ADD', 'ADC', 'AND', 'OR', 'XOR']
	MOVE_DATA_CMDS = ['MOV', 'LD']
	ONE_OPERAND_ARITHMETIC_CMDS = ['NEG', 'INC', 'DEC']
	FLAG_CMDS = ['CLC', 'STC']
	LAST_CMD = ['RET', ]

	NONE_OPERAND_CMDS = FLAG_CMDS + LAST_CMD
	ONE_OPERAND_CMDS = UNCONDITIONAL_JUMP + CONDITIONAL_JUMPS + \
		ONE_OPERAND_ARITHMETIC_CMDS
	TWO_OPERAND_CMDS = TWO_OPERAND_ARITHMETIC_CMDS + \
		MOVE_DATA_CMDS

	def __init__(self, name=None, line_number=None):
		self.name = name
		self.line_number = line_number
		self.operands = []
		self.parents = []
		self.childs = []
	
	def add_parent(self, command):
		self.parents.append(command)

	def add_child(self, command):
		self.childs.append(command)

	def add_operand(self, operand):
		self.operands.append(operand)

	def add_operands(self, operands):
		self.operands.extend(operands)

	def __str__(self):
		# hard coded!
		if len(self.operands) == 1:
			return '%s %s %s' % (self.line_number, self.name, self.operands[0])
		if len(self.operands) == 2:
			return '%s %s %s,%s' % \
				(self.line_number, self.name, self.operands[0], self.operands[1])
		return '%s %s' % (self.line_number, self.name)

	@classmethod
	def get_success_condition(self, cmd):
		condition = Condition()
		if cmd == 'JZ':
			condition.add_flag(Flag(name='ZF', value=1))
		elif cmd == 'JNZ':
			condition.add_flag(Flag(name='ZF', value=0))
		elif cmd == 'JC':
			condition.add_flag(Flag(name='CF', value=1))
		elif cmd == 'JNC':
			condition.add_flag(Flag(name='CF', value=0))
		return condition

	@classmethod
	def get_failure_condition(self, cmd):
		condition = Condition()
		if cmd == 'JZ':
			condition.add_flag(Flag(name='ZF', value=0))
		elif cmd == 'JNZ':
			condition.add_flag(Flag(name='ZF', value=1))
		elif cmd == 'JC':
			condition.add_flag(Flag(name='CF', value=0))
		elif cmd == 'JNC':
			condition.add_flag(Flag(name='CF', value=1))
		return condition

	@classmethod
	def revert_command(self, cmd):
		# hard coded!
		if cmd.name == 'JZ':
			cmd.name = 'JNZ'
		elif cmd.name == 'JNZ':
			cmd.name = 'JZ'
		elif cmd.name == 'JC':
			cmd.name = 'JNC'
		elif cmd.name == 'JNC':
			cmd.name = 'JC'
			

class Context:

	def __init__(self):
		self.registers = {}
		self.flags = {}

	def add_register(self, name, register):
		self.registers[name] = register
			
	def add_flag(self, name, flag):
		self.flags[name] = flag


class Condition(Context):
	pass


class Register:
	BITS_COUNT = 8
	UNKNOWN_VALUE = -1
	
	def __init__(self, bits=None):
		self.bits = bits or [UNKNOWN_VALUE for _ in range(BITS_COUNT)]

	def set_bit(self, idx, value):
		self.bits[idx] = value

	@classmethod
	def number2bits(self, number):
		work = number
		bits = [0 for  _ in range(BITS_COUNT)]
		idx = 0
		while work:
			bits[idx]  = work % 2
			work = work / 2
			idx = idx + 1
		return bits

class FLAG:
	UNKNOWN_VALUE = -1
	
	def __init__(self, value=None):
		self.value = value or UNKNOWN_VALUE


class ProgrammGraphCommand(Command):
	
	def __init__(self, **kwargs):
		super(ProgrammGraphCommand, self).__init__(**kwargs)
		self.context = None
		self.condition = None

	def set_context(self, context):
		self.context = context

	def add_condition(self, condition):
		self.condition = condition

	def __str__(self):
		return super(ProgrammGraphCommand, self).__str__()


	def calculate_context(self, context=None):
		# hard coded!
		if context:
			if self.name == 'MOV':
				self.modify_mov_context(context)
			elif self.name == 'LD':
				self.modify_ld_context(context)
			elif self.name == 'ADD':
				self.modify_add_context(context)

		else:
			context = Context()
			if self.name == 'MOV':
				self.fill_initial_mov_context(context)
			elif self.name == 'LD':
				self.fill_initiali_ld_context(context)
			elif self.name == 'ADD':
				self.fill_initiali_add_context(context)
			elif self.name == 'NEG':
				self.fill_initial_neg_context(context)
			elif self.name == 'AND':
				self.fill_initial_and_context(context)
			elif self.name == 'OR':
				self.fill_initial_or_context(context)
			elif self.name == 'XOR':
				self.fill_initial_xor_context(context)
			elif self.name == 'CLC':
				self.fill_initial_clc_context(context)
			elif self.name == 'STC':
				self.fill_initial_stc_context(context)

	def modify_mov_context(self, context):
		pass		
	
	def fill_initial_mov_context(self, context):
		register = Register()
		context.add_register(cmd.operands[0], register)
		context.add_register(cmd.operands[1], register)

	def fill_initial_ld_context(self, context):
		register = Register(bits=Register.number2bits(cmd.operands[1]))
		context.add_register(cmd.operands[0], register)

	def fill_initial_add_context(self, context):
		if cmd.operands[0] == cmd.operands[1]:
			register = Register()	
				register.set_bit(idx=0, value=0)			
			context.add_register(name=cmd.operands[0], register)

	def fill_initial_neg_context(self, context):
		context.add_flag(name='CF', Flag(value=1))

	def fill_initial_and_context(self, context):
		context.add_flag(name='CF', Flag(value=0))

	def fill_initial_or_context(self, context):
		context.add_flag(name='CF', Flag(value=0))

	def fill_initial_xor_context(self, context):
		context.add_flag(name='CF', Flag(value=0))

	def fill_initial_clc_context(self, context):
		context.add_flag(name='CF', Flag(value=0))

	def fill_initial_stc_context(self, context):
		context.add_flag(name='CF', Flag(value=0))



class ProgrammGraph:

	def __init__(self):
		self.commands = []

	def add_command(self, command):
		self.commands.append(command)

	def remove_command(self, idx):
		del self.commands[idx]

	def __str__(self):
		return ''.join(['%s\n' % str(cmd) for cmd in self.commands])


class ProgrammGraphReader:

	def __init__(self):
		self.pg = None

	def read(self, filename):
		with open(filename, 'r') as fin:
			lines = [line.strip().split(' ') for line in fin]
		self.pg = ProgrammGraph()
		self.parse_lines(lines)
		self.connect_commands()
		return self.pg

	def parse_lines(self, lines):
		for line in lines[:-1]:
			cmd = self.parse_line(line);

	def parse_line(self, line):
		cmd = ProgrammGraphCommand(line_number=int(line[0]), name=line[1].strip())	
		if cmd.name in Command.TWO_OPERAND_CMDS:
			operands = line[2].split(',')
			if cmd.name == 'LD':
				operands[1] = int(operands[1])
			cmd.add_operands(operands)
		if cmd.name in Command.ONE_OPERAND_CMDS:
			operand = line[2]
			if cmd.name in Command.UNCONDITIONAL_JUMP or \
					cmd.name in Command.CONDITIONAL_JUMPS:
				operand = int(operand)
			cmd.add_operand(operand)
		self.pg.add_command(cmd)

	def connect_commands(self):
		for cmd in self.pg.commands:
			if cmd.name in Command.UNCONDITIONAL_JUMP:
				self.connect_unconditional_jump(cmd)
			elif cmd.name in Command.CONDITIONAL_JUMPS:
				self.connect_conditional_jump(cmd)
			elif cmd.name not in Command.LAST_CMD:
				self.connect_ordinary_command(cmd)

	def connect_unconditional_jump(self, cmd):
		child_cmd_idx = cmd.operands[0] - 1
		child_cmd = self.pg.commands[child_cmd_idx]
		cmd.add_child(child_cmd)
		child_cmd.add_parent(cmd)

	def connect_conditional_jump(self, cmd):
		success_child_cmd_idx = cmd.operands[0] - 1
		child_cmd = self.pg.commands[success_child_cmd_idx]
		cmd.add_child(child_cmd)
		child_cmd.add_parent(cmd)
		child_cmd.add_condition(Command.get_success_condition(cmd))

		failure_child_cmd_idx = cmd.line_number
		child_cmd = self.pg.commands[failure_child_cmd_idx]
		cmd.add_child(child_cmd)
		child_cmd.add_parent(cmd)
		child_cmd.add_condition(Command.get_failure_condition(cmd))

	def connect_ordinary_command(self, cmd):
		child_cmd_idx = cmd.line_number
		child_cmd = self.pg.commands[child_cmd_idx]
		cmd.add_child(child_cmd)
		child_cmd.add_parent(cmd)
	
					
class ProgrammGraphOptimizer(object):
	
	def __init__(self, pg):
		self.pg = pg

	def optimize(self):
		self.remove_unused_commands()
		self.modify_conditional_jumps()
		self.remove_useless_jumps()

	def remove_useless_jumps(self):
		useless_jump = self.find_useless_jump()
		while useless_jump:
			# renumber commands
			for cmd in self.pg.commands:				
				if cmd.line_number != useless_jump.line_number:
					if cmd.line_number > useless_jump.line_number:
						cmd.line_number = cmd.line_number - 1
					if cmd.name in Command.UNCONDITIONAL_JUMP and \
							cmd.operands[0] > useless_jump.line_number:
						cmd.operands[0] = cmd.operands[0] - 1
			# remove
			self.pg.remove_command(useless_jump.line_number - 1)
			# find next
			useless_jump = self.find_useless_jump()

	def find_useless_jump(self):
		for cmd in self.pg.commands:
			if cmd.name in Command.UNCONDITIONAL_JUMP and \
					len(cmd.childs[0].parents) == 1:
				return cmd
		return None

	def modify_conditional_jumps(self):
		conditional_jump, connection_cmd = self.find_special_conditional_jump()
		while conditional_jump:
			# renumber commands
			for cmd in self.pg.commands:				
				if cmd.line_number != conditional_jump.childs[1].line_number:
					if cmd.line_number > conditional_jump.line_number:
						cmd.line_number = cmd.line_number - 1
					if cmd.name in Command.UNCONDITIONAL_JUMP and \
							cmd.operands[0] > conditional_jump.line_number:
						cmd.operands[0] = cmd.operands[0] - 1
					if cmd.name in Command.CONDITIONAL_JUMPS and \
							cmd != conditional_jump and \
							cmd.operands[0] > conditional_jump.line_number:
						cmd.operands[0] = cmd.operands[0] - 1
			# remove useless jump
			conditional_jump.operands[0] = connection_cmd.line_number
			# change command
			Command.revert_command(conditional_jump)
			conditional_jump.line_number = connection_cmd.line_number
			old_child = conditional_jump.childs[1]
			conditional_jump.childs[1] = conditional_jump.childs[0]
			conditional_jump.childs[0] = connection_cmd
			pg.remove_command(old_child.line_number - 1)						
			# find next
			conditional_jump, connection_cmd = self.find_special_conditional_jump()
			
	def find_special_conditional_jump(self):
		for cmd in self.pg.commands:
			if cmd.name in  Command.CONDITIONAL_JUMPS and \
					cmd.childs[1].name in Command.UNCONDITIONAL_JUMP:
				connection_cmd = self.find_connection_command(cmd)
				if cmd.childs[1].childs[0].line_number == connection_cmd.line_number:
					return cmd, connection_cmd
		return None, None

	def find_connection_command(self, cmd):
		left_two_parent_commands = self.find_two_parent_commands(cmd.childs[0])
		rigth_two_parent_commands = self.find_two_parent_commands(cmd.childs[1])
		for left_cmd in left_two_parent_commands:
			for right_cmd in rigth_two_parent_commands:
				if left_cmd.line_number == right_cmd.line_number:
					return left_cmd
		raise Exception()			

	def find_two_parent_commands(self, cmd):
		two_parent_commands = []
		child_cmd = cmd
		while len(child_cmd.childs) > 0:
			if len(child_cmd.childs) == 2:
				two_parent_commands.extend(
					self.find_two_parent_commands(child_cmd.childs[0]))
				two_parent_commands.extend(
					self.find_two_parent_commands(child_cmd.childs[1]))
				return two_parent_commands
			child_cmd = child_cmd.childs[0]
			if len(child_cmd.parents) >= 2:
				two_parent_commands.append(child_cmd)
		return two_parent_commands
			
	def remove_unused_commands(self):
		used_commands = []
		cmd = self.pg.commands[0]
		cmd.calculate_context()
		used_commands.append(cmd)
		while cmd.name != 'RET':
			
	
		
			
		
				
		


pg = ProgrammGraphReader().read('input2.txt')
print str(pg)

ProgrammGraphOptimizer(pg).optimize()
print "optimized graph:"
print str(pg)
	

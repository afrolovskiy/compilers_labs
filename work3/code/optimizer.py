 #! /usr/bin/python
 # -*- coding: utf-8 -*-
import copy

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

class Register:
	BITS_COUNT = 8
	UNKNOWN_VALUE = -1
	UNKNOWN_BITS = [UNKNOWN_VALUE for _ in range(BITS_COUNT)]
	
	def __init__(self, bits=None):
		self.bits = bits or [self.UNKNOWN_VALUE for _ in range(self.BITS_COUNT)]

	def set_bit(self, idx, value):
		self.bits[idx] = value

	def get_bit(self, idx):
		return self.bits[idx]

	def has(self, value):
		for idx in range(BITS_COUNT):
			if self.bits[idx] == value:
				return True
		return False
	
	def value(self):
		return self.bits2number(self.bits, self.BITS_COUNT)

	def __str__(self):
		result = ''
		for idx in range(self.BITS_COUNT):
			if self.bits[idx] == self.UNKNOWN_VALUE:
				result += 'unknown '
			else:
				result += '%s ' % str(self.bits[idx])
		return result		

	@classmethod
	def bits2number(self, bits, count):
		value = 0
		for idx in range(count):
			if bits[idx] == self.UNKNOWN_VALUE:
				return self.UNKNOWN_VALUE
			value += bits[idx] * 2  ** idx
		return value

	@classmethod
	def number2bits(self, number):
		work = number
		bits = [0 for  _ in range(self.BITS_COUNT)]
		idx = 0
		while work:
			bits[idx]  = work % 2
			work = work / 2
			idx = idx + 1
		return bits

	@classmethod
	def and_bits(self, bits1, bits2):
		bits = [self.UNKNOWN_VALUE for _ in range(self.BITS_COUNT)]
		for idx in range(self.BITS_COUNT):
			if bits1[idx] == self.UNKNOWN_VALUE and \
					bits2 == self.UNKNOWN_VALUE:
				# UNKNOWN_VALUE & UNKNOWN_VALUE = UNKNOWN_VALUE
				bits[idx] = self.UNKNOWN_VALUE
			else:
				# x & 1 = x, x & 0 = 0
				bits[idx] = bits1[idx] * bits2[idx]
		return bits

	@classmethod
	def or_bits(self, bits1, bits2):
		bits = [UNKNOWN_VALUE for _ in range(BITS_COUNT)]
		for idx in range(BITS_COUNT):
			if bits1[idx] == self.UNKNOWN_VALUE and \
					bits2[idx] == self.UNKNOWN_VALUE:
				# UNKNOWN_VALUE | UNKNOWN_VALUE  = UNKNOWN_VALUE
				bits[idx] = UNKNOWN_VALUE
			elif bits1[idx] == 1 or bits2[idx] == 1:
				# x | 1  = 1
				bits[idx] = 1
			elif bits1[idx] == 0 and bits2[idx] == 0:
				# 0 | 0 = 0
				bits[idx] = 0
			else:
				# x | 0 = x
				bits[idx] = self.UNKNOWN_VALUE
		return bits

	@classmethod
	def xor_bits(self, bits1, bits2):
		bits = [UNKNOWN_VALUE for _ in range(BITS_COUNT)]
		for idx in range(BITS_COUNT):
			if bits1[idx] == UNKNOWN_VALUE or bits2[idx] == UNKNOWN_VALUE:
				bits[idx] = UNKNOWN_VALUE
			else:
				bits[idx] = bits1[idx] ^ bits2[idx]
		return bits

	@classmethod
	def left_shift(self, bits):
		for idx in reversed(range(self.BITS_COUNT - 1)):
			bits[idx + 1] = bits[idx]
		bits[0] = 0
		return bits

	@classmethod
	def begin_known_bits(self, bits):
		count = 0
		for idx in range(len(bits)):
			if bits[idx] == UNKNOWN_VALUE:
				break
			count = count + 1
		return count

	@classmethod
	def sum(self, bits1, bits2):
		bkb1 = Register.begin_known_bits(bits1)
		bkb2 = Register.begin_known_bits(bits2)
		bkb = min([bkb1, bkb2])
		
		v1 = Register.bits2number(bits1[:bkb])
		v2 = Register.bits2number(bits2[:bkb])
		bits = Register.number2bits(v1 + v2)
		
		return bits[:bkb] + Register.UNKNOWN_BITS[bkb:]

	@classmethod
	def inc_bits(self, bits1):
		# TODO
		pass

	@classmethod
	def dec_bits(self, bits1):
		# TODO
		pass


class Flag:
	UNKNOWN_VALUE = -1
	
	def __init__(self, value=None):
		self.value = value or self.UNKNOWN_VALUE

	def __str__(self):
		if self.value == self.UNKNOWN_VALUE:
			return 'unknown'
		return str(self.value)
			

class Context:

	def __init__(self):
		self.registers = {}
		self.flags = {}

	def set_register(self, name, register):
		self.registers[name] = register

	def set_register_bits(self, name, bits):
		reg = self.registers.get(name)
		if not reg:
			reg = Register()
			self.set_register(name, reg)
		reg.bits = bits
			
	def set_flag(self, name, flag):
		self.flags[name] = flag

	def set_flag_value(self, name, value):
		flag = self.flags.get(name)
		if not flag:
			flag = Flag()
			self.set_flag(name, flag)
		flag.value = value

	def __str__(self):
		result = 'flags:\n'
		for fname, fvalue in self.flags.items():
			result += '%s: %s\n' % (fname, fvalue)

		result += 'registers:\n'
		for rname, rvalue in self.registers.items():
			result += '%s: %s\n' % (rname, rvalue)

		return result
		

class Condition(Context):
	pass


class ProgrammGraphCommand(Command):
	
	def __init__(self, **kwargs):
		super(ProgrammGraphCommand, self).__init__(**kwargs)
		self.context = Context()
		self.condition = None

	def set_context(self, context):
		self.context = context

	def add_condition(self, condition):
		self.condition = condition

	def __str__(self):
		return super(ProgrammGraphCommand, self).__str__()

	def calculate_context(self, context=None):
		print 'calculate context'
		if not context:
			context = Context()
		if self.name == 'MOV':
			self.fill_mov_context(context)
		elif self.name == 'LD':
			self.fill_ld_context(context)
		elif self.name == 'ADD':
			self.fill_add_context(context)
		elif self.name == 'ADC':
			self.fill_adc_context(context)
		elif self.name == 'NEG':
			self.fill_neg_context(context)
		elif self.name == 'AND':
			self.fill_and_context(context)
		elif self.name == 'OR':
			self.fill_or_context(context)
		elif self.name == 'XOR':
			self.fill_xor_context(context)
		elif self.name == 'INC':
			self.fill_inc_context(context)
		elif self.name == 'DEC':
			self.fill_dec_context(context)
		elif self.name == 'CLC':
			self.fill_clc_context(context)
		elif self.name == 'STC':
			self.fill_stc_context(context)

	def fill_mov_context(self, context):
		reg2 = context.registers.get(self.operands[1])
		if not reg2:
			reg2 = Register()
			context.set_register(self.operands[1], reg2)
		context.set_register(self.operands[0], reg2)
	
	def fill_ld_context(self, context):
		context.set_register_bits(self.operands[0], Register.number2bits(self.operands[1]))

	def fill_add_context(self, context):
		print 'calculate add context'
		# TODO: refactoring
		# bad code: i wanna sleep!
		# warning: hard code!!
		if self.operands[0] == self.operands[1]:
			reg = context.registers.get(self.operands[0])
			if not reg:
				bits = Register.UNKNOWN_BITS
			else:
				bits = reg.bits
			context.set_register_bits(self.operands[0], Register.left_shift(bits))
			reg = context.registers[self.operands[0]]
			# TODO: definition of this flag value
			context.set_flag_value(name='CF', value=Flag.UNKNOWN_VALUE)			
			# zf definition
			reg_value = reg.value()
			if reg_value == Register.UNKNOWN_VALUE:
				context.set_flag_value(name='ZF', value=Flag.UNKNOWN_VALUE)
			else:
				value = 1 if reg_value == 0 else 0
				context.set_flag_value(name='ZF', value=value)
		else:
			reg1 = context.registers.get(self.operands[0])
			reg2 = context.registers.get(self.operands[1])
			if reg1 and reg2:
				reg1_value = reg1.value()
				reg2_value = reg2.value()
				if reg1_value != Register.UNKNOWN_VALUE and \
						reg2_value != Register.UNKNOWN_VALUE:
					v = reg1_value + reg2_value
					context.set_flag_value(name='CF', value=v / 256)	
					v = v % 256
					context.set_register_value(
						name=self.operands[0], value=Register.number2bits(v))
					zf_value = 1 if v == 0 else 0
					context.set_flag_value(name='ZF', value=zf_value)	
				else:
					# TODO: this case
					context.set_register_value(
						name=self.operands[0], value=Register.UNKNOWN_BITS)
					context.set_flag_value(
						name='CF', value=FLAG.UNKNOWN_VALUE)			
					context.set_flag_value(
						name='ZF', value=FLAG.UNKNOWN_VALUE)

			else:
				context.set_register_value(
					name=self.operands[0], value=Register.UNKNOWN_BITS)
				context.set_flag_value(
					name='CF', value=FLAG.UNKNOWN_VALUE)			
				context.set_flag_value(
					name='ZF', value=FLAG.UNKNOWN_VALUE)

	def fill_adc_context(self, context):
		# TODO
		pass

	def fill_neg_context(self, context):
		reg = context.registers.get(self.operands[0])
		if reg:
			for idx in range(Register.BITS_COUNT):
				if reg.get_bit(idx) != Register.UNKNOWN_VALUE:
					reg.set_bit(idx, 1 - reg.get_bit(idx))

			reg_value = reg.value()
			if reg_value == Register.UNKNOWN_VALUE:
				value = FLAG.UNKNOWN_VALUE
			else:
				value = 1 if reg_value == 0 else 0
			context.set_flag_value(name='ZF', value=value)
		else:
			context.set_flag_value(name='ZF', value=FLAG.UNKNOWN_VALUE)
							
		context.set_flag_value(name='CF', value=1)

	def fill_and_context(self, context):
		self.fill_bitwise_operation_context(context, Register.and_bits)

	def fill_or_context(self, context):
		self.fill_bitwise_operation_context(context, Register.or_bits)

	def fill_xor_context(self, context):
		self.fill_bitwise_operation_context(context, Register.xor_bits)

	def fill_bitwise_operation_context(self, context, operation):
		reg1 = context.registers.get(self.operands[0])
		bits1 = reg1.bits if reg1 else Register.UNKNOWN_BITS
		reg2 = context.registers.get(self.operands[1])
		bits2 = reg2.bits if reg2 else Register.UNKNOWN_BITS
		context.set_register_bits(self.operands[0], operation(bits1, bits2))
		
		reg1 = context.registers.get(self.operands[0])
		reg1_value = reg1.value()
		if reg1_value == Register.UNKNOWN_VALUE:
			context.set_flag_value(name='ZF', value=Flag.UNKNOWN_VALUE)
		else:
			value = 1 if reg1_value == 0 else 0
			context.set_flag_value(name='ZF', value=value)
		
		context.set_flag_value(name='CF', value=0)

	def fill_inc_context(self, context):
		# TODO
		pass

	def fill_dec_context(self, context):
		# TODO
		pass

	def fill_clc_context(self, context):
		context.set_flag_value(name='CF', value=0)

	def fill_stc_context(self, context):
		context.set_flag_value(name='CF', value=1)


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
		# 4 main cases:
		self.remove_unused_commands()
		#self.remove_useless_conditional_jumps() TODO: !!
		#self.modify_conditional_jumps()
		#self.remove_useless_jumps()

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
		cmd = self.pg.commands[0]
		cmd.calculate_context()
		using_commands = self.find_using_commands(cmd)
		print [str(cmd.line_number) for cmd in using_commands]


	def find_using_commands(self, cmd):
		# it is not optimal way for using commands seraching!!!
		commands = set([])
		while True:
			print cmd.context
			if cmd.name in ['JZ', 'JNZ', 'JC', 'JNC']:
				commands.add(cmd)
				zf = cmd.context.flags.get('ZF')
				cf = cmd.context.flags.get('CF')
				if cmd.name == 'ZF' and zf and zf.value == 1:
					commands.update(
						self.find_using_commands(copy.deepcopy(cmd.childs[0])))
				elif cmd.name == 'ZF' and zf and zf.value == 0:
					commands.update(
						self.find_using_commands(copy.deepcopy(cmd.childs[1])))
				elif cmd.name == 'CF' and cf and cf.value == 1:
					commands.update(
						self.find_using_commands(copy.deepcopy(cmd.childs[0])))
				elif cmd.name == 'CF' and cf and cf.value == 0:
					commands.update(
						self.find_using_commands(copy.deepcopy(cmd.childs[1])))
				else:
					commands.update(self.find_using_commands(
						copy.deepcopy(cmd.childs[0])))
					commands.update(self.find_using_commands(
						copy.deepcopy(cmd.childs[1])))
				return commands
			else:
				commands.add(cmd)
				if cmd.name == 'RET':
					break
				cmd.childs[0].calculate_context(cmd.context)				
				cmd = cmd.childs[0]
		return commands
			
	
		
			
		
				
		


pg = ProgrammGraphReader().read('input1.txt')
print str(pg)

ProgrammGraphOptimizer(pg).optimize()
print "optimized graph:"
print str(pg)
	

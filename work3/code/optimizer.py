 #! /usr/bin/python
 # -*- coding: utf-8 -*-
import copy

class Command(object):
	UNKNOWN_VALUE = -1

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

	def __init__(self, name=None):
		self.name = name
		self.operands = []


	def add_operand(self, operand):
		self.operands.append(operand)

	def add_operands(self, operands):
		self.operands.extend(operands)

	def is_conditional_jump(self):
		return self.name in self.CONDITIONAL_JUMPS

	def is_unconditional_jump(self):
		return self.name in self.UNCONDITIONAL_JUMP

	def is_jump(self):
		return self.is_unconditional_jump() or self.is_conditional_jump()

	def __str__(self):
		# hard coded!
		if len(self.operands) == 1:
			return '%s %s %s' % (self.line_number, self.name, self.operands[0])
		if len(self.operands) == 2:
			return '%s %s %s,%s' % \
				(self.line_number, self.name, self.operands[0], self.operands[1])
		return '%s %s' % (self.line_number, self.name)
	
	def print2str(self):
		return str(self)

	def __eq__(self, other):
		if self.name != other.name:
			return False
		
		if len(self.operands) != len(other.operands):
			return False

		for idx in range(len(self.operands)):
			if self.operands[idx] != other.operands[idx]:
				return False

		return True
		
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
		return self.bits2number(self.bits)

	def __str__(self):
		result = ''
		for idx in range(self.BITS_COUNT):
			if self.bits[idx] == self.UNKNOWN_VALUE:
				result += 'unknown '
			else:
				result += '%s ' % str(self.bits[idx])
		return result		

	@classmethod
	def bits2number(self, bits):
		value = 0
		for idx in range(len(bits)):
			if bits[idx] == self.UNKNOWN_VALUE:
				return self.UNKNOWN_VALUE
			value += bits[idx] * 2  ** idx
		return value

	@classmethod
	def number2bits(self, number):
		work = number
		bits = [0 for _ in range(self.BITS_COUNT)]
		idx = 0
		while work:
			bits[idx] = work % 2
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
			result += '%s: %s\n' % (fname, str(fvalue))

		result += 'registers:\n'
		for rname, rvalue in self.registers.items():
			result += '%s: %s\n' % (rname, str(rvalue))

		return result


class ProgrammGraphCommand(Command):
	
	def __init__(self, name=None, line_number=None):
		super(ProgrammGraphCommand, self).__init__(name)
		self.context = Context()
		self.line_number = line_number
		self.parents = []
		self.childs = []

	def set_context(self, context):
		self.context = context
	
	def clean_parents(self):
		self.parents = []	

	def add_parent(self, command):
		self.parents.append(command)

	def clean_childs(self):
		self.childs = []

	def add_child(self, command):
		self.childs.append(command)

	def __str__(self):
		return super(ProgrammGraphCommand, self).__str__()

	def print2str(self):
		result = super(ProgrammGraphCommand, self).print2str()
		if self.childs:
			result += '\nchilds:\n'
			result += self.childs2str()
		if self.parents:
			result += '\nparents:\n'
			result += self.parents2str()
		return result

	def childs2str(self):
		result = ''
		for child in self.childs:
			result += '\t%s\n' % str(child)
		return result

	def parents2str(self):
		result = ''
		for parent in self.parents:
			result += '\t%s\n' % str(parent)
		return result

	def __eq__(self, other):
		if not super(ProgrammGraphCommand, self).__eq__(other):
			return False

		if self.line_number != other.line_number:
			return False

		return True

	def calculate_context(self, context=None):
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
		self.context = context

	def fill_mov_context(self, context):
		reg2 = context.registers.get(self.operands[1])
		if not reg2:
			reg2 = Register()
			context.set_register(self.operands[1], reg2)
		context.set_register(self.operands[0], reg2)
	
	def fill_ld_context(self, context):
		context.set_register_bits(self.operands[0], Register.number2bits(self.operands[1]))

	def fill_add_context(self, context):
		reg1 = context.registers.get(self.operands[0])
		reg2 = context.registers.get(self.operands[1])
		if reg1 and reg2 and reg1.value(0) != self.UNKNOWN_VALUE and \
				reg2.value() != self.UNKNOWN_VALUE:
			result = reg1.value() + reg2.value()
			context.set_flag_value(name='CF', value=result % 256)
			context.set_register_bits(name=self.operands[0], 
							     bits=Register.number2bits(result / 256))
		else:
			# try to apply heuristics
			if self.operands[0] == self.operands[1]:
				if not reg1:
					reg1 = Register()
				context.set_register_bits(name=self.operands[0],
								     bits=Register.left_shift(reg1.bits))
			context.set_flag_value(name='CF', value=self.UNKNOWN_VALUE)
			# TODO: apply others!
			
		if reg1 and reg1.value() == 0:
			context.set_flag_value(name='ZF', value=1)
		elif reg1 and reg1.value() == 1:
			context.set_flag_value(name='ZF', value=0)
		else:
			context.set_flag_value(name='ZF', value=self.UNKNOWN_VALUE)

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

	def __str__(self):
		return ''.join(['%s\n' % str(cmd) for cmd in self.commands])

	def print2str(self):
		result = ''
		for cmd in self.commands:
			result += '%s\n' % cmd.print2str()
		return result

	def remove_command(self, removed_cmd):
		self.renumber_lines(removed_cmd)
		self.exclude_cmd(removed_cmd)
		self.renumber_jumps()

	def renumber_lines(self, removed_cmd):
		for cmd in self.commands:
			if cmd.line_number > removed_cmd.line_number:
				cmd.line_number = cmd.line_number - 1

	def exclude_cmd(self, removed_cmd):
		if removed_cmd.childs and removed_cmd.parents:
			if removed_cmd.parents[0].childs:
				removed_cmd.parents[0].childs[0] = removed_cmd.childs[0]
			if removed_cmd.childs[0].parents:
				removed_cmd.childs[0].parents[0] = removed_cmd.parents[0]
		
		if removed_cmd.childs:
			for child in removed_cmd.childs:
				if removed_cmd in child.parents:
					child.parents.remove(removed_cmd)

		if removed_cmd.parents:
			for parent in removed_cmd.parents:
				if removed_cmd in parent.childs:
					parent.childs.remove(removed_cmd)		

		self.commands.remove(removed_cmd)
		
	def renumber_jumps(self):
		for cmd in self.commands:
			if cmd.is_jump():
				cmd.operands[0] = cmd.childs[0].line_number


class ProgrammGraphReader:

	def __init__(self, pg=None):
		self.pg = pg

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

		failure_child_cmd_idx = cmd.line_number
		child_cmd = self.pg.commands[failure_child_cmd_idx]
		cmd.add_child(child_cmd)
		child_cmd.add_parent(cmd)

	def connect_ordinary_command(self, cmd):
		child_cmd_idx = cmd.line_number
		child_cmd = self.pg.commands[child_cmd_idx]
		cmd.add_child(child_cmd)
		child_cmd.add_parent(cmd)
	

class BaseOptimizer(object):
	
	def __init__(self, pg):
		self.pg = pg

	def execute(self):
		raise NotImplementedError()


class UselessUnconditionalJumpRemover(BaseOptimizer):

	def execute(self):
		useless_jump = self.find_useless_jump()
		while useless_jump:
			self.pg.remove_command(useless_jump)
			useless_jump = self.find_useless_jump()

	def find_useless_jump(self):
		for cmd in self.pg.commands:
			if self.is_useless_jump(cmd):
				return cmd
		return None

	def is_useless_jump(self, cmd):
		return cmd.is_unconditional_jump() and len(cmd.childs) == 1 and \
			len(cmd.childs[0].parents) == 1 and len(cmd.parents) == 1 and \
			not cmd.parents[0].is_conditional_jump()

class ConditionalJumpModifier(BaseOptimizer):

	def execute(self):
		conditional_jump = self.find_special_conditional_jump()
		while conditional_jump:
			self.remove_useless_jump(conditional_jump)
			conditional_jump = self.find_special_conditional_jump()
			
	def find_special_conditional_jump(self):
		for cmd in self.pg.commands:
			if cmd.is_conditional_jump() and cmd.childs[1].is_unconditional_jump():
				return cmd
		return None

	def remove_useless_jump(self, conditional_jump):
		removed_cmd = conditional_jump.childs[1]
		for cmd in self.pg.commands:
			if cmd.line_number > removed_cmd.line_number:
				cmd.line_number = cmd.line_number - 1
			if cmd.is_jump() and cmd.operands[0] > removed_cmd.line_number:
				cmd.operands[0] = cmd.operands[0] - 1
			
		conditional_jump.childs[1] = conditional_jump.childs[1].childs[0]
		conditional_jump.operands[0] = conditional_jump.childs[1].line_number
		conditional_jump.childs[0], conditional_jump.childs[1] = \
			conditional_jump.childs[1], conditional_jump.childs[0]
		Command.revert_command(conditional_jump)
		self.pg.commands.remove(removed_cmd)


class UselessConditionalJumpRemover(BaseOptimizer):

	def execute(self):
		for cmd in self.pg.commands:
			if self.is_useless_conditional_jump(cmd):
				self.pg.remove_command(cmd)

	def is_useless_conditional_jump(self, cmd):
		return  cmd.is_conditional_jump() and \
			cmd.childs[0].line_number == cmd.line_number + 1


class UnusedCommandsRemover(BaseOptimizer):

	def execute(self):
		cmd = self.pg.commands[0]
		cmd.calculate_context()
	
		unusing_cmds= self.find_unusing_commands(cmd)
		self.modify_jumps(unusing_cmds)
		for cmd in unusing_cmds:
			self.pg.remove_command(cmd)
		
	def find_unusing_commands(self, cmd):
		using_commands = self.find_using_commands(cmd)
		return filter(
			lambda x: x.line_number not in [cmd.line_number for cmd in using_commands], 
			self.pg.commands)
		
	def find_using_commands(self, cmd):
		# it is not optimal way for using commands seraching!!!
		commands = set([])
		while True:
			commands.add(cmd)
			if cmd.is_conditional_jump():				
				zf = cmd.context.flags.get('ZF')
				cf = cmd.context.flags.get('CF')
				if (cmd.name == 'JZ' and zf and zf.value == 1) or \
						(cmd.name == 'JNZ' and zf and zf.value == 0):
					commands.update(
						self.find_using_commands(cmd.childs[0]))					
				elif (cmd.name == 'JZ' and zf and zf.value == 0) or \
						(cmd.name == 'JNZ' and zf and zf.value == 1):
					commands.update(
						self.find_using_commands(cmd.childs[1]))
				elif (cmd.name == 'JC' and cf and cf.value == 1) or \
						(cmd.name == 'JNC' and cf and cf.value == 0):
					commands.update(
						self.find_using_commands(cmd.childs[0]))
				elif (cmd.name == 'JC' and cf and cf.value == 0) or \
						(cmd.name == 'JNC' and cf and cf.value == 1):
					commands.update(
						self.find_using_commands(cmd.childs[1]))
				else:
					context = copy.deepcopy(cmd.context)
					commands.update(self.find_using_commands(
						copy.deepcopy(cmd.childs[0])))
					cmd.context = context
					commands.update(self.find_using_commands(
						copy.deepcopy(cmd.childs[1])))
				return commands
			else:
				if cmd.name == 'RET':
					break
				cmd.childs[0].calculate_context(cmd.context)				
				cmd = cmd.childs[0]
		return commands

	def modify_jumps(self, unusing_cmds):
		for cmd in self.pg.commands:
			if cmd.is_conditional_jump():
				if cmd.childs[0] in unusing_cmds:
					cmd.name = 'JUMP'
					cmd.operands[0] = cmd.childs[1].line_number
					cmd.childs[0].parents.remove(cmd)
					cmd.childs.remove(cmd.childs[0])
				elif cmd.childs[1] in unusing_cmds:
					cmd.name = 'JUMP'
					cmd.operands[0] = cmd.childs[0].line_number
					cmd.childs[1].parents.remove(cmd)
					cmd.childs.remove(cmd.childs[1])


class Optimizer(BaseOptimizer):
	
	def execute(self):
		UnusedCommandsRemover(self.pg).execute()
		ConditionalJumpModifier(self.pg).execute()
		UselessUnconditionalJumpRemover(self.pg).execute()
		UselessConditionalJumpRemover(self.pg).execute()


pg = ProgrammGraphReader().read('input21.txt')
print str(pg)

Optimizer(pg).execute()
print "optimized graph:\n", str(pg)

with  open("output.txt", "w") as fout:
	fout.write(str(pg))


#!/usr/bin/env python

from pwn import *

class CPU:

	def __init__(self):

		self.state = State()

	def ops(self):

		names = [ m for m in dir(self) if m.startswith("op_") ]
		methods = { n: getattr(self, n) for n in names }
		return methods

	def set_state(self, state):
		self.state.set(state)

	def op_addr(self, args):

		log.debug("_addr_: add REG_A to REG_B and store in REG_C")

		a = self.state.reg[args[0]]
		b = self.state.reg[args[1]]
		r = a + b

		c = args[2]
		self.state.reg[c] = r
		return 

	def op_addi(self, args):

		log.debug("_addi_: add REG_A to ARG_B and store in REG_C")

		a = self.state.reg[args[0]]
		b = args[1]
		r = a + b

		c = args[2]
		self.state.reg[c] = r
		return 

	def op_mulr(self, args):

		log.debug("_mulr_: multiply REG_A and REG_B and store in REG_C")

		a = self.state.reg[args[0]]
		b = self.state.reg[args[1]]
		r = a * b

		c = args[2]
		self.state.reg[c] = r
		return

	def op_muli(self, args):

		log.debug("_muli_: multiply REG_A and ARG_B and store in REG_C")

		a = self.state.reg[args[0]]
		b = args[1]
		r = a * b

		c = args[2]
		self.state.reg[c] = r
		return

	def op_banr(self, args):

		log.debug("_banr_: bitwise and REG_A and REG_B and store in REG_C")

		a = self.state.reg[args[0]]
		b = self.state.reg[args[1]]
		r = a & b

		c = args[2]
		self.state.reg[c] = r
		return

	def op_bani(self, args):

		log.debug("_bani_: bitwise and REG_A and ARG_B and store in REG_C")

		a = self.state.reg[args[0]]
		b = args[1]
		r = a & b

		c = args[2]
		self.state.reg[c] = r
		return

	def op_borr(self, args):

		log.debug("_borr_: bitwise or REG_A with REG_B and store in REG_C")

		a = self.state.reg[args[0]]
		b = self.state.reg[args[1]]
		r = a | b

		c = args[2]
		self.state.reg[c] = r
		return

	def op_bori(self, args):

		log.debug("_bori_: bitwise or REG_A with ARG_B and store in REG_C")

		a = self.state.reg[args[0]]
		b = args[1]
		r = a | b

		c = args[2]
		self.state.reg[c] = r
		return

	def op_setr(self, args):

		log.debug("_setr_: copies contents of REG_A into REG_C")

		r = self.state.reg[args[0]]

		c = args[2]
		self.state.reg[c] = r
		return

	def op_seti(self, args):

		log.debug("_seti_: copies contents of ARG_A into REG_C")

		r = args[0]

		c = args[2]
		self.state.reg[c] = r
		return

	def op_gtir(self, args):

		log.debug("_gtir_: sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.")

		a = args[0]
		b = self.state.reg[args[1]]
		r = 1 if a > b else 0

		c = args[2]
		self.state.reg[c] = r
		return

	def op_gtri(self, args):

		log.debug("_gtri_: sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.")

		a = self.state.reg[args[0]]
		b = args[1]
		r = 1 if a > b else 0

		c = args[2]
		self.state.reg[c] = r
		return

	def op_gtrr(self, args):

		log.debug("_gtir_: sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.")

		a = self.state.reg[args[0]]
		b = self.state.reg[args[1]]
		r = 1 if a > b else 0

		c = args[2]
		self.state.reg[c] = r
		return

	def op_eqir(self, args):

		log.debug("_eqir_: sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.")

		a = args[0]
		b = self.state.reg[args[1]]
		r = 1 if a == b else 0

		c = args[2]
		self.state.reg[c] = r
		return

	def op_eqri(self, args):

		log.debug("_eqri_: sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.")

		a = self.state.reg[args[0]]
		b = args[1]
		r = 1 if a == b else 0

		c = args[2]
		self.state.reg[c] = r
		return

	def op_eqrr(self, args):

		log.debug("_eqir_: sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.")

		a = self.state.reg[args[0]]
		b = self.state.reg[args[1]]
		r = 1 if a == b else 0

		c = args[2]
		self.state.reg[c] = r
		return

class State:

	def __init__(self, instr = None, state=None):
		
		# the cpu has 4 registers
		if instr:
			instr = instr.replace("[", "")
			instr = instr.replace("]", "")
			self.reg = map(lambda x: int(x), instr.split(','))
		else:
			self.reg = [ 0 for i in range(4) ]
			if state:
				self.set(state)

	def __repr__(self):

		return "[{}]".format(", ".join(map(lambda x: str(x), self.reg)))

	def set(self, state):
	
		for i in range(len(self.reg)):
			self.reg[i] = state.reg[i]

	def clear(self):
		
		for r in self.reg:
			r = 0

class Operation:

	def __init__(self, instr):
		
		[ self.opcode, self.inputs ] = instr.split(' ')

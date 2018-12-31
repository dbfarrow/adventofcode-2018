#!/usr/bin/env python

from pwn import *

NUM_REGS = 6

class CPU:

	def __init__(self):

		self.reg = [ 0 for i in range(NUM_REGS) ]
		self.ip = 0
		self.rip = None

		names = [ m for m in dir(self) if m.startswith("op_") ]
		self.methods = { n: getattr(self, n) for n in names }

	def do(self, method, args):
	
		if self.rip == None:
			raise Exception("instruction pointer not mapped to a register yet: {}".format(self.rip))

		# move the instruction pointer into the mapped register
		self.reg[self.rip] = self.ip

		# now do the method
		#log.debug("{}({})".format(method, args))
		m = self.methods["op_{}".format(method)]
		a = map(lambda x: int(x), args) 
		m(a)

		# and copy the mapped register back to the instruction
		# pointer and increment it one
		self.ip = self.reg[self.rip] + 1
		

	def op_addr(self, args):

		#log.debug("_addr_: add REG_A to REG_B and store in REG_C")

		a = self.reg[args[0]]
		b = self.reg[args[1]]
		r = a + b

		c = args[2]
		self.reg[c] = r
		return 

	def op_addi(self, args):

		#log.debug("_addi_: add REG_A to ARG_B and store in REG_C")

		a = self.reg[args[0]]
		b = args[1]
		r = a + b

		c = args[2]
		self.reg[c] = r
		return 

	def op_mulr(self, args):

		#log.debug("_mulr_: multiply REG_A and REG_B and store in REG_C")

		a = self.reg[args[0]]
		b = self.reg[args[1]]
		r = a * b

		c = args[2]
		self.reg[c] = r
		return

	def op_muli(self, args):

		#log.debug("_muli_: multiply REG_A and ARG_B and store in REG_C")

		a = self.reg[args[0]]
		b = args[1]
		r = a * b

		c = args[2]
		self.reg[c] = r
		return

	def op_banr(self, args):

		#log.debug("_banr_: bitwise and REG_A and REG_B and store in REG_C")

		a = self.reg[args[0]]
		b = self.reg[args[1]]
		r = a & b

		c = args[2]
		self.reg[c] = r
		return

	def op_bani(self, args):

		#log.debug("_bani_: bitwise and REG_A and ARG_B and store in REG_C")

		a = self.reg[args[0]]
		b = args[1]
		r = a & b

		c = args[2]
		self.reg[c] = r
		return

	def op_borr(self, args):

		#log.debug("_borr_: bitwise or REG_A with REG_B and store in REG_C")

		a = self.reg[args[0]]
		b = self.reg[args[1]]
		r = a | b

		c = args[2]
		self.reg[c] = r
		return

	def op_bori(self, args):

		#log.debug("_bori_: bitwise or REG_A with ARG_B and store in REG_C")

		a = self.reg[args[0]]
		b = args[1]
		r = a | b

		c = args[2]
		self.reg[c] = r
		return

	def op_setr(self, args):

		#log.debug("_setr_: copies contents of REG_A into REG_C")

		r = self.reg[args[0]]

		c = args[2]
		self.reg[c] = r
		return

	def op_seti(self, args):

		#log.debug("_seti_: copies contents of ARG_A into REG_C")

		r = args[0]

		c = args[2]
		self.reg[c] = r
		return

	def op_gtir(self, args):

		#log.debug("_gtir_: sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.")

		a = args[0]
		b = self.reg[args[1]]
		r = 1 if a > b else 0

		c = args[2]
		self.reg[c] = r
		return

	def op_gtri(self, args):

		#log.debug("_gtri_: sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.")

		a = self.reg[args[0]]
		b = args[1]
		r = 1 if a > b else 0

		c = args[2]
		self.reg[c] = r
		return

	def op_gtrr(self, args):

		#log.debug("_gtir_: sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.")

		a = self.reg[args[0]]
		b = self.reg[args[1]]
		r = 1 if a > b else 0

		c = args[2]
		self.reg[c] = r
		return

	def op_eqir(self, args):

		#log.debug("_eqir_: sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.")

		a = args[0]
		b = self.reg[args[1]]
		r = 1 if a == b else 0

		c = args[2]
		self.reg[c] = r
		return

	def op_eqri(self, args):

		#log.debug("_eqri_: sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.")

		a = self.reg[args[0]]
		b = args[1]
		r = 1 if a == b else 0

		c = args[2]
		self.reg[c] = r
		return

	def op_eqrr(self, args):

		#log.debug("_eqir_: sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.")

		a = self.reg[args[0]]
		b = self.reg[args[1]]
		r = 1 if a == b else 0

		c = args[2]
		self.reg[c] = r
		return

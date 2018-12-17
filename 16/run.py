#!/usr/bin/env python

import argparse
from pwn import *
import time

from cpu import *

########################################################################
#
# boilerplate script setup
#
# command line arguments
CMDLINE = None 

def parse_cmdline():
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 16")
	parser.add_argument('-t', '--testing', action='store_true', default=False)
	parser.add_argument('-v', '--verbose', action='store_true', default=False)
	parser.add_argument('-p', '--part')
	global CMDLINE 
	CMDLINE = parser.parse_args()

	context.log_level = 'debug' if CMDLINE.verbose else 'info'

def get_input(part):

	lines = []

	filename = "./input-{}".format(part) if not CMDLINE.testing else "./input-test-{}".format(part)
	with open(filename, "r") as infile:
		lines = infile.readlines()

	return map(lambda x: x.rstrip(), lines)

def do_part(part):
    if not CMDLINE.part or CMDLINE.part == part:
        return True
    else:
        return False

########################################################################
#
# Classes

class Observation:

	def __init__(self, lines):

		self.before = State(lines[0][len('Before: '):])
		self.oper = map(lambda x: int(x), lines[1].split(' '))
		self.after = State(lines[2][len('After: '):])

		if len(lines[3]) != 0:
			raise Exception("unexpected input: {}".format(lines[3]))

	def __repr__(self):
		return "{} changes {} to {}".format(self.oper, self.before, self.after)


########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day 16 part A")

	lines = get_input('a')

	cpu = CPU()
	opcodes = cpu.ops()
	hit_samples = 0
		
	for i in range(0, len(lines), 4):
		args = lines[i:i+4]
		obs = Observation(args)
		log.debug(obs)

		hits = 0
		for name in sorted(opcodes.keys()):

			cpu.state = State(state=obs.before)
			opcodes[name](obs.oper[1:])

			if CMDLINE.verbose:
				log.debug("{:8s} : {}".format(name, obs.oper[1:]))
				log.debug("before   : {}".format(obs.before))
				log.debug("after    : {}".format(cpu.state))
				log.debug("expected : {}".format(obs.after))

			if cpu.state.reg == obs.after.reg:
				log.debug("obs[{}] hit on {}".format(i, name))
				hits += 1

			cpu.state.clear()

		if hits >= 3:
			log.debug("obs[{}] hit on {} ops".format(i, hits))
			hit_samples += 1

	log.success(hit_samples)

########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day 16 part B")

	## Redo part A and infer from it the mapping of opcodes to 
	## instructions.
	lines = get_input('a')
	cpu = CPU()
	opcodes = cpu.ops()
	instructions = [ None for i in range(16) ]

	for i in range(0, len(lines), 4):
		args = lines[i:i+4]
		obs = Observation(args)

		hits = []
		for name in sorted(opcodes.keys()):

			cpu.state = State(state=obs.before)
			opcodes[name](obs.oper[1:])

			if cpu.state.reg == obs.after.reg:
				hits.append(name) 

			cpu.state.clear()

		hitnames = []
		for h in hits:
			if h not in instructions:
				hitnames.append(h)
		if len(hitnames) == 1:
			code = obs.oper[0]
			instructions[code] = hitnames[0]

	## print out the opcode table... because... inquiring minds want to know
	for code, instr in enumerate(instructions):
		log.info("op[{:02d}] = {}".format(code, instr))

	## now load the program, initialize the CPU's state to 0s and let the program fly
	lines = get_input('b')
	cpu.state = State()
	with log.progress("cpu state:") as p:
		for ix, l in enumerate(lines):
			
			instr = map(lambda x: int(x), l.split(' '))
			op = instr[0]
			args = instr[1:]

			opname = instructions[op]
			m = opcodes[opname]

			log.debug("input[{:04d}]: {}".format(ix, l))
			log.debug("   {:8s}   : {}".format(opname, instr[1:]))
			log.debug("   before     : {}".format(cpu.state))

			m(args)
			log.debug("   after      : {}".format(cpu.state))

			p.status("[{}]: {}".format(ix, cpu.state))

	log.success(cpu.state)


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

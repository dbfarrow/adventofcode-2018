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
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 19")
	parser.add_argument('-t', '--testing', action='store_true', default=False)
	parser.add_argument('-v', '--verbose', action='store_true', default=False)
	parser.add_argument('-p', '--part')
	global CMDLINE 
	CMDLINE = parser.parse_args()

	context.log_level = 'debug' if CMDLINE.verbose else 'info'

def get_input(part):

	lines = []

	#filename = "./input-{}".format(part) if not CMDLINE.testing else "./input-test-{}".format(part)
	filename = "./input" if not CMDLINE.testing else "./input-test"
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

__progress = None

def log_state(ip, before, instr, after):

	global __progress
	if __progress == None:
		__progress = log.progress("")

	bstr = ",".join(map(lambda x: "{:8d} ".format(x), before))
	astr = ",".join(map(lambda x: "{:8d} ".format(x), after))
	__progress.status("ip={:2d}   [{}]   {:12s}   [ {} ]".format(ip, bstr, instr, astr))


########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day 19 part A")

	lines = get_input('a')

	# initialize the CPU
	cpu = CPU()
	cpu.reg = [ 0 for i in range(6) ]
	
	# get the mapping of IP to register
	l = lines[0]
	del lines[0]
	[ instr, rip ] = l.split(" ")
	if instr != "#ip":
		raise Exception ("malformed first line: {}".format(l))
	else:
		cpu.rip = int(rip)
		log.info("IP mapped to register: {}".format(cpu.rip))
	
	steps = 0
	first = True
	target = 0
	prog_throttle = 0
	while cpu.ip < len(lines):

		l = lines[cpu.ip]
		parts = l.split(" ")
		instr = parts[0]
		args = parts[1:]

		ip_before = cpu.ip
		reg_before = [ r for r in cpu.reg ]
		cpu.do(instr, args)

		if cpu.ip == 2 and first:
			first = False
			target = cpu.reg[2]
			log.info("factoring: {}".format(cpu.reg[2]))

		if cpu.ip == 3:
			if prog_throttle % target == 0:
				log_state(ip_before, reg_before, l, cpu.reg)
			prog_throttle += 1
				
		steps += 1

	log.info("steps = {}".format(steps))
	log.success(cpu.reg[0])

########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day 19 part B")

	## run the same program but with a different initial state
	lines = get_input('a')

	# initialize the CPU
	cpu = CPU()
	cpu.reg = [ 0 for i in range(6) ]
	cpu.reg = [ 1, 0, 0, 0, 0, 0 ]
	
	# get the mapping of IP to register
	l = lines[0]
	del lines[0]
	[ instr, rip ] = l.split(" ")
	if instr != "#ip":
		raise Exception ("malformed first line: {}".format(l))
	else:
		cpu.rip = int(rip)
		log.info("IP mapped to register: {}".format(cpu.rip))
	
	steps = 0
	first = True
	target = None
	prog_throttle = 0
	while cpu.ip < len(lines) and target == None:

		l = lines[cpu.ip]
		parts = l.split(" ")
		instr = parts[0]
		args = parts[1:]

		ip_before = cpu.ip
		reg_before = [ r for r in cpu.reg ]
		cpu.do(instr, args)

		if cpu.ip == 2 and first:
			first = False
			target = cpu.reg[2]
			
	log.info("factoring: {}".format(cpu.reg[2]))

	factors = []
	for i in range(1, int(math.sqrt(target) + 1)):
		if target % i == 0:
			factors.append(i)
			factors.append(target / i)
			log.info(str(i))
			log.info(str(target / i))
	log.success(sum(factors))



if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

#!/usr/bin/env python

import argparse
from pwn import *
from cpu import *

########################################################################
#
# boilerplate script setup
#
# command line arguments
CMDLINE = None 

def parse_cmdline():
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 21")
	parser.add_argument('-t', '--testing', action='store_true', default=False)
	parser.add_argument('-v', '--verbose', action='store_true', default=False)
	parser.add_argument('-p', '--part')
	global CMDLINE 
	CMDLINE = parser.parse_args()

	context.log_level = 'debug' if CMDLINE.verbose else 'info'

def get_input():

	lines = []

	filename = "./input"	# if not CMDLINE.testing else "./input-test"
	with open(filename, "r") as infile:
		lines = infile.readlines()

	return lines

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

	#iparts = instr.split(" ")
	#istr = "{} {:8x} {:8x} {}".format(iparts[0], int(iparts[1]), int(iparts[2]), iparts[3])

	if len(astr) > 60:
		m = astr[0:56] + "..."
		astr = m
	if len(bstr) > 60:
		m = bstr[0:56] + "..."
		bstr = m
	#__progress.status("ip={:2d} [{}] -- {:17s} --  [ {} ]".format(ip, bstr, instr, astr))
	log.info("ip={:2d} [{}] -- {:17s} --  [ {} ]".format(ip, bstr, instr, astr))


########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day 21 part A")

	lines = get_input()

	# initialize the CPU
	cpu = CPU()
	cpu.reg = [ 0 for i in range(6) ]
	#cpu.reg[0] = 6778585
	cpu.reg[0] = 0

	# get the mapping of IP to register
	l = lines[0]
	del lines[0]
	[ instr, rip ] = l.split(" ")
	cpu.rip = int(rip)
	log.info("IP mapped to register: {}".format(cpu.rip))
	
	steps = 0
	while cpu.ip < len(lines):

		l = lines[cpu.ip].rstrip()
		parts = l.split(" ")
		instr = parts[0]
		args = parts[1:]

		ip_before = cpu.ip
		reg_before = [ r for r in cpu.reg ]
		cpu.do(instr, args)

		if cpu.ip == 12:
			log.info("step   = {}".format(steps))
			log.info("reg[5] = {}".format(cpu.reg[5]))
			break

		steps += 1

	# re-initialize the CPU
	cpu2 = CPU()
	cpu2.reg = [ 0 for i in range(6) ]
	cpu2.reg[0] = cpu.reg[5]

	steps = 0
	while cpu2.ip < len(lines):

		l = lines[cpu2.ip].rstrip()
		parts = l.split(" ")
		instr = parts[0]
		args = parts[1:]
		cpu2.do(instr, args)
		steps += 1
	
	log.success(cpu2.reg[0])
		
########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day 21 part B")
	log.failure("not implemented")


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

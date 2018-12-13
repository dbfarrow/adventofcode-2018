#!/usr/bin/env python

import argparse
from pwn import *

########################################################################
#
# boilerplate script setup
#
# command line arguments
CMDLINE = None 

def parse_cmdline():
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day N")
	parser.add_argument('-t', '--testing', action='store_true', default=False)
	parser.add_argument('-v', '--verbose', action='store_true', default=False)
	parser.add_argument('-p', '--part')
	parser.add_argument('-o', '--origin', type=int, default=7)
	global CMDLINE 
	CMDLINE = parser.parse_args()

	context.log_level = 'debug' if CMDLINE.verbose else 'info'

def get_input():

	lines = []

	filename = "./input" if not CMDLINE.testing else "./input-test"
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
# Classes / global methods

def parse_lines(lines):

	initial_state = ("." * CMDLINE.origin) + lines[0].rstrip().replace("initial state: ", "")
	while(len(initial_state) < 44):
		initial_state = initial_state + "."	

	notes = {}
	for i in range(2, len(lines)):
		[pattern, outcome] = lines[i].rstrip().split(" => ")
		#log.debug("pattern = {}".format(pattern))
		#log.debug("outcome = {}".format(outcome))
		notes[pattern] = outcome

	return [ initial_state, notes ]
	
def calc_generation(current, notes):

	nextgen = [ '.' '.' ]

	for i in range(len(current)):
		matched = 0
		for j, (pattern, outcome) in enumerate(notes.items()):
			frag = current[i:i+len(pattern)]
			if frag == pattern:
				matched += 1

		if matched > 1: 
			raise Exception("too many patterns matched")
		nextgen += outcome if matched == 1 else '.'

	return "".join(nextgen)
	
def calc_score(gen):

	score = 0
	for i in range(len(gen)):
		if gen[i] == '#':
			score += (i -CMDLINE.origin)	

	return score
	

########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day N part A")

	[ curr, notes ] = parse_lines(get_input())
	log.debug("    {}0         1         2         3         4".format(" "*CMDLINE.origin))
	log.debug(" 0: {}".format(curr))

	for i in range(1, 21):
		curr = calc_generation(curr, notes)
		log.debug("{:2d}: {}".format(i, curr))

	score = calc_score(curr)
	log.success(score)

########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day N part B")
	log.failure("not implemented")


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

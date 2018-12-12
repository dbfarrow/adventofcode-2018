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

	initial_state = ".." + lines[0].rstrip().replace("initial state: ", "")
	while(len(initial_state) < 44):
		initial_state = initial_state + "."	

	notes = {}
	for i in range(2, len(lines)):
		[pattern, outcome] = lines[i].rstrip().split(" => ")
		outcome = pattern[:2] + outcome + pattern[3:]
		log.debug("pattern = {}".format(pattern))
		log.debug("outcome = {}".format(outcome))
		notes[pattern] = outcome

	return [ initial_state, notes ]
	
def calc_generation(current, notes):

	nextgen = current

	for i in range(len(current)):
		for j, (pattern, outcome) in enumerate(notes.items()):
			#log.debug("applying {}".format(pattern))
			frag = current[i:i+len(pattern)]
			if frag == pattern:
				log.debug("current[{}] matches pattern {} ({})".format(i, j, pattern))
				log.debug("    updating current[{}] to {}".format(i, outcome))
				#nextgen[i+2] = outcome
				nextgen = nextgen[0:i] + outcome + nextgen[i+5:]
				log.debug(nextgen)

	return nextgen
	
	

########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day N part A")

	[ curr, notes ] = parse_lines(get_input())
	log.info("      0         1         2         3         4")
	log.info(" 0: {}".format(curr))

	for i in range(1, 20):
		curr = calc_generation(curr, notes)
		log.info("{:2d}: {}".format(i, curr))
		if i == 2:
			break

	log.failure("not implemented")

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

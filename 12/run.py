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
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 12")
	parser.add_argument('-t', '--testing', action='store_true', default=False)
	parser.add_argument('-v', '--verbose', action='store_true', default=False)
	parser.add_argument('-p', '--part')
	parser.add_argument('-o', '--origin', type=int, default=3)
	parser.add_argument('-g', '--generations', type=int, default=20)
	parser.add_argument('-j', '--projected', type=int, default=50000000000)
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

	initial_state = ("." * CMDLINE.origin) + lines[0].rstrip().replace("initial state: ", "") + ("."*10)
	while(len(initial_state) < 44):
		initial_state = initial_state + "."	

	notes = {}
	for i in range(2, len(lines)):
		[pattern, outcome] = lines[i].rstrip().split(" => ")
		notes[pattern] = outcome

	return [ initial_state, notes ]
	
def calc_generation(current, notes):

	nextgen = [ '.' '.' ]

	for i in range(len(current)):
		outcome = None
		for j, (pattern, o) in enumerate(notes.items()):
			frag = current[i:i+len(pattern)]
			if frag == pattern:
				
				log.debug("ix={:2d}: current[{:2d}] = {} -> pattern[{:2d}] ({})".format(i-CMDLINE.origin, i-CMDLINE.origin+2, o, j, pattern))
				if outcome != None:	
					raise Exception("too many patterns matched")
				else:
					outcome = o

		nextgen.append(outcome if outcome else '.')

	return "".join(nextgen)
	
def calc_score(gen):

	score = 0
	for i in range(len(gen)):
		if gen[i] == '#':
			ix = i - CMDLINE.origin 
			log.debug("score += {}".format(ix))
			score += ix

	return score
	

########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day 12 part A")

	[ curr, notes ] = parse_lines(get_input())
	log.info("    {}0         1         2         3         4".format(" "*CMDLINE.origin))
	log.info(" 0: {}".format(curr))

	with log.progress("") as p:
		for i in range(1, CMDLINE.generations+1):
			curr = calc_generation(curr, notes)
			p.status("{:2d}: {}".format(i, curr[:200]))

	log.info("{:2d}: {}".format(i, curr))
	score = calc_score(curr)
	log.success(score)

########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day 12 part B")

	[ curr, notes ] = parse_lines(get_input())
	log.info("    {}0         1         2         3         4".format(" "*CMDLINE.origin))
	log.info(" 0: {}".format(curr))

	ngens = 10000

	# using the -g param with partA and observing the output, at g=168 the 
	# output beomes completely regular and simply shifts right one 
	# position with each new generation.
	#
	# So... start by calculating the plans at the 168th generation
	with log.progress("") as p:
		for i in range(1, 168+1):
			curr = calc_generation(curr, notes)
			p.status("{:2d}: {}".format(i, curr[:200]))

	num_plants = curr.count('#')
	log.info("terminal state: {} plants/generation".format(num_plants))

	# Given a projected generation to score, each plant will be in 
	# a pot that is offset from the pots in gen 168 by the amount:
	# projected_generation - 168. So when calculating the score
	# for each pot, just add the offset to each pot. Or, more
	# simply, for each plant, add (num_plants * offset) to the
	# score for g=168
	offset = CMDLINE.projected - 168
	score = calc_score(curr)
	score += (num_plants * offset)

	log.success(score)


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

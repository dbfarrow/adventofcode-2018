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
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 2")
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
		for ix, line in enumerate(infile):
			lines.append(line.rstrip())

	return lines

def do_part(part):
    if not CMDLINE.part or CMDLINE.part == part:
        return True
    else:
        return False

########################################################################
#
# Classes


########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day 2 part A")

	twice = 0
	thrice = 0

	lines = get_input()

	for line in lines:
		counts = { c : line.count(c) for c in line }
		freqs = { f : 1 for c, f in counts.items() }
		twice += (1 if 2 in freqs else 0)
		thrice += (1 if 3 in freqs else 0)

	chksum = twice * thrice
	log.success(str(chksum))

########################################################################
#
# PART B

def differs_by_one(a, b):

	diffs = 0
	for i, c in enumerate(a):
		diffs += (1 if a[i] != b[i] else 0)
		
	return True if diffs == 1 else 0	

def get_answer(a, b):
	answer = ""
	for i, c in enumerate(a):
		answer += (a[i] if a[i] == b[i] else "")
		
	return answer
	

def do_partB():

	log.info("AdventOfCode 2018 - day 2 part B")

	# read the input into a list of lines without newlines
	lines = get_input()

	# compare each line with all of the rest looking for 
	# lines that differ by only one character (in the same
	# position)
	for i, line in enumerate(lines):
		for j in range(i+1, len(lines)):
			if differs_by_one(lines[i], lines[j]):
				log.success(get_answer(lines[i], lines[j]))
				return


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

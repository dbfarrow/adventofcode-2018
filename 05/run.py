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
# Classes / and global methods

lower = [ chr(c) for c in range(ord('a'), ord('z')+1) ]
upper = [ chr(c) for c in range(ord('A'), ord('Z')+1) ]

def compress(line):

	log.debug("starting    : {}".format(line))

	while True:
		l = len(line)
		for i in range(len(lower)):
			pat = lower[i] + upper[i]
			if pat in line:
				line = line.replace(pat, "", 1)
				log.debug("replacing {}: {}".format(pat, line))

			pat = upper[i] + lower[i]
			if pat in line:
				line = line.replace(pat, "", 1)
				log.debug("replacing {}: {}".format(pat, line))

		if len(line) == l:
			return line;

	return None


########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day N part A")

	lines = get_input()
	line = lines[0].rstrip()
	line = compress(line)
	log.success(len(line))

########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day N part B")

	lines = get_input()
	minlen = len(lines[0])
	minc = None
	with log.progress("removing unit types") as p:
		for i in range(len(lower)):
			line = lines[0].rstrip()
			line = line.replace(lower[i], "")	
			line = line.replace(upper[i], "")	
			line = compress(line)
			log.debug("replacing '{}' reduced compressed string to {}".format(lower[i], len(line)))
			if len(line) < minlen:
				minlen = len(line)
				minc = lower[i]
				log.debug("'{}' results in new min length compression".format(lower[i]))
			p.status("removing {} reduces length to {}; current min = {}".format(lower[i], len(line), minlen))

	log.success(minlen)


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

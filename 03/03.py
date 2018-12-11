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

LENGTH = 2000
WIDTH = 2000

fabric = [ [ 0 for i in xrange(WIDTH) ] for j in xrange(LENGTH) ]

def parse_line(line):

	# parse out the big pieces:
	#   elf_id @ pos: dims
	parts = line.split(' ')
	elf_id = parts[0]
	pos = parts[2]
	dims = parts[3]

	# parse the pos:
	#   <x>,<y>:
	pos = pos.replace(':', '')
	[x, y] = [ int(i) for i in pos.split(',')]


	# parse the dims:
	#   <w>x<l>
	[w, h] = [ int(i) for i in dims.split('x')]

	return [ x, y, w, h]

def map_line(line):
	
	[ x, y, w, h ] = parse_line(line)

	# now mark the pattern on the map
	for i in range(x, x+w):
		for j in range(y, y+h):
			fabric[j][i] = fabric[j][i] + 1
	

def count_overlaps():

	overlaps = 0
	for row in fabric:
		for cell in row:
			overlaps += (1 if cell > 1 else 0)

	return overlaps 

def is_freestanding(line):

	[ x, y, w, h ] = parse_line(line)
	for i in range(x, x+w):
		for j in range(y, y+h):
			if fabric[j][i] > 1:
				return False

	return True


########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day N part A")

	lines = get_input()
	for line in lines:
		map_line(line)

	for row in fabric:
		log.debug(row)

	log.success(str(count_overlaps()))

########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day N part B")

	lines = get_input()
	for line in lines:
		if is_freestanding(line):
			log.success("freestanding claims: {} ".format(line))


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

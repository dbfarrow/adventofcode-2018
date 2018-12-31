#!/usr/bin/env python

import argparse
from pwn import *
import re


########################################################################
#
# boilerplate script setup
#
# command line arguments
CMDLINE = None 

def parse_cmdline():
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 23")
	parser.add_argument('-t', '--testing', action='store_true', default=False)
	parser.add_argument('-v', '--verbose', action='store_true', default=False)
	parser.add_argument('-p', '--part')
	global CMDLINE 
	CMDLINE = parser.parse_args()

	context.log_level = 'debug' if CMDLINE.verbose else 'info'

def get_input(step):

	lines = []

	filename = "./input" if not CMDLINE.testing else "./input-test-{}".format(step)
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

def parse_line(l):

	m = re.match("pos=<([-]?\d+),([-]?\d+),([-]?\d+)>, r=([-]?\d+)", l)
	if m:
		x = int(m.group(1))
		y = int(m.group(2))
		z = int(m.group(3))
		r = int(m.group(4))
		pos = (x, y, z)
		return [ r, pos ]
	else:
		raise Exception("input format error: {}".format(l))


def distance_apart(a, b):
	
	return abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])

########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day 23 part A")

	lines = map(parse_line, get_input('a'))
	max_range = max(map(lambda x: x[0], lines))
	strongest = next(iter([ n for n in lines if n[0] == max_range]))
	in_range = filter(lambda x: distance_apart(x[1], strongest[1]) <= max_range, lines)
	log.success(len(in_range))

########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day 23 part B")

	num_in_range = 0
	closest = None
	lines = map(lambda x: parse_line(x), get_input('b'))
	for l in lines:
		in_range = filter(lambda x: distance_apart(x[1], l[1]) <= x[0], lines)
		if len(in_range) > num_in_range:
			closest = [ l ]
			num_in_range = len(in_range)
		elif len(in_range) == num_in_range:
			closest.append(l)

	log.info("closest: {}".format(closest))


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

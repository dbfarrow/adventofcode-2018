#!/usr/bin/env python

import argparse
from pwn import *
import time
import math

########################################################################
#
# boilerplate script setup
#
# command line arguments
CMDLINE = None 

def parse_cmdline():
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 25")
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
		for ix, l in enumerate(infile):
			if '#' in l:
				continue
			lines.append(map(lambda x: int(x), l.rstrip().split(",")))

	return lines

def do_part(part):
    if not CMDLINE.part or CMDLINE.part == part:
        return True
    else:
        return False

########################################################################
#
# Classes / global functions

def calc_distance(a, b):

	try:
		d = 0
		d += abs(int(a[0]) - int(b[0]))
		d += abs(int(a[1]) - int(b[1]))
		d += abs(int(a[2]) - int(b[2]))
		d += abs(int(a[3]) - int(b[3]))
		return d
	except:
		log.failure("a = {}".format(a))
		log.failure("b = {}".format(b))
		exit(-1)

########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day 25 part A")

	cons = []

	lines = get_input()
	for l in lines:

		in_cons = []
		for i, c in enumerate(cons):
			for p in c:
				d = calc_distance(l, p) 
				log.debug("{} - {} = {}".format(l, p, d))
				if d <= 3:
					in_cons.append(i)
					break
			
		if len(in_cons) == 0:
			log.debug("starting new constellation with {}".format(l))
			cons.append( [ l ])
		else:
			log.debug("len in_cons={}".format(len(in_cons)))
			log.debug("l = {}".format(l))
			fc = in_cons[0]
			cons[fc].append(l)
			for ac in range(1, len(in_cons)):
				#log.debug(cons[0])
				log.debug("merging constellation {} into {}".format(cons[ac], cons[fc]))
				cons[fc] += cons[ac]
				del cons[ac]
					
		#sleep(.5)
	for i, c in enumerate(cons):
		log.debug("c[{}] = {}".format(i, c))

	log.success(len(cons))

########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day 25 part B")
	log.failure("not implemented")


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

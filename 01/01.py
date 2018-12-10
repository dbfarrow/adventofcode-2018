#!/usr/bin/env python

import time
import argparse
from pwn import *

########################################################################
#
# boilerplate script setup
#
# command line arguments
CMDLINE = None 

def parse_cmdline():
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 1")
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
# Classes


########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day 1 part A")

	total = 0

	lines = get_input()
	for line in lines:
		total = total + int(line)

	log.success(total)

########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day 1 part B")

	passnum = 1
	total = 0
	freqs = {}
	firstdup = -1

	with log.progress('pass: ') as p:
		while (1):
			passnum += 1
			p.status(str(passnum))
	
			lines = get_input()
			for line in lines:
				val = int(line)
				total = total + val
				log.debug("{}:{}".format(val, total))
				if total in freqs:
					if firstdup < 0:
						firstdup = total
						log.debug("first dup: {}".format(firstdup))
						log.debug("passnum  : {}".format(passnum))
						log.success(firstdup)
						return
				else:
					freqs[total] = 1


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

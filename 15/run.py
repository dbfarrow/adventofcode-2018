#!/usr/bin/env python

import argparse
from pwn import *
import time

from field import *

########################################################################
#
# boilerplate script setup
#
# command line arguments
CMDLINE = None 

def parse_cmdline():
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 15")
	parser.add_argument('-t', '--testing', action='store_true', default=False)
	parser.add_argument('-v', '--verbose', action='store_true', default=False)
	parser.add_argument('-p', '--part')
	parser.add_argument('-d', '--delay', type=float, default=0.25)
	global CMDLINE 
	CMDLINE = parser.parse_args()

	context.log_level = 'debug' if CMDLINE.verbose else 'info'

def get_input():

	lines = []

	filename = "./input" if not CMDLINE.testing else "./input-test"
	with open(filename, "r") as infile:
		lines = infile.readlines()

	return Field(lines)

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

	log.info("AdventOfCode 2018 - day 15 part A")

	field = get_input()
	field.render()

	turn = 0
	with log.progress("turn") as tp:
		tp.status("0")
		while 1:
		
			p = field.next_player()
			if p == None:
				tp.status("end of turn: {}".format(turn))
				turn += 1
				continue
	
			p.start_turn()
			field.render()

			# emulate processing turn
			p.targets = field.find_targets(p)
			field.render()
			time.sleep(CMDLINE.delay)

			p.in_range = field.find_in_range(p)
			field.render()
			time.sleep(CMDLINE.delay)

			p.end_turn()
			field.render()
	
			if turn > 3:
				break

	log.failure("not implemented")

########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day 15 part B")
	log.failure("not implemented")


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

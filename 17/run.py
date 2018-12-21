#!/usr/bin/env python

import argparse
from pwn import *
import time

from reservoir import *

########################################################################
#
# boilerplate script setup
#
# command line arguments
CMDLINE = None 

def parse_cmdline():
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 17")
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
			if l.startswith("#"):
				continue
			lines.append(l.rstrip())

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

def do_partAB():

	log.info("AdventOfCode 2018 - day 17 part A")

	drips = 0
	res = Reservoir(get_input())
	while len(res.sources) > 0:
		res.drip()
		if (res.depth < 20) or (drips % 100 == 0):
			res.render()
		drips += 0

		if CMDLINE.testing:
			time.sleep(0.1)
	
	log.success(res.measure_water(withspills=True))
	log.success(res.measure_water(withspills=False))

	#res.render(force=True)

if __name__ == "__main__":

	parse_cmdline()
	do_partAB()


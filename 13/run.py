#!/usr/bin/env python

import argparse
from pwn import *

from track import *
from cart import *

########################################################################
#
# boilerplate script setup
#
# command line arguments
CMDLINE = None 

def parse_cmdline():
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 13")
	parser.add_argument('-t', '--testing', action='store_true', default=False)
	parser.add_argument('-v', '--verbose', action='store_true', default=False)
	parser.add_argument('--show_maps', action='store_true', default=False)
	parser.add_argument('-p', '--part')
	parser.add_argument('--step', action='store_true', default=False)
	parser.add_argument('--delay', type=float, default=0)
	global CMDLINE 
	CMDLINE = parser.parse_args()

	context.log_level = 'debug' if CMDLINE.verbose else 'info'

def get_input(part):

	lines = []

	filename = "./input" if not CMDLINE.testing else "./input-test-{}".format(part)
	log.info("filename: {}".format(filename))
	with open(filename, "r") as infile:
		lines = infile.readlines()

	return Track(CMDLINE, lines)

def do_part(part):
    if not CMDLINE.part or CMDLINE.part == part:
        return True
    else:
        return False

########################################################################
#
# Classes
#
# externally included...

########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day 13 part A")

	# read in the map
	track = get_input('a')
	track.print_locations(None)
	
	with log.progress("") as t:
		while 1:

			c = track.next_cart()
			if c != None:
				c.move(track)
				track.print_locations(c)

				# check for collisions
				crash = track.remove_crash(c)
				if crash:
					log.info("carts collided: t[{}] at ({:3d},{:3d})".format(track.tick, crash[0], crash[1]))
					track.print_locations(c)
					log.success(crash)
					break

				t.status("t = {}".format(track.tick))
			
			else:
				break


########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day 13 part B")

	# read in the map
	track = get_input('b')
	track.print_locations(None)
	
	with log.progress("") as t:
		while 1:

			if track.tick % 100 == 0:
				t.status("t = {}".format(track.tick))

			c = track.next_cart()
			if c != None:

				if c.last:
					track.print_locations(c)
					log.success("{},{}".format(c.x, c.y))
					return
				else:
					c.move(track)

				# check for collisions
				crash = track.remove_crash(c)
				if crash:
					log.info("carts collided: t[{}] at ({:3d},{:3d})".format(track.tick, crash[0], crash[1]))
					track.print_locations(c)
	
			else:
				break

	log.failure("something failed")


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

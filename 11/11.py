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
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 11")
	parser.add_argument('-t', '--testing', action='store_true', default=False)
	parser.add_argument('-v', '--verbose', action='store_true', default=False)
	parser.add_argument('-p', '--part')
	parser.add_argument('-d', '--dim', type=int, default=300)
	parser.add_argument('-s', '--serial', type=int, default=8444)
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

def calc_power(x, y, s):

	rack_id = x + 10
	power_level = rack_id * y
	power_level += s
	power_level *= rack_id
	power_level /= 100
	power_level %= 10
	power_level -= 5

	return power_level

def calc_total_power(grid, x, y, d):

	total = 0
	for i in range(d):
		for j in range(d):
			total += grid[y + i][x + j]

	return total

def log_grid(g):

	for l in g:
		log.debug(l)

########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day 11 part A")

	# create the 300x300 grid
	dim = CMDLINE.dim
	grid = [[ 0 for x in range(dim) ] for y in range(dim) ]

	# calculate the power level in each cell
	for y in range(len(grid)):
		for x in range(len(grid[y])):
			grid[y][x] = calc_power(x, y, CMDLINE.serial)

	#log_grid(grid)

	# calculate the power for each 3x3 cell
	max_power = 0
	max_x = 0
	max_y = 0
	with log.progress("search 3x3 cells:") as p:
		for y in range(len(grid) - 3):
			for x in range(len(grid[y]) - 3):
				tp = calc_total_power(grid, x, y, 3)
				if tp > max_power:
					max_power = tp
					max_x = x
					max_y = y
			p.status("max_power = {} after {} searched".format(max_power, str(y*CMDLINE.dim + x)))
			#time.sleep(1)	

	log.success("the 9 cells at ({}, {}) have max power at: {}".format(max_x, max_y, max_power))

########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day 11 part B")

	# create the 300x300 grid
	dim = CMDLINE.dim
	grid = [[ 0 for x in range(dim) ] for y in range(dim) ]

	# calculate the power level in each cell
	for y in range(len(grid)):
		for x in range(len(grid[y])):
			grid[y][x] = calc_power(x, y, CMDLINE.serial)

	#log_grid(grid)

	# calculate the power for each 3x3 cell
	max_power = 0
	max_x = 0
	max_y = 0
	max_dim = 1

	with log.progress("search cells:") as p:
		for d in range(1, 300):
			for y in range(len(grid) - d):
				for x in range(len(grid[y]) - d):
					tp = calc_total_power(grid, x, y, d)
					if tp > max_power:
						max_power = tp
						max_x = x
						max_y = y
						max_dim = d
			p.status("max_power = {0} (dim={1}x{1} at ({3},{4}) after {2}x{2} searched".format(max_power, max_dim, d, max_x, max_y))

	log.success("the {}x{} block at ({}, {}) have max power at: {}".format(max_dim, max_dim, max_x, max_y, max_power))


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

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

	label = None
	depth = None
	target = None

	filename = "./input" if not CMDLINE.testing else "./input-test"
	with open(filename, "r") as infile:
		for ix, l in enumerate(infile):
			if "depth: " in l:
				[ label, depth ] = l.split(": ")
			elif "target: " in l:
				[ label, target ] = l.split(": ")
				coords = target.split(",")
				target = (int(coords[0]), int(coords[1]))		

	return [ int(depth), target ]

def do_part(part):
    if not CMDLINE.part or CMDLINE.part == part:
        return True
    else:
        return False

########################################################################
#
# Classes

class Cave:

	def __init__(self, depth, target):
	
		self.types = [ '.', '=', '|' ]
		self.target = target
		self.regions = []
		width = target[0]

		for y in range(depth+1):
			row = []
			for x in range(width+1):
				
				r = Region(x, y)

				# geo index...
				if (x, y) == (0, 0):
					r.geo_ix = 0
					r.type = 'M'
				elif x == target[0] and y == target[1]:
					r.geo_ix = 0
					r.type = 'T'
				elif y == 0:
					r.geo_ix = x * 16807
				elif x == 0:
					r.geo_ix = y * 48271
				else:
					left = row[x-1].erosion_level
					up = self.regions[y-1][x].erosion_level
					r.geo_ix = left * up

				# erosion level
				r.erosion_level = (r.geo_ix + depth) % 20183
				if r.type == None:
					r.risk = r.erosion_level % 3
					r.type = self.types[r.risk]

				row.append(r)			
				
			self.regions.append(row)
			log.info("".join(map(lambda x: x.type, row)))
	
	def render(self):
		
		for y in range(len(self.regions)):
			if y >= self.target[1]+1:
				return
			row = self.regions[y]
			m = ""
			for region in row:
				m += region.type
			log.debug(m)

class Region:

	def __init__(self, x, y):

		self.x = x
		self.y = y
		self.geo_ix = 0
		self.erosion_level = 0
		self.type = None
		self.risk = 0

	def __repr__(self):
		return "({},{}): type={}, erosion_level={}, geo_ix={}".format(self.x, self.y, self.type, self.erosion_level, self.geo_ix)

########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day N part A")

	[ depth, target ] = get_input()
	log.info("Caverns are {} deep".format(depth))
	log.info("Target is located at: {}".format(target))
		
	c = Cave(depth, target)
	c.render()

	risk = 0
	for y, row in enumerate(c.regions):
		for x, r in enumerate(row):
			if x > target[0] or y > target[1]:
				continue
			risk += r.risk
	
	log.success(risk)

########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day N part B")
	log.failure("not implemented")


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

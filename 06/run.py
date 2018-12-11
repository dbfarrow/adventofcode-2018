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
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 6")
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

class Space:

	def __init__(self):

		self.points = []
		self.maxX = 0
		self.maxY = 0
		self.edge_points = set()

		# load the points and determine the bounds of the space
		# containing the points
		lines = get_input()
		for ix in range(len(lines)):
			p = Point(ix, lines[ix])
			if p.x > self.maxX:
				self.maxX = p.x
			if p.y > self.maxY:
				self.maxY = p.y

			self.points.append(p)

		# initialize the space map
		log.debug("bounds: [0, 0] -> [{}, {}]".format(self.maxX, self.maxY))
		self.map = []
		for i in range(self.maxY + 1):
			self.map.append([ None for j in range(self.maxX + 1) ])

		# and add the points to the space
		for ix, p in enumerate(self.points):
			self.map[p.y][p.x] = p

	def calc_distances(self):
	
		pp = Point()

		for y in range(len(self.map)):
			for x in range(len(self.map[y])):
				minD = self.maxX + self.maxY
				for p in self.points:
					d = abs(x - p.x) + abs(y - p.y)
					if d < minD:
						minD = d
						self.map[y][x] = p	
					elif d == minD:
						self.map[y][x] = pp
		
	def exclude_edge_points(self):
		
		for y in [0, self.maxY]:
			for x in range(self.maxX):
				self.edge_points.add(self.map[y][x])
	
		for x in [0, self.maxX]:
			for y in range(self.maxY):
				self.edge_points.add(self.map[y][x])

	def get_finite_spaces(self):
	
		sizes = {}
		for p in self.points:
			if p in self.edge_points:
				continue
			else:
				sizes[p] = 0
				for y in self.map:
					for x in y:
						if x == p:
							sizes[p] += 1

		return sizes

	def calc_closest(self, maxD):

		pp = Point()
		pp.name = "#"

		size = 0

		for y in range(len(self.map)):
			for x in range(len(self.map[y])):
				d = 0
				for p in self.points:
					d += abs(x - p.x) + abs(y - p.y)
				if d < maxD:
					self.map[y][x] = pp
					size += 1

		return size

	def __repr__(self):

		if not testing:
			return ""

		r = ""
		for y in self.map:
			for x in y:
				r += x.name if x != None else "."
			r += "\n" 
		return r

class Point:

	def __init__(self):
		self.name = "."
		self.x = self.y = -1

	def __init__(self, ix = -1 , datastr = ""):

		if ix < 0:
			self.name = "."
			self.x = self.y = 0
		else:
			self.name = chr(ord('A')+ix)
			[self.x, self.y] = [ int(c) for c in datastr.split(', ') ]
		
	def __repr__(self):

		if not testing:
			return ""
		return "[{}, {}]".format(self.x, self.y)



########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day 6 part A")

	log.info("loading space")
	s = Space()
	log.debug(s)

	log.info("calculating distances")
	s.calc_distances()
	log.debug(s)

	log.info("excluding edge points")
	s.exclude_edge_points()

	log.info("searching for finite spaces")
	finites = s.get_finite_spaces()

	a = max(finites, key=lambda key: finites[key])
	log.info("{} (size = {})".format(a.name, finites[a]))
	log.success(finites[a])

########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day 6 part B")

	s = Space()
	log.debug(s)

	d = 32 if CMDLINE.testing else 10000
	size = s.calc_closest(d)
	log.debug(s)
	log.success(size)


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()


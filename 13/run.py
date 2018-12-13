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
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 13")
	parser.add_argument('-t', '--testing', action='store_true', default=False)
	parser.add_argument('-v', '--verbose', action='store_true', default=False)
	parser.add_argument('--show_maps', action='store_true', default=False)
	parser.add_argument('-p', '--part')
	parser.add_argument('--max_steps', type=int, default=-1)
	global CMDLINE 
	CMDLINE = parser.parse_args()

	context.log_level = 'debug' if CMDLINE.verbose else 'info'

def get_input():

	lines = []

	filename = "./input" if not CMDLINE.testing else "./input-test"
	with open(filename, "r") as infile:
		lines = infile.readlines()

	tracks = Track(lines)
	
	# find the carts, note their positions, and remove
	# them from the track
	carts = []
	for y in range(len(tracks.grid)):
		row = tracks.grid[y]
		for x in range(len(row)):
			c = chr(row[x])
			cart = None
			if c == '>' or c == '<' or c == '^' or c == 'v':
				carts.append(Cart(x, y, c))

	tracks.remove_carts()
	return [ tracks, carts ]

def do_part(part):
    if not CMDLINE.part or CMDLINE.part == part:
        return True
    else:
        return False

########################################################################
#
# Classes

class Track:

	def __init__(self, lines):

		# read each line and add it to the grid
		self.grid = []
		for l in lines:
			self.grid.append(bytearray(l))
					
		self.max_y = len(self.grid)
		self.max_x = len(self.grid[0])
		self.collision = None

	def get_cell(self, x, y):
		if x < 0 or x > self.max_x:
			return ' '
		elif y < 0 or y > self.max_y:
			return ' '
		else:
			return chr(self.grid[y][x])

	def remove_carts(self):
		
		for y in range(len(self.grid)):
			row = self.grid[y]
			for x in range(len(row)):
				c = chr(self.grid[y][x])
				if c == '>' or c == '<':
					self.grid[y][x] = '-'
				elif c == '^' or c == 'v':
					self.grid[y][x] = '|'
				
class Cart:
	
	def __init__(self, x, y, c):

		self.x = x
		self.y = y
		self.c = c
		self.num_turns = 0

	def __repr__(self):

		return "cart travelling {} at ({}, {})".format(self.c, self.x, self.y)

	def move(self, tracks):

		# calculate the new position of the cart
		log.debug("old position: ({}, {})".format(self.x, self.y))
		if self.c == '>':
			self.x += 1
		elif self.c == 'v':
			self.y += 1
		elif self.c == '<':
			self.x -= 1
		elif self.c == '^':
			self.y -= 1
		log.debug("new position: ({}, {})".format(self.x, self.y))

		if self.x < 0 or self.y < 0 or self.x >= tracks.max_x or self.y >= tracks.max_y:
			raise Exception('cart is off the tracks')
	
		# calculate the new direction of the chart	
		cell = tracks.get_cell(self.x, self.y)
		log.debug("cell = {}".format(cell))
		log.debug("old c = {}".format(self.c))
		if cell == '/':
			if self.c == '^':
				self.c = '>'
			elif self.c == '>':
				self.c = '^'
			elif self.c == 'v':
				self.c = '<'
			elif self.c == '<':
				self.c = 'v'
		elif cell == '\\':
			if self.c == '^':
				self.c = '<'
			elif self.c == '<':
				self.c = '^'
			elif self.c == 'v':
				self.c = '>'
			elif self.c == '>':
				self.c = 'v'
		elif cell == '+':
			cell = self.turn()	
		log.debug("new c = {}".format(self.c))

	def turn(self):
		
		dir_rules = [ 
			{	# turn left
				'>': '^',
				'^': '<',
				'<': 'v',
				'v': '>'
			},	# go straight
			{
				'>': '>',
				'^': '^',
				'<': '<',
				'v': 'v'
			},	
			{	# turn right
				'>': 'v',
				'^': '>',
				'<': '^',
				'v': '<'
			},	
		]
		
		self.c = dir_rules[self.num_turns % 3][self.c]
		self.num_turns += 1


__map = None

def print_map(tracks, carts):

	global __map
	if __map == None:
		__map = [ log.progress("") for i in range(len(tracks.grid)) ]

	locs = { (c.x, c.y) : c for c in carts }

	for y in range(len(tracks.grid)):
		m = ""
		row = tracks.grid[y]
		for x in range(len(row)):
			if (x,y) in locs:
				m += locs[(x,y)].c
			else:
				m += chr(row[x])
		__map[y].status(m)

########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day 13 part A")

	# read in the map
	[ tracks, carts ] = get_input()
	if CMDLINE.show_maps:
		print_map(tracks, carts)
	
	step = 0
	with log.progress("") as t:
		while 1:

			for c in carts:
				c.move(tracks)
				if CMDLINE.show_maps:
					print_map(tracks, carts)

				# check for collisions
				positions = {}
				for c in carts:
					pos = (c.x, c.y)
					if pos in positions:
						log.info("carts collided at t={}".format(step))
						log.success(pos)
						return
					else:
						positions[pos] = c
	
			t.status("t = {}".format(step))
			step += 1

			# check the max_steps command line parameter so we can 
			# bail if things go on too long
			if CMDLINE.max_steps > 0 and step >= CMDLINE.max_steps:
				break

			if CMDLINE.show_maps:
				time.sleep(0.25)

	log.fail("carts never collided")

########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day 13 part B")
	log.failure("not implemented")


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

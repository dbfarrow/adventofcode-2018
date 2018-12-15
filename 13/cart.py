#!/urr/bin/env python

from pwn import *

class Cart:
	
	def __init__(self, x, y, c):

		self.x = x
		self.y = y
		self.c = c
		self.num_turns = 0
		self.crash_id = -1
		self.last = False

	def __repr__(self):

		m = ""
		if self.c == 'X':
			m += "crash #{}   ".format(self.crash_id)
		else:
			m += "         {} ".format(self.c)
		m += ": ({:3d}, {:3d})".format(self.x, self.y)
		return m

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
		
		dirs = "<^>v"

		old_dir = self.c
		ix = dirs.find(old_dir)
		ix += ((self.num_turns % 3) - 1)
		self.num_turns += 1
		if ix < 0:
			ix = len(dirs)-1
		if ix == len(dirs):
			ix = 0
		self.c = dirs[ix]



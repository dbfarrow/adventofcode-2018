#!/usr/bin/env python

from pwn import *
from cart import *

class Track:

	def __init__(self, env, lines):

		self.env = env

		# read each line and add it to the grid
		self.carts = []
		self.grid = []
		for y, l in enumerate(lines):
			self.grid.append(bytearray(l))

			# find the carts, note their positions, and remove
			# them from the track
			for x, c in enumerate(l):
				if c == '^' or c == 'v':
					self.carts.append(Cart(x, y, c))
					self.grid[y][x] = '|'
				if c == '>' or c == '<':
					self.carts.append(Cart(x, y, c))
					self.grid[y][x] = '-'
		
		# note the size of the grid so we know when something
		# has gone off the tracks. that should never happen
		# so it's only here for catching runaway logic errors
		self.max_y = len(self.grid)
		self.max_x = len(self.grid[0])
		self.collision = None
		self.tick = 0
		self.step = None
		self.crash_count = 0
		self.__map = None

	def get_cell(self, x, y):
		if x < 0 or x > self.max_x:
			return ' '
		elif y < 0 or y > self.max_y:
			return ' '
		else:
			return chr(self.grid[y][x])

	def next_cart(self):
			
		# if there are no carts in the step, reload the step 
		# list from the carts list
		if self.step == None or (len(self.step) == 0):
			self.step = { (c.y, c.x): c for c in self.carts if c.c != 'X' }
			self.tick += 1
			if len(self.step) == 0:
				return None
			if len(self.step) == 1:
				next_cart = self.step.values()[0]
				next_cart.last = True
				return next_cart

		# sort the carts to determine which one moves next. the order
		# is top to bottom, left to right. the order should be 
		# recalculated after each cart moves since the movement may
		# change the order or processing
		pos = sorted([ p for p in self.step.keys() ])
		for p in pos:
			log.debug(p)

		# now remove the first item in the list and return it to
		# the caller
		next_cart = self.step[pos[0]]
		del self.step[pos[0]]
		for p in self.step.keys():
			log.debug(p)
		log.debug("returning: {}".format(next_cart))
		log.debug("{} carts left in step".format(len(self.step)))

		return next_cart

	def remove_crash(self, cart):

		cart_ix = -1
		other_cart_ix = -1
		other_cart = None

		for i, c in enumerate(self.carts):
			if c == cart:
				cart_ix = i

			if c.c == 'X':
				continue	# this crash has already been cleared

			if (cart.x, cart.y) == (c.x, c.y) and (c != cart):
				if other_cart != None:
					raise Exception("I haven't accounted for a three+ car pileup")
				other_cart = c
				other_cart_ix = i
				continue

		if other_cart:
			other_cart.c = 'X'
			other_cart.crash_id = self.crash_count
			cart.c = 'X'
			cart.crash_id = self.crash_count
			self.crash_count += 1
			log.info("removed crash at ({:3d},{:3d})".format(cart.x, cart.y))
			return (other_cart.x, other_cart.y)
		else:
			return None

	def print_locations(self, curr):

		if self.env.show_maps and len(self.grid) < 10:
			if self.__map == None:
				self.__map = [ log.progress("") for i in range(len(self.grid)) ]

			locs = { (c.x, c.y) : c for c in self.carts }

			for y in range(len(self.grid)):
				m = ""
				row = self.grid[y]
				for x in range(len(row)):
					if (x,y) in locs:
						m += locs[(x,y)].c
					else:
						m += chr(row[x])
				self.__map[y].status(m)

		else:
		
			if self.__map == None:
				self.__map = [ log.progress("cart[{:2d}]".format(i)) for i, c in enumerate(self.carts) ]
		
			for i, c in enumerate(self.carts):
				m = str(c)
				if c == curr:
					m += " **"
				self.__map[i].status(m)
	
		if self.env.step:
			a = raw_input("hit enter to continue (or q to quit): ")
			if a.rstrip() == "q":
				log.failure("quiting at user request")
				exit(-1)
			else:
				sys.stdout.write("\033[F")
		else:
			if self.env.delay > 0:
				sleep(self.env.delay)



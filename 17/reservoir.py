#!/usr/bin/env python

from pwn import *

SPRING_X = 500
MARGIN = 3

DRIP_COUNT =0
SOURCES = 1
PROGRESS_COUNT = 2

class Reservoir:

	def __init__(self, cfgstrs):

		self.sides = [ Side(s) for s in cfgstrs ]
		self.calc_dims()
		self.drip_count = 0

		self.slice = [ [ '.' for x in range(self.width) ] for y in range(self.depth) ]
		self.plot_clay()

		self.sources = [ (SPRING_X - self.min_x, 0) ]
		self.positions = {}
		self.slice[self.sources[0][1]][self.sources[0][0]] = '+'

		if self.depth < 20:
			self.screen = [ log.progress("{:4d} ".format(i)) for i in range(self.depth) ]
		self.progress = [ None for i in range(PROGRESS_COUNT) ]
		self.progress[DRIP_COUNT] = log.progress("drips  : ")
		self.progress[SOURCES]    = log.progress("sources: ")

		self.progress[DRIP_COUNT].status(str(self.drip_count))
		self.progress[SOURCES].status(str(self.sources))

	def calc_dims(self):

		max_x = max_y = 0
		min_x = min_y = 0xffffffff

		for s in self.sides:
			min_x = s.min_x if s.min_x < min_x else min_x
			min_y = s.min_y if s.min_y < min_y else min_y
			max_x = s.max_x if s.max_x > max_x else max_x
			max_y = s.max_y if s.max_y > max_y else max_y

		self.min_x = min_x - MARGIN
		self.min_y = 0
		self.highest = min_y
		self.max_x = max_x - MARGIN
		self.max_y = max_y
		self.width = max_x - min_x + (2 * MARGIN)
		self.depth = max_y + MARGIN
		log.info("slice is  {:3d} x {:3d} between ({:3d},{:3d}) and ({:3d},{:3d})".format(self.width, self.depth, self.min_x, self.min_y, self.max_x, self.max_y))
		log.info("max water = {}".format(self.width * self.depth))
		log.info("")
		return 


	def plot_clay(self):

		for s in self.sides:
			for y in range(s.min_y, s.max_y+1):
				for x in range(s.min_x, s.max_x+1):
					self.slice[y][x - self.min_x] = '#'
	
	def drip(self):
		
		sp = self.sources[:]
		for ix, s in enumerate(sp):
				
			(x, y) = self.positions[s] if s in self.positions else s
			self.drip_count += 1

			#log.debug("drip_count: {}, pos: {}".format(self.drip_count, (x, y)))

			if y >= self.depth:
				for j, js in enumerate(self.sources):
					if s == js:
						del self.sources[j]
						self.progress[SOURCES].status(str(self.sources))
				continue

			if y >= len(self.slice) or x >= len(self.slice[y]):
				raise Exception("dims={} x {}, source={}, x={}, y={}".format(self.width, self.depth, s, x, y))
			spot = self.slice[y][x]
			if spot in '+':
				y += 1
			if spot in '|':
				if (x, y) != s:
					self.delete_source(ix, s)
				y += 1
			elif spot == '.':
				self.slice[y][x] = '|'
				y += 1
			elif spot == '#':
				y -= 1
				if self.flow(x, y):
					self.delete_source(ix, s)
			elif spot == '~':
				y -= 1
				if self.flow(x, y):
					self.delete_source(ix, s)

		#log.debug("updating position to: {}".format((x, y)))

		self.positions[s] = (x, y)

	''' returns True if the source has more space to flow into... false otherwise '''	
	def flow(self, x, y):
	
		# determine the bounds of the flow
		min_x = max_x = 0
		min_overflow = max_overflow = None

		while (x - min_x > 0) and self.slice[y][x - min_x] != '#' and not min_overflow:
			if self.slice[y+1][x - min_x] == '.':
				min_overflow = x - min_x
				self.add_source((min_overflow, y))
				#log.debug("new left spring at {},{}".format(min_overflow, y))
			min_x += 1

		while (x + max_x < self.width) and self.slice[y][x + max_x] != '#' and not max_overflow:
			if self.slice[y+1][x + max_x] == '.':
				max_overflow = max_x
				self.add_source((x + max_overflow, y))
				#log.debug("new right spring at {},{}".format(x + max_overflow, y))
			max_x += 1

		overflowing = (min_overflow > 0 or max_overflow > 0) 
		sym = '|' if overflowing else '~' 
		for i in range(min_x):
			self.slice[y][x-i] = sym
		for i in range(max_x):
			self.slice[y][x+i] = sym

		return overflowing
	
	def add_source(self, pos):

		if pos in self.sources:
			log.info("source {} exists".format(pos))
			return

		self.sources.append(pos)
		self.progress[SOURCES].status(str(self.sources))


	def delete_source(self, ix, s):

		try:
			log.debug("ix = {}".format(ix))
			log.debug("deleting # source at {}".format(self.sources[ix]))
			log.debug("sources: {}".format(self.sources))
			for i, src in enumerate(self.sources):
				if src == s:
					del self.sources[i]
			self.progress[SOURCES].status(str(self.sources))
		
		except:
			log.info("error deleting source[{}] from list of {} sources".format(ix, len(self.sources)))
			log.info(self.sources)
			log.info(s)
			exit(-1)

	def measure_water(self, withspills = True):

		water = 0
		for y, row in enumerate(self.slice):
			for x, cell in enumerate(row):
				if withspills:
					if self.slice[y][x] in '~|' and y <= self.max_y:
						water += 1
				else:
					if self.slice[y][x] in '~' and y <= self.max_y:
						water += 1

		water -= (self.highest - 1)
		return water
	
	def render(self, force=False):

		self.progress[DRIP_COUNT].status(str(self.drip_count))
		self.progress[SOURCES].status(str(self.sources))

		if self.depth <= 20:
			for y, s in enumerate(self.slice):
				self.screen[y].status("".join(self.slice[y]))
		elif force:
			for y, s in enumerate(self.slice):
				log.info("".join(self.slice[y]))

class Side:

	def __init__(self, instr):
		
		self.min_x = 0
		self.max_x = 0
		self.min_y = 0
		self.max_y = 0

		[ left, right ] = instr.rstrip().split(",")
		[ lp, lv ] = left.split("=")
		[ rp, rr ] = right.split("=")
		[ rn, rx ] = rr.split("..")

		if lp == 'x':
			self.min_x = self.max_x = int(lv)
			self.min_y = int(rn)
			self.max_y = int(rx)
		else:
			self.min_y = self.max_y = int(lv)
			self.min_x = int(rn)
			self.max_x = int(rx)

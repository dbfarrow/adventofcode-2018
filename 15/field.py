#!/usr/bin/env python

from pwn import *

class Field:

	def __init__(self, lines):

		# set up the field of action and 
		# the progress indicators we will be using to 
		# animate the game play
		self.rows = []
		self.players = []
		self.positions = []
		self.screen = []
		for y, l in enumerate(lines):
			l = l.rstrip()
			self.screen.append(log.progress(""))
			row = []
			for x, c in enumerate(l):
				square = Square(x, y, c)
				row.append(square)
				if square.is_player():
					self.players.append(square)

			self.rows.append(row)
				
		self.order = None

	def next_player(self):
			
		if self.order == None:
			self.positions = { (p.y, p.x): p for p in self.players }
			self.order = sorted(self.positions.keys())

		if len(self.order) == 0:
			self.order = None
			self.positions = None
			return None
		else:
			n = self.order[0]
			del self.order[0]
			return self.positions[n]

	def get_cell_type(self, x, y):
		return self.rows[y][x].t

	def find_targets(self, player):

		targets = []
		for p in self.players:
			if p.is_player() and p.t != player.t:
				targets.append(p)

		return targets
			
	def find_in_range(self, player):

		in_range = []
		for t in player.targets:
			x = t.x
			y = t.y
			if self.get_cell_type(x+1, y) == '.':
				in_range.append((x+1,y))	
			if self.get_cell_type(x-1, y) == '.':
				in_range.append((x-1,y))	
			if self.get_cell_type(x, y+1) == '.':
				in_range.append((x,y+1))	
			if self.get_cell_type(x, y-1) == '.':
				in_range.append((x,y-1))	
		return in_range

	def render(self):

		colors = {
			'G': '\033[31m',
			'E': '\033[32m',
			'#': '\033[2;37;40m',
			'.': '\033[2;37;40m',
			'?': '\033[2;37;40m',
			'@': '\033[2;37;40m',
			'!': '\033[2;37;40m',
		}
		nocolor = '\033[0m'
		bold = '\033[1m'	
		underline = '\033[4m'	
	
		# find the current player
		currents = [ p for p in self.players if p.current ]
		current = None
		if len(currents) > 0:
			current = currents[0]

		# now draw the map
		for y, row in enumerate(self.rows):
			m = ""
			for x, c in enumerate(row):

				# select the color based on what's in the cell
				m += colors[c.t]

				# bold it if it's the current player
				if c.current:
					m += bold

				# bold it if it's a targert of the current player
				if current and (c in current.targets):	
					m += bold

				# if it's in range, change the character to display
				if current and ((x,y) in current.in_range):
					m += '?'
				else:
					m += c.t 
	
				# and turn off the color
				m += nocolor

			m += "  "
			#m += "".join(map(lambda x: str(x), [ r in row if r.y == i]))
			m += ", ".join(map(lambda x: str(x), [ p for p in self.players if p.y == y ]))
			self.screen[y].status(m)

class Square:

	def __init__(self, x, y, t):
	
		self.x = x
		self.y = y
		self.t = t
		self.current = False

		if self.is_player:
			self.hp = 300
			self.ap = 3

	def __repr__(self):
		
		m = "{}{}({:02d},{:02d})".format('*' if self.current else ' ', self.t, self.x, self.y)
		return m

	def is_player(self):
		return self.t in "EG"

	def start_turn(self):
		if self.is_player == False:
			raise Exception("non pieces don't have turns")
		self.current = True
		self.targets = []
		self.in_range = []

	def end_turn(self):
		if self.is_player == False:
			raise Exception("non pieces don't have turns")
		self.current = False
		self.targets = None
		self.in_range = None

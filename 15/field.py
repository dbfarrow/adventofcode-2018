#!/usr/bin/env python

from pwn import *

class Field:

	def __init__(self, lines):

		# set up the field of action and 
		# the progress indicators we will be using to 
		# animate the game play
		self.rows = []
		self.players = {}
		self.positions = []
		self.order = None
		self.screen = []

		# create the visual screen elements. Each row of the
		# field is represented by a progress bar that will be updated
		# each move. 
		# In the process, extract the players from the field
		# and store them in a separate list
		for y, l in enumerate(lines):
			l = l.rstrip()
			self.screen.append(log.progress(""))
			row = []
			for x, c in enumerate(l):
				square = Square(x, y, c)
				row.append(square)
				if square.is_player():
					p = Square(x, y, c)
					p.name = "{}-{}".format(p.t, len(self.players))
					self.players[(x,y)] = p
					square.t = '.'
	
			self.rows.append(row)
				

	''' Stateful list of players in the order they must take their turn 
		in the current round. When the self.order is empty, a new round
		is starting. It is populated with the list of living players
		sorted in reading order. Players continue to move in this order
		even if a move by another player within the round changes the 
		reading order of the players. '''
	''' TODO - verify that play continues in the same order even if 
		a move changes the order '''
	def next_player(self):
			
		if self.order == None:
			# make a copy of the players list so that changes to it don't affect play order
			self.positions = dict(self.players) 
			self.order = sorted(self.positions.keys(), cmp=compare_positions)

		if len(self.order) == 0:
			self.order = None
			self.positions = None
			return None
		else:
			n = self.order[0]
			del self.order[0]
			return self.positions[n]

	def get_square(self, x, y):
		return self.rows[y][x]

	''' Removes from the active player list any players whose hit points
		have dropped to zero or below. 
		The function returns False if both teams still have players alive. '''
	def harvest_the_dead(self):

		for p in self.players.values():
			if p.hp <= 0:
				del self.players[(p.x, p.y)]
				log.info("%s is dead and has been carted away", p)
		
		elves = [ p for p in self.players.values() if p.t == 'E' ]
		goblins = [ p for p in self.players.values() if p.t == 'G' ]
		
		# if either the elves or the goblins are all gone, return
		# True to indicate that the battle is over
		return len(elves) == 0 or len(goblins) == 0

	''' Finds all players on the board that are of the opposing type
		from the player passed in. The list of targets is sorted in 
		reading order relative to the entire board '''
	def find_targets(self, player):

		targets = []
		for p in self.players.values():
			if p.is_player() and p.t != player.t:
				targets.append(p)

		# TODO - sort by reading order
		return targets
			
	''' Finds all squares adjacent to target players that can be
		occupied by the player passed in. This list will be used
		as an input to the shorted path algorithm. The list of
		attack points does not need to be sorted. '''
	def find_attack_positions(self, player):

		positions = []

		#target = None
		#min_d = 0xffff
		
		#if player.t == 'E':
			#context.log_level = 'debug'

		log.debug("getting attack positions for: %s", (player.x, player.y))
		#log.debug("  choosing from: %s", self.players.values())

		#for p in self.players.values():
		targets = self.find_targets(player)
		for t in targets:

			adjacencies = [ (0,-1), (-1,0), (1,0), (0,1) ]
			for adj in adjacencies:
				x = t.x+adj[0]
				y = t.y+adj[1]
				a = self.rows[y][x]
				op = (x,y) in self.players
				if a.t in '.?' and not op:
					log.debug("found: %s", a)
					positions.append(a)
	
			#if p.x == player.x and p.y == player.y:
				#log.debug("skipping %s", p)
				#continue
			#if p.t == player.t:
				#log.debug("skipping %s", p)
				#continue

			#d = abs(p.x - player.x) + abs(p.y - player.y)
			#if d < min_d:
				#target = p
				#min_d = d
				#log.debug("setting target %s with d=%d", target, d)
			#elif d == min_d:
				#log.debug("choosing between: target:%d,%d and p=%d,%d", target.x, target.y, p.x, p.y)
				#if p.y < target.y:
					#log.debug("p has smaller y: %s", p)
					#log.debug("target=%s", target)
					#target = p
				#elif p.y == target.y and p.x < target.x:
					#log.debug("p has smaller x: %s", p)
					#log.debug("p.y=%d, target.y=%d", p.y, target.y)
					#log.debug("target=%s", target)
					#target = p
				#else:
					#log.debug("skipping: %s", p)
			#else:
				#log.debug("%s too far away: %d", p, d)

		#if player.t == 'E':
			#context.log_level = 'info'

		#log.debug("best target for %s: %s,%s; distance=%d", player, target.x, target.y, d)

		#positions = []
		#if target:
			#adjacencies = [ (0,-1), (1,0), (0,1), (-1,0) ]
			#for adj in adjacencies:
				#a = self.get_square(target.x+adj[0], target.y+adj[1])
				#if a.t in '.?' and op != None:
					#log.debug("found: %s", a)
					#positions.append(a)
	
		return positions

	''' Finds all enemy players that are within attack range of the player
		passed in. The list must return the first target in reading order 
		if there is more than one target in range '''
	def select_target(self, player):

		log.debug("getting targets for: {}".format((player.x, player.y)))
		in_range = []

		for p in self.players.values():
			if p.t == player.t:
				continue

			d = abs(p.x - player.x) + abs(p.y - player.y)
			if d == 1:
				in_range.append(p)
				log.debug("attack %s", p)
			else:
				log.debug("%s not in range; d=%d", p, d)

		if len(in_range) > 1:
			# sort them in reading order
			in_range.sort(cmp=compare_reading_order)
			return in_range[0]
		elif len(in_range) == 1:
			return in_range[0]
		else:
			return None

	''' A neighbor is any adjacent square that is open or is occupied by an enemy '''
	def get_neighbors(self, node):

		#log.debug("getting neighbors for: {}".format((node.x, node.y)))
		#adjacencies = [ (0, -1), (0, 1), (1,0), (-1,0) ]
		#adjacencies = [ (0, -1), (1, 0), (0, 1), (-1,0) ]
		adjacencies = [ (-1, 0), (1, 0), (0, -1), (0, 1) ]
		x = node.x
		y = node.y
		neighbors = []

		for adj in adjacencies:
			a = self.get_square(x+adj[0], y+adj[1])
			op = self.players[(x+adj[0],y+adj[1])] if (x+adj[0], y+adj[1]) in self.players else None
			if a.t in '.?' and (op == None or op.t != node.t):
				#log.info("found: {}: {}".format((a.x, a.y), a.t))
				neighbors.append(a)

		return neighbors

	def move(self, node, new_pos):
	
		try:
			old_pos = (node.x, node.y)
			p = self.players[old_pos]
			p.x = new_pos.x
			p.y = new_pos.y
			del self.players[old_pos]
			self.players[(new_pos.x, new_pos.y)] = p
			return p
		
		except:
			log.info("no player at {}".format(node))
			return None

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
		currents = [ p for p in self.players.values() if p.current ]
		current = None
		if len(currents) > 0:
			current = currents[0]

		# now draw the map
		for y, row in enumerate(self.rows):
			m = ""
			pir = [ p for p in self.players.values() if p.y == y ]

			for x, c in enumerate(row):

				pis = [ p for p in pir if p.x == x]
				p = pis[0] if len(pis) > 0 else None
	
				# select the color based on what's in the cell
				t = c.t if len(pis) == 0 else pis[0].t
				m += colors[t]

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
					m += t 
	
				# and turn off the color
				m += nocolor

			m += "  "
			#m += "".join(map(lambda x: str(x), [ r in row if r.y == i]))
			ps = sorted([ p for p in self.players.values() if p.y == y ], compare_reading_order)
			m += ", ".join(map(lambda x: str(x), [ p for p in ps if p.y == y ]))
			self.screen[y].status(m)


def compare_reading_order(a, b):
	if a.y != b.y:
		return a.y - b.y
	elif a.x != b.x:
		return a.x - b.x
	else:
		return 0

def compare_positions(a, b):
	if a[1] != b[1]:
		return a[1] - b[1]
	else:
		return a[0] - b[0]



class Square:

	def __init__(self, x, y, t):
	
		self.x = x
		self.y = y
		self.t = t
		self.name = ""

		self.current = False

		if self.is_player:
			self.hp = 300
			self.ap = 3

	def __repr__(self):
		
		m = "{}{}({:02d},{:02d}) hp={}".format('*' if self.current else ' ', self.name, self.x, self.y, self.hp)
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

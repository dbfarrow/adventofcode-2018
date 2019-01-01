#!/usr/bin/env python

from pwn import *
from graph import *

class Field:

	def __init__(self, filename, lines, headless=False):

		# set up the field of action and 
		# the progress indicators we will be using to 
		# animate the game play
		self.rows = []
		self.players = {}
		self.screen = []
		self.headless = headless
		self.current = None

		# create the visual screen elements. Each row of the
		# field is represented by a progress bar that will be updated
		# each move. 
		# In the process, extract the players from the field
		# and store them in a separate list
		for y, l in enumerate(lines):
			l = l.rstrip()
			if not headless:
				self.screen.append(log.progress(filename))
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
				
		self.h = len(self.rows)
		self.w = len(self.rows[0])

	def set_ap(self, t, ap):
		
		for p in self.players.values():
			if p.t == t:
				p.ap = ap

	def next_player(self, turn):
		
		ps = [ p for p in self.players.values() if p.turn < turn ]
		if len(ps) == 0:
			return None
		else:
			ps.sort(cmp=compare_reading_order)
			pn = ps[0]
			pn.turn = turn
			return pn

	def get_square(self, x, y):
		try:
			if (x,y) in self.players:
				return self.players[(x,y)]
			else:
				return self.rows[y][x]
		except:
			log.failure("x,y     = %d,%d", x, y)
			log.failure("players = %s", self.players)
			player = (x,y) in self.players
			log.failure("player  = %s", foo)
			exit(-1)

	def get_move(self, p):

		# get the list of nodes that could be the next move
		next_moves = [ n for n in self.get_neighbors(p) if n.t == '.' ]
		log.debug("current player    = %s", p)
		log.debug("possible moves    = %s", next_moves)

		ts = self.select_target(p)
		if ts:
			log.debug("%s won't move, attacking: %s", p, ts)
			return None

		# then find all the positions adjacent to any enemy
		aps=[]
		ts = [ t for t in self.players.values() if t.is_player() and p.t != t.t ]
		for t in ts:
			aps.extend([ n for n in self.get_neighbors(t) if n.t == '.' ])
		log.debug("enemy players      = %s", ts)
		log.debug("adjacent positions = %s", aps)
	
		# for each of the nodes that could be the next move, determine
		# the shortest path from that node to each of the positions
		# adjacent to a target
		paths = []
		for n in next_moves:
	
			# if the move puts us into a position adjacent to the enemy
			# then it's a good move
			if n in aps:
				nn = Node(n)
				nn.distance = 0
				paths.append((n, 0, nn))
			else:
				g = Graph(self, p, n, aps)
				paths.extend([ (n, p.distance, p) for p in g.paths ])

		if len(paths) == 0:
			log.debug("no paths exist to targets")
			return None

		min_d = min([ x[1] for x in paths ])
		min_paths = [ p for p in paths if p[1] == min_d ]	
		moves = sorted(min_paths, cmp=compare_reading_order, key=lambda x: x[0])
		
		for mp in moves:
			log.debug("%d,%d: %d %d,%d", mp[0].x, mp[0].y, mp[1], mp[2].x, mp[2].y)

		if len(moves) > 0:
			m = moves[0][0]
			if m in self.players.keys():
				raise Exception ("can't move on top of another player")
			else:	
				return m
		else:
			return None

	''' Removes from the active player list any players whose hit points
		have dropped to zero or below. 
		The function returns False if both teams still have players alive. '''
	def harvest_the_dead(self, turn):

		for p in self.players.values():
			if p.hp <= 0:
				del self.players[(p.x, p.y)]
				log.debug("%s is dead and has been carted away", p)
		
		elves = [ p for p in self.players.values() if p.t == 'E' ]
		goblins = [ p for p in self.players.values() if p.t == 'G' ]
		
		# if either the elves or the goblins are all gone, return
		# True to indicate that the battle is over
		return len(elves) == 0 or len(goblins) == 0

	''' Finds all squares adjacent to target players that can be
		occupied by the player passed in. This list will be used
		as an input to the shorted path algorithm. The list of
		attack points does not need to be sorted. '''
	def find_attack_positions(self, player):

		positions = []
		log.debug("getting attack positions for: %s", (player.x, player.y))

		targets = [ t for t in self.players.values() if t.is_player() and t.t != player.t ]
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
			min_hp = min([ x.hp for x in in_range ])
			weakest = [ x for x in in_range if x.hp == min_hp ]
			if len(weakest) > 1:
				weakest.sort(cmp=compare_reading_order)
				return weakest[0]
			else:
				return weakest[0]
		elif len(in_range) == 1:
			return in_range[0]
		else:
			return None

	''' A neighbor is any adjacent square that is open or is occupied by an enemy '''
	def get_neighbors(self, node):

		#log.debug("getting neighbors for: {}".format((node.x, node.y)))
		adjacencies = map(lambda x: (node.x+x[0], node.y+x[1]), [ (-1, 0), (1, 0), (0, -1), (0, 1) ])
		inbounds = [ a for a in adjacencies if a[0] >= 0 and a[0] < self.w and a[1] >= 0 and a[1] < self.h ]
		neighbors = [ self.get_square(x[0], x[1]) for x in inbounds ]
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

		if self.headless:
			return

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
		self.name = None

		self.current = False

		if self.is_player:
			self.hp = 200
			self.ap = 3
			self.turn = -1

	def __repr__(self):
		
		m = "{}{}({:02d},{:02d})".format('*' if self.current else ' ', self.name if self.name else self.t, self.x, self.y)
		if self.t in [ 'E', 'G' ]:
			m += " hp={}".format(self.hp)
		return m

	def is_player(self):
		return self.t in "EG"

	def start_turn(self):
		if self.is_player == False:
			raise Exception("non pieces don't have turns")
		self.current = True

	def end_turn(self):
		if self.is_player == False:
			raise Exception("non pieces don't have turns")
		self.current = False

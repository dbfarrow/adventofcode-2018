#!/usr/bin/env python

from field import *
from pwn import *

class Graph:
   
	def __init__(self, field, start, ends):

		self.field = field
		self.start = start
		self.current = Node(start)
		self.current.distance = 0 

		self.unvisited = [ self.current ]
		self.visited = []
		self.paths = []

		step = 0
		terminal_nodes = [ (e.x, e.y) for e in ends ]
		log.debug("terminal nodes: %s", terminal_nodes)

		while (len(self.unvisited) > 0):

			#log.debug("%d: unvisited: %s", step, self.unvisited)

			# get the next unvisited node. The docs suggest
			# selecting the node with the lowest distance value
			# but we're tying it without sorting
			cn = self.unvisited.pop(0)
			#log.debug("%d: current node: %s", step, cn)
			#log.debug("%d: unvisited   : %s", step, self.unvisited)
			
			# find each neighbor of the current node and 
			# add one to each node's distance - because
			# the cost to move to any node is the same as 
			# moving to any other. 
			neighbors = self.field.get_neighbors(cn.data)
			#log.debug("%d: neighbors   : %s", step, neighbors)
			for n in neighbors:
				npos = (n.x, n.y)
				if npos in [ (v.x, v.y) for v in self.visited ]:
					#log.debug("%d: %s has already been visited", step, npos)
					continue

				# calculate the cost of choosing this node as the next 
				# step. Hopefully this will solve the problem of identifying
				# the shortest path that moves in reading order when there
				# are multiple shortest paths
				cost = None
				if n.y < cn.y:
					cost = 0
				elif n.y == cn.y:
					cost = 1 if n.x < cn.x else 2
				else:
					cost = 3

				# If the node has been seen already but not fully visited, 
				# we need to treat it differently 
				#un = self.unvisited[npos] if npos in self.unvisited else None
				un = None
				for ux, u in enumerate(self.unvisited):
					if (u.x, u.y) == npos:
						un = u
						break
				
				if un:
				#if npos in self.unvisited:
					#un = self.unvisited[ux]
					cost = un.cost*10 + cost
					#log.debug("%d: neighbor %s already in unvisited", step, npos)
					#log.debug("%d:     unvisited: %s", step, self.unvisited)
					if cn.distance + 1 < un.distance:
						un.distance = cn.distance + 1
						un.parent = cn
						un.cost += cost
						self.unvisited[ux].distance = cn.distance + 1
						self.unvisited[ux].parent = cn
						#self.unvisited[ux].cost += cost
						#log.debug("%d: updating distance and parent: cn=%s, u=%s", step, cn, un)
					elif cost < cn.cost:
						#log.debug("%d: u already has shortest distance: u.distance=%s < cn.distance+1=%s", step, un.distance, cn.distance+1)
						un.parent = cn
						#un.cost += cost
						un.cost += (un.cost * 10) + cost
						#self.unvisited[ux].parent = cn
						#self.unvisited[ux].cost += cost	
				else:
					nn = Node(n)
					nn.distance = cn.distance + 1
					nn. cost = cost
					nn.parent = cn
					self.unvisited.append(nn)
					#log.debug("%d: neighbor %s seen for first time", step, npos)
					#log.debug("%d:     unvisited=%s", step, self.unvisited)
					if (n.x, n.y) in terminal_nodes:
						log.debug("%s is a terminal node", nn)
						nn.terminal = True
						self.paths.append(nn)
	
			# Mark the current node as visited
			self.current.visited = True
			self.visited.append(cn)
			#log.debug("%d: marking %s as visited", step, cn)
			#log.debug("%d:     visited=%s", step, self.visited)

			step += 1

		#log.debug("%d: done", step)
		log.debug("num paths: %d", len(self.paths))
		for ix, path in enumerate(self.paths):
			log.debug("path[%d]: pos=%s, distance=%s", ix, (path.x, path.y), path.distance)
			while path.parent:	
				log.debug("    %s->%s", (path.parent.x, path.parent.y), (path.x, path.y))
				path = path.parent


	''' Select a move from the set of paths calculated. If there is more than
		one shortest path, select the one whose next move comes first in reading
		order '''
	def get_move(self):

		# find the shortest path(s)
		min_d = min(p.distance for p in self.paths)
		paths = [ p for p in self.paths if p.distance == min_d ]
		steps = [ self.get_next_step_in_path(p) for p in paths ]
		moves = sorted(steps, cmp=lambda a,b: compare(a, b))
		#if len(moves) > 1:
			#log.info("%s", self.start)
			#log.info("  paths = %s", paths)
			#log.info("  steps = %s", steps)
			#log.info("  moves = %s", moves)

		if len(moves) > 0:
			m = moves[0]
			return m
		else:
			return None

	def get_next_step_in_path(self, p):
		
		m = p
		while m.parent and m.parent.parent:
			m = m.parent
		return m

	def __repr__(self):
		
		return ",".join([ str(u) for u in self.unvisited ])

def compare(a, b):
	
	if a.distance != b.distance:
		return a.distance - b.distance
	elif a.y != b.y:
		return a.y - b.y
	elif a.x != b.x:
		return a.x - b.x
	else:
		return 0

	
class Node:

	def __init__(self, data):

		self.data = data
		self.x = data.x
		self.y = data.y
		self.distance = 0xffff
		self.cost = 0
		self.parent = None
		self.visited = False
		self.terminal = False

	def __repr__(self):
		ppos = (self.parent.x, self.parent.y) if self.parent else None
		return "({}) -> ({}) d={}, c={}, term={}".format(ppos, (self.x, self.y), self.distance, self.cost, self.terminal)

	def __repr2__(self):

		path = []
		p = self
		coords = (p.x, p.y)
		while p.parent:
			path.append(coords)
			p = p.parent
		path.append(coords)
		path.reverse() 
		return "{}, parent={}, distance={}".format((self.x, self.y), path, self.distance)


if __name__ == "__main__":

	lines = [
		'#####',
		'#E..#',
		'#...#',
		'#..G#',
		'#...#',
		'#...#',
		'#####',
		#'##############',
		#'#E..#........#',
		#'#...#..##..#.#',
		#'#...#.G#...#.#',
		#'#...####...#.#',
		#'#..........#.#',
		#'##############',
		#'#######',
		#'#.G...#',
		#'#...EG#',
		#'#.#.#G#',
		#'#..G#E#',
		#'#.....#',
		#'#######',
	]

	context.log_level = 'info'

	field = Field(lines)
	field.render()
	sleep(1)

	p = field.players[(1, 1)]
	t = field.players[(3, 3)]
	g = Graph(field, p, [ t ])
	while True:

		aps = field.find_attack_positions(p)
		#log.info("aps: %s", aps)
		g = Graph(field, p, aps)
		move = g.get_move()
		if move:
			p = field.move(p, move)
			if move.terminal:
				targets = field.select_target(p)
				log.info("die, gravy sucking pig!: {}".format(targets))
				break

			field.render()
			sleep(1)
		else:
			break

	field.render()
	log.success("Qapla!!")


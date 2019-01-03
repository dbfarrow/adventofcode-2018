#!/usr/bin/env python

from field import *
from pwn import *

class Graph:
   
	def __init__(self, field, player, start, ends):

		#raise Exception("%s", player.t)

		self.field = field
		self.start = start
		self.current = Node(start)
		self.current.distance = 0 

		self.unvisited = [ self.current ]
		self.visited = []
		self.paths = []

		step = 0
		terminal_nodes = [ (e.x, e.y) for e in ends ]
		#log.debug("terminal nodes: %s", terminal_nodes)

		min_distance = None

		while (len(self.unvisited) > 0):

			# Once we find a path to a target, then any node we search
			# that is farther away is, by definition, not a shortest path.
			# So we can stop looking
			if min_distance == None and len(self.paths) > 0:
				min_distance = self.paths[0].distance
			if min_distance and (min([ u.distance for u in self.unvisited ]) > min_distance):
				return
	
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
			neighbors = [ n for n in self.field.get_neighbors(cn.data) if n.t == '.' ] #in [ '.', field.current.t ] ]
			#log.debug("%d: neighbors   : %s", step, neighbors)
			for n in neighbors:
				npos = (n.x, n.y)
				if npos in [ (v.x, v.y) for v in self.visited ]:
					#log.debug("%d: %s has already been visited", step, npos)
					continue

				# If the node has been seen already but not fully visited, 
				# we need to treat it differently 
				#un = self.unvisited[npos] if npos in self.unvisited else None
				un = None
				for ux, u in enumerate(self.unvisited):
					if (u.x, u.y) == npos:
						un = u
						break
				
				if un:
					#log.debug("%d: neighbor %s already in unvisited", step, npos)
					#log.debug("%d:     unvisited: %s", step, self.unvisited)
					if cn.distance + 1 < un.distance:
						self.unvisited[ux].distance = cn.distance + 1
						self.unvisited[ux].parent = cn
						#log.debug("%d: updating distance and parent: cn=%s, u=%s", step, cn, un)
					#else:
						#log.debug("%d: u already has shortest distance: u.distance=%s < cn.distance+1=%s", step, un.distance, cn.distance+1)
				else:
					nn = Node(n)
					nn.distance = cn.distance + 1
					nn.parent = cn
					self.unvisited.append(nn)
					#log.debug("%d: neighbor %s seen for first time", step, npos)
					#log.debug("%d:     unvisited=%s", step, self.unvisited)
					if (n.x, n.y) in terminal_nodes:
						#log.debug("%s is a terminal node", nn)
						nn.terminal = True
						self.paths.append(nn)
	
			# Mark the current node as visited
			self.current.visited = True
			self.visited.append(cn)
			#log.debug("%d: marking %s as visited", step, cn)
			#log.debug("%d:     visited=%s", step, self.visited)

			step += 1

		#log.debug("%d: done", step)
		#log.debug("num paths: %d", len(self.paths))
		#for ix, path in enumerate(self.paths):
			#log.debug("path[%d]: pos=%s, distance=%s", ix, (path.x, path.y), path.distance)
			#while path.parent:	
				#log.debug("    %s->%s", (path.parent.x, path.parent.y), (path.x, path.y))
				#path = path.parent


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
		self.parent = None
		self.visited = False
		self.terminal = False

	def __repr__(self):
		ppos = (self.parent.x, self.parent.y) if self.parent else None
		return "({}) -> ({}) d={}, term={}".format(ppos, (self.x, self.y), self.distance, self.terminal)

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


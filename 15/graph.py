#!/usr/bin/env python

from field import *
from pwn import *

class Graph:

	def __init__(self, field, source):

		self.field = field
		self.source = source
		self.destinations = []
		self.visited = []
		self.paths = Node(self, None, source, 0) 
		

class Node:
	
	def __init__(self, graph, parent, me, cost):

		if cost > 5:
			raise Exception("things are out of hand")

		self.graph = graph
		self.parent = parent
		self.me = me
		self.coords = (self.me.x, self.me.y)
		self.neighbors = []
		self.cost = cost
		
		log.debug("node {}: parent = {}, cost = {}".format(self.coords, self.parent.coords if self.parent else "None", self.cost))

		neighbors = self.get_neighbors(self.coords)
		for n in neighbors:
			loc = (n.x, n.y)
			if loc not in graph.visited:
				graph.visited.append(loc)
				log.debug("visited: {}".format(graph.visited))
				log.debug("adding neighbor: {}".format(loc))
				node = Node(graph, self, n, cost + 1)
				self.neighbors.append(node)
				if n.t != '.':
					log.info("hit terminal node: {}".format(n))
					self.graph.destinations.append(node)
				
	def __repr__(self):

		path = []
		p = self
		while p.parent:
			path.append(p.coords)
			p = p.parent
		path.append(p.coords)
		path.reverse() 
		return "{}, parent={}, cost={}".format(self.coords, path, self.cost)

	''' A neighbor is any adjaent square that is currently empty '''
	def get_neighbors(self, coords):
	
		log.debug("getting neighbors for: {}".format(coords))
		adjacencies = [ (0,-1), (1,0), (0,1), (-1,0) ]
		x = coords[0]
		y = coords[1]
		neighbors = []

		for adj in adjacencies:
			n = self.graph.field.rows[y+adj[0]][x+adj[1]]
			if n.t not in 'EG#':
				log.debug("found: {}".format((n.x, n.y)))
				neighbors.append(n)

		return neighbors


if __name__ == "__main__":

	lines = [
		'#######',
		'#E.?G?#',
		'#.?.#?#',
		'#?G?#G#',
		'#######',
	]

	context.log_level = 'debug'

	field = Field(lines)
	field.render()

	src = field.rows[1][1]
	g = Graph(field, src)
	
	for d in g.destinations:
		log.info(d)

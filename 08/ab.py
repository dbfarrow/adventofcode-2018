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
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 8")
	parser.add_argument('-t', '--testing', action='store_true', default=False)
	parser.add_argument('-v', '--verbose', action='store_true', default=False)
	parser.add_argument('-p', '--part')
	global CMDLINE 
	CMDLINE = parser.parse_args()

	context.log_level = 'debug' if CMDLINE.verbose else 'info'

def get_input():

	lines = []

	filename = "./input" if not CMDLINE.testing else "./input-test"
	with open(filename, "r") as infile:
		lines = infile.readlines()

	return lines

def do_part(part):
	if not CMDLINE.part or CMDLINE.part == part:
		return True
	else:
		return False

########################################################################
#
# Classes

class Node:
	
	__next_name = 0

	def __init__(self, data, p):
		
		# generate a name
		self.name = Node.make_name(p)

		# parse the header
		self.node_count = int(data[0])
		self.metadata_count = int(data[1])
		del data[:2]
		log.debug("  Node {} -> {} nodes, {} metadata".format(self.name, self.node_count, self.metadata_count))

		# parse the nodes
		self.nodes = []
		for i in range(self.node_count):
			log.debug("  node: next node header: {}".format(data[:2]))
			self.nodes.append(Node(data, p))

		# parse the medadata
		self.metadata = []
		for i in range(self.metadata_count):
			m = int(data[0])
			del data[0]
			self.metadata.append(m)
		log.debug("    meta: {}.metadata: {}".format(self.name, self.metadata))

		
	def __repr__(self):
		return self.name

	def sum_metadata(self):

		total = 0
		
		# get the metadata totals for all included nodes
		for n in self.nodes:
			#log.debug("adding metatdata for node {}".format(n.name))
			total += n.sum_metadata()

		# and add in the total for this node
		total += sum(self.metadata)	

		return total

	''' implements the summation of node valuations defined in part B of the challenge '''
	def metasum_nodes(self):

		log.debug("metasumming {}".format(self.name))

		total = 0

		# if the node has no children, then the value of the node is the 
		# sum of the metadata values
		if len(self.nodes) == 0:
			total += sum(self.metadata)
		else:
			for i in self.metadata:
				if i > 0 and i <= len(self.nodes):
					n =  self.nodes[i - 1]
					total += n.metasum_nodes()

			total += 0
			
		return total

	@classmethod
	def make_name(cls, p):

		name = str(cls.__next_name)
		cls.__next_name += 1
		p.status("making node {}".format(name))
		return name

########################################################################
#
# PART A

def do_partA(instr):

	log.info("AdventOfCode 2018 - day 8 part A")

	data = instr.split(' ')
	with log.progress('deserializing node tree') as p:
		top = Node(data, p)

	log.success(top.sum_metadata())


########################################################################
#
# PART B

def do_partB(instr):

	log.info("AdventOfCode 2018 - day 8 part B")

	data = instr.split(' ')
	with log.progress('deserializing node tree') as p:
		top = Node(data, p)

	log.success("{}".format(top.metasum_nodes()))


if __name__ == "__main__":

	parse_cmdline()

	lines = get_input()
	line = lines[0].rstrip()
	if do_part('a'):
		do_partA(line)

	if do_part('b'):
		do_partB(line)



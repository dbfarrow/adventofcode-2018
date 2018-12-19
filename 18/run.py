#!/usr/bin/env python

import argparse
from pwn import *
import time

########################################################################
#
# boilerplate script setup
#
# command line arguments
CMDLINE = None 

def parse_cmdline():
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 18")
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
		for ix, l in enumerate(infile):
			lines.append(list(l.rstrip()))

	return lines

def do_part(part):
    if not CMDLINE.part or CMDLINE.part == part:
        return True
    else:
        return False

########################################################################
#
# Classes / global functions

def get_surroundings(field, x, y):

	o = w = l = 0

	min_x = x if x == 0 else x - 1
	min_y = y if y == 0 else y - 1
	max_x = x + 1 if x < len(field[0]) - 1 else x 
	max_y = y + 1 if y < len(field) - 1 else y 
	#if (x == 8) and (y == 1):
		#log.debug("j: {}-{}, i: {}-{}".format(min_x, max_x, min_y, max_y))
		#exit(-1)

	for i in range(min_y, max_y+1):
		for j in range(min_x, max_x+1):
			if j == x and i == y:
				continue
			try:
				c = field[i][j]
				o += 1 if c == '.' else 0	
				w += 1 if c == '|' else 0	
				l += 1 if c == '#' else 0	
			except:
				log.info("!!! x={}, y={}".format(x, y))	
				log.info("  x: {},{}, y={},{} ".format(min_x, max_x, min_y, max_y))
				log.info("  h: {}, w: {}".format(len(field), len(field[y])))
				log.info("  {}".format("".join(field[y])))
				exit(-1)

			#if x == 8 and y == 1:
				#log.debug("field[{},{}] = {}".format(i,j,c))

	#log.debug("{},{}: c={}, o={}, w={}, l={} ".format(x, y, field[y][x], o, w, l))
	#log.debug("  x: {},{}, y={},{} ".format(min_x, max_x, min_y, max_y))
	#exit(-1)

	return [ o, w, l ]


__screen = None

def render(field):

	global __screen
	if __screen == None:
		__screen = [ log.progress("") for i in range(len(field)) ]

	for i, row in enumerate(field):
		__screen[i].status("".join(row))

########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day 18 part A")

	field = get_input()
	render(field)
	with log.progress("t") as p:
		for t in range(10):

			p.status(str(t))

			new_field = []
			for y, l in enumerate(field):
				row = []
				for x, u in enumerate(l):
					[ o, w, l ] = get_surroundings(field, x, y)
					if u == '.' and w >= 3:
						new_u = '|'
					elif u == '|' and l >= 3:
						new_u = '#' 
					elif u == '#' and (l < 1 or w < 1):
						new_u = '.'
					else:
						new_u = u
					row.append(new_u)
				new_field.append(row)
			field = new_field
			render(field)
			time.sleep(0.5)

	# count the wooded and lumberyard acres
	w = l = 0
	for row in field:
		for c in row:
			if c == '#':
				l += 1
			elif c == '|':
				w += 1

	log.info("w={}, l={}".format(w, l))
	log.success(w * l)

########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day 18 part B")

	field = get_input()
	scores = {}
	cycle = {}
	cycle_len = None
	cycle_base = None
	answer = 0

	target_time = 1000000000
	#target_time = 700

	with log.progress("t") as p:

		score = 0
		for t in range(1000):

			new_field = []
			for y, l in enumerate(field):
				row = []
				for x, u in enumerate(l):
					[ o, w, l ] = get_surroundings(field, x, y)
					if u == '.' and w >= 3:
						new_u = '|'
					elif u == '|' and l >= 3:
						new_u = '#' 
					elif u == '#' and (l < 1 or w < 1):
						new_u = '.'
					else:
						new_u = u
					row.append(new_u)
				new_field.append(row)
			field = new_field

			# count the wooded and lumberyard acres
			w = l = 0
			for row in new_field:
				for c in row:
					if c == '#':
						l += 1
					elif c == '|':
						w += 1
	
			score = w * l
			if score not in scores:
				scores[score] = [ t ]
			else:
				scores[score].append(t)

			if (len(scores[score]) == 4):
				#log.debug("scores[{}]: {}".format(score, scores[score]))
				deltas = []
				for i, s in enumerate(scores[score]):
					if i == 0:
						continue
					t1 = scores[score][i-1]
					t2 = scores[score][i]
					delta = t2 - t1
					#log.debug("s[{}]: {}, s[{}]: {}, d = {}".format(i-1, t1, i, t2, delta))
					deltas.append(delta)

				if len(set(deltas)) == 1 and cycle_base == None:
					cycle_len = deltas[0]
					cycle_base = t
					log.info("cycle: base={}, len={}".format(cycle_base, cycle_len))

			if len(cycle.keys()) == cycle_len:

				offset = ((target_time - cycle_base) % cycle_len) - 1
				if offset < 0:
					offset = cycle_len - 1
				answer = cycle[offset]
				#if ((t - cycle_base) % cycle_len) == 0:
					#answer = cycle[(t - cycle_base) % cycle_len]
					#log.info("t:{}, expected:{}, got: {}".format(t, answer, score))
				break	

			elif cycle_len > 0:
				cycle_ix = t - cycle_base
				log.debug("cycle[{}]: {}".format(cycle_ix, score))
				cycle[cycle_ix] = score

			if t % 100 == 0:
				p.status("{},{}".format(t, w * l))

		#log.info("score:{}, answer: {}".format(score, answer))
		log.success(answer)

	log.failure("not implemented")


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

#!/usr/bin/env python

import re
import argparse
from pwn import *

########################################################################
#
# boilerplate script setup
#
# command line arguments
CMDLINE = None 

def parse_cmdline():
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 10")
	parser.add_argument('-t', '--testing', action='store_true', default=False)
	parser.add_argument('-v', '--verbose', action='store_true', default=False)
	parser.add_argument('-p', '--part')
	parser.add_argument('-s', '--start-time', default=10000)	# start at t=10000 for runs of real data (to save time)
	global CMDLINE 
	CMDLINE = parser.parse_args()

	context.log_level = 'debug' if CMDLINE.verbose else 'info'

def get_input():

	lines = []

	filename = "./input" if not CMDLINE.testing else "./input-test"
	with open(filename, "r") as infile:
		for i, line in enumerate(infile):
			lines.append(Point(line))

	return lines

def do_part(part):
    if not CMDLINE.part or CMDLINE.part == part:
        return True
    else:
        return False

########################################################################
#
# Classes

class Point:

	def __init__(self, data):

		m = re.match("position=<(.+),(.+)> velocity=<(.+),(.+)>", data)
		if m:
			self.px = int(m.group(1))
			self.py = int(m.group(2))
			self.vx = int(m.group(3))
			self.vy = int(m.group(4))

	def __repr__(self):
		return "({}, {}) going {},{})".format(self.px, self.py, self.vx, self.vy)

def calc_bounds(points, t):

	max_x = 0
	max_y = 0
	min_x = 0x7fffffff
	min_y = 0x7fffffff

	for p in points:
		px = p.px + (p.vx * t)
		py = p.py + (p.vy * t)

		log.debug("{}, {}".format(px, py))

		if px < min_x:
			min_x = px
		if px > max_x:
			max_x = px
		if py < min_y:
			min_y = py
		if py > max_y:
			max_y = py
		w = max_x - min_x
		h = max_y - min_y
		area = w * h

	log.debug("bounds: {}x{} at ({},{}) - area = {}".format(w, h, min_x, min_y, area))
	log.debug("")
	return [ min_x, min_y, w, h ]

def print_message(points, min_x, min_y, min_w, min_h, min_t):

	log.info("allocating {}x{} array at ({}, {})".format(min_w + 1, min_h + 1, min_x, min_y))

	# allocate the data structure for the message
	msg = []
	for h in range(min_h + 1):
		msg.append([ "." for w in range(0, min_w + 1) ])

	# now plot the points 
	for t in range(len(points)):
		p = points[t]
		x = p.px + (p.vx * min_t)
		y = p.py + (p.vy * min_t)
		log.debug("{}, {}".format(x, y))
		msg[y - min_y][x - min_x] = "#"

	# and print it
	for m in msg:
		log.info("".join(m))

########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day 10 part A")

	points = get_input()

	[ min_x, min_y, min_w, min_h ] = calc_bounds(points, 0)
	min_area = min_w * min_h
	min_t = 0

	with log.progress("") as p:
		t = CMDLINE.start_time 
		while 1:
			[ x, y, w, h ] = calc_bounds (points, t)
			area = w * h
			if area < min_area:
				min_x = x
				min_y = y
				min_w = w
				min_h = h
				min_area = area
			elif area > min_area:
				log.info("Y axis began expanding at t = {}".format(t))
				print_message(points, min_x, min_y, min_w, min_h, t - 1)

				global part_b_answer
				part_b_answer = t - 1
				break
	
			t += 1
			if t % 100 == 0:
				p.status("{}: {}x{} ({}) at ({}, {})".format(t, min_w, min_h, min_area, min_x, min_y))


	log.success("read the message above ^")

########################################################################
#
# PART B

part_b_answer = -1

def do_partB():

	log.info("AdventOfCode 2018 - day 10 part B")
	log.success(str(part_b_answer))

if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

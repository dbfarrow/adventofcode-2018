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
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day N")
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

	return sorted(lines)

def do_part(part):
    if not CMDLINE.part or CMDLINE.part == part:
        return True
    else:
        return False

########################################################################
#
# Classes

header = """Date   ID    Minute
             000000000011111111112222222222333333333344444444445555555555
             012345678901234567890123456789012345678901234567890123456789"""

class Guard:

	def __init__(self, guard_id):
		self.id = guard_id
		self.total_sleep = 0
		self.napmap = [ 0 for i in range(0, 60) ]
		self.naps = []
	
	def add_nap(self, nap):

		self.naps.append(nap)
		self.total_sleep += nap.duration
		
		for i in range(0, len(nap.napmap)):
			self.napmap[i] += nap.napmap[i]

class Nap:

	def __init__(self, gid):
		self.date = None
		self.gid = gid
		self.sleep = 0
		self.wake = 0
		self.duration = 0
		self.napmap = [ 0 for i in range(0,60) ]

	def start(self, datestr):

		# parse the start date and time out
		m  = re.match('\[[0-9]{4}-([0-9]{2}-[0-9]{2}) [0-9]{2}:([0-9]{2})\].*', datestr)
		if m:
			self.date = m.group(1)
			self.sleep = int(m.group(2))

		#print("{}: sleeping at: {} on {}".format(datestr, self.sleep, self.date))
		return

	def end(self, datestr):

		# parse the start date and time out
		m  = re.match('\[[0-9]{4}-([0-9]{2}-[0-9]{2}) [0-9]{2}:([0-9]{2})\].*', datestr)
		if m:
			date = m.group(1)
			if date != self.date:
				raise Exception("guard woke up on a different day than he went to sleep: {}".format(datestr))
			self.wake = int(m.group(2))

		# now we can fill in the sleep map and calculate the duration
		for i in range(self.sleep, self.wake):
			self.napmap[i] += 1
		self.duration = self.wake - self.sleep

		#print("{}: waking at: {} on {}".format(datestr, self.wake, self.date))
		return

	def display(self):
		s = ""
		for t in self.napmap:
			s +=  '.' if t == 0 else '#' 
		return s

def get_guards():

	guards = {}
	naps = []
	current_guard = None
	nap = None

	lines = get_input()
	for line in lines:

		# check if a new guard came on duty
		m = re.match("(.*) Guard (.*) begins shift", line)
		if m:
			gid = m.group(2)	
			if gid not in guards:
				guards[gid] = Guard(gid)
			current_guard = guards[gid]
			continue
		
		# check if a guard fell asleep
		m = re.match(".* falls asleep", line)
		if m:
			nap = Nap(current_guard.id)
			nap.start(line)
			naps.append(nap)

		# check if a guard woke up
		m = re.match(".* wakes up", line)
		if m:
			if nap == None:
				raise Exception("guard work up without falling asleep... something is wrong")
			else:
				nap.end(line)
				current_guard.add_nap(nap)
				nap = None

	# print out the list of naps with their napmaps
	log.debug(header)
	for n in naps:
		log.debug("{d}  {s:{n}} {m}".format(d=n.date, s=n.gid, n=5, m=n.display()))
	log.debug("")

	return guards

def napmap_header():

	h1 = ''
	for i in range(0, 6):
		h1 += str(i)*10
	
	h2 = ''
	for i in range(0,6):
		for j in range(0, 10):
			h2 += str(j)

	return [
		"Date  ID   Minute",
		"           {}".format(h1),
		"           {}".format(h2),
	]
	
def find_sleepiest_minute(guards):

	guard = None
	minute = -1
	times = 0

	for gid, g in guards.items():
		for i in range(0, 60):
			if g.napmap[i] > times:
				times = g.napmap[i]
				minute = i
				guard = gid
				
	return [ guard, minute, times ]



########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day N part A")

	# the sleepiest guard is the one with the most total sleep. dig how
	# pythonic this answer is...
	guards = get_guards()
	g = max(guards.values(), key=lambda item: item.total_sleep)
	m = g.napmap.index(max(g.napmap))
	a = int(g.id.replace("#", "")) * int(m)
	log.info("{} is the sleepiest guard with {} total nap minutes".format(g.id, g.total_sleep))
	log.info("{} is his sleepiest minute".format(m))
	log.info("part A: {} x {} = {}".format(g.id, m, a))
	log.success(a)


########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day N part B")

	guards = get_guards()
	[g, m, n]  = find_sleepiest_minute(guards)
	g = int(g.replace("#", ""))
	log.info("{} slept during {} {} times".format(g, m, n))  
	log.info("part B: {} x {} = {}".format(g, m, g*m))
	log.success(str(g*m))


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()


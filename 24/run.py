#!/usr/bin/env python

import argparse
from pwn import *
import re

########################################################################
#
# boilerplate script setup
#
# command line arguments
CMDLINE = None 

def parse_cmdline():
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 24")
	parser.add_argument('-t', '--testing', action='store_true', default=False)
	parser.add_argument('-v', '--verbose', action='store_true', default=False)
	parser.add_argument('-p', '--part')
	global CMDLINE 
	CMDLINE = parser.parse_args()

	context.log_level = 'debug' if CMDLINE.verbose else 'info'

def get_input():

	filename = "./input" if not CMDLINE.testing else "./input-test"
	with open(filename, "r") as infile:

		groups = []
		curren_army = None

		lines = infile.readlines()
		for ix, l in enumerate(lines):
		
			if re.match("^$", l):
				current_army = None
				continue

			m = re.match("(.*):", l)
			if m:
				current_army = m.group(1)
				log.info("current army: %s", current_army)
				continue
			else:
				groups.append(Group(current_army, l))

		return groups

def do_part(part):
    if not CMDLINE.part or CMDLINE.part == part:
        return True
    else:
        return False

########################################################################
#
# Classes

_counts = {}

class Group:

	def __init__(self, army, line):

		m = re.match("(\d+) units each with (\d+) hit points(.*)with an attack that does (\d+) (.*) damage at initiative (\d+)", line)
		if m:
			self.army = army
			self.count = int(m.group(1))
			self.hp = int(m.group(2))
			self.ap = int(m.group(4))
			self.type = m.group(5).replace(' ', '')
			self.initiative = int(m.group(6))
			self.weaknesses = ""
			self.immunities = ""

			# parse weaknesses and immunitities (wni)
			wnis = m.group(3).replace(' (', '').replace(') ', '')
			if wnis != ' ':
				wnis = wnis.split('; ')
				for wni in wnis:
					m = re.match("(\w+) to (.*)", wni)
					if m:
						which = m.group(1)
						attacks = m.group(2)
						if which == 'weak':
							self.weaknesses = attacks
						elif which == 'immune':
							self.immunities = attacks
						else:
							raise Exception("unexpected w&i: {}; which: {}".format(wni, which))
					else:
						raise Exception("no w&i found in: {}".format(wni)) 

			_counts[army] = _counts[army] + 1 if army in _counts else 1
			self.name = "{} {}".format(army, _counts[army])

			# state params used during battles
			self.target = None
			self.targeted = False
			self.kills = 0

		else:
			raise Exception("unexpected format: %s", line)

	''' effective power = # units x attack power / unit '''
	def effective_power(self):
		return self.count * self.ap

	def does_damages_to(self, target):
		
		damages = self.effective_power()
		if self.type in target.immunities:
			damages = 0
		elif self.type in target.weaknesses:
			damages *= 2
	
		return damages

	def __repr__(self):
		m = ''
		m += "name: {}".format(self.name)
		m += ", count: {}".format(self.count)
		m += ", hp: {}".format(self.hp)
		m += ", ep: {}".format(self.effective_power())
		m += ", ap: {}".format(self.ap)
		m += ", type: {}".format(self.type)
		m += ", weaknesses: {}".format(self.weaknesses)
		m += ", immunities: {}".format(self.immunities)
		m += ", initiative: {}".format(self.initiative)
		return m

''' Comparator for determining which group goes first in selecting targets
Groups are selected by:
	1. highest effective power, then by
	2. initiative
'''
def compare_groups(a, b):
	
	ep_a = a.effective_power()
	ep_b = b.effective_power()
	if ep_a != ep_b:
		return ep_b - ep_a
	else:
		return b.initiative - a.initiative

''' Comparator for determining target selections order:
Targets are selected by:
	1. highest expected damage, then by
	2. highest effective power, then by
	3. highest initiative
'''	
def compare_targets(a, b):
	da = a.does_damages_to(b)
	db = b.does_damages_to(a)

	if da != db:
		return da - db
	else:
		return compare(groups(a, b))	

########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day 24 part A")

	groups = get_input()
	while True:

		# sort the groups into targeting order
		groups.sort(key=lambda x: (x.effective_power(), x.initiative), reverse=True)
		log.debug("targt selection order:")
		for g in groups:
			log.debug("  %s: ep:%d, inititive: %d", g.name, g.effective_power(), g.initiative)	
			g.target = None
			g.targeted = False
			g.kills = 0

		log.debug("")
	   	
		# select the targets
		for g in groups:
			targets = [ t for t in groups if ((t.count > 0) and (t.army != g.army) and not t.targeted) ]
			#log.debug("attacker: %s", g.name)
			#log.debug("targets : %s", [ t.name for t in targets ])

			best_damage = 0
			best_choice = None
			for t in targets:
				damage = g.does_damages_to(t)
				if damage == 0:
					continue
				elif damage > best_damage:
					g.target = t
					best_damage = damage
				elif damage == best_damage:
					if t.initiative < g.target.initiative:
						g.target = t
			if g.target is not None:
				g.target.targeted = True
	
			#log.debug("%s targets %s for %d damage", g.name, g.target.name, best_damage)
			#log.debug("")

		attacks = sorted([ g for g in groups if g.target != None ], key= lambda x: x.initiative, reverse=True)
		for a in attacks:
			damages = a.does_damages_to(a.target) 
			units = min(damages/a.target.hp, a.target.count)
			a.target.count -= units
			log.debug("%s attacks %s killing %d units (damage: %d, hp: %d)", a.name, a.target.name, units, damages, a.target.hp)
		log.debug("")

		# check to see if anyone won
		armies = set([ g.army for g in groups if g.count > 0 ])
		log.debug("armies: %s", armies)
		if len(armies) == 1:
			total = 0
			for g in groups:
				log.debug("%s: %d", g.name, g.count)
				total += g.count
			log.success(total)
			return

########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day 24 part B")
	log.failure("not implemented")


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

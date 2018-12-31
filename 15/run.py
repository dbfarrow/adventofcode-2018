#!/usr/bin/env python

import argparse
from pwn import *
import time

from field import *
from graph import *

########################################################################
#
# boilerplate script setup
#
# command line arguments
CMDLINE = None 

def parse_cmdline():
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 15")
	#parser.add_argument('-t', '--testing', action='store_true', default=False)
	parser.add_argument('-t', '--testing', type=int, default=None)
	parser.add_argument('-v', '--verbose', action='store_true', default=False)
	parser.add_argument('-p', '--part')
	parser.add_argument('-d', '--delay', type=float, default=0.25)
	parser.add_argument('-c', '--confirm', action='store_true', default=False)
	global CMDLINE 
	CMDLINE = parser.parse_args()

	context.log_level = 'debug' if CMDLINE.verbose else 'info'

def get_input():

	lines = []

	filename = "./input" if not CMDLINE.testing else "./input-test-{}".format(CMDLINE.testing)
	with open(filename, "r") as infile:
		lines = infile.readlines()

	return Field(lines)

def do_part(part):
    if not CMDLINE.part or CMDLINE.part == part:
        return True
    else:
        return False

########################################################################
#
# Classes

def attack(field, a, t):

	t.hp -= a.ap
	if t.hp < 0:
		log.info("%s has died", t)
		field.remove_player(t)

########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day 15 part A")

	field = get_input()
	field.render()

	turn = 0
	with log.progress("turn") as tp:
		tp.status("0")
		a = raw_input("hit enter to continue; q to quit: ")
		if a.rstrip() == 'q':
			return
		while 1:
		
			p = field.next_player()
			if p == None:
				turn += 1
				tp.status("end of turn: {}".format(turn))
				log.info("end of turn: {}".format(turn))
				if CMDLINE.confirm:
				#if turn in [ 0, 1, 2, 23, 24, 25, 26, 27, 28, 47, 48 ]:
					a = raw_input("hit enter to continue; q to quit: ")
					if a.rstrip() == 'q':
						return
				continue
	
			log.debug("%s starting turn", p)
			p.start_turn()
			field.render()

			# emulate processing turn
			t = field.select_target(p)
			if t:
				log.debug("%s attacks %s without moving", p, p.targets)
				t.hp -= p.ap
			else:
				ts = field.find_targets(p)
				log.debug("%s targeting: %s", p, ts)
				g = Graph(field, p, ts)
				move = g.get_move()
				if move:
					src = field.move(p, move)
					log.debug("%s moving: %s", p, move)
					field.render()
					if move.terminal:
						t = field.select_target(p)
						if t:
							log.debug("%s attacks %s after moving", p, t)
							t.hp -= p.ap
						else:
							log.debug("no targets at terminal node?")
				else:
					log.info("no move?")

			if field.harvest_the_dead():
				log.info("the battle is over")
				log.info("last completed turn: %d", turn)
				total_hp = sum([ p.hp for p in field.players.values() ])
				log.info("victors' total hit points: %d", total_hp)
				log.success(turn * total_hp)
				break

			p.end_turn()
			log.debug("%s ending turn", p)
			log.debug("--------------")
			log.debug("")
			field.render()
			time.sleep(CMDLINE.delay)
	
			#break

	log.failure("not implemented")

########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day 15 part B")
	log.failure("not implemented")


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

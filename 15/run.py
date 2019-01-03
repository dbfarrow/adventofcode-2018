#!/usr/bin/env python

import sys
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
	parser.add_argument('-t', '--testing', action='store_true', default=False)
	parser.add_argument('--headless', action='store_true', default=False)
	parser.add_argument('-v', '--verbose', action='store_true', default=False)
	parser.add_argument('-p', '--part')
	parser.add_argument('-d', '--delay', type=float, default=0)
	parser.add_argument('--confirm-move', action='store_true', default=False)
	parser.add_argument('--confirm-turn', action='store_true', default=False)
	global CMDLINE 
	CMDLINE = parser.parse_args()

	context.log_level = 'debug' if CMDLINE.verbose else 'info'

def get_input():

	lines = []

	filename = "./input" if not CMDLINE.testing else "./input-test-{}".format(CMDLINE.testing)
	with open(filename, "r") as infile:
		lines = infile.readlines()

	return Field(filename, lines, headless=CMDLINE.headless)

def do_part(part):
    if not CMDLINE.part or CMDLINE.part == part:
        return True
    else:
        return False


########################################################################
#
# Classes / global functions

def play_game(field):

	field.render()
	if CMDLINE.confirm_turn or CMDLINE.confirm_move:
		a = raw_input("hit enter to continue; q to quit: ")
		if a.rstrip() == 'q':
			return

	turn = 0
	with log.progress("turn") as tp:

		while 1:
		
			tp.status("start of turn: %d", turn + 1)
			p = field.next_player(turn)
			if p == None:
				tp.status("end of turn: %d", turn + 1)
				turn += 1

				if CMDLINE.confirm_turn and confirm_step(field, turn, None) == False:
					return	
				continue

			log.debug("%s starting turn", p)
			p.start_turn()
			field.current = p
			field.render()

			if CMDLINE.confirm_move and confirm_step(field, turn, p) == False:
				return

			# determine the next move. the get_move functions won't
			# return a move if the player is in range of someone
			# he can fight
			#if turn == 16 and p.name == 'G-4':
				#context.log_level = 'debug'
			move = field.get_move(p)
			if move:
				field.move(p, move)
				field.render()
				sleep(CMDLINE.delay)

			# find any targets we can fight
			t = field.select_target(p)
			if t:
				#log.info("%s attacks %s after moving", p, t)
				t.hp -= p.ap

			# drag the bodies off the field
			if field.harvest_the_dead(turn):

				#if this was the last player in the round then the turn has
				# finished and we should increment the turn count for the
				# final score tally
				if field.next_player(turn) == None:
					log.debug("last player died at the end of the round")
					turn += 1

				field.render()
				team = set([ p.t for p in field.players.values() ]).pop()
				total_hp = sum([ p.hp for p in field.players.values() ])
				return (team, turn, total_hp)

			p.end_turn()
			field.current = None
			log.debug("%s ending turn", p)
			log.debug("--------------")
			log.debug("")
			field.render()
			time.sleep(CMDLINE.delay)
	

	return (None, None, None)

old_level = 'info'
confirm_prompt = None

def confirm_step(field, turn, player):

	global old_level
	global confirm_prompt

	if confirm_prompt == None:
		confirm_prompt = log.progress("")
	#if turn in [ 0, 1, 2, 23, 24, 25, 26, 27, 28, 47, 48 ]:
	#if turn not in range(15, 30):
	#if turn not in [ 20, 25, 30, 35, 40, 45 ]:
		#return

	#CMDLINE.headless = False
	#field.headless = False

	confirm_prompt.status("hit enter to continue; q to quit; d to enable debugging: ")
	a = sys.stdin.read(1)
	if a.rstrip() == 'q':
		return False
	elif a.rstrip() == 'd':
		old_level = context.log_level
		context.log_level = 'debug'
	confirm_prompt.status("")
	
	return True

def check_results(game, team, turn, total_hp, ap):

	log.info("the battle is over")

	winning = True
	if CMDLINE.testing:
		log.info("winners:           : %s (expected: %s)", team, game[1])
		log.info("last completed turn: %d (expected: %d)", turn, game[2])
		log.info("victors' total HP  : %d (expected: %d)", total_hp, game[3])
		log.info("victors' AP        : %d (expected: %d)", ap, game[4])
		winning = (team == game[1] and turn == game[2] and total_hp == game[3] and ap == game[4])
	else:
		log.info("winners:           : %s", team)
		log.info("last completed turn: %d", turn)
		log.info("victors' total HP  : %d", total_hp)
		log.info("victors' AP        : %d", ap)

	if winning:
		log.success(turn * total_hp)
	else:
		log.failure("didn't get what i wanted for christmas")

########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day 15 part A")

	if CMDLINE.testing:
		games = [ 
			( 1, 'G', 47, 590 ),
			( 2, 'E', 37, 982 ),
			( 3, 'E', 46, 859 ),
			( 4, 'G', 35, 793 ),
			( 5, 'G', 54, 536 ),
			( 6, 'G', 20, 937 ),
		]
	else:
		games = [( None, None, None, None)]

	for g in games:
	
		if g[0]:
			CMDLINE.testing = g[0]
		else:
			log.info("this is not a drill...")

		field = get_input()
		team, turn, total_hp = play_game(field)

		log.info("the battle is over")
		winning = True
		if CMDLINE.testing:
			log.info("winners:           : %s (expected: %s)", team, g[1])
			log.info("last completed turn: %d (expected: %d)", turn, g[2])
			log.info("victors' total HP  : %d (expected: %d)", total_hp, g[3])
			winning = (team == g[1] and turn == g[2] and total_hp == g[3])
		else:
			log.info("winners:           : %s", team)
			log.info("last completed turn: %d", turn)
			log.info("victors' total HP  : %d", total_hp)

		if winning:
			log.success(turn * total_hp)
		else:
			log.failure("didn't get what i wanted for christmas")


########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day 15 part B")

	if CMDLINE.testing:
		games = [ 
			( 1, 'E', 29, 172, 15 ),
			#( 2, 'E', 33, 948, 4 ),
			( 3, 'E', 33, 948, 4 ),
			( 4, 'E', 37, 94, 15 ),
			( 5, 'E', 39, 166, 12 ),
			( 6, 'E', 30, 38, 34 ),
		]
	else:
		games = [( None, None, None, None)]

	CMDLINE.headless = True
	for g in games:
	
		if g[0]:
			CMDLINE.testing = g[0]

		elf_ap = 32
		incr = 32
		high = None
		low = None
		scores = {}

		searching = True
		while searching:

			field = get_input()
			field.set_ap('E', elf_ap)

			before = sum([ 1 for p in field.players.values() if p.t == 'E' ])
			team, turn, total_hp = play_game(field)
			after = sum([ 1 for p in field.players.values() if p.t == 'E' ])
			scores[elf_ap] = (team, turn, total_hp, elf_ap)
	
			log.info("ap: %d (incr: %d), before: %d, after: %d", elf_ap, incr, before, after)

			if after == before:
				log.info("Elves win with no damages for AP=%d", elf_ap)
				if incr == 1:
					break
				high = elf_ap
				incr /= 2
				elf_ap -= incr
			else:
				log.info("Elves sustain damages for AP=%d", elf_ap)
				if high == None:
					elf_ap += incr
				elif incr == 1:
					elf_ap += 1
					break
				else:
					low = elf_ap
					incr /= 2
					elf_ap += incr

		s = scores[elf_ap]
		check_results(g, s[0], s[1], s[2], s[3])


########################################################################
#
# Testing

	
if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()
	
	if do_part('b'):
		do_partB()

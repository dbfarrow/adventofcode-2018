#!/usr/bin/env python

import math
import argparse
from pwn import *

########################################################################
#
# boilerplate script setup
#
# command line arguments
CMDLINE = None 

def parse_cmdline():
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 9")
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
		for linenum, line in enumerate(infile):
			if line[0] == "#":
				continue
			m = re.match("(\d+) players; last marble is worth (\d+) points", line)
			if m:
				spec = {}
				spec["num_players"] = int(m.group(1))
				spec["num_marbles"] = int(m.group(2))

				m = re.match(".*: high score is (\d+)", line)
				if m:
					spec["high_score"] = int(m.group(1))

				lines.append(spec)

	return lines

def do_part(part):
    if not CMDLINE.part or CMDLINE.part == part:
        return True
    else:
        return False

########################################################################
#
# Classes

class Game:

	def __init__(self, num_players, num_marbles):

		self.players = [ 0 for i in range(num_players) ]
		self.board = [ 0 ]
		self.num_marbles = num_marbles
		self.current_marble = 0
		self.current_pos = 0

	def add_marble(self, marble):

		score = 0
		
		# add the marble to the board
		if marble % 23 != 0:
			if len(self.board) == 1:
				self.board.append(marble)
				self.current_marble = marble
				self.current_pos = 1
				return 0
			else:
				self.current_marble = marble
				new_pos = ((self.current_pos + 2) % len(self.board))
				log.debug("playing marble: {}".format(marble))
				log.debug("current pos   : {}".format(self.current_pos))
				log.debug("new pos	     : {}".format(new_pos))
				if new_pos == 0:
					self.board.append(marble)
					self.current_pos = len(self.board) - 1
				else:
					self.board.insert(new_pos, marble)
					self.current_pos = new_pos
				log.debug("marble at pos : {}".format(self.board[self.current_pos]))

		else:
			# compute the score
			score += marble
	
			# now walk the list to the left (counter-clockwise) seven
			# places. Since this can only happen when there are least
			# 23 marbles on the board, we don't need to worry about
			# wrapping more than once
			pos = self.current_pos
			if pos < 7:
				pos += len(self.board)
			pos -= 7
			log.debug("scoring: removing marble at board[{}]: {}".format(pos, self.board[pos]))

			score += self.board[pos]
			self.current_pos = pos if pos > 0 else len(self.board)
			del self.board[pos]

			log.debug("scoring: new current pos: {}".format(self.current_pos))
			log.debug("marble {} is worth {}".format(marble, score))

		return score

	def add_score(self, player, score):
		self.players[player] += score

	def log_board(self):
	
		w = int(math.log(len(self.players), 10))
		player_fmt = "[{:" + str(w) + "d}]  "

		w = int(math.log(self.num_marbles, 10)) + 1
		marble_fmt = "{:" + str(w) + "d}"

		msg = "[{}]  ".format(self.current_marble % len(self.players))
		for i in range(len(self.board)):
			
			msg += "(" if i == self.current_pos else " "
			#msg += marble_fmt.format(self.board[i])
			msg += str(self.board[i])
			msg += ")" if i == self.current_pos else " "
		
		log.debug(msg)
		
########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day 9 part A")

	game_specs = get_input()

	for spec in game_specs:

		log.info("Playing game with [{} players], [{} marbles]".format(spec["num_players"], spec["num_marbles"]))
		if "high_score" in spec:
			log.info("   expecting score = {}".format(spec["high_score"]))

		num_marbles = spec['num_marbles']
		num_players = spec['num_players']

		g = Game(num_players, num_marbles)
		g.log_board()

		with log.progress('playing marbles:') as p:
			for i in range(1, num_marbles + 1):
				g.add_score(i % num_players, g.add_marble(i))
				g.log_board()
				p.status(str(i))

		# the winner is the one with the highest score
		#
		# the real game input run for a long time. Don't 
		# bother running it again. the answer is:
		#  434674
		#
		winner = max(g.players)
		if 'high_score' in spec:
			hs = spec['high_score']
			if winner == hs:
				log.success(winner)
			else:
				log.failure("expected {}; got {}".format(hs, winner))
		else:
			log.success(winner)
	

########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day 9 part B")

	num_players = 404
	num_marbles = 71952
	g = Game(num_players, num_marbles)
	with log.progress('playing marbles:') as p:
		for i in range(1, num_marbles + 1):
			g.add_score(i % num_players, g.add_marble(i))
			g.log_board()
			p.status(str(i))

	winner = max(g.players)
	log.success(winner)


if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

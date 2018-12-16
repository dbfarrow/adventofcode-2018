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
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 14")
	parser.add_argument('-t', '--testing', action='store_true', default=False)
	parser.add_argument('-v', '--verbose', action='store_true', default=False)
	parser.add_argument('-p', '--part')
	global CMDLINE 
	CMDLINE = parser.parse_args()

	context.log_level = 'debug' if CMDLINE.verbose else 'info'

def get_input(part):

	lines = []

	filename = "./input" if not CMDLINE.testing else "./input-test-{}".format(part)
	with open(filename, "r") as infile:
		lines = infile.readlines()

	problems = []
	for l in lines:
		if l[0] == '#':
			continue

		problem = {}
		[ a, b ] = l.rstrip().split(':')
		if part == 'a':
			problem['num_recipes'] = int(a)
			problem['answer'] = int(b)
		else:
			problem['pattern'] = a
			problem['answer'] = int(b)
			
		problems.append(problem)

	return problems

def do_part(part):
    if not CMDLINE.part or CMDLINE.part == part:
        return True
    else:
        return False

########################################################################
#
# Classes / global methods

def make_new_recipe(elves, scores):
	
	# get the score of each elf's current recipe
	recipes = []
	for i, e in enumerate(elves):
		if e >= len(scores):
			raise Exception("wtf? e = {}\n scores={}".format(elves, scores))
		recipes.append(scores[elves[i]])

	# calculate the sum of the scores and append
	# each digit to the recipe list	
	new_recipe = str(sum(recipes))
	log.debug("elves      : {}".format(elves))
	log.debug("new recipes: {}".format(new_recipe))
	for d in new_recipe:
		scores.append(int(d))

	# now move the elves
	num_recipes = len(scores)
	for i, e in enumerate(elves):
		start = elves[i]
		score = scores[start]
		spaces = scores[start] + 1
		end = start + spaces
		if end >= len(scores):
			end %= len(scores)
		log.debug("e[{}]={} starts at {}, moves {} spaces, and ends at {}".format(i, score, start, spaces, end))
		elves[i] = end

def print_step(elves, scores, stepnum):

	if len(scores) > 40:
		return

	log.debug(elves)
	m = "{:2d}:".format(stepnum)
	for i, s in enumerate(scores):
		
		if i == elves[0]:
			m += "("
		elif i == elves[1]:
			m += "["
		else:
			m += " "

		m += str(s)

		if i == elves[0]:
			m += ")"
		elif i == elves[1]:
			m += "]"
		else:
			m += " "

	log.info(m)

########################################################################
#
# PART A

def do_partA():

	log.info("AdventOfCode 2018 - day 14 part A")

	problems = get_input('a')
	
	for p in problems:
		step = 0
		with log.progress("step: ") as lp:
			log.info("num_recipes = {}".format(p['num_recipes']))
			
			# this part of the challenge starts with two elves with
			# recipes scores of 3 and 7 respectively
			elves = [ 0, 1]
			scores = [ 3, 7 ]
			print_step(elves, scores, step)

			# make the specified number of recipes
			for i in range(p['num_recipes']):
				make_new_recipe(elves, scores)
				step += 1
				print_step(elves, scores, step)
				if step % 100 == 0:
					lp.status(str(step))
	
			# now we need to print the next 10 recipe scores. However,
			# there may not be enough scores yet so we may need to make
			# some more
			pos = p['num_recipes'] - 1
			while len(scores) - pos <= 10:
				make_new_recipe(elves, scores)
				step += 1
				print_step(elves, scores, step)

			answer = "".join([ str(scores[i]) for i in range(pos+1, pos+11) ])
			if p['answer'] > 0:
				if int(answer) == int(p['answer']):
					log.success("passed: {}".format(answer))
				else:
					log.failure("failed: got     : {}".format(answer))
					log.failure("failed: expected: {}".format(p['answer']))
			else:
				log.success(answer)

########################################################################
#
# PART B

def do_partB():

	log.info("AdventOfCode 2018 - day 14 part B")

	problems = get_input('b')
	
	for p in problems:
		step = 0
		stats = [ 0 for i in range(10) ]

		with log.progress("step: ") as lp:
			
			# this part of the challenge starts with two elves with
			# recipes scores of 3 and 7 respectively
			elves = [ 0, 1]
			scores = [ 3, 7 ]
			pattern = p['pattern']
			pattern_len = len(str(pattern))
			answer = int(p['answer'])
			seq_num = 0

			log.info("looking for {} character pattern: [{}]".format(pattern_len, pattern))

			found = False
			while found == False:

				make_new_recipe(elves, scores)
				#print_step(elves, scores, step)

				if len(scores) < pattern_len:
					continue

				while (found == False) and (seq_num < len(scores) - pattern_len):

					seq = "".join([ str(scores[seq_num + i]) for i in range(0, pattern_len) ])
					seq_num += 1
					#log.info(seq)

					if pattern == seq:
						seq_num -= 1
						if answer > 0:
							if answer == seq_num:
								log.success(seq_num)
								found = True
							else:
								log.failure("expected: {}".format(answer))
								log.failure("got     : {}".format(seq_num))
						else:
							log.success(seq_num)
							found = True
						break
					
					stats[scores[seq_num] % 10] += 1

					if seq_num % 10000 == 0:
						pcts = map(lambda x: "{:02d}".format((x * 100) / seq_num), stats)
						lp.status(str("{}: current pattern: {}; {}".format(seq_num, seq, pcts)))

				step += 1



if __name__ == "__main__":

	parse_cmdline()

	if do_part('a'):
		do_partA()

	if do_part('b'):
		do_partB()

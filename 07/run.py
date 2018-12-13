#!/usr/bin/env python

import re
import time
import argparse
from pwn import *

# command line arguments
CMDLINE = None 

def parse_cmdline():
	
	parser = argparse.ArgumentParser(description="AdventOfCode 2018 - day 7")
	parser.add_argument('-t', '--testing', action='store_true', default=False)
	parser.add_argument('-v', '--verbose', action='store_true', default=False)
	parser.add_argument('-p', '--part')
	parser.add_argument('-b', '--base_duration', type=int, default=60)
	parser.add_argument('-w', '--workers', type=int, default=5)
	global CMDLINE 
	CMDLINE = parser.parse_args()

	context.log_level = 'debug' if CMDLINE.verbose else 'info'

class Task:

	def __init__(self, name):
		self.name = name
		self.nexts = []
		self.prereqs = []
		self.complete = False

		self.duration = CMDLINE.base_duration + (ord(self.name) - ord('A') + 1)
		self.worker = None


	def add_prereq(self, prereq):
	
		self.prereqs.append(prereq)
		prereq.nexts.append(self)

	def prereqs_complete(self):
	
		if len(self.prereqs) == 0:
			return True
		else:
			for p in self.prereqs:
				if p.complete == False:
					return False
		
		return True
	
class Worker:

	def __init__(self, num):
		self.name = "Worker {}".format(num)
		self.task = None
		self.start_time = -1

def load_tasks():

	tasks = {}

	filename = "./input" if not CMDLINE.testing else "./input-test"
	with open(filename, "r") as infile:
		for linenum, line in enumerate(infile):
			m = re.match("Step (.*) must be finished before step (.*) can begin.", line)
			if m:
				step_name = m.group(2)
				prereq_name = m.group(1)
				
				if step_name not in tasks:
					tasks[step_name] = Task(step_name)
				step = tasks[step_name]

				if prereq_name not in tasks:
					tasks[prereq_name] = Task(prereq_name)
				prereq = tasks[prereq_name]

				step.add_prereq(prereq)

			else:
				raise Exception("malformed input line {}: {}".format(linenum, line))
	
	return tasks

def find_starting_candidates(tasks):

	candidates = {}
	for n, t in tasks.items():
		if t.prereqs_complete() and t.complete == False:
			candidates[n] = t
	return candidates


def do_partA(tasks):

	order = ""

	# find candidates to execute. to be a candidate, all prereqs must be complete
	# and the task must not already be complete
	candidates = find_starting_candidates(tasks)
	while 1:
		
		# we're done when there are no candidate tasks left to do
		if len(candidates) == 0:
			break

		# the next task up is the candidate with the lowest alphabetical name
		log.debug("candidates for next step: {}".format([n for n in candidates.keys() ]))
		t = candidates[sorted(candidates.keys())[0]]

		# to do the task:
		#	1. mark the task as complete
		#	2. add the task name to the instruction order string
		#	3. add the completed task's next steps to the candidate list
		#	4. remove the completed task from the candidate list
		log.debug("completing task: {}".format(t.name))
		t.complete = True
		order += t.name
		for n in t.nexts:
			if n.prereqs_complete():
				candidates[n.name] = n
		del candidates[t.name]
		#time.sleep(1)

	log.info("AdventOfCode 2018: 7A")
	log.success(order)

def do_partB(tasks):

	partB = None
	log.info("AdventOfCode 2018: 7B")

	# create the workers
	workers = allocate_workers(CMDLINE.workers)
	log.debug("free_workers: {}".format([ n for n in free_workers.keys() ]))
	log.debug("busy_workers: {}".format([ n for n in busy_workers.keys() ]))

	# log the task durations
	for n, t in tasks.items():
		log.debug("{}.duration = {}".format(n, t.duration))

	tick = 0
	order = ""
	candidates = find_starting_candidates(tasks)
	log.info("starting candidates: {}".format([ n for n, t in candidates.items() ]))

	# print the header of the debug table
	debug_schedule(tick, workers, order)

	with log.progress("schedule") as p:
		while 1:
		
			# for each candidate task to work on, find an idle worker
			# to assign it to
			for n, t in candidates.items():
				if t.worker == None:
					w = get_available_worker(workers)
					if w:
						log.debug("assigning {} to {}".format(t.name, w.name))
						w.task = t
						t.worker = w
						w.start_time = tick
						order += t.name
					else:
						break
			
			# We are done when there are no more candidates
			if len(candidates) == 0:
				break
	
			log.debug("free_workers: {}".format([ n for n in free_workers.keys() ]))
			log.debug("busy_workers: {}".format([ n for n in busy_workers.keys() ]))
	
			debug_schedule(tick, workers, order, p)
	
			# check to see if any tasks are complete
			# For completed tasks:
			#	1. mark the task complete
			#	2. remove the task from the list of candidate steps
			#	3. add the task's next steps to the list of candidate steps
			#	4. clear the worker's assigned task
			#	5. return the worker to the work pool
			for n, w in busy_workers.items():
				w = busy_workers[n]
				log.debug("worker: {}".format(w.name))
				if w.task:
					if (tick - w.start_time + 1) >= w.task.duration:
						log.debug("task {} completed".format(w.task.name))
	
						# 1
						w.task.complete = True
	
						# 2
						log.debug("removing {} from candidate list".format(w.task.name))
						del candidates[w.task.name]
						log.debug("  --> candidates: {}".format([ c for c in candidates.keys() ]))
	
						#3
						for nt in w.task.nexts:
							log.debug("adding {} to candidate list from {} task next list".format(nt.name, w.task.name))
							if nt.prereqs_complete() and not nt.complete:
								log.debug("adding {} to candidates".format(nt.name))
								candidates[nt.name] = nt
								log.debug("  --> candidates: {}".format([ c for c in candidates.keys() ]))
							else:
								log.debug("can't add {} because prereqs={} or complete={}".format(nt.name, nt.prereqs_complete(), nt.complete))
								log.debug("  {}".format([pn.name for pn in nt.prereqs]))
	
						# 4
						free_workers[w.name] = w		
	
						# 5 
						del busy_workers[w.name]
						w.task = None
	
					else:
						log.debug("{} has {} seconds left on {}".format(w.name, w.task.duration - (tick - w.start_time), w.task.name))
			
			# ok... this is gratuitous. but if I don't slow things down here you
			# won't see the awesome progress message i cooked up for y'all. so
			# chill and watch the work you aren't having to do yourself.
			time.sleep(0.01)
			tick += 1
	
	log.success(tick)


free_workers = {}
busy_workers = {}

def allocate_workers(count):

	global free_workers
	free_workers = {}
	
	for i in range(CMDLINE.workers):
		w = Worker(i+1)
		free_workers[w.name] = w

def get_available_worker(workers):

	if len(free_workers) == 0:
		return None
	else:
		w = free_workers[sorted(free_workers.keys())[0]]
		del free_workers[w.name]
		busy_workers[w.name] = w
		return w

def debug_schedule(tick, workers, order, p=None):

	msg = ""
	if not p:
		msg += "Second  "
		for i in range(CMDLINE.workers):
			name = "Worker {}".format(i+1)
			msg += name + "  "
		msg += " Done"
		log.info(msg)
	else:
		msg += "{:4d}     ".format(tick)
		for i in range(CMDLINE.workers):
			name = "Worker {}".format(i+1)
			t = "."
			if name in busy_workers:
				t = busy_workers[name].task.name

			msg += "  {:8s}".format(t)
		msg += "{}".format(order)
		p.status(msg)


if __name__ == "__main__":

	parse_cmdline()

	if CMDLINE.part == None or CMDLINE.part == 'a':
		tasks = load_tasks()
		do_partA(tasks)
	if CMDLINE.part == None or CMDLINE.part == 'b':
		tasks = load_tasks()
		do_partB(tasks)


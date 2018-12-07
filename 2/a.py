#!/usr/bin/env python
#
# See prompt-a.txt for problem statement
#

counts = {}

def process(line):
	_count = { c : line.count(c) for c in line }
	_freqs = { f : 1 for c, f in _count.items() }
	return _freqs

if __name__ == "__main__":

	twice = 0
	thrice = 0

	with open("input", "r") as infile:
		for cnt, line in enumerate(infile):
			freqs = process(line)
			twice += (1 if 2 in freqs else 0)
			thrice += (1 if 3 in freqs else 0)

	chksum = twice * thrice
	print(chksum)


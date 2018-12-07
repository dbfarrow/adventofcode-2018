#!/usr/bin/env python

passnum = 1
total = 0
freqs = {}
firstdup = -1

while (1):
	passnum += 1
	print("pass #{}".format(passnum))

	with open("input", "r") as infile:
		for cnt, line in enumerate(infile):	
			val = int(line)
			total = total + val
			#print("{}:{}".format(val, total))
			if total in freqs:
				if firstdup < 0:
					firstdup = total
					print("first dup: {}".format(firstdup))
					print("passnum  : {}".format(passnum))
					exit(-1)
			else:
				freqs[total] = 1
	

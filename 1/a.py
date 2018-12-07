#!/usr/bin/env python

total = 0

with open("input", "r") as infile:
	for cnt, line in enumerate(infile):	
		total = total + int(line)
print "final frequency: {}".format(total)	

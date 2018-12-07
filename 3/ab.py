#!/usr/bin/env python

LENGTH = 2000
WIDTH = 2000

fabric = [ [ 0 for i in xrange(WIDTH) ] for j in xrange(LENGTH) ]

def parse_line(line):

	# parse out the big pieces:
	#   elf_id @ pos: dims
	parts = line.split(' ')
	elf_id = parts[0]
	pos = parts[2]
	dims = parts[3]

	# parse the pos:
	#   <x>,<y>:
	pos = pos.replace(':', '')
	[x, y] = [ int(i) for i in pos.split(',')]


	# parse the dims:
	#   <w>x<l>
	[w, h] = [ int(i) for i in dims.split('x')]

	return [ x, y, w, h]

def map_line(line):
	
	[ x, y, w, h ] = parse_line(line)

	# now mark the pattern on the map
	for i in range(x, x+w):
		for j in range(y, y+h):
			fabric[j][i] = fabric[j][i] + 1
	

def count_overlaps():

	overlaps = 0
	for row in fabric:
		for cell in row:
			overlaps += (1 if cell > 1 else 0)

	return overlaps 

def is_freestanding(line):

	[ x, y, w, h ] = parse_line(line)
	for i in range(x, x+w):
		for j in range(y, y+h):
			if fabric[j][i] > 1:
				return False

	return True

if __name__ == "__main__":

	#lines = [ 
		#"#1 @ 1,3: 4x4",
		#"#2 @ 3,1: 4x4",
		#"#3 @ 5,5: 2x2",
	#]

	lines = []
	with open("input", "r") as infile:
		for line in infile.readlines():
			lines.append(line)

	for line in lines:
		map_line(line)

	#for row in fabric:
		#print row

	print("part A: {}: ".format(count_overlaps()))

	for line in lines:
		if is_freestanding(line):
			print("freestanding claims: {}: ".format(line))


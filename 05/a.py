#!/usr/bin/env python

testing = False

lower = [ chr(c) for c in range(ord('a'), ord('z')+1) ]
upper = [ chr(c) for c in range(ord('A'), ord('Z')+1) ]

def get_lines():

    filename = "./input" if not testing else "./input-test"
    with open(filename, "r") as infile:
        lines = infile.readlines()

    return lines

def compress(line):

	#print("starting    : {}".format(line))

	while True:
		l = len(line)
		for i in range(len(lower)):
			pat = lower[i] + upper[i]
			if pat in line:
				line = line.replace(pat, "", 1)
				#print("replacing {}: {}".format(pat, line))

			pat = upper[i] + lower[i]
			if pat in line:
				line = line.replace(pat, "", 1)
				#print("replacing {}: {}".format(pat, line))

		if len(line) == l:
			return line;

	return None



if __name__ == "__main__":

	lines = get_lines()
	line = lines[0].rstrip()
	line = compress(line)
	print("part A      : {}".format(len(line)))
	
	minlen = len(lines[0])
	minc = None
	for i in range(len(lower)):
		line = lines[0].rstrip()
		line = line.replace(lower[i], "")	
		line = line.replace(upper[i], "")	
		line = compress(line)
		#print("replacing '{}' reduced compressed string to {}".format(lower[i], len(line)))
		if len(line) < minlen:
			minlen = len(line)
			minc = lower[i]
			#print("'{}' results in new min length compression".format(lower[i]))

	print("part B: {}".format(minlen)) 

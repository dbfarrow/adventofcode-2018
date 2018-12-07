#!/usr/bin/env python
#
# See prompt-b.txt for problem statement
#

def differs_by_one(a, b):

	diffs = 0
	for i, c in enumerate(a):
		diffs += (1 if a[i] != b[i] else 0)
		
	return True if diffs == 1 else 0	

def get_answer(a, b):
	answer = ""
	for i, c in enumerate(a):
		answer += (a[i] if a[i] == b[i] else "")
		
	return answer
	

if __name__ == "__main__":

	# read the input into a list of lines without newlines
	lines = [line.rstrip('\n') for line in open('input')]

	# compare each line with all of the rest looking for 
	# lines that differ by only one character (in the same
	# position)
	for i, line in enumerate(lines):
		for j in range(i+1, len(lines)):
			if differs_by_one(lines[i], lines[j]):
				print(get_answer(lines[i], lines[j]))

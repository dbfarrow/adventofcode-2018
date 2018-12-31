#!/usr/bin/env python

# regs:		0 1 2 3 4 5 
# vars:		i j k l m n

i = 0
j = 0
k = 0
l = 0
m = 0
n = 0

# 00: seti 123 0 5
# 01: bani 5 456 5
# 02: eqri 5 72 5
# 03: addr 5 3 3
# 04: seti 0 0 3
# 05: seti 0 5 5
# 06: bori 5 65536 2
# 07: seti 10362650 3 5
# 08: bani 2 255 4
# 09: addr 5 4 5
# 10: bani 5 16777215 5
# 11: muli 5 65899 5
# 12: bani 5 16777215 5
# 13: gtir 256 2 4
# 14: addr 4 3 3
# 15: addi 3 1 3
# 16: seti 27 4 3
# 17: seti 0 3 4
# 18: addi 4 1 1
# 19: muli 1 256 1
# 20: gtrr 1 2 1
# 21: addr 1 3 3
# 22: addi 3 1 3
# 23: seti 25 2 3
# 24: addi 4 1 4
# 25: seti 17 7 3
# 26: setr 4 0 2
# 27: seti 7 8 3
# 28: eqrr 5 0 4
# 29: addr 4 3 3
# 30: seti 5 1 3


# 00-05
while 1:
	n =	123
	if (456 & n) != 72:
		continue
	else:
		n = 0

	# 06-12
	j = n | 0x1000			# 65536
	n = 0x9e1f1a			# 10362650	
	m = (j | 0xff)			# 255
	m = n + m
	m &= 0xffff				# 16777215
	m *= 65889
	m &= 0xffff
	
	# 13-17
	l = 1 if 256 > j else 0
	if l == 0:
		# goto 27
	else:
		l = 0

	# 18-25
	l += 1
	j *= 256
	i = 1 if j > k else 0
	if i == 0:
		# goto 25
	else:
		l += 1
		
	# 25-
	n = 17
	j = l
	
	# 27
	n = 7

	# 28
	l = 1 if m == 0 else 0
	n = l + k
	n = 5


#!/usr/bin/env python
#
#

import os
from pwn import *

def find_scripts():

	script_dirs = []

	for dirpath, dirnames, filenames in os.walk("."):
		if "run.py" in filenames:
			script_dirs.append(dirpath)

	return(sorted(script_dirs))

def do_script(script_dir, part):

	cmd = ["./run.py", "--part={}".format(part)]
	os.chdir(script_dir)
	log.info(cmd)

	with log.progress(script_dir) as p:
		pro = process(cmd, stdout=PIPE)
		while 1:
			try:
				result = pro.recv()

				if "[x]" in result:
				#if result[1] == 'x':
					p.status(result[4:])
				elif result[1] == '*':
					log.info(result[4:])
				elif result[1] == '-':
					log.failure(result[4:])
				elif result[1] == '+':
					log.success(result[4:])
				elif result[1] == 'D':
					log.debug(result[8:])
				else:	
					log.info(result[4:])
			except EOFError:
				pro.wait_for_close()
				break	

	os.chdir("..")
	return False

if __name__ == "__main__":

	#context.log_level = 'debug'

	scripts = find_scripts()
	for s in scripts:
		do_script(s, 'a')
		do_script(s, 'b')
		break
	

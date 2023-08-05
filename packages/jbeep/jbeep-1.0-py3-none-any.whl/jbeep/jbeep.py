import os
import time

def alert():
	return os.system('spd-say -t female3 "your code has finished"')

def start():
	global t0 
	t0 = time.time()
	return

def end():
	t1 = time.time()
	total = t1-t0
	return print("Your code took %f seconds" % total)

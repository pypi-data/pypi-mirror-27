import os
import time

def alert():
	os.system('spd-say -t female3 "your code has finished"')

def start():
	global t0 
	t0 = time.time()

def end():
	t1 = time.time()
	total = t1-t0
	print("Your code took %f seconds" % total)

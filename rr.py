from process import Process
from processor import Processor
from queue import Queue 

import parser

events_queue = parser.get_processes()
processor = Processor()
time_elapsed = 0 
iterations = 0

def new_processes():
	global time_elapsed
	while not events_queue.is_empty():
		print 'Time Elasped: ', time_elapsed
		while not events_queue.is_empty() and events_queue.front().arrival_time <= time_elapsed:
			processor.insert(events_queue.dequeue())
	 	if events_queue.is_empty():
			while not processor.is_idle():
				time_elapsed += processor.run_process()
				print 'Time Elapsed: ', time_elapsed
		else:
			while events_queue.front().arrival_time <= time_elapsed:
				time_elapsed += processor.run_process()
				print 'Time Elapsed: ', time_elapsed

new_processes()
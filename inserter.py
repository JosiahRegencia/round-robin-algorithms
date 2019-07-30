from process import Process
from processor import Processor
from queue import Queue 

import parser

events_queue = parser.get_processes()
processor = Processor()
time_elapsed = 0 
iterations = 0

def new_processes():
	while not events_queue.is_empty() and not processor.process_queue.is_empty():
	 	while events_queue.front().cpu_burts <= time_elapsed:
	 		processor.insert(events_queue.dequeue())
	 	time_elapsed += processor.run_process()

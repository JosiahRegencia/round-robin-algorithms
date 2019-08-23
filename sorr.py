"""

Smart Optimized Round Robin (SORR) CPU Scheduling Algorithm by Rahul Joshi and Shashi Bhushan Tyagi

"""

from heapq import heappush, heappop, heapify
from process import Process
from processor import Processor
from queue import Queue 

import parser

class SORR_Processor(Processor):
	def arrange(self):
		self.process_queue.queue = sorted(self.process_queue.queue, key=lambda process: process.cpu_burst)

	def STQ(self):
		mean = 0

		top_quantum = max(self.process_queue.queue, key=lambda item:item.cpu_burst).cpu_burst

		for process in self.process_queue.queue:
			mean += process.cpu_burst

		mean = mean / self.process_queue.size()
		stq = (mean + top_quantum) / 2
		print 'STQ: ', stq
		self.time_quantum = stq

	def run_process(self):
		process = self.process_queue.dequeue()
		print 'Enter\t',
		print 'Process ID: {}\t'.format(process.process_id),
		print 'Arrival Time: {}\t'.format(process.arrival_time),
		print 'Remaining Burst: {}\t'.format(process.cpu_burst)
		print '----------------------------------------------------------------------'
		if process.cpu_burst <= self.time_quantum:
			elapsed_time = process.cpu_burst
			process.cpu_burst = 0
			print 'Exit\t',
			print 'Process ID: {}\t'.format(process.process_id),
			print 'Arrival Time: {}\t'.format(process.arrival_time),
			print 'Remaining Burst: {}\t'.format(process.cpu_burst)
			print '----------------------------------------------------------------------'

			return elapsed_time
		else:
			process.cpu_burst -= self.time_quantum
			print 'Exit\t',
			print 'Process ID: {}\t'.format(process.process_id),
			print 'Arrival Time: {}\t'.format(process.arrival_time),
			print 'Remaining Burst: {}\t'.format(process.cpu_burst)
			print '----------------------------------------------------------------------'
			if process.cpu_burst <= self.time_quantum:
				self.process_queue.insert_top(process)
			else:
				self.process_queue.enqueue(process)

			return self.time_quantum


events_queue = parser.get_processes()
processor = SORR_Processor()
time_elapsed = 0 
iterations = 0

def new_processes():
	global time_elapsed, iterations
	while not events_queue.is_empty():
		iterations += 1
		print 'Time Elasped: ', time_elapsed
		while not events_queue.is_empty() and events_queue.front().arrival_time <= time_elapsed:
			processor.insert(events_queue.dequeue())
		if iterations == 1:
			time_quantum = processor.STQ()
	 	while not processor.is_idle():
	 		time_elapsed += processor.run_process()
	 		print 'Time Elasped: ', time_elapsed

new_processes()
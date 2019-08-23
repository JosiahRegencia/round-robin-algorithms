"""
	
Implementation of Triggered Dynamic Time Quantum Round Robin Scheduling
This is based from the paper of Dr. Patricia Abu entitled

"""

from heapq import heappush, heappop, heapify
from process import Process
from processor import Processor
from queue import Queue 

import parser
import operator

class TDTQRR_Processor(Processor):
	def __init__(self):
		self.BTQ = 0
		self.time_quantum = 0
		self.TDTQ = 0
		self.min_tq = 0
		self.process_queue = Queue()

	def STQ(self):
		mean = 0

		top_quantum = max(self.process_queue.queue, key=lambda item:item.cpu_burst).cpu_burst

		for process in self.process_queue.queue:
			mean += process.cpu_burst

		mean = mean / self.process_queue.size()
		stq = (mean + top_quantum) / 2
		
		self.time_quantum = stq
		self.TDTQ = 0
		self.min_tq = min(self.process_queue.queue, key=lambda item:item.cpu_burst).cpu_burst

	def arrange(self):
		self.process_queue.queue = sorted(self.process_queue.queue, key=lambda process: process.cpu_burst)

	def run_process(self):
		print 'Time quantum: ', self.time_quantum
		process = self.process_queue.dequeue()
		print 'Enter\t',
		print 'Process ID: {}\t'.format(process.process_id),
		print 'Arrival Time: {}\t'.format(process.arrival_time),
		print 'Remaining Burst: {}\t'.format(process.cpu_burst)
		print '----------------------------------------------------------------------'
		if process.cpu_burst <= self.time_quantum:
			print 'Time quantum: ', self.time_quantum
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
			elapsed_time = self.time_quantum
			print 'Time quantum: ', self.time_quantum
			print 'Exit\t',
			print 'Process ID: {}\t'.format(process.process_id),
			print 'Arrival Time: {}\t'.format(process.arrival_time),
			print 'Remaining Burst: {}\t'.format(process.cpu_burst)
			print '----------------------------------------------------------------------'

			if process.cpu_burst == self.time_quantum + 1:
				self.TDTQ = self.time_quantum + 1
			elif self.TDTQ == 0 or self.time_quantum == self.time_quantum:
				self.TDTQ = self.time_quantum - 1
			elif self.TDTQ < self.min_tq:
				self.TDTQ = self.min_tq
			else:
				self.TDTQ -= 1
			self.time_quantum = self.TDTQ

			return elapsed_time


events_queue = parser.get_processes()
processor = TDTQRR_Processor()
time_elapsed = 0 
iterations = 0

def new_processes():
	global time_elapsed, iterations
	while not events_queue.is_empty():
		iterations += 1
		print 'Time Elasped: ', time_elapsed
		while not events_queue.is_empty() and events_queue.front().arrival_time <= time_elapsed:
			processor.insert(events_queue.dequeue())
		processor.STQ()
		processor.arrange()
		if events_queue.is_empty():
			while not processor.is_idle():
				time_elapsed += processor.run_process()
				print 'Time Elapsed: ', time_elapsed
		else:
			while events_queue.front().arrival_time <= time_elapsed:
				time_elapsed += processor.run_process()
				print 'Time Elapsed: ', time_elapsed

new_processes()
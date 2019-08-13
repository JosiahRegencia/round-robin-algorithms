from queue import Queue 


class Processor():
	def __init__(self):
		self.time_quantum = 5
		self.process_queue = Queue()

	def insert(self, process):
		self.process_queue.enqueue(process)

	def is_idle(self):
		if self.process_queue.is_empty():
			return True
		return False

	def run_process(self):
		process = self.process_queue.dequeue()
		print 'Enter\t',
		print 'Process ID: {}\t'.format(process.process_id),
		print 'Arrival Time: {}\t'.format(process.arrival_time),
		print 'Remaining Burst: {}\t'.format(process.cpu_burst)
		print '----------------------------------------------------------------------'
		if process.cpu_burst <= self.time_quantum:
			process.cpu_burst = 0
			print 'Exit\t',
			print 'Process ID: {}\t'.format(process.process_id),
			print 'Arrival Time: {}\t'.format(process.arrival_time),
			print 'Remaining Burst: {}\t'.format(process.cpu_burst)
			print '----------------------------------------------------------------------'

			return process.cpu_burst
		else:
			process.cpu_burst -= self.time_quantum
			self.process_queue.enqueue(process)
			print 'Exit\t',
			print 'Process ID: {}\t'.format(process.process_id),
			print 'Arrival Time: {}\t'.format(process.arrival_time),
			print 'Remaining Burst: {}\t'.format(process.cpu_burst)
			print '----------------------------------------------------------------------'

			return self.time_quantum
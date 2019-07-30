from queue import Queue 


class Processor():
	def __init__(self):
		time_quantum = 5
		process_queue = Queue()

	def insert(self, process):
		process_queue.enqueue(process)

	def is_idle(self):
		if process_queue.is_empty():
			return True
		return False

	def run_process(self):
		process = process_queue.dequeue()
		if process.cpu_burst <= time_quantum:
			process.cpu_burst = 0
			return process.cpu_burst
		else:
			process.cpu_burst -= time_quantum
			process_queue.enqueue(process)
			return time_quantum
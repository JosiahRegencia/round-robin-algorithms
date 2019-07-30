from process import Process
from queue import Queue

def get_processes():
	external_queue = Queue()
	with open('Processes.csv') as file:
	process_data = [line.split() for line in file]
	
	for data in process_data:
		external_queue.enqueue(Process(data[0], data[1], data[2]))
	return external_queue
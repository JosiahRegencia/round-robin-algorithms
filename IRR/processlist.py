from operator import attrgetter


class ProcessList:
	def __init__(self):
		self.process_list = list()

	def is_empty(self):
		if len(self.process_list) == 0:
			return True
		return False

	def add_process(self, process):
		self.process_list.append(process)

	def del_process(self, process):
		self.process_list.remove(process)

	def get_min_process(self):
		shortest = min(self.process_list, key=attrgetter('cpu_burst'))
		self.del_process(shortest)
		return shortest

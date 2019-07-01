class Queue:
	def __init__(self):
		self.queue = list()

	def is_empty(self):
		if len(self.queue) == 0:
			return True
		return False

	def front(self):
		try:
			return self.queue[0]
		except IndexError as error:
			print 'Error: ', error
			print 'Queue is empty'

	def rear(self):
		try:
			return self.queue[len(self.queue) - 1]
		except IndexError as error:
			print 'Error: ', error
			print 'Queue is empty'

	def enqueue(self, item):
		self.queue.append(item)

	def dequeue(self):
		try:
			front = self.front()
			self.queue.remove(front)
			return front
		except ValueError as error:
			print 'Error: ', error
			print 'Queue is empty'

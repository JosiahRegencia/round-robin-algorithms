from process import Process
from queue import Queue 


pcb = Queue()
pcb.enqueue(Process(0, 0, 5))
pcb.enqueue(Process(1, 0, 12))
pcb.enqueue(Process(2, 0, 20))
pcb.enqueue(Process(3, 0, 26))
pcb.enqueue(Process(4, 0, 34))


for process in pcb.queue:
	print 'P{}\t->\tCPU Burst: {}'.format(process.index, process.cpu_burst)
	
print 'Start Scheduling Algorithm: \n\n'

def rr(pcb):
	time_quantum = 15
	
	while not pcb.is_empty():
		curr_proc = pcb.dequeue()
		if curr_proc.cpu_burst <= time_quantum:
			curr_proc.cpu_burst = 0
		else:
			curr_proc.cpu_burst -= time_quantum
			pcb.enqueue(curr_proc)
		print 'P{}\t->\tCPU Remaining Burst: {}'.format(curr_proc.index, curr_proc.cpu_burst)

def main():
	rr(pcb)


if __name__ == '__main__':
	main()
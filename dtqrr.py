"""
	
Implementation of Triggered Dynamic Time Quantum Round Robin Scheduling
This is based from the paper of Dr. Patricia Abu entitled

"""

from heapq import heappush, heappop, heapify
from process import Process
from processor import Processor
from queue import Queue

import parser


class TDTQRR_Processor(Processor):
    def __init__(self):
        self.time_quantum = 0
        self.TDTQ = 0
        self.process_queue = Queue()

    def insert(self, process):
        heappush(self.process_queue.queue, (process.cpu_burst, process))

    def STQ(self):
        mean = 0

        top_quantum = max(self.process_queue.queue,
                          key=lambda item: item[1])[0]

        for priority, process in self.process_queue.queue:
            mean += process.cpu_burst

        mean = mean / self.process_queue.size()
        stq = (mean + top_quantum) / 2
        return stq

    def set_time_quantum(self):
        self.time_quantum = self.STQ()

    def get_min_time_quantum(self):
        return min(self.process_queue.queue, key=lambda item: item[1])[0]

    def run_process(self):
        priority, process = heappop(self.process_queue.queue)
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
            if process.cpu_burst == self.time_quantum + 1:
                self.TDTQ = self.time_quantum + 1
            elif self.TDTQ == 0 or self.TDTQ == self.time_quantum:
                self.TDTQ = self.time_quantum - 1
            elif self.TDTQ < self.get_min_time_quantum():
                self.TDTQ = self.get_min_time_quantum()
            else:
                self.TDTQ -= 1

            self.time_quantum = self.TDTQ
            print 'Time quantum: ', self.time_quantum
            process.cpu_burst -= self.time_quantum

            heappush(self.process_queue.queue, (process.cpu_burst, process))
            print 'Exit\t',
            print 'Process ID: {}\t'.format(process.process_id),
            print 'Arrival Time: {}\t'.format(process.arrival_time),
            print 'Remaining Burst: {}\t'.format(process.cpu_burst)
            print '----------------------------------------------------------------------'

            return self.time_quantum


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
        if iterations == 1:
            processor.set_time_quantum()
        while not processor.is_idle():
            time_elapsed += processor.run_process()
            print 'Time Elasped: ', time_elapsed


new_processes()

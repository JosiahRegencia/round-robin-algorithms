"""
	
Goal unta ni hahahaha

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
        self.process_iteration = 0

    def STQ(self):
        mean = 0

        top_quantum = max(self.process_queue.queue,
                          key=lambda item: item.cpu_burst).cpu_burst

        for process in self.process_queue.queue:
            mean += process.cpu_burst

        mean = mean / self.process_queue.size()
        stq = (mean + top_quantum) / 2

        self.time_quantum = stq
        self.TDTQ = 0
        self.min_tq = min(self.process_queue.queue,
                          key=lambda item: item.cpu_burst).cpu_burst

    def run_process(self):
        print 'Time quantum: ', self.time_quantum
        process = self.process_queue.dequeue()
        self.print_results('Enter', process.process_id,
                           process.arrival_time, process.cpu_burst)
        if process.cpu_burst <= self.time_quantum:
            print 'Time quantum: ', self.time_quantum
            elapsed_time = process.cpu_burst
            process.cpu_burst = 0
            self.print_results('Exit', process.process_id,
                               process.arrival_time, process.cpu_burst)
            return elapsed_time, process
        else:
            process.cpu_burst -= self.time_quantum
            elapsed_time = self.time_quantum
            print 'Time quantum: ', self.time_quantum
            self.print_results('Exit', process.process_id,
                               process.arrival_time, process.cpu_burst)

            if process.cpu_burst == self.time_quantum + 1:
                self.TDTQ = self.time_quantum + 1
            elif self.TDTQ == 0 or self.time_quantum == self.time_quantum:
                self.TDTQ = self.time_quantum - 1
            elif self.TDTQ < self.min_tq:
                self.TDTQ = self.min_tq
            else:
                self.TDTQ -= 1
            self.time_quantum = self.TDTQ

            print 'Time quantum: ', self.time_quantum
            if process.cpu_burst <= self.time_quantum:
                elapsed_time += process.cpu_burst
                process.cpu_burst = 0
            else:
                process.cpu_burst -= self.time_quantum
                elapsed_time += self.time_quantum
                self.process_queue.enqueue(process)
            self.print_results('Exit', process.process_id,
                               process.arrival_time, process.cpu_burst)

            return elapsed_time, process


events_queue = parser.get_processes()
processor = TDTQRR_Processor()
finished_processes = list()
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
                exec_time, process = processor.run_process()
                time_elapsed += exec_time
                print 'Time Elapsed: ', time_elapsed
                check_process(process, time_elapsed)
        else:
            while events_queue.front().arrival_time <= time_elapsed:
                exec_time, process = processor.run_process()
                time_elapsed += exec_time
                print 'Time Elapsed: ', time_elapsed
                check_process(process, time_elapsed)
    for process in finished_processes:
        print 'Process ID:\t', process.process_id,
        print 'Arrival Time:\t', process.arrival_time,
        print 'CPU Burst:\t', process.cpu_burst,
        print 'Completion Time:\t', process.completion_time,
        print 'Turnaround Time:\t', process.turnaround_time,
        print 'Waiting Time:\t', process.waiting_time


def check_process(process, time_elapsed):
    if process.cpu_burst == 0:
        process.completion_time = time_elapsed
        process.set_time_values()
        finished_processes.append(process)


new_processes()

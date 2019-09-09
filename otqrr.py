"""

Optimized Time Quantum for Dynamic Round Robin Algorithm

"""

from heapq import heappush, heappop, heapify
from process import Process
from processor import Processor
from queue import Queue

import parser
import math


class OTQRR_Processor(Processor):
    def arrange(self):
        self.process_queue.queue = sorted(
            self.process_queue.queue, key=lambda process: process.cpu_burst)

    def STQ(self):
        mean = 0

        TQ = math.floor(math.sqrt(sum(
            process.cpu_burst**2 for process in self.process_queue.queue) / self.process_queue.size()) * 0.9)
        min_quantum = self.get_min_quantum()
        median = self.get_burst_median()

        self.time_quantum = TQ

    def run_process(self):
        process = self.process_queue.dequeue()
        print 'Time quantum: ', self.time_quantum
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
            print 'Time quantum: ', self.time_quantum
            self.print_results('Exit', process.process_id,
                               process.arrival_time, process.cpu_burst)
            if process.cpu_burst <= self.time_quantum:
                self.process_queue.insert_top(process)
            else:
                self.process_queue.enqueue(process)

            return self.time_quantum, process


events_queue = parser.get_processes()
processor = OTQRR_Processor()
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
    calculate_averages(finished_processes)


def check_process(process, time_elapsed):
    if process.cpu_burst == 0:
        process.completion_time = time_elapsed
        process.set_time_values()
        finished_processes.append(process)


def calculate_averages(processes):
    AWT = sum(process.waiting_time for process in processes) / len(processes)
    ATT = sum(process.turnaround_time for process in processes) / \
        len(processes)
    print 'Average Waiting Time:\t', AWT
    print 'Average Turnaround Time:\t', ATT


new_processes()

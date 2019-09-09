"""

Efficient Dynamic Round Robin Algorithm by Muhammad Umar Farooq, Aamna Shakoor, Abu Bakar Siddique

"""

from heapq import heappush, heappop, heapify
from process import Process
from processor import Processor
from queue import Queue

import parser


class SORR_Processor(Processor):
    def arrange(self):
        self.process_queue.queue = sorted(
            self.process_queue.queue, key=lambda process: process.cpu_burst)

    def STQ(self):
        mean = 0

        top_quantum = self.get_max_quantum()
        min_quantum = self.get_min_quantum()
        median = self.get_burst_median()

        self.time_quantum = 0.8 * top_quantum

    def run_process(self):
        process = self.process_queue.dequeue()
        print ('Time quantum: ', self.time_quantum)
        self.print_results('Enter', process.process_id,
                           process.arrival_time, process.cpu_burst)
        if process.cpu_burst <= self.time_quantum:
            print ('Time quantum: ', self.time_quantum)
            elapsed_time = process.cpu_burst
            process.cpu_burst = 0
            self.print_results('Exit', process.process_id,
                               process.arrival_time, process.cpu_burst)

            return elapsed_time, process
        else:
            process.cpu_burst -= self.time_quantum
            print ('Time quantum: ', self.time_quantum)
            self.print_results('Exit', process.process_id,
                               process.arrival_time, process.cpu_burst)
            if process.cpu_burst <= self.time_quantum:
                self.process_queue.insert_top(process)
            else:
                self.process_queue.enqueue(process)

            return self.time_quantum, process


events_queue = parser.get_processes()
processor = SORR_Processor()
finished_processes = list()
time_elapsed = 0
iterations = 0


def new_processes():
    global time_elapsed, iterations
    while not events_queue.is_empty():
        iterations += 1
        print ('Time Elasped: ', time_elapsed)
        while not events_queue.is_empty() and events_queue.front().arrival_time <= time_elapsed:
            processor.insert(events_queue.dequeue())
        processor.arrange()
        processor.STQ()
        if events_queue.is_empty():
            while not processor.is_idle():
                exec_time, process = processor.run_process()
                time_elapsed += exec_time
                print ('Time Elapsed: ', time_elapsed)
                check_process(process, time_elapsed)
        else:
            while time_elapsed <= events_queue.front().arrival_time:
                exec_time, process = processor.run_process()
                time_elapsed += exec_time
                print ('Time Elapsed: ', time_elapsed)
                check_process(process, time_elapsed)
    for process in finished_processes:
        print ('Process ID:', process.process_id, end="\t"),
        print ('Arrival Time:', process.arrival_time, end="\t"),
        print ('CPU Burst:', process.cpu_burst, end="\t"),
        print ('Completion Time:', process.completion_time, end="\t"),
        print ('Turnaround Time:', process.turnaround_time, end="\t"),
        print ('Waiting Time:', process.waiting_time)
    calculate_averages(finished_processes)


def check_process(process, time_elapsed):
    if process.cpu_burst == 0:
        process.completion_time = time_elapsed
        process.set_time_values()
        finished_processes.append(process)


def calculate_averages(processes):
    AWT = sum(float(process.waiting_time)
              for process in processes) / len(processes)
    ATT = sum(float(process.turnaround_time)
              for process in processes) / len(processes)
    print ('Average Waiting Time:', AWT, end="\t")
    print ('Average Turnaround Time:', ATT, end="\n")


new_processes()

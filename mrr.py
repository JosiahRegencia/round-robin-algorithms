# Josiah Eleazar Regencia
# Implementation of Modified Round Robin (MRR) Algorithm by Montek Singh and Rohit Agrawal

from heapq import heappush, heappop, heapify
from process import Process
from processor import Processor
from queue import Queue

import parser
import operator
import statistics


class MRR_Processor(Processor):
    def __init__(self):
        self.time_quantum = 0
        self.process_queue = Queue()
        self.flag = 0

    def calculateMedian(self, bursts):
        bursts = sorted(bursts)
        if len(bursts) < 1:
            return None
        elif len(bursts) % 2 == 0:
            return (bursts[(self.process_queue.size()-1)/2] + bursts[(self.process_queue.size()+1)/2]) / 2

    def findTimeQuantum(self):
        bursts = [proc.cpu_burst for proc in self.process_queue.queue]
        mean = sum(bursts) / len(bursts)
        median = self.calculateMedian(bursts)

        if mean > median:
            self.time_quantum = (mean * max(bursts)) ** 0.5
        else:
            self.time_quantum = (median * max(bursts)) ** 0.5


events_queue = parser.get_processes()
processor = MRR_Processor()
time_elapsed = 0
iterations = 0


def new_processes():
    global time_elapsed
    while not events_queue.is_empty():
        print 'Time Elasped: ', time_elapsed
        while not events_queue.is_empty() and events_queue.front().arrival_time <= time_elapsed:
            processor.insert(events_queue.dequeue())
        if events_queue.is_empty():
            while not processor.is_idle():
                time_elapsed += processor.run_process()
                print 'Time Elapsed: ', time_elapsed
        else:
            while events_queue.front().arrival_time <= time_elapsed:
                time_elapsed += processor.run_process()
                print 'Time Elapsed: ', time_elapsed


new_processes()

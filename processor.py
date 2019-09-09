from queue import Queue
from numpy import median


class Processor():
    def __init__(self):
        self.time_quantum = 5
        self.process_queue = Queue()

    def insert(self, process):
        self.process_queue.enqueue(process)

    def is_idle(self):
        if self.process_queue.is_empty():
            return True
        return False

    def arrange(self):
        self.process_queue.queue = sorted(
            self.process_queue.queue, key=lambda process: process.cpu_burst)

    def get_max_quantum(self):
        return max(self.process_queue.queue, key=lambda item: item.cpu_burst).cpu_burst

    def get_min_quantum(self):
        return min(self.process_queue.queue, key=lambda item: item.cpu_burst).cpu_burst

    def get_burst_median(self):
        return median([process.cpu_burst for process in self.process_queue.queue])

    def print_results(self, state, process_id, arrival_time, cpu_burst):
        print ('{}\t'.format(state)),
        print ('Process ID: {}\t'.format(process_id)),
        print ('Arrival Time: {}\t'.format(arrival_time)),
        print ('Remaining Burst: {}\t'.format(cpu_burst))
        print ('----------------------------------------------------------------------')

    def run_process(self):
        process = self.process_queue.dequeue()
        self.print_results('Enter', process.process_id,
                           process.arrival_time, process.cpu_burst)
        if process.cpu_burst <= self.time_quantum:
            elapsed_time = process.cpu_burst
            process.cpu_burst = 0
            self.print_results('Exit', process.process_id,
                               process.arrival_time, process.cpu_burst)
            return elapsed_time, process
        else:
            process.cpu_burst -= self.time_quantum
            self.process_queue.enqueue(process)
            self.print_results('Exit', process.process_id,
                               process.arrival_time, process.cpu_burst)

            return self.time_quantum, process

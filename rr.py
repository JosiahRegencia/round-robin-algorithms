from process import Process
from processor import Processor
from queue import Queue

import parser

events_queue = parser.get_processes()
processor = Processor()
finished_processes = list()
time_elapsed = 0
iterations = 0


def new_processes():
    global time_elapsed
    while not events_queue.is_empty():
        print ('Time Elasped: ', time_elapsed)
        while (not events_queue.is_empty()) and (events_queue.front().arrival_time <= time_elapsed):
            processor.insert(events_queue.dequeue())
        if events_queue.is_empty():
            while not processor.is_idle():
                exec_time, process = processor.run_process()
                time_elapsed += exec_time
                print ('Time Elapsed: ', time_elapsed)
                check_process(process, time_elapsed)
        else:
            while time_elapsed <= events_queue.front().arrival_time:
                print ('else while')
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

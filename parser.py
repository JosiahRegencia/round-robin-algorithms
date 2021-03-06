from process import Process
from queue import Queue


def get_processes():
    external_queue = Queue()
    with open('Processes.csv') as file:
        process_data = [line.split(',') for line in file]

    for data in process_data[1:]:
        external_queue.enqueue(
            Process(int(data[0]), int(data[1]), int(data[2])))
    return external_queue

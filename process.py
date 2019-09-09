class Process:
    def __init__(self, process_id, arrival_time, cpu_burst):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.cpu_burst = cpu_burst
        self.initial_burst = cpu_burst
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.AWT = 0
        self.ATT = 0

    def set_time_values(self):
        self.turnaround_time = self.completion_time - self.arrival_time
        self.waiting_time = self.turnaround_time - self.initial_burst

    def is_finished():
        if self.cpu_burst == 0:
            return True
        else:
            return False

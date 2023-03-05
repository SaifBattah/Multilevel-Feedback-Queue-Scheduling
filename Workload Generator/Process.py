class Process:
    def __init__(self, pid, arrival_time, cpu_bursts, io_bursts):
        self.pid = pid
        self.arrival_time = arrival_time
        self.cpu_bursts = cpu_bursts
        self.io_bursts = io_bursts
        self.total_burst_time = sum(cpu_bursts)
        self.waiting_time = 0
        self.current_cpu_burst_location = 0
        self.current_io_burst_location = -1
        self.queued1 = 0
        self.queued2 = 0
        self.queued3 = 0
        self.current_burst = 0
        self.queued4 = 0
        self.current_counter = 0 # counter to the 10 time quanta checker
        self.unblock_at = 0 # re-assign process to queue-time after IO finishes
        self.in_IO_Queue = 0 # flag if process has io in queue
        self.done = 0
        self.moveto2 = 0
        self.moveto3 = 0
        self.momveto4 = 0
        self.current_queue = 0
        # ------------------------
        self.current_tau = 0
        self.next_tau = 0
        self.preempt_count = 0
        self.estimated_time = 0
        # ------------------------
        self.Old_Time = 0
# Done By Saif Battah - 1170986 @ 12/2/2023
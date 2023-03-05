from Process import Process
# Done By Saif Battah - 1170986 @ 12/2/2023
def read_processes(file_path):
    processes = []
    with open(file_path, "r") as file:
        for line in file:
            values = [int(num) for num in line.split()]
            pid = values[0]
            arrival_time = values[1]
            cpu_bursts = values[2::2]
            io_bursts = values[3::2]
            process = Process(pid, arrival_time, cpu_bursts, io_bursts)
            processes.append(process)
            #processes = sorted(processes, key=lambda x: x.Arrival_Time)
    return processes

def print_processes(process):
    for process in processes:
        print("PID:", process.pid)
        #print("Arrival Time:", process.arrival_time)
        print("CPU_Bursts:", process.cpu_bursts)
        print("IO_Bursts:", process.io_bursts)
        #print("Preempt Count:", process.preempt_count)
        print("Total Burst Time:", process.total_burst_time)
        #print("Waiting Time:", process.waiting_time)
        print("---")

def multilevel_scheduling(processes, q1, q2, alpha):
    # Sort processes by their arrival time
    processes = sorted(processes, key=lambda x: x.arrival_time)
    Gant_Chart = "|"
    FinishedSequence = "|"
    FinishedCpuBursts = "|"

    # Calculations
    Cpu_Busy_Time = 0
    Total_Waiting_Time = 0
    #initialize all queues
    queue1 = []
    queue2 = []
    queue3 = []
    queue4 = []
    IOqueue = []

    #exit counter
    counter = 0

    #set timer to first arrival process
    current_time = 0

    # --------------------------First Assign To Queue#1--------------------------------------------
    #  Executed Only 1 time
    while len(queue1) <= 0:
        for process_FA in processes:
            if process_FA.arrival_time <= current_time:
                process_FA.Old_Time = process_FA.arrival_time
                queue1.append(process_FA)
                process_FA.queued1 = 1
        if len(queue1) <= 0:
            print("at Time = " + str(current_time) + " | Queue#1 has " + str(len(queue1)) + " Processes.")
            current_time += 1
    # -------------------------- End Of First Assign-----------------------------------------------
    print("at Time = " + str(current_time) + " | Queue#1 has " + str(len(queue1)) + " Processes.")
    # -------------------------- Assign to queue1--------------------------------------------------
    ProcessNo = len(processes)
    length = len(processes)
    while length > 0:
        while len(queue1) > 0:
            print("Time = "+str(current_time))
            print("Queue1 length = " + str(len(queue1)))
            Current_in_CPU = queue1.pop(0) # remove one process from the queue -> queue doesn't contain this process.
            print(str(Current_in_CPU.pid)+" | "+str(Current_in_CPU.current_cpu_burst_location))
            if Current_in_CPU.cpu_bursts[Current_in_CPU.current_cpu_burst_location] >= q1:
                Current_in_CPU.cpu_bursts[Current_in_CPU.current_cpu_burst_location] -= q1
                Cpu_Busy_Time += q1
                Total_Waiting_Time += current_time - Current_in_CPU.Old_Time
                current_time += q1
                Current_in_CPU.Old_Time = current_time
                Gant_Chart += " -> P" + str(Current_in_CPU.pid)
                # -------------------------------------------- UPDATE Queue#1 AND IO Queue ---------------------------------
                if len(IOqueue) > 0:
                    for i, element in enumerate(IOqueue):
                        if element.unblock_at <= current_time:
                            free = IOqueue.pop(i)
                            free.io_bursts[free.current_io_burst_location] = 0
                            free.current_counter = 0
                            free.current_cpu_burst_location += 1
                            free.unblock_at = 0
                            if free.current_queue == 1:
                                print("P" + str(free.pid) +" re-added to queue1 after IO")
                                queue1.append(free)
                            elif free.current_queue == 2:
                                print("P" + str(free.pid) + " re-added to queue2 after IO")
                                queue2.append(free)
                            elif free.current_queue == 3:
                                print("P" + str(free.pid) + " re-added to queue3 after IO")
                                queue3.append(free)
                            elif free.current_queue == 4:
                                print("P" + str(free.pid) + " re-added to queue4 after IO")
                                queue4.append(free)
                            else:
                                print("REVIEW YOUR IOQUEUE CODE")
                for process_SA in processes:
                    if process_SA.queued1 == 0 and process_SA.queued2 == 0 and process_SA.queued3 == 0 and process_SA.queued4 == 0:
                        if process_SA.arrival_time <= current_time:
                            process_SA.Old_Time = process_SA.arrival_time
                            queue1.append(process_SA)
                            process_SA.queued1 = 1
                # ------------------------------------------- END OF UPDATING PROCESS --------------------------------------

                # After Update Check
                if Current_in_CPU.cpu_bursts[Current_in_CPU.current_cpu_burst_location] != 0:
                    Current_in_CPU.current_counter += 1
                    if Current_in_CPU.current_counter > 9:
                        print("enter queue2 P"+str(Current_in_CPU.pid))
                        # Add to Queue2
                        Current_in_CPU.current_counter = 0 # reset counter to use it in queue#2
                        queue2.append(Current_in_CPU)
                        Current_in_CPU.queued2 = 1
                    else:
                        print("re enter queue1 P"+str(Current_in_CPU.pid))
                        # Re-Add to Queue#1
                        queue1.append(Current_in_CPU)
                else: # if Burst after execute q1 from it , its new value is 0
                    print("process burst = 0")
                    FinishedCpuBursts += " -> P" + str(Current_in_CPU.pid)
                    try:
                        if Current_in_CPU.cpu_bursts[Current_in_CPU.current_cpu_burst_location + 1]:  # check for next cpu burst if exist
                            print("there exist next cpu - so go io")
                            # go to IO queue
                            Current_in_CPU.current_io_burst_location += 1
                            Current_in_CPU.unblock_at = current_time + Current_in_CPU.io_bursts[Current_in_CPU.current_io_burst_location]
                            Current_in_CPU.current_queue = 1
                            IOqueue.append(Current_in_CPU)
                    except IndexError:
                        print("process is done")
                        Current_in_CPU.done = 1
                        length -= 1
                        FinishedSequence += " -> P" + str(Current_in_CPU.pid)
                        print("Process #" + str(Current_in_CPU.pid) + " is All Done!, at Time = " + str(current_time))
            else:
                Total_Waiting_Time += current_time - Current_in_CPU.Old_Time
                current_time += Current_in_CPU.cpu_bursts[Current_in_CPU.current_cpu_burst_location]
                Current_in_CPU.Old_Time = current_time
                Cpu_Busy_Time += Current_in_CPU.cpu_bursts[Current_in_CPU.current_cpu_burst_location]
                Gant_Chart += " -> P" + str(Current_in_CPU.pid)
                FinishedCpuBursts += " -> P" + str(Current_in_CPU.pid)
                # You may set the current burst to zero
                # -------------------------------------------- UPDATE Queue#1 AND IO Queue ---------------------------------
                if len(IOqueue) > 0:
                    for j, elemento in enumerate(IOqueue):
                        if elemento.unblock_at <= current_time:
                            freeo = IOqueue.pop(j)
                            freeo.io_bursts[freeo.current_io_burst_location] = 0
                            freeo.current_counter = 0
                            freeo.current_cpu_burst_location += 1
                            freeo.unblock_at = 0
                            if freeo.current_queue == 1:
                                print("P" + str(freeo.pid) + " re-added to queue1 after IO")
                                queue1.append(freeo)
                            elif freeo.current_queue == 2:
                                print("P" + str(freeo.pid) + " re-added to queue2 after IO")
                                queue2.append(freeo)
                            elif freeo.current_queue == 3:
                                print("P" + str(freeo.pid) + " re-added to queue3 after IO")
                                queue3.append(freeo)
                            elif freeo.current_queue == 4:
                                print("P" + str(freeo.pid) + " re-added to queue4 after IO")
                                queue4.append(freeo)
                            else:
                                print("REVIEW YOUR IOQUEUE CODE")
                for process_SA2 in processes:
                    if process_SA2.queued1 == 0 and process_SA2.queued2 == 0 and process_SA2.queued3 == 0 and process_SA2.queued4 == 0:
                        if process_SA2.arrival_time <= current_time:
                            process_SA2.Old_Time = process_SA2.arrival_time
                            queue1.append(process_SA2)
                            process_SA2.queued1 = 1
                # ------------------------------------------- END OF UPDATING PROCESS --------------------------------------

                try:
                    if Current_in_CPU.cpu_bursts[Current_in_CPU.current_cpu_burst_location + 1]:
                        # go to IO queue
                        Current_in_CPU.current_io_burst_location += 1
                        Current_in_CPU.unblock_at = current_time + Current_in_CPU.io_bursts[Current_in_CPU.current_io_burst_location]
                        #Current_in_CPU.in_IO_Queue = 1
                        Current_in_CPU.current_queue = 1
                        IOqueue.append(Current_in_CPU)
                except IndexError:
                    Current_in_CPU.done = 1
                    length -= 1
                    print("Process #" + str(Current_in_CPU.pid) + " is All Done!, at Time = " + str(current_time))
                    FinishedSequence += " -> P" + str(Current_in_CPU.pid)
    # -------------------------- End of queue1-----------------------------------------------------
        if len(queue1) <= 0:
            if len(queue2) > 0:
                print("-----------------------------------------Queue2-------------------------------------------")

                # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
                print("Time = " + str(current_time))
                print("Queue1 length = " + str(len(queue2)))
                Current_in_CPU = queue2.pop(0)  # remove one process from the queue -> queue doesn't contain this process.
                print(str(Current_in_CPU.pid) + " | " + str(Current_in_CPU.current_cpu_burst_location) +" /Q2")
                if Current_in_CPU.cpu_bursts[Current_in_CPU.current_cpu_burst_location] >= q2:
                    Current_in_CPU.cpu_bursts[Current_in_CPU.current_cpu_burst_location] -= q2
                    Total_Waiting_Time += current_time - Current_in_CPU.Old_Time
                    current_time += q2
                    Current_in_CPU.Old_Time = current_time
                    Cpu_Busy_Time += q2
                    Gant_Chart += " -> P" + str(Current_in_CPU.pid)
                    # -------------------------------------------- UPDATE Queue#1 AND IO Queue ---------------------------------
                    if len(IOqueue) > 0:
                        for ii, elementi in enumerate(IOqueue):
                            if elementi.unblock_at <= current_time:
                                freei = IOqueue.pop(ii)
                                freei.io_bursts[freei.current_io_burst_location] = 0
                                freei.current_counter = 0
                                freei.current_cpu_burst_location += 1
                                freei.unblock_at = 0
                                if freei.current_queue == 1:
                                    print("P" + str(freei.pid) + " re-added to queue1 after IO")
                                    queue1.append(freei)
                                elif freei.current_queue == 2:
                                    print("P" + str(freei.pid) + " re-added to queue2 after IO")
                                    queue2.append(freei)
                                elif freei.current_queue == 3:
                                    print("P" + str(freei.pid) + " re-added to queue3 after IO")
                                    queue3.append(freei)
                                elif freei.current_queue == 4:
                                    print("P" + str(freei.pid) + " re-added to queue4 after IO")
                                    queue4.append(freei)
                                else:
                                    print("REVIEW YOUR IOQUEUE CODE")
                    for process_SAA in processes:
                        if process_SAA.queued1 == 0 and process_SAA.queued2 == 0 and process_SAA.queued3 == 0 and process_SAA.queued4 == 0:
                            if process_SAA.arrival_time <= current_time:
                                process_SAA.Old_Time = process_SAA.arrival_time
                                queue1.append(process_SAA)
                                process_SAA.queued1 = 1
                    # ------------------------------------------- END OF UPDATING PROCESS --------------------------------------

                    # After Update Check
                    if Current_in_CPU.cpu_bursts[Current_in_CPU.current_cpu_burst_location] != 0:
                        Current_in_CPU.current_counter += 1
                        if Current_in_CPU.current_counter > 9:
                            print("enter queue3 P" + str(Current_in_CPU.pid))
                            # Add to Queue3
                            Current_in_CPU.current_counter = 0  # reset counter to use it in queue#2
                            queue3.append(Current_in_CPU)
                            Current_in_CPU.queued3 = 1
                        else:
                            print("re enter queue2 P" + str(Current_in_CPU.pid))
                            # Re-Add to Queue#2
                            queue2.append(Current_in_CPU)
                    else:  # if Burst after execute q1 from it , its new value is 0
                        print("process burst = 0")
                        FinishedCpuBursts += " -> P" + str(Current_in_CPU.pid)
                        try:
                            if Current_in_CPU.cpu_bursts[Current_in_CPU.current_cpu_burst_location + 1]:  # check for next cpu burst if exist
                                print("there exist next cpu - so go io")
                                # go to IO queue
                                Current_in_CPU.current_io_burst_location += 1
                                Current_in_CPU.unblock_at = current_time + Current_in_CPU.io_bursts[Current_in_CPU.current_io_burst_location]
                                Current_in_CPU.current_queue = 2
                                IOqueue.append(Current_in_CPU)
                        except IndexError:
                            print("process is done")
                            Current_in_CPU.done = 1
                            length -= 1
                            print("Process #" + str(Current_in_CPU.pid) + " is All Done! in Q2, at Time = "+str(current_time))
                            FinishedSequence += " -> P" + str(Current_in_CPU.pid)
                else:
                    Total_Waiting_Time += current_time - Current_in_CPU.Old_Time
                    current_time += Current_in_CPU.cpu_bursts[Current_in_CPU.current_cpu_burst_location]
                    Current_in_CPU.Old_Time = current_time
                    Cpu_Busy_Time += Current_in_CPU.cpu_bursts[Current_in_CPU.current_cpu_burst_location]
                    Gant_Chart += " -> P" + str(Current_in_CPU.pid)
                    FinishedCpuBursts += " -> P" + str(Current_in_CPU.pid)
                    # -------------------------------------------- UPDATE Queue#1 AND IO Queue ---------------------------------
                    if len(IOqueue) > 0:
                        for jj, elementoj in enumerate(IOqueue):
                            if elementoj.unblock_at <= current_time:
                                freeoj = IOqueue.pop(jj)
                                freeoj.io_bursts[freeoj.current_io_burst_location] = 0
                                freeoj.current_counter = 0
                                freeoj.current_cpu_burst_location += 1
                                freeoj.unblock_at = 0
                                if freeoj.current_queue == 1:
                                    print("P" + str(freeoj.pid) + " re-added to queue1 after IO")
                                    queue1.append(freeoj)
                                elif freeoj.current_queue == 2:
                                    print("P" + str(freeoj.pid) + " re-added to queue2 after IO")
                                    queue2.append(freeoj)
                                elif freeoj.current_queue == 3:
                                    print("P" + str(freeoj.pid) + " re-added to queue3 after IO")
                                    queue3.append(freeoj)
                                elif freeoj.current_queue == 4:
                                    print("P" + str(freeoj.pid) + " re-added to queue4 after IO")
                                    queue4.append(freeoj)
                                else:
                                    print("REVIEW YOUR IOQUEUE CODE")
                    for process_SAA2 in processes:
                        if process_SAA2.queued1 == 0 and process_SAA2.queued2 == 0 and process_SAA2.queued3 == 0 and process_SAA2.queued4 == 0:
                            if process_SAA2.arrival_time <= current_time:
                                process_SAA2.Old_Time = process_SAA2.arrival_time
                                queue1.append(process_SAA2)
                                process_SAA2.queued1 = 1
                    # ------------------------------------------- END OF UPDATING PROCESS --------------------------------------

                    try:
                        if Current_in_CPU.cpu_bursts[Current_in_CPU.current_cpu_burst_location + 1]:
                            # go to IO queue
                            Current_in_CPU.current_io_burst_location += 1
                            Current_in_CPU.unblock_at = current_time + Current_in_CPU.io_bursts[Current_in_CPU.current_io_burst_location]
                            # Current_in_CPU.in_IO_Queue = 1
                            Current_in_CPU.current_queue = 2
                            IOqueue.append(Current_in_CPU)
                    except IndexError:
                        Current_in_CPU.done = 1
                        length -= 1
                        print("Process #" + str(Current_in_CPU.pid) + " is All Done! in Q2, at Time = "+str(current_time))
                        FinishedSequence += " -> P" + str(Current_in_CPU.pid)
                # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
            elif len(queue2) <= 0:
                if len(queue3) > 0:
                    print("-----------------------------------------Queue3-------------------------------------------")
                    # calculate each process estimated time
                    for process_ET in queue3:
                        process_ET.estimated_time = (alpha * process_ET.cpu_bursts[process_ET.current_cpu_burst_location]) + ((1 - alpha) * process_ET.current_tau)
                        process_ET.next_tau = process_ET.estimated_time

                    # sort the Queue3 according to estimated time
                    queue3 = sorted(queue3, key=lambda x: x.estimated_time)

                    # pop the first/lowest estimated time from the queue
                    print("before pop ATTTTTTTTTTTT Queue3 length = " + str(len(queue3)))
                    for ks in queue3:
                        print(str(ks.pid))
                    Current_in_CPU = queue3.pop(0)
                    print("after pop ATTTTTTTTTTTT Queue3 length = " + str(len(queue3)))
                    # execute but using for loop -> timer +1
                    while Current_in_CPU.estimated_time > 0:
                        Current_in_CPU.estimated_time -= 1
                        current_time += 1
                        Cpu_Busy_Time += 1
                        flag = 0
                        # -------------------------------------------- UPDATE Queue#1 AND IO Queue ---------------------------------
                        if len(IOqueue) > 0:
                            for jx, elementox in enumerate(IOqueue):
                                if elementox.unblock_at <= current_time:
                                    freeox = IOqueue.pop(jx)
                                    freeox.io_bursts[freeox.current_io_burst_location] = 0
                                    freeox.current_counter = 0
                                    freeox.current_cpu_burst_location += 1
                                    freeox.unblock_at = 0
                                    if freeox.current_queue == 1:
                                        flag = 1
                                        print("P" + str(freeox.pid) + " re-added to queue1 after IO")
                                        queue1.append(freeox)
                                    elif freeox.current_queue == 2:
                                        flag = 1
                                        print("P" + str(freeox.pid) + " re-added to queue2 after IO")
                                        queue2.append(freeox)
                                    elif freeox.current_queue == 3:
                                        print("P" + str(freeox.pid) + " re-added to queue3 after IO")
                                        queue3.append(freeox)
                                        # if time_newly_added < time_current_running -> preemption
                                        if (alpha * freeox.cpu_bursts[freeox.current_cpu_burst_location]) + ((1 - alpha) * freeox.current_tau) < Current_in_CPU.estimated_time:
                                            flag = 1
                                    elif freeox.current_queue == 4:
                                        flag = 1
                                        print("P" + str(freeox.pid) + " re-added to queue4 after IO")
                                        queue4.append(freeox)
                                    else:
                                        print("REVIEW YOUR IOQUEUE CODE")
                        for process_SA23 in processes:
                            if process_SA23.queued1 == 0 and process_SA23.queued2 == 0 and process_SA23.queued3 == 0 and process_SA23.queued4 == 0:
                                if process_SA23.arrival_time <= current_time:
                                    flag = 1
                                    process_SA23.Old_Time = process_SA23.arrival_time
                                    queue1.append(process_SA23)
                                    process_SA23.queued1 = 1
                        # ------------------------------------------- END OF UPDATING PROCESS --------------------------------------
                        if flag == 1: # there's a preemption -> tau updated
                            Current_in_CPU.Old_Time = current_time
                            Gant_Chart += " -> P" + str(Current_in_CPU.pid)
                            print("Preemption Occured")
                            Current_in_CPU.preempt_count += 1
                            if Current_in_CPU.preempt_count == 3: # at the third preemption
                                print(str(Current_in_CPU.preempt_count)+" preemptions -> go to Queue4")
                                queue4.append(Current_in_CPU)
                                Current_in_CPU.queued4 = 1
                            else:
                                print("Re append to queue3")
                                queue3.append(Current_in_CPU)
                                print("After Re append after preemption, queue3 length = " + str(len(queue3)))
                                Current_in_CPU.queued3 = 1
                                break
                    # the given cpu burst finished his SRJF execution
                    if Current_in_CPU.estimated_time <= 0:
                        Current_in_CPU.Old_Time = current_time
                        Gant_Chart += " -> P" + str(Current_in_CPU.pid)
                        FinishedCpuBursts += " -> P" + str(Current_in_CPU.pid)
                        print(" Before P" + str(Current_in_CPU.pid) + " B[" + str(
                            Current_in_CPU.current_cpu_burst_location) + "] = " + str(Current_in_CPU.cpu_bursts[
                                  Current_in_CPU.current_cpu_burst_location]))
                        Current_in_CPU.cpu_bursts[Current_in_CPU.current_cpu_burst_location] = 0
                        print(" After P" + str(Current_in_CPU.pid) + " B[" + str(
                            Current_in_CPU.current_cpu_burst_location) + "] = " + str(Current_in_CPU.cpu_bursts[
                                  Current_in_CPU.current_cpu_burst_location]))
                        # Check if there still other cpu bursts
                        try:
                            if Current_in_CPU.cpu_bursts[Current_in_CPU.current_cpu_burst_location + 1]:
                                print("there exist next cpu - so go io")
                                # go to IO queue
                                Current_in_CPU.current_io_burst_location += 1
                                print("going to execute io number " + str(Current_in_CPU.current_io_burst_location))
                                Current_in_CPU.unblock_at = current_time + Current_in_CPU.io_bursts[Current_in_CPU.current_io_burst_location]
                                Current_in_CPU.current_queue = 3
                                Current_in_CPU.current_tau = 0
                                Current_in_CPU.next_tau = 0
                                Current_in_CPU.estimated_time = 0
                                IOqueue.append(Current_in_CPU)
                        except IndexError:
                            print("process is done")
                            if Current_in_CPU.done == 1:
                                print("HOWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
                                print("DA5eeel P"+str(Current_in_CPU.pid) + " las cpu position is "+str(Current_in_CPU.current_cpu_burst_location))
                            else:
                                Current_in_CPU.done = 1
                                length -= 1
                                print("Process #" + str(Current_in_CPU.pid) + " is All Done! at Q3, at Time = " + str(current_time))
                                FinishedSequence += " -> P" + str(Current_in_CPU.pid)
                elif len(queue3) <= 0:
                    if len(queue4) > 0:
                        print("-----------------------------------------Queue4-------------------------------------------")
                        print("Time = " + str(current_time))
                        print("Queue4 length = " + str(len(queue2)))
                        Current_in_CPU = queue4.pop(0)
                        print(str(Current_in_CPU.pid) + " | " + str(Current_in_CPU.current_cpu_burst_location) + " /Q4")
                        Total_Waiting_Time += current_time - Current_in_CPU.Old_Time
                        current_time += Current_in_CPU.cpu_bursts[Current_in_CPU.current_cpu_burst_location]
                        Current_in_CPU.Old_Time = current_time
                        Cpu_Busy_Time += Current_in_CPU.cpu_bursts[Current_in_CPU.current_cpu_burst_location]
                        Gant_Chart += " -> P" + str(Current_in_CPU.pid)
                        FinishedCpuBursts += " -> P" + str(Current_in_CPU.pid)
                        Current_in_CPU.cpu_bursts[Current_in_CPU.current_cpu_burst_location] = 0
                        # -------------------------------------------- UPDATE Queue#1 AND IO Queue -------------------------
                        if len(IOqueue) > 0:
                            for kk, elementsk in enumerate(IOqueue):
                                if elementsk.unblock_at <= current_time:
                                    freesk = IOqueue.pop(kk)
                                    freesk.io_bursts[freesk.current_io_burst_location] = 0
                                    freesk.current_counter = 0
                                    freesk.current_cpu_burst_location += 1
                                    freesk.unblock_at = 0
                                    if freesk.current_queue == 1:
                                        print("P" + str(freesk.pid) + " re-added to queue1 after IO")
                                        queue1.append(freesk)
                                    elif freesk.current_queue == 2:
                                        print("P" + str(freesk.pid) + " re-added to queue2 after IO")
                                        queue2.append(freesk)
                                    elif freesk.current_queue == 3:
                                        print("P" + str(freesk.pid) + " re-added to queue3 after IO")
                                        queue3.append(freesk)
                                    elif freesk.current_queue == 4:
                                        print("P" + str(freesk.pid) + " re-added to queue4 after IO")
                                        queue4.append(freesk)
                                    else:
                                        print("REVIEW YOUR IOQUEUE CODE")
                        for process_TAk in processes:
                            if process_TAk.queued1 == 0 and process_TAk.queued2 == 0 and process_TAk.queued3 == 0 and process_TAk.queued4 == 0:
                                if process_TAk.arrival_time <= current_time:
                                    process_TAk.Old_Time = process_TAk.arrival_time
                                    queue1.append(process_TAk)
                                    process_TAk.queued1 = 1
                        # ------------------------------------------- END OF UPDATING PROCESS ------------------------------
                        try:
                            if Current_in_CPU.cpu_bursts[Current_in_CPU.current_cpu_burst_location + 1]:
                                print("there exist next cpu - so go io")
                                # go to IO queue
                                Current_in_CPU.current_io_burst_location += 1
                                Current_in_CPU.unblock_at = current_time + Current_in_CPU.io_bursts[Current_in_CPU.current_io_burst_location]
                                Current_in_CPU.current_queue = 4
                                IOqueue.append(Current_in_CPU)
                        except IndexError:
                            print("process is done")
                            Current_in_CPU.done = 1
                            length -= 1
                            print("Process #" + str(Current_in_CPU.pid) + " is All Done! at Q4, at Time = " + str(current_time))
                            FinishedSequence += " -> P" + str(Current_in_CPU.pid)
                    else:  # just increase time
                        current_time += 1
                        # -------------------------------------------- UPDATE Queue#1 AND IO Queue -------------------------
                        if len(IOqueue) > 0:
                            for k, elements in enumerate(IOqueue):
                                if elements.unblock_at <= current_time:
                                    frees = IOqueue.pop(k)
                                    #frees.io_bursts[frees.current_io_burst_location] = 0
                                    frees.current_counter = 0
                                    frees.current_cpu_burst_location += 1
                                    frees.unblock_at = 0
                                    if frees.current_queue == 1:
                                        print("P" + str(frees.pid) + " re-added to queue1 after IO")
                                        queue1.append(frees)
                                    elif frees.current_queue == 2:
                                        print("P" + str(frees.pid) + " re-added to queue2 after IO")
                                        queue2.append(frees)
                                    elif frees.current_queue == 3:
                                        print("P" + str(frees.pid) + " re-added to queue3 after IO")
                                        queue3.append(frees)
                                    elif frees.current_queue == 4:
                                        print("P" + str(frees.pid) + " re-added to queue4 after IO")
                                        queue4.append(frees)
                                    else:
                                        print("REVIEW YOUR IOQUEUE CODE")
                        for process_TA in processes:
                            if process_TA.queued1 == 0 and process_TA.queued2 == 0 and process_TA.queued3 == 0 and process_TA.queued4 == 0:
                                if process_TA.arrival_time <= current_time:
                                    process_TA.Old_Time = process_TA.arrival_time
                                    queue1.append(process_TA)
                                    process_TA.queued1 = 1
                        # ------------------------------------------- END OF UPDATING PROCESS ------------------------------


    if length <= 0:
        print("--------------------------------------------Results----------------------------------------------------")
        print("* Gantt-Chart: " + str(Gant_Chart) + ".")
        print("* Cpu-Bursts Done as: " + str(FinishedCpuBursts) + ".")
        print("* Processes Done as: " + str(FinishedSequence))
        print("* Total CPU Busy Time = " + str(Cpu_Busy_Time))
        print("* Total Time = " + str(current_time))
        print("* Cpu Utilization = " + str(( Cpu_Busy_Time / current_time ) * 100 ) + " %")
        print("* Total Waiting Time = " + str(Total_Waiting_Time) + " ms")
        print("* Number of processes = "+ str(ProcessNo))
        print("* Average Waiting Time For all Processes = " + str(Total_Waiting_Time / ProcessNo) + " ms")
        print("--------------------------------------------Results----------------------------------------------------")
        print("                                     Thanks For Using My System!")

#-----------------Main------------------------
processes = read_processes("C:\\Users\\msi\\Desktop\\OS\\osproject\\workload.txt")
print_processes(processes)
print("Processes is loaded Successfully!")
qu1 = float(input("Enter the value of quantum1: "))
while qu1 <= 0:
    print("Quantum1 must be a positive number greater than 0.")
    qu1 = float(input("Enter the value of quantum1: "))

qu2 = float(input("Enter the value of quantum2: "))
while qu2 <= 0:
    print("Quantum2 must be a positive number greater than 0.")
    qu2 = float(input("Enter the value of quantum2: "))

alpha = float(input("Enter the value of alpha: "))
while alpha <= 0 or alpha >= 1:
    print("Alpha must be a positive number between 0 and 1.")
    alpha = float(input("Enter the value of alpha: "))

multilevel_scheduling(processes, qu1, qu2, alpha)
#----------------End of Main------------------
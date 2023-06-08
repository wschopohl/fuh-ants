from multiprocessing import cpu_count, Process, current_process
from multiprocessing.shared_memory import SharedMemory
import time
import numpy as np

def start_process(shm_info):
    processes = []
    print("You have", cpu_count(), "CPU's, we will use them all!")
    for i in range(cpu_count()):
        process = Process(target=change_array, args=(shm_info,i * 10))
        process.start()
        processes.append(process)
    return processes

def change_array(shm_info, row):
    curr_proc = current_process()
    print("New Changer: ", curr_proc.name)

    shm = SharedMemory(name=shm_info['name'], create=False)
    arr = np.ndarray(shm_info['shape'], dtype=shm_info['dtype'], buffer=shm.buf)
    arr = arr.view(dtype=np.uint8).reshape((*arr.shape[0:2], 4))

    for i in range(800):
        arr[i][row] = (0,0,255,0)
        time.sleep(0.01)


def join(processes):
    for process in processes:
        process.join()
        print("Process", process.name, "stopped")

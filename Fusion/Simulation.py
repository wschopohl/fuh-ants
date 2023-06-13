import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'True'
import pygame
from multiprocessing import cpu_count, Process, current_process
from multiprocessing.shared_memory import SharedMemory
import SharedArray
import time
import numpy as np

def create_wall_array(map_file):
    map_walls = pygame.image.load(map_file)
    walls_mask = pygame.mask.from_surface(map_walls)
    shm, arr, info = SharedArray.create_with(map_walls.get_width(), map_walls.get_height(), bool)

    for y in range(map_walls.get_height()):
        for x in range(map_walls.get_width()):
            arr[x][y] = walls_mask.get_at((x,y))

    return info

def setup(render_info):
    simulation_info = {}
    simulation_info['wall-array-shm'] = create_wall_array(render_info['map']['file'])
    return simulation_info

    # dynamic_overlay_surface = pygame.Surface(map_surface.get_size(), pygame.SRCALPHA)
    # rgba_array = pygame.surfarray.array2d(dynamic_overlay_surface)

    # dynamic_overlay_surface = pygame.Surface(map_surface.get_size(), pygame.SRCALPHA)
    # rgba_array = pygame.surfarray.array2d(dynamic_overlay_surface)
    
    # shm = SharedMemory(create=True, size=rgba_array.nbytes)
    # arr = np.ndarray(rgba_array.shape, dtype=rgba_array.dtype, buffer=shm.buf)
    # arr[:] = 0

    # render_info = {}
    # render_info['map'] = {'file':map_file, 'width':map_surface.get_width(), 'height':map_surface.get_height()}
    # render_info['overlay-shm'] = {'name':shm.name, 'dtype':rgba_array.dtype, 'shape':rgba_array.shape, 'nbytes':rgba_array.nbytes}
        
    # return render_info

def start_process(overlay_shm_info):
    processes = []
    print("You have", cpu_count(), "CPU's, we will use them all!")
    for i in range(cpu_count()):
        process = Process(target=change_array, args=(overlay_shm_info,i * 50))
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
        arr[i][row] = (255,0,255,255)
        time.sleep(0.01)


def join(processes):
    for process in processes:
        process.join()
        print("Process", process.name, "stopped")

def close(simulation_info):
    shm = SharedMemory(name=simulation_info['wall-array-shm']['name'], create=False)
    shm.close()
    shm.unlink()
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'True'
import pygame
import pygame.surfarray as surfarray
from multiprocessing import Process, current_process
from multiprocessing.shared_memory import SharedMemory
import numpy as np
import time

render_params = {'shm_name':'', }

def get_memory(map):
    # print("Number of cpu : ", cpu_count())
    map_surface = pygame.image.load(map)
    rgbarray = surfarray.array3d(map_surface)
    shm = SharedMemory(create=True, size=rgbarray.nbytes)
    shm_info = {'name':shm.name, 'dtype':rgbarray.dtype, 'shape':rgbarray.shape, 'nbytes':rgbarray.nbytes}
    arr = np.ndarray(rgbarray.shape, dtype=rgbarray.dtype, buffer=shm.buf)
    print(type(rgbarray), type(arr))
    arr[:] = rgbarray[:]
    return shm, shm_info

def start_process(shm_info):
    process = Process(target=render_process, args=(shm_info,))
    process.start()
    return process
    
def render_process(shm_info):
    curr_proc = current_process()
    print("Rendering: ", curr_proc.name)

    screen = pygame.display.set_mode([800, 600])
    pygame.display.set_caption("MAS Fusion")
    pygame.font.init()

    shm = SharedMemory(name=shm_info['name'], create=False)
    # arr = np.frombuffer(shm.buf, dtype=shm_info['dtype'], count=shm_info['nbytes'])
    arr = np.ndarray(shm_info['shape'], dtype=shm_info['dtype'], buffer=shm.buf)
    # arr = arr.reshape(shm_info['shape'])

    surf = pygame.surfarray.make_surface(arr)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        surf = pygame.surfarray.make_surface(arr)
        screen.blit(surf, (0,0))
        pygame.display.flip()
        time.sleep(0.04)
    


def close(shm):
    shm.close()
    shm.unlink()
    
    
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
    arr = np.ndarray(rgbarray.shape, dtype=rgbarray.dtype, buffer=shm.buf)
    print(type(rgbarray), type(arr))
    arr[:] = rgbarray[:]
    shm_info = {'name':shm.name, 'dtype':rgbarray.dtype, 'shape':rgbarray.shape, 'nbytes':rgbarray.nbytes,
        'width':map_surface.get_width(),'height':map_surface.get_height()}
    return shm, shm_info

def start_process(shm_info):
    process = Process(target=render_process, args=(shm_info,))
    process.start()
    return process
    
def render_process(shm_info):
    curr_proc = current_process()
    print("Rendering: ", curr_proc.name)

    screen = pygame.display.set_mode([shm_info['width'], shm_info['height']])
    pygame.display.set_caption("MAS Fusion")
    pygame.font.init()

    shm = SharedMemory(name=shm_info['name'], create=False)
    arr = np.ndarray(shm_info['shape'], dtype=shm_info['dtype'], buffer=shm.buf)
    
    font = pygame.font.Font('freesansbold.ttf', 32)   
    render_time_average = 0
    average_counter = 0
    running = True
    
    direct_array_blit = False # set this to true or false to test different blit techniques
    
    while running:
        timer = time.perf_counter()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if direct_array_blit:
            pygame.surfarray.blit_array(screen, arr)
        else:
            surf = pygame.surfarray.make_surface(arr)
            screen.blit(surf, (0,0))
        
        render_time = time.perf_counter() - timer
        render_time_average += render_time
        average_counter += 1
        text = font.render(f"Render Time (avg): = {1000*(render_time_average/average_counter):.3f}ms", True, (0,0,0), None)
        
        screen.blit(text, (10,10))
        pygame.display.flip()
        time.sleep(0.04)
    

def close(shm):
    shm.close()
    shm.unlink()
    
    
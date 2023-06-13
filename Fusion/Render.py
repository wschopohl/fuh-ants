import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'True'
import pygame

from multiprocessing import Process, current_process
import SharedArray
import numpy as np
import time


def setup(map_file):
    print((np.uint8))
    map_surface = pygame.image.load(map_file)
    dynamic_overlay_surface = pygame.Surface(map_surface.get_size(), pygame.SRCALPHA)
    
    shn, arr, info = SharedArray.create_from_surface(dynamic_overlay_surface)

    render_info = {}
    render_info['map'] = {'file':map_file, 'width':map_surface.get_width(), 'height':map_surface.get_height()}
    render_info['overlay-shm'] = info
        
    return render_info

def start_process(render_info):
    process = Process(target=render_process, args=(render_info,))
    process.start()
    return process
    
def render_process(render_info):
    curr_proc = current_process()
    print("Rendering: ", curr_proc.name)

    screen = pygame.display.set_mode([render_info['map']['width'], render_info['map']['height']])
    map_surface = pygame.image.load(render_info['map']['file'])
    main_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    
    pygame.display.set_caption("MAS Fusion")
    pygame.font.init()

    shm, arr = SharedArray.get_array(render_info['overlay-shm'])

    font = pygame.font.Font('freesansbold.ttf', 32)   
    render_time_average = 0
    average_counter = 0
    running = True
    
    direct_array_blit = True # set this to true or false to test different blit techniques
    
    while running:
        timer = time.perf_counter()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0,255,0))
        screen.blit(map_surface, (0,0))

        if direct_array_blit:
            pygame.surfarray.blit_array(main_surface, arr)
        else:
            # colors are bgra, but wull not be used anyway
            surf = pygame.surfarray.make_surface(arr)
            main_surface.blit(surf, (0,0))
        
        render_time = time.perf_counter() - timer
        render_time_average += render_time
        average_counter += 1
        text = font.render(f"Render Time (avg): = {1000*(render_time_average/average_counter):.3f}ms", True, (0,0,0), None)
        
        screen.blit(main_surface, (0,0))
        screen.blit(text, (10,10))
        pygame.display.flip()
        time.sleep(0.04)
    

def close(render_info):
    SharedArray.close(render_info['overlay-shm'])
    
    
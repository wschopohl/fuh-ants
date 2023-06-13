import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'True'
import pygame
from multiprocessing.shared_memory import SharedMemory
import numpy as np

def create_from_surface(surface):
    rgba_array = pygame.surfarray.array2d(surface)
    shm = SharedMemory(create=True, size=rgba_array.nbytes)
    arr = np.ndarray(rgba_array.shape, dtype=rgba_array.dtype, buffer=shm.buf)
    arr[:]=rgba_array[:]
    info = {'name':shm.name, 'dtype':rgba_array.dtype, 'shape':rgba_array.shape, 'nbytes':rgba_array.nbytes}
    return (shm, arr, info)

def create_with(width=0, height=0, dtype=np.uint8):
    arr = np.ndarray(shape=(width, height), dtype=dtype)
    shm = SharedMemory(create=True, size=arr.nbytes)
    arr = np.ndarray(shape=(width, height), dtype=dtype, buffer=shm.buf)
    info = {'name':shm.name, 'dtype':arr.dtype, 'shape':arr.shape, 'nbytes':arr.nbytes}
    return (shm, arr, info)

def get_array(info):
    shm = SharedMemory(name=info['name'], create=False)
    arr = np.ndarray(info['shape'], dtype=info['dtype'], buffer=shm.buf)
    return (shm, arr)

def close(shm_info):
    shm = SharedMemory(name=shm_info['name'], create=False)
    shm.close()
    shm.unlink()

def get():
    pass
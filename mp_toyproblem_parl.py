
###############################################################
### PARALLELIZATION USING PYTHON’S MULTIPROCESSING LIBRARY  ###
### A TOY PROBLEM                                           ###
### by: OAMEED NOAKOASTEEN                                  ###
###############################################################

import os
import time
import argparse
import numpy                    as np
import multiprocessing          as mp
import multiprocessing.managers as mpm

def init_worker(shm_info):
    global x_shm_wrk, y_shm_wrk, z_shm_wrk
    global x_shared , y_shared , z_shared
    
    x_shm_wrk = mp.shared_memory.SharedMemory(name = shm_info['x']['name'], create = False)
    x_shared  = np.ndarray(shm_info['x']['shape'], dtype = shm_info['x']['dtype'], buffer = x_shm_wrk.buf)

    y_shm_wrk = mp.shared_memory.SharedMemory(name = shm_info['y']['name'], create = False)
    y_shared  = np.ndarray(shm_info['y']['shape'], dtype = shm_info['y']['dtype'], buffer = y_shm_wrk.buf)
    
    z_shm_wrk = mp.shared_memory.SharedMemory(name = shm_info['z']['name'], create = False)
    z_shared  = np.ndarray(shm_info['z']['shape'], dtype = shm_info['z']['dtype'], buffer = z_shm_wrk.buf)

    print('[Worker Initialized] Process ID: {}\n'.format(os.getpid()))
    

def sumnumbers(index):
    z_shared[index] = x_shared[index] + y_shared[index]


if __name__ == '__main__':
    parser       = argparse.ArgumentParser()
    parser.add_argument('-n', type = int, required = True)
    args         = parser.parse_args()
    shape        = (args.n,)
    dtype        = np.float64
    bytes_needed = np.prod(shape)*np.dtype(dtype).itemsize
    cpu_count    = mp.cpu_count() # mp.cpu_count()
    chunksize    = None
    indeces      = [index for index in range(shape[0])]
    
    with mpm.SharedMemoryManager() as smm:
        
        x_shm    = smm.SharedMemory(size = bytes_needed)
        y_shm    = smm.SharedMemory(size = bytes_needed)
        z_shm    = smm.SharedMemory(size = bytes_needed)
        
        shm_info = {'x': {'name': x_shm.name, 'shape': shape, 'dtype': dtype},
                    'y': {'name': y_shm.name, 'shape': shape, 'dtype': dtype},
                    'z': {'name': z_shm.name, 'shape': shape, 'dtype': dtype} }

        x        = np.ndarray(shape, dtype = dtype, buffer = x_shm.buf)
        y        = np.ndarray(shape, dtype = dtype, buffer = y_shm.buf)
        z        = np.ndarray(shape, dtype = dtype, buffer = z_shm.buf)
        for i in range(shape[0]):
            x[i] =   i
            y[i] = 2*i
            z[i] = 0
        
        with mp.Pool(processes = cpu_count, initializer = init_worker, initargs = (shm_info,)) as pool:
            tick = time.perf_counter()
            pool.map(sumnumbers, indeces, chunksize = chunksize)
            tock = time.perf_counter()
            
            pool.close()
            pool.join ()
    
    #print(x)
    #print(y)    
    #print(z)
    print('[BENCHMARK] Parallel execution segment took: {:.3f} (ms)\n'.format((tock - tick)/1e-3))

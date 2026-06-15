###############################################################
### PARALLELIZATION USING PYTHON’S MULTIPROCESSING LIBRARY  ###
### A TOY PROBLEM                                           ###
### by: OAMEED NOAKOASTEEN                                  ###
###############################################################

import os
import time
import argparse
import numpy    as np


def sumnumbers(x,y,z,index):
    z[index] = x[index] + y[index]

def main():
    parser  = argparse.ArgumentParser()
    parser.add_argument('-n', type = int, required = True)
    args    = parser.parse_args()
    shape   = (args.n,)
    indeces = [index for index in range(shape[0])]
    
    x       = np.zeros(shape)
    y       = np.zeros(shape)
    z       = np.zeros(shape)
    for index in indeces:
        x[index] =   index
        y[index] = 2*index

    tick = time.perf_counter()
    for index in indeces:
        sumnumbers(x,y,z,index)
    tock = time.perf_counter()

    #print(x)
    #print(y)
    #print(z)
    print('[BENCHMARK] Serial execution segment took: {:.3f} (ms)\n'.format((tock - tick)/1e-3))


if __name__ == '__main__':
    main()

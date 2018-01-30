from multiprocessing import Process, Manager, current_process
from multiprocessing.managers import BaseManager, SyncManager
from multiprocessing import Pool, freeze_support, Process, Array
from functools import partial
import os
import time
import multiprocessing
import threading
import copy

num_tile = 4
num_process = 4
max_cycles = 5

class Tile():

    def __init__ (self):
        self.tile_halt = 0
        self.counter = 0

    def tile_run(self, cycle):
        #START SOME COMPUTATION
        aba = []
        for i in range(10000):
            aba.append(i ** 10 + (i * 10) ** 10 + (i * 10) ** 10)
        #END SOME COMPUTATION

        self.counter += 1
        if self.counter == max_cycles -1:
            self.tile_halt = 1

    def get_halt(self):
        return self.tile_halt

def run_tile(tile, cycle, i):
    if (not tile.get_halt()):
        tile.tile_run (cycle)

class Node(object):
    def __init__(self):
        BaseManager.register('Tile', Tile)
        self.manager = BaseManager()
        self.manager.start()

        self.tile_list = [self.manager.Tile() for _ in range(num_tile)]
        self.tile_halt_list = [0 for _ in range(num_tile)]

    def node_run_process(self, cycle):
        process_list = []

        for i in xrange(num_tile):
            p = Process(target=run_tile, args=(self.tile_list[i], cycle,i,))
            p.daemon = True
            process_list.append(p)

        for p in process_list:
            p.start()

        for p in process_list:
            p.join()

        for i in xrange(num_tile):
            self.tile_halt_list[i] = self.tile_list[i].get_halt()

        print "Cycle: {} Halted? {}".format(cycle, self.halt())

    def node_run_single(self, cycle):
        for i in range(num_tile):
            self.tile_list[i].tile_run (cycle)
            self.tile_halt_list[i] = self.tile_list[i].get_halt()

        print "Cycle: {} Halted? {}".format(cycle, self.halt())

    def halt(self):
        return all(self.tile_halt_list)

def run_process():
    node = Node()
    for i in range(max_cycles):
        node.node_run_process(i)

def run_sync():
    node = Node()
    for i in range(max_cycles):
        node.node_run_single(i)


if __name__ == '__main__':
    freeze_support()
    print 'Tiles {}'.format(num_tile)

    start = time.time()
    run_process()
    end = time.time()
    print ('time process: ' + str(end-start) + 'secs')

    start = time.time()
    run_sync()
    end = time.time()
    print ('time single thread: ' + str(end-start) + 'secs')


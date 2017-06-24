# Defines a configurable tile with its methods

import sys
sys.path.insert (0, '/home/ankitaay/dpe/include')

import numpy as np
import constants as param
import ima as ima
import tile_modules as tmod

# IMA specific modules (should not be needed)
import ima_modules
import generate_inst

class tile (object):

    # Instantiate different modules
    def __init__ (self):
        self.ima_list = []
        for i in range (param.num_ima):
            temp_ima = ima.ima ()
            self.ima_list.append(temp_ima)

        # EDRAM controller includes edram too
        self.edram_controller = tmod.edram_controller ()

        # Halt for tile - Tile halts when all IMAs halt
        self.halt_list = []

        # Fid list for IMA tracefiles
        self.fid_list = []


    # Initialize the tile (all IMAs in the tile)
    def tile_init (self):
        # Initialize the IMAs
        for i in range (param.num_ima):
            self.ima_list[i].pipe_init ()

        self.halt_list = [0] * param.num_ima


    # One cycle execution of tile - run all IMAs until all of them halt
    def tile_run (self, cycle, path = ''):
        # open tracefile(s) list & haltlist for IMAs in the first cycle
        if (cycle == 0):
            self.fid_list = []
            for i in range (param.num_ima):
                tracefile = path + 'trace' + str(i) + '.txt'
                fid_temp = open (tracefile, 'w')
                self.fid_list.append (fid_temp)

        if (0 in self.halt_list): # do until all imas have halted
            for i in range (param.num_ima): # traverse ima list and run only if not halted
                if (self.halt_list[i] != 1):
                    self.ima_list[i].pipe_run (cycle, self.fid_list[i])
                    self.halt_list[i] = self.ima_list[i].halt #uodate halt

        # for DEBUG only
        print 'cycle: ' + str(cycle) + ' halt_list:', self.halt_list

        # for DEBUG only
        if (sum(self.halt_list) == param.num_ima):
            print ('Tile ran for ' + str(cycle) + ' cycles')


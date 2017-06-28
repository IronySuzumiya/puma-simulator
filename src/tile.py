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

        # File list for IMA tracefiles
        self.fid_list = []

        # Book-keeping variables for edram controller
        self.memstate = 'free' # can be free/busy
        self.latency = 0 # holds latency for memory access
        self.stage_cycle = 0 # holds current cycle invested in memory access


    # Initialize the tile (all IMAs in the tile)
    def tile_init (self):
        # Initialize the IMAs
        for i in range (param.num_ima):
            self.ima_list[i].pipe_init ()

        self.halt_list = [0] * param.num_ima


    # Simulate one cycle exectution of all IMAs (which have't halted)
    def tile_run (self, cycle, path = ''):
        ## open tracefile(s) list & haltlist for IMAs in the first cycle
        if (cycle == 0):
            self.fid_list = []
            for i in range (param.num_ima):
                tracefile = path + 'trace' + str(i) + '.txt'
                fid_temp = open (tracefile, 'w')
                self.fid_list.append (fid_temp)

        ## run IMAs that haven't halted
        if (not all(self.halt_list)): # A tile halts whwn all IMAs (within the tile) halt
            for i in range (param.num_ima):
                if (self.halt_list[i] != 1):
                    self.ima_list[i].pipe_run (cycle, self.fid_list[i])
                    self.halt_list[i] = self.ima_list[i].halt #update halt

        ## Simulate a cycle of memory operation
        # Probe IMA mem_interface to find one/many pending memory requests
        ren_list = [0] * param.num_ima
        wen_list = ren_list[:]
        ramstore_list = [''] * param.num_ima
        addr_list = ren_list[:]
        for i in range (param.num_ima):
            ren_list[i] = self.ima_list[i].mem_interface.ren
            wen_list[i] = self.ima_list[i].mem_interface.wen
            addr_list[i] = self.ima_list[i].mem_interface.addr
            ramstore_list[i] = self.ima_list[i].mem_interface.ramstore

        # Invoke memory request if memory is free (latency = 0)
        if (self.memstate == 'free' and self.stage_cycle == 0 and (any (ren_list) or any (wen_list))):
            self.memstate = 'busy'
            self.latency = self.edram_controller.getLatency ()
            self.stage_cycle = self.stage_cycle + 1

            # check if the access lateny is 2 cycles - need to update ima mem_interface
            if (self.stage_cycle == self.latency - 1):
                [idx, ramload] = self.edram_controller.propagate (ren_list, \
                        wen_list, ramstore_list, addr_list)

                self.ima_list[idx].mem_interface.wait = 0
                self.ima_list[idx].mem_interface.ramload = ramload

            # check if access latnecy is 1 cycle - need to complete execute in this cycle
            elif (self.stage_cycle == self.latency):
                # finish & free up edram controller
                self.stage_cycle = 0
                self.memstate = 'free'

                # update memory interface of served ima
                [idx, ramload] = self.edram_controller.propagate (ren_list, \
                        wen_list, ramstore_list, addr_list)

                self.ima_list[idx].mem_interface.wait = 0
                self.ima_list[idx].mem_interface.ramload = ramload

                # do a cycle (finish in case of ST) of execute pipeline stage of the served ima
                # Note - update_ready fo execute stage is always 1 (Current Deisgn)
                ex_op = self.ima_list[idx].de_opcode
                if (ex_op == 'st'):
                    do_execute (self, ex_op)
                    self.stage_done[sId] = 1
                    self.stage_cycle[sId] = 0
                    self.stage_empty[sId] = 1
                # Assumption - DataMemory cannot be done in the last access cycle
                elif (ex_op == 'ld'):
                    self.stage_cycle[sId] = self.latency[sId] - self.dataMem.getLatency () # can be data_mem too

        elif (self.memstate == 'busy'): # busy state
            # Update ima mem interface of ima a cycle before finishing
            if (self.stage_cycle == self.latency - 2):
                self.stage_cycle = self.stage_cycle + 1
                [idx, ramload] = self.edram_controller.propagate (ren_list, \
                        wen_list, ramstore_list, addr_list)

                self.ima_list[idx].mem_interface.wait = 0
                self.ima_list[idx].mem_interface.ren = 0
                self.ima_list[idx].mem_interface.wen = 0
                self.ima_list[idx].mem_interface.ramload = ramload

            # Finish the access and free up controller from previous access
            elif (self.stage_cycle == self.latency -1):
                self.stage_cycle = 0
                self.memstate = 'free'

            # Wait for request to finish
            else:
                self.stage_cycle = self.stage_cycle + 1

        ## for DEBUG only
        print 'cycle: ' + str(cycle) + ' halt_list:', self.halt_list
        if (all(self.halt_list)):
            print ('Tile ran for ' + str(cycle) + ' cycles')


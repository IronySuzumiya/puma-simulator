# Defines a configurable tile with its methods

import sys
sys.path.insert (0, '/home/ankitaay/dpe/include')

import Queue

import numpy as np
import constants as param
import ima as ima
import tile_modules as tmod

# IMA specific modules (should not be needed)
import ima_modules

class tile (object):

    ### Instantiate different modules in a tile
    def __init__ (self):
        ## Objects which correspond to a hardware component (at least NOW!)
        # ima_list
        self.ima_list = []
        for i in range (param.num_ima):
            temp_ima = ima.ima ()
            self.ima_list.append(temp_ima)
        # EDRAM controller (icnludes edram)
        self.edram_controller = tmod.edram_controller ()
        # intruction memory
        self.instrn_memory = tmod.instrn_memory (param.tile_instrnMem_size)
        # receive buffer
        self.receive_buffer = tmod.receive_buffer (param.receive_buffer_size)
        # program counter
        self.pc = 0
        # fetched instruction
        self.instrn = param.dummy_instrn_tile

        ## Book-keeping variables (may not have a harwdare relevance)
        # send_queue - part of NOC that connects the tiles
        self.send_queue = Queue.Queue()
        # track instruction being executed hasn't completed yet or not
        self.stall = 0
        # latch tag_hit and data (prevents unnecessary repeated buff accesses)
        self.tag_matched = 0
        self.received_data = '' * param.edram_buswidth
        # halt for tile
        self.tile_halt = 0
        # for imas
        # tracks the halts of ima all IMAs halt
        self.halt_list = []
        self.ima_nma_list = [] # tells which ima would be running
        # File list for IMA tracefiles
        self.fid_list = []
        # For edram interface (send/receive generated edram accesses)
        self.latency_sr = 0
        self.stage_cycle_sr = 0
        # For edram controller (ima generated edram accesses)
        self.memstate = 'free' # can be free/busy
        self.latency = 0 # holds latency for memory access
        self.stage_cycle = 0 # holds current cycle invested in memory access


    ### Initialize the tile (all IMAs in the tile)
    def tile_init (self, instrnpath, tracepath):
        # Initialize the tile instruction memory
        instrn_filepath = instrnpath + 'tile_imem1' + '.npy'
        dict_list = np.load(instrn_filepath)
        self.instrn_memory.load (dict_list)

        # Initialize the IMAs and their trace file ids
        for i in range (param.num_ima):
            # tracefile is where stats are dumped
            tracefile = tracepath + 'trace' + str(i+1) + '.txt'
            fid_temp = open (tracefile, 'w')
            self.fid_list.append (fid_temp)
            # instrn_file provides the instrn_list that the IMA will execute
            instrnfile = instrnpath + 'ima_imem' + str(i+1) + '.npy'
            self.ima_list[i].pipe_init (instrnfile, self.fid_list[i])

        # Initialize the EDRAM - invalidate all entries (valid_list)
        self.edram_controller.valid = [0] * param.edram_size
        for i in range(3):
            self.edram_controller.valid[i+7] = 1
            self.edram_controller.counter[i+7] = 1

        # Intiialize the receive buffer - invalidate
        self.receive_buffer.inv ()
        # Initialize the program counter
        self.pc = 0
        # Intialize tile
        self.tile_halt = 0
        # Initiaize the halt list & stall flag for tile
        self.halt_list = [0] * param.num_ima
        self.ima_nma_list = [0] * param.num_ima
        self.stall = 0


    ### Simulate one cycle exectution of all IMAs (which have't halted) & their EDRAM interactions
    def tile_compute (self, cycle):
        ## Simulate a cycle if IMA(s) that haven't halted
        if (not all(self.halt_list)): # A tile halts whwn all IMAs (within the tile) halt
            for i in range (param.num_ima):
                if ((not self.halt_list[i]) and self.ima_nma_list[i]):
                    self.ima_list[i].pipe_run (cycle, self.fid_list[i])
                    self.halt_list[i] = self.ima_list[i].halt # update halt

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

        # Invoke memory request if memory is free
        if (self.memstate == 'free' and self.stage_cycle == 0 and (any (ren_list) or any (wen_list))):
            self.memstate = 'busy'
            self.latency = self.edram_controller.getLatency ()
            self.stage_cycle = self.stage_cycle + 1
            # For DEUG only
            #print ('memory controller enters BUSY')

            # check if the access lateny is 2 cycles - need to update ima mem_interface
            if (self.stage_cycle == self.latency - 1):
                [found, idx, ramload] = self.edram_controller.propagate (ren_list, \
                        wen_list, ramstore_list, addr_list)

                if (found): # edram controller returns after finisning the LD/ST
                    self.ima_list[idx].mem_interface.wait = 0
                    self.ima_list[idx].mem_interface.ren = 0
                    self.ima_list[idx].mem_interface.wen = 0
                    self.ima_list[idx].mem_interface.ramload = ramload

            #### This case NEEDS FIXING!!
            # check if access latency is 1 cycle - need to complete execute in this cycle
            elif (self.stage_cycle == self.latency):
                # finish & free up edram controller
                self.stage_cycle = 0
                self.memstate = 'free'

                # update memory interface of served ima
                [found, idx, ramload] = self.edram_controller.propagate (ren_list, \
                        wen_list, ramstore_list, addr_list)

                if (found): # edram controller returns after finisning the LD/ST
                    self.ima_list[idx].mem_interface.wait = 0
                    self.ima_list[idx].mem_interface.ren = 0
                    self.ima_list[idx].mem_interface.wen = 0
                    self.ima_list[idx].mem_interface.ramload = ramload

                    # do a cycle (finish in case of ST) of execute pipeline stage of the served ima
                    # Note - update_ready fo execute stage is always 1 (Current Deisgn)
                    ex_op = self.ima_list[idx].de_opcode
                    sId = 2
                    if (ex_op == 'st'):
                        do_execute (self, ex_op)
                        self.ima_list[idx].stage_done[sId] = 1
                        self.ima_list[idx].stage_cycle[sId] = 0
                        self.ima_list[idx].stage_empty[sId] = 1
                    # Assumption - DataMemory cannot be done in the last access cycle
                    elif (ex_op == 'ld'):
                        self.stage_cycle[sId] = self.latency[sId] - self.ima_list[0].dataMem.getLatency () # can be data_mem too

        elif (self.memstate == 'busy'): # busy state
            # Update ima mem interface of ima a cycle before finishing
            if (self.stage_cycle == self.latency - 2):
                self.stage_cycle = self.stage_cycle + 1
                [found, idx, ramload] = self.edram_controller.propagate (ren_list, \
                        wen_list, ramstore_list, addr_list)

                if (found): # edram controller returns after finisning the LD/ST
                    self.ima_list[idx].mem_interface.wait = 0
                    self.ima_list[idx].mem_interface.ren = 0
                    self.ima_list[idx].mem_interface.wen = 0
                    self.ima_list[idx].mem_interface.ramload = ramload

            # Finish the access and free up controller from previous access
            elif (self.stage_cycle == self.latency -1):
                self.stage_cycle = 0
                self.memstate = 'free'
                #print ('memory controller FREE')

            # Wait for request to finish
            else:
                self.stage_cycle = self.stage_cycle + 1


    ### tile_run - simulate a cycle of execution of the tile
    # data addition to receive buffer happens by the higher level hierarchy
    # ?? - All memory access parts will be modified (based on changes in edram_controller)
    def tile_run (self, cycle):
        ## execute the current instruction in tile's instruction memory
        # Fetch a new instrn only after the previous instrn completes
        if (not self.stall):
            self.instrn = self.instrn_memory.read (self.pc)
            self.pc = self.pc + 1

        # Check if the current fetched instrn can  be completed
        assert (self.instrn['opcode'] in param.op_list_tile), 'Tile: unsupported opcode'
        if (self.instrn['opcode'] == 'send'):
            # check if the mem_addr is valid
            mem_addr = self.instrn['mem_addr']
            if (self.edram_controller.valid[mem_addr]):
                # first but not last cycle of edram access
                if (self.stage_cycle_sr == 0 and self.edram_controller.getLatency() != 1):
                    self.latency_sr = self.edram_controller.getLatency ()
                    self.stage_cycle_sr += 1
                    self.stall = 1
                # last cycle of edram access
                elif (self.stage_cycle_sr == self.latency_sr - 1 or self.edram_controller.getLatency() == 1):
                    # reset the stage_cycle
                    self.stage_cycle_sr = 0
                    # add the entry to send list (send_list is physically part of NOC and not tile)
                    data = self.edram_controller.mem.read(mem_addr)
                    target_addr = self.instrn['r2']
                    neu_id = self.instrn['neuron_id']
                    temp_dict = {'data':data, 'target_addr':target_addr, 'cycle':cycle, 'neu_id':neu_id}
                    self.send_queue.put (temp_dict)
                    # update the counter and valid flag (if req.) for edram
                    self.edram_controller.counter[mem_addr] -= 1
                    if (self.edram_controller.counter[mem_addr] <= 0):
                        self.edram_controller.valid[mem_addr] = 0
                    self.stall = 0
                # other cycles (not first or last)
                else:
                    self.stage_cycle_sr += 1
            # stall if edram entry is not empty
            else:
                self.stall = 1

        elif (self.instrn['opcode'] == 'receive'):
            # check tag if only if not checked previously
            if (self.tag_matched == 0):
                neu_id = self.instrn['neuron_id']
                [tag_hit, data] = self.receive_buffer.read (neu_id)
                self.tag_matched = tag_hit
                self.received_data = data

            mem_addr = self.instrn['mem_addr']
            # if tag matches check if edram entry is empty/free (invalid)
            if (self.tag_matched and (not self.edram_controller.valid[mem_addr])):
                # first but not last cycle of edram access
                if (self.stage_cycle_sr == 0 and self.edram_controller.getLatency() != 1):
                    self.latency_sr = self.edram_controller.getLatency ()
                    self.stage_cycle_sr += 1
                    self.stall = 1
                # last cycle of edram access
                elif (self.stage_cycle_sr == self.latency_sr - 1 or self.edram_controller.getLatency() == 1):
                    # reset the stage_cycle
                    self.stage_cycle_sr = 0
                    # write data to edram and set valid &counter entries
                    temp_counter = self.instrn['r2']
                    self.edram_controller.mem.write (mem_addr, self.received_data)
                    self.edram_controller.valid[mem_addr] = 1
                    self.edram_controller.counter[mem_addr] = temp_counter
                    # set other book-keeping flags
                    self.tag_matched = 0
                    self.stall = 0
                # other cycles (not first or last)
                else:
                    self.stage_cycle_sr += 1
            else:
                self.stall = 1

        elif (self.instrn['opcode'] == 'compute'):
            # mask tells which new ima(s) should start executing
            # note: some ima(s) could have already been running previously
            temp_ima_nma = self.instrn['ima_nma']  # this is a bit-string
            for i in range (param.num_ima):
                self.ima_nma_list[i] = self.ima_nma_list[i] | int(temp_ima_nma[i])

        else: # halt instruction
            # tile can halt only after all imas halt
            # those imas which haven't been used don't matter
            for k in range(len(self.halt_list)):
                if (not self.ima_nma_list[k]):
                    self.halt_list[k] = 1

            # check if all imas halted
            if (all(self.halt_list)):
                self.tile_halt = 1
                self.stall = 0 # Doesn't matter as this was the last cycle
            else:
                # prevent new instructions to befetched
                self.stall = 1

        ## simulate a cycle of ima execution based on current state of self.ima_nma
        self.tile_compute (cycle)

        ## for DEBUG only
        print 'cycle: ' + str(cycle) + ' halt_list:', self.halt_list
        if (self.tile_halt):
            print ('send_list', self.send_queue.queue)
            print ('Tile ran for ' + str(cycle) + ' cycles')
            # Close all the trace files
            for tr_fid in self.fid_list:
                tr_fid.close ()

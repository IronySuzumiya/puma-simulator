# Defines a configurable node with its methods
import sys, getopt
sys.path.insert (0, '/home/ankitaay/dpe/include/')
sys.path.insert (0, '/home/ankitaay/dpe/src/')

import numpy as np
import constants as param
import ima_modules
import ima
import tile_modules
import tile
import node_modules as nmod

class node (object):

    instances_created = 0

    ### Instantiate different modules in a node
    def __init__ (self):

        # Assign a node_id for identification purpose in debug trace
        self.node_id = node.instances_created

        # Instantiate the tile list
        self.tile_list = []
        for i in range (param.num_tile): #first & last tiles - dummy, others - compute
            temp_tile = tile.tile ()
            self.tile_list.append (temp_tile)

        # Instantiate the NOC
        self.noc = nmod.noc ()

        # Some book-keeping variables (Can have harwdare correspondance)
        self.node_halt = 0
        self.tile_halt_list = [0] * param.num_tile
        self.tile_fid_list = []


    ### Initialize the tiles within node and open the trace file for each tile
    def node_init (self, instrnpath, tracepath):
        for i in range (param.num_tile):
            # open tracefile for tile - place where stats are dumped
            tracefile = tracepath + 'tile' + str(i) + '/tile_trace.txt'
            fid_temp = open (tracefile, 'w')
            self.tile_fid_list.append (fid_temp)

            # initialize the tile
            temp_instrnpath = instrnpath + 'tile' + str(i) + '/'
            temp_tracepath = tracepath + 'tile' + str(i) + '/'
            self.tile_list[i].tile_init (temp_instrnpath, temp_tracepath)

        # intialize the tile_halt_list and node_halt
        self.node_halt = 0
        self.tile_halt_list = [0] * param.num_tile


    ### Simulate a cycle of execution of a node
    def node_run (self, cycle):

        # data transfer latency includes noc latency and receive buffer latency
        #transfer_latency = self.noc.getLatency() + \
        #        self.tile_list[0].receive_buffer.getLatency()

        # A cyle execution of each tile and probe each tile's halt
        for i in range (param.num_tile):
            # run a tile only if has not halted
            if (not self.tile_list[i].tile_halt):
                self.tile_list[i].tile_run (cycle, self.tile_fid_list[i])
                self.tile_halt_list[i] = self.tile_list[i].tile_halt

        # A cycle execution of noc (data transfers between tiles)
        # If latency satisfies, write to destination tile's receive buffer
        for i in range (param.num_tile):
            # check entry at head of queue (if non-empty) for all tiles for noc latency
            if (not self.tile_list[i].send_queue.empty()):
                temp_queue_head = self.tile_list[i].send_queue.queue[0]
                #print ('Tile: ', i, 'send_queue_size: ', len(self.tile_list[i].send_queue.queue))
                target_addr = temp_queue_head['target_addr']
                transfer_latency = self.noc.getLatency (target_addr) + \
                        self.tile_list[0].receive_buffer.getLatency()
                [node_addr, tile_addr] = self.noc.propagate (target_addr)
                if (((cycle - temp_queue_head['cycle']) >= transfer_latency-1) and \
                        (not self.tile_list[tile_addr].receive_buffer.isfull()[0])):
                    # remove from queue
                    self.tile_list[i].send_queue.get()
                    # write to destination's receive buffer
                    [node_addr, tile_addr] = self.noc.propagate (target_addr)
                    # ignoring node_addr for now -- NEED TO FIX!!!
                    temp_data = temp_queue_head['data']
                    temp_neuron_id = temp_queue_head['neuron_id']
                    temp_dict = {'data':temp_data, 'neuron_id':temp_neuron_id}
                    #print (tile_addr)
                    self.tile_list[tile_addr].receive_buffer.write (temp_dict)

        # For DEBUG
        print ('Cycle: ', cycle, 'Tile halt list', self.tile_halt_list)

        # check if node halted
        if (all (self.tile_halt_list)):
            self.node_halt = 1
            for tr_id in self.tile_fid_list:
                tr_id.close ()
            print ('cycle: ' + str (cycle) + ' Node Halted')


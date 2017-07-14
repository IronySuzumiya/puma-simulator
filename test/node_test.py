# Test script for node simulations
tracepath = '/home/ankitaay/dpe/test/traces/LSTM2/'
instrnpath = '/home/ankitaay/dpe/test/testasm/LSTM2/'

import sys, getopt
sys.path.insert (0, '/home/ankitaay/dpe/include/')
sys.path.insert (0, '/home/ankitaay/dpe/src/')

import numpy as np
import constants as param
import ima_modules
import ima
import tile_modules
import tile
import node_modules
import node

# Can be needed for integer to binary conversions
from ima_modules import int2bin

# Define the node dump function
# Define a dump function which dums the all memory components into a file
def dump (node, filepath = ''):
    for i in range(len(node.tile_list)):
        filename = filepath + 'tile' + str(i+1) + '/memsim1.txt'
        fid = open (filename, 'w')

        # define a dump function for a memory entity
        def mem_dump (memfile, name): # for conciseness
            assert (type(memfile) == list), 'memfile should be list'
            fid.write (name + ' contents\n')
            for entry in memfile:
                if (entry != ''):
                    fid.write(entry + '\n')

        # dump the edram - one per tile
        mem_dump (node.tile_list[i].edram_controller.mem.memfile, 'EDRAM')

        # dump the memory components of IMA
        for i in range (param.num_ima):
            # dump the datamemory
            fid.write ('IMA id: ' + str(i) + '\n')
            mem_dump (node.tile_list[i].ima_list[i].dataMem.memfile, 'DataMemory')

            for j in range (param.num_xbar):
                # dump the xbar input memory
                mem_dump (node.tile_list[i].ima_list[i].xb_inMem_list[j].memfile, 'Xbar Input Memory')
                # dump the xbar output memory
                mem_dump (node.tile_list[i].ima_list[i].xb_outMem_list[j].memfile, 'Xbar Output Memory')

        fid.close()

# Instantiate the tile under test
node_dut = node.node ()

# Generate the instruction file(s) for ima(s)
# generate_inst.generate_inst ()

# Initialize the tile - instrnpath provides instrns for tile as well as resident imas
node_dut.node_init (instrnpath, tracepath)

# Run the tile
cycle = 0
while (not node_dut.node_halt and cycle < param.cycles_max):
    node_dut.node_run (cycle)
    cycle = cycle + 1

    # Add things to receive buffers (tile1 and tile2) at cycle x
    if (cycle == 10):
        # Enter values for tile 0
        tile_id = 0
        for i in range (7):
            data = int2bin (i, param.data_width)
            temp_dict = {'data':data, 'neuron_id':i}
            node_dut.tile_list[tile_id].receive_buffer.write (temp_dict)

        # Enter values for tile 1
        tile_id = 1
        for i in range (4):
            data = int2bin (i, param.data_width)
            temp_dict = {'data':data, 'neuron_id':i}
            node_dut.tile_list[tile_id].receive_buffer.write (temp_dict)

print 'Finally node halted' + ' | PS: max_cycles ' + str (param.cycles_max)

dumpfile = ''
dump (node_dut, tracepath)


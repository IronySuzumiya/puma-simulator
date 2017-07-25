# Test script for tile simulations
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

from data_convert import int2bin

# Define the tile dump function
# Define a dump function which dums the all memory components into a file
def dump (tile, filename = ''):
    if (filename == ''):
        filename = 'memsim1.txt'

    fid = open (filename, 'w')

    def mem_dump (memfile, name): # for conciseness
        assert (type(memfile) == list), 'memfile should be list'
        fid.write (name + ' contents\n')
        for entry in memfile:
            if (entry != ''):
                fid.write(entry + '\n')

    # dump the edram - one per tile
    mem_dump (tile.edram_controller.mem.memfile, 'EDRAM')

    # dump the memory components of IMA
    for i in range (param.num_ima):
        # dump the datamemory
        fid.write ('IMA id: ' + str(i) + '\n')
        mem_dump (tile.ima_list[i].dataMem.memfile, 'DataMemory')

        for j in range (param.num_xbar):
            # dump the xbar input memory
            mem_dump (tile.ima_list[i].xb_inMem_list[j].memfile, 'Xbar Input Memory')
            # dump the xbar output memory
            mem_dump (tile.ima_list[i].xb_outMem_list[j].memfile, 'Xbar Output Memory')

    fid.close()

# Instantiate the tile under test
tile_dut = tile.tile ()

# Generate the instruction file(s) for ima(s)
# generate_inst.generate_inst ()

# Initialize the tile - instrnpath provides instrns for tile as well as resident imas
tile_dut.tile_init (instrnpath, tracepath)

# Run the tile
cycle = 0
tracefile = tracepath + 'tile_trace1.txt'
tile_fid = open (tracefile, 'w')

while (not tile_dut.tile_halt and cycle < param.cycles_max):
    tile_dut.tile_run (cycle, tile_fid)
    cycle = cycle + 1

    # Add things to receive buffer at cycle x
    if (cycle == 10):
        for i in range (7):
            data = int2bin (i, param.data_width)
            temp_dict = {'data':data, 'neuron_id':i}
            tile_dut.receive_buffer.write (temp_dict)
            # print (tile_dut.receive_buffer.buffer)

tile_fid.close()
print 'Finally tile halted' + ' | PS: max_cycles ' + str (param.cycles_max)

dumpfile = ''
dump (tile_dut, dumpfile)

# Test script for tile simulations
tracepath = '/home/ankitaay/dpe/test/traces/'
instrnpath = '/home/ankitaay/dpe/test/testasm/LSTM/'

import sys, getopt
sys.path.insert (0, '/home/ankitaay/dpe/include/')
sys.path.insert (0, '/home/ankitaay/dpe/src/')

import numpy as np
import constants as param
import ima_modules
import ima
import tile_modules
import tile

# Define the tile dump function
# Define a dump function which dums the all memory components into a file
def dump (tile, filename = ''):
    if (filename == ''):
        filename = 'memsim.txt'

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
tile = tile.tile ()

# Generate the instruction file(s) for ima(s)
# generate_inst.generate_inst ()

# Initialize the tile
tile.tile_init (instrnpath)

# Run the tile
cycle = 0
while (all(tile.halt_list) != 1 and cycle < param.cycles_max):
    tile.tile_run (cycle, tracepath)
    cycle = cycle + 1

# Close all the trace files
for tr_fid in tile.fid_list:
    tr_fid.close ()

print 'Finally tile halted'

dumpfile = ''
dump (tile, dumpfile)

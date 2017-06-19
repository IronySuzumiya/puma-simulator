# Test script for ima.py
# add the folder location for include files
import sys, getopt
sys.path.insert (0, '/home/ankitaay/dpe/include')
sys.path.insert (0, '/home/ankitaay/dpe/src/ima')

import numpy as np
import constants as param
import ima as ima
import ima_modules
import generate_inst

# Define a dump function which dums the all memory components into a file
def dump (ima, filename = ''):
    if (filename == ''):
        filename = 'memsim.txt'

    fid = open (filename, 'w')

    def mem_dump (memfile, name): # for conciseness
        assert (type(memfile) == list), 'memfile should be list'
        fid.write (name + ' contents\n')
        for entry in memfile:
            if (entry != ''):
                fid.write(entry + '\n')

    # dump the edram
    mem_dump (ima.mem_interface.edram.memfile, 'EDRAM')
    # dump the datamemory
    mem_dump (ima.dataMem.memfile, 'DataMemory')

    for i in range (param.num_xbar):
        # dump the xbar input memory
        mem_dump (ima.xb_inMem_list[i].memfile, 'Xbar Input Memory')
        # dump the xbar output memory
        mem_dump (ima.xb_outMem_list[i].memfile, 'Xbar Output Memory')

    fid.close()

# Initialize the ima under test
ima = ima.ima ()

# Generate the instructions
generate_inst.generate_inst ()

# Initialize the pipeline
ima.pipe_init ()

# Run the pipeline on the loaded instructions & store the trace (if applicable)
tracefile = ''
dumpfile = ''
try:
    opts, args = getopt.getopt (sys.argv[1:], 't:d:')
except getopt.GetoptError:
    print ('ima_test.py -t <tracefile> -d <dumpfile>')
    sys.exit(2)
for opt, arg in opts:
    if (opt == '-t'):
        tracefile = arg
    if (opt == '-d'):
        dumpfile = arg

ima.pipe_run (tracefile)
dump (ima, dumpfile)

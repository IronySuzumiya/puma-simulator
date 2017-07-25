# Test script for node simulations
# Currently running lstm2 on the node with 2 tiles >> 2imas >> 3 crossbars, 4*4 size
tracepath = '/home/ankitaay/dpe/test/traces/LSTM2/'
instrnpath = '/home/ankitaay/dpe/test/testasm/LSTM2/'

import sys, getopt
import torchfile as tf

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

from data_convert import *

# Define the node dump function
# Define a dump function which dums the all memory components into a file
def dump (node, filepath = ''):

    # define a dump function for a memory entity
    def mem_dump (memfile, name, tile_id = 0): # for conciseness
        assert (type(memfile) == list), 'memfile should be list'
        fid.write (name + ' contents\n')
        for addr in range(len(memfile)):
            # to print in float format
            if (memfile[addr] != ''):
                temp_val = fixed2float (memfile[addr], param.int_bits, param.frac_bits)
            else:
                temp_val = 0.0
            if (name == 'EDRAM'): # for EDRAM also show counter/valid
                fid.write ('valid: ' + str(node.tile_list[tile_id].edram_controller.valid[addr]) \
                        + ' | counter: ' + str(node.tile_list[tile_id].edram_controller.counter[addr]) + ' | ')
            fid.write(str(temp_val) + '\n')
            # to print in fixed forrmat (binary) -- use this
            #fid.write(entry + '\n')

    for i in range(len(node.tile_list)):
        print ('Dumping tile num: ', i)
        filename = filepath + 'tile' + str(i+1) + '/memsim1.txt'
        fid = open (filename, 'w')

        # dump the edram - one per tile
        mem_dump (node.tile_list[i].edram_controller.mem.memfile, 'EDRAM', i)

        # dump the memory components of IMA
        for j in range (param.num_ima):
            # dump the datamemory
            fid.write ('IMA id: ' + str(i) + '\n')
            mem_dump (node.tile_list[i].ima_list[j].dataMem.memfile, 'DataMemory')

            for k in range (param.num_xbar):
                # dump the xbar input memory
                mem_dump (node.tile_list[i].ima_list[j].xb_inMem_list[k].memfile, 'Xbar Input Memory')
                # dump the xbar output memory
                mem_dump (node.tile_list[i].ima_list[j].xb_outMem_list[k].memfile, 'Xbar Output Memory')

        fid.close()

# Instantiate the tile under test
node_dut = node.node ()

# Initialize the tile - instrnpath provides instrns for tile as well as resident imas
node_dut.node_init (instrnpath, tracepath)

# Load the matrix values onto xbars -- Both Tiles have same weights
# Note: Loaded matrix size must fit (smaller or equal) within the xbar size
lstm2_t7 = tf.load (instrnpath + 'lstm.t7')
for tile in node_dut.tile_list:
    print ('Programming tile no: ', tile.tile_id)
    i2h = lstm2_t7['i2h']
    h2h = lstm2_t7['h2h']
    for ima in tile.ima_list:
        # ima 0(2 in tile1) holds i2h
        if (ima.ima_id % 2 == 0):
            print ('Programming ima no: ', ima.ima_id)
            for i in range (3):
                xb_val = i2h[:, i*4:(i+1)*4]
                ima.xbar_list[i].program (xb_val)
        # ima 1(3 in tile 2) holds h2h
        else:
            print ('Programming ima no: ', ima.ima_id)
            for i in range (3):
                xb_val = h2h[:, i*4:(i+1)*4]
                ima.xbar_list[i].program (xb_val)

# Run the tile
cycle = 0
while (not node_dut.node_halt and cycle < param.cycles_max):
    node_dut.node_run (cycle)
    cycle = cycle + 1

    # Add things to receive buffers (tile1 and tile2) at cycle x
    if (cycle == 10):
        # Enter values for tile 0 - i_t, h_t, c_t
        tile_id = 0
        inp1 = lstm2_t7['inp1']
        for i in range (4):
            data = float2fixed (inp1[0][i].copy(), param.int_bits, param.frac_bits)
            temp_dict = {'data':data, 'neuron_id':i}
            node_dut.tile_list[tile_id].receive_buffer.write (temp_dict)

        h0 = lstm2_t7['h0']
        for i in range (3):
            data = float2fixed (h0[0][i].copy(), param.int_bits, param.frac_bits)
            temp_dict = {'data':data, 'neuron_id':i+4}
            node_dut.tile_list[tile_id].receive_buffer.write (temp_dict)

        c0 = lstm2_t7['c0']
        for i in range (3):
            data = float2fixed (c0[0][i].copy(), param.int_bits, param.frac_bits)
            temp_dict = {'data':data, 'neuron_id':i+7}
            node_dut.tile_list[tile_id].receive_buffer.write (temp_dict)

        # Enter values for tile 1 - i_t+1
        tile_id = 1
        inp2 = lstm2_t7['inp2']
        for i in range (4):
            data = float2fixed (inp2[0][i].copy(), param.int_bits, param.frac_bits)
            temp_dict = {'data':data, 'neuron_id':i}
            node_dut.tile_list[tile_id].receive_buffer.write (temp_dict)


print 'Finally node halted' + ' | PS: max_cycles ' + str (param.cycles_max)

dumpfile = ''
dump (node_dut, tracepath)

'''# Generate golden results (torch) and actual results (dpe) - write float values
tile_id = 0

filename = tracepath + 'torchsim.txt'
fid = open (filename, 'w')
fid.write ('Tile'+ str(tile_id) + ':\n')
for i in range (4): #inp1
    data = inp1[0][i].copy()
    fid.write (str(data) + '\n')
for i in range(3): #h0
    data = h0[0][i].copy()
    fid.write (str(data) + '\n')
for i in range(3): #c0
    data = c0[0][i].copy()
    fid.write (str(data) + '\n')

h1 = lstm2_t7['h1']
for i in range(3): #h1
    data = h1[0][i].copy()
    fid.write (str(data) + '\n')

c1 = lstm2_t7['c1']
for i in range(3): #c1
    data = c1[0][i].copy()
    fid.write (str(data) + '\n')
fid.close ()


filename = tracepath + 'dpesim.txt'
fid = open (filename, 'w')
fid.write ('Tile'+ str(tile_id) + ':\n')
for i in range (16):
    if (i <= 9): # 0-9
        data = node_dut.tile_list[tile_id].edram_controller.mem.memfile[i]
        data = fixed2float (data , param.int_bits, param.frac_bits)
    elif (10 <= i <= 15): # 22-24
        data = node_dut.tile_list[tile_id].edram_controller.mem.memfile[i-10+22]
        data = fixed2float (data , param.int_bits, param.frac_bits)
    fid.write (str(data) + '\n')
fid.close ()'''

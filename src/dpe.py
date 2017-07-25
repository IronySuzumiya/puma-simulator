#****************************************************************************************
# Designed by - Aayush Ankit
#               School of Elctrical and Computer Engineering
#               Nanoelectronics Research Laboratory
#               Purdue University
#               (aankit at purdue dot edu)
#
# DPEsim - Dot-Product Engine Simulator
#
# Input Tile (tile_id = 0) - has instructions to send input layer data to tiles
#       -> Dump the SEND instructions correponding to input data in this tile
#
# Output Tile (tile_id = num_tile) - has instructions to receive output data from tiles
#       -> Dump the data in EDRAM - that's your DNN output
#
# Other tiles (0 < tile_id < num_tile) - physical tiles used in computations
#****************************************************************************************


## Import constituent modeles/dependencies
import sys, getopt, os
sys.path.insert (0, '/home/ankitaay/dpe/include/')
sys.path.insert (0, '/home/ankitaay/dpe/src/')

import torchfile as tf
from data_convert import *
from node_dump import *
import numpy as np

import constants as param
import ima_modules
import ima
import tile_modules
import tile
import node_modules
import node


## Set the instruction & trace paths (create the folder hierarchy)
# Assumption: All instructions for all TILEs and IMAs have already been generated
net = 'LSTM2_new'
instrndir = '/home/ankitaay/dpe/test/testasm/' + net
tracedir = '/home/ankitaay/dpe/test/traces/' + net

assert (os.path.exists(instrndir) == 1), 'Instructions for net missing: generate intuctions (in folder hierarchy) hierarchy'
'''if not os.path.exists(instrndir):
    os.makedirs(instrndir)
    for i in range (param.num_tile):
        temp_tiledir = instrndir + '/tile' + str(i)
        os.makedirs(temp_tiledir)'''

if not os.path.exists(tracedir):
    os.makedirs(tracedir)
    for i in range (param.num_tile):
        temp_tiledir = tracedir + '/tile' + str(i)
        os.makedirs(temp_tiledir)

instrnpath = instrndir + '/'
tracepath = tracedir + '/'


## Instantiate the node under test
# A physical node consists of several logical nodes equal to the actual node size
node_dut = node.node ()


## Initialize the node with instrn & trace paths
# instrnpath provides instrns for tile & resident imas
# tracepath is where all tile & ima traces will be stored
node_dut.node_init (instrnpath, tracepath)


## Read the input data (input.t7) into the input tile's edram(controller)
inp_filename = instrnpath + 'input.t7'
inp_tileId = 0
print (os.path.exists (inp_filename))
assert (os.path.exists (inp_filename) == True), 'Input Error: Provide inputbefore running the DPE'
inp = tf.load (inp_filename)
for i in range (len(inp.data)):
    data = float2fixed (inp['data'][i], param.int_bits, param.frac_bits)
    node_dut.tile_list[inp_tileId].edram_controller.mem.memfile[i] = data
    node_dut.tile_list[inp_tileId].edram_controller.counter[i]     = int(inp['counter'][i])
    node_dut.tile_list[inp_tileId].edram_controller.valid[i]       = int(inp['valid'][i])


## Program DNN weights on the xbars
# torch table in file - (tracepath/tile<>/weights/ima<>_xbar<>.t7)
for i in range (1, param.num_tile-1):
    print ('Programming tile no: ', i)
    for j in range (param.num_ima):
        print ('Programming ima no: ', j)
        for k in range (param.num_xbar):
            wt_filename = instrnpath + 'tile' + str(i) + '/weights/' + \
                        'ima' + str(j) + '_xbar' + str(k) + '.t7'
            if (os.path.exists(wt_filename)): # check if weights for the xbar exist
                wt_temp = tf.load (wt_filename)
                node_dut.tile_list[i].ima_list[j].xbar_list[k].program (wt_temp)


## Run all the tiles
cycle = 0
while (not node_dut.node_halt and cycle < param.cycles_max):
    node_dut.node_run (cycle)
    cycle = cycle + 1
print 'Finally node halted' + ' | PS: max_cycles ' + str (param.cycles_max)


## For DEBUG only - dump the contents of all tiles
# NOTE: Output and input tiles are dummy tiles to enable self-contained simulation
if (param.debug):
    node_dump (node_dut, tracepath)


## Dump the contents of output tile to output file (output.txt)
output_file = tracepath + 'output.txt'
fid = open (output_file, 'w')
tile_id  = param.num_tile - 1
mem_dump (fid, node_dut.tile_list[tile_id].edram_controller.mem.memfile, 'EDRAM')
fid.close ()
print 'Success: Output Tile dump finished!!'


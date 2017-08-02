# Converts vgg11 to dpe ISA (tile and IMA instructions)
import sys, os
import numpy as np
import models
import torch
import math
import constants as param
sys.path.insert (0, '/home/ankitaay/dpe/include/')
sys.path.insert (0, '/home/ankitaay/dpe/src/')

# import the data_convert module (float to fixed conversions)
from data_convert import *

#*****************************************************************************************************************
## Rules to map a conv layer (for now!) - (**produces one output neuron of all outpur maps at once)
# 1. each xbar column maps a different output (no input repetition)
# 2. for output/num_output_maps (per output column) larger than xbar_size, map them across different xbars (x-axis)
# 3. for input size (reqd. for one output)larger than xbar_size, map them across multiple xbars (y-axis)
# 4. for weight precision larger than xbar bits map, the weight bits across multiple xbars (z-axis)

## Rules for xbar replication (for now!)
# 1. produce multiple output neurons  (adjacent ones from same output map) simultaneously

## Think of ways to use input sharing between strides - can lead to energy savings
# 1. Repeated within xb_inmem movements - use xb_inmem movements for computing with different strides
# 2. Muxed conenction to DAC input from xb_inmem

#*****************************************************************************************************************
# Load the DNN model
'''torch.manual_seed (1)
net = models.vgg11()

## generate vxbars from feature list in vgg11:
layer_list = [0, 3, 6, 8, 11, 13, 16, 18]
vxbar_list = []

for layer in layer_list:
    l = net.features[layer]
    kernel_size = l.kernel_size
    in_channels = l.in_channels
    out_channels = l.out_channels

    # map to a virtual xbar - each xpoint is full weight (eg: 16 bit weights)
    numIn_vxbar = in_channels * kernel_size[0] * kernel_size[1] # num of virtual inputs to xbar
    numOut_vxbar = out_channels # number of virtual outputs from xbar
    wt = l.weight.data.numpy()
    vxbar_temp = np.zeros ((numIn_vxbar, numOut_vxbar), dtype=float)
    for i in range (numOut_vxbar):
        vxbar_temp[:,i] = wt [i,:,:,:].reshape(numIn_vxbar)
    vxbar_list.append (vxbar_temp)


# Analyzed the formed vxbar(s)
print ('See size of formed virtual xbars')
for vxbar in vxbar_list:
    print (np.shape(vxbar))

#*****************************************************************************************************************
## Produce actual xbar weights file based on above xbar params (bits & size)
# each list entry is a wtfile list for one vxbar
wtfile_list = [[] for i in range(len(vxbar_list))] # A list of (list of dictionaries)

# hw parameters that will affect mapping (in terms of number of xbars needed)
wt_bits = param.num_bits # 16
xbar_bits = param.xbar_bits # 2
xbar_size = param.xbar_size # 128

for i in range (len(vxbar_list)):  # x: output, y: input, z: weight
    # axes traversal pattern: z >> x >> y
    [inp_size, out_size] = np.shape (vxbar_list[i])
    for j in range (int(math.ceil(float(out_size)/xbar_size))): # output
        for k in range (int(math.ceil(float(inp_size)/xbar_size))): # input
            col_end = min ((j+1)*xbar_size-1, out_size)
            row_end = min ((k+1)*xbar_size-1, inp_size)
            temp_wtfile  = vxbar_list[i][k*xbar_size:row_end+1, j*xbar_size:col_end+1]
            temp_wtfile_fixed  = float2fixed_2d (temp_wtfile, param.int_bits, param.frac_bits)
            for l in range (wt_bits/xbar_bits): # weight
                temp_wtfile_name = 'out' + str (j) + 'inp' + str (k) + 'wt' + str (l)
                temp_xbar_val = getBitsFromList (temp_wtfile_fixed, l*xbar_bits, xbar_bits) #matrix, start_bits, num_bits
                temp_xbar_val_float = fixed2float_2d (temp_xbar_val, param.int_bits, param.frac_bits)
                temp_dict = {'name':temp_wtfile_name, 'xbar_val':temp_xbar_val_float}
                wtfile_list[i].append(temp_dict)

# Saving to save time in processing again n again
np.save ('wtfile_list.npy', wtfile_list)

# Analyzed the formed xbar_files
wtfile_list = np.load ('wtfile_list.npy')
print ('See the number of xbar wt files (program files) generated for each feature layer')
for wtfile in wtfile_list:
    print (len(wtfile))

#*****************************************************************************************************************
## Rules for organizing xbars in tiles and ima based on num_xbar (in ima), num_ima (in tile)
# 1. Each ima maps to one layer only (even if xbars in ima remain unutilized)
# 2. Placement of xbars in imas is focussed to exploit input sharing (Other option: Output Sharing)
# 3. No xbar replication (replication can lead to improved throughput) (Other option: replicate to produce multiple
# ouputs from in an putput map in parallel)

num_xbar = 8
num_ima = 12'''

#*****************************************************************************************************************
instrnpath = '/home/ankitaay/dpe/test/testasm/vgg11'

## Generate instruction for Tile 0 (dummy tile)
temp_dir = instrnpath + '/tile0'
if not os.path.exists(instrnpath):
    os.makedirs(instrnpath)

# Generate all ima_imem.npy with halts for Tile 0
dict_temp = {}
i_temp = i_halt ()
dict_list.append (i_temp.copy())
for i in range (param.num_ima):
    filename = instrnpath + '/ima_imem' + str(i) '.npy'
    print (filename + ' generated')
    np.save(filename, dict_list)
    print ('Total no of instructions: ', len(dict_list))

# Generate tile.imem.npy
# 16 sends per in_channel (4*4 kernel)
i_temp = i_send (0, 0, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (1, 1, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (2, 2, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (3, 3, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (4, 4, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (5, 5, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (6, 6, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (7, 7, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (8, 8, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (9, 9, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (10, 10, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (11, 11, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (12, 12, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (13, 13, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (14, 14, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (15, 15, '001')
dict_list.append (i_temp.copy())

# 16 sends per in_channel (4*4 kernel)
i_temp = i_send (16, 16, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (17, 17, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (18, 18, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (19, 19, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (20, 20, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (21, 21, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (22, 22, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (23, 23, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (24, 24, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (25, 25, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (26, 26, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (27, 27, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (28, 28, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (29, 29, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (30, 30, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (31, 31, '001')
dict_list.append (i_temp.copy())

# 16 sends per in_channel (4*4 kernel)
i_temp = i_send (32, 0, '001')
dict_list.append (i_temp.copy())
i_temp = i_send 33, 1, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (34, 2, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (35, 3, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (36, 4, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (37, 5, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (38, 6, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (39, 7, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (40, 8, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (41, 9, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (10, 10, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (11, 11, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (12, 12, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (13, 13, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (14, 14, '001')
dict_list.append (i_temp.copy())
i_temp = i_send (15, 15, '001')
dict_list.append (i_temp.copy())

# Halt instruction in the end
i_temp = i_halt ()
dict_list.append (i_temp.copy())


## Generate instruction for Tile 1 (compute tile)
temp_dir = instrnpath + '/tile1'
if not os.path.exists(instrnpath):
    os.makedirs(instrnpath)

# Use 8 xbars - 1 IMA




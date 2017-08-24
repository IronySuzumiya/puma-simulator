# This example instruction generation file shows writing instructions using JMP, BEQ, stride functionality for char_rnn
# on DPE - num_layer=2, rnn_size = 128 on 2 tiles
# Tile1: Input -> rnn_layer1
# Tile2: rnn_layer1 -> rnn_layer2, rnn_layer2 -> output
# Also verfies EDRAM sharing between different IMAs
# Converts vgg11 to dpe ISA (tile and IMA instructions)
import sys, os
import numpy as np
import math

sys.path.insert (0, '/home/ankitaay/dpe/include/')
sys.path.insert (0, '/home/ankitaay/dpe/src/')
import config as cfg

# import the data_convert module (float to fixed conversions)
from data_convert import *
from instrn_proto import *
from tile_instrn_proto import *

#*******************************************Declare network constants*********************************************
instrnpath = '/home/ankitaay/dpe/test/testasm/char_rnn'
if not os.path.exists(instrnpath):
    os.makedirs(instrnpath)

num_layer = 2
in_size = 65
rnn_size = 128
out_size = 65
datamem_off = cfg.num_xbar*cfg.xbar_size

#********************************************************Tile0****************************************************
## Generate input data for Tile 0
import random
random.seed(1)
inp_path = instrnpath + '/input.npy'
num_inputs = in_size + 4*rnn_size
inp = {}
data = np.random.randn(num_inputs)
counter = np.ones (num_inputs)
valid = np.ones (num_inputs)
inp = {'data':data, 'counter': counter, 'valid':valid}
np.save (inp_path, inp)

## Generate instruction for Tile 0 (dummy tile)
temp_dir = instrnpath + '/tile0'
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Generate tile.imem.npy
dict_temp = {}
dict_list = []

# Send instruction to send input data to tile_compute_1
send_vw = 5
send_width = in_size/send_vw
i_temp = i_send (mem_addr=0, vtile_id=0, send_width=send_width, target_addr=1, vec=send_vw)
dict_list.append (i_temp.copy())

# Send instruction to prev_h & prev_c to tile_compute_1 (layer1)
send_vw = 8
send_width = rnn_size/send_vw
i_temp = i_send (mem_addr=in_size, vtile_id=0, send_width=send_width, target_addr=1, vec=send_vw)
dict_list.append (i_temp.copy())
i_temp = i_send (mem_addr=in_size+rnn_size, vtile_id=0, send_width=send_width, target_addr=1, vec=send_vw)
dict_list.append (i_temp.copy())

# Send instruction to prev_h & prev_c to tile_compute_2 (layer2)
send_vw = 8
send_width = rnn_size/send_vw
i_temp = i_send (mem_addr=in_size+2*rnn_size, vtile_id=0, send_width=send_width, target_addr=2, vec=send_vw)
dict_list.append (i_temp.copy())
i_temp = i_send (mem_addr=in_size+3*rnn_size, vtile_id=0, send_width=send_width, target_addr=2, vec=send_vw)
dict_list.append (i_temp.copy())

# Halt instruction in the end
i_temp = i_halt ()
dict_list.append (i_temp.copy())

filename = temp_dir + '/tile_imem.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))

# Generate all ima_imem.npy with halts for Tile 0
dict_temp = {}
dict_list = []
i_temp = i_hlt ()
dict_list.append (i_temp.copy())
for i in range (cfg.num_ima):
    filename = temp_dir + '/ima_imem' + str(i) + '.npy'
    print (filename + ' generated')
    np.save(filename, dict_list)
    print ('Total no of instructions: ', len(dict_list))


#********************************************************Tile1****************************************************
## Generate instruction for Tile 1 (compute tile)
temp_dir = instrnpath + '/tile1'
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Generate tile.imem.npy
dict_temp = {}
dict_list = []

# Receive in_size number of neuron data (input layer)
receive_vw = 5
receive_width = in_size/receive_vw
i_temp = i_receive (mem_addr=0, vtile_id=0, receive_width=receive_width, counter=4, vec=receive_vw)
dict_list.append (i_temp.copy())

# Receive rnn_size number of h_prev data
receive_vw = 8
receive_width = rnn_size/receive_vw
i_temp = i_receive (mem_addr=in_size, vtile_id=0, receive_width=receive_width, counter=4, vec=receive_vw)
dict_list.append (i_temp.copy())

# initiate the imas to compute
i_temp = i_compute ('1' * cfg.num_ima)
dict_list.append (i_temp.copy())

# Receive rnn_size number of c_prev data
receive_vw = 8
receive_width = rnn_size/receive_vw
i_temp = i_receive (mem_addr=in_size+rnn_size, vtile_id=0, receive_width=receive_width, counter=1, vec=receive_vw)
dict_list.append (i_temp.copy())

# Send rnn_size number of h from layer2 to Til2 (layer2)
send_vw = 8
send_width = rnn_size/send_vw
i_temp = i_send (mem_addr=in_size+5*rnn_size, vtile_id=1, send_width=send_width, target_addr=2, vec=send_vw)
dict_list.append (i_temp.copy())

# Halt instruction in the end
i_temp = i_halt ()
dict_list.append (i_temp.copy())

filename = temp_dir + '/tile_imem.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))


# Generate instruction for ima0 - first quarter of i2h & h2h [input gate]
dict_temp = {}
dict_list = []
# load input data - for 65*128 mvm operation (first 8 xbars)
i_temp = i_set (datamem_off+0, int2bin(0, 16))
dict_list.append (i_temp.copy())

load_vw = 5
load_width = in_size/load_vw
i_temp = i_load (0, datamem_off+0, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# load h_prev data - for 128*128 mvm operation (second set of 8 xbars)
i_temp = i_set (datamem_off+1, int2bin(in_size, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (cfg.xbar_size, datamem_off+1, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# mvm operation
i_temp = i_mvm (cfg.num_xbar, 0, 0) # nn.Linear()
dict_list.append (i_temp.copy())

# vector add
i_temp = i_alu ('add', datamem_off+10, 0, cfg.xbar_size, vec=cfg.xbar_size) # nn.CAddTable()
dict_list.append (i_temp.copy())

# vector sigmoid
i_temp = i_alu ('sig', datamem_off+10, datamem_off+10, vec=cfg.xbar_size) # nn.Sigmoid()
dict_list.append (i_temp.copy())

# load the in_transform value (computed by ima 3) [mem_transfer btw ima0 & ima3 use: in_size+2*rnn_size+:rnn_size]
i_temp = i_set (datamem_off+2, int2bin(in_size+2*rnn_size, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (datamem_off+10+rnn_size, datamem_off+2, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# vector multiplication
i_temp = i_alu ('mul', datamem_off+10, datamem_off+10, datamem_off+10+rnn_size, cfg.xbar_size) # nn.CMulTable() {in_gate, in_transform}
dict_list.append (i_temp.copy())

# load the c_forget value (computed by ima 1) [mem_transfer btw ima0 & ima1 use: (in_size+2*rnn_size+rnn_size)+:rnn_size]
i_temp = i_set (datamem_off+3, int2bin(in_size+2*rnn_size+rnn_size, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (datamem_off+10+rnn_size, datamem_off+3, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# vector add
i_temp = i_alu ('add', datamem_off+10, datamem_off+10, datamem_off+10+rnn_size, vec=cfg.xbar_size) #nn.CAddTable(){c_forget,c_input}
dict_list.append (i_temp.copy())

# store the output (c_next) to edram [use mem_addr- (in_size+4*rnn_size)+:rnn_size]
i_temp = i_set (datamem_off+4, int2bin(in_size+4*rnn_size, 16))
dict_list.append (i_temp.copy())

store_vw = 8
store_width = rnn_size/store_vw
i_temp = i_store (datamem_off+4, datamem_off+10, counter=1, store_width=store_width, vec=store_vw)
dict_list.append (i_temp.copy())

i_temp = i_hlt ()
dict_list.append (i_temp.copy())
filename = temp_dir + '/ima_imem' + str(0) + '.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))


# Generate instruction for ima1 - second quarter of i2h & h2h [forget gate]
dict_temp = {}
dict_list = []
# load input data - for 65*128 mvm operation (first 8 xbars)
i_temp = i_set (datamem_off+0, int2bin(0, 16))
dict_list.append (i_temp.copy())

load_vw = 5
load_width = in_size/load_vw
i_temp = i_load (0, datamem_off+0, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# load h_prev data - for 128*128 mvm operation (second set of 8 xbars)
i_temp = i_set (datamem_off+1, int2bin(in_size, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (cfg.xbar_size, datamem_off+1, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# mvm operation
i_temp = i_mvm (cfg.num_xbar, 0, 0) # nn.Linear
dict_list.append (i_temp.copy())

# vector add
i_temp = i_alu ('add', datamem_off+10, 0, cfg.xbar_size, vec=cfg.xbar_size) # nn.CAddTable
dict_list.append (i_temp.copy())

# vector sigmoid
i_temp = i_alu ('sig', datamem_off+10, datamem_off+10, cfg.xbar_size) # nn.Sigmoid()
dict_list.append (i_temp.copy())

# load prev_c (from edram) [mem_addr- in_size+rnn_size+:rnn_size]
i_temp = i_set (datamem_off+2, int2bin(in_size+rnn_size, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (datamem_off+10+rnn_size, datamem_off+2, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# vector multiplication
i_temp = i_alu ('mul', datamem_off+10, datamem_off+10, datamem_off+10+rnn_size, cfg.xbar_size) # nn.CMulTable() {f_gate, c_prev}
dict_list.append (i_temp.copy())

# store the data to edram (to be sent to ima0) [mem_transfer btw ima0 & ima1 use: (in_size+2*rnn_size+rnn_size)+:rnn_size]
i_temp = i_set (datamem_off+3, int2bin(in_size+3*rnn_size, 16))
dict_list.append (i_temp.copy())

store_vw = 8
store_width = rnn_size/store_vw
i_temp = i_store (datamem_off+3, datamem_off+10, counter=1, store_width=store_width, vec=store_vw)
dict_list.append (i_temp.copy())

i_temp = i_hlt ()
dict_list.append (i_temp.copy())
filename = temp_dir + '/ima_imem' + str(1) + '.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))


# Generate instruction for ima2 - third quarter of i2h & h2h [out_gate]
dict_temp = {}
dict_list = []
# load input data - for 65*128 mvm operation (first 8 xbars)
i_temp = i_set (datamem_off+0, int2bin(0, 16))
dict_list.append (i_temp.copy())

load_vw = 5
load_width = in_size/load_vw
i_temp = i_load (0, datamem_off+0, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# load h_prev data - for 128*128 mvm operation (second set of 8 xbars)
i_temp = i_set (datamem_off+1, int2bin(in_size, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (cfg.xbar_size, datamem_off+1, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# mvm operation
i_temp = i_mvm (cfg.num_xbar, 0, 0) # nn.Linear
dict_list.append (i_temp.copy())

# vector add
i_temp = i_alu ('add', datamem_off+10, 0, cfg.xbar_size, vec=cfg.xbar_size) # nn.CAddTable
dict_list.append (i_temp.copy())

# vector sigmoid
i_temp = i_alu ('sig', datamem_off+10, datamem_off+10, cfg.xbar_size) # nn.Sigmoid()
dict_list.append (i_temp.copy())

# load the c_next value (computed by ima 0) [mem_transfer btw edram and ima2: (in_size+4*rnn_size)+:rnn_size]
i_temp = i_set (datamem_off+2, int2bin(in_size+4*rnn_size, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (datamem_off+10+rnn_size, datamem_off+2, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# vector tanh
i_temp = i_alu ('tanh', datamem_off+10+rnn_size, datamem_off+10+rnn_size, cfg.xbar_size) # nn.Tanh()
dict_list.append (i_temp.copy())

# vector mul
i_temp = i_alu ('mul', datamem_off+10, datamem_off+10, datamem_off+10+rnn_size, cfg.xbar_size) # nn.CMulTable() {o_gate, c_transform}
dict_list.append (i_temp.copy())

# store next_h to edram [mem_transfer btw ima2 & edram use: (in_size+5*rnn_size)+:rnn_size]
i_temp = i_set (datamem_off+3, int2bin(in_size+5*rnn_size, 16))
dict_list.append (i_temp.copy())

store_vw = 8
store_width = rnn_size/store_vw
i_temp = i_store (datamem_off+3, datamem_off+10, counter=1, store_width=store_width, vec=store_vw)
dict_list.append (i_temp.copy())

i_temp = i_hlt ()
dict_list.append (i_temp.copy())
filename = temp_dir + '/ima_imem' + str(2) + '.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))


# Generate instruction for ima3 - last quater of i2h & h2h [in_transform]
dict_temp = {}
dict_list = []
# load input data - for 65*128 mvm operation (first 8 xbars)
i_temp = i_set (datamem_off+0, int2bin(0, 16))
dict_list.append (i_temp.copy())

load_vw = 5
load_width = in_size/load_vw
i_temp = i_load (0, datamem_off+0, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# load h_prev data - for 128*128 mvm operation (second set of 8 xbars)
i_temp = i_set (datamem_off+1, int2bin(in_size, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (cfg.xbar_size, datamem_off+1, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# mvm operation
i_temp = i_mvm (cfg.num_xbar, 0, 0) # nn.Linear
dict_list.append (i_temp.copy())

# vector add
i_temp = i_alu ('add', datamem_off+10, 0, cfg.xbar_size, vec=cfg.xbar_size) # nn.CAddTable
dict_list.append (i_temp.copy())

# vector tanh
i_temp = i_alu ('tanh', datamem_off+10, datamem_off+10, cfg.xbar_size) # nn.Sigmoid()
dict_list.append (i_temp.copy())

# store the in_transform value to edram (required by ima 0) [mem_transfer btw ima0 & ima3 use: in_size+2*rnn_size+:rnn_size]
i_temp = i_set (datamem_off+2, int2bin(in_size+2*rnn_size, 16))
dict_list.append (i_temp.copy())

store_vw = 8
store_width = rnn_size/store_vw
i_temp = i_store (datamem_off+2, datamem_off+10, counter=1, store_width=store_width, vec=store_vw)
dict_list.append (i_temp.copy())

i_temp = i_hlt ()
dict_list.append (i_temp.copy())
filename = temp_dir + '/ima_imem' + str(3) + '.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))


# Generate rest ima_imem.npy with halts for Tile 1
dict_temp = {}
dict_list = []
i_temp = i_hlt ()
dict_list.append (i_temp.copy())
for i in range (4, cfg.num_ima):
    filename = temp_dir + '/ima_imem' + str(i) + '.npy'
    print (filename + ' generated')
    np.save(filename, dict_list)
    print ('Total no of instructions: ', len(dict_list))


#********************************************************Tile2****************************************************
## Generate instruction for Tile 2 (compute tile)
temp_dir = instrnpath + '/tile2'
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Generate tile.imem.npy
dict_temp = {}
dict_list = []

# Receive rnn_size number of h_prev data for layer 2
receive_vw = 8
receive_width = rnn_size/receive_vw
i_temp = i_receive (mem_addr=rnn_size, vtile_id=0, receive_width=receive_width, counter=4, vec=receive_vw)
dict_list.append (i_temp.copy())

# initiate the imas to compute
i_temp = i_compute ('1' * cfg.num_ima)
dict_list.append (i_temp.copy())

# Receive rnn_size number of c_prev data for layer 2
receive_vw = 8
receive_width = rnn_size/receive_vw
i_temp = i_receive (mem_addr=2*rnn_size, vtile_id=0, receive_width=receive_width, counter=1, vec=receive_vw)
dict_list.append (i_temp.copy())

# Receive h from previous layer (input data for layer 2)
receive_vw = 8
receive_width = rnn_size/receive_vw
i_temp = i_receive (mem_addr=0, vtile_id=1, receive_width=receive_width, counter=4, vec=receive_vw)
dict_list.append (i_temp.copy())

# Halt instruction in the end
i_temp = i_halt ()
dict_list.append (i_temp.copy())

filename = temp_dir + '/tile_imem.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))


# Generate instruction for ima0 - first quarter of i2h & h2h [input gate]
dict_temp = {}
dict_list = []
# load input data - for 128*128 mvm operation (first 8 xbars)
i_temp = i_set (datamem_off+0, int2bin(0, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (0, datamem_off+0, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# load h_prev data - for 128*128 mvm operation (second set of 8 xbars)
i_temp = i_set (datamem_off+1, int2bin(rnn_size, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (cfg.xbar_size, datamem_off+1, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# mvm operation
i_temp = i_mvm (cfg.num_xbar, 0, 0) # nn.Linear()
dict_list.append (i_temp.copy())

# vector add
i_temp = i_alu ('add', datamem_off+10, 0, cfg.xbar_size, vec=cfg.xbar_size) # nn.CAddTable()
dict_list.append (i_temp.copy())

# vector sigmoid
i_temp = i_alu ('sig', datamem_off+10, datamem_off+10, vec=cfg.xbar_size) # nn.Sigmoid()
dict_list.append (i_temp.copy())

# load the in_transform value (computed by ima 3) [mem_transfer btw ima0 & ima3 use: rnn_size+2*rnn_size+:rnn_size]
i_temp = i_set (datamem_off+2, int2bin(rnn_size+2*rnn_size, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (datamem_off+10+rnn_size, datamem_off+2, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# vector multiplication
i_temp = i_alu ('mul', datamem_off+10, datamem_off+10, datamem_off+10+rnn_size, cfg.xbar_size) # nn.CMulTable() {in_gate, in_transform}
dict_list.append (i_temp.copy())

# load the c_forget value (computed by ima 1) [mem_transfer btw ima0 & ima1 use: (in_size+2*rnn_size+rnn_size)+:rnn_size]
i_temp = i_set (datamem_off+3, int2bin(rnn_size+2*rnn_size+rnn_size, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (datamem_off+10+rnn_size, datamem_off+3, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# vector add
i_temp = i_alu ('add', datamem_off+10, datamem_off+10, datamem_off+10+rnn_size, vec=cfg.xbar_size) #nn.CAddTable(){c_forget,c_input}
dict_list.append (i_temp.copy())

# store the output (c_next) to edram [use mem_addr- (in_size+4*rnn_size)+:rnn_size]
i_temp = i_set (datamem_off+4, int2bin(rnn_size+4*rnn_size, 16))
dict_list.append (i_temp.copy())

store_vw = 8
store_width = rnn_size/store_vw
i_temp = i_store (datamem_off+4, datamem_off+10, counter=1, store_width=store_width, vec=store_vw)
dict_list.append (i_temp.copy())

i_temp = i_hlt ()
dict_list.append (i_temp.copy())
filename = temp_dir + '/ima_imem' + str(0) + '.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))


# Generate instruction for ima1 - second quarter of i2h & h2h [forget gate]
dict_temp = {}
dict_list = []
# load input data - for 65*128 mvm operation (first 8 xbars)
i_temp = i_set (datamem_off+0, int2bin(0, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (0, datamem_off+0, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# load h_prev data - for 128*128 mvm operation (second set of 8 xbars)
i_temp = i_set (datamem_off+1, int2bin(rnn_size, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (cfg.xbar_size, datamem_off+1, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# mvm operation
i_temp = i_mvm (cfg.num_xbar, 0, 0) # nn.Linear
dict_list.append (i_temp.copy())

# vector add
i_temp = i_alu ('add', datamem_off+10, 0, cfg.xbar_size, vec=cfg.xbar_size) # nn.CAddTable
dict_list.append (i_temp.copy())

# vector sigmoid
i_temp = i_alu ('sig', datamem_off+10, datamem_off+10, cfg.xbar_size) # nn.Sigmoid()
dict_list.append (i_temp.copy())

# load prev_c (from edram) [mem_addr- in_size+rnn_size+:rnn_size]
i_temp = i_set (datamem_off+2, int2bin(rnn_size+rnn_size, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (datamem_off+10+rnn_size, datamem_off+2, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# vector multiplication
i_temp = i_alu ('mul', datamem_off+10, datamem_off+10, datamem_off+10+rnn_size, cfg.xbar_size) # nn.CMulTable() {f_gate, c_prev}
dict_list.append (i_temp.copy())

# store the data to edram (to be sent to ima0) [mem_transfer btw ima0 & ima1 use: (in_size+2*rnn_size+rnn_size)+:rnn_size]
i_temp = i_set (datamem_off+3, int2bin(rnn_size+3*rnn_size, 16))
dict_list.append (i_temp.copy())

store_vw = 8
store_width = rnn_size/store_vw
i_temp = i_store (datamem_off+3, datamem_off+10, counter=1, store_width=store_width, vec=store_vw)
dict_list.append (i_temp.copy())

i_temp = i_hlt ()
dict_list.append (i_temp.copy())
filename = temp_dir + '/ima_imem' + str(1) + '.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))


# Generate instruction for ima2 - third quarter of i2h & h2h [out_gate]
dict_temp = {}
dict_list = []
# load input data - for 65*128 mvm operation (first 8 xbars)
i_temp = i_set (datamem_off+0, int2bin(0, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (0, datamem_off+0, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# load h_prev data - for 128*128 mvm operation (second set of 8 xbars)
i_temp = i_set (datamem_off+1, int2bin(rnn_size, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (cfg.xbar_size, datamem_off+1, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# mvm operation
i_temp = i_mvm (cfg.num_xbar, 0, 0) # nn.Linear
dict_list.append (i_temp.copy())

# vector add
i_temp = i_alu ('add', datamem_off+10, 0, cfg.xbar_size, vec=cfg.xbar_size) # nn.CAddTable
dict_list.append (i_temp.copy())

# vector sigmoid
i_temp = i_alu ('sig', datamem_off+10, datamem_off+10, cfg.xbar_size) # nn.Sigmoid()
dict_list.append (i_temp.copy())

# load the c_next value (computed by ima 0) [mem_transfer btw edram and ima2: (in_size+4*rnn_size)+:rnn_size]
i_temp = i_set (datamem_off+2, int2bin(rnn_size+4*rnn_size, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (datamem_off+10+rnn_size, datamem_off+2, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# vector tanh
i_temp = i_alu ('tanh', datamem_off+10+rnn_size, datamem_off+10+rnn_size, cfg.xbar_size) # nn.Tanh()
dict_list.append (i_temp.copy())

# vector mul
i_temp = i_alu ('mul', datamem_off+10, datamem_off+10, datamem_off+10+rnn_size, cfg.xbar_size) # nn.CMulTable() {o_gate, c_transform}
dict_list.append (i_temp.copy())

# store next_h to edram [mem_transfer btw ima2 & edram use: (in_size+5*rnn_size)+:rnn_size]
i_temp = i_set (datamem_off+3, int2bin(rnn_size+5*rnn_size, 16))
dict_list.append (i_temp.copy())

store_vw = 8
store_width = rnn_size/store_vw
i_temp = i_store (datamem_off+3, datamem_off+10, counter=1, store_width=store_width, vec=store_vw)
dict_list.append (i_temp.copy())

i_temp = i_hlt ()
dict_list.append (i_temp.copy())
filename = temp_dir + '/ima_imem' + str(2) + '.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))


# Generate instruction for ima3 - last quater of i2h & h2h [in_transform]
dict_temp = {}
dict_list = []
# load input data - for 65*128 mvm operation (first 8 xbars)
i_temp = i_set (datamem_off+0, int2bin(0, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (0, datamem_off+0, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# load h_prev data - for 128*128 mvm operation (second set of 8 xbars)
i_temp = i_set (datamem_off+1, int2bin(rnn_size, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (cfg.xbar_size, datamem_off+1, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# mvm operation
i_temp = i_mvm (cfg.num_xbar, 0, 0) # nn.Linear
dict_list.append (i_temp.copy())

# vector add
i_temp = i_alu ('add', datamem_off+10, 0, cfg.xbar_size, vec=cfg.xbar_size) # nn.CAddTable
dict_list.append (i_temp.copy())

# vector tanh
i_temp = i_alu ('tanh', datamem_off+10, datamem_off+10, cfg.xbar_size) # nn.Sigmoid()
dict_list.append (i_temp.copy())

# store the in_transform value to edram (required by ima 0) [mem_transfer btw ima0 & ima3 use: in_size+2*rnn_size+:rnn_size]
i_temp = i_set (datamem_off+2, int2bin(rnn_size+2*rnn_size, 16))
dict_list.append (i_temp.copy())

store_vw = 8
store_width = rnn_size/store_vw
i_temp = i_store (datamem_off+2, datamem_off+10, counter=1, store_width=store_width, vec=store_vw)
dict_list.append (i_temp.copy())

i_temp = i_hlt ()
dict_list.append (i_temp.copy())
filename = temp_dir + '/ima_imem' + str(3) + '.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))


# Generate instruction for ima4 - decoder/output layer of rnn: 128*65 nn.Linear()
dict_temp = {}
dict_list = []
# load input data - for 128*128 mvm operation (first 8 xbars)
i_temp = i_set (datamem_off+0, int2bin(6*rnn_size, 16))
dict_list.append (i_temp.copy())

load_vw = 8
load_width = rnn_size/load_vw
i_temp = i_load (0, datamem_off+0, load_width=load_width, vec=load_vw)
dict_list.append (i_temp.copy())

# mvm operation
i_temp = i_mvm (cfg.num_xbar, 0, 0) # nn.Linear
dict_list.append (i_temp.copy())

# vector tanh
i_temp = i_alu ('tanh', datamem_off+10, 0, vec=cfg.xbar_size) # nn.Sigmoid()
dict_list.append (i_temp.copy())

# store the final output to edram [use: 7*rnn_size+:rnn_size]
i_temp = i_set (datamem_off+1, int2bin(8*rnn_size, 16))
dict_list.append (i_temp.copy())

store_vw = 8
store_width = rnn_size/store_vw
i_temp = i_store (datamem_off+1, datamem_off+10, counter=1, store_width=store_width, vec=store_vw)
dict_list.append (i_temp.copy())

i_temp = i_hlt ()
dict_list.append (i_temp.copy())
filename = temp_dir + '/ima_imem' + str(4) + '.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))


# Generate rest ima_imem.npy with halts for Tile 2
dict_temp = {}
dict_list = []
i_temp = i_hlt ()
dict_list.append (i_temp.copy())
for i in range (5, cfg.num_ima):
    filename = temp_dir + '/ima_imem' + str(i) + '.npy'
    print (filename + ' generated')
    np.save(filename, dict_list)
    print ('Total no of instructions: ', len(dict_list))

#********************************************************Tile3****************************************************
## Generate instruction for Tile 3 (dummy tile)
temp_dir = instrnpath + '/tile3'
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Generate tile.imem.npy
dict_temp = {}
dict_list = []

# Halt instruction in the end
i_temp = i_halt ()
dict_list.append (i_temp.copy())

filename = temp_dir + '/tile_imem.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))

# Generate all ima_imem.npy with halts for Tile 2
dict_temp = {}
dict_list = []
i_temp = i_hlt ()
dict_list.append (i_temp.copy())
for i in range (cfg.num_ima):
    filename = temp_dir + '/ima_imem' + str(i) + '.npy'
    print (filename + ' generated')
    np.save(filename, dict_list)
    print ('Total no of instructions: ', len(dict_list))

# Generates instructions that are used by ima
# add the folder location for include files
import sys
sys.path.insert (0, '/home/ankitaay/dpe/include')

import numpy as np
import constants as param

num_inst = 0 # global variable keeps track of num instructions generated

# Define nstruction prototypes
# generate load protype
def i_load (d1, addr):
    global num_inst
    i_temp = param.dummy_instrn
    i_temp['opcode'] = 'ld'
    i_temp['d1'] = d1
    i_temp['addr'] = addr
    num_inst = num_inst + 1
    return i_temp

# generate store protype
def i_store (r1, addr):
    global num_inst
    i_temp = param.dummy_instrn
    i_temp['opcode'] = 'st'
    i_temp['r1'] = r1
    i_temp['addr'] = addr
    num_inst = num_inst + 1
    return i_temp

# generate alu/alui prototype
def i_alu (aluop, d1, r1, r2 = '', imm = ''):
    global num_inst
    i_temp = param.dummy_instrn
    i_temp['opcode'] = 'alu' if (r2 != '') else 'alui'
    i_temp['aluop'] = aluop
    i_temp['d1'] = d1
    i_temp['r1'] = r1
    i_temp['r2'] = r2 # will be used in alu
    i_temp['imm'] = imm # will be used in alui
    num_inst = num_inst + 1
    return i_temp

# generate mvm prototype
def i_mvm (xb_nma = 4):
    global num_inst
    i_temp = param.dummy_instrn
    i_temp['opcode'] = 'mvm'
    i_temp['xb_nma'] = xb_nma
    num_inst = num_inst + 1
    return i_temp

# generate halt prototype
def i_halt ():
    global num_inst
    i_temp = param.dummy_instrn
    i_temp['opcode'] = 'hlt'
    num_inst = num_inst + 1
    return i_temp


instrnpath = '/home/ankitaay/dpe/test/testasm/LSTM/'
# Generate actual instructions
def generate_inst ():
    # num_instrn = param.instrnMem_size
    datamem_off = param.num_xbar * param.xbar_size # offset tells where datamem starts
    dict_list = []

    global num_inst

    # Load Input data - 4*3 Load data to xb_inMem0/1/2
    i_temp = i_load (0, 0)
    dict_list.append (i_temp.copy())
    i_temp = i_load (1, 1)
    dict_list.append (i_temp.copy())
    i_temp = i_load (2, 2)
    dict_list.append (i_temp.copy())
    i_temp = i_load (3, 3)
    dict_list.append (i_temp.copy())
    i_temp = i_load (4, 0)
    dict_list.append (i_temp.copy())
    i_temp = i_load (5, 1)
    dict_list.append (i_temp.copy())
    i_temp = i_load (6, 2)
    dict_list.append (i_temp.copy())
    i_temp = i_load (7, 3)
    dict_list.append (i_temp.copy())
    i_temp = i_load (8, 0)
    dict_list.append (i_temp.copy())
    i_temp = i_load (9, 1)
    dict_list.append (i_temp.copy())
    i_temp = i_load (10, 2)
    dict_list.append (i_temp.copy())
    i_temp = i_load (11, 3)
    dict_list.append (i_temp.copy())

    # Load Hidden State Data - 3*3 Load data to xb_inMem1 - for Hidden state data
    i_temp = i_load (12, 4)
    dict_list.append (i_temp.copy())
    i_temp = i_load (13, 5)
    dict_list.append (i_temp.copy())
    i_temp = i_load (14, 6)
    dict_list.append (i_temp.copy())
    i_temp = i_load (16, 4)
    dict_list.append (i_temp.copy())
    i_temp = i_load (17, 5)
    dict_list.append (i_temp.copy())
    i_temp = i_load (18, 6)
    dict_list.append (i_temp.copy())
    i_temp = i_load (20, 4)
    dict_list.append (i_temp.copy())
    i_temp = i_load (21, 5)
    dict_list.append (i_temp.copy())
    i_temp = i_load (22, 6)
    dict_list.append (i_temp.copy())

    # Load previous cell state into datamemory
    i_temp = i_load (datamem_off + 0, 7)
    dict_list.append (i_temp.copy())
    i_temp = i_load (datamem_off + 1, 8)
    dict_list.append (i_temp.copy())
    i_temp = i_load (datamem_off + 2, 9)
    dict_list.append (i_temp.copy())

    # mvm instrn - 6 xbars (3 for i2h, 3 for h2h)
    i_temp = i_mvm (6)
    dict_list.append (i_temp.copy())

    # 12 ALU instructions for Vector add
    i_temp = i_alu ('add', datamem_off + 3,  0,  12)
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('add', datamem_off + 4,  1,  13)
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('add', datamem_off + 5,  2,  14)
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('add', datamem_off + 6,  3,  15)
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('add', datamem_off + 7,  4,  16)
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('add', datamem_off + 8,  5,  17)
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('add', datamem_off + 9,  6,  18)
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('add', datamem_off + 10, 7,  19)
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('add', datamem_off + 11, 8,  20)
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('add', datamem_off + 12, 9,  21)
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('add', datamem_off + 13, 10, 22)
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('add', datamem_off + 14, 11, 23)
    dict_list.append (i_temp.copy())

    # 12 ALU instructions for Vector non-linearity
    # input gate
    i_temp = i_alu ('sig', datamem_off + 3,  datamem_off + 3,  '', '')
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('sig', datamem_off + 4,  datamem_off + 4,  '', '')
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('sig', datamem_off + 5,  datamem_off + 5,  '', '')
    dict_list.append (i_temp.copy())
    # forget gate
    i_temp = i_alu ('sig', datamem_off + 6,  datamem_off + 6,  '', '')
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('sig', datamem_off + 7,  datamem_off + 7,  '', '')
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('sig', datamem_off + 8,  datamem_off + 8,  '', '')
    dict_list.append (i_temp.copy())
    # output gate
    i_temp = i_alu ('sig', datamem_off + 9,  datamem_off + 9,  '', '')
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('sig', datamem_off + 10, datamem_off + 10, '', '')
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('sig', datamem_off + 11, datamem_off + 11, '', '')
    dict_list.append (i_temp.copy())
    # c_int
    i_temp = i_alu ('sig', datamem_off + 12, datamem_off + 12, '', '')
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('sig', datamem_off + 13, datamem_off + 13, '', '')
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('sig', datamem_off + 14, datamem_off + 14, '', '')
    dict_list.append (i_temp.copy())

    # 3 ALU instructions for ALU multiply - foget .* c_prev
    i_temp = i_alu ('mul', datamem_off + 0, datamem_off + 0, datamem_off + 6)
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('mul', datamem_off + 1, datamem_off + 1, datamem_off + 7)
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('mul', datamem_off + 2, datamem_off + 2, datamem_off + 8)
    dict_list.append (i_temp.copy())

    # 3 ALU instructions for ALU multiply - input .* c_int
    i_temp = i_alu ('mul', datamem_off + 3, datamem_off + 3, datamem_off + 12)
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('mul', datamem_off + 4, datamem_off + 4, datamem_off + 13)
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('mul', datamem_off + 5, datamem_off + 5, datamem_off + 14)
    dict_list.append (i_temp.copy())

    # ALU instructions for ALU add - vector ADD - c_next (one of the outputs)
    i_temp = i_alu ('mul', datamem_off + 0, datamem_off + 0, datamem_off + 0)
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('mul', datamem_off + 1, datamem_off + 1, datamem_off + 1)
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('mul', datamem_off + 2, datamem_off + 2, datamem_off + 2)
    dict_list.append (i_temp.copy())

    # ALU instructins for non-linearity
    i_temp = i_alu ('sig', datamem_off + 3, datamem_off + 0, '', '')
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('sig', datamem_off + 4, datamem_off + 1, '', '')
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('sig', datamem_off + 5, datamem_off + 2, '', '')
    dict_list.append (i_temp.copy())

    # 3 ALU instructions for ALU multiply - h_t
    i_temp = i_alu ('mul', datamem_off + 3, datamem_off + 3, datamem_off + 9)
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('mul', datamem_off + 4, datamem_off + 4, datamem_off + 10)
    dict_list.append (i_temp.copy())
    i_temp = i_alu ('mul', datamem_off + 5, datamem_off + 5, datamem_off + 11)
    dict_list.append (i_temp.copy())

    # 6 Stores - Vector store to store back the output to EDRAM
    i_temp = i_store (datamem_off + 0, 10)
    dict_list.append (i_temp.copy())
    i_temp = i_store (datamem_off + 1, 11)
    dict_list.append (i_temp.copy())
    i_temp = i_store (datamem_off + 2, 12)
    dict_list.append (i_temp.copy())
    i_temp = i_store (datamem_off + 3, 13)
    dict_list.append (i_temp.copy())
    i_temp = i_store (datamem_off + 4, 14)
    dict_list.append (i_temp.copy())
    i_temp = i_store (datamem_off + 5, 15)
    dict_list.append (i_temp.copy())

    # Add a halt instruction
    i_temp = i_halt ()
    dict_list.append (i_temp.copy())

    filename = instrnpath + 'imem.npy'
    print (filename + ' generated')
    np.save(filename, dict_list)

# Call the instruction generator
generate_inst ()

print ('Total no of instructions: ', num_inst)



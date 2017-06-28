# Generates instructions that are used by ima
# add the folder location for include files
import sys
sys.path.insert (0, '/home/ankitaay/dpe/include')

import numpy as np
import constants as param

# Define nstruction prototypes
# generate load protype
def i_load (d1, addr):
    i_temp = param.dummy_instrn
    i_temp['opcode'] = 'ld'
    i_temp['d1'] = d1
    i_temp['addr'] = addr
    return i_temp

# generate store protype
def i_store (r1, addr):
    i_temp = param.dummy_instrn
    i_temp['opcode'] = 'st'
    i_temp['r1'] = r1
    i_temp['addr'] = addr
    return i_temp

# generate alu/alui prototype
def i_alu (aluop, d1, r1, r2 = '', imm = ''):
    i_temp = param.dummy_instrn
    i_temp['opcode'] = 'alu' if (r2 != '') else 'alui'
    i_temp['aluop'] = aluop
    i_temp['d1'] = d1
    i_temp['r1'] = r1
    i_temp['r2'] = r2 # will be used in alu
    i_temp['imm'] = imm # will be used in alui
    return i_temp

# generate mvm prototype
def i_mvm (xb_nma = 4):
    i_temp = param.dummy_instrn
    i_temp['opcode'] = 'mvm'
    i_temp['xb_nma'] = xb_nma
    return i_temp

# generate halt prototype
def i_halt ():
    i_temp = param.dummy_instrn
    i_temp['opcode'] = 'hlt'
    return i_temp


# Generate actual instructions
def generate_inst ():
    # num_instrn = param.instrnMem_size
    num_instrn = 3
    datamem_off = param.num_xbar * param.xbar_size
    dict_list = []

    ## Add a load instruction
    #i_temp = i_load (datamem_off + 1, 1)
    #dict_list.append (i_temp.copy())

    ## Add a load instruction
    #i_temp = i_load (datamem_off + 2, 2)
    #dict_list.append (i_temp.copy())

    ## Add a alu instruction
    #i_temp = i_alu ('add', datamem_off + 3, datamem_off + 1, datamem_off + 2)
    #dict_list.append (i_temp.copy())

    ## Add a alui instruction
    #imm = '00001111'
    #i_temp = i_alu ('add', datamem_off + 4, datamem_off + 1, '', imm)
    #dict_list.append (i_temp.copy())

    ## Add a st instruction
    #i_temp = i_store (datamem_off + 3, 8)
    #dict_list.append (i_temp.copy())

    ## Add a st instruction
    #i_temp = i_store (datamem_off + 4, 9)
    #dict_list.append (i_temp.copy())

    ## Checking an mvm instruction
    # Load data to xb_inMem (4 loads)
    i_temp = i_load (0, 1)
    dict_list.append (i_temp.copy())
    i_temp = i_load (1, 2)
    dict_list.append (i_temp.copy())
    i_temp = i_load (2, 3)
    dict_list.append (i_temp.copy())
    i_temp = i_load (3, 4)
    dict_list.append (i_temp.copy())

    # mvm instrn
    i_temp = i_mvm (2)
    dict_list.append (i_temp.copy())

    # store data back from xbout_mem
    i_temp = i_store (0, 9)
    dict_list.append (i_temp.copy())
    i_temp = i_store (1, 10)
    dict_list.append (i_temp.copy())
    i_temp = i_store (2, 11)
    dict_list.append (i_temp.copy())
    i_temp = i_store (3, 12)
    dict_list.append (i_temp.copy())

    # Add a halt instruction
    i_temp = i_halt ()
    dict_list.append (i_temp.copy())

    filename = 'imem.npy'
    np.save(filename, dict_list)


# Define the instruction prototypes which will be used by the generate_instrn.py file
import sys
sys.path.insert (0, '/home/ankitaay/dpe/include')

import numpy as np
import constants as param

num_inst = 0 # global variable keeps track of num instructions generated

# Define nstruction prototypes
# generate load protype
def i_load (d1, addr):
    i_temp = param.dummy_instrn.copy ()
    i_temp['opcode'] = 'ld'
    i_temp['d1'] = d1
    i_temp['addr'] = addr
    return i_temp

# generate store protype
def i_store (r1, addr, counter = 1):
    i_temp = param.dummy_instrn.copy ()
    i_temp['opcode'] = 'st'
    i_temp['r1'] = r1
    i_temp['r2'] = counter
    i_temp['addr'] = addr
    return i_temp

# generate alu/alui prototype
def i_alu (aluop, d1, r1, r2 = '', imm = ''):
    i_temp = param.dummy_instrn.copy()
    i_temp['opcode'] = 'alu' if (r2 != '') else 'alui'
    i_temp['aluop'] = aluop
    i_temp['d1'] = d1
    i_temp['r1'] = r1
    i_temp['r2'] = r2 # will be used in alu
    i_temp['imm'] = imm # will be used in alui
    return i_temp

# generate mvm prototype
def i_mvm (xb_nma = 4):
    i_temp = param.dummy_instrn.copy()
    i_temp['opcode'] = 'mvm'
    i_temp['xb_nma'] = xb_nma
    return i_temp

# generate halt prototype
def i_halt ():
    i_temp = param.dummy_instrn.copy()
    i_temp['opcode'] = 'hlt'
    return i_temp


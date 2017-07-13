# Define the instruction prototypes which will be used by the generate_instrn.py file
import sys
sys.path.insert (0, '/home/ankitaay/dpe/include')

import numpy as np
import constants as param

# Define instruction prototypes
# generate compute prototype
ima_nma_dummy = '1' + (param.num_ima-1)*'0'
def i_compute (ima_nma = ima_nma_dummy):
    i_temp = param.dummy_instrn_tile.copy()
    i_temp['opcode'] = 'compute'
    i_temp['ima_nma'] = ima_nma
    return i_temp

# generate receive prototype
def i_receive (mem_addr, neuron_id, counter):
    i_temp = param.dummy_instrn_tile.copy()
    i_temp['opcode'] = 'receive'
    i_temp['mem_addr'] = mem_addr
    i_temp['neuron_id'] = neuron_id
    i_temp['r2'] = counter
    return i_temp

# generate send prototype
def i_send (mem_addr, neuron_id, target_addr):
    i_temp = param.dummy_instrn_tile.copy()
    i_temp['opcode'] = 'send'
    i_temp['mem_addr'] = mem_addr
    i_temp['neuron_id'] = neuron_id
    i_temp['r2'] = target_addr
    return i_temp

# generate halt prototype
def i_halt ():
    i_temp = param.dummy_instrn_tile.copy()
    i_temp['opcode'] = 'halt'
    return i_temp




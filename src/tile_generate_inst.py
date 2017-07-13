# Generates instructions that are used by ima
# add the folder location for include files
import sys
sys.path.insert (0, '/home/ankitaay/dpe/include')

import numpy as np
import constants as param
from tile_instrn_proto import *

instrnpath = '/home/ankitaay/dpe/test/testasm/LSTM2/'
num_inst = 0 # global variable keeps track of num instructions generated

## Instruction for Tile
dict_list = []
# 4 receive instructions - inputs to be received by IMA1
i_temp = i_receive (0, 0, 3)
dict_list.append (i_temp.copy())

i_temp = i_receive (1, 1, 3)
dict_list.append (i_temp.copy())

i_temp = i_receive (2, 2, 3)
dict_list.append (i_temp.copy())

i_temp = i_receive (3, 3, 3)
dict_list.append (i_temp.copy())

# 3 receive instructions - inputs to be received by IMA2
i_temp = i_receive (4, 4, 3)
dict_list.append (i_temp.copy())

i_temp = i_receive (5, 5, 3)
dict_list.append (i_temp.copy())

i_temp = i_receive (6, 6, 3)
dict_list.append (i_temp.copy())

# Add a tile_compute instruction
i_temp = i_compute ('1'*param.num_ima)
dict_list.append (i_temp.copy())

# Add 2 sends
i_temp = i_send (26, 32, 100)
dict_list.append (i_temp.copy())

i_temp = i_send (27, 33, 200)
dict_list.append (i_temp.copy())

# Add a halt instruction
i_temp = i_halt ()
dict_list.append (i_temp.copy())

filename = instrnpath + 'tile_imem1.npy'
print (filename + ' generated')
np.save(filename, dict_list)
print ('Total no of instructions: ', len(dict_list))

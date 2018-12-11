
import sys, os
import numpy as np
import math
sys.path.insert (0, '/home/fernando/Workspace/virtus/hp/dpe/dpe_emulate/include/')
sys.path.insert (0, '/home/fernando/Workspace/virtus/hp/dpe/dpe_emulate/src/')
from data_convert import *
from instrn_proto import *
from tile_instrn_proto import *
dict_temp = {}
dict_list = []
i_temp = i_set(d1=257, imm=128, vec=1)
dict_list.append(i_temp.copy())
i_temp = i_load(d1=257, r1=257, load_width=16, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_set(d1=385, imm=1280, vec=1)
dict_list.append(i_temp.copy())
i_temp = i_load(d1=0, r1=385, load_width=16, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_set(d1=385, imm=1408, vec=1)
dict_list.append(i_temp.copy())
i_temp = i_load(d1=128, r1=385, load_width=16, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_mvm(0b11)
dict_list.append(i_temp.copy())
i_temp = i_alu('add', d1=257, r1=257, r2=0, vec=128)
dict_list.append(i_temp.copy())
i_temp = i_alu('add', d1=257, r1=257, r2=128, vec=128)
dict_list.append(i_temp.copy())
i_temp = i_set(d1=385, imm=256, vec=1)
dict_list.append(i_temp.copy())
i_temp = i_store(d1=385, r1=257, counter=1, store_width=16, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_hlt()
dict_list.append(i_temp.copy())
filename = 'large/tile3/core_imem2.npy'
np.save(filename, dict_list)

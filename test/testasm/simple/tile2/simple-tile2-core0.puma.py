
import sys, os
import numpy as np
import math
sys.path.insert (0, '/home/glau/puma/training-emul-comp/dpe_emulate/include/')
sys.path.insert (0, '/home/glau/puma/training-emul-comp/dpe_emulate/src/')
from data_convert import *
from instrn_proto import *
from tile_instrn_proto import *
dict_temp = {}
dict_list = []
i_temp = i_set(d1=257, imm=0, vec=1)
dict_list.append(i_temp.copy())
i_temp = i_load(d1=0, r1=257, load_width=5, vec=1)
dict_list.append(i_temp.copy())
i_temp = i_mvm('100001')
dict_list.append(i_temp.copy())
i_temp = i_set(d1=257, imm=5, vec=1)
dict_list.append(i_temp.copy())
i_temp = i_store(d1=257, r1=0, counter=1, store_width=5, vec=1)
dict_list.append(i_temp.copy())
i_temp = i_hlt()
dict_list.append(i_temp.copy())
filename = 'simple/tile2/core_imem0.npy'
np.save(filename, dict_list)

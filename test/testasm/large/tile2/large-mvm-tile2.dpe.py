
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
i_temp = i_receive(mem_addr=768, vtile_id=0, receive_width=16, counter=2, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=896, vtile_id=0, receive_width=16, counter=2, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1024, vtile_id=0, receive_width=16, counter=2, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1152, vtile_id=0, receive_width=16, counter=2, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1280, vtile_id=0, receive_width=16, counter=2, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1408, vtile_id=0, receive_width=16, counter=2, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1536, vtile_id=0, receive_width=16, counter=2, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_receive(mem_addr=1664, vtile_id=0, receive_width=16, counter=2, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1920, vtile_id=2, send_width=16, target_addr=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_send(mem_addr=1792, vtile_id=2, send_width=16, target_addr=1, vec=8)
dict_list.append(i_temp.copy())
i_temp = i_halt()
dict_list.append(i_temp.copy())
filename = 'large/tile2/tile_imem.npy'
np.save(filename, dict_list)

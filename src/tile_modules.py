# Defines all the components needed by a tile
# IMA, EDRAM, EDRAM controller

import sys
sys.path.insert (0, '/home/ankitaay/dpe/include')
sys.path.insert (0, '/home/ankitaay/dpe/src/ima')
import constants as param
import ima_modules
from ima_modules import int2bin


# a memory instance for edram
class edram (ima_modules.memory):

    def getLatency (self):
        return param.edram_lat

    # redefine the write assertion
    def write (self, addr, data):
        assert (type(addr) == int), 'addr type should be int'
        assert (self.addr_start <= addr <= self.addr_end), 'addr exceeds the memory bounds'
        print ('EDRAM data width', len(data))
        assert ((type(data) ==  str) and (len(data) == param.edram_buswidth)), 'data should be a string with edram_datawidth bits'
        self.memfile[addr - self.addr_start] = data


# edram controller includes edram too
class edram_controller (object):
    def __init__ (self):

        # Intialize EDRAM
        self.mem  = edram (param.edram_size)
        for i in range (len(self.mem.memfile)/2):
            val = int2bin (i, param.data_width)
            self.mem.memfile[i] = val

        # Define latency
        self.latency = param.edram_lat

        # Last served IMA
        self.lastIdx = -1

    def getLatency (self):
        return self.latency

    # Based on the arbitration logic, decide which ima will be served
    def find_next (self, ren_list, wen_list):
        if (len(ren_list) > 1):
            if ((1 in ren_list[self.lastIdx+1:]) or (1 in wen_list[self.lastIdx+1:])):
                idx1 = ren_list[self.lastIdx+1:].index(1)
                idx2 = wen_list[self.lastIdx+1:].index(1)
                return min (idx1, idx2)
            else:
                idx1 = ren_list[0:lastIdx+1].index(1)
                idx2 = wen_list[0:lastIdx+1].index(1)
                return min (idx1, idx2)
        else: # for one IMA case only
            return 0

    def propagate (self, ren_list, wen_list, ramstore_list, addr_list):
        # check if any wen or ren siganl is active
        assert (any(ren_list) or any(wen_list)), 'atleast one memory access should be present'

        # choose the ima to be served
        idx = self.find_next (ren_list, wen_list)
        self.lastIdx = idx # update last index

        # based on ren and wen perfrom the required action
        assert ((ren_list[idx] ^ wen_list[idx]) == 1), 'Ram Access Error: both ren and wen cannot be same'

        if (ren_list[idx] == 1):
            ramload = self.mem.read (addr_list[idx])
            return [idx, ramload]
        else:
            self.mem.write (addr_list[idx], ramstore_list[idx])
            return [idx, '']









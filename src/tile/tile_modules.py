# Defines all the components needed by a tile
# IMA, EDRAM, EDRAM controller

import sys
sys.path.insert (0, '/home/ankitaay/dpe/include')
sys.path.insert (0, '/home/ankitaay/dpe/src/ima')
import constants
import ima_modules

class edram (ima_modules.memory):

    # redefine the write assertion
    def write (self, addr, data):
        assert (type(addr) == int), 'addr type should be int'
        assert (self.addr_start <= addr <= self.addr_end), 'addr exceeds the memory bounds'
        #print 'length of data ' + str(len(data))
        assert ((type(data) ==  str) and (len(data) == constants.edram_buswidth)), 'data should be a string with edram_datawidth bits'
        self.memfile[addr - self.addr_start] = data

class edram_controller (object):
    def __init__ (self):

        # Intialize EDRAM
        self.mem  = edram (param.edram_size)

        # Define latency
        self.latency = param.edram_lat

        # Last served IMA
        self.lastIdx = 0

    def getLatency (self):
        return self.latency

    def find_next (self, ren_list, wen_list):
        if ((1 in ren_list[self.lastIdx:]) or (1 in wen_list[self.lastIdx:])):
            idx1 = ren_list[self.lastIdx:].index(1)
            idx2 = wen_list[self.lastIdx:].index(1)
            return min (idx1, idx2)
        else:
            idx1 = ren_list[0:lastIdx+1].index(1)
            idx2 = wen_list[0:lastIdx+1].index(1)
            return min (idx1, idx2i)

    def propagate (self, ren_list, wen_list, ramstore_list, addr_list):
        # choose the ima to be served
        idx = self.find_next (ren_list, wen_list)

        # based on ren and wen perfrom the required action
        assert ((ren_list[idx] ^ wen_list[idx]) == 1), 'Ram Access Error: both ren and wen cannot be same

        wait_list = [1] * param.num_ima
        wait_list[idx] = 0

        if (ren_list[idx] == 1):
            ramload = self.mem.read (addr_list[idx])
            return [wait_list, ramload]
        else:
            self.mem.write (addr_list[idx], ramstore_list[idx])
            return wait_list









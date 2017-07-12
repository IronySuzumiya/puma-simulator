# Defines all the components needed by a tile
# IMA, EDRAM, EDRAM controller

import sys
sys.path.insert (0, '/home/ankitaay/dpe/include')
sys.path.insert (0, '/home/ankitaay/dpe/src/ima')
import constants as param
import ima_modules
from ima_modules import int2bin

# function to check keys match between two dictionaries
def dict_match (dict1, dict2):
    for keyone in dict1.keys():
        if keyone not in dict2.keys():
            return 0
    return 1

# an instruction memory to store the tile instructions
class instrn_memory (ima_modules.memory):
    def write (self, addr, data):
        assert (type(addr) == int), 'addr type should be int'
        assert (self.addr_start <= addr <= self.addr_end), 'addr exceeds the memory bounds'
        assert ((dict_match(data, param.dummy_instrn_tile) == 1) and (len(data) == constants.data_width)), 'data should be a string with mem_width bits'
        self.memfile[addr - self.addr_start] = data

# adding a receive buffer (full-assoc cache (tag = neuron_id)) to enable non-blocking receives
class receive_buffer (object):
    def __init__ (self, buff_size):
         # Consists of a list of dictionaries (data, neuron_id)
         temp_dict = {'data': '', 'neuron_id': 0, 'valid': 0}
         self.buffer = [temp_dict] * buff_size
         self.rd_ptr = 0
         self.wr_ptr = 0

    # invalidates all entries
    def inv (self):
        for temp_dict in self.buffer:
            temp_dict['valid'] = 0

    # checks if buffer is empty
    def isempty (self):
        for idx in range(len(self.buffer)):
            temp_dict = self.buffer[idx]
            if (temp_dict['valid']):
                return 0
        return 1

    # checks if buffer is full
    def isfull (self):
        for idx in range(len(self.buffer)):
            temp_dict = self.buffer[idx]
            if (not temp_dict['valid']):
                return [0, idx]
        return [1, idx]

    # write the data coming from router to buffer if non-full
    def write (self, dict_entry):
        [valid, idx] = self.isfull ()
        assert (not valid), 'Receive buffer full - fails to receive data'
        self.buffer[idx]['data'] = dict_entry['data']
        self.buffer[idx]['neuron_id'] = dict_entry['neuron_id']
        self.buffer[idx]['valid'] = 1

    # read the value from buffer if tag matches - else stall receive instruction
    def read (self, neuron_id):
        if (not self.isempty()):
            for idx in range(len(self.buffer)):
                temp_dict = self.buffer[idx]
                if (temp_dict['neuron_id'] == neuron_id):
                    temp_dict['valid'] = 0
                    return [1, temp_dict['data']]
        return [0, 0] # tag-hit, data

# a memory instance for edram
class edram (ima_modules.memory):

    def getLatency (self):
        return param.edram_lat

    # redefine the write assertion
    def write (self, addr, data):
        assert (type(addr) == int), 'addr type should be int'
        assert (self.addr_start <= addr <= self.addr_end), 'addr exceeds the memory bounds'
        assert ((type(data) ==  str) and (len(data) == param.edram_buswidth)), 'data should be a string with edram_datawidth bits'
        self.memfile[addr - self.addr_start] = data


# edram controller includes edram too
class edram_controller (object):
    def __init__ (self):

        # Instantiate EDRAM, valid and counter fields
        self.mem  = edram (param.edram_size)
        self.valid = [0] * param.edram_size
        self.counter = [0] * param.edram_size

        # Intialize EDRAM & other fields
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
                idx1 = ren_list[self.lastIdx+1:].index(1) if any(ren_list[self.lastIdx+1:]) else param.infinity
                idx2 = wen_list[self.lastIdx+1:].index(1) if any(wen_list[self.lastIdx+1:]) else param.infinity
                return (self.lastIdx+1) + min (idx1, idx2)
            else:
                idx1 = ren_list[0:self.lastIdx+1].index(1) if any(ren_list[0:self.lastIdx+1]) else param.infinity
                idx2 = wen_list[0:self.lastIdx+1].index(1) if any(wen_list[0:self.lastIdx+1]) else param.infinity
                return min (idx1, idx2)
        else: # for one IMA case only
            return 0

    def propagate (self, ren_list, wen_list, ramstore_list, addr_list):
        # check if any wen or ren siganl is active
        assert (any(ren_list) or any(wen_list)), 'atleast one memory access should be present'

        # Traverse the WEN(s) and REN(s) to find the ima to be served
        found = 0
        count = 0
        while (found == 0 and count < param.num_ima):
            count = count + 1
            # choose the ima to be served
            idx = self.find_next (ren_list, wen_list)
            assert (idx < param.num_ima), 'Find Error: IMA Index not possible'
            self.lastIdx = idx # update last index

            # based on ren and wen perfrom the required action
            assert ((ren_list[idx] ^ wen_list[idx]) == 1), 'Ram Access Error: both ren and wen cannot be same'

            # Check for valid (invalid) for LD (ST)
            if ((self.valid[addr_list[idx]] and ren_list[idx]) or \
                    ((not self.valid[addr_list[idx]]) and wen_list[idx])):
                found = 1

        # Once idx found complete ren/wen operation
        addr = addr_list[idx]
        if (ren_list[idx] == 1): # LD instrcution
            if (found): # change state only if an idx was found
                # update the counter & valid flags accordingly
                self.counter[addr] = self.counter[addr] - 1
                if (self.counter[addr] == 0):
                    self.valid[addr] = 0
            # read the data and send to ima - if found is 0, ramload is junk
            ramload = self.mem.read (addr_list[idx])
            return [found, idx, ramload]

        else: # ST instruction
            if (found): # change state only if an idx was found
                data = ramstore_list[idx][-1*param.data_width:]
                counter = ramstore_list[idx][0:-1*param.data_width]
                self.mem.write (addr_list[idx], data)
                self.valid[addr] = 1
                self.counter[addr] = int(counter)
            return [found, idx, '']


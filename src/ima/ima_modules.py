# Defining all modules within an ima and its methods (Propagate and or Update)
# 'Propagate' is the combinational part evaluation
# 'Update' - (NOT BEING USED CURRENTLY!) is the flip fop evaluation (for clocked elements of the circuit only)

import numpy as np
import constants


class xbar (object):
    def __init__ (self, xbar_size, xbar_value = 'nil'):
        # xbar_value is the weights meant for one crossbar
        self.xbar_size = xbar_size
        self.xbar_value = np.zeros((xbar_size, xbar_size), dtype=float)
        # unprogrammed xbar contains zeros
        if (xbar_value != 'nil'):
            self.xbar_value = xbar_value

    def propagate (self, inp = 'nil'):
        assert (inp != 'nil'), 'propagate needs a non-nil input'
        assert (len(inp) == self.xbar_size), 'xbar input size mismatch'
        return np.dot(inp, self.xbar_value)


class dac (object):
    def __init__ (self, dac_res):
       self.dac_res = dac_res

    def bin2real (self, inp, num_bits):
        # gets a n-bit (n = dac_res) digital value & returns an analog voltage value
        inp_max = '1' * num_bits # string with all 1s
        analog_max = constants.vdd
        frac = int(inp, 2) / float(int(inp_max, 2))
        return analog_max * frac

    def propagate (self, inp):
        assert ((type(inp) == str) and (len(inp) == self.dac_res)), 'dac input type/size (bits) mismatch (string expected)'
        num_bits = self.dac_res
        return self.bin2real (inp, num_bits)


# A dac_array is an arrays of DACs private to a xbar
class dac_array (object):
    def __init__ (self, xbar_size, dac_res):
        # generate multiple dacs (one per xbar input)
        self.dac_list = []
        self.xbar_size = xbar_size
        for i in xrange(xbar_size):
            temp_dac = dac (dac_res)
            self.dac_list.append(temp_dac)

    def propagate (self, inp_list):
        assert (len(inp_list) == self.xbar_size), 'dac_array input list size mismatch'
        out_list = []
        for i in xrange(self.xbar_size):
            temp_out = self.dac_list[i].propagate(inp_list[i])
            out_list.append(temp_out)
        return out_list


# Probably - also doing the sampling part of (sampel and hold) inside
class adc (object):
    def __init__ (self, adc_res):
        self.adc_res = adc_res

    def real2bin (self, inp, num_bits):
        num_levels = 2**num_bits
        step = float((constants.xbar_out_max - constants.xbar_out_min)) / num_levels
        int_value = int(np.ceil((inp - constants.xbar_out_min) / float(step)))
        bin_value = bin(int_value - 1)[2:]
        return ('0'*(num_bits - len(bin_value)) + bin_value)

    def propagate (self, inp):
        assert (type(inp) == float), 'adc input type mismatch (float expected)'
        num_bits = self.adc_res
        return self.real2bin (inp, num_bits)


# Doesn't replicate the exact (sample and hold) functionality (just does hold)
class sampleNhold (object):
    def __init__ (self, xbar_size):
        self.hold_latch = np.zeros(xbar_size)

    def propagate (self, inp_list):
        assert (len(inp_list) == len(self.hold_latch)), 'sample&hold input size mismatch'
        for i in xrange(len(inp_lisaddrt)):
            self.hold_latch[i] = inp_list[i]
        return self.hold_latch


class mux (object):
    def __init__ (self, num_in):
        # num_in is the inputs for the multiplexer
        self.num_in = num_in

    def propagate (self, inp_list, sel):
        assert (len(inp_list) == self.num_in), 'Mux input list size mismatch'
        assert ((type(sel) == int) & (-1 < sel < self.num_in)), 'Mux select input size/type error'
        return inp_list[sel]


#### Needs some change - add function op (for instance, shift bits for shift)
class alu (object):
    def __init__ (self):
        def add (a, b): return (a + b)
        def sub (a, b): return (a - b)
        def shift_add (a, b): return (a + (b << 1))
        self.options = {'add' : add, 'sub' : sub, 'shift_add' : shift_add}

    def propagate (self, a, b, aluop):
        assert ((type(aluop) == str) and (aluop in self.options.keys())), 'Invalid alu_op'
        out = self.options[aluop](a, b)
        return out


# Assumes a half-word oriented memory (each entry - 16 bits)
class memory (object):
    def __init__ (self, size):
        # memfile will store half-word (16 bits digital data) length strings
        self.size = size
        self.memfile = [''] * size
        self.addr_start = constants.xbar_size + 1
        self.addr_end = self.addr_start + self.size

    def read (self, addr):
        assert (type(addr) == int), 'addr type should be int'
        assert (self.addr_start < addr < self.addr_end), 'addr exceeds the memory bounds'
        return self.memfile[addr]

    def write (self, addr, data):
        assert (type(addr) == int), 'addr type should be int'
        assert (self.addr_start < addr < self.addr_end), 'addr exceeds the memory bounds'
        assert ((type(data) ==  str) and (len(data) == constants.data_width)), 'data should be a string with less than or equal to mem_width bits'
        self.memfile[addr] = data
        return 1

    def reset (self):
        self.memfile = [''] * self.size


# xbar input memory reads differently than typical memory
# Each read is a shift and read operation
class xb_inMem (object):
    def __init__ (self, xbar_size):
        # size equals the xbar_size, each entry being to
        self.xbar_size = xbar_size
        self.memfile = [''] * self.xbar_size

    # reads & shifts all entries in parallel
    def read (self):
        out_list = []
        for i in xrange(self.xbar_size):
            value = self.memfile[i]
            self.memfile[i] = value[:start_idx]
            out_list.append(value)
        return out_list

    def write (self, addr, data):
        assert (type(addr) == int), 'addr type should be int'
        assert (-1 < addr < self.size), 'addr exceeds the memory bounds'
        assert ((type(data) ==  str) and (len(data) == constants.xbdata_width)), 'data should be a string with less than or equal to mem_width bits'
        self.memfile[addr] = data
        return 1

    def reset (self):
        self.memfile = [''] * self.xbar_size


# xbar output memory
class xb_outMem (xb_inMem):
    def __init__ (self, xbar_size):
        # size equals the xbar_size, each entry being to
        self.xbar_size = xbar_size
        self.memfile = [''] * self.xbar_size
        self.wr_pointer = 0

    def read (self, addr):
        assert (type(addr) == int), 'addr type should be int'
        assert (-1 < addr < self.size), 'addr exceeds the memory bounds'
        return self.memfile[addr]

    def write (self, data):
        self.memfile[self.wr_pointer] = data

    def reset (self):
        self.memfile = [''] * self.xbar_size
        self.wr_pointer = 0


# Instruction memory stores dict unlike memory (string)
class instrn_memory (memory):
    def write (self, addr, data):
        assert (type(addr) == int), 'addr type should be int'
        assert (-1 < addr < self.size), 'addr exceeds the memory bounds'
        assert (type(data) == dict), 'instrn should of type dictionary'
        self.memfile[addr] = data
        return 1


# Memory interface to interact with an external memory
class mem_interface (object):
    def __init__ (self):
        self.wait = 0 # 0 represents wait state
        self.addr = 0
        self.data = 0

    def request (self):
        self.wait = 0

    def ack (self):
        self.wait = 1


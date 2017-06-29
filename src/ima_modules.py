# Defining all modules within an ima and its methods (Propagate and or Update)
# Also define sime support functions (commonly used)
# 'Propagate' is the combinational part evaluation
# 'Update' - (NOT BEING USED CURRENTLY!) is the flip fop evaluation (for clocked elements of the circuit only)

import sys
sys.path.insert (0, '/home/ankitaay/dpe/include')

import numpy as np
import constants
import math

# Convert int to binary of specified bits
def int2bin (inp, bits):
    out = bin(inp)[2:]
    return ((bits-len(out))*'0' + out)


class xbar (object):
    def __init__ (self, xbar_size, xbar_value = 'nil'):
        # define latency
        self.latency = constants.xbar_lat

        # xbar_value is the weights meant for one crossbar
        self.xbar_size = xbar_size
        self.xbar_value = np.ones((xbar_size, xbar_size), dtype=float)
        # unprogrammed xbar contains zeros
        if (xbar_value != 'nil'):
            self.xbar_value = xbar_value

    def getLatency (self):
        return self.latency

    def propagate (self, inp = 'nil'):
        assert (inp != 'nil'), 'propagate needs a non-nil input'
        assert (len(inp) == self.xbar_size), 'xbar input size mismatch'
        return np.dot(inp, self.xbar_value)


class dac (object):
    def __init__ (self, dac_res):
        # define latency
        self.latency = constants.dac_lat

        self.dac_res = dac_res

    def getLatency (self):
        return self.latency

    def bin2real (self, inp, num_bits):
        # gets a n-bit (n = dac_res) digital value & returns an analog voltage value
        inp_max = '1' * num_bits # string with all 1s
        analog_max = constants.vdd
        frac = int(inp, 2) / float(int(inp_max, 2))
        return analog_max * frac

    def propagate (self, inp):
        if (inp == ''):
            inp = '0' * constants.dac_res
        assert ((type(inp) == str) and (len(inp) == self.dac_res)), 'dac input type/size (bits) mismatch (string expected)'
        num_bits = self.dac_res
        return self.bin2real (inp, num_bits)


# A dac_array is an arrays of DACs private to a xbar
class dac_array (object):
    def __init__ (self, xbar_size, dac_res):
        # define latency
        self.latency = constants.dac_lat

        # generate multiple dacs (one per xbar input)
        self.dac_list = []
        self.xbar_size = xbar_size
        for i in xrange(xbar_size):
            temp_dac = dac (dac_res)
            self.dac_list.append(temp_dac)

    def getLatency (self):
        return self.latency

    def propagate (self, inp_list):
        assert (len(inp_list) == self.xbar_size), 'dac_array input list size mismatch'
        out_list = []
        for i in xrange(self.xbar_size):
            temp_out = self.dac_list[i].propagate(inp_list[i])
            out_list.append(temp_out)
        return out_list


# Probably - also doing the sampling part of (sample and hold) inside
class adc (object):
    def __init__ (self, adc_res):
        # define latency
        self.latency = constants.adc_lat

        self.adc_res = adc_res

    def getLatency (self):
        return self.latency

    def real2bin (self, inp, num_bits):
        num_levels = 2**num_bits
        step = float((constants.xbar_out_max - constants.xbar_out_min)) / num_levels
        int_value = int(np.ceil((inp - constants.xbar_out_min) / float(step)))
        bin_value = bin(int_value - 1)[2:]
        return ('0'*(num_bits - len(bin_value)) + bin_value)

    def propagate (self, inp):
        assert (type(inp) in [float, np.float32, np.float64]), 'adc input type mismatch (float, np.float32, np.float64 expected)'
        num_bits = self.adc_res
        return self.real2bin (inp, num_bits)


# Doesn't replicate the exact (sample and hold) functionality (just does hold)
class sampleNhold (object):
    def __init__ (self, xbar_size):
        # define latency
        self.latency = constants.snh_lat

        self.hold_latch = np.zeros(xbar_size)

    def getLatency (self):
        return self.latency

    def propagate (self, inp_list):
        assert (len(inp_list) == len(self.hold_latch)), 'sample&hold input size mismatch'
        for i in xrange(len(inp_list)):
            self.hold_latch[i] = inp_list[i]
        return self.hold_latch


class mux (object):
    def __init__ (self, num_in):
        # define latency
        self.latency = constants.mux_lat

        # num_in is the inputs for the multiplexer
        self.num_in = num_in

    def getLatency (self):
        return self.latency

    def propagate (self, inp_list, sel):
        assert (len(inp_list) == self.num_in), 'Mux input list size mismatch'
        assert ((type(sel) == int) & (-1 < sel < self.num_in)), 'Mux select input size/type error'
        return inp_list[sel]


#### Needs some change - add function op (for instance, shift bits for shift)
class alu (object):
    def __init__ (self):
        # define latency
        self.latency = constants.alu_lat

        def add (a, b, c): return (a + b)
        def sub (a, b, c): return (a - b)
        def shift_add (a, b, c): return (a + (b << c))
        def multiply (a, b, c): return (a * b)
        def sigmoid (a, b, c): return a # A pass through unti for now
        self.options = {'add' : add, 'sub' : sub, 'sna' : shift_add, 'mul': multiply, 'sig': sigmoid}

    def getLatency (self):
        return self.latency

    def propagate (self, a, b, aluop, c = 0): # c can be shift operand for sna operation (add others later)
        assert ((type(aluop) == str) and (aluop in self.options.keys())), 'Invalid alu_op'
        a = int (a, 2)
        b = int (b, 2) if (b != '') else 0
        out = self.options[aluop] (a, b, c)
        out = bin(out)[2:]
        #assert (len(out) <= constants.data_width), 'ALU Overflow error'
        if (len(out) > constants.data_width):
            out = '1'*constants.data_width
            print ('ALU Overflow Exception, allowed to run')
        return ((constants.data_width - len(out))*'0' + out)


# Assumes a half-word oriented memory (each entry - 16 bits)
class memory (object):
    def __init__ (self, size, addr_offset = 0):
        # define latency
        self.latency = constants.mem_lat

        # memfile will store half-word (16 bits digital data) length strings
        self.size = size
        self.memfile = [''] * size
        self.addr_start = addr_offset
        self.addr_end = self.addr_start + self.size -1

    def getLatency (self):
        return self.latency

    def read (self, addr):
        assert (type(addr) == int), 'addr type should be int'
        assert (self.addr_start <= addr <= self.addr_end), 'addr exceeds the memory bounds'
        return self.memfile[addr - self.addr_start]

    def write (self, addr, data):
        assert (type(addr) == int), 'addr type should be int'
        assert (self.addr_start <= addr <= self.addr_end), 'addr exceeds the memory bounds'
        #print 'length of data ' + str(len(data))
        assert ((type(data) ==  str) and (len(data) == constants.data_width)), 'data should be a string with mem_width bits'
        self.memfile[addr - self.addr_start] = data

    def reset (self):
        self.memfile = [''] * self.size


# xbar input memory reads differently than typical memory
# Each read is a shift and read operation
class xb_inMem (object):
    def __init__ (self, xbar_size):
        # define latency
        self.latency = constants.mem_lat

        # size equals the xbar_size, each entry being to
        self.xbar_size = xbar_size
        self.memfile = [''] * self.xbar_size

    def getLatency (self):
        return self.latency

    # reads & shifts all entries in parallel
    def read (self, num_bits):
        out_list = []
        for i in xrange(self.xbar_size):
            value = self.memfile[i]
            #self.memfile[i] = '0'*num_bits + value[:-1*num_bits]
            self.memfile[i] = value[-1*num_bits:] + value[:-1*num_bits]
            out_list.append(value[-1*num_bits:])
        return out_list

    def write (self, addr, data):
        assert (type(addr) == int), 'addr type should be int'
        assert (-1 < addr < self.xbar_size), 'addr exceeds the memory bounds'
        assert ((type(data) ==  str) and (len(data) == constants.xbdata_width)), 'data should be a string with xbdata_width bits'
        self.memfile[addr] = data

    def reset (self):
        self.memfile = [''] * self.xbar_size


# xbar output memory
class xb_outMem (xb_inMem):
    def __init__ (self, xbar_size):
        # define latency
        self.latency = constants.mem_lat

        # size equals the xbar_size, each entry being to
        self.xbar_size = xbar_size
        self.memfile = ['0' * constants.xbdata_width] * self.xbar_size
        self.wr_pointer = 0

    def getLatency (self):
        return self.latency

    def read (self, addr):
        assert (type(addr) == int), 'addr type should be int'
        assert (-1 < addr < self.xbar_size), 'addr exceeds the memory bounds'
        return self.memfile[addr]

    def write (self, data):
        assert ((type(data) ==  str) and (len(data) == constants.xbdata_width)), 'data should be a string with xbdata_width bits'
        self.memfile[self.wr_pointer] = data
        self.wr_pointer = self.wr_pointer + 1

    def restart (self):
        self.wr_pointer = 0

    def reset (self):
        self.memfile = ['0' * constants.xbdata_width] * self.xbar_size
        self.wr_pointer = 0


# Instruction memory stores dict unlike memory (string)
class instrn_memory (memory):
    # To initilzie the memory with instructions
    def load (self, dict_list):
        assert (len(dict_list) <= self.size), 'instructions exceed the instruction memory size'
        for i in xrange(len(dict_list)):
            self.memfile[i] = dict_list[i]

    def read (self, addr):
        assert (type(addr) == int), 'addr type should be int'
        # assert (-1 < addr < self.size), 'addr exceeds the memory bounds'
        if (-1 < addr < self.size):
            return self.memfile[addr]
        else:
            return self.memfile[len(memfile)]

    def write (self, addr, data):
        assert (type(addr) == int), 'addr type should be int'
        assert (-1 < addr < self.size), 'addr exceeds the memory bounds'
        assert (type(data) == dict), 'instrn should of type dictionary'
        self.memfile[addr] = data
        return 1


# Memory interface to interact with an external memory
class mem_interface (object):
    def __init__ (self):
        # define latency
        self.latency = constants.memInterface_lat

        # in/out ports
        self.wait = 0  # wait signal from (EDRAM) controller to ima
        self.ren = 0  # ren = 1, for LD
        self.wen = 0  # wen = 1, for ST
        self.addr = 0 # add sent by ima to mem controller
        self.ramload = 0 # data (for LD) sent by edram to ima
        self.ramstore = 0 # data (for ST) sent by ima to men controller

        ## For DEBUG of IMA only - define a memory element and preload some values
        #self.edram = memory (constants.dataMem_size, 0)
        #for i in range (len(self.edram.memfile)/2):
        #    val = int2bin (i, constants.data_width)
        #    self.edram.memfile[i] = val

    def getLatency (self):
        return self.latency

    def wrRequest (self, addr, ramstore):
        assert (type(ramstore) == str), 'data type expected string'
        self.wen = 1
        self.ren = 0
        self.addr = addr
        self.ramstore = ramstore
        self.wait = 1

        ## For DEBUG of IMA only
        #self.edram.memfile[addr] = ramstore

    def rdRequest (self, addr):
        self.ren = 1
        self.wen = 0
        self.addr = addr
        self.wait = 1

        ## For DEBUG of IMA only
        #self.ramload = self.edram.memfile[addr]



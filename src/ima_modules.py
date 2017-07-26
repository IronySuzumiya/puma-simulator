# Defining all modules within an ima and its methods (Propagate and or Update)
# Also define sime support functions (commonly used)
# 'Propagate' is the combinational part evaluation
# 'Update' - (NOT BEING USED CURRENTLY!) is the flip fop evaluation (for clocked elements of the circuit only)

import sys
sys.path.insert (0, '/home/ankitaay/dpe/include')

import numpy as np
import constants
import math
from data_convert import *


class xbar (object):
    def __init__ (self, xbar_size, xbar_value = 'nil'):
        # define num_access
        self.num_access = 0

        # define latency
        self.latency = constants.xbar_lat

        # xbar_value is the weights meant for one crossbar
        self.xbar_size = xbar_size
        self.xbar_value = np.ones((xbar_size, xbar_size), dtype=float)
        # unprogrammed xbar contains zeros
        if (xbar_value != 'nil'):
            self.xbar_value = xbar_value

    def program (self, xbar_value = ''):
        # programs the crossbar with given matrix values
        val_size = np.shape (xbar_value)
        size_max = constants.xbar_size
        assert (val_size[0] <= size_max and val_size[1] <= size_max), \
                    'Xbar values format should be a numpy array of the xbar dimensions'
        self.xbar_value[0:val_size[0], 0:val_size[1]] = xbar_value.copy ()

    def getLatency (self):
        return self.latency

    def propagate (self, inp = 'nil'):
        self.num_access += 1
        assert (inp != 'nil'), 'propagate needs a non-nil input'
        assert (len(inp) == self.xbar_size), 'xbar input size mismatch'
        return np.dot(inp, self.xbar_value)

    # HACK - until propagate doesn't have correct analog functionality
    def propagate_dummy (self, inp = 'nil'):
        self.num_access += 1
        # data input is list of bit strings (of length dac_res) - fixed point binary
        assert (inp != 'nil'), 'propagate needs a non-nil input'
        assert (len(inp) == self.xbar_size), 'xbar input size mismatch'
        # convert input from fixed point binary (string) to float
        inp_float = [0.0] * self.xbar_size
        for i in range(len(inp)):
            # extend data to num_bits for computation (sign extended)
            temp_inp = (constants.num_bits - constants.dac_res) * '0' + inp[i]
            inp_float[i] = fixed2float(temp_inp, constants.int_bits, constants.frac_bits)
        inp_float = np.asarray (inp_float)
        out_float = np.dot(inp_float, self.xbar_value)
        # convert float back to fixed point binary
        out_fixed  = [''] * self.xbar_size
        for i in range(len(out_fixed)):
            out_fixed[i] = float2fixed(out_float[i], constants.int_bits, constants.frac_bits)
        return out_fixed


class dac (object):
    def __init__ (self, dac_res):
        # define num_access
        self.num_access = 0

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
        self.num_access += 1
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

    # HACK - until propagate doesn't have correct analog functionality
    def propagate_dummy (self, inp_list):
        assert (len(inp_list) == self.xbar_size), 'dac_array input list size mismatch'

        # just to keep track of individual dacs
        junk_list = []
        for i in xrange(self.xbar_size):
            temp_out = self.dac_list[i].propagate(inp_list[i])
            junk_list.append(temp_out)
        # just to keep track of individual dacs

        out_list = inp_list [:]
        return out_list


# Probably - also doing the sampling part of (sample and hold) inside
class adc (object):
    def __init__ (self, adc_res):
        # define num_access
        self.num_access = 0

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
        self.num_access += 1
        assert (type(inp) in [float, np.float32, np.float64]), 'adc input type mismatch (float, np.float32, np.float64 expected)'
        num_bits = self.adc_res
        return self.real2bin (inp, num_bits)

    # HACK - until propagate doesn't have correct analog functionality
    def propagate_dummy (self, inp):
        self.num_access += 1
        return inp

# Doesn't replicate the exact (sample and hold) functionality (just does hold)
class sampleNhold (object):
    def __init__ (self, xbar_size):
        # define num_access
        self.num_access = 0

        # define latency
        self.latency = constants.snh_lat

        self.hold_latch = np.zeros(xbar_size)

    def getLatency (self):
        return self.latency

    # propagate needs to be updated withe xact analog functionaloty if any
    def propagate (self, inp_list):
        self.num_access += 1
        assert (len(inp_list) == len(self.hold_latch)), 'sample&hold input size mismatch'
        for i in xrange(len(inp_list)):
            self.hold_latch[i] = inp_list[i]
        return self.hold_latch

    def propagate_dummy (self, inp_list):
        self.num_access += 1
        assert (len(inp_list) == constants.xbar_size), 'sample&hold input size mismatch'
        out_list = inp_list[:]
        return out_list

# Note the mux instantiations will be analog mux
class mux (object):
    def __init__ (self, num_in):
        # define num_access
        self.num_access = 0

        # define latency
        self.latency = constants.mux_lat

        # num_in is the inputs for the multiplexer
        self.num_in = num_in

    def getLatency (self):
        return self.latency

    def propagate (self, inp_list, sel):
        self.num_access += 1
        assert (len(inp_list) == self.num_in), 'Mux input list size mismatch'
        assert ((type(sel) == int) & (-1 < sel < self.num_in)), 'Mux select input size/type error'
        return inp_list[sel]

    # Note for all practical purpose we will use prop_dummy (mux funtinality is taken care of in code)
    def propagate_dummy (self, inp):
        self.num_access += 1
        return inp


#### Needs some change - add function op (for instance, shift bits for shift)
## Needs to add ALU overflow check/mitigation
class alu (object):
    def __init__ (self):
        # define num_access
        self.num_access = 0

        # define latency
        self.latency = constants.alu_lat

        # Arithmetic operations
        def add (a, b): return (a + b)
        def sub (a, b): return (a - b)
        def shift_add (a, b): return (a + b) # does add, b is already shifted
        def multiply (a, b): return (a * b)

        # Neuronal operations - put here for simplicity (can be made a separate unit)
        # Using aluop (arith./neuronal) dependent power numbers (they will be separate units in harwdare)
        def sigmoid (a, b): # b is unused
            return 1 / (1 + math.exp(-a))
        def tanh (a, b): # b is unused
            return np.tanh(a)
        def relu (a, b): # b is unused
            out = a if (a > 0) else 0
            return out

        self.options = {'add':add, 'sub':sub, 'sna':shift_add, 'mul':multiply,\
                        'sig':sigmoid, 'tanh':tanh, 'relu':relu}

    def getLatency (self):
        return self.latency

    def propagate (self, a, b, aluop, c = 0): # c can be shift operand for sna operation (add others later)
        self.num_access += 1
        assert ((type(aluop) == str) and (aluop in self.options.keys())), 'Invalid alu_op'
        assert (type(c) == int), 'ALU sna: only integral shifts allowed'
        a = fixed2float (a, constants.int_bits, constants.frac_bits)
        if (b == ''):
            b = 0
        else:
            if (aluop == 'sna'): # shift left in fixed point binary
                b = b[c:] + '0' * c
            b = fixed2float (b, constants.int_bits, constants.frac_bits)
        out = self.options[aluop] (a, b)
        # overflow needs to be detected while conversion
        ovf = 0
        out = float2fixed (out, constants.int_bits, constants.frac_bits)
        return [out, ovf]


# Assumes a half-word oriented memory (each entry - 16 bits)
class memory (object):
    def __init__ (self, size, addr_offset = 0):
        # define num_access
        self.num_access = 0

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
        self.num_access += 1
        assert (type(addr) == int), 'addr type should be int'
        assert (self.addr_start <= addr <= self.addr_end), 'addr exceeds the memory bounds'
        return self.memfile[addr - self.addr_start]

    def write (self, addr, data):
        self.num_access += 1
        assert (type(addr) == int), 'addr type should be int'
        assert (self.addr_start <= addr <= self.addr_end), 'addr exceeds the memory bounds'
        #print 'length of data ' + str(len(data))
        assert ((type(data) ==  str) and (len(data) == constants.data_width)), 'data should be a string with mem_width bits'
        self.memfile[addr - self.addr_start] = data

    def reset (self):
        self.num_access += 1
        self.memfile = [''] * self.size


# xbar input memory reads differently than typical memory
# Each read is a shift and read operation
class xb_inMem (object):
    def __init__ (self, xbar_size):
        # define num_access
        self.num_access = 0

        # define latency
        self.latency = constants.mem_lat

        # size equals the xbar_size, each entry being to
        self.xbar_size = xbar_size
        self.memfile = [''] * self.xbar_size

    def getLatency (self):
        return self.latency

    # reads & shifts all entries in parallel
    def read (self, num_bits):
        self.num_access += 1
        out_list = []
        for i in xrange(self.xbar_size):
            value = self.memfile[i]
            #self.memfile[i] = '0'*num_bits + value[:-1*num_bits]
            self.memfile[i] = value[-1*num_bits:] + value[:-1*num_bits]
            out_list.append(value[-1*num_bits:])
        return out_list

    def write (self, addr, data):
        self.num_access += 1
        assert (type(addr) == int), 'addr type should be int'
        assert (-1 < addr < self.xbar_size), 'addr exceeds the memory bounds'
        assert ((type(data) ==  str) and (len(data) == constants.xbdata_width)), 'data should be a string with xbdata_width bits'
        self.memfile[addr] = data

    def reset (self):
        self.num_access += 1
        self.memfile = [''] * self.xbar_size


# xbar output memory
class xb_outMem (xb_inMem):
    def __init__ (self, xbar_size):
        # define num_access
        self.num_access = 0

        # define latency
        self.latency = constants.mem_lat

        # size equals the xbar_size, each entry being to
        self.xbar_size = xbar_size
        self.memfile = ['0' * constants.xbdata_width] * self.xbar_size
        self.wr_pointer = 0

    def getLatency (self):
        return self.latency

    def read (self, addr):
        self.num_access += 1
        assert (type(addr) == int), 'addr type should be int'
        assert (-1 < addr < self.xbar_size), 'addr exceeds the memory bounds'
        return self.memfile[addr]

    def write (self, data):
        self.num_access += 1
        assert ((type(data) ==  str) and (len(data) == constants.xbdata_width)), 'data should be a string with xbdata_width bits'
        self.memfile[self.wr_pointer] = data
        self.wr_pointer = self.wr_pointer + 1

    def restart (self):
        self.num_access += 1
        self.wr_pointer = 0

    def reset (self):
        self.num_access += 1
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
        self.num_access += 1
        assert (type(addr) == int), 'addr type should be int'
        # assert (-1 < addr < self.size), 'addr exceeds the memory bounds'
        if (-1 < addr < self.size):
            return self.memfile[addr]
        else:
            return self.memfile[len(memfile)]

    def write (self, addr, data):
        self.num_access += 1
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


# Defining all modules within an ima and its methods (Propagate and or Update)
# 'Propagate' is the combinational part evaluation
# 'Update' is the flip fop evaluation (for clocked elements of teh circuit only)

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
        #dac_res - resolution
        print ('init: under construction')

    def bin2real (inp, num_bits):
        # gets a n-bit (n = dac_res) digital value & returns an analog voltage value
        inp_max = '1' * num_bits # string with all 1s
        analog_max = vdd
        frac = int(inp, 2) / int(inp_max, 2)
        return analog_max * frac
    
    def propagate (self, inp):
        assert (type(a) == str), 'dac input type mismatch (string expected)'
        num_bits = dac_res
        return bin2real (inp, num_bits)


# A dac_array is an arrays of DACs private to a xbar
class dac_array (object):
    def __init__ (self, xbar_size, dac_res):
        # generate multiple dacs (one per xbar input)
        self.dac_list = []
        self.xbar_size = xbar_size
        for i in xrange(xbar_size):
            temp_dac = dac (dac_res)
            dac_list.append(temp_dac)

    def propagate (self, inp_list):
        out_list = []
        for i in xrange(self.xbar_size):
            temp_out = self.dac_list[i].propagate(inp_list[i])
            out_list.append(temp_out)
        return out_list


# Probably - also doing the sampling part of (sampel and hold) inside
class adc (object):
    def __init__ (self, adc_res):
        # adc_res - adc resolution
        print ('init: under construction')

    def real2bin (inp, num_bits):
        num_levels = 2**num_bits
        step = float((xbar_out_max - xbar_out_min)) / num_levels
        int_value = ceil(((inp - xbar_out_min) / floatstep))
        return (bin(int_value)[2:])
        
    def propagate (self, inp):
        assert (type(inp) == float), 'adc input type mismatch (float expected)'
        num_bits = adc_res
        return real2bin (inp, num_bits)


# Instantiates a list of ADCs each of which can be indpendently used
# An adc_pool is a pool of ADCs shared by all crossbars
class adc_pool (object):
    def __init__ (self, num_adc):
        self.num_adc = num_adc
        self.adc_list = []
        for i in xraange(num_adc):
            temp_adc = adc (adc_res)
            adc_list.append(temp_adc)

##    def propagate (self, inp_list):
##        out_list = []
##        for i in xrange(self.num_adc):
##            temp_out = self.adc_list[i].propagate(inp_list[i])
##            out_list.append(temp_out)


# Doesn't replicate the exact (sample and hold) functionality (just does hold)
class samplehold (object):
    def __init__ (self, xbar_size):
        self.hold_latch = np.zeros(xbar_size)

    def propagate (self, inp):
        assert (len(inp) == len(self.hold_latch)), 'sample&hold input size mismatch'
        for i in inp:
            self.hold_latch[i] = inp[i]
        return self.hold_latch


class mux (object):
    def __init__ (self, num_in):
        # num_in is the inputs for the multiplexer
        self.num_in = num_in

    def propagate (self, inp_list, sel):
        assert (len(inp_list) == self.num_in), 'Mux input list size mismatch'
        assert ((type(sel) == int) && (-1 < sel < self.num_in)), 'Mux select input size/type error'
        return inp_list[sel]
 

class alu (object):
    def __init__ (self):
        # the output port which holds the result
        self.out = 0
        def add (a, b): return (a + b)
        def sub (a, b): return (a - b)
        def shift_add (a, b): return (a + (b << 2))
        self.options = {'add' : add, 'sub' : sub, 'shift_add', : shift_add}
    
    def propgate (self, a, b, aluop):
        assert ((type(alu_op) == str) & (aluop in self.options.keys())), 'Invalid alu_op'
        self.out = options[alu_op](a, b)
        return self.out


# Instantiates a list of ALUs for an IMA (each can be used independently)
class alu_array (object):
    def __init__ (self, num_ALUs):
        # instantiate multiple alus based on the dpe configuration
        self.num_ALUs = num_ALUs
        self.ALU_list = []
        for i in xrange(num_ALUs):
            temp_ALU = alu ()
            ALU_list.append(temp_ALU)

##    def propagate (self, a_list, b_list, aluop_list):
##        assert(len(a_list) == len(b_list) == len(aluop_list) == self.num_ALUs), 'input (a/b/aluop) size mismatch'
##        out_list = []
##        for i in xrange(self.num_ALUs):
##            out_list[i] = self.ALU_list[i](a_list[i], b_list[i], aluop_list[i])
##        return out_list[i]


# Assumes a half-word oriented memory (each entry - 16 bits)
class memory (object):
    def __init__ (self, size):
        # memfile will store half-word (16 bits digital data) length strings
        self.size = size
        self.memfile = ['']*size

    def read (self, addr):
        assert (type(addr) == int), 'addr type shoudl be int'
        assert (-1 < addr < size), 'addr exceeds the memory bounds'
        return self.memfile[addr]

    def write (self, addr, data):
        assert (type(addr) == int), 'addr type shoudl be int'
        assert (-1 < addr < size), 'addr exceeds the memory bounds'
        assert ((type(data) ==  str) & (len(data) < mem_width)), 'data should be a string with less than or equal to mem_width bits'
        memfile[addr] = data
        return 1


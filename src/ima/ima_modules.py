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


class adc (object):
    def __init__ (self, adc_res):
        # adc_res - adc resolution

    def real2bin (inp, num_bits):
        num_levels = 2**num_bits
        step = float((xbar_out_max - xbar_out_min)) / num_levels
        int_value = ceil(((inp - xbar_out_min) / floatstep))
        return (bin(int_value)[2:])
        
    def propagate (self, inp):
        assert (type(inp) == float), 'adc input type mismatch (float expected)'
        num_bits = adc_res
        return real2bin (inp, num_bits)
            
# An adc_pool is a pool of ADCs shared by all crossbars
class adc_pool (object):
    def __init__ (self, num_adc):
        self.num_adc = num_adc
        self.adc_list = []
        for i in xraange(num_adc):
            temp_adc = adc (adc_res)
            adc_list.append(temp_adc)

    def propagate (self, inp_list):
        out_list = []
        for i in xrange(self.num_adc):
            temp_out = self.adc_list[i].propagate(inp_list[i])
            out_list.append(temp_out)


class samplehold (object):


class mux (object):


class alu (object):


class inpregister (object):


class outregister (object):


# Validate the outer product algorithm with bit-slicing and signed arithmetic
# Validation with 16-bit integers with 32-bit outer-product is sufficient to validate for 16-bit fixed point for fractional numbers
# Supposing:
#   16 xbar of 2bit each -> 32bit total sliced output

import sys
import os
import numpy as np

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

# Specify parameters for testing
num_bits = 16                     # Weights size is num_bits + int_bits size
int_bits = 16                     # Word size
frac_bits = num_bits - int_bits   # Not concerning regarding fractional representation. Everything is binary in the end.
xbar_bits = 2                     # XBAR are 2bit (2 rows, 2 columns)

# assumed extra bits for accumulation
xbar_extraBits = 7                # Each delta XBAR has xabar_extraBits accumulator
zero_offset = 2** (xbar_extraBits-1)     #  In the delta XBAR the values are store with as unsigned, so zero_offset means the values that represets the zero. 

max_xbar_value = (1 << xbar_extraBits) - 1

def bin2int (binary_string, bits):
    val = int (binary_string,2)
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val

def int2bin (int_data, bits):
    data_str = bin(int_data & (2**bits-1))[2:].zfill(bits)
    return data_str

def float2fixed (float_data, int_bits, frac_bits):
    temp = float_data * (2**frac_bits)
    temp = int(round (temp))
    return int2bin (temp, (int_bits+frac_bits))

def fixed2float (binary_string, int_bits, frac_bits):
    temp = bin2int (binary_string, (int_bits + frac_bits))
    return float(temp) / (2**frac_bits)

# function to slice an unsigned weight into 2-bit chunks (number of weight bits = 2*num_bits)
def wt_bitSlice (wt):
    wt_slice = []
    wt_fixed = float2fixed (wt, int_bits, frac_bits)
    # append zeros to first num_bits
    for i in range (num_bits//xbar_bits):
        temp = "0"*(xbar_extraBits)
        temp_int = bin2int(temp,xbar_extraBits) + zero_offset
        bias_temp = float2fixed (temp_int, xbar_extraBits, 0)
        wt_slice.append (bias_temp)
    # add wt_fixed bits starting from MSB
    for i in range (num_bits//xbar_bits):
        temp = wt_fixed[i*xbar_bits:(i+1)*xbar_bits]
        temp_int = bin2int(temp,xbar_extraBits) + zero_offset
        bias_temp = float2fixed (temp_int, xbar_extraBits, 0)
        wt_slice.append (bias_temp)

    return wt_slice

# function to slice an unsigned weight into 2-bit chunks (number of weight bits = 2*num_bits)
def wt_bitSlice2 (wt):
    wt_ = wt
    wt_sliced = []
    for i in range (num_bits):
        wt_sliced.append(wt % (1<<xbar_bits) + zero_offset)
        wt_ = wt_ >> xbar_bits
    return wt_sliced

# add/sub two fixed point numbers (the numbers are unsigned)
def add_fixed (in1, in2, sub=0):
    in1_float = fixed2float (in1, int_bits, frac_bits)
    in2_float = fixed2float (in2, int_bits, frac_bits)
    if (sub == 0):
        out = in1_float + in2_float
        # cap the output at the maximum (memristor behaviour, staurates at max. positive)
        #if (out > )
    else:
        out = in1_float - in2_float
    #print ('in1: ' + str(in1_float) + ' in2: ' + str(in2_float) + ' out: ' + str(out))
    return float2fixed (out, xbar_extraBits, frac_bits)

# function to multiply two inputs and accumulate over weight using bit-streamed multiplication
def outer_prod (wt_slice, in1_fixed, in2_fixed, sub=0):
    # stream over in1 bits
    for i in range (num_bits):
        # compute the 2*num_bits value to be accumulated
        temp = in2_fixed
        if (in1_fixed[-1*(i+1)] == '0'): # lsb is the right-most bit
            temp = num_bits * '0'
        acc = (num_bits-i)*'0' + temp + i*'0' # left shifted for bit-streamed mul
        #print ('Bit pos: ' + str(i) + "acc: " + acc)
        # add respective parts of acc on wt_slice
        for j in range (num_bits):
            wt_slice[j] = add_fixed (wt_slice[j], acc[j*xbar_bits:(j+1)*xbar_bits], sub)
        #print ('Wt slice: ', wt_slice)

# function to multiply two inputs and accumulate over weight using bit-streamed multiplication
def outer_prod2 (wt_sliced, in1, in2, sub=0):
    in1 = abs(in1)
    in2 = abs(in2)
    for i in range (num_bits):
        lsb1 = in1 % 2 # get LSB
        if lsb1 == 1:
            op2 = in2 << i
            for j in range (num_bits):
                acc = op2 % (1<<xbar_bits) # get 2 bit
                if sub == 1:
                    acc *= -1
                wt_sliced[j] += acc
                wt_sliced[j] = np.clip(wt_sliced[j], 0, max_xbar_value)
                op2 = op2>>xbar_bits
        in1 = in1 >> 1
    return wt_sliced

# run crs over wt_slice to give 16-bit weight
def crs (wt_slice):
    val = 0.0
    for i in range (len(wt_slice)):
        shift_pos = 2 * ((len(wt_slice)-1) - i)
        val += (fixed2float (wt_slice[i], 2*int_bits, 2*frac_bits)- zero_offset) * (2**shift_pos)

    return val

# run crs over wt_slice to give 16-bit weight
def crs2 (wt_slice):
    val = 0.0
    for i in range (len(wt_slice)):
        shift_pos = 2**(i*xbar_bits)
        val += shift_pos * (wt_slice[i]-zero_offset)
    return val

# evaluation script
def eval (in1, in2, wt):
    wt_slice = wt_bitSlice (wt)
    wt_slice2 = wt_bitSlice2 (wt)
    # use magnitudes of in1 and in2 - signed magnitude representation
    in1_fixed = float2fixed (abs(in1), int_bits, frac_bits)
    in2_fixed = float2fixed (abs(in2), int_bits, frac_bits)
    sub = 0 if (in1*in2 >= 0) else 1
    #print ('in1_fixed: ' + str(in1_fixed) + ' in2_fixed: ' + str(in2_fixed))

    outer_prod (wt_slice, in1_fixed, in2_fixed, sub)
    outer_prod2(wt_slice2, in1, in2, sub)
    
    val = crs (wt_slice)
    val2 = crs2(wt_slice2)
    print ('val_exp', wt+in1*in2)
    print ('val_out', val)
    print ('val_out2', val2)


## testcases
# Case 1: evaluate for positive integers (num_bits = 16, int_bits = 16)
in1 = 1645
in2 = 232
wt = 2406 # this will always be positive (weight on crossbar is represneted as an unsigned number with zero_offset column)
# eval (in1, in2, wt)

# Case 2: evaluate for negative integers (num_bits = 16, int_bits = 16)
# this will always be positive (weight on crossbar is represneted as an unsigned number with zero_offset stored seperately)
in1 = -214
in2 = 178
wt = 50000
# eval (in1, in2, wt)

# Case 3: evaluate for negative integers (num_bits = 16, int_bits = 16)
# this will always be positive (weight on crossbar is represneted as an unsigned number with zero_offset stored seperately)
in1 = -114
in2 = -378
wt = 50000
eval (in1, in2, wt)



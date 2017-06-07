# Technology constants for all the modules (components in an IMA)
vdd = 0.9
xbar_out_min = 0
xbar_out_max = 1 # think about this
mem_width = 16

#################################################
# DPE Hardware Configuration Parameters
#################################################

#################################################
# IMA Hierarchy
    # Number of Xbars
    # Crossbar Size
    # Bit resolution of ADCs and DACs
    # Number of ADCs
    # Number of ALUs
    # Input memory, Output memory (Register) & Instruction memory sizes
#################################################

# Enter parameters here:
num_xbar = 2
xbar_size = 4
dac_res = 2
adc_res = 2
num_adc = 1
num_ALU = 1
inMem_size = 8
outMem_size = 8
instrMem_size = 8


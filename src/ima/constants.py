# Technology constants for all the modules (components in an IMA)
vdd = 0.9
xbar_out_min = 0
xbar_out_max = 1 # think about this
data_width = 16 # (microarchitecture param)
xbdata_width = 8 # (nn speciic for now)

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
    # Data memory, Xbar in/out memory (Register) & Instruction memory sizes
#################################################

# Enter parameters here:
num_xbar = 2
xbar_size = 4
dac_res = 2
adc_res = 2
num_adc = 1
num_ALU = 1
dataMem_size = 16
instrnMem_size = 8

import math
import sys
sys.path.insert (0, '/home/aankit/dpe_emulate/include')
import matplotlib.pyplot as plt
from collections import OrderedDict

import config as cfg
# PUMA tile sweep (parameters) for CE(computation efficiency)
# CE is measured as the number of 16-bit operations performed per second per mm2

# Computation units:
# 1. xbar for matrix-vector multiplication
# 2. vfu for performing vector operations
# 3. rom (dataMem embedded ROM-RAM) for look-up table based operations

# datamemory (4*xbar_size*(num_xbar/8)) - Constant (from PUMA compiler based on register allocation)

# Time step considered (based on xbar latency) = 128ns

log2phy_xbfactor = cfg.data_width / cfg.xbar_bits # logical xbar count

# Sweep Parameters considered:
#xbar_size_list = [64, 128, 256]
#num_mvmu_list = [1, 4, 16, 64]
#num_vfu_list = [1, 4, 16, 64]
#num_core_list = [1, 4, 8, 16]
#regfile_size_list = [0.25, 1, 4, 16]

## single sweeps (sweet spot S128-X16-V4-C8, 772.13)
xbar_size_list = [128]
num_mvmu_list = [16]
num_vfu_list = [4]
num_core_list = [8]
regfile_size_list = [0.25, 1, 4, 16]

num_xbar_list = [] # [xbar_size (DACs,SnH), 1 ADC, 1 SnA per xbar]
for i in range(len(num_mvmu_list)):
    num_xbar_list.append (num_mvmu_list[i]*log2phy_xbfactor)

time_step_dict = {'64':60, '128':100, '256':400}

num_data_points = len(xbar_size_list) * len(num_xbar_list) * len(num_vfu_list) * len(num_core_list)
print ('num_data_points', num_data_points)

ns = 10**(-9) #wrt seconds
mw = 10**(-3) #wrt watt
mm2 = 1 #wrt millimetres2
# Logical to physical xbar ratio
# xbar latency for 128 sized xbar in ns
time_step = 100

# fixing the number of ADCs in a core
num_adc = 16

# Component areas in mm2 (per component)
xbar128_area = 2.5 * 10**(-5)
dac_area = 1.67 * 10**(-7)
adc_area = 0.0012
snh_area = 0.00004/8/128
sna_area = 0.00006
alu_area = 0.00567 * 32.0/45.0
dataMem128_2_area = 0.00192 # datamem area for xbar_size 128 and num_xbar 16
instrnMem_area = 0.00108 * math.sqrt(8) #512 entries
xbar_inMem128_area = 0.00078
xbar_outMem128_area = 0.00078
ccu_area = 0.00145*2.25

edram_area = 0.086
tile_instrnMem_area = 0.00192 * math.sqrt(8) #1024 entries
counter_buff_area = 0.0041 * math.sqrt(8)
edram_bus_area = 0.090
edram_ctrl_area = 0.00145
receive_buffer_area = 0.0022 * math.sqrt(4)
tcu_area = 0.00145
router_area = 0.047/cfg.cmesh_c


# Function to measure tile are for given parameters # in mm2
def get_tile_area (xbar_size, num_xbar, num_vfu, num_core, regfile_size):
    core_area = 0.0
    # assumption xbar area scales quadratically with xbar_size (Confirm with JPS)
    core_area += num_xbar * ((xbar_size/128.0)**2) * xbar128_area
    core_area += num_xbar/log2phy_xbfactor * xbar_size * dac_area
    # adc area is dependent on xbar_size - some components have exponential dependance
    #core_area += num_xbar * adc_area * (xbar_size/128)**1.2
    #core_area += num_xbar * adc_area * (xbar_size/128.0)**(2.3)
    # Assumption - ADC of fixed sampling rate is used
    #core_area += num_xbar * adc_area * (xbar_size/128.0)**(2.3)
    core_area += num_adc * adc_area * (xbar_size/128.0)**(2.3)
    core_area += num_xbar * xbar_size * snh_area
    core_area += num_xbar * sna_area
    core_area += num_vfu * alu_area
    # memory units grow as square root w.r.t. number of entries
    core_area += math.sqrt((xbar_size/128.0) * (num_xbar/16.0)) * dataMem128_2_area * regfile_size
    # instrn mem area is dependent on num_xbars (num_mvms a core can do)
    # memory units grow as square root w.r.t. number of entries
    core_area += math.sqrt(num_xbar/16.0) * instrnMem_area
    # memory units grow as square root w.r.t. number of entries
    core_area += math.sqrt(xbar_size/128.0) * (num_xbar/8.0) * xbar_inMem128_area
    # memory units grow as square root w.r.t. number of entries
    core_area += math.sqrt(xbar_size/128.0) * (num_xbar/8.0) * xbar_outMem128_area
    core_area += ccu_area
    tile_area = num_core * core_area
    #tile_area += math.sqrt((num_core/8.0)*(xbar_size/128.0)*(num_xbar/16.0)) * edram_area
    #tile_area += ((num_core/8.0)*(xbar_size/128.0)*(num_xbar/16.0)) * edram_area
    tile_area += math.sqrt((xbar_size/128.0)*(num_xbar/16.0)) * edram_area
    # Less send and receives between tiles
    tile_area += tile_instrnMem_area / (math.sqrt((xbar_size/128.0)*(num_xbar/16.0)*(num_core/8.0)))
    tile_area += math.sqrt((xbar_size/128.0)*(num_xbar/16.0)) * counter_buff_area
    tile_area += math.sqrt(num_core/8.0) * edram_bus_area
    tile_area += math.sqrt((xbar_size/128.0)*(num_xbar/16.0)) * edram_ctrl_area
    # Less tiles will fan-out to a next layer tile
    # Less send and receives between tiles
    #tile_area += receive_buffer_area/ (math.sqrt((xbar_size/128.0)*(num_xbar/16.0)))
    tile_area += receive_buffer_area
    tile_area += tcu_area
    tile_area += router_area
    return tile_area


# Measure the number of computations for given parameters
def get_num_comp (xbar_size, num_xbar, num_vfu, num_core):
    num_comp_xbar = (num_xbar/log2phy_xbfactor) * (2*xbar_size*xbar_size)
    num_comp_vfu = (num_xbar/log2phy_xbfactor) * xbar_size
    num_comp_rom = (num_xbar/log2phy_xbfactor) * xbar_size # lut (1 RAM read, 1 ROM read, 1 RAM write, 1 ALU for interpolation)
    num_comp_total = num_core*(num_comp_xbar + num_comp_vfu + num_comp_rom)
    return num_comp_total


def get_time (xbar_size, num_xbar, num_vfu, num_core):
    # assumption: xbar latency scales linearly with xbar_size (Confirm with John-Paul)
    # A highly parallel synthtic workload going through all units (VFU, MVM, MEU) in Core
    # all xbars in a core implement separate matrix
    # all xbars in a core run in ||el
    # all xbars outputs go through vfu (to get xbar_size outputs)
    # all vfu outputs go through lut
    # xbar_size outputs are stored
    # overall time makes sure that last core's store finishes
    #time_step_new = time_step * (xbar_size/128.0)
    time_step_new = time_step_dict[str(xbar_size)]
    ld_time = num_core * (num_xbar/log2phy_xbfactor) * (xbar_size/16) #1 edram read is 16 entries 1ns
    mvm_time = (16+2) * time_step_new
    # vfu and lut can clocked at a frequency at higher power (same energy), so that they finish xbar_width number of
    # operation in time_step of crossbars
    vfu_time = time_step_new * math.ceil((num_xbar/log2phy_xbfactor)/num_vfu)
    lut_time = time_step_new * (num_xbar/log2phy_xbfactor)
    st_time = (num_xbar/log2phy_xbfactor) * (xbar_size/16)
    time_total = ld_time + mvm_time + vfu_time + lut_time + st_time
    return time_total * ns


# Sweep to generate computational efficiency data
#ce_dict = OrderedDict()
ce_list = []
name_list = []
for xbar_size in xbar_size_list:
    if (xbar_size != xbar_size_list[0]):
        ce_list.append(0)
        name_list.append(' ')
        ce_list.append(0)
        name_list.append(' ')
    for num_vfu in num_vfu_list:
        ce_list.append(0)
        name_list.append(' ')
        ce_list.append(0)
        name_list.append(' ')
        for num_xbar in num_xbar_list:
            ce_list.append(0)
            name_list.append(' ')
            for num_core in num_core_list:
                for regfile_size in regfile_size_list:
                    tile_area = get_tile_area (xbar_size, num_xbar, num_vfu, num_core, regfile_size)
                    num_comp_total = get_num_comp (xbar_size, num_xbar, num_vfu, num_core)
                    time = get_time (xbar_size, num_xbar, num_vfu, num_core)
                    ce = num_comp_total / tile_area / time / (10**9) #in GigaOps
                    name = 'S'+str(xbar_size)+'-V'+str(num_vfu)+'-X'+str(num_xbar/log2phy_xbfactor)+'-C'+str(num_core)
                    ce_list.append(ce)
                    name_list.append(name)

# Plot the sweep
#plt.bar(range(len(ce_dict)), ce_dict.values(), align='center')
#plt.xticks(range(len(ce_dict)), ce_dict.keys())

# Print max and corresponding numbers
print (max(ce_list))
idx = ce_list.index (max(ce_list))
print (name_list[idx])

plt.bar(range(len(ce_list)), ce_list, align='center')
plt.xticks(range(len(name_list)), name_list)

plt.xticks(fontsize=6, rotation=70)
#plt.autoscale(tight=True)
plt.show()
#plt.savefig('/home/aa/dpe_emulate/isca_results/puma_ce_sweep')




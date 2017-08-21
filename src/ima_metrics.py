# APIs to compute ima power and area stats

import sys
sys.path.insert (0, '/home/ankitaay/dpe/include')

# import dependency files
import config as cfg
import constants as param

# Compute metrics of the ima based on paramaters in config file and dicts in constants file
# Area is computed as the summation of all component area (doesn't consider physical layout)
def compute_area (): #in mm2
    area = 0.0
    area += cfg.num_xbar * param.xbar_inMem_area # xbar_inMem
    area += (cfg.num_xbar * cfg.xbar_size) * param.dac_area # dac
    area += cfg.num_xbar * param.xbar_area # xbar
    area += (cfg.num_xbar * cfg.xbar_size) * param.snh_area # snh
    area += cfg.num_adc * param.adc_area # adc
    area += cfg.num_xbar * param.sna_area # sna
    #area += cfg.num_xbar * param.xbar_outMem_area # xbar_outMem
    area += 2 * param.xbar_outMem_area # xbar_outMem (1 OR for 8 xbars - 16 bit weights, 2 bit xbars)
    area += param.instrnMem_area # instrnMem
    area += param.dataMem_area # dataMem
    area += param.alu_area # alu
    area += param.act_area # activation (sigmoid)
    #print ('6 IMA area: ' + str (6 * area) + ' mm2')

    ## Comapre with ISSAC area for iso-xbars (computational efficiency - ops/mm2)
    #ima_issac_area = 0.157/12.0 + 8 * 1*param.xbar_inMem_area - 0.0021 #- 0.00077 # 8 * param.xbar_inMem_area is area of
    ## 2KB RAM in an IMA - acc to CACTI 6.0
    #print ('12 IMA area ISSAC: ' + str (12 * ima_issac_area) + ' mm2')
    #print ('Area increase for iso xbars: ' + str((6*area - 12*ima_issac_area) / (12*ima_issac_area)*100) + ' %')
    return area

# Leakage power is computed as sum of leakage powers of all components
def compute_pow_leak ():
    leak_pow = 0.0
    leak_pow += cfg.num_xbar * param.xbar_inMem_pow_leak # xbar_inMem
    leak_pow += (cfg.num_xbar * cfg.xbar_size) * param.dac_pow_leak # dac
    leak_pow += cfg.num_xbar * param.xbar_pow_leak # xbar area
    leak_pow += (cfg.num_xbar * cfg.xbar_size) * param.snh_pow_leak # snh
    leak_pow += cfg.num_adc * param.adc_pow_leak # adc
    leak_pow += cfg.num_xbar * param.sna_pow_leak # sna
    leak_pow += cfg.num_xbar * param.xbar_outMem_pow_leak # xbar_outMem
    leak_pow += param.instrnMem_pow_leak # instrnMem
    leak_pow += param.dataMem_pow_leak # dataMem
    leak_pow += param.alu_pow_leak # alu
    leak_pow += param.act_pow_leak # activation (sigmoid) areacompute_leak_pow: # in mw
    # print ('IMA leak power: ' + str (leak_pow) + ' mW')
    return leak_pow

# Peak dynamic power (assumes all components are being accessed in each cycle)
def compute_pow_dyn ():
    dyn_pow = 0.0
    dyn_pow += cfg.num_xbar * param.xbar_inMem_pow_dyn / cfg.xbar_size # xbar_inMem - num_xbar * dac_res bits will be
                    #   read from xb_inMem in an interval that equals xbar_access time
    # dyn_pow += cfg.num_xbar/2 * 1.2 # (adding dyn pow the way issac does for comparison)
    dyn_pow += (cfg.num_xbar * cfg.xbar_size) * param.dac_pow_dyn # dac
    dyn_pow += cfg.num_xbar * param.xbar_pow_dyn # xbar
    dyn_pow += (cfg.num_xbar * cfg.xbar_size) * param.snh_pow_dyn # snh
    dyn_pow += cfg.num_adc * param.adc_pow_dyn # adc
    dyn_pow += cfg.num_xbar * param.sna_pow_dyn # sna
    #dyn_pow = cfg.num_xbar * param.xbar_outMem_pow_dyn # xbar_outMem
    dyn_pow += 2 * param.xbar_outMem_pow_dyn # xbar_outMem (1 OR for 8 xbars - 16 bit weights, 2 bit xbars)
    dyn_pow += param.instrnMem_pow_dyn # instrnMem
    dyn_pow += param.dataMem_pow_dyn # dataMem
    dyn_pow += param.alu_pow_dyn # alu
    dyn_pow += param.act_pow_dyn # activation (sigmoid) areacompute_leak_pow: # in mw
    # print ('IMA dyn power: ' + str (dyn_pow) + ' mW')
    return dyn_pow

# Peak power of ima - leak pow + peak_dyn power
def compute_pow_peak ():
    peak_pow = compute_pow_leak() + compute_pow_dyn()
    #print ('6 IMA peak (leak+dyn) power: ' + str (6 * peak_pow) + ' mW')

    ## Compare with ISSAC for iso-xbars (computational effciiency - ops/mm2)
    #ima_issac_pow = 289/12.0 # 12 IMA
    #print ('12 IMA power ISSAC: ' + str (12 * ima_issac_pow) + ' mW')
    #print ('Peak power increase for iso xbars: ' + str((6 *peak_pow - 12*ima_issac_pow) / (12*ima_issac_pow)*100) + ' %')
    return peak_pow

#compute_area()
#compute_pow_leak()
#compute_pow_dyn()
#compute_pow_peak()


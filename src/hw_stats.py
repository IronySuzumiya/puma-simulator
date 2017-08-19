# API to extract hardware trace (stats) from DPE execution
# Write to file
import sys
sys.path.insert (0, '/home/ankitaay/dpe/include/')
import config as cfg

ns = 10 ** (-9)
mw = 10 ** (-3)
nj = 10 ** (-9)

hw_comp_energy = {'xbar':2.4/8*mw*ns,    'dac':4/8/128*mw*ns,    'snh':0,        'mux1':0,       'mux2':0,\
        'adc':(16/8+0.2/4)*mw*ns,    'alu':1.5*mw*ns,     'imem':0.0017*nj,   'dmem':0.00104*nj,       'xbInmem':0.0037*nj,\
        'xbOutmem':0.0003*nj, 'imem_t':0.0017*nj,  'rbuff':0.00104*nj,  'edram':(20.7*1.25+7)/16*mw*ns,      'edctrl':0.5*mw*ns, \
       'noc_intra':0,           'noc_inter':0
       }

def get_hw_stats (fid, node_dut):

    hw_comp_access = {'xbar':0,    'dac':0,    'snh':0,        'mux1':0,       'mux2':0,    'adc':0, \
           'alu':0,     'imem':0,   'dmem':0,       'xbInmem':0,    'xbOutmem':0, \
           'imem_t':0,  'rbuff':0,  'edram':0,      'edctrl':0, \
           'noc_intra':0,           'noc_inter':0
           }

    # traverse comp_accessonents to populate dict (hw_comp_access)
    hw_comp_access['noc_intra'] += node_dut.noc.num_access_intra
    hw_comp_access['noc_inter'] += node_dut.noc.num_access_inter

    for i in range (1, cfg.num_tile-1): # ignore dummy (input & output) tiles
        hw_comp_access['imem_t'] += node_dut.tile_list[i].instrn_memory.num_access
        hw_comp_access['rbuff'] += node_dut.tile_list[i].receive_buffer.num_access
        hw_comp_access['edram'] += node_dut.tile_list[i].edram_controller.mem.num_access
        hw_comp_access['edctrl'] += node_dut.tile_list[i].edram_controller.num_access

        for j in range (cfg.num_ima):
            for k in range (cfg.num_xbar):
                hw_comp_access['xbar'] += node_dut.tile_list[i].ima_list[j].xbar_list[k].num_access

            for k in range (cfg.num_xbar):
                for l in range (cfg.xbar_size):
                    hw_comp_access['dac'] += node_dut.tile_list[i].ima_list[j].dacArray_list[k].dac_list[l].num_access

            for k in range (cfg.num_xbar):
                hw_comp_access['snh'] += (node_dut.tile_list[i].ima_list[j].snh_list[k].num_access * cfg.xbar_size) # each snh is
                # basically an array of multiple snhs (individual power in constants file must be for one discerete snh)

            for k in range (cfg.num_xbar):
                hw_comp_access['mux1'] += node_dut.tile_list[i].ima_list[j].mux1_list[k].num_access

            for k in range (cfg.num_xbar / cfg.num_adc):
                hw_comp_access['mux2'] += node_dut.tile_list[i].ima_list[j].mux1_list[k].num_access

            for k in range (cfg.num_adc):
                hw_comp_access['adc'] += node_dut.tile_list[i].ima_list[j].adc_list[k].num_access

            for k in range (cfg.num_ALU):
                hw_comp_access['alu'] += node_dut.tile_list[i].ima_list[j].alu_list[k].num_access

            hw_comp_access['imem'] += node_dut.tile_list[i].ima_list[j].instrnMem.num_access

            hw_comp_access['dmem'] += node_dut.tile_list[i].ima_list[j].dataMem.num_access

            for k in range (cfg.num_xbar):
                hw_comp_access['xbInmem'] += node_dut.tile_list[i].ima_list[j].xb_inMem_list[k].num_access

            for k in range (cfg.num_xbar):
                hw_comp_access['xbOutmem'] += node_dut.tile_list[i].ima_list[j].xb_outMem_list[k].num_access

    total_energy = 0
    # Write the dict comp_accessonents to a file for visualization
    for key, value in hw_comp_access.items():
        if (key != 'alu'):
            total_energy += value * hw_comp_energy[key]
        else:
            total_energy += (value - hw_comp_access['adc']) * hw_comp_energy[key]
        fid.write (key + ': ')
        fid.write (str(value) + '\n')
    return total_energy



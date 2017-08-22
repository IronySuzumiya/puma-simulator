# API to extract hardware trace (stats) from DPE execution
# Write to file
import sys
sys.path.insert (0, '/home/ankitaay/dpe/include/')
sys.path.insert (0, '/home/ankitaay/dpe/src/')
import config as cfg
import constants as param
import node_metrics
import tile_metrics
import ima_metrics


ns = 10 ** (-9)
mw = 10 ** (-3)
nj = 10 ** (-9)

# Copied from /include/constants.py file
# Enlists components at core, tile, and node levels
hw_comp_energy = {'xbar':param.xbar_pow_dyn*100, 'dac':param.dac_pow_dyn, 'snh':param.snh_pow_dyn, \
        'mux1':param.mux_pow_dyn, 'mux2':param.mux_pow_dyn, 'adc':param.adc_pow_dyn, \
        'alu_div': param.alu_pow_div_dyn, 'alu_mul':param.alu_pow_mul_dyn, \
        'alu_act': param.act_pow_dyn, 'alu_other':param.alu_pow_others_dyn, \
        'alu_sna': param.sna_pow_dyn, \
        'imem':param.instrnMem_pow_dyn, 'dmem':param.dataMem_pow_dyn, 'xbInmem_rd':param.xbar_inMem_pow_dyn_read, \
        'xbInmem_wr':param.xbar_inMem_pow_dyn_write, 'xbOutmem':param.xbar_outMem_pow_dyn, \
        'imem_t':param.tile_instrnMem_pow_dyn, 'rbuff':param.receive_buffer_pow_dyn,\
        'edram':param.edram_pow_dyn, 'edctrl':param.edram_ctrl_pow_dyn, \
        'edram_bus':param.edram_bus_pow_dyn, 'edctrl_counter':param.counter_buff_pow_dyn, \
        'noc_intra':param.noc_intra_pow_dyn, 'noc_inter':param.noc_inter_pow_dyn \
        }

# Used to calculate dynamic energy consumption and other metrics (area/time/total_power/peak_power)
def get_hw_stats (fid, node_dut, cycle):

    # List of all components that dissipate power
    hw_comp_access = {'xbar':0, 'dac':0, 'snh':0, \
            'mux1':0, 'mux2':0, 'adc':0, \
            'alu_div':0, 'alu_mul':0, \
            'alu_act':0, 'alu_other':0, \
            'alu_sna':0, \
            'imem':0, 'dmem':0, 'xbInmem_rd':0, \
            'xbInmem_wr':0, 'xbOutmem':0, \
            'imem_t':0, 'rbuff':0, \
            'edram':0, 'edctrl':0, \
            'edram_bus':0, 'edctrl_counter':0, \
            'noc_intra':0, 'noc_inter':0 \
            }

    # traverse components to populate dict (hw_comp_access)
    hw_comp_access['noc_intra'] += node_dut.noc.num_access_intra
    hw_comp_access['noc_inter'] += node_dut.noc.num_access_inter

    # Count num_cycles for leakage energy computations (power-gating granularity: ima/tile/noc)
    sum_num_cycle_tile = 0
    sum_num_cycle_ima = 0
    sum_num_cycle_noc = node_dut.noc.num_access_intra


    for i in range (1, cfg.num_tile-1): # ignore dummy (input & output) tiles
        sum_num_cycle_tile += node_dut.tile_list[i].cycle_count # used for leakage energy of tiles

        hw_comp_access['imem_t'] += node_dut.tile_list[i].instrn_memory.num_access
        hw_comp_access['rbuff'] += node_dut.tile_list[i].receive_buffer.num_access
        hw_comp_access['edram'] += node_dut.tile_list[i].edram_controller.mem.num_access
        hw_comp_access['edram_bus'] += node_dut.tile_list[i].edram_controller.mem.num_access
        hw_comp_access['edctrl'] += node_dut.tile_list[i].edram_controller.num_access
        hw_comp_access['edctrl_counter'] += node_dut.tile_list[i].edram_controller.num_access_counter

        for j in range (cfg.num_ima):
            sum_num_cycle_ima += node_dut.tile_list[i].ima_list[j].cycle_count # used for leakage energy of imas

            for k in range (cfg.num_xbar):
                hw_comp_access['xbar'] += node_dut.tile_list[i].ima_list[j].xbar_list[k].num_access

            for k in range (cfg.num_xbar/(cfg.data_width/cfg.xbar_bits)):
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
                hw_comp_access['alu_div'] += node_dut.tile_list[i].ima_list[j].alu_list[k].num_access_div + \
                        node_dut.tile_list[i].ima_list[j].alu_int.num_access_div

                hw_comp_access['alu_mul'] += node_dut.tile_list[i].ima_list[j].alu_list[k].num_access_mul + \
                        node_dut.tile_list[i].ima_list[j].alu_int.num_access_mul

                hw_comp_access['alu_other'] += node_dut.tile_list[i].ima_list[j].alu_list[k].num_access_other + \
                        node_dut.tile_list[i].ima_list[j].alu_int.num_access_other

                hw_comp_access['alu_act'] += node_dut.tile_list[i].ima_list[j].alu_list[k].num_access_act

                hw_comp_access['alu_sna'] += node_dut.tile_list[i].ima_list[j].alu_list[k].num_access_sna

            hw_comp_access['imem'] += node_dut.tile_list[i].ima_list[j].instrnMem.num_access

            hw_comp_access['dmem'] += node_dut.tile_list[i].ima_list[j].dataMem.num_access

            for k in range (cfg.num_xbar/(cfg.data_width/cfg.xbar_bits)):
                hw_comp_access['xbInmem_rd'] += node_dut.tile_list[i].ima_list[j].xb_inMem_list[k].num_access_read
                hw_comp_access['xbInmem_wr'] += node_dut.tile_list[i].ima_list[j].xb_inMem_list[k].num_access_write

            for k in range (cfg.num_xbar/(cfg.data_width/cfg.xbar_bits)):
                hw_comp_access['xbOutmem'] += node_dut.tile_list[i].ima_list[j].xb_outMem_list[k].num_access

    total_energy = 0
    # Compute the total dynamic energy consumption
    for key, value in hw_comp_access.items():
        total_energy += value * hw_comp_energy[key]

    # Write the dict comp_access & energy proportion to a file for visualization
    fid.write ('Access and energy distribution of dynamic energy: \n')
    fid.write ('Component                 num_access              percent\n')
    for key, value in hw_comp_access.items():
        # put extra spaces for better visulalization of values
        bl_spc1 = (28-len(key)) * ' '
        bl_spc2 = (22-len(str(value))) * ' '
        fid.write (key + bl_spc1 + str(value) + bl_spc2 +\
                    (str(value*hw_comp_energy[key]/total_energy*100))[0:4] + ' %\n')

    fid.write ('\n')


    # Evaluate leakage_energy (tile/ima/noc is power-gated if unused
    leakage_energy = sum_num_cycle_noc * param.noc_intra_pow_leak + \
            sum_num_cycle_tile * tile_metrics.compute_pow_leak_non_ima () + \
            sum_num_cycle_ima * ima_metrics.compute_pow_leak()


    # Write the leakage energy(J), total_energy(J), average_power (mW), peak_power (mW),
    # area (mm2), cycles and time (seconds) to a dict & file
    metric_dict = {'leakage_energy':0.0,
            'dynamic_energy':0.0,
            'total_energy':0.0,
            'average_power':0.0,
            'peak_power':0.0,
            'leakage_power':0.0,
            'area':0.0,
            'cycles':0,
            'time':0.0}

    metric_dict['leakage_power'] = node_metrics.compute_pow_leak () # in mW
    metric_dict['peak_power'] = node_metrics.compute_pow_peak () # in mW
    metric_dict['area'] = node_metrics.compute_area () # in mm2
    metric_dict['cycles'] = cycle
    metric_dict['time'] = cycle * param.cycle_time * (10**(-9)) # in sec
    metric_dict['dynamic_energy'] = total_energy * ns * mw # in joule
    #metric_dict['leakage_enegy'] = metric_dict['leakage_power'] * mw * metric_dict['time'] # in joule
    metric_dict['leakage_energy'] =  leakage_energy * ns * mw # in joule
    metric_dict['total_energy'] = metric_dict['dynamic_energy'] + metric_dict['leakage_energy']
    metric_dict['average_power'] = metric_dict['total_energy'] / metric_dict['time'] * (10**(3)) # in mW

    for key, value in metric_dict.items():
        fid.write (key + ': ' + str (value) + '\n')

    return metric_dict



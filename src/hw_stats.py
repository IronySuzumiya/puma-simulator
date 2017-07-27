# API to extract hardware trace (stats) from DPE execution
# Write to file

def hw_stats (fid, node):

    hw_comp = {'xbar':0,    'dac':0,    'snh':0,        'mux1':0,       'mux2':0,    'adc':0, \
           'alu':0,     'imem':0,   'dmem':0,       'xbInmem':0,    'xbOutmem':0, \
           'imem_t':0,  'rbuff':0,  'edram':0,      'edctrl':0, \
           'noc_intra':0,           'noc_inter':0
           }



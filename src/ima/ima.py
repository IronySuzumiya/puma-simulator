# Defines a configurable IMA module with its methods
import numpy as np
import constants as param
import ima_modules as imod

class ima (object):
    #######################################################
    ### Instantiate different (phycical + virtual) modules
    #######################################################
    def __init__ (self):

        ######################################################################
        ## Parametrically instantiate different physical IMA hardware modules
        ######################################################################
        # Instantiate crossbars
        self.xbar_list = []
        for i in xrange(param.num_xbar):
            temp_xbar = imod.xbar (param.xbar_size)
            self.xbar_list.append(temp_xbar)

        # Instantiate dac array (misnomer - is a list)
        self.dac_array = imod.dac_array (param.xbar_size, param.dac_res)

        # Instatiate adcs
        self.adc_list = []
        for i in xrange(param.num_adc):
            temp_adc = imod.adc (param.adc_res)
            self.adc_list.append(temp_adc)

        # Instantiate sample and hold
        self.snh_list = []
        for i in xrange(param.num_xbar):
            temp_snh = imod.sampleNhold (param.xbar_size)
            self.snh_list.append(temp_snh)

        # Instatiate mux (num_mux depends on num_xbars and num_adcs)
        # The mux design (described below) will vary (xbar_size = 64):
        # For 2 xbars with 1 ADC : Two 64-1 mux and One 2-1 mux
        # For 2 xbars with 2 ADCs: Two 64-1 mux
        # Similarly, 8 xbars & 1 ADC: Eight 64-1 mux and One 8-1 mux
        # *** Number of "xbar_size-1" muxes = num_xbar ***
        # *** Number of "(num_xbar/num_adc)-1" muxes = num_adcs ***

        self.mux1_list = [] # from xbar
        inp1_size = param.xbar_size
        for i in xrange(param.num_xbar):
            temp_mux = imod.mux (imp1_size)
            self.mux1_list.append(temp-mux)

        self.mux2_list = [] # to adc
        inp2_size = param.num-xbar / param.num_adc
        for i in xrange(inp2_size):
            temp_mux = imod.mux(imp1_size)
            self.mux2_list.append(temp_mux)

        # Instantiate ALUs
        self.alu_list = []
        for i in xrange(param.num_ALU):
            temp_alu = imod.alu ()
            self.alu_list.append(temp_alu)

        # Instantiate input memory (stores data)
        self.inmem = imod.memory (param.inMem_size)

        # Instantiate output memory (stores data)
        self.outmem = imod.memory (param.outMem_size)

        # Instantiate instruction memory (stores instruction)
        self.instrn_mem = imod.memory (param.instrMem_size)

        ##############################################################
        ## Define virtual (just for software emulation purpose) parts
        ##############################################################
        # used in Fetch stage
        self.pc = 0 # holds the next program counter value

        # used in Decode stage
        self.instrn = {} # holds the currently fetched instruction

        # used in Execute stage
        self.

        # used in Memory stage
        self.edram_addr = 0


    ############################################################
    ### Define what a pipeline stage does for each instruction
    ############################################################
    # "Fetch" stage (common to all instructions)
    def fetch (self):
        self.instrn = self.instrnmem.read (self.pc)
        self.pc = self.pc + 1

    # "Decode" stage - instruction specifc
    # Extracts operands and puts into the specific data structures
    def decode (self):
        def ld_dec (): self.edram_addr = self.inst.op1
        def st_dec (): self.edram-addr = self.inst.op1
        def mvm_dec (): self.



    # Decode stage is common to all instructions
    def instr_emulate (self, instrn, stage):

        # Fetch & Decode stages are common to all instructions
        def fetch (self, pc):
            instrn = self.instrnmem.read (pc)

        def dec (self,):


        def ld_ex  (self,):


        def ld_mem (self,):


        def ld_wb  (self,):


        # stages of LD (Load) instruction
        ld = {'fetch'    : fetch,
              'decode'   : ld_dec,
              'execute'  : ld_ex,
              'memory'   : ld_mem,
              'writeback': ld_wb}






        # stages of ST (Store) instruction
        st = {'fetch'    : fetch,
              'decode'   : st_dec,
              'execute'  : st_ex,
              'memory'   : st_mem,
              'writeback': st_wb}

        # stages of MVM (Matrix-Vector-Multiply) instruction
        mvm = {'fetch'    : fetch,
               'decode'   : mvm_dec,
               'execute'  : mvm_ex,
               'memory'   : mvm_mem,
               'writeback': mvm_wb}


        self.instrns = {'ld' : ld, 'st' : st, 'mvm' : mvm}

    # Emulate a particular instruction on IMA
    def emulate (instrn_list):




# Defines a configurable IMA module with its methods
import numpy as np
import constants as param
import ima_modules as imod

class ima (object):
    #######################################################
    ### Instantiate different modules
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

        # Instantiate DACs
        self.dacArray_list = []
        for i in xrange(param.num_xbar):
            temp_dacArray = imod.dac_array (param.xbar_size, param.dac_res)
            self.dacArray_list.append(temp_dacArray)

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

        # Instantiate  data memory (stores data)
        self.dataMem = imod.memory (param.dataMem_size)

        # Instantiate multiple xbar input memories (stores xbar input data)
        self.xb_inMem_list = []
        for i in xrange (param.num_xbar):
            temp_xb_inMem = imod.xb_inMem (param.xbar_size)
            self.xb_inMem_list.append(temp_xb_inMem)

        # Instantiate multiple xbar output memories (stores xbar output data)
        self.xb_outMem_list = []
        for i in xrange (param.num_xbar):
            temp_xb_outMem = imod.xb_outMem (param.xbar_size)
            self.xb_outMem_list.append(temp_xb_outMem)

        # Instantiate instruction memory (stores instruction)
        self.instrnMem = imod.instrn_memory (param.instrnMem_size)

        # Instantiate the memory interface (interface to edram controller)
        self.mem_interface = imod.mem_interface ()

        #############################################################################################################
        ## Define virtual (currently for software emulation purpose (doesn't have a corresponding hardware currenty)
        #############################################################################################################

        # List of supported opcodes/aluos
        op_list = ['ld', 'st', 'alu', 'alui', 'mvm']
        aluop_list = ['add', 'sub', 'shift_add']

        # Instruction is a dictionary of several fields
        temp_instrn = {'opcode' : op_list[0],       # instrn op
                       'aluop'  : aluop_list[0],    # alu function
                       'd1'     : 0,                # destination
                       'r1'     : 0,                # operand1
                       'r2'     : 0,                # opearnd2
                       'addr'   : 0,                # ext_mem (edram) address
                       'imm'    : 0,                # immediate (scalar) data
                       'xb_nma' : 0 }               # xbar negative-mask, a xbar evaluates if neg-mask = 1

        # Define stage-wise pipeline registers (f - before fetch, fd -fetch_decode, de - decode_execute)
        self.pc = 0 # holds the next program counter value

        self.fd_instrn = temp_instrn

        self.de_opcode = temp_instrn['opcode']
        self.de_aluop = temp_instrn['aluop']
        self.de_d1 = temp_instrn['d1'] # target register addr for alu/alui/ld
        self.de_addr = temp_instrn['addr'] # edram addr for ld/st
        self.de_imm = temp_instrn['imm'] # imm value for alui
        self.de_xb_nma = temp_instrn['xb_nma'] # nma value for xbar execution

        self.de_val1 = 0 # operand read from r1 address
        self.de_val2 = 0 # operand read from r2 address

        ########################################################
        ## Define book-keeping variables for pipeline execution
        ########################################################

        # List the pipeline stages
        self.stage_list = ['fet', 'dec', 'ex']
        self.num_stages = len (self.stage_list)

        # Define the book-keeping variables - stage-specific
        self.stage_empty = [0] * self.num_stage
        self.stage_cycle = [0] * self.num_stage
        self.stage_latency = [0] * self.num_stage # tells how many cycles will the current method running in a stage will require
        self.stage_done = [0] * self.num_stage

        # Define global pipeline variables
        self.cycles = 0

        # Define a halt signal - think about the logic later
        self.halt = 0


    ############################################################
    ### Define what a pipeline stage does for each instruction
    ############################################################
    # Increment stage cycles but update pipeline registers at end only

    # "Fetch" stage (common to all instructions)
    def fetch (self):
        sId = 0 # sId - stageId

        # First cycle - update the target latency
        if (self.stage_cycle[sId] == 0):
            self.stage_latency[sId] = self.instrnMem.getLatency ()
            self.stage_cycle[sId] = self.stage_cycle[sId] + 1

        # Other than first cycles (Note first and last cycle may be same)
        # Last cycle - update pipeline registers & done flag
        if (self.stage_latency[sId]-1 <= self.stage_cycle[sId] <= self.stage_latency[sId]):
            self.fd_instrn = self.instrnMem.read (self.pc)
            self.pc = self.pc + 1

            self.stage_done[stage_id] = 1
            self.stage_cycle[stage_id] = 0

        # For cycles other than first and last cycles
        elif (self.stage_cycle[sId] != 0):
            self.stage_cycle[sId] = self.stage_cycle[sId] + 1

    # "Decode" stage - Reads operands (if needed) and puts into the specific data structures
    def decode (self):
        sId = 1

        # common to all instructions
        dec_op = self.fd_instrn['opcode']
        assert (dec_op in op_list), 'unsupported opcode'

        self.de_opcode = dec_op

        # instruction specific (for eg: ld_dec - load's decode stage)
        if (dec_op == 'ld'):
            self.de_addr = self.fd_instrn['addr']
            self.de_d1 = self.fd_instrn['d1']

        elif (dec_op == 'st'):
            self.de_addr = self.fd_instrn['addr']
            self.de_val1 = self.inMem.read (self.fd_instrn['r1'])

        elif (dec_op == 'alu'):
            self.de_aluop = self.fd_instrn['aluop']
            self.de_d1 = self.fd_instrn['d1']
            self.de_val1 = self.inMem.read (self.fd_instrn['r1'])
            self.de_val2 = self.inMem.read (self.fd_instrn['r2'])

        elif (dec_op == 'alui'):
            self.de_aluop = self.fd_instrn['aluop']
            self.de_d1 = self.fd_instrn['d1']
            self.de_val1 = self.inMem.read (self.fd_instrn['r1'])
            self.de_val2 = self.fd_instrn['imm']

        else: # mvm instrn
            xb_nma = self.fd_instrn['xb_nma']
            assert (0 <= xb_nma <= param.num_xbar), 'unsupported xbar configuration'
            self.de_xb_nma = xb_nma

    # Execute stage - compute and store back to registers
    def execute (self):
        sId = 2

        # common to all instructions
        ex_op = self.de_opcode
        assert (ex_op in op_list), 'unsupported opcode'

        # instruction specific
        if (ex_op == 'ld'):
            ren = 1
            self.mem_interface.request (ren, self.de_addr,)
            # waits until data is brought from edram
            if (self.mem_interface.wait_in == 0):
                data = self.mem_interface.data_in
                self.outMem.write (self.de_d1, data)

        elif (ex_op == 'st'):
            self.mem_interface.request (ren, self.de_addr, self.de_val1)
            # waits until store finishes
            ## Incomplete

        elif (ex_op == 'alu'): #multiple ALUs in parallel will be used in ALUvec instrn
            # compute in ALU
            out = self.alu_list[0].propagate (self.de_val1, self.de_val2, self.de_aluop)
            # write to outMem
            self.outMem.write (self.de_d1, out)

        elif (ex_op == 'alui'):
            # compute in ALU
            out = self.alu_list[0].propagate (self.de_val1, self.de_val2, self.de_aluop)
            # write to outMem
            self.outMem.write (self.de_d1, out)

        else: # mvm instrn
            # traverse through the xbars - (nma is the number of crossbars which will evaluate)
            for i in xrange (self.de_xb_nma):

                ## Loop to cover all bits of inputs
                    # read the values from the xbar's input register
                    out_xb_inMem = self.xb_inMem_list[i].read ()

                    # convert digital values to analog
                    out_dac = self.dacArray_list[i].propagate (out_xb_inMem)
                    out_dac = np.asarray (out_dac)

                    # compute dot-product
                    out_xbar = self.xbar_list[i].propagate (out_dac)

                    # do sampling and hold
                    out_snh = self.snh_list[i].propagate (out_xbar)

                    # convert from analog to digital

                    # shift and add

                    # store back to xbar's output register

    #####################################################
    ## Define how pipeline executes
    #####################################################
    def pipe_init (self):
        self.cycles = 0

        zero_list = [0] * self.num_stages
        self.stage_empty = zero_list
        self.stage_cycle = zero_list
        self.stage_done = zero_list

    def run (self):
        # define a list for individual stage executions
        run_stage = [self.fetch, self.decode, self.execute]

        # Initialize the pipeline
        self.pipe_init ()

        # Run the pipeline
        while (!self.halt):
            # Each iteration of while loop is a cycle of ima pipeline execution
            # Simulate each stage - start from the last stage - except the fetch stage
            for i in range (self.num_stages, 0, -1):
                # Check if the instruction in stage 'i-1' can be moved to stage 'i'
                if (self.stage_done[i] & self.stage_done[i-1]):
                    self.stage_empty[i] = self.stage_empty[i-1]
                    self.stage_done[i] = 0

                # Simulate one cycle of execution of stage 'i'
                run_stage[i]

            # Simulate 'Fetch' stage
            if (self.pc <= param.instrnMem_size):
                # Check if the previous stage finished
                if (self.stage_done[0]):
                    self.stage_done[0] = 0

                # Simulate a cycle of fetch stage
                run_stage[0]
            else:
                self.stage_empty[0] = 1

            # Check for halt condition - halt when all stages are empty
            if (self.cycles != 0 and self.stage_empty == zero_list):
                self.halt = 1
            else:
                self.cycles = self.cycles + 1

        print ('IMA ran for' + self.cycles + 'cycles')
        return


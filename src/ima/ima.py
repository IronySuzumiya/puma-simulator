# Defines a configurable IMA module with its methods

# add the folder location for include files
import sys
sys.path.insert (0, '/home/ankitaay/dpe/include')

# import dependancy files
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
        # *** Number of "xbar_size" muxes = num_xbar ***
        # *** Number of "(num_xbar/num_adc)" muxes = num_adcs ***
        # A mux with inp_size = 1 is basically a dammy mux (wire)

        self.mux1_list = [] # from xbar
        inp1_size = param.xbar_size
        for i in xrange(param.num_xbar):
            temp_mux = imod.mux (inp1_size)
            self.mux1_list.append(temp_mux)

        self.mux2_list = [] # to adc
        inp2_size = param.num_xbar / param.num_adc
        for i in xrange(param.num_adc):
            temp_mux = imod.mux (inp2_size)
            self.mux2_list.append(temp_mux)

        # Instantiate ALUs
        self.alu_list = []
        for i in xrange(param.num_ALU):
            temp_alu = imod.alu ()
            self.alu_list.append(temp_alu)

        # Instantiate  data memory (stores data)
        self.dataMem = imod.memory (param.dataMem_size, param.num_xbar * param.xbar_size)

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
        self.op_list = ['ld', 'st', 'alu', 'alui', 'mvm', 'hlt']
        self.aluop_list = ['add', 'sub', 'shift_add']

        # Instruction is a dictionary of several fields
        temp_instrn = {'opcode' : self.op_list[0],      # instrn op
                       'aluop'  : self.aluop_list[0],   # alu function
                       'd1'     : 0,                    # destination
                       'r1'     : 0,                    # operand1
                       'r2'     : 0,                    # opearnd2
                       'addr'   : 0,                    # ext_mem (edram) address
                       'imm'    : 0,                    # immediate (scalar) data
                       'xb_nma' : 0 }                   # xbar negative-mask, a xbar evaluates if neg-mask = 1

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
        self.num_stage = len (self.stage_list)

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
    # Increment stage cycles but update pipeline registers at end only when update_ready flag is set

    # "Fetch" stage (common to all instructions)
    def fetch (self, update_ready):
        sId = 0 # sId - stageId

        # Define what to do in fetch
        def do_fetch (self):
            # commmon to all instructions
            self.fd_instrn = self.instrnMem.read (self.pc) # update pipeline register (fetch/decode)
            self.stage_empty[sId+1] = 0

            self.pc = self.pc + 1 # update pipeline register before fetch stage
            self.stage_empty[sId] = 0


        # Describe the functionality on a cycle basis
        # First cycle - update the target latency
        if (self.stage_cycle[sId] == 0 and self.stage_empty[sId] != 1):
            self.stage_latency[sId] = self.instrnMem.getLatency()

            # Check if first = last cycle
            if (self.stage_latency[sId] == 1 and update_ready):
                do_fetch (self)
                self.stage_done[stage_id] = 1
                self.stage_cycle[sId] = 0
                self.stage_empty[sId] = 1
            else:
                self.stage_cycle[sId] = self.stage_cycle[sId] + 1

        # Last cycle - update pipeline registers & done flag
        elif (self.stage_cycle[sId] >= self.stage_latency[sId]-1 and update_ready):
            do_fetch (self)
            self.stage_done[sId] = 1
            self.stage_cycle[sId] = 0
            self.stage_empty[sId] = 1

        # For all other cycles
        else:
            self.stage_cycle[sId] = self.stage_cycle[sId] + 1


    # "Decode" stage - Reads operands (if needed) and puts into the specific data structures
    def decode (self, update_ready):
        sId = 1

        # Define what to do in decode (done for conciseness)
        def do_decode (self, dec_op):
            # common to all instructions
            self.de_opcode = dec_op
            self.stage_empty[sId+1] = 0

            # instruction specific (for eg: ld_dec - load's decode stage)
            if (dec_op == 'ld'):
                self.de_addr = self.fd_instrn['addr']
                self.de_d1 = self.fd_instrn['d1']

            elif (dec_op == 'st'):
                self.de_addr = self.fd_instrn['addr']
                self.de_val1 = self.dataMem.read (self.fd_instrn['r1'])

            elif (dec_op == 'alu'):
                self.de_aluop = self.fd_instrn['aluop']
                self.de_d1 = self.fd_instrn['d1']
                self.de_val1 = self.dataMem.read (self.fd_instrn['r1'])
                self.de_val2 = self.dataMem.read (self.fd_instrn['r2'])

            elif (dec_op == 'alui'):
                self.de_aluop = self.fd_instrn['aluop']
                self.de_d1 = self.fd_instrn['d1']
                self.de_val1 = self.dataMem.read (self.fd_instrn['r1'])
                self.de_val2 = self.fd_instrn['imm']

            elif (dec_op == 'mvm'):
                xb_nma = self.fd_instrn['xb_nma']
                assert (0 <= xb_nma <= param.num_xbar), 'unsupported xbar configuration'
                self.de_xb_nma = xb_nma


        # Describe the functionality on a cycle basis
        # First cycle - update the target latency
        if (self.stage_cycle[sId] == 0 and self.stage_empty[sId] != 1):
            # Check for assertion pass
            dec_op = self.fd_instrn['opcode']
            assert (dec_op in self.op_list), 'unsupported opcode'

            self.stage_latency[sId] = self.dataMem.getLatency()

            # Check if first = last cycle
            if (self.stage_latency[sId] == 1 and update_ready):
                do_decode (self, dec_op)
                self.stage_done[sId] = 1
                self.stage_cycle[sId] = 0
                self.stage_empty[sId] = 1
            else:
                self.stage_cycle[sId] = self.stage_cycle[sId] + 1

        # Last cycle - update pipeline registers (if ??) & done flag
        elif (self.stage_cycle[sId] >= self.stage_latency[sId]-1 and update_ready):
            dec_op = self.fd_instrn['opcode']
            do_decode (self, dec_op)
            self.stage_done[sId] = 1
            self.stage_cycle[sId] = 0
            self.stage_empty[sId] = 1

        # For all other cycles
        else:
            self.stage_cycle[sId] = self.stage_cycle[sId] + 1


    # Execute stage - compute and store back to registers
    def execute (self):
        sId = 2

        # Define what to do in execute (done for conciseness)
        def do_execute (self, ex_op):
            if (ex_op == 'ld'):
                ren = 1
                self.mem_interface.request (ren, self.de_addr)
                # waits until data is brought from edram
                #if (self.mem_interface.wait_in == 0):
                #    data = self.mem_interface.data_in
                #    self.outMem.write (self.de_d1, data)
                data = self.mem_interface.data_in  # temporary
                self.outMem.write (self.de_d1, data) # temporary

            elif (ex_op == 'st'):
                ren = 0
                self.mem_interface.request (ren, self.de_addr, self.de_val1)
                # waits until store finishes
                ## Incomplete

            elif (ex_op == 'alu'): #multiple ALUs in parallel will be used in ALUvec instrn
                # compute in ALU
                out = self.alu_list[0].propagate (self.de_val1, self.de_val2, self.de_aluop)
                # write to outMem
                self.dataMem.write (self.de_d1, out)

            elif (ex_op == 'alui'):
                # compute in ALU
                out = self.alu_list[0].propagate (self.de_val1, self.de_val2, self.de_aluop)
                # write to outMem
                self.dataMem.write (self.de_d1, out)

            elif (ex_op == 'mvm'):
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

                        for j in xrange (param.xbar_size):
                            # convert from analog to digital
                            out_adc = self.adc_list[i].propagate (out_snh)
                            # read from xbar's output register
                            out_xb_outMem = self.xb_outMem_list[i].read (j)
                            # shift and add - make a dedicated sna unit -- PENDING
                            out_sna = self.alu_list[0].propagate (out_xb_outMem, out_adc)
                            # store back to xbar's output register
                            self.outMem_list[i].write (out_sna)

            else: # for halt instruction
                self.halt = 1


        # Computes the latency for mvm instruction based on DPE configuration
        def xbComputeLatency (self):
            # assumption1: num_adc = num_s&a = num_outReg_Ports
            # assumption2: an adc connects to only one xbar
            # assumption3: shift&add unit is seen as an alu for now
            # assumption4: two stage pipeline - unit1 & unit2 as shown below

            # using '\' to continue on enxt line
            latency_unit1 =  self.xb_inMem_list[0].getLatency() +\
                            self.dacArray_list[0].getLatency() +\
                            self.xbar_list[0].getLatency() +\
                            self.snh_list[0].getLatency()

            latency_unit2 = param.xbar_size * (self.mux1_list[0] +\
                                               self.mux2_list[0] +\
                                               self.adc_list[0] +\
                                               self.alu_list[0] +\
                                               self.xb_outMem_list[0]) *\
                            param.num_xbar/param.num_adc

            latency_unit = max (latency_unit1, latency_unit2)

            return (param.xbdata_width / param.dac_res) * latency_unit


        # Describe the functionality on a cycle basis
        # First cycle - update the target latency
        if (self.stage_cycle[sId] == 0 and self.stage_empty[sId] != 1):
            # Check for assertion pass
            ex_op = self.de_opcode
            assert (ex_op in self.op_list), 'unsupported opcode'

            # assign execution unit based stage latency
            if (ex_op == ('ld' or 'st')):
                self.stage_latency[sId] = self.mem_interface.getLatency()
            elif (exop == 'alu' or exop == 'alui'):
                # ALU instructions access ALU and write to memory
                self.stage_latency[sId] = self.alu_list[0].getLatency() +\
                                          self.dataMem.getLatency()
            else: # for xbar operation
                self.stage_latency[sId] = xbComputeLatency (self)

            # Check if first = last cycle
            if (self.stage_latency[sId] == 1 and update_ready):
                do_execute (self, ex_op)
                self.stage_done[sId] = 1
                self.stage_cycle[sId] = 0
                self.stage_empty[sId] = 1

            else:
                self.stage_cycle[sId] = self.stage_cycle[sId] + 1

        # Last cycle - update pipeline registers (if ??) & done flag
        elif (self.stage_cycle[sId] >= self.stage_latency[sId]-1 and update_ready):
            ex_op = self.de_opcode
            do_execute (self, ex_op)
            self.stage_done[sId] = 1
            self.stage_cycle[sId] = 0
            self.stage_empty[sId] = 1

        # For all other cycles
        else:
            self.stage_cycle[sId] = self.stage_cycle[sId] + 1


    #####################################################
    ## Define how pipeline executes
    #####################################################
    def pipe_init (self):
        self.cycles = 0
        self.halt = 0

        zero_list = [0] * self.num_stage
        one_list = [1] * self.num_stage
        self.stage_empty = zero_list
        self.stage_cycle = zero_list
        self.stage_done = one_list

        #Initialize the instruction memory
        dict_list = np.load('imem.npy')
        self.instrnMem.load(dict_list)

    def pipe_run (self):
        # define a list for individual stage executions
        run_stage = [self.fetch, self.decode, self.execute]

        # Run the pipeline
        while (self.halt != 1):
            # Each iteration of while loop is a cycle of ima pipeline execution

            # Traverse the pipeline to update the update_ready flag
            update_ready = [0] * self.num_stages
            for i in range (self.num_stages-1,-1,-1):
                if (i == 2): #Execute stage
                    update_ready[i] == 1
                else:
                    if (self.stage_done[i+1] == 1):
                        update_ready[i] = 1

            # Run the pipeline stages based on the update_ready flags
            self.execute (update_read[2])
            self.decode (update_read[1])
            self.fetch (update_read[0])

            # Check for halt condition
            if (self.halt != 1):
                self.cycles = self.cycles + 1

        print ('IMA ran for' + self.cycles + 'cycles')


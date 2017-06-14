# Generates instructions that are used by ima
import numpy as np
import constants

filename = 'imem.npy'

num_instrn = constants.instrnMem_size

# List of supported opcodes/aluos
op_list = ['ld', 'st', 'alu', 'alui', 'mvm', 'hlt']
aluop_list = ['add', 'sub', 'shift_add']

# Instruction format
temp_instrn = {'opcode' : op_list[0],      # instrn op
               'aluop'  : aluop_list[0],   # alu function
               'd1'     : 0,               # destination
               'r1'     : 0,               # operand1
               'r2'     : 0,               # opearnd2
               'addr'   : 0,               # ext_mem (edram) address
               'imm'    : 0,               # immediate (scalar) data
               'xb_nma' : 0 }              # xbar negative-mask, a xbar evaluates if neg-mask = 1

dict_list = []
for i in xrange(num_instrn):
    dict_list.append(temp_instrn)

np.save(filename, dict_list)

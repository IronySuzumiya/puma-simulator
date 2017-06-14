## Testing the invidual modules in an IMA
import numpy as np
import ima_modules as ima
import constants


### Check xbar class methods
##xb_size = 2
##wt = np.random.rand(2,2)
##inp = np.ones(2)
##xbar1 = xbar(xb_size)
###xbar1 = xbar(xb_size, wt)
##out = xbar1.propagate(inp)
##print('output', out)


### Check ima class methods
##num_xbar = 1
##xbar_size = 2
##wt_list = []
##inp_list = []
##for i in xrange(num_xbar):
##    wt_list.append(np.random.rand(xbar_size,xbar_size))
##    inp_list.append(np.ones(xbar_size))
##ima1 = xbar.ima(num_xbar, xbar_size, wt_list)
##ima1.propagate(inp_list)


### Check the dac_array class methods
##inp_list = ['00', '01', '10', '11']
##dac_array = ima.dac_array (constants.xbar_size, constants.dac_res)
##out_list = dac_array.propagate (inp_list)
##print (out_list)


### Check the adc class method
##inp_list = [0.9, 0.74, 0.24, 0.49]
##adc = ima.adc (constants.adc_res)
##out = adc.propagate (inp_list[1])
##print (out)


### Check sample&hold class methods
##snh = ima.sampleNhold(constants.xbar_size)
##inp_list = [2,3,4,5]
##print(snh.propagate(inp_list))


### Check mux class methods
##mux = ima.mux(3)
##inp_list = [1,2,3]
##print(mux.propagate(inp_list,0))


### Check alu class methods
##alu = ima.alu()
##print (alu.propagate(2,3,'shift_add'))


### Check the memory class methods
##mem = ima.memory(constants.dataMem_size)
##print ('initial', mem.memfile)
##addr = constants.xbar_size
##mem.write(addr, '1001'*4)
##print('post-write', mem.memfile)
##print('read', mem.read(addr))
##print (mem.getLatency())

### Check the instruction memory class methods
##mem = ima.instrn_memory(constants.instrnMem_size)
##print ('initial', mem.memfile)
##addr = 64
##data = {'a':1, 'b':2}
##mem.write(addr, data)
##print('post-write', mem.memfile)
##print('read', mem.read(addr))
##print (mem.getLatency())

### Check the xbar input memory and methods
##xb_inMem = ima.xb_inMem (constants.xbar_size)
##print (xb_inMem.getLatency ())
##addr = 2
##data = 4*'10'
##dac_res = 2
##print (xb_inMem.memfile)
##xb_inMem.write (addr, data)
##print (xb_inMem.memfile)
##print (xb_inMem.read(dac_res))
##print (xb_inMem.memfile)
##xb_inMem.reset ()
##print (xb_inMem.memfile)

### Check the xbar input memory and methods
##xb_outMem = ima.xb_outMem (constants.xbar_size)
##print ('latency', xb_outMem.getLatency ())
##data = 4*'10'
##dac_res = 2
##print ('initial', xb_outMem.memfile)
##xb_outMem.write (data)
##print ('post-write', xb_outMem.memfile)
##print ('write pointer', xb_outMem.wr_pointer)
##
##data = 4*'11'
##xb_outMem.write (data)
##print ('post-write', xb_outMem.memfile)
##print ('write pointer', xb_outMem.wr_pointer)
##
##addr = 1
##print ('read',xb_outMem.read(addr))
##xb_outMem.reset ()
##print (xb_outMem.memfile)

# memory interface
# function to probe the interface signals
def probe (interface):
    print (interface.wait_in)
    print (interface.data_in)
    print (interface.req_out)
    print (interface.ren_out)
    print (interface.addr_out)
    print (interface.data_out)
    
mem_interface = ima.mem_interface()
print ('latency\n', mem_interface.getLatency ())

print ('ld')
addr = 2
ren = 1
mem_interface.request (ren, addr)
print ('probe all the in/out signals')
probe(mem_interface)
print ('\n')

print ('Acknowledge ld')
data = '10'
mem_interface.ack (data)
print ('probe all the in/out signals')
probe(mem_interface)
print ('\n')

print ('st')
addr = 2
ren = 1
data = '1010'
mem_interface.request (ren, addr, data)
print ('probe all the in/out signals')
probe(mem_interface)
print ('\n')

print ('Acknowledge st')
mem_interface.ack ()
print ('probe all the in/out signals')
probe(mem_interface)
print ('\n')

print ('check reset')
mem_interface.reset ()
print ('probe all the in/out signals')
probe(mem_interface)
print ('\n')





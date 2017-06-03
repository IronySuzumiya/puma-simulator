import ima_modules
import ima
import numpy as np
## Testing

### Check xbar class methods
##xb_size = 2
##wt = np.random.rand(2,2)
##inp = np.ones(2)
##xbar1 = xbar(xb_size)
###xbar1 = xbar(xb_size, wt)
##out = xbar1.propagate(inp)
###print('output', out)

# Check ima class methods
num_xbar = 1
xbar_size = 2
wt_list = []
inp_list = []
for i in xrange(num_xbar):
    wt_list.append(np.random.rand(xbar_size,xbar_size))
    inp_list.append(np.ones(xbar_size))
ima1 = xbar.ima(num_xbar, xbar_size, wt_list)
ima1.propagate(inp_list)

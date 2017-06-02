# Defining xbar object and its methods - propagate, update
import numpy as np
#import constants

##class ima(object):
##    def __init__(self, num_xbar, xbar_size, xbar_value_list = 'nil')
##    # xbar_value_list is the list of weights of all crossbars in ima
##        # generate multiple crossbars
##        for i in xrange(num_xbar):
##            xbar[]
##        
##        
    

class xbar (object):
    def __init__(self, xbar_size, xbar_value = 'nil'):
    # xbar_value is the weights meant for one crossbar
        self.xbar_size = xbar_size
        self.xbar = np.zeros((xbar_size, xbar_size), dtype=float)
        if (xbar_value != 'nil'):
            self.xbar = xbar_value

    def propagate(self, inp):
        assert (len(inp) == self.xbar_size), 'input to xbar is of wrong size'
        return inp * self.xbar


# Check class function
xb_size = 2
wt = np.random.rand(2,2)
inp = np.ones(2)

print('weight', wt)
print('input', inp)

xbar1 = xbar(xb_size, wt)
out = xbar1.propagate(inp)

print('output', out)

# Defines an ima and its methods
import ima_modules

class ima (object):
    def __init__ (self, num_xbar, xbar_size, xbar_value_list = 'nil'):
        # xbar_value_list is the list of weights of all crossbars in ima
        # generate multiple crossbars
        self.xbar_list = []
        self.num_xbar = num_xbar
        self.xbar_size = xbar_size
        for i in xrange(num_xbar):
            temp_xbar = xbar(xbar_size, xbar_value_list[i])
            self.xbar_list.append(temp_xbar)

    def propagate (self, inp_list = 'nil'):
        assert (inp_list != 'nil'), 'propagate needs a non-nil input'
        assert (np.shape(inp_list) == (self.num_xbar, self.xbar_size)), 'ima input size mismatch'
        out_xbar_list = []
        for i in xrange(self.num_xbar):
            out_xbar_temp = self.xbar_list[i].propagate(inp_list[i])
            out_xbar_list.append(out_xbar_temp)
        return (out_xbar_list)

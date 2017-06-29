-- API to implement an LSTM cell
torch.setdefaulttensortype('torch.FloatTensor')
require 'nn'

-- input and hidden state sizes
in_size = 4
h_size = 3

-- Specify the non-linearities
nl1 = nn.Sigmoid ()
nl2 = nn.Tanh ()

-- specify the transformation matices (for preactivations)
i2h_mat = torch.rand (in_size, 4 * h_size)
h2h_mat = torch.rand (h_size, 4 * h_size)
bias_vec = torch.rand(1, 4 * h_size)

-- specify the input and hidden state, IMA Vector LD (2 Loads)
inp = torch.rand (1, in_size)
h_prev = torch.rand (1, h_size)
c_prev = torch.rand (1, h_size)

-- IMA MVM
preact_inp = inp * i2h_mat
preact_h = h_prev * h2h_mat

-- IMA Vector Add
temp_out = preact_inp + preact_h

-- IMA Vector Add
out = temp_out + bias_vec

-- IMA Vector Non-Linear operations
i_gate = nl1:forward(out)[{{1}, {0*h_size+1, 0*h_size+h_size}}]
f_gate = nl1:forward(out)[{{1}, {1*h_size+1, 1*h_size+h_size}}]
o_gate = nl1:forward(out)[{{1}, {2*h_size+1, 2*h_size+h_size}}]
c_int = nl2:forward(out)[{{1}, {3*h_size+1, 3*h_size+h_size}}]

-- Update the cell state
-- 2 IMA  Vector multiply & 1 IMA Vector ADD
c_t = torch.cmul (f_gate, c_prev) + torch.cmul (i_gate, c_int)

-- IMA Vector Non-linearity and Vector Multiply
h_t = torch.cmul (o_gate, nl2:forward(c_t))

print ('Cell state', c_t, 'Hidden state', h_t)


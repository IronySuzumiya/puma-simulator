-- Doing some matrix computation, arithmetic and some non-liar operation in
-- Check against its implementation on DPE
-- Produce input files, matrix files, output files
torch.setdefaulttensortype('torch.FloatTensor')

-- fix seed
torch.manualSeed(1)

invec_size = 4
inp = torch.randn (1, invec_size)
xbar = torch.rand (invec_size, invec_size)
out = inp * xbar


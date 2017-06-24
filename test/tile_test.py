# Test script for tile simulations
tarcepath = '/home/ankitaay/dpe/test/'

import sys, getopt
sys.path.insert (0, '/home/ankitaay/dpe/include')
sys.path.insert (0, '/home/ankitaay/dpe/src/')

import numpy as np
import constants as param
import ima
import ima_modules
import generate_inst
import tile_modules
import tile

# Instantiate the tile under test
tile = tile.tile ()

# Generate the instruction file(s) for ima(s)
generate_inst.generate_inst ()

# Initialize the tile
tile.tile_init ()

# Run the tile
cycle = 0
while (all(tile.halt_list) != 1):
    tile.tile_run (cycle)
    cycle = cycle + 1

print 'Finally tile halted'

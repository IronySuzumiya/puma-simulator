# Defines a configurable tile with its methods

import sys, json
sys.path.insert (0, '/home/ankitaay/dpe/include')
sys.path.insert (0, '/home/ankitaay/dpe/src/ima')
sys.path.insert (0, '/home/ankitaay/dpe/src/itile')

import numpy as np
import constants as param
import ima as ima
import tile_modules as tmod

# IMA specific modules (should not be needed)
import ima_modules
import generate_inst

class tile (object):

    # Instantiate different modules
    def __init__ (self):
        self.ima_list = []
        for i in range (param.num_ima):
            temp_ima = ima.ima ()
            self.ima_list.append(temp_ima)

        self.edram_controller = tmod.edram_controller ()

    # Write a init function
    def tile_init (self):

    # Write a tile_run function
    self tile_rin (self):

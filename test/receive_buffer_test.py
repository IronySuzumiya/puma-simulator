# Test Receive buffer in tile_modules

import sys
sys.path.insert (0, '/home/ankitaay/dpe/include')
sys.path.insert (0, '/home/ankitaay/dpe/src/')
import constants as param
import tile_modules as tmod

# instantiate receive buffer
buff = tmod.receive_buffer (param.receive_buffer_size)

# invalidate all entries
buff.inv ()

# check if buffer empty
print ('Buffer empty status:', buff.isempty())

# write to buffer
temp_dict = {'data':'10101111', \
             'neuron_id': 1}
buff.write (temp_dict)
print ('checking first write', buff.buffer)

# check if buffer empty
print ('Buffer empty status:', buff.isempty())

# check if buffer full
print ('Buffer full status:', buff.isfull())

# write to buffer
temp_dict = {'data':'00001111', \
             'neuron_id': 2}
buff.write (temp_dict)
print ('checking second write', buff.buffer)

# check if buffer full
print ('Buffer full status:', buff.isfull())

# attempt a read for hit
neu_id = 2
[hit, data] = buff.read (neu_id)
print ('Tag hit expected, actual: ', hit, 'data', data)
print ('Buffer contents', buff.buffer)

# attempt a read for miss
neu_id = 2
[hit, data] = buff.read (neu_id)
print ('Tag hit not expected, actual: ', hit, 'data', data)
print ('Buffer contents', buff.buffer)



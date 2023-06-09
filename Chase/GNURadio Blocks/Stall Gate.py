"""
Embedded Python Blocks:

Each example_param this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, example_param=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Stall Gate',   # will show up in GRC
            in_sig=[np.byte],
            out_sig=[np.byte]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.example_param = example_param
        self.toggle = 0
        self.clock = 0



    def work(self, input_items, output_items):

        if (self.toggle == 0):
                if (np.any(input_items[0] == 1)):
                        self.toggle = 1
                        output_items[0][:] = 1
                else:
                        output_items[0][:] = 0
        if (self.toggle == 1):
                output_items[0][:] = 1
                self.clock = self.clock+1
                if (self.clock >= self.example_param):
                        self.toggle = 0
                        self.clock = 0
                        output_items[0][:] = 0
        return len(output_items[0])

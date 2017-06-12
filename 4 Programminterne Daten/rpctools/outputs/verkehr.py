# -*- coding: utf-8 -*-

from rpctools.utils.output import Output


class VerkehrOutput(Output):
    _workspace = 'FGDB_Verkehr.gdb'

    def define_outputs(self):
        # Add Layers
        self.add_layer('verkehr', 'Zielpunkte',
                       featureclass='Zielpunkte',
                       template_folder='Verkehr')
        
        self.add_layer('verkehr', 'links',
                       featureclass='links',
                       template_folder='Verkehr')
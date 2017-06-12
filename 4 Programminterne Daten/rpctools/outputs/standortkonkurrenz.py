# -*- coding: utf-8 -*-

from rpctools.utils.output import Output


class MarketsOutput(Output):
    _workspace = 'FGDB_Standortkonkurrenz_Supermaerkte.gdb'
    
    def define_outputs(self):
        group_layer = ("standortkonkurrenz")
        fc = 'Maerkte'
        layer_nullfall = 'Märkte Nullfall'
        layer_planfall = 'Märkte Planfall'
        
        self.add_layer(group_layer, layer_nullfall, fc, zoom=False)
        self.add_layer(group_layer, layer_planfall, fc, zoom=False)
# -*- coding: utf-8 -*-

from rpctools.utils.output import Output


class VerkehrOutput(Output):

    def add_outputs(self):
        # Add Layers
        self.add_layer('verkehr', 'Zielpunkte',
                       featureclass='Zielpunkte',
                       template_folder='Verkehr')
        
        #lyr_nodes = self.folders.get_layer('nodes', 'Verkehr')
        #fc_nodes = self.folders.get_table('nodes')
        #self.output.add_output('verkehr', lyr_nodes, fc_nodes)
        
        self.add_layer('verkehr', 'links',
                       featureclass='links',
                       template_folder='Verkehr')
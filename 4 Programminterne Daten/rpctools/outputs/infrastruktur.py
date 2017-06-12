# -*- coding: utf-8 -*-

from rpctools.utils.output import Output
from rpctools.diagrams.infrastruktur import MassnahmenKosten, Netzlaenge


class InfrastrukturOutput(Output):
    _workspace = 'FGDB_Kosten.gdb'
    
    def define_outputs(self):
        self.add_diagram(MassnahmenKosten, Netzlaenge)
        group_layer = "infrastruktur"
        
        fc = 'Erschliessungsnetze_Linienelemente'
        layer = "Erschließungsnetz"
        self.add_layer(group_layer, layer, fc, zoom=False)
    
        fc = 'Erschliessungsnetze_Punktelemente'
        layer = "Erschließungsnetz - punktuelle Maßnahmen" 
        self.add_layer(group_layer, layer, fc, zoom=False)
        


# -*- coding: utf-8 -*-
import sys
import datetime
import arcpy
from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode
import pandas as pd
import numpy as np
from rpctools.diagrams.infrastruktur import MassnahmenKosten, Netzlaenge


class InfrastrukturmengenBilanz(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Kosten.gdb'
    
    def add_outputs(self):
        group_layer = 'infrastruktur'
        fc = 'Erschliessungsnetze_Linienelemente'
        layer = "Erschließungsnetz"
        self.output.add_layer(group_layer, layer, fc, zoom=False)
    
        fc = 'Erschliessungsnetze_Punktelemente'
        layer = "Erschließungsnetz - punktuelle Maßnahmen" 
        self.output.add_layer(group_layer, layer, fc, zoom=False)
        
        kosten_diagram = MassnahmenKosten()
        kosten_diagram.create()
    
        netz_diagram = Netzlaenge()
        netz_diagram.create()
        
        self.output.add_diagram(kosten_diagram, netz_diagram)
        
    def run(self):
        self.output.show_diagrams()


class TbxInfrastrukturmengenBilanz(Tbx):
    """Toolbox Projekt loeschen"""
    @property
    def label(self):
        return u'Schritt ?: Infrastrukturmengen bilanzieren'

    @property
    def Tool(self):
        return InfrastrukturmengenBilanz

    def _getParameterInfo(self):

        # Bestehendes_Projekt_auswählen
        p = self.add_parameter('projectname')
        p.name = encode('Projekt')
        p.displayName = encode('Projekt')
        p.parameterType = 'Required'
        p.direction = 'Input'
        p.datatype = 'GPString'
        p.filter.list = []

        return self.par

    def _updateParameters(self, params):
        pass
    
if __name__ == "__main__":
    t = TbxInfrastrukturmengenBilanz()
    t.getParameterInfo()
    t.par.projectname.value = t.config.active_project
    t.execute()
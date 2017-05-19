# -*- coding: utf-8 -*-
import sys
import datetime
import arcpy
from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode
import pandas as pd
import numpy as np
from rpctools.diagrams.infrastruktur import Netzlaenge, MassnahmenKosten


class InfrastrukturmengenBilanz(Tool):
    _param_projectname = 'projectname'
    _workspace = 'FGDB_Kosten.gdb'
    _group_layer = "infrastruktur"
    _line_layer = "Erschließungsnetz"
    _point_layer = "Erschließungsnetz - punktuelle Maßnahmen" 
    _line_table = 'Erschliessungsnetze_Linienelemente'
    _point_table = 'Erschliessungsnetze_Punktelemente'    
    
    def add_output(self):
        # add Erschliessungsnetz
        fc = self.folders.get_table(self._line_table)
        layer = self.folders.get_layer(self._line_layer)
        self.output.add_output(self._group_layer, layer, fc, zoom=False)
        
        fc = self.folders.get_table(self._point_table)
        layer = self.folders.get_layer(self._point_layer)
        self.output.add_output(self._group_layer, layer, fc, zoom=False)
        
    def run(self):
        netz_diagram = Netzlaenge()
        netz_diagram.create()
        netz_diagram.show()
        kosten_diagram = MassnahmenKosten()
        kosten_diagram.create()
        kosten_diagram.show()


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
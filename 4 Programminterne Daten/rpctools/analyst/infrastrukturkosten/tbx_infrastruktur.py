# -*- coding: utf-8 -*-

import datetime
import arcpy
from rpctools.utils.params import Tbx, Tool
from rpctools.utils.encoding import encode

class Infrastruktur(Tool):    
    _param_projectname = 'projectname'
    _dbname = 'FGDB_Kosten.gdb'

    def add_output(self):
        # add Erschliessungsnetz
        fc = self.folders.get_table("Erschliessungsnetze_Linienelemente")
        layer = self.folders.get_layer("Erschließungsnetz")
        self.output.add_output("infrastruktur", layer, fc, zoom=False)
        
        fc = self.folders.get_table("Erschliessungsnetze_Punktelemente")
        layer = self.folders.get_layer("Erschließungsnetz - "
                                       "punktuelle Maßnahmen")
        self.output.add_output("infrastruktur", layer, fc, zoom=False)
    
    def run(self):
        pass


class TbxInfrastruktur(Tbx):
    """Toolbox Projekt loeschen"""
    @property
    def label(self):
        return u'Infrastruktur (Dummy)'

    @property
    def Tool(self):
        return Infrastruktur

    def _getParameterInfo(self):
        projects = self.folders.get_projects()

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
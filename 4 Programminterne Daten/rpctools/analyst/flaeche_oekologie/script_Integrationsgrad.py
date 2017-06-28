# -*- coding: utf-8 -*-

import os
import sys

import arcpy
from rpctools.utils.params import Tool

class Integrationsgrad(Tool):
    """Integrationsgrad"""

    _param_projectname = 'name'
    _workspace = 'FGDB_Flaeche_und_Oekologie.gdb'

    def add_outputs(self):
        pass

    def run(self):
        params = self.par
        projekt = self.projectname

        path_teilflaechen = self.folders.get_table('Teilflaechen_Plangebiet', "FGDB_Definition_Projekt.gdb", projekt)
        path_teilflaechen_dissolved = self.folders.get_table('Teilflaechen_Plangebiet_dissolved', "FGDB_Flaeche_und_Oekologie.gdb", projekt)
        arcpy.Dissolve_management(path_teilflaechen, path_teilflaechen_dissolved)




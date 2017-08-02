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
        self.output.add_layer(groupname = "oekologie", featureclass = "Grenze_Siedlungskoerper", template_layer = "Grenze_Siedlungskoerper", template_folder="oekologie",  zoom=False, disable_other = True)
        self.output.show_layers()

    def run(self):
        params = self.par
        projekt = self.projectname



class Integrationsgrad_loeschen(Tool):
    """Integrationsgrad_loeschen"""

    _param_projectname = 'name'
    _workspace = 'FGDB_Flaeche_und_Oekologie.gdb'

    def add_outputs(self):
        pass

    def run(self):
        params = self.par
        projekt = self.projectname

        table_grenzlinie = self.folders.get_table("Grenze_SIedlungskoerper", "FGDB_Flaeche_und_Oekologie.gdb")

        cursor = arcpy.da.UpdateCursor(table_grenzlinie, ["*"])
        for row in cursor:
            cursor.deleteRow()

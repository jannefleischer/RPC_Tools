# -*- coding: utf-8 -*-
import os
import sys

import arcpy
from rpctools.utils.params import Tool

class Ueberschneidungen(Tool):
    """Ueberschneidungen"""

    _param_projectname = 'name'
    _workspace = 'FGDB_Flaeche_und_Oekologie.gdb'

    def add_outputs(self):
        params = self.par

        if params.layer_number.value == 1:
            path = "Waldgebiete"
        elif params.layer_number.value == 2:
            path = "Naturschutzgebiete"
        elif params.layer_number.value == 3:
            path = "Landschaftsschutzgebiete"
        elif params.layer_number.value == 4:
            path = "Wasserflaechen"
        elif params.layer_number.value == 5:
            path = "Freiraeume"
        elif params.layer_number.value == 6:
            path = "Bodenversiegelung"
        elif params.layer_number.value == 7:
            path = "Hochspannung"

        self.output.add_layer(groupname = "oekologie", template_layer = path, template_folder="oekologie", zoom=False, disable_other = False)
        self.output.add_image("C:\\Temp\\hui.png", "Test")

        arcpy.RefreshTOC()
        arcpy.RefreshActiveView()


    def run(self):
        params = self.par
        projekt = self.projectname
        #self.output.enable_layer('projektdefinition')











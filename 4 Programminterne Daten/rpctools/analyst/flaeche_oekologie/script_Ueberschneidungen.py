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

        if params.label.value == 1:
            path = self.folders.get_layer("Waldgebiete", "oekologie")
        elif params.label.value == 2:
            path = self.folders.get_layer("Naturschutzgebiete", "oekologie")
        elif params.label.value == 3:
            path = self.folders.get_layer("landschaftsschutzgebiete", "oekologie")
        elif params.label.value == 4:
            path = self.folders.get_layer("Wasserflaechen", "oekologie")

        self.output.add_layer(groupname = "oekologie", template_layer = path, zoom=False)

    def run(self):
        params = self.par
        projekt = self.projectname










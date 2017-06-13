# -*- coding: utf-8 -*-

import arcpy
import os
from collections import OrderedDict

from rpctools.utils.params import Tool
from rpctools.diagrams.diagram_teilflaechen import DiaTeilflaechen


class TeilflaechenVerwalten(Tool):

    _param_projectname = 'projectname'
    _workspace = 'FGDB_Definition_Projekt.gdb'
    
    def add_outputs(self):
        self.output.add_diagram(DiaTeilflaechen())

    def run(self):
        # atm there is nothing to do here, setting db is already done in toolbox
        # ToDo: add output layer
        #self.add_diagramm()
        arcpy.RefreshActiveView()
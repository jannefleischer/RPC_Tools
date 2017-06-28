# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# schutzwuerdigeBoedenTesten.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# ILS gGmbH
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


import os
import sys
import arcpy
from os.path import join
from rpctools.utils.params import Tool
import rpctools.utils.config 

class Ueberschneidung(Tool):
    
    _param_projectname = 'projectname'
    _dbname = 'FGDB_Flaeche_und_Oekologie.gdb'

    def run(self):
        parameters = self.par
        projektname = self.par.projectname.value
    	workspace_oekologie = self.folders.get_db('FGDB_Flaeche_und_Oekologie.gdb')
        workspace_projekt = self.folders.get_db('FGDB_Definition_Projekt.gdb')
    	pfadProjektflaeche = join(workspace_projekt,'Teilflaechen_Plangebiet')
        current_mxd = arcpy.mapping.MapDocument("CURRENT")
        current_dataframe = current_mxd.activeDataFrame
        
        #pfad_verschnitt = os.path.join(workspace_oekologie, "Waldgebiete")
        #if arcpy.Exists(pfad_verschnitt):
        #    arcpy.Delete_management(pfad_verschnitt)
        wald_path = self.folders.get_layer("Waldgebiete", "oekologie")
        #wald_layer = arcpy.mapping.Layer(wald_path)
        #wald_yearlayer = arcpy.mapping.ListLayers(wald_layer, "2015_a")[0]
        #arcpy.Intersect_analysis([pfadProjektflaeche, wald_yearlayer], pfad_verschnitt)
        #self.output.add_output("oekologie", pfad_verschnitt)
        self.output.add_output("oekologie", wald_path)
        
        wasser_path = self.folders.get_layer("Wasserflaechen", "oekologie")
        self.output.add_output("oekologie", wasser_path)
        naturschutz_path = self.folders.get_layer("Naturschutzgebiete", "oekologie")
        self.output.add_output("oekologie", naturschutz_path)
        landschaftsschutz_path = self.folders.get_layer("landschaftsschutzgebiete", "oekologie")
        self.output.add_output("oekologie", landschaftsschutz_path)
        

        


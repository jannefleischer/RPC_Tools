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

class Ueberschneidung(Tool):

    def run(self):
        messages = self.mes
        parameters = self.par

    	projektname = parameters[0].valueAsText
    	#projektname = "Bultweg_Sued_fiktiv"
    	#Pfade einrichten
    	base_path = str(sys.path[0]).split("2 Planungsprojekte analysieren")[0]

    	workspace_projekt = self.folders.get_db('FGDB_Definition_Projekt.gdb', projektname)
    	workspace_tool = join(base_path,'2_Tool','Flaeche_und_Oekologie')

    	pfadNiSa = join(workspace_tool,'bodenNiSa.lyr')
    	pfadNRW = join(workspace_tool,'bodenNRW.lyr')
    	pfadProjektflaeche = join(workspace_projekt,'Teilflaechen_Plangebiet')

    	mxd = arcpy.mapping.MapDocument("CURRENT")
    	df = arcpy.mapping.ListDataFrames(mxd)[0]
    	#Pfade zu den hinzuzufügenden Dateien anlegen
    	bodenNISA = arcpy.mapping.Layer(pfadNiSa)
    	bodenNRW = arcpy.mapping.Layer(pfadNRW)
    	projektgebiet = arcpy.mapping.Layer(pfadProjektflaeche)
    	#extent des projektgebietes speichern
    	projektgebiet_extent = projektgebiet.getExtent()
    	#Layerhinzufuegen
    	arcpy.mapping.AddLayer(df, bodenNISA)
    	arcpy.mapping.AddLayer(df, bodenNRW)
    	arcpy.mapping.AddLayer(df, projektgebiet)
    	#auf Projektgebiet zoomen
    	df.extent = projektgebiet_extent
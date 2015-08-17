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


import arcpy, os
projektname = arcpy.GetParameterAsText(0)
#projektname = "Bultweg_Sued_fiktiv"
#Pfade einrichten
base_path = str(sys.path[0]).split("2_Tool")[0]

workspace_projekt = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
workspace_tool = os.path.join(base_path,'2_Tool','36_Flaeche_und_Oekologie')

pfadNiSa = os.path.join(workspace_tool,'bodenNiSa.lyr')
pfadNRW = os.path.join(workspace_tool,'bodenNRW.lyr')
pfadProjektflaeche = os.path.join(workspace_projekt,'Teilflaechen_Plangebiet')

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
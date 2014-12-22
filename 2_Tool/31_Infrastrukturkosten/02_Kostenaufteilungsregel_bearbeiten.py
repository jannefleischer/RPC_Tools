# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 02_Kostenaufteilungsregel_bearbeiten.py
# 
# Description: Erstellung der Bevölkerungsprognose für das zu untersuchende Projekt
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# GGR Planung
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


# Import arcpy modules
import arcpy, os, inspect, pyodbc, shutil, gc
import kosten_lib as k

arcpy.env.overwriteOutput = True

#Pfade einrichten
name = arcpy.GetParameterAsText(0)
gemeinden = float(arcpy.GetParameterAsText(1))/100
kreis = float(arcpy.GetParameterAsText(2))/100
private = float(arcpy.GetParameterAsText(3))/100

k.kostenregel_bearbeiten(name,gemeinden,kreis,private)

# Endmeldung
message = 'Regel bearbeitet'
print message
arcpy.AddMessage(message)
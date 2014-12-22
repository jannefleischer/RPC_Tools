# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 02_Kostenermittlung.py
#
# Description:
#
#Author:
#Achim Tack / Gertz Gutsche Rümenapp
# ---------------------------------------------------------------------------

#############################################################################################################
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
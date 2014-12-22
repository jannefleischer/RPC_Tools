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

k.kostenregel_loeschen(name)

# Endmeldung
message = 'Regel geloescht'
print message
arcpy.AddMessage(message)
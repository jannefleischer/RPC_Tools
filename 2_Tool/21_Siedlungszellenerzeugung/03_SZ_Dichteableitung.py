# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 03_SZ_Dichteableitung.py
# 
# Description: 
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# GGR Planung
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


# Import arcpy modules
import os
import gc
import sys

import arcpy

gc.collect()

arcpy.env.overwriteOutput = True

# Variablen definieren
projektname = arcpy.GetParameterAsText(0)
punktlayer = arcpy.GetParameterAsText(1)

#Pfade einrichten
base_path = str(sys.path[0]).split("2_Tool")[0]

workspace_projekt = os.path.join(base_path, '3_Projekte', projektname,
                                 'FGDB_11_Definition_Projekt_' + projektname + '.gdb')
workspace_siedlungszellen = os.path.join(base_path, '3_Projekte', projektname,
                                         'FGDB_21_Siedlungszellen_' + projektname + '.gdb')

siedlungszellenlayer = os.path.join(workspace_siedlungszellen, "Siedlungszellen")
siedlungszellenlayer_join = os.path.join(workspace_siedlungszellen, "Siedlungszellen_Join")

# Nachricht
arcpy.AddMessage("Beginne Berechnung \n")

#############################################################################################################
# Eingangsdaten für Spatial Join

#Loesche Feld "Join Count" (falls vorhanden)
try:
    arcpy.DeleteField_management(siedlungszellenlayer, "Join_Count")
except:
    pass

# Process: Räumliche Verbindung
arcpy.SpatialJoin_analysis(siedlungszellenlayer, punktlayer, siedlungszellenlayer_join, "JOIN_ONE_TO_ONE", "KEEP_ALL",
                           "GEN \"GEN\" true true false 50 Text 0 0 ,First,#," + siedlungszellenlayer + ",GEN,-1,-1;AGS \"AGS\" true true false 12 Text 0 0 ,First,#," + siedlungszellenlayer + ",AGS,-1,-1;EWZ \"EWZ\" true true false 8 Double 0 0 ,First,#," + siedlungszellenlayer + ",EWZ,-1,-1;SZ_ID \"SZ_ID\" true true true 4 Long 0 0 ,First,#," + siedlungszellenlayer + ",SZ_ID,-1,-1",
                           "INTERSECT", "", "")

# Nachricht
arcpy.AddMessage("Punkte mit Rasterzelle verschnitten \n")

#############################################################################################################
# Anteil der Punkte je Rasterzelle an Punkten im Gemeindelayer ermitteln

# Feld "Anteil" erzeugen
arcpy.AddField_management(siedlungszellenlayer_join, "Anteil", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Nachricht
arcpy.AddMessage("Feld 'Anteil' hinzugefuegt \n")

#############################################################################################################
# Summe der Punktfeatures je Gemeinde ermitteln und in eine Tabelle schreiben
joinField = "AGS"
arcpy.Statistics_analysis(siedlungszellenlayer_join, str(siedlungszellenlayer_join) + "_stat", [["Join_Count", "SUM"]],
                          joinField)

# Nachricht
arcpy.AddMessage("Summe je Gemeinde ermittelt \n")

#############################################################################################################
# Gesamtsumme der Punktfeatures je Gemeinde an den Siedlungszellenlayer anfuegen
joinfeld = "AGS"

jointable_name = str(siedlungszellenlayer_join) + "_stat"
jointable = os.path.join(workspace_siedlungszellen, jointable_name)

Siedlungszellen_Join = os.path.join(workspace_siedlungszellen, "Siedlungszellen_Join")
Siedlungszellen_Join_stat = os.path.join(workspace_siedlungszellen, "Siedlungszellen_Join_stat")

# Process: Feld verbinden
arcpy.JoinField_management(Siedlungszellen_Join, joinField, jointable, joinField, "SUM_Join_Count")

# Process: Features kopieren
arcpy.CopyFeatures_management(Siedlungszellen_Join, siedlungszellenlayer, "", "0", "0", "0")

# Nachricht
arcpy.AddMessage("Joincount je Gemeinde angefuegt \n")


#############################################################################################################
# Anteile der Siedlungszellen an Gemeinde ermitteln

# Process: Feld berechnen
arcpy.CalculateField_management(siedlungszellenlayer, "Anteil", "divide(!SUM_JOIN_Count!,!Join_Count!)", "PYTHON",
                                "def divide(a,b):\\n    if a == 0:\\n        value = 0\\n    else:\\n        value = float(b)/float(a)\\n    return value\\n\\n\\n")

arcpy.AddMessage("Anteile ermittelt \n")

#############################################################################################################
# Erzeuge Spalte - Bevoelkerungszahl je Siedlungszelle
schrittmeldung = 'Bevoelkerungszahl je Siedlungszelle \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

#Loesche Feld "SZ_Einwohner" (falls vorhanden)
try:
    arcpy.DeleteField_management(siedlungszellenlayer, "SZ_Einwohner")
except:
    pass

# Feld "SZ_Einwohner" erzeugen
arcpy.AddField_management(siedlungszellenlayer, "SZ_Einwohner", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED",
                          "")

arcpy.CalculateField_management(siedlungszellenlayer, "SZ_Einwohner", "[Anteil] * [EWZ]", "VB", "")

#############################################################################################################
#Aufraeumen und ueberfluessige Variablen loeschen
schrittmeldung = 'Aufraeumen und ueberfluessige Variablen loeschen \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

deletelist = [jointable, Siedlungszellen_Join]

for element in deletelist:
    try:
        e = str(element)
        arcpy.Delete_management(e)
    except:
        print element, "konnte nicht geloescht werden"

gc.collect()
print "fertig"
arcpy.AddMessage("Siedlungsdichteermittlung abgeschlossen \n")


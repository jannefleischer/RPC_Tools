# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# projektLoeschen.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# ILS gGmbH
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


import shutil
import os
import sys

import arcpy

#Das zu löschende Projekt
projektName = arcpy.GetParameterAsText(0)

#aktuelles Arbeitsverzeichnis bekommen
pfad = str(sys.path[0]).split("2_Tool")[0]

#Mit dem Projektnamen zum neuen Projektpfad zusammenführen"
projektePfad = os.path.join(pfad,'3_Projekte')
projektPfad= os.path.join(projektePfad,projektName)
arcpy.AddMessage("Suche Ordner: " + projektPfad)

#entferne alle aktuellen Layer aus dem TOC (Locks aufheben)
arcpy.AddMessage("Loese aktive Layer aus MXD \n")
mxd = arcpy.mapping.MapDocument("CURRENT")
for df in arcpy.mapping.ListDataFrames(mxd):
    for lyr in arcpy.mapping.ListLayers(mxd, "", df):
        arcpy.mapping.RemoveLayer(df, lyr)
del mxd

try:
    #Überprüfen, ob ein Eintrag in der Datenbank vorliegt
    fcPfad = os.path.join(pfad,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb','angelegteProjekte')
    #arcpy.AddMessage(fcPfad)
    sql = "Name = '" + projektName +"'"
    x=0
    cursor = arcpy.UpdateCursor(fcPfad,sql)
    for row in cursor:
        #arcpy.AddMessage(row.Name)
        x = x+1
    del cursor, row

    #Überprüfen, ob der Projektordner existiert
    if(os.path.isdir(projektPfad)):
        print("Projektordner gefunden")
        arcpy.AddMessage("Projektordner gefunden \n")
        shutil.rmtree(projektPfad)
        print("Projektordner gelöscht")
        arcpy.AddMessage("Projektordner gelöscht \n")
    else:
        print("Projektordner "+ projektName + " nicht gefunden \n")
        arcpy.AddMessage("Projektordner "+ projektName + " nicht gefunden \n")

    if x == 1:
        print "Eintrag in der Datenbank gefunden"
        arcpy.AddMessage("Eintrag in der Datenbank gefunden \n")
        delcursor = arcpy.UpdateCursor(fcPfad,sql)
        try:
            for fc in delcursor:
                #arcpy.AddMessage("Loeschschleife")
                #arcpy.AddMessage(fc.Name)
                delcursor.deleteRow(fc)
                print("Eintrag gelöscht")
                arcpy.AddMessage("Eintrag gelöscht \n")
        except:
            arcpy.AddMessage("Löschen fehlgeschlagen \n")

        del delcursor


    else:
        print("Projekt "+ projektName + " nicht gefunden")
        arcpy.AddMessage("Projekt "+ projektName + " nicht gefunden \n")


    arcpy.AddMessage("*********************************************************************************")
    arcpy.AddMessage("Das Projekt " + projektName + " wurde erfolgreich entfernt \n")

except Exception as e:
    print(e)
    arcpy.AddMessage(e)
finally:
    try:
        del cursor, delcursor
    except:
        print""


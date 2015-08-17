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


import shutil, arcpy, os, sys
try:
    #Das zu löschende Projekt
    projektName = arcpy.GetParameterAsText(0)

    #aktuelles Arbeitsverzeichnis bekommen
    pfad = str(sys.path[0]).split("2_Tool")[0]

    #Mit dem Projektnamen zum neuen Projektpfad zusammenführen"
    projektePfad = os.path.join(pfad,'3_Projekte')
    projektPfad= os.path.join(projektePfad,projektName)
    arcpy.AddMessage("Suche Ordner: " + projektPfad)
    #Überprüfen, ob der Projektordner existiert
    if(os.path.isdir(projektPfad)):
        print("Projektordner gefunden")
        arcpy.AddMessage("Projektordner gefunden")
        shutil.rmtree(projektPfad)
        print("Projektordner gelöscht")
        arcpy.AddMessage("Projektordner gelöscht")
    else:
        print("Projektordner "+ projektName + " nicht gefunden")
        arcpy.AddMessage("Projektordner "+ projektName + " nicht gefunden")

    #Überprüfen, ob ein Eintrag in der Datenbank vorliegt
    fcPfad = os.path.join(pfad,'1_Basisdaten','FGBD_01_Basisdaten_deutschland.gdb','angelegteProjekte')
    #arcpy.AddMessage(fcPfad)
    sql = "Name = '" + projektName +"'"
    x=0
    cursor = arcpy.UpdateCursor(fcPfad,sql)
    for row in cursor:
        #arcpy.AddMessage(row.Name)
        x = x+1
    if x == 1:
        print "Eintrag in der Datenbank gefunden"
        arcpy.AddMessage("Eintrag in der Datenbank gefunden")
        delcursor = arcpy.UpdateCursor(fcPfad,sql)
        try:
            for fc in delcursor:
                #arcpy.AddMessage("Loeschschleife")
                #arcpy.AddMessage(fc.Name)
                delcursor.deleteRow(fc)
                print("Eintrag gelöscht")
                arcpy.AddMessage("Eintrag gelöscht")
        except:
            arcpy.AddMessage("Löschen fehlgeschlagen")
    else:
        print("Projekt "+ projektName + " nicht gefunden")
        arcpy.AddMessage("Projekt "+ projektName + " nicht gefunden")
    arcpy.AddMessage("*********************************************************************************")
    arcpy.AddMessage("Das Projekt " + projektName + "wurde erfolgreich entfernt")
except Exception as e:
    print(e)
    arcpy.AddMessage(e)
finally:
    try:
        del cursor, delcursor
    except:
        print""


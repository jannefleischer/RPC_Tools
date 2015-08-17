# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# kosten_lib.py
# 
# Description: Erstellung der Bevölkerungsprognose für das zu untersuchende Projekt
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# GGR Planung
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


#
# Allgemeine Funktionen
#


def kostenregel_anlegen(name,gemeinden,kreis,private):
    print "anlegen"
    import sys, os, arcpy
    # Create Paths
    base_path = str(sys.path[0]).split("2_Tool")[0] # Pfad zum Basisverzeichnis RPC
    kosten_tool = os.path.join(base_path,'2_Tool',"31_Infrastrukturkosten","FGDB_31_Kosten_Tool.gdb")
    kostenaufteilungsregel_tabelle = os.path.join(kosten_tool,'T01DEF_Kostenaufteilungsregeln')

    #gemeinden
    rows = arcpy.InsertCursor(kostenaufteilungsregel_tabelle)
    row = rows.newRow()
    row.Kostenregelname = name
    row.Kostentraeger = 1
    row.Anteil = gemeinden
    rows.insertRow(row)

    #kreis
    rows = arcpy.InsertCursor(kostenaufteilungsregel_tabelle)
    row = rows.newRow()
    row.Kostenregelname = name
    row.Kostentraeger = 2
    row.Anteil = kreis
    rows.insertRow(row)

    #private
    rows = arcpy.InsertCursor(kostenaufteilungsregel_tabelle)
    row = rows.newRow()
    row.Kostenregelname = name
    row.Kostentraeger = 3
    row.Anteil = private
    rows.insertRow(row)

    #text = gemeinden,kreis,private
    #arcpy.AddMessage(text)

    # Delete cursor and row objects to remove locks on the data
    #
    del row
    del rows


def kostenregel_bearbeiten(name,gemeinden,kreis,private):
    import sys, os, arcpy
    print "bearbeiten"
    # Create Paths
    base_path = str(sys.path[0]).split("2_Tool")[0] # Pfad zum Basisverzeichnis RPC
    kosten_tool = os.path.join(base_path,'2_Tool',"31_Infrastrukturkosten","FGDB_31_Kosten_Tool.gdb")
    kostenaufteilungsregel_tabelle = os.path.join(kosten_tool,'T01DEF_Kostenaufteilungsregeln')

    # Step 1 - delete rule
    rows = arcpy.UpdateCursor(kostenaufteilungsregel_tabelle)

    for row in rows:
        # Delete all rows that have a roads type of 4
        if row.Kostenregelname == name:
            rows.deleteRow(row)

    del row, rows

    # Step 2 - create rule

    #gemeinden
    rows = arcpy.InsertCursor(kostenaufteilungsregel_tabelle)
    row = rows.newRow()
    row.Kostenregelname = name
    row.Kostentraeger = 1
    row.Anteil = gemeinden
    rows.insertRow(row)

    #kreis
    rows = arcpy.InsertCursor(kostenaufteilungsregel_tabelle)
    row = rows.newRow()
    row.Kostenregelname = name
    row.Kostentraeger = 2
    row.Anteil = kreis
    rows.insertRow(row)

    #private
    rows = arcpy.InsertCursor(kostenaufteilungsregel_tabelle)
    row = rows.newRow()
    row.Kostenregelname = name
    row.Kostentraeger = 3
    row.Anteil = private
    rows.insertRow(row)

    # Delete cursor and row objects to remove locks on the data
    #
    del row, rows

def kostenregel_loeschen(name):
    import sys, os, arcpy
    print "loeschen"
    # Create Paths
    base_path = str(sys.path[0]).split("2_Tool")[0] # Pfad zum Basisverzeichnis RPC
    kosten_tool = os.path.join(base_path,'2_Tool',"31_Infrastrukturkosten","FGDB_31_Kosten_Tool.gdb")
    kostenaufteilungsregel_tabelle = os.path.join(kosten_tool,'T01DEF_Kostenaufteilungsregeln')

    rows = arcpy.UpdateCursor(kostenaufteilungsregel_tabelle)

    for row in rows:
        # Delete all rows that have a roads type of 4
        if row.Kostenregelname == name:
            rows.deleteRow(row)
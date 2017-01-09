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

import sys, os, arcpy

def kostenregel_anlegen(name,gemeinden,kreis,private):
    # Create Paths
    base_path = str(sys.path[0]).split("2_Tool")[0] # Pfad zum Basisverzeichnis RPC
    kosten_tool = os.path.join(base_path,'2_Tool',"A_Infrastrukturkosten","FGDB_Kosten_Tool.gdb")
    kostenaufteilungsregel_tabelle = os.path.join(kosten_tool,'T01DEF_Kostenaufteilungsregeln')

    #gemeinden
    rows = arcpy.InsertCursor(kostenaufteilungsregel_tabelle)
    row = rows.newRow()
    row.Kostenregelname = name
    row.Kostentraeger = 1
    row.Anteil = gemeinden
    row.Vorgabewert = 0
    rows.insertRow(row)

    #kreis
    rows = arcpy.InsertCursor(kostenaufteilungsregel_tabelle)
    row = rows.newRow()
    row.Kostenregelname = name
    row.Kostentraeger = 2
    row.Anteil = kreis
    row.Vorgabewert = 0
    rows.insertRow(row)

    #private
    rows = arcpy.InsertCursor(kostenaufteilungsregel_tabelle)
    row = rows.newRow()
    row.Kostenregelname = name
    row.Kostentraeger = 3
    row.Anteil = private
    row.Vorgabewert = 0
    rows.insertRow(row)

    #text = gemeinden,kreis,private
    #arcpy.AddMessage(text)

    # Delete cursor and row objects to remove locks on the data
    #
    del row
    del rows


def kostenregel_bearbeiten(name,gemeinden,kreis,private:
    # Create Paths
    base_path = str(sys.path[0]).split("2_Tool")[0] # Pfad zum Basisverzeichnis RPC
    kosten_tool = os.path.join(base_path,'2_Tool',"A_Infrastrukturkosten","FGDB_Kosten_Tool.gdb")
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
    row.Vorgabewert = 0
    rows.insertRow(row)

    #kreis
    rows = arcpy.InsertCursor(kostenaufteilungsregel_tabelle)
    row = rows.newRow()
    row.Kostenregelname = name
    row.Kostentraeger = 2
    row.Anteil = kreis
    row.Vorgabewert = 0
    rows.insertRow(row)

    #private
    rows = arcpy.InsertCursor(kostenaufteilungsregel_tabelle)
    row = rows.newRow()
    row.Kostenregelname = name
    row.Kostentraeger = 3
    row.Anteil = private
    row.Vorgabewert = 0
    rows.insertRow(row)

    # Delete cursor and row objects to remove locks on the data
    #
    del row, rows

def kostenregel_loeschen(name):
    # Create Paths
    base_path = str(sys.path[0]).split("2_Tool")[0] # Pfad zum Basisverzeichnis RPC
    kosten_tool = os.path.join(base_path,'2_Tool',"A_Infrastrukturkosten","FGDB_Kosten_Tool.gdb")
    kostenaufteilungsregel_tabelle = os.path.join(kosten_tool,'T01DEF_Kostenaufteilungsregeln')

    rows = arcpy.UpdateCursor(kostenaufteilungsregel_tabelle)

    for row in rows:
        # Delete all rows that have a roads type of 4
        if row.Kostenregelname == name:
            rows.deleteRow(row)
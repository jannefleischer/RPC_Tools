# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 02_Kostenaufteilungsregel_bearbeiten.py
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
import arcpy,sys,os

arcpy.env.overwriteOutput = True

#Pfade einrichten
action = arcpy.GetParameterAsText(0)
rule_name_old = arcpy.GetParameterAsText(1)
rule_name = arcpy.GetParameterAsText(2)

gemeinden = float(arcpy.GetParameterAsText(3))/100
kreis = float(arcpy.GetParameterAsText(4))/100
private = float(arcpy.GetParameterAsText(5))/100


if action == 'Kostenaufteilungsregel anlegen':
    base_path = str(sys.path[0]).split("2_Tool")[0] # Pfad zum Basisverzeichnis RPC
    kosten_tool = os.path.join(base_path,'2_Tool',"A_Infrastrukturkosten","FGDB_Kosten_Tool.gdb")
    kostenaufteilungsregel_tabelle = os.path.join(kosten_tool,'T01DEF_Kostenaufteilungsregeln')

    #gemeinden
    rows = arcpy.InsertCursor(kostenaufteilungsregel_tabelle)
    row = rows.newRow()
    row.Kostenregelname = rule_name
    row.Kostentraeger = 1
    row.Anteil = gemeinden
    row.Vorgabewert = 0
    rows.insertRow(row)

    #kreis
    rows = arcpy.InsertCursor(kostenaufteilungsregel_tabelle)
    row = rows.newRow()
    row.Kostenregelname = rule_name
    row.Kostentraeger = 2
    row.Anteil = kreis
    row.Vorgabewert = 0
    rows.insertRow(row)

    #private
    rows = arcpy.InsertCursor(kostenaufteilungsregel_tabelle)
    row = rows.newRow()
    row.Kostenregelname = rule_name
    row.Kostentraeger = 3
    row.Anteil = private
    row.Vorgabewert = 0
    rows.insertRow(row)

    del row
    del rows

elif action == 'Kostenaufteilungsregel bearbeiten':
    base_path = str(sys.path[0]).split("2_Tool")[0] # Pfad zum Basisverzeichnis RPC
    kosten_tool = os.path.join(base_path,'2_Tool',"A_Infrastrukturkosten","FGDB_Kosten_Tool.gdb")
    kostenaufteilungsregel_tabelle = os.path.join(kosten_tool,'T01DEF_Kostenaufteilungsregeln')

    rows = arcpy.UpdateCursor(kostenaufteilungsregel_tabelle)

    for row in rows:
        if row.Kostenregelname == rule_name_old:
            rows.deleteRow(row)
    del row, rows

    #gemeinden
    rows = arcpy.InsertCursor(kostenaufteilungsregel_tabelle)
    row = rows.newRow()
    row.Kostenregelname = rule_name
    row.Kostentraeger = 1
    row.Anteil = gemeinden
    row.Vorgabewert = 0
    rows.insertRow(row)

    #kreis
    rows = arcpy.InsertCursor(kostenaufteilungsregel_tabelle)
    row = rows.newRow()
    row.Kostenregelname = rule_name
    row.Kostentraeger = 2
    row.Anteil = kreis
    row.Vorgabewert = 0
    rows.insertRow(row)

    #private
    rows = arcpy.InsertCursor(kostenaufteilungsregel_tabelle)
    row = rows.newRow()
    row.Kostenregelname = rule_name
    row.Kostentraeger = 3
    row.Anteil = private
    row.Vorgabewert = 0
    rows.insertRow(row)

    del row
    del rows

elif action == 'Kostenaufteilungsregel entfernen':
    base_path = str(sys.path[0]).split("2_Tool")[0] # Pfad zum Basisverzeichnis RPC
    kosten_tool = os.path.join(base_path,'2_Tool',"A_Infrastrukturkosten","FGDB_Kosten_Tool.gdb")
    kostenaufteilungsregel_tabelle = os.path.join(kosten_tool,'T01DEF_Kostenaufteilungsregeln')

    rows = arcpy.UpdateCursor(kostenaufteilungsregel_tabelle)

    for row in rows:
        if row.Kostenregelname == rule_name:
            rows.deleteRow(row)
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# Bodenbedeckungbeschreiben.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# ILS gGmbH
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------
import os
import arcpy
import sys

def main(parameters, messages):
    wcd = os.getcwd()
    rootPfad = str(sys.path[0]).split("2_Tool")[0]

    #Projektname
    projekt = parameters[0].valueAsText
    gdb = "FGDB_Flaeche_und_Oekologie_" + projekt + ".gdb"
    pfad_flaeche = join(rootPfad,'3_Projekte',projekt,gdb,"Bodenbedeckung")
    #Feldliste erstellen
    try:
        fields = arcpy.ListFields(pfad_flaeche)
        #messages.AddMessage(fields)
        update = arcpy.UpdateCursor(pfad_flaeche)
        for row in update:
            #messages.AddMessage(row.Teilflaeche)
            for field in fields:
                #messages.AddMessage(field.name)
                if row.getValue(field.name) == None:
                    #messages.AddMessage(field.name)
                    row.setValue(field.name,0)
            update.updateRow(row)
        del update
    except Exception as e:
        messages.AddMessage(e)
        del update
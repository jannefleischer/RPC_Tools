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


def main():
    pass

if __name__ == '__main__':
    main()

import os, arcpy
wcd = os.getcwd()
rootPfad = str(sys.path[0]).split("2_Tool")[0]

#Projektname
projekt = arcpy.GetParameterAsText(0)
gdb = "FGDB_36_Flaeche_und_Oekologie_Projekt_" + projekt + ".gdb"
pfad_flaeche = os.path.join(rootPfad,'3_Projekte',projekt,gdb,"Bodenbedeckung")
#Feldliste erstellen
try:
    fields = arcpy.ListFields(pfad_flaeche)
    #arcpy.AddMessage(fields)
    update = arcpy.UpdateCursor(pfad_flaeche)
    for row in update:
        #arcpy.AddMessage(row.Teilflaeche)
        for field in fields:
            #arcpy.AddMessage(field.name)
            if row.getValue(field.name) == None:
                #arcpy.AddMessage(field.name)
                row.setValue(field.name,0)
        update.updateRow(row)
    del update
except Exception as e:
    arcpy.AddMessage(e)
    del update
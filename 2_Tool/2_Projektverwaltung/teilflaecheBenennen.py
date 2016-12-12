# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# projektAnlegen_work.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# ILS gGmbH / HCU Hamburg / GGR Planung
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


import arcpy, os, shutil, sys

def main():
    # Teilfläche speichern
    projectname = arcpy.GetParameterAsText(0)
    flaechenname = arcpy.GetParameterAsText(1)
    alter_name = flaechenname.split('|')[2].strip()
    neuer_name = arcpy.GetParameterAsText(2)
    flaechenname_id = flaechenname.split('|')[0].replace('Nr.','').strip()

    base_path = str(sys.path[0]).split("2_Tool")[0]

    tabelle_teilflaechen = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb','Teilflaechen_Plangebiet')

    where = '"OBJECTID" = ' + flaechenname_id

    rows = arcpy.UpdateCursor(tabelle_teilflaechen,where)
    for row in rows:
        row.NAME = neuer_name  #arcpy.GetParameterAsText(2)
        rows.updateRow(row)

    del rows


    # Name der Teilfl�che in anderen Tabellen aktualisieren

    path_definition = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Definition_Projekt_'+projectname+'.gdb')
    path_oekologie = os.path.join(base_path,'3_Projekte',projectname,'FGDB_Flaeche_und_Oekologie_Projekt_'+projectname+'.gdb')

    rows = arcpy.UpdateCursor(os.path.join(path_definition, 'Flaechenbilanz'))
    for row in rows:
        if row.Teilflaeche_Plangebiet == alter_name:
            row.Teilflaeche_Plangebiet = neuer_name
            rows.updateRow(row)

    rows = arcpy.UpdateCursor(os.path.join(path_definition, 'Gebaeude_Details'))
    for row in rows:
        if row.Teilflaeche_Plangebiet == alter_name:
            row.Teilflaeche_Plangebiet = neuer_name
            rows.updateRow(row)

    rows = arcpy.UpdateCursor(os.path.join(path_definition, 'Gewerbe_Anteile'))
    for row in rows:
        if row.teilflaeche == alter_name:
            row.teilflaeche = neuer_name
            rows.updateRow(row)

    rows = arcpy.UpdateCursor(os.path.join(path_definition, 'Gewerbe_Beschaeftigte'))
    for row in rows:
        if row.Teilflaeche_Plangebiet == alter_name:
            row.Teilflaeche_Plangebiet = neuer_name
            rows.updateRow(row)

    rows = arcpy.UpdateCursor(os.path.join(path_definition, 'Gewerbe_Betriebsflaechen'))
    for row in rows:
        if row.teilflaeche == alter_name:
            row.teilflaeche = neuer_name
            rows.updateRow(row)

    rows = arcpy.UpdateCursor(os.path.join(path_definition, 'Gewerbe_Betriebsstruktur'))
    for row in rows:
        if row.teilflaeche == alter_name:
            row.teilflaeche = neuer_name
            rows.updateRow(row)

    rows = arcpy.UpdateCursor(os.path.join(path_definition, 'Gewerbe_Teilflaechen'))
    for row in rows:
        if row.teilflaeche == alter_name:
            row.teilflaeche = neuer_name
            rows.updateRow(row)

    rows = arcpy.UpdateCursor(os.path.join(path_definition, 'Grundlagen'))
    for row in rows:
        if row.Name == alter_name:
            row.Name = neuer_name
            rows.updateRow(row)

    rows = arcpy.UpdateCursor(os.path.join(path_definition, 'Versorgung_Verkaufsflaechen'))
    for row in rows:
        if row.Teilflaeche_Plangebiet == alter_name:
            row.Teilflaeche_Plangebiet = neuer_name
            rows.updateRow(row)

    rows = arcpy.UpdateCursor(os.path.join(path_definition, 'Wohneinheiten_Details'))
    for row in rows:
        if row.Teilflaeche_Plangebiet == alter_name:
            row.Teilflaeche_Plangebiet = neuer_name
            rows.updateRow(row)

    rows = arcpy.UpdateCursor(os.path.join(path_oekologie, 'Bodenbedeckung'))
    for row in rows:
        if row.Teilflaeche == alter_name:
            row.Teilflaeche = neuer_name
            rows.updateRow(row)

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-

import os
import sys

import arcpy
import rpctools.utils.chronik as c
from rpctools.utils.params import Tool


class Einkommensteuer(Tool):
    """Einkommensteuer-Tool"""

    _param_projectname = 'name'
    _workspace = 'FGDB_Einnahmen.gdb'

    def run(self):
        """run Einkommensteuer Tool"""

        params = self.par
        projektname = self.projectname

        we_efh = 0
        we_dh = 0
        we_rh = 0
        we_mfh = 0

        fields = ['IDGebaeudetyp', 'WE']
        tablepath_wohnen = self.folders.get_table('Wohnen_WE_in_Gebaeudetypen', "FGDB_Definition_Projekt.gdb")
        cursor = arcpy.da.SearchCursor(tablepath_wohnen, fields)
        for row in cursor:
            if row[0] == 1:
                we_efh += row[1]
            if row[0] == 2:
                we_dh += row[1]
            if row[0] == 3:
                we_rh += row[1]
            if row[0] == 4:
                we_mfh += row[1]

        fields = ['AGS', 'Gemeindetyp']
        tablepath_rahmendaten = self.folders.get_table('Projektrahmendaten', "FGDB_Definition_Projekt.gdb")
        cursor = arcpy.da.SearchCursor(tablepath_rahmendaten, fields)
        for row in cursor:
            ags = row[0]
            gemeindetyp = row[1]

        ags2 = ags[0:2]

        table_ESt_pro_WE = self.folders.get_base_table("FGDB_Einnahmen_Tool.gdb", "ESt_Einnahmen_pro_WE")
        fields = ["AGS2", "Gemeindetyp", "IDGebaeudetyp", "ESt_pro_WE"]
        where_clause = '"AGS2"' + "='" + ags2 + "'" + " AND " + '"Gemeindetyp"' + " = " + str(gemeindetyp)
        cursor = arcpy.da.SearchCursor(table_ESt_pro_WE, fields, where_clause)
        for row in cursor:
            if row[2] == 1:
                ESt_pro_WE_efh = row[3]
            if row[2] == 2:
                ESt_pro_WE_dh = row[3]
            if row[2] == 3:
                ESt_pro_WE_rh = row[3]
            if row[2] == 4:
                ESt_pro_WE_mfh = row[3]


        Einkommensteuer_gesamt = we_efh * ESt_pro_WE_efh + we_dh * ESt_pro_WE_dh + we_rh * ESt_pro_WE_rh + we_mfh * ESt_pro_WE_mfh
        Gesamtzahl_Bewohner = 0
        fields = ['AGS', 'Einw_Zuzug']
        where_clause = '"AGS"' + "='" + ags + "'"
        tablepath_bilanz = self.folders.get_table('Gemeindebilanzen', "FGDB_Einnahmen.gdb")
        cursor = arcpy.da.SearchCursor(tablepath_bilanz, fields, where_clause)
        for row in cursor:
            Gesamtzahl_Bewohner = row[1]
        ESt_pro_Bewohner = Einkommensteuer_gesamt / Gesamtzahl_Bewohner

        fields = ['ESt', 'Einw_Saldo']
        cursor = arcpy.da.UpdateCursor(tablepath_bilanz, fields)
        for gemeinde in cursor:
            gemeinde[0] = ESt_pro_Bewohner * gemeinde[1]
            cursor.updateRow(gemeinde)

        c.set_chronicle("Einkommensteuer", self.folders.get_table(tablename='Chronik_Nutzung',workspace="FGDB_Einnahmen.gdb",project=projektname))

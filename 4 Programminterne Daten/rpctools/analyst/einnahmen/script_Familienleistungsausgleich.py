# -*- coding: utf-8 -*-

import os
import sys

import arcpy
import rpctools.utils.chronik as c
from rpctools.utils.params import Tool


class Familienleistungsausgleich(Tool):
    """FLA-Tool"""

    _param_projectname = 'name'
    _workspace = 'FGDB_Einnahmen.gdb'

    def add_outputs(self):
        pass

    def run(self):
        """run FLA Tool"""

        params = self.par
        projektname = self.projectname


        tablepath_bilanz = self.folders.get_table('Gemeindebilanzen', "FGDB_Einnahmen.gdb")
        fields = ['FamLeistAusgl', 'ESt', 'AGS']

        tablepath_landesfaktor = self.folders.get_base_table("FGDB_Einnahmen_Tool.gdb", "FLA_Landesfaktoren")
        fields2 = ['AGS_Land', 'FLA_Faktor']

        cursor = arcpy.da.UpdateCursor(tablepath_bilanz, fields)
        for gemeinde in cursor:
            ags2 = gemeinde[2][0:2]
            where = '"AGS_Land"' + "='" + ags2 + "'"
            cursor2 = arcpy.da.SearchCursor(tablepath_landesfaktor, fields2, where)
            for land in cursor2:
                landesfaktor = land[1]
            gemeinde[0] = gemeinde[1] * landesfaktor
            cursor.updateRow(gemeinde)

        c.set_chronicle("Einkommensteuer", self.folders.get_table(tablename='Chronik_Nutzung',workspace="FGDB_Einnahmen.gdb",project=projektname))


# -*- coding: utf-8 -*-

import os
import sys

import arcpy
from rpctools.utils.params import Tool

class BodenbedeckungKontrolle(Tool):
    """BodenbedeckungKontrolle"""

    _param_projectname = 'name'
    _workspace = 'FGDB_Flaeche_und_Oekologie.gdb'

    def add_outputs(self):
        pass

    def run(self):
        params = self.par
        projekt = self.projectname

        path_bodenbedeckung = self.folders.get_table('Bodenbedeckung_Anteile', "FGDB_Flaeche_und_Oekologie.gdb", projekt)

        fields = ["IDBodenbedeckung", "Planfall", "Bodenbedeckung_Anteil"]
        cursor = arcpy.da.UpdateCursor(path_bodenbedeckung, fields)
        for row in cursor:
            if row[1] == 0 and row[0] == 1:
                 row[2] = params.ueberbauteflaechen_alt.value
            elif row[1] == 0 and row[0] == 2:
                 row[2] = params.wasser_alt.value
            elif row[1] == 0 and row[0] == 3:
                 row[2] = params.platten_alt.value
            elif row[1] == 0 and row[0] == 4:
                 row[2] = params.baeume_alt.value
            elif row[1] == 0 and row[0] == 5:
                 row[2] = params.rasengittersteine_alt.value
            elif row[1] == 0 and row[0] == 6:
                 row[2] = params.stauden_alt.value
            elif row[1] == 0 and row[0] == 7:
                 row[2] = params.wiese_alt.value
            elif row[1] == 0 and row[0] == 8:
                 row[2] = params.beton_alt.value
            elif row[1] == 0 and row[0] == 9:
                 row[2] =params.acker_alt.value
            elif row[1] == 0 and row[0] == 10:
                 row[2] = params.kleinpflaster_alt.value
            elif row[1] == 0 and row[0] == 11:
                 row[2] = params.rasen_alt.value
            elif row[1] == 1 and row[0] == 1:
                 row[2] = params.ueberbauteflaechen_neu.value
            elif row[1] == 1 and row[0] == 2:
                 row[2] = params.wasser_neu.value
            elif row[1] == 1 and row[0] == 3:
                 row[2] = params.platten_neu.value
            elif row[1] == 1 and row[0] == 4:
                 row[2] =params.baeume_neu.value
            elif row[1] == 1 and row[0] == 5:
                 row[2] = params.rasengittersteine_neu.value
            elif row[1] == 1 and row[0] == 6:
                 row[2] = params.stauden_neu.value
            elif row[1] == 1 and row[0] == 7:
                 row[2] = params.wiese_neu.value
            elif row[1] == 1 and row[0] == 8:
                 row[2] = params.beton_neu.value
            elif row[1] == 1 and row[0] == 9:
                 row[2] = params.acker_neu.value
            elif row[1] == 1 and row[0] == 10:
                 row[2] = params.kleinpflaster_neu.value
            elif row[1] == 1 and row[0] == 11:
                 row[2] = params.rasen_neu.value
            cursor.updateRow(row)



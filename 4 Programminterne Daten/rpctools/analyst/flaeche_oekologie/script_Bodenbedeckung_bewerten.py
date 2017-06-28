# -*- coding: utf-8 -*-

import os
import sys

import arcpy
from rpctools.utils.params import Tool

class BodenbedeckungBewertung(Tool):
    """BodenbedeckungBewertung"""

    _param_projectname = 'name'
    _workspace = 'FGDB_Flaeche_und_Oekologie.gdb'

    def add_outputs(self):
        pass

    def run(self):
        params = self.par
        projekt = self.projectname

        path_bodenbedeckung = self.folders.get_table('Bodenbedeckung_Anteile', "FGDB_Flaeche_und_Oekologie.gdb", projekt)

        boden_anteile_alt = [0,0,0,0,0,0,0,0,0,0,0]
        boden_anteile_neu = [0,0,0,0,0,0,0,0,0,0,0]

        fields = ["IDBodenbedeckung", "Planfall", "Bodenbedeckung_Anteil"]
        cursor = arcpy.da.SearchCursor(path_bodenbedeckung, fields)
        for row in cursor:
            if row[1] == 0 and row[0] == 1:
                 boden_anteile_alt[0] = row[2]
            elif row[1] == 0 and row[0] == 2:
                 boden_anteile_alt[1] = row[2]
            elif row[1] == 0 and row[0] == 3:
                 boden_anteile_alt[2] = row[2]
            elif row[1] == 0 and row[0] == 4:
                 boden_anteile_alt[3] = row[2]
            elif row[1] == 0 and row[0] == 5:
                 boden_anteile_alt[4] = row[2]
            elif row[1] == 0 and row[0] == 6:
                 boden_anteile_alt[5] = row[2]
            elif row[1] == 0 and row[0] == 7:
                 boden_anteile_alt[6] = row[2]
            elif row[1] == 0 and row[0] == 8:
                 boden_anteile_alt[7] = row[2]
            elif row[1] == 0 and row[0] == 9:
                 boden_anteile_alt[8] = row[2]
            elif row[1] == 0 and row[0] == 10:
                 boden_anteile_alt[9] = row[2]
            elif row[1] == 0 and row[0] == 11:
                 boden_anteile_alt[10] = row[2]
            elif row[1] == 1 and row[0] == 1:
                 boden_anteile_neu[0] = row[2]
            elif row[1] == 1 and row[0] == 2:
                 boden_anteile_neu[1] = row[2]
            elif row[1] == 1 and row[0] == 3:
                 boden_anteile_neu[2] = row[2]
            elif row[1] == 1 and row[0] == 4:
                 boden_anteile_neu[3] = row[2]
            elif row[1] == 1 and row[0] == 5:
                 boden_anteile_neu[4] = row[2]
            elif row[1] == 1 and row[0] == 6:
                 boden_anteile_neu[5] = row[2]
            elif row[1] == 1 and row[0] == 7:
                 boden_anteile_neu[6] = row[2]
            elif row[1] == 1 and row[0] == 8:
                 boden_anteile_neu[7] = row[2]
            elif row[1] == 1 and row[0] == 9:
                 boden_anteile_neu[8] = row[2]
            elif row[1] == 1 and row[0] == 10:
                 boden_anteile_neu[9] = row[2]
            elif row[1] == 1 and row[0] == 11:
                 boden_anteile_neu[10] = row[2]



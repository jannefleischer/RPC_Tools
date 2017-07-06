# -*- coding: utf-8 -*-

import os
import sys

import arcpy
import rpctools.utils.chronik as c
from rpctools.utils.params import Tool
import rpctools.utils.layer_einnahmen as lib_einnahmen

class Gesamtsumme(Tool):
    """Gesamtsumme-Tool"""

    _param_projectname = 'name'
    _workspace = 'FGDB_Einnahmen.gdb'

    def add_outputs(self):
        self.output.delete_output("Gesamtsumme")

        gemeinde_werte = lib_einnahmen.get_values(["Summe_Einnahmenbilanz"], self.projectname)

        symbology = lib_einnahmen.get_symbology(gemeinde_werte, 1)

        self.output.add_layer(
            groupname = "einnahmen",
            featureclass = "Gemeindebilanzen",
            template_layer = symbology,
            template_folder = "einnahmen",
            name = "Gesamtsumme",
            disable_other = True,
            symbology = {'valueField': "Summe_Einnahmenbilanz"},
            label_replace = {'Einw_Saldo': 'Summe_Einnahmenbilanz'}
        )

        arcpy.RefreshTOC()
        arcpy.RefreshActiveView()

    def run(self):
        """run Gesamtsumme Tool"""

        params = self.par
        projektname = self.projectname


        tablepath_bilanz = self.folders.get_table('Gemeindebilanzen', "FGDB_Einnahmen.gdb")
        fields = ["Summe_Einnahmenbilanz", "GrSt", "ESt", "FamLeistAusgl", "GewSt", "USt"]


        cursor_bilanz = arcpy.da.UpdateCursor(tablepath_bilanz, fields)
        for gemeinde in cursor_bilanz:
            gemeinde[0] = round(gemeinde[1] + gemeinde[2] + gemeinde[3] + gemeinde[4] + gemeinde[5])
            cursor.updateRow(gemeinde)

        c.set_chronicle("Gesamtbilanz", self.folders.get_table(tablename='Chronik_Nutzung',workspace="FGDB_Einnahmen.gdb",project=projektname))


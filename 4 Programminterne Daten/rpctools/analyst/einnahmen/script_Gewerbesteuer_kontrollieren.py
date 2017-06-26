# -*- coding: utf-8 -*-

import os
import sys

import arcpy

from rpctools.utils.params import Tool


class HebesaetzeKontrolle(Tool):
    """HebesaetzeKontrolle-Tool"""

    _param_projectname = 'name'
    _workspace = 'FGDB_Einnahmen.gdb'

    def add_outputs(self):
        pass

    def run(self):
        """run HebesaetzeKontrolle Tool"""

        parameters = self.par
        projektname = self.par.name.value
        hebesatz = self.par.hebesatz.value
        target_gemeinde = self.par.gemeinde.value
        target_gemeinde_kurz = target_gemeinde.split(" ||")[0]
        workspace_projekt_einnahmen = self.folders.get_db('FGDB_Einnahmen.gdb', projektname)
        wanderungssalden = os.path.join(workspace_projekt_einnahmen, 'Gemeindebilanzen')
        fields = ["GEN", "Hebesatz_GewSt"]
        where_clause = '"GEN"' + "='" + target_gemeinde_kurz + "'"
        cursor = arcpy.da.UpdateCursor(wanderungssalden, fields, where_clause)
        for gemeinde in cursor:
            gemeinde[1] = hebesatz
            cursor.updateRow(gemeinde)

        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = mxd.activeDataFrame
        if arcpy.mapping.ListLayers(mxd, projektname, df):
            projekt_layer = arcpy.mapping.ListLayers(mxd, projektname, df)[0]
            if arcpy.mapping.ListLayers(projekt_layer, "Gewerbesteuer"):
                lyr = arcpy.mapping.ListLayers(projekt_layer, "Gewerbesteuer")[0]
                lyr.symbology.reclassify()

            arcpy.RefreshActiveView()
            arcpy.RefreshTOC()






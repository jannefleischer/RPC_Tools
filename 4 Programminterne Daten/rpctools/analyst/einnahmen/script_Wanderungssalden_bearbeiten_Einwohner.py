# -*- coding: utf-8 -*-

import arcpy, sys

import arcpy, os, inspect, pyodbc, shutil, gc, sys, datetime, xlsxwriter, imp
from xlsxwriter.utility import xl_rowcol_to_cell
from os.path import join, isdir, abspath, dirname, basename
import rpctools.utils.chronik as c
from rpctools.utils.params import Tool

import rpctools.utils.tempmdb_lib as mdb
import rpctools.utils.population_lib as pop

class Salden_bearbeiten(Tool):

    _param_projectname = 'name'
    _workspace = 'FGDB_Einnahmen.gdb'

    def add_outputs(self):
        pass

    def run(self):

        parameters = self.par
        projektname = self.par.name.value
        saldo = self.par.saldo.value
        target_gemeinde = self.par.gemeinde.value

        workspace_projekt_einnahmen = self.folders.get_db('FGDB_Einnahmen.gdb', projektname)
        wanderungssalden = os.path.join(workspace_projekt_einnahmen, 'Gemeindebilanzen')
        fields = ["GEN", "Einw_Saldo", "SvB_Saldo"]
        cursor = arcpy.da.UpdateCursor(wanderungssalden, fields)
        for gemeinde in cursor:
            if gemeinde[0] == target_gemeinde.split(" ||")[0]:
                gemeinde[1] = saldo
                cursor.updateRow(gemeinde)

        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = mxd.activeDataFrame
        if arcpy.mapping.ListLayers(mxd, projektname, df):
            projekt_layer = arcpy.mapping.ListLayers(mxd, projektname, df)[0]
            if arcpy.mapping.ListLayers(projekt_layer, "Wanderungssalden Einwohner"):
                lyr = arcpy.mapping.ListLayers(projekt_layer, "Wanderungssalden Einwohner")[0] # 5th layer in TOC
                lyr.symbology.reclassify()

            arcpy.RefreshActiveView()
            arcpy.RefreshTOC()

        c.set_chronicle("Wanderung Einwohner", self.folders.get_table(tablename='Chronik_Nutzung',workspace="FGDB_Einnahmen.gdb",project=projektname))



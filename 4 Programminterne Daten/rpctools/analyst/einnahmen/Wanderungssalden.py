# -*- coding: utf-8 -*-

import arcpy, sys

import arcpy, os, inspect, pyodbc, shutil, gc, sys, datetime, xlsxwriter, imp
from xlsxwriter.utility import xl_rowcol_to_cell
from os.path import join, isdir, abspath, dirname, basename

from rpctools.utils.params import Tool

import rpctools.utils.tempmdb_lib as mdb
import rpctools.utils.population_lib as pop

class Wanderungssalden(Tool):

    _param_projectname = 'name'
    _dbname = 'FGDB_Einnahmen.gdb'

    def run(self):

        parameters = self.par
        projektname = self.par.name.value

    # Pruefen, ob Wanderungssalden-Layer existiert; falls ja, dann loeschen
        layer_pfad = self.folders.get_db("FGDB_Einnahmen.gdb", projektname)
        wanderungssalden_pfad = os.path.join(layer_pfad, "Wanderungssalden")
        layer_existiert = arcpy.Exists(wanderungssalden_pfad)

        if layer_existiert == 1:
            arcpy.Delete_management(wanderungssalden_pfad)


    # Gemeinden im Umkreis ermitteln und speichern
        km = 20
        umkreis_km = str(km) + " Kilometers"

        workspace_basisdaten = self.folders.get_basedb('FGDB_Basisdaten_deutschland.gdb')
        inputGemeinden = join(workspace_basisdaten, 'bkg_gemeinden')
        if  arcpy.Exists("gemeinden_lyr"):
            arcpy.Delete_management("gemeinden_lyr")
        arcpy.MakeFeatureLayer_management(inputGemeinden, "gemeinden_lyr")

        workspace_projekt_definition = self.folders.get_db('FGDB_Definition_Projekt.gdb', projektname)
        projektflaechen = join(workspace_projekt_definition, 'Teilflaechen_Plangebiet')
        if  arcpy.Exists("projektflaechen_lyr"):
            arcpy.Delete_management("projektflaechen_lyr")
        arcpy.MakeFeatureLayer_management(projektflaechen, "projektflaechen_lyr")

        workspace_projekt_einnahmen = self.folders.get_db('FGDB_Einnahmen.gdb', projektname)
        wanderungssalden = join(workspace_projekt_einnahmen, 'Wanderungssalden')
        arcpy.SelectLayerByLocation_management("gemeinden_lyr", "INTERSECT", "projektflaechen_lyr", umkreis_km, "NEW_SELECTION")
        arcpy.CopyFeatures_management("gemeinden_lyr", wanderungssalden)

    # Hinzuf?gen leerer Spalten zu Wanderungssalden
        arcpy.AddField_management(wanderungssalden, "Einw_Zuzug", "LONG")
        arcpy.AddField_management(wanderungssalden, "Einw_Fortzug", "LONG")
        arcpy.AddField_management(wanderungssalden, "Einw_Saldo", "LONG")
        arcpy.AddField_management(wanderungssalden, "SvB_Zuzug", "LONG")
        arcpy.AddField_management(wanderungssalden, "SvB_Fortzug", "LONG")
        arcpy.AddField_management(wanderungssalden, "SvB_Saldo", "LONG")

    # Anteile der Herkunftsgemeinden an SvB/Einwohner bestimmen
    # Dummy-Rechenweg
        fields = ["Einw_Zuzug", "Einw_Fortzug", "Einw_Saldo", "SvB_Zuzug", "SvB_Fortzug", "SvB_Saldo", "Shape_Area"]
        cursor = arcpy.da.UpdateCursor(wanderungssalden, fields)
        for gemeinde in cursor:
            gemeinde[0] = (gemeinde[6] % 10) *2
            gemeinde[1] = ((gemeinde[6] % 8) * -1) *2
            gemeinde[2] = gemeinde[0] + gemeinde[1]
            gemeinde[3] = (gemeinde[6] % 7) *2
            gemeinde[4] = ((gemeinde[6] % 6) * -1)*2
            gemeinde[5] = gemeinde[3] + gemeinde[4]
            cursor.updateRow(gemeinde)

    #Pr?fen, ob Gewerbe und/oder Wohngebiete existieren
        wohnen_exists = False
        gewerbe_exists = False

        table_teilflaechen = self.folders.get_table(tablename= 'Teilflaechen_Plangebiet', fgdb = "FGDB_Definition_Projekt.gdb", project = projektname)
        fields = "Nutzungsart"
        cursor = arcpy.da.SearchCursor(table_teilflaechen, fields)
        wohnen_gewerbe_exists = False

        for flaeche in cursor:
            if flaeche[0] == 1:
                wohnen_exists = True
            if flaeche[0] == 2:
                gewerbe_exists = True

    #Einwohnersaldo-Layer hinzuf?gen
        if wohnen_exists:
            self.output.delete_output("Positive Wanderungssalden Einwohner")
            self.output.add_output(group = self.output.module["einnahmen"],
                                featureclass = self.folders.get_table(project = projektname, tablename = "Wanderungssalden"),
                                layername = self.folders.get_layer(layername = "Positive Wanderungssalden Einwohner", enhance = True, folder="einnahmen"),
                                subgroup = "Wanderungssalden Einwohner"
                                    )
            self.output.delete_output("Negative Wanderungssalden Einwohner")
            self.output.add_output(group = self.output.module["einnahmen"],
                                    featureclass = self.folders.get_table(project = projektname, tablename = "Wanderungssalden"),
                                    layername = self.folders.get_layer(layername = "Negative Wanderungssalden Einwohner", enhance = True, folder="einnahmen"),
                                    disable_other = False,
                                    subgroup = "Wanderungssalden Einwohner"
                                    )

    #Gewerbesaldo-Layer hinzuf?gen
        if gewerbe_exists:
            self.output.delete_output("Positive Wanderungssalden Erwerbstätige")
            self.output.add_output(group = self.output.module["einnahmen"],
                                featureclass = self.folders.get_table(project = projektname, tablename = "Wanderungssalden"),
                                layername = self.folders.get_layer(layername = "Positive Wanderungssalden Erwerbstätige", enhance = True, folder="einnahmen"),
                                disable_other = False,
                                subgroup = "Wanderungssalden Erwerbstätige"
                                )
            self.output.delete_output("Negative Wanderungssalden Erwerbstätige")
            self.output.add_output(group = self.output.module["einnahmen"],
                                featureclass = self.folders.get_table(project = projektname, tablename = "Wanderungssalden"),
                                layername = self.folders.get_layer(layername = "Negative Wanderungssalden Erwerbstätige", enhance = True, folder="einnahmen"),
                                disable_other = False,
                                subgroup = "Wanderungssalden Erwerbstätige"
                                )

    #   Symbology anpassen
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = mxd.activeDataFrame
        projekt_layer = arcpy.mapping.ListLayers(mxd, projektname, df)[0]
        if arcpy.mapping.ListLayers(projekt_layer, "Negative Wanderungssalden Einwohner"):
            lyr = arcpy.mapping.ListLayers(projekt_layer, "Negative Wanderungssalden Einwohner")[0]
            lyr.symbology.reclassify()
        if arcpy.mapping.ListLayers(mxd, "Negative Wanderungssalden Erwerbstätige"):
            lyr = arcpy.mapping.ListLayers(mxd, "Negative Wanderungssalden Erwerbstätige")[0]
            lyr.symbology.reclassify()
        arcpy.RefreshTOC()



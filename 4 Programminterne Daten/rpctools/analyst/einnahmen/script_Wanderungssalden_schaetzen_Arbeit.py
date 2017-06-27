# -*- coding: utf-8 -*-

import arcpy, sys
import numpy as np
import arcpy, os, inspect, pyodbc, shutil, gc, sys, datetime, xlsxwriter, imp
from xlsxwriter.utility import xl_rowcol_to_cell
from os.path import join, isdir, abspath, dirname, basename

from rpctools.utils.params import Tool
import rpctools.utils.weighted_mean as wmean
import rpctools.utils.tempmdb_lib as mdb
import rpctools.utils.allgemeine_Rahmendaten as rahmendaten
import rpctools.utils.chronik as c
import rpctools.utils.layer_einnahmen as lib_einnahmen

class Wanderungssalden2(Tool):

    _param_projectname = 'name'
    _workspace = 'FGDB_Einnahmen.gdb'

    def add_outputs(self):
        self.output.delete_output("SvB_Saldo")

        gemeinde_werte = lib_einnahmen.get_values(["SvB_Saldo"], self.projectname)

        symbology = lib_einnahmen.get_symbology(gemeinde_werte, 1)

        self.output.add_layer(
            groupname = "einnahmen",
            featureclass = "Gemeindebilanzen",
            template_layer = symbology,
            template_folder = "einnahmen",
            name = "SvB_Saldo",
            disable_other = True,
            symbology = {'valueField': "SvB_Saldo"},
            label_replace = {'Einw_Saldo': 'SvB_Saldo'}
        )

        arcpy.RefreshTOC()
        arcpy.RefreshActiveView()

    def run(self):

        parameters = self.par
        projektname = self.projectname

        lib_einnahmen.create_gemeindebilanzen(self, projektname)

    # Pruefen, ob Wanderungssalden-Tabelle existiert; falls ja, dann loeschen
        layer_pfad = self.folders.get_db("FGDB_Einnahmen.gdb", projektname)
        wanderungssalden_pfad = os.path.join(layer_pfad, "Gemeindebilanzen")

    #Alte Layer löschen
        self.output.delete_output("Wanderungssalden Erwerbstätige")

        workspace_projekt_definition = self.folders.get_db('FGDB_Definition_Projekt.gdb', projektname)
        workspace_projekt_einnahmen = self.folders.get_db('FGDB_Einnahmen.gdb', projektname)
        wanderungssalden = join(workspace_projekt_einnahmen, 'Gemeindebilanzen')

        projektflaechen = join(workspace_projekt_definition, 'Teilflaechen_Plangebiet')
        if  arcpy.Exists("projektflaechen_lyr"):
            arcpy.Delete_management("projektflaechen_lyr")
        arcpy.MakeFeatureLayer_management(projektflaechen, "projektflaechen_lyr")

        fields = ["SvB_Zuzug", "SvB_Fortzug", "SvB_Saldo"]
        cursor = arcpy.da.UpdateCursor(wanderungssalden, fields)
        for gemeinde in cursor:
            gemeinde[0] = 0
            gemeinde[1] = 0
            gemeinde[2] = 0
            cursor.updateRow(gemeinde)

    # Anteile der Herkunftsgemeinden an SvB bestimmen

        km = 20
        umkreis_km = str(km) + " Kilometers"

        # Buffer um Teilflächen
        pfad_buffer = os.path.join(workspace_projekt_einnahmen, "Buffer")
        if arcpy.Exists(pfad_buffer):
            arcpy.Delete_management(pfad_buffer)

        arcpy.Buffer_analysis(
                                in_features = "projektflaechen_lyr",
                                out_feature_class = pfad_buffer,
                                buffer_distance_or_field = umkreis_km,
                                dissolve_option = "ALL")

        # Verschneiden von Buffer und Gemeindebilanzen-Gemeinde-Layer
        pfad_verschnitt = os.path.join(workspace_projekt_einnahmen, "Verschnitt")
        if arcpy.Exists(pfad_verschnitt):
            arcpy.Delete_management(pfad_verschnitt)

        arcpy.Intersect_analysis([wanderungssalden, pfad_buffer], pfad_verschnitt)

        # Parameter: Exponentialfaktoren für Umzugsweiten Wohnen und Gewerbe
        exponentialfaktor_gewerbe = -0.13
        konstant_bis_km_gewerbe = 3

        # Mittelpunkt der Projektflächen
        table = 'Teilflaechen_Plangebiet'
        columns = np.array(['Nutzungsart', 'Flaeche_ha', 'INSIDE_X', 'INSIDE_Y'])
        Results = wmean.Read_FGDB(workspace_projekt_definition, table, columns)
        Results.get_result_block()
        gewichtete_koordinaten = wmean.calc_weighted_mean(Results.result_block)
        x_projektflaeche = gewichtete_koordinaten[0]
        y_projektflaeche = gewichtete_koordinaten[1]

        # Gewichtete Einwohner/SvB bestimmen
        gewichtete_ew_gesamt = 0
        gewichtete_SvB_gesamt = 0
        fields = ["AGS", "Einwohner", "SvB_pro_Ew", "Shape_Area", "Gewichtete_Ew", "Gewichtete_SvB", "GK3_X", "GK3_Y"]
        cursor = arcpy.da.UpdateCursor(wanderungssalden, fields)
        for gemeinde in cursor:
            flaeche_verschnitt = 0
            cursor_verschnitt = arcpy.da.SearchCursor(pfad_verschnitt, ["AGS", "Shape_Area"])
            for gemeinde_verschnitt in cursor_verschnitt:
                if gemeinde[0] == gemeinde_verschnitt[0]:
                    flaeche_verschnitt += gemeinde_verschnitt[1]
            entfernung_km = (((x_projektflaeche - gemeinde[6]) ** 2 +  (y_projektflaeche - gemeinde[7]) ** 2) ** 0.5) / 1000
            # Gewerbe
            if entfernung_km < konstant_bis_km_gewerbe:
                entfernungsgewichtung_gewerbe = 1
            else:
                entfernungsgewichtung_gewerbe = np.exp((entfernung_km - konstant_bis_km_gewerbe) * exponentialfaktor_gewerbe)
            gewichtete_SvB = gemeinde[1] * gemeinde[2] * (flaeche_verschnitt / gemeinde[3]) * entfernungsgewichtung_gewerbe
            gemeinde[5] = gewichtete_SvB
            gewichtete_SvB_gesamt += gewichtete_SvB
            cursor.updateRow(gemeinde)

        # Wanderungsanteile bestimmen
        fields = ["Gewichtete_SvB", "Wanderungsanteil_SvB"]
        cursor = arcpy.da.UpdateCursor(wanderungssalden, fields)
        for gemeinde in cursor:

            gemeinde[1] = gemeinde[0] / gewichtete_SvB_gesamt
            cursor.updateRow(gemeinde)

        # Berechnung der Einwohner und SvB im Plangebiet
        erwerbstaetige_projekt = rahmendaten.Erwerbstaetige_referenz_plangebiet(self, projektname)

        # Bestimme AGS der Projektgemeinde
        pfad_rahmendaten = self.folders.get_table(
            tablename='Projektrahmendaten',
            workspace="FGDB_Definition_Projekt.gdb",
            project=projektname)
        cursor = arcpy.da.SearchCursor(pfad_rahmendaten, ["AGS"])
        for projekt in cursor:
            ags_projekt = projekt[0]


        #Ergebnis einfügen
        fields = ["SvB_Zuzug", "SvB_Fortzug", "SvB_Saldo", "Wanderungsanteil_SvB", "AGS"]
        cursor = arcpy.da.UpdateCursor(wanderungssalden, fields)
        for gemeinde in cursor:
            gemeinde[1] = erwerbstaetige_projekt * gemeinde[3] * -1
            if gemeinde[4] == ags_projekt:
                gemeinde[0] = erwerbstaetige_projekt
            else:
                gemeinde[0] = 0
            gemeinde[2] = gemeinde[0] + gemeinde[1]
            cursor.updateRow(gemeinde)

        #Prüfen, ob Gewerbe  existieren
        wohnen_exists = False
        gewerbe_exists = False

        table_teilflaechen = self.folders.get_table(
            tablename='Teilflaechen_Plangebiet',
            workspace="FGDB_Definition_Projekt.gdb",
            project=projektname)
        fields = "Nutzungsart"
        cursor = arcpy.da.SearchCursor(table_teilflaechen, fields)
        wohnen_gewerbe_exists = False

        for flaeche in cursor:
            if flaeche[0] == 2:
                gewerbe_exists = True

        groupname = "einnahmen"
        tbl_wanderungssalden = self.folders.get_table("Gemeindebilanzen")
        folder = "einnahmen"
        disable_other = False

##        #Gewerbesaldo-Layer hinzufügen
##        if gewerbe_exists:
##            subgroup = "Wanderungssalden Erwerbstätige"
##            lyrnames = ["Wanderungssalden Erwerbstätige"]
##            for layername in lyrnames:
##                self.output.replace_output(
##                    groupname, tbl_wanderungssalden, layername,
##                    folder, subgroup, disable_other)
##
##    #   Symbology anpassen
##        mxd = arcpy.mapping.MapDocument("CURRENT")
##        negative_saldos = [
##            "Negative Wanderungssalden Einwohner",
##            "Negative Wanderungssalden Erwerbstätige",
##        ]
##        projekt_layer = self.output.get_projectlayer(projektname)
##        for layername in negative_saldos:
##            self.output.reclassify_layer(projekt_layer, layername)
##        arcpy.RefreshTOC()







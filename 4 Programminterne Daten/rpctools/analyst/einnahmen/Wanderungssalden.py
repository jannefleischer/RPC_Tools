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

class Wanderungssalden(Tool):

    _param_projectname = 'name'
    _workspace = 'FGDB_Einnahmen.gdb'

    def run(self):

        parameters = self.par
        projektname = self.projectname

    # Pruefen, ob Wanderungssalden-Tabelle existiert; falls ja, dann loeschen
        layer_pfad = self.folders.get_db("FGDB_Einnahmen.gdb", projektname)
        wanderungssalden_pfad = os.path.join(layer_pfad, "Wanderungssalden")
        layer_existiert = arcpy.Exists(wanderungssalden_pfad)

        if layer_existiert == 1:
            arcpy.Delete_management(wanderungssalden_pfad)

    #Alte Layer löschen
        self.output.delete_output("Wanderungssalden Einwohner")
        self.output.delete_output("Wanderungssalden Erwerbstätige")


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
        arcpy.AddField_management(wanderungssalden, "Gewichtete_Ew", "DOUBLE")
        arcpy.AddField_management(wanderungssalden, "Gewichtete_SvB", "DOUBLE")
        arcpy.AddField_management(wanderungssalden, "Wanderungsanteil_Ew", "DOUBLE")
        arcpy.AddField_management(wanderungssalden, "Wanderungsanteil_SvB", "DOUBLE")
        arcpy.AddField_management(wanderungssalden, "Einw_Zuzug", "LONG")
        arcpy.AddField_management(wanderungssalden, "Einw_Fortzug", "LONG")
        arcpy.AddField_management(wanderungssalden, "Einw_Saldo", "LONG")
        arcpy.AddField_management(wanderungssalden, "SvB_Zuzug", "LONG")
        arcpy.AddField_management(wanderungssalden, "SvB_Fortzug", "LONG")
        arcpy.AddField_management(wanderungssalden, "SvB_Saldo", "LONG")

        fields = ["Einw_Zuzug", "Einw_Fortzug", "Einw_Saldo", "SvB_Zuzug", "SvB_Fortzug", "SvB_Saldo"]
        cursor = arcpy.da.UpdateCursor(wanderungssalden, fields)
        for gemeinde in cursor:
            gemeinde[0] = 0
            gemeinde[1] = 0
            gemeinde[2] = 0
            gemeinde[3] = 0
            gemeinde[4] = 0
            gemeinde[5] = 0
            cursor.updateRow(gemeinde)

    # Anteile der Herkunftsgemeinden an SvB/Einwohner bestimmen

        # Buffer um Teilflächen
        pfad_buffer = os.path.join(workspace_projekt_einnahmen, "Buffer")
        if arcpy.Exists(pfad_buffer):
            arcpy.Delete_management(pfad_buffer)

        arcpy.Buffer_analysis(
                                in_features = "projektflaechen_lyr",
                                out_feature_class = pfad_buffer,
                                buffer_distance_or_field = umkreis_km,
                                dissolve_option = "ALL")

        # Verschneiden von Buffer und Wanderungssalden-Gemeinde-Layer
        pfad_verschnitt = os.path.join(workspace_projekt_einnahmen, "Verschnitt")
        if arcpy.Exists(pfad_verschnitt):
            arcpy.Delete_management(pfad_verschnitt)

        arcpy.Intersect_analysis([wanderungssalden, pfad_buffer], pfad_verschnitt)

        # Parameter: Exponentialfaktoren für Umzugsweiten Wohnen und Gewerbe
        exponentialfaktor_wohnen = -0.1
        exponentialfaktor_gewerbe = -0.13
        konstant_bis_km_wohnen = 3
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
            # Einwohner
            if entfernung_km < konstant_bis_km_wohnen:
                entfernungsgewichtung_wohnen = 1
            else:
                entfernungsgewichtung_wohnen = np.exp((entfernung_km - konstant_bis_km_wohnen) * exponentialfaktor_wohnen)
            gewichtete_ew = gemeinde[1] * (flaeche_verschnitt / gemeinde[3]) * entfernungsgewichtung_wohnen
            gemeinde[4] = gewichtete_ew
            gewichtete_ew_gesamt += gewichtete_ew
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
        fields = ["Gewichtete_Ew", "Wanderungsanteil_Ew", "Gewichtete_SvB", "Wanderungsanteil_SvB"]
        cursor = arcpy.da.UpdateCursor(wanderungssalden, fields)
        for gemeinde in cursor:

            gemeinde[1] = gemeinde[0] / gewichtete_ew_gesamt
            gemeinde[3] = gemeinde[2] / gewichtete_SvB_gesamt
            cursor.updateRow(gemeinde)

        # Berechnung der Einwohner und SvB im Plangebiet
        einwohner_projekt = rahmendaten.Bewohner_referenz_plangebiet(self, projektname)
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
        fields = ["Einw_Zuzug", "Einw_Fortzug", "Einw_Saldo", "SvB_Zuzug",
                  "SvB_Fortzug", "SvB_Saldo", "Wanderungsanteil_Ew",
                  "Wanderungsanteil_SvB", "AGS"]
        cursor = arcpy.da.UpdateCursor(wanderungssalden, fields)
        for gemeinde in cursor:
            gemeinde[1] = einwohner_projekt * gemeinde[6] * -1
            if gemeinde[8] == ags_projekt:
                gemeinde[0] = einwohner_projekt
            else:
                gemeinde[0] = 0
            gemeinde[2] = gemeinde[0] + gemeinde[1]
            gemeinde[4] = erwerbstaetige_projekt * gemeinde[6] * -1
            if gemeinde[8] == ags_projekt:
                gemeinde[3] = erwerbstaetige_projekt
            else:
                gemeinde[3] = 0
            gemeinde[5] = gemeinde[3] + gemeinde[4]
            cursor.updateRow(gemeinde)

        #Prüfen, ob Gewerbe und/oder Wohngebiete existieren
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
            if flaeche[0] == 1:
                wohnen_exists = True
            if flaeche[0] == 2:
                gewerbe_exists = True

        groupname = "einnahmen"
        tbl_wanderungssalden = self.folders.get_table("Wanderungssalden")
        folder = "einnahmen"
        disable_other = False

        #Einwohnersaldo-Layer hinzufügen
        if wohnen_exists:
            subgroup = "Wanderungssalden Einwohner"
            lyrnames = ["Positive Wanderungssalden Einwohner",
                        "Negative Wanderungssalden Einwohner"]
            for layername in lyrnames:
                self.output.replace_output(
                    groupname, tbl_wanderungssalden, layername,
                    folder, subgroup, disable_other)

        #Gewerbesaldo-Layer hinzufügen
        if gewerbe_exists:
            subgroup = "Wanderungssalden Erwerbstätige"
            lyrnames = ["Positive Wanderungssalden Erwerbstätige",
                        "Negative Wanderungssalden Erwerbstätige"]
            for layername in lyrnames:
                self.output.replace_output(
                    groupname, tbl_wanderungssalden, layername,
                    folder, subgroup, disable_other)

    #   Symbology anpassen
        mxd = arcpy.mapping.MapDocument("CURRENT")
        negative_saldos = [
            "Negative Wanderungssalden Einwohner",
            "Negative Wanderungssalden Erwerbstätige",
        ]
        projekt_layer = self.output.get_projectlayer(projektname)
        for layername in negative_saldos:
            self.output.reclassify_layer(projekt_layer, layername)
        arcpy.RefreshTOC()







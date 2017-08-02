# -*- coding: utf-8 -*-

import arcpy, sys
import numpy as np
import arcpy, os, inspect, pyodbc, shutil, gc, sys, datetime, xlsxwriter, imp
from xlsxwriter.utility import xl_rowcol_to_cell
from os.path import join, isdir, abspath, dirname, basename
import rpctools.utils.output as output
from rpctools.utils.params import Tool
import rpctools.utils.weighted_mean as wmean
import rpctools.utils.tempmdb_lib as mdb
import rpctools.utils.allgemeine_Rahmendaten as rahmendaten
import rpctools.utils.chronik as c
import rpctools.utils.layer_einnahmen as lib_einnahmen

class Wanderungssalden1(Tool):

    _param_projectname = 'name'
    _workspace = 'FGDB_Einnahmen.gdb'

    def add_outputs(self):

        arcpy.RefreshTOC()
        arcpy.RefreshActiveView()

    def run(self):

        parameters = self.par
        projektname = self.projectname

        lib_einnahmen.create_gemeindebilanzen(self, projektname)

        workspace_projekt_definition = self.folders.get_db('FGDB_Definition_Projekt.gdb', projektname)
        workspace_projekt_einnahmen = self.folders.get_db('FGDB_Einnahmen.gdb', projektname)
        wanderungssalden = os.path.join(workspace_projekt_einnahmen, "Gemeindebilanzen")

        projektflaechen = join(workspace_projekt_definition, 'Teilflaechen_Plangebiet')
        if  arcpy.Exists("projektflaechen_lyr"):
            arcpy.Delete_management("projektflaechen_lyr")
        arcpy.MakeFeatureLayer_management(projektflaechen, "projektflaechen_lyr")

        fields = ["Einw_Zuzug", "Einw_Fortzug", "Einw_Saldo", "Wanderungsanteil_Ew", "Gewichtete_Ew"]
        cursor = arcpy.da.UpdateCursor(wanderungssalden, fields)
        for gemeinde in cursor:
            gemeinde[0] = 0
            gemeinde[1] = 0
            gemeinde[2] = 0
            gemeinde[3] = 0
            gemeinde[4] = 0
            cursor.updateRow(gemeinde)


    # Anteile der Herkunftsgemeinden an Einwohner bestimmen

        # Entfernungsringe um Teilflaechen erstellen
        pfad_buffer = os.path.join(workspace_projekt_einnahmen, "Enternungsringe")
        if arcpy.Exists(pfad_buffer):
            arcpy.Delete_management(pfad_buffer)

        arcpy.MultipleRingBuffer_analysis(
                            "projektflaechen_lyr",
                            pfad_buffer,
                            "1500;2500;3500;4500;6500;8500;11500;14500;18500;25000",
                            "Meters",
                            "distance",
                            "ALL",
                            "OUTSIDE_ONLY"
                            )

        # Verschneiden von Entfernungsringen und Gemeindebilanzen-Gemeinde-Layer
        pfad_verschnitt = os.path.join(workspace_projekt_einnahmen, "Herkunftsraeume")
        if arcpy.Exists(pfad_verschnitt):
            arcpy.Delete_management(pfad_verschnitt)

        arcpy.Intersect_analysis([wanderungssalden, pfad_buffer], pfad_verschnitt)

        #Wichtungsfaktoren auslesen
        Wichtungen_Gewerbe = {}
        Wichtungen_Wohnen = {}

        path_distanzen = self.folders.get_base_table("FGDB_Einnahmen_Tool.gdb", "Wanderung_Entfernungswichtung")
        cursor = arcpy.da.SearchCursor(path_distanzen, ["Distance", "Wichtung_Wohnen", "Wichtung_Gewerbe"])
        for distanz in cursor:
            Wichtungen_Wohnen[str(distanz[0])] = distanz[1]
            Wichtungen_Gewerbe[str(distanz[0])] = distanz[2]

        #Schleife ueber Herkunftsraeume

        pfad_clip = os.path.join(workspace_projekt_einnahmen, "clip")
        if arcpy.Exists(pfad_clip):
            arcpy.Delete_management(pfad_clip)

        pfad_zensusgrid = self.folders.ZENSUS_RASTER_FILE
        herkunftsraeume = []
        Summe_Wichtungsfaktoren_Gesamtraum_Wohnen = 0
        Summe_Wichtungsfaktoren_Gesamtraum_Gewerbe = 0

        cursor = arcpy.da.SearchCursor(pfad_verschnitt, ["OBJECTID", "AGS", "Shape_Area", "distance", "SHAPE@"])
        for polygon in cursor:

            #Verschneidung mit Zensusraster
            arcpy.Clip_management(pfad_zensusgrid, "#", pfad_clip, polygon[4], "-1", "ClippingGeometry")

            #Summe der Pixelwerte/Einwohner bestimmen
            einwohner = arcpy.RasterToNumPyArray(pfad_clip, nodata_to_value = 0)
            einwohner_summe = einwohner.sum()

            if einwohner_summe >= 0:
                arcpy.Delete_management(pfad_clip)

            #SvB pro EW bestimmen
            SvB_je_EW = 0

            where = '"AGS"' + "='" + polygon[1] +"'"
            cursor_gemeindebilanz = arcpy.da.SearchCursor(wanderungssalden, ["AGS", "SvB_pro_Ew"], where)
            for gemeinde in cursor_gemeindebilanz:
                SvB_je_EW += gemeinde[1]

            #Interne Liste der Herkunfstorte erweitern
            Wichtungsfaktor_Wohnen = einwohner_summe * polygon[2] * Wichtungen_Wohnen[str(int(polygon[3]))]
            Wichtungsfaktor_Gewerbe = einwohner_summe * SvB_je_EW * Wichtungen_Gewerbe[str(int(polygon[3]))]

            herkunftsraeume.append([polygon[0], polygon[1], Wichtungsfaktor_Wohnen, Wichtungsfaktor_Gewerbe])

            #Wichtungen zur Summe der Wichtungsfaktoren addieren
            Summe_Wichtungsfaktoren_Gesamtraum_Gewerbe += Wichtungsfaktor_Gewerbe
            Summe_Wichtungsfaktoren_Gesamtraum_Wohnen += Wichtungsfaktor_Wohnen


            arcpy.AddMessage(polygon[1])
            arcpy.AddMessage(einwohner_summe)





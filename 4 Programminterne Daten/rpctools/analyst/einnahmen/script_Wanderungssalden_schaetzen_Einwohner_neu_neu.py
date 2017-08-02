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

        pfad_buffer = os.path.join(workspace_projekt_einnahmen, "buffer_25km")
        if arcpy.Exists(pfad_buffer):
            arcpy.Delete_management(pfad_buffer)

        pfad_Rasterausschnitt = os.path.join(workspace_projekt_einnahmen, "Rasterausschnitt")
        if arcpy.Exists(pfad_Rasterausschnitt):
            arcpy.Delete_management(pfad_Rasterausschnitt)

        pfad_Rasterausschnitt_25km = os.path.join(workspace_projekt_einnahmen, "Rasterausschnitt_25km")
        if arcpy.Exists(pfad_Rasterausschnitt_25km):
            arcpy.Delete_management(pfad_Rasterausschnitt_25km)

        pfad_Punktlayer_25km_posWerte = os.path.join(workspace_projekt_einnahmen, "Punktlayer_25km_posWerte")
        if arcpy.Exists(pfad_Punktlayer_25km_posWerte):
            arcpy.Delete_management(pfad_Punktlayer_25km_posWerte)

        pfad_Entfernungsringe = os.path.join(workspace_projekt_einnahmen, "Entfernungsringe")
        if arcpy.Exists(pfad_Entfernungsringe):
            arcpy.Delete_management(pfad_Entfernungsringe)

        pfad_Herkunftsraeume = os.path.join(workspace_projekt_einnahmen, "Herkunftsgebiete")
        if arcpy.Exists(pfad_Herkunftsraeume):
            arcpy.Delete_management(pfad_Herkunftsraeume)

        pfad_Herkunftsraeume_mit_Ew = os.path.join(workspace_projekt_einnahmen, "Herkunftsgebiete_mit_Ew")
        if arcpy.Exists(pfad_Herkunftsraeume_mit_Ew):
            arcpy.Delete_management(pfad_Herkunftsraeume_mit_Ew)

        pfad_zensusgrid = self.folders.ZENSUS_RASTER_FILE
        pfad_bkggemeinden = self.folders.get_base_table("FGDB_Basisdaten_deutschland.gdb", "bkg_gemeinden")
        Summe_Wichtungsfaktoren_Gesamtraum_Wohnen = 0
        Summe_Wichtungsfaktoren_Gesamtraum_Gewerbe = 0

        cursor = arcpy.da.SearchCursor(pfad_verschnitt, ["OBJECTID", "AGS", "Shape_Area", "distance", "SHAPE@"])

        #25km Buffer um Projektflaeche
        arcpy.Buffer_analysis(projektflaechen, pfad_buffer, "25000 Meters", "FULL", "ROUND", "ALL", "", "PLANAR")

        #Verschneidung mit Zensusraster
        arcpy.Clip_management(pfad_zensusgrid, "7,05950279760912 51,2479511306414 9,96218940268301 53,7710632922632", pfad_Rasterausschnitt, pfad_buffer, "2147483647", "ClippingGeometry", "NO_MAINTAIN_EXTENT")

        #Raterausschnitt in Punktlayer konvertieren
        arcpy.RasterToPoint_conversion(pfad_Rasterausschnitt, pfad_Rasterausschnitt_25km, "Value")

        #LeereSiedlungszellen entfernen
        arcpy.Select_analysis(pfad_Rasterausschnitt_25km, pfad_Punktlayer_25km_posWerte, "[grid_code] > 0")

        #Mehrere Buffer um Projektflaeche erzeugen
        arcpy.MultipleRingBuffer_analysis(projektflaechen, pfad_Entfernungsringe, "1500;2500;3500;4500;6500;8500;11500;14500;18500;25000", "Meters", "distance", "ALL", "FULL")

        #Buffer mit Gemeinden verschneiden
        arcpy.Intersect_analysis([pfad_bkggemeinden, pfad_Entfernungsringe], pfad_Herkunftsraeume, "NO_FID", "", "INPUT")

        #Verschneiden der Herkunftsraume mit den Summen der jeweiligen Punktfeatures
        fm = arcpy.FieldMap()
        fm.mergeRule = 'Sum'

        fms = arcpy.FieldMappings()
        fms.addFieldMap(fm)

        arcpy.SpatialJoin_analysis(pfad_Herkunftsraeume, pfad_Punktlayer_25km_posWerte, pfad_Herkunftsraeume_mit_Ew, "JOIN_ONE_TO_ONE", "KEEP_ALL", fms)


























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





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


        #Wichtungsfaktoren auslesen
        Wichtungen_Gewerbe = {}
        Wichtungen_Wohnen = {}

        path_distanzen = self.folders.get_base_table("FGDB_Einnahmen_Tool.gdb", "Wanderung_Entfernungswichtung")
        cursor = arcpy.da.SearchCursor(path_distanzen, ["Distance", "Wichtung_Wohnen", "Wichtung_Gewerbe"])
        for distanz in cursor:
            Wichtungen_Wohnen[str(int(distanz[0]))] = distanz[1]
            Wichtungen_Gewerbe[str(int(distanz[0]))] = distanz[2]


        #Anteile der Herkunftsgemeinden an Einwohner bestimmen
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


        #25km Buffer um Projektflaeche
        arcpy.Buffer_analysis(projektflaechen, pfad_buffer, "25000 Meters", "FULL", "ROUND", "ALL", "", "PLANAR")

        #Verschneidung mit Zensusraster
        arcpy.Clip_management(pfad_zensusgrid, "7,05950279760912 51,2479511306414 9,96218940268301 53,7710632922632", pfad_Rasterausschnitt, pfad_buffer, "2147483647", "ClippingGeometry", "NO_MAINTAIN_EXTENT")

        #Raterausschnitt in Punktlayer konvertieren
        arcpy.RasterToPoint_conversion(pfad_Rasterausschnitt, pfad_Rasterausschnitt_25km, "Value")

        #LeereSiedlungszellen entfernen
        arcpy.Select_analysis(pfad_Rasterausschnitt_25km, pfad_Punktlayer_25km_posWerte, '"grid_code" > 0')

        #Mehrere Buffer um Projektflaeche erzeugen
        arcpy.MultipleRingBuffer_analysis(projektflaechen, pfad_Entfernungsringe, "1500;2500;3500;4500;6500;8500;11500;14500;18500;25000", "Meters", "distance", "ALL", "FULL")

        #Buffer mit Gemeinden verschneiden
        arcpy.Intersect_analysis([pfad_bkggemeinden, pfad_Entfernungsringe], pfad_Herkunftsraeume, "NO_FID", "", "INPUT")

        #Verschneiden der Herkunftsraume mit den Summen der jeweiligen Punktfeatures

        fieldmappings = arcpy.FieldMappings()
        fieldmappings.addTable(pfad_Herkunftsraeume)
        fieldmappings.addTable(pfad_Punktlayer_25km_posWerte)

        gridcode_FieldIndex = fieldmappings.findFieldMapIndex("grid_code")
        fieldmap = fieldmappings.getFieldMap(gridcode_FieldIndex)
        field = fieldmap.outputField
        field.name = "Summe_Ew"
        field.aliasName = "Summe_Ew"
        fieldmap.outputField = field
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(gridcode_FieldIndex, fieldmap)

        arcpy.SpatialJoin_analysis(pfad_Herkunftsraeume, pfad_Punktlayer_25km_posWerte, pfad_Herkunftsraeume_mit_Ew, "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings)


        #SvB_je_EW

        Summe_Wichtungsfaktoren_Gesamtraum_Wohnen = 0
        Summe_Wichtungsfaktoren_Gesamtraum_Gewerbe = 0
        Summe_Wichtungsfaktoren_Gemeinde_Wohnen = 0
        Summe_Wichtungsfaktoren_Gemeinde_Gewerbe = 0
        SvB_je_EW = 0
        herkunftsraeume = []

        cursor_gemeindebilanz = arcpy.da.SearchCursor(wanderungssalden, ["AGS", "SvB_pro_Ew"])
        for gemeinde in cursor_gemeindebilanz:
            where = '"AGS"' + "='" + gemeinde[0] +"'"
            cursor_Summe_Ew = arcpy.da.SearchCursor(pfad_Herkunftsraeume_mit_Ew, ["AGS", "Summe_Ew", "distance", "Shape_Area"], where)
            for gemeindeteil in cursor_Summe_Ew:
                if gemeindeteil[1] >= 1:
                    Wichtungsfaktor_Wohnen = gemeindeteil[1] * gemeindeteil[3] * Wichtungen_Wohnen[str(int(gemeindeteil[2]))]
                    Wichtungsfaktor_Gewerbe = gemeindeteil[1] * gemeinde[1] * gemeindeteil[3] * Wichtungen_Gewerbe[str(int(gemeindeteil[2]))]
                    herkunftsraeume.append([gemeindeteil[0], Wichtungsfaktor_Wohnen, Wichtungsfaktor_Gewerbe])
                    Summe_Wichtungsfaktoren_Gesamtraum_Wohnen += Wichtungsfaktor_Wohnen
                    Summe_Wichtungsfaktoren_Gesamtraum_Gewerbe += Wichtungsfaktor_Gewerbe

        ap = 0
        bewohner = 0
        teilflaechen = self.folders.get_table("Teilflaechen_Plangebiet", "FGDB_Definition_Projekt.gdb")
        cursor = arcpy.da.SearchCursor(teilflaechen, ["ew", "AP_gesamt"])
        for flaeche in cursor:
            ap += flaeche[1]
            bewohner += flaeche[0]

        cursor_gemeindebilanz = arcpy.da.UpdateCursor(wanderungssalden, ["AGS", "SvB_pro_Ew", "Einw_Fortzug", "SvB_Fortzug", "Einw_Zuzug", "SvB_Zuzug", "SvB_Saldo", "Einw_Saldo"])
        for gemeinde in cursor_gemeindebilanz:
            Summe_Wichtungsfaktoren_Gemeinde_Wohnen = 0
            Summe_Wichtungsfaktoren_Gemeinde_Gewerbe = 0
            for raum in herkunftsraeume:
                if raum[0] == gemeinde[0]:
                    Summe_Wichtungsfaktoren_Gemeinde_Wohnen += raum[1]
                    Summe_Wichtungsfaktoren_Gemeinde_Gewerbe += raum[2]
            gemeinde[2] = -1 * bewohner * Summe_Wichtungsfaktoren_Gemeinde_Wohnen / Summe_Wichtungsfaktoren_Gesamtraum_Wohnen
            gemeinde[3] = -1 * bewohner * Summe_Wichtungsfaktoren_Gemeinde_Gewerbe / Summe_Wichtungsfaktoren_Gesamtraum_Gewerbe
            if gemeinde[0] == "03359010":
                gemeinde[4] = bewohner
                gemeinde[5] = ap
            gemeinde[6] = gemeinde[3] + gemeinde[5]
            gemeinde[7] = gemeinde[4] + gemeinde[2]
            cursor_gemeindebilanz.updateRow(gemeinde)
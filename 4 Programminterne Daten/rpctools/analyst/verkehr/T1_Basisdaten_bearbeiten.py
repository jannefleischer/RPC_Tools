# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 00_Templates_einladen.py
#
# Description: Erstellung der Bevölkerungsprognose für das zu untersuchende Projekt
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# GGR Planung
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


# Import arcpy modules
import os
import gc
import sys

import arcpy
from os.path import join
from rpctools.utils.params import Tool
from rpctools.utils.encoding import encode


class Basisdatenbearbeiten(Tool):
    ws_definition = 'FGDB_Definition_Projekt.gdb'
    _dbname = 'FGDB_Verkehr.gdb'

    def delete_feature_classes(self, deletelist):
        """
        delete feature classes

        Parameters
        ----------
        deletelist : list of str
            the feature classes to be deleted
        """
        for element in deletelist:
            try:
                e = str(element)
                arcpy.Delete_management(e)
            except:
                arcpy.AddWarning(encode(
                    "{} konnte nicht gelöscht werden".format(element)))

    def run(self):

        messages = self.mes
        parameters = self.par

        arcpy.env.overwriteOutput = True

        #Abgeleitete Variablen
        Teilflaechen_Plangebiet = self.folders.get_table(
            'Teilflaechen_Plangebiet', workspace=self.ws_definition)
        Teilflaechen_Plangebiet_Proj = self.folders.get_table(
            'Teilflaechen_Plangebiet')
        Teilflaechen_Plangebiet_Buffer = self.folders.get_table(
            'Teilflaechen_Plangebiet_Buffer', check=False)
        bounding_box = self.folders.get_table('Teilflaechen_Plangebiet_BBox',
                                              check=False)

        gridWGS84 = self.folders.get_table('Siedlungszellen',
                                           check=False)
        grid_bound = self.folders.get_table('Gridbound',
                                            check=False)

        zensusRaster = self.folders.get_base_table(
            'ZensusGrid', 'Zensus2011GridWGS84_int.tif', )
        clippedRaster = self.folders.get_table('clippedZensus100mGrid.tif', check=False)

        #ggf vorhandene Layer loeschen
        deletelist = [gridWGS84, clippedRaster,
                      bounding_box, Teilflaechen_Plangebiet_Buffer]

        self.delete_feature_classes(deletelist)

        #############################################################################################################
        #Puffern und Entstehende Elemente Zusammenfuehren (Dissolve)
        schrittmeldung = u'2000m Umring um Teilflächen des Plangebietes erstellen \n'
        messages.AddMessage(encode(schrittmeldung))

        arcpy.Buffer_analysis(Teilflaechen_Plangebiet, Teilflaechen_Plangebiet_Buffer, "2000 Meters", "FULL", "ROUND", "NONE", "")

        schrittmeldung = u'Entstehende Elemente zu einem Projektumkreis zusammenführen \n'
        messages.AddMessage(encode(schrittmeldung))

        arcpy.Dissolve_management(Teilflaechen_Plangebiet_Buffer, bounding_box, "", "", "MULTI_PART", "DISSOLVE_LINES")

        #############################################################################################################
        #Zensus 2011 Raster zuschneiden
        schrittmeldung = u'Zensus-2011-Raster zuschneiden'
        messages.AddMessage(encode(schrittmeldung))

        # ClipDeutschlandRaster
        arcpy.Clip_management(zensusRaster, "#", clippedRaster, bounding_box, "0", "ClippingGeometry")

        #Zugeschnittenes Zensus-Raster vektorisieren
        arcpy.RasterToPolygon_conversion(clippedRaster, gridWGS84, "NO_SIMPLIFY", "VALUE")

        #############################################################################################################
        #SiedlungszellenIDs erzeugen
        schrittmeldung = u'SiedlungszellenIDs und Einwohnerzahl erzeugen \n'
        messages.AddMessage(encode(schrittmeldung))

        # Felder hinzufügen
        arcpy.AddField_management(gridWGS84, "SZ_ID", "LONG", 9, "", "", "SZ_ID", "NULLABLE", "REQUIRED")
        arcpy.AddField_management(gridWGS84, "SZ_Einwohner", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

        # Felder berechnen
        arcpy.CalculateField_management(gridWGS84, "SZ_ID", "!OBJECTID!", "PYTHON")
        arcpy.CalculateField_management(gridWGS84, "SZ_Einwohner", "round (([Shape_Area]*1000000),0)* [gridcode]", "VB", "")

        # nicht mehr benötigte Felder löschen
        arcpy.DeleteField_management(gridWGS84, "gridcode")

        #############################################################################################################
        # Einladen der Umgebungslayer
        beginmeldung = u'Starte Überarbeitung Übergabepunkte \n'
        messages.AddMessage(encode(beginmeldung))

        #############################################################################################################
        # Schritt 1 - Fuege Layer hinzu
        schrittmeldung = u'Füge Layer hinzu \n'
        messages.AddMessage(encode(schrittmeldung))

        OSM_Baselayer = self.folders.get_layer('OpenStreetMap', enhance=True)
        Teilflaechen_Plangebiet = self.folders.get_table(
            'Teilflaechen_Plangebiet', workspace=self.ws_definition)
        L00_Umfeldabgrenzung = self.folders.get_table('L00_Umfeldabgrenzung')
        L01_Uebergabepunkte = self.folders.get_table('L01_Uebergabepunkte')
        L10_Bestand_Arbeitsplaetze = self.folders.get_table(
            'L10_Bestand_Arbeitsplaetze')
        L11_Bestand_Einzelhandelsflaechen = self.folders.get_table(
            'L11_Bestand_Einzelhandelsflaechen')
        L11_Bestand_Schulen = self.folders.get_table('L11_Bestand_Schulen')

        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd, "*")[0]

        arcpy.mapping.AddLayer(df,OSM_Baselayer,"TOP")
        arcpy.mapping.AddLayer(df,L00_Umfeldabgrenzung,"TOP")
        arcpy.mapping.AddLayer(df,Teilflaechen_Plangebiet,"TOP")
        arcpy.mapping.AddLayer(df,L01_Uebergabepunkte,"TOP")
        arcpy.mapping.AddLayer(df,L10_Bestand_Arbeitsplaetze,"TOP")
        arcpy.mapping.AddLayer(df,L11_Bestand_Einzelhandelsflaechen,"TOP")
        arcpy.mapping.AddLayer(df,L11_Bestand_Schulen,"TOP")

        ext = Teilflaechen_Plangebiet.getExtent()
        df.extent = ext

        names = ['L00_Umfeldabgrenzung']
        layers = arcpy.mapping.ListLayers(mxd, "*", df)

        for layer in layers:
            if layer.name in names:
                layer.visible = False

        arcpy.RefreshTOC()
        arcpy.RefreshActiveView()

        #############################################################################################################
        #Aufraeumen und ueberfluessige Variablen loeschen
        schrittmeldung = 'Aufräumen und überfluessige Variablen löschen \n'
        messages.AddMessage(encode(schrittmeldung))

        deletelist = [clippedRaster, bounding_box,
                      Teilflaechen_Plangebiet_Buffer]

        self.delete_feature_classes(deletelist)
        gc.collect()

        #############################################################################################################
        # Endmeldung
        gc.collect()
        message = 'Script abgeschlossen'
        messages.AddMessage(encode(message))
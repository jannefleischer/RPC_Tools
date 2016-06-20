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
import arcpy, os, gc, sys
import verkehr_lib as v

arcpy.env.overwriteOutput = True

#Pfade einrichten

i=-1

i+=1 ; projektname = arcpy.GetParameterAsText(i)

base_path = str(sys.path[0]).split("2_Tool")[0] # Pfad zum Basisverzeichnis RPC
workspace_projekt_definition =  os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
workspace_projekt_verkehr = os.path.join(base_path,'3_Projekte',projektname,'FGDB_33_Verkehr_'+projektname+'.gdb')
workspace_tool_verkehr = os.path.join(base_path,"2_Tool","33_Verkehr","33_Verkehr_Tool.gdb")
directory_tool_verkehr = os.path.join(base_path,"2_Tool","33_Verkehr")

#Abgeleitete Variablen
Teilflaechen_Plangebiet = os.path.join(workspace_projekt_definition, 'Teilflaechen_Plangebiet')
Teilflaechen_Plangebiet_Proj = os.path.join(workspace_projekt_verkehr, 'Teilflaechen_Plangebiet')
Teilflaechen_Plangebiet_Buffer = os.path.join(workspace_projekt_verkehr, 'Teilflaechen_Plangebiet_Buffer')
bounding_box = os.path.join(workspace_projekt_verkehr, 'Teilflaechen_Plangebiet_BBox')

gridWGS84 = os.path.join(workspace_projekt_verkehr, 'Siedlungszellen')
grid_bound = os.path.join(workspace_projekt_verkehr, 'Gridbound')

zensusRaster = os.path.join(base_path, '1_Basisdaten','ZensusGrid','Zensus2011GridWGS84_int.tif')
clippedRaster = os.path.join(base_path, '3_Projekte', projektname,'clippedZensus100mGrid.tif')

#ggf vorhandene Layer loeschen
deletelist = [gridWGS84, clippedRaster, bounding_box, Teilflaechen_Plangebiet_Buffer]

for element in deletelist:
    try:
        e = str(element)
        arcpy.Delete_management(e)
    except:
        print element, "konnte nicht geloescht werden"

#############################################################################################################
#Puffern und Entstehende Elemente Zusammenfuehren (Dissolve)
schrittmeldung = '2000m Umring um Teilflaechen des Plangebietes erstellen \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

arcpy.Buffer_analysis(Teilflaechen_Plangebiet, Teilflaechen_Plangebiet_Buffer, "2000 Meters", "FULL", "ROUND", "NONE", "")

schrittmeldung = 'Entstehende Elemente zu einem Projektumkreis zusammenfuehren \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

arcpy.Dissolve_management(Teilflaechen_Plangebiet_Buffer, bounding_box, "", "", "MULTI_PART", "DISSOLVE_LINES")

#############################################################################################################
#Zensus 2011 Raster zuschneiden
schrittmeldung = 'Zensus-2011-Raster zuschneiden'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

# ClipDeutschlandRaster
arcpy.Clip_management(zensusRaster, "#", clippedRaster, bounding_box, "0", "ClippingGeometry")

#Zugeschnittenes Zensus-Raster vektorisieren
arcpy.RasterToPolygon_conversion(clippedRaster, gridWGS84, "NO_SIMPLIFY", "VALUE")

#############################################################################################################
#SiedlungszellenIDs erzeugen
schrittmeldung = 'SiedlungszellenIDs und Einwohnerzahl erzeugen \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

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
beginmeldung = 'Starte Ueberarbeitung Uebergabepunkte \n'
arcpy.AddMessage(beginmeldung)
print beginmeldung

#############################################################################################################
# Schritt 1 - Fuege Layer hinzu
schrittmeldung = 'Fuege Layer hinzu \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

OSM_Baselayer = arcpy.mapping.Layer(os.path.join(directory_tool_verkehr,'OpenStreetMap.lyr'))
Teilflaechen_Plangebiet = arcpy.mapping.Layer(os.path.join(workspace_projekt_definition,'Teilflaechen_Plangebiet'))
L00_Umfeldabgrenzung = arcpy.mapping.Layer(os.path.join(workspace_projekt_verkehr,'L00_Umfeldabgrenzung'))
L01_Uebergabepunkte = arcpy.mapping.Layer(os.path.join(workspace_projekt_verkehr,'L01_Uebergabepunkte'))
L10_Bestand_Arbeitsplaetze = arcpy.mapping.Layer(os.path.join(workspace_projekt_verkehr,'L10_Bestand_Arbeitsplaetze'))
L11_Bestand_Einzelhandelsflaechen = arcpy.mapping.Layer(os.path.join(workspace_projekt_verkehr,'L11_Bestand_Einzelhandelsflaechen'))
L11_Bestand_Schulen = arcpy.mapping.Layer(os.path.join(workspace_projekt_verkehr,'L11_Bestand_Schulen'))

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
schrittmeldung = 'Aufraeumen und ueberfluessige Variablen loeschen \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

deletelist = [clippedRaster, bounding_box, Teilflaechen_Plangebiet_Buffer]

for element in deletelist:
    try:
        e = str(element)
        arcpy.Delete_management(e)
    except:
        print element, "konnte nicht geloescht werden"

gc.collect()

#############################################################################################################
# Endmeldung
gc.collect()
message = 'Script abgeschlossen'
print message
arcpy.AddMessage(message)
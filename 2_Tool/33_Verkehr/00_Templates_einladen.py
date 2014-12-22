# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 01_Uebergabepunkte_bearbeiten.py
#
# Description:
#
#Author:
#Achim Tack / Gertz Gutsche Rümenapp
# ---------------------------------------------------------------------------

#############################################################################################################
# Import arcpy modules
import arcpy, os, gc, sys
import verkehr_lib as v

arcpy.env.overwriteOutput = True

#Pfade einrichten

i=-1

i+=1 ; projektname = arcpy.GetParameterAsText(i)

base_path = str(sys.path[0]).split("2_Tool")[0] # Pfad zum Basisverzeichnis RPC
workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
workspace_projekt_verkehr = os.path.join(base_path,'3_Projekte',projektname,'FGDB_33_Verkehr_'+projektname+'.gdb')
workspace_tool_verkehr = os.path.join(base_path,"2_Tool","33_Verkehr","33_Verkehr_Tool.gdb")

directory_tool_verkehr = os.path.join(base_path,"2_Tool","33_Verkehr")


#############################################################################################################
#
# Durchlauf Berechnung
#
#############################################################################################################
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
arcpy.mapping.AddLayer(df,Teilflaechen_Plangebiet,"TOP")
arcpy.mapping.AddLayer(df,L00_Umfeldabgrenzung,"TOP")
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

# Endmeldung
gc.collect()
message = 'Script abgeschlossen'
print message
arcpy.AddMessage(message)
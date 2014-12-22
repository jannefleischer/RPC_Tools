# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 02_SZ_Erzeugung.py
#
# Description: Erzeuge Siedlungszellen aus einem Grundraster und damit verschnittenen OSM-Elemementen
#
#Author:
#Achim Tack / Gertz Gutsche Rümenapp
# ---------------------------------------------------------------------------

#############################################################################################################
# Import arcpy modules
import os
import gc
import sys

import arcpy


gc.collect()

i = 0
i = i + 1

arcpy.env.overwriteOutput = True

# Variablen definieren
projektname = arcpy.GetParameterAsText(0)
#projektname = 'Bultweg-Sued_01_verdichtet_ohne_Versorger' # haendische Ueberbrueckung bei manueller Scriptnutzung

#Pfade einrichten
base_path = str(sys.path[0]).split("2_Tool")[0]

workspace_basis = os.path.join(base_path, '1_Basisdaten', 'FGBD_01_Basisdaten_deutschland.gdb')
workspace_projekt = os.path.join(base_path, '3_Projekte', projektname,
                                 'FGDB_11_Definition_Projekt_' + projektname + '.gdb')
workspace_siedlungszellen = os.path.join(base_path, '3_Projekte', projektname,
                                         'FGDB_21_Siedlungszellen_' + projektname + '.gdb')

#Abgeleitete Variablen
Teilflaechen_Plangebiet = os.path.join(workspace_projekt, 'Teilflaechen_Plangebiet')
Teilflaechen_Plangebiet_Proj = os.path.join(workspace_siedlungszellen, 'Teilflaechen_Plangebiet_GK3')
Teilflaechen_Plangebiet_Buffer = os.path.join(workspace_siedlungszellen, 'Teilflaechen_Plangebiet_GK3_Buffer')
bounding_box = os.path.join(workspace_siedlungszellen, 'Teilflaechen_Plangebiet_GK3_BBox')

gridlocation = workspace_siedlungszellen
gridname = 'Siedlungszellen'
gridname84 = 'Siedlungszellen_WGS84'

grid = os.path.join(workspace_siedlungszellen, gridname)
grid84 = os.path.join(workspace_siedlungszellen, gridname84)
grid_bound = os.path.join(workspace_siedlungszellen, 'Gridbound')
grid_osm_union = os.path.join(workspace_siedlungszellen, 'Grid_OSM_Union')
grid_osm_singlepart = os.path.join(workspace_siedlungszellen, 'Grid_OSM_Singlepart')

OSM_roads = os.path.join(workspace_siedlungszellen, 'OSM_roads')
OSM_railways = os.path.join(workspace_siedlungszellen, 'OSM_railways')
OSM_roads_buff = os.path.join(workspace_siedlungszellen, 'OSM_roads_buff')
OSM_railways_buff = os.path.join(workspace_siedlungszellen, 'OSM_railways_buff')
OSM_Features = os.path.join(workspace_siedlungszellen, 'OSM_features')
OSM_Features_dissolved = os.path.join(workspace_siedlungszellen, 'OSM_Features_dissolved')

grid_centroids = os.path.join(workspace_siedlungszellen, 'Siedlungszellen_Centroide')

#############################################################################################################
# Variablen definieren
schrittmeldung = 'Uebergabe der Projektvariablen an Tool \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

k = 150  #rastergoesse in m
schrittweite = 10
iterationen = 4  #anzahl der iterationen um den kern des rasters

#############################################################################################################
#Projizieren
schrittmeldung = 'Teilflaechen des Plangebietes in GK3 projizieren \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

# Determine if the input has a defined coordinate system, can't project it if it does not
dsc = arcpy.Describe(Teilflaechen_Plangebiet)

if dsc.spatialReference.Name == "Unknown":

    print ('skipped this fc due to undefined coordinate system: ' + 'Teilflaechen_Plangebiet')
else:
    # Set output coordinate system
    outCS = arcpy.SpatialReference(31467)

    # start Projection
    arcpy.Project_management(Teilflaechen_Plangebiet, Teilflaechen_Plangebiet_Proj, outCS)

#############################################################################################################
#Puffern
schrittmeldung = '1000m Umring um Teilflaechen des Plangebietes erstellen \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung
arcpy.Buffer_analysis(Teilflaechen_Plangebiet_Proj, Teilflaechen_Plangebiet_Buffer, "1000 Meters", "FULL", "ROUND",
                      "NONE", "")

#############################################################################################################
#Zusammenfuehren (Dissolve)
schrittmeldung = 'Entstehende Elemente zu einem Projektumkreis zusammenfuehren \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

arcpy.Dissolve_management(Teilflaechen_Plangebiet_Buffer, bounding_box, "", "", "MULTI_PART", "DISSOLVE_LINES")

#############################################################################################################
#Groesse der BBox bestimmen
schrittmeldung = 'Groesse des Projektumkreises bestimmen \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

descFC = arcpy.Describe(bounding_box)
extent_x = descFC.extent.XMax - descFC.extent.XMin
extent_y = descFC.extent.YMax - descFC.extent.YMin

#bestimmen, ob hoehe oder breite groesser sind
if extent_x > extent_y:
    l = extent_x
else:
    l = extent_y

#############################################################################################################
#Kachelerzeugung
schrittmeldung = 'Erzeugung der Siedlungszellen (Berechnung und Geometrieerzeugung dauert ggf. mehrere Minuten) \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

arcpy.env.overwriteOutput = True

#minimale Anzahl der Kachelwerte finden, die in die BBox hinein passen
n = int(l / k) + 1
i = i + 1

rasternullpunkt_x = descFC.extent.XMin
rasternullpunkt_y = descFC.extent.YMin

#neue FeatureClass erzeugen
try:
    arcpy.CreateFeatureclass_management(gridlocation, gridname, "POLYGON", "", "DISABLED", "DISABLED",
                                        "PROJCS['DHDN_3_Degree_Gauss_Zone_3',GEOGCS['GCS_Deutsches_Hauptdreiecksnetz',DATUM['D_Deutsches_Hauptdreiecksnetz',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',3500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',9.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]];-2122500 -10001000 10000;-100000 10000;-100000 10000;0,001;0,001;0,001;IsHighPrecision",
                                        "", "0", "0", "0")
except:
    arcpy.DeleteFeatures_management(grid)
    arcpy.CreateFeatureclass_management(gridlocation, gridname, "POLYGON", "", "DISABLED", "DISABLED",
                                        "PROJCS['DHDN_3_Degree_Gauss_Zone_3',GEOGCS['GCS_Deutsches_Hauptdreiecksnetz',DATUM['D_Deutsches_Hauptdreiecksnetz',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',3500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',9.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]];-2122500 -10001000 10000;-100000 10000;-100000 10000;0,001;0,001;0,001;IsHighPrecision",
                                        "", "0", "0", "0")


#Rasterzellen fuer erste Rasterstufe erstellen
cur = arcpy.InsertCursor(grid)
for i1 in range(0, n):
    for i2 in range(0, n):

        point1 = [rasternullpunkt_x + (i1 * k), rasternullpunkt_y + (i2 * k)]
        point2 = [(rasternullpunkt_x + (i1 * k) + k), (rasternullpunkt_y + (i2 * k))]
        point3 = [(rasternullpunkt_x + (i1 * k) + k), (rasternullpunkt_y + (i2 * k) + k)]
        point4 = [(rasternullpunkt_x + (i1 * k)), (rasternullpunkt_y + (i2 * k) + k)]

        coordList = [point1, point2, point3, point4]

        point = arcpy.Point()
        ary = arcpy.Array()

        for coord in coordList:
            point.X = coord[0]
            point.Y = coord[1]
            ary.add(point)

        #zum Abschluss greife ich nochmal auf meine coordList zu und fuege den ersten Punkt nochmals ein.
        #Hiermit wird sichergestellt, dass das Polygon geschlossen ist.
        point.X = coordList[0][0]
        point.Y = coordList[0][1]
        ary.add(point)

        polygon = arcpy.Polygon(ary)

        row = cur.newRow()
        row.Shape = polygon
        cur.insertRow(row)

del cur
del point1, point2, point3, point4

#Rasterzellen fuer naechste Rasterstufen erstellen
i = i + 1
print 'Schritt ', i

m = n
k = (m * k) / (m - schrittweite)
rasternullpunkt_x = rasternullpunkt_x - (k * schrittweite)
rasternullpunkt_y = rasternullpunkt_y - (k * schrittweite)

arcpy.CopyFeatures_management(grid, grid_bound, "", "0", "0", "0")

cur = arcpy.InsertCursor(grid)

for s in range(0, iterationen):

    m = m + schrittweite

    for i1 in range(0, (m)):
        for i2 in range(0, (m)):
            if i1 <= schrittweite - 1 or i1 >= (m - schrittweite) or i2 <= schrittweite - 1 or i2 >= (m - schrittweite):

                #Punkte fuer die neue Rasterzelle erstellen
                point1 = [(rasternullpunkt_x + (i1 * k)), rasternullpunkt_y + (i2 * k)]
                point2 = [(rasternullpunkt_x + (i1 * k) + k), (rasternullpunkt_y + (i2 * k))]
                point3 = [(rasternullpunkt_x + (i1 * k) + k), (rasternullpunkt_y + (i2 * k) + k)]
                point4 = [(rasternullpunkt_x + (i1 * k)), (rasternullpunkt_y + (i2 * k) + k)]

                coordList = [point1, point2, point3, point4]

                point = arcpy.Point()
                ary = arcpy.Array()

                for coord in coordList:
                    point.X = coord[0]
                    point.Y = coord[1]
                    ary.add(point)

                #zum Abschluss greife ich nochmal auf meine coordList zu und fuege den ersten Punkt nochmals ein.
                #Hiermit wird sichergestellt, dass das Polygon geschlossen ist.
                point.X = coordList[0][0]
                point.Y = coordList[0][1]
                ary.add(point)

                polygon = arcpy.Polygon(ary)

                row = cur.newRow()
                row.Shape = polygon
                cur.insertRow(row)


    #Kachelgroesse anpassen und neuen Rasternullpunkt erstellen
    k = (m * k) / (m - schrittweite)
    rasternullpunkt_x = rasternullpunkt_x - (k * schrittweite)
    rasternullpunkt_y = rasternullpunkt_y - (k * schrittweite)

del cur
del point1, point2, point3, point4

#############################################################################################################
#Verschneiden der Rasterzellen mit OSM-Features
schrittmeldung = 'Verschneiden der Siedlungszellen mit OpenStreetMap-Daten \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

# Script arguments

OSM_roads = os.path.join(workspace_siedlungszellen, 'OSM_roads')
OSM_railways = os.path.join(workspace_siedlungszellen, 'OSM_railways')

OSM_roads_Layer = 'OSM_roads_Layer'
OSM_railways_Layer = 'OSM_railways_Layer'

OSM_roads_buff = os.path.join(workspace_siedlungszellen, 'OSM_roads_buff')
OSM_railways_buff = os.path.join(workspace_siedlungszellen, 'OSM_railways_buff')

OSM_Features = os.path.join(workspace_siedlungszellen, 'OSM_features')
DissolveFeatures = os.path.join(workspace_siedlungszellen, 'Dissolve_features')

# Process: Feature-Layer erstellen (2)
arcpy.MakeFeatureLayer_management(OSM_railways, OSM_railways_Layer, "", "",
                                  "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;osm_id osm_id VISIBLE NONE;name name VISIBLE NONE;type type VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE")

# Process: Layer nach Attributen auswählen (2)
arcpy.SelectLayerByAttribute_management(OSM_railways_Layer, "NEW_SELECTION", "")

# Process: Puffer
arcpy.Buffer_analysis(OSM_railways_Layer, OSM_railways_buff, "1 Meters", "FULL", "ROUND", "NONE", "")

# Process: Feature-Layer erstellen
arcpy.MakeFeatureLayer_management(OSM_roads, OSM_roads_Layer, "", "",
                                  "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;osm_id osm_id VISIBLE NONE;name name VISIBLE NONE;ref ref VISIBLE NONE;type type VISIBLE NONE;oneway oneway VISIBLE NONE;bridge bridge VISIBLE NONE;tunnel tunnel VISIBLE NONE;maxspeed maxspeed VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE")

# Process: Layer nach Attributen auswählen
arcpy.SelectLayerByAttribute_management(OSM_roads_Layer, "NEW_SELECTION",
                                        "\"type\" = 'motorway' OR \"type\" = 'motorway_link' OR \"type\" = 'primary' OR \"type\" = 'primary_link' OR \"type\" = 'secondary' OR \"type\" = 'secondary_link' OR \"type\" = 'tertiary'")

# Process: Puffer (2)
arcpy.Buffer_analysis(OSM_roads_Layer, OSM_roads_buff, "1 Meters", "FULL", "ROUND", "NONE", "")

#Union
inFeatures = [OSM_roads_buff, OSM_railways_buff]
arcpy.Union_analysis(inFeatures, OSM_Features, "ALL", "", "GAPS")

arcpy.Dissolve_management(OSM_Features, OSM_Features_dissolved)

inFeatures = [OSM_Features_dissolved, grid]
arcpy.Union_analysis(inFeatures, grid_osm_union, "ALL", "", "GAPS")

# Process: Multipart to Singlepart
arcpy.MultipartToSinglepart_management(grid_osm_union, grid_osm_singlepart)

# Process: Feature-Layer erstellen
Grid_OSM_Singlepart_Layer = 'Grid_OSM_Singlepart_Layer'
arcpy.MakeFeatureLayer_management(grid_osm_singlepart, Grid_OSM_Singlepart_Layer, "", "",
                                  "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;FID_OSM_Features_dissolved FID_OSM_Features_dissolved VISIBLE NONE;FID_Teilflaechen_Plangebiet_GK3_Grid FID_Teilflaechen_Plangebiet_GK3_Grid VISIBLE NONE;ORIG_FID ORIG_FID VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE")

# Process: Layer nach Attributen auswählen
arcpy.SelectLayerByAttribute_management(Grid_OSM_Singlepart_Layer, "NEW_SELECTION",
                                        "\"FID_OSM_Features_dissolved\" = -1")

# Process: Features kopieren
arcpy.CopyFeatures_management(Grid_OSM_Singlepart_Layer, grid, "", "0", "0", "0")

### Process: Integrieren
#arcpy.Integrate_management(grid, "5 Meters")

#############################################################################################################
#Verschneiden der Rasterzellen mit Gemeindeumringen
schrittmeldung = 'Verschneiden der Siedlungszellen mit Gemeindeumringen \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

gemeinden = os.path.join(workspace_basis, 'bkg_gemeinden')
ausgabe = os.path.join(workspace_siedlungszellen, 'Grid_Gemeinden')
Grid_Gemeinden_Layer = 'Grid_Gemeinden_Layer'

inFeatures = [grid, gemeinden]
arcpy.Union_analysis(inFeatures, ausgabe, "ALL", "", "GAPS")

# Process: Feature-Layer erstellen
arcpy.MakeFeatureLayer_management(ausgabe, Grid_Gemeinden_Layer, "", "", "")

# Process: Layer nach Attributen auswählen
arcpy.SelectLayerByAttribute_management(Grid_Gemeinden_Layer, "NEW_SELECTION", "\"FID_Siedlungszellen_1\" > 0")

# Process: Features kopieren
arcpy.CopyFeatures_management(Grid_Gemeinden_Layer, grid, "", "0", "0", "0")

#############################################################################################################
#SiedlungszellenIDs erzeugen
schrittmeldung = 'SiedlungszellenIDs erzeugen \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

arcpy.AddField_management(grid, "SZ_ID", "LONG", 9, "", "", "SZ_ID", "NULLABLE", "REQUIRED")

arcpy.CalculateField_management(grid, "SZ_ID", "!OBJECTID!", "PYTHON")


#############################################################################################################
#Aufraeumen und ueberfluessige Variablen loeschen
schrittmeldung = 'Aufraeumen und ueberfluessige Variablen loeschen \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

deletelist = [bounding_box, OSM_roads_buff, OSM_railways_buff, OSM_Features, OSM_Features_dissolved, grid_bound,
              grid_osm_union,
              grid_osm_singlepart, Teilflaechen_Plangebiet_Proj, Teilflaechen_Plangebiet_Buffer, DissolveFeatures,
              ausgabe]

for element in deletelist:
    try:
        e = str(element)
        arcpy.Delete_management(e)
    except:
        print element, "konnte nicht geloescht werden"

gc.collect()

# Endmeldung
message = 'Script abgeschlossen'
print message
arcpy.AddMessage(message)
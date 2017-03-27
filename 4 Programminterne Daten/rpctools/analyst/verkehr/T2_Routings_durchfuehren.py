# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 02_Routings_durchfuehren.py
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
import pyodbc
import shutil
import gc
import sys
import imp
from os.path import join
from rpctools.utils.params import Tool

import arcpy

import rpctools.utils.verkehr_lib as v
import rpctools.utils.tempmdb_lib as mdb

class Routingsdurchfuehren(Tool):

    def run(self):

        messages = self.mes
        parameters = self.par
        arcpy.env.overwriteOutput = True

    	# Variables
    	i=-1

    	i+=1 ; projektname = self.par.projectname.value
    	i+=1 ; mapquest_key =self.par.mapkey.value

    	#projektname = "Bultweg-Sued_02_verdichtet_mit_Versorger"

    	# Workspaces
    	base_path = str(sys.path[0]).split("2 Planungsprojekte analysieren")[0] # Pfad zum Basisverzeichnis RPC
    	workspace_projekt = join(base_path,'3 Benutzerdefinierte Projekte',projektname)
    	workspace_projekt_definition = self.folders.get_db('FGDB_Definition_Projekt.gdb', projektname)
    	workspace_projekt_verkehr = self.folders.get_db('FGDB_Verkehr.gdb', projektname)
    	workspace_tool_verkehr = join(base_path,'4 Programminterne Daten','fgdbs',"Verkehr_Tool.gdb")

    	# Layers and Tables
    	out_folder_path = join(workspace_projekt,"temp") # Pfad zur temporaeren mdb inkl.
    	temp_mdb_path = join(out_folder_path,"PGDB_Temp.mdb")

    	teilflaechen_plangebiet = join(workspace_projekt_definition,'Teilflaechen_Plangebiet')
    	teilflaechen_plangebiet_centroid = join(workspace_projekt_definition,'Teilflaechen_Plangebiet_Centroide')
    	siedlungszellen_centroid = join(workspace_projekt_verkehr,'Siedlungszellen_Centroide')
    	siedlungszellen_centroid_projektumfeld = join(workspace_projekt_verkehr,"L02_SZ_Umfeld")

    	umfeldabgrenzung = join(workspace_projekt_verkehr,"L00_Umfeldabgrenzung")
    	uebergabepunkte = join(workspace_projekt_verkehr,"L01_Uebergabepunkte")

    	routen_sz = join(workspace_projekt_verkehr,"L03_Routen_SZ")
    	routen_tf = join(workspace_projekt_verkehr,"L03_Routen_TF")

    	routen_geometrie_sz = join(workspace_projekt_verkehr,"L04_Routing_Geometrie_SZ")
    	routen_geometrie_tf = join(workspace_projekt_verkehr,"L04_Routing_Geometrie_TF")

    	strassenabschnitte_sz = join(temp_mdb_path,"strassenabschnitte_sz")
    	strassenabschnitte_tf = join(temp_mdb_path,"strassenabschnitte_tf")

    	routen_ergebniskacheln = join(workspace_projekt_verkehr,"L05_Ergebniskacheln")
    	routen_ergebniskacheln_sz_join = join(workspace_projekt_verkehr,"L05_Ergebniskacheln_sz_join")
    	routen_ergebniskacheln_tf_join = join(workspace_projekt_verkehr,"L05_Ergebniskacheln_tf_join")

    	grid = join(workspace_projekt_verkehr,'Siedlungszellen')
    	grid_centroids = join(workspace_projekt_verkehr,'Siedlungszellen_Centroide')


    	#############################################################################################################
    	#
    	# Durchlauf Berechnung
    	#
    	#############################################################################################################
    	beginmeldung = 'Starte Routenberechnung und Verkehrsmengenerzeugung \n'
    	messages.AddMessage(beginmeldung)
    	print beginmeldung
    	#############################################################################################################
    	# Punktlayer aus Siedlungszellen erzeugen
    	schrittmeldung = 'Punktlayer aus Siedlungszellen erzeugen \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	# Process: Feature-Class erstellen
    	try:
    		arcpy.DeleteFeatures_management(grid_centroids)
    	except Exception as e:
    		print e

    	arcpy.CreateFeatureclass_management(workspace_projekt_verkehr, "Siedlungszellen_Centroide", "POINT", "", "DISABLED", "DISABLED", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8,98315284119522E-09;0,001;0,001;IsHighPrecision", "", "0", "0", "0")

    	# Set local variables
    	fieldName = "SZ_ID"
    	fieldAlias = "SZ_ID"
    	fieldPrecision = 9

    	# Execute AddField twice for two new fields
    	arcpy.DeleteField_management(grid_centroids, fieldName)
    	arcpy.AddField_management(grid_centroids, fieldName, "LONG", fieldPrecision, "", "",fieldAlias, "NULLABLE")

    	# Create search cursor
    	polygon_rows = arcpy.SearchCursor(grid)
    	shapeName = arcpy.Describe(grid).shapeFieldName

    	centroid_rows = arcpy.InsertCursor(grid_centroids)

    	for polygon_row in polygon_rows:
    		feat = polygon_row.getValue(shapeName)
    		SZ_ID = polygon_row.SZ_ID
    		werte = (SZ_ID, feat.trueCentroid)
    		#messages.AddMessage(werte)
    		#print werte

    		latValue = str(feat.trueCentroid).split(' ')[1]
    		lonValue = str(feat.trueCentroid).split(' ')[0]

    		#print latValue, lonValue

    		vertex = arcpy.CreateObject("Point")
    		vertex.X = lonValue
    		vertex.Y = latValue

    		feature = centroid_rows.newRow()
    		feature.shape = vertex
    		feature.SZ_ID = SZ_ID
    		centroid_rows.insertRow(feature)

    	del centroid_rows
    	del polygon_row
    	del polygon_rows

    	arcpy.AddXY_management(grid_centroids)

    	#############################################################################################################
    	# TeilflaechenIDs erzeugen
    	schrittmeldung = 'TeilflaechenIDs erzeugen \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	try:
    		arcpy.DeleteField_management(teilflaechen_plangebiet, "TF_ID")
    	except Exception as e:
    		print schrittmeldung, e

    	try:
    		arcpy.AddField_management(teilflaechen_plangebiet, "TF_ID", "LONG", 9, "", "", "SZ_ID", "NULLABLE", "REQUIRED")
    		arcpy.CalculateField_management(teilflaechen_plangebiet, "TF_ID", "!OBJECTID!", "PYTHON")
    	except Exception as e:
    		print schrittmeldung, e

    	#############################################################################################################
    	# Erzeuge Punktlayer fuer Teilflaechen
    	schrittmeldung = 'Erzeuge Punktlayer fuer Teilflaechen \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	try:
    		arcpy.DeleteFeatures_management(teilflaechen_plangebiet_centroid)
    	except:
    		pass

    	# Process: Feature-Class erstellen
    	arcpy.CreateFeatureclass_management(workspace_projekt_definition, "Teilflaechen_Plangebiet_Centroide", "POINT", "", "DISABLED", "DISABLED", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8,98315284119522E-09;0,001;0,001;IsHighPrecision", "", "0", "0", "0")

    	# Set local variables
    	fieldName = "TF_ID"
    	fieldAlias = "TF_ID"
    	fieldPrecision = 9

    	# Execute AddField twice for two new fields
    	arcpy.AddField_management(teilflaechen_plangebiet_centroid, fieldName, "LONG", fieldPrecision, "", "",fieldAlias, "NULLABLE")

    	# Create search cursor
    	polygon_rows = arcpy.SearchCursor(teilflaechen_plangebiet)
    	shapeName = arcpy.Describe(teilflaechen_plangebiet).shapeFieldName

    	centroid_rows = arcpy.InsertCursor(teilflaechen_plangebiet_centroid)

    	for polygon_row in polygon_rows:
    		feat = polygon_row.getValue(shapeName)
    		TF_ID = polygon_row.TF_ID
    		#werte = (TF_ID, feat.trueCentroid)
    		#messages.AddMessage(werte)
    		#print werte

    		latValue = str(feat.trueCentroid).split(' ')[1]
    		lonValue = str(feat.trueCentroid).split(' ')[0]

    		#print latValue, lonValue

    		vertex = arcpy.CreateObject("Point")
    		vertex.X = lonValue
    		vertex.Y = latValue

    		feature = centroid_rows.newRow()
    		feature.shape = vertex
    		feature.TF_ID = TF_ID
    		centroid_rows.insertRow(feature)

    	del centroid_rows
    	del polygon_row
    	del polygon_rows

    	arcpy.AddXY_management(teilflaechen_plangebiet_centroid)

    	#############################################################################################################
    	# XY-Koordinaten fuer Uebergabepunkte erzeugen
    	schrittmeldung = 'XY-Koordinaten fuer Uebergabepunkte erzeugen \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	try:
    		dropFields = ['POINT_X','POINT_Y']
    		arcpy.DeleteField_management(uebergabepunkte, dropFields)
    	except:
    		pass

    	arcpy.AddXY_management(uebergabepunkte)

    	try:
    		dropFields = ['POINT_X','POINT_Y']
    		arcpy.DeleteField_management(siedlungszellen_centroid, dropFields)
    	except:
    		pass

    	arcpy.AddXY_management(siedlungszellen_centroid)

    	#############################################################################################################
    	# Selektiere Siedlungszellen im Projektumfeld
    	schrittmeldung = 'Selektiere Siedlungszellen im Projektumfeld \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	# First, make a layer from the Feature CLass
    	arcpy.MakeFeatureLayer_management(siedlungszellen_centroid, "sz_centroid_lyr")

    	# Process: Layer lagebezogen auswählen
    	arcpy.SelectLayerByLocation_management("sz_centroid_lyr", "INTERSECT", umfeldabgrenzung, "", "NEW_SELECTION")

    	# Process: Features kopieren
    	arcpy.CopyFeatures_management("sz_centroid_lyr", siedlungszellen_centroid_projektumfeld, "", "0", "0", "0")


    	#############################################################################################################
    	#############################################################################################################
    	# Programmabschnitt Routings Siedlungszellen
    	#############################################################################################################
    	#############################################################################################################

    	# Erzeuge Routendatenbank
    	schrittmeldung = 'Erzeuge Routendatenbank \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	arcpy.env.overwriteOutput = True

    	# Create Temp Folder
    	if not os.path.exists(out_folder_path):
    		arcpy.CreateFolder_management(workspace_projekt, "temp")

    	# Create Temp MDB File
    	out_name = "PGDB_Temp.mdb"
    	out_version = "10.0"
    	try:
    		arcpy.CreatePersonalGDB_management(out_folder_path, out_name, out_version)
    	except:
    		shutil.rmtree(out_folder_path)
    		if not os.path.exists(out_folder_path): os.makedirs(out_folder_path)


    	# run SQL code to create table in PGDB
    	sql = """CREATE TABLE routes
    				(
    				route_id int,
    				lat1 double,
    				lon1 double,
    				lat2 double,
    				lon2 double,
    				checksum double
    				);"""

    	connectionstring = 'DRIVER={Microsoft Access Driver (*.mdb)};DBQ='+temp_mdb_path # create connection string

    	conn = pyodbc.connect(connectionstring)
    	cursor = conn.cursor()
    	try:
    		cursor.execute(sql)
    		messages.AddMessage("Befehl ausgefuehrt \n")
    	except Exception as e:
    		print sql
    		print e
    		print "sql-fehlerhaft"
    		messages.AddMessage("sql-fehlerhaft \n")
    	conn.commit()
    	conn.close()

    	#############################################################################################################
    	# Erzeuge Liste der SZ Routings
    	schrittmeldung = 'Erzeuge Liste der Verkehrszellenroutings \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	eingangstabellen = [
    		(workspace_projekt_verkehr,'L02_SZ_Umfeld'),
    		(workspace_projekt_verkehr,'L01_Uebergabepunkte')
    	]

    	ausgabetabelle = (workspace_projekt_verkehr,'L03_Routen_SZ')

    	sql = """SELECT L02_SZ_Umfeld.SZ_ID, L02_SZ_Umfeld.POINT_Y AS SZ_lat, L02_SZ_Umfeld.POINT_X AS SZ_lon, L01_Uebergabepunkte.Punkt_Name, L01_Uebergabepunkte.POINT_Y AS UP_lat, L01_Uebergabepunkte.POINT_X AS UP_lon
    				INTO L03_Routen_SZ
    				FROM L01_Uebergabepunkte, L02_SZ_Umfeld
    				ORDER BY L02_SZ_Umfeld.SZ_ID, L01_Uebergabepunkte.Punkt_Name;
    				"""

    	mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    	#############################################################################################################
    	# RoutingIDs - SZ erzeugen
    	schrittmeldung = 'RoutingIDs - SZ erzeugen \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	arcpy.AddField_management(routen_sz, "Routen_ID", "LONG", 9, "", "", "SZ_ID", "NULLABLE", "REQUIRED")
    	arcpy.CalculateField_management(routen_sz, "Routen_ID", "!OBJECTID!", "PYTHON")

    	#############################################################################################################
    	# Durchfuehrung Routings - SZ (kann einige Zeit dauern)
    	schrittmeldung = 'Durchfuehrung Routings und Geometrieerzeugung - SZ (kann einige Zeit dauern) \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	# Process: Feature-Class erstellen
    	arcpy.CreateFeatureclass_management(workspace_projekt_verkehr, "L04_Routing_Geometrie_SZ", "POLYLINE", "", "DISABLED", "DISABLED", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8,98315284119522E-09;0,001;0,001;IsHighPrecision", "", "0", "0", "0")

    	# Process: Feld hinzufügen
    	arcpy.AddField_management(routen_geometrie_sz, "Route_ID", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    	rows = arcpy.SearchCursor(routen_sz)

    	count = 0

    	for row in rows:
    		count += 1

    	rows = arcpy.SearchCursor(routen_sz)

    	for row in rows:

    		#Counter fuer Anzeige
    		count = count - 1
    		if count % 50 == 0:
    			meldung = "Noch "+ str(count) + " Routen werden berechnet."
    			messages.AddMessage(meldung)

    		try:
    			print row.Routen_ID
    			route_id = row.Routen_ID
    			lat_start = row.SZ_lat
    			lon_start = row.SZ_lon
    			lat_end = row.UP_lat
    			lon_end = row.UP_lon

    			# Routing via Openmapquest
    			waypoints = v.get_mapquest_route(route_id,lat_start,lon_start,lat_end,lon_end,mapquest_key)

    			featureList = []
    			array = arcpy.Array()
    			cursor = arcpy.InsertCursor(routen_geometrie_sz)

    			for routepart in waypoints:

    				wp_lat = routepart[2]
    				wp_lon = routepart[1]

    				point = arcpy.Point()
    				feat = cursor.newRow()

    				# Set X and Y for start and end points
    				point.X = wp_lat
    				point.Y = wp_lon
    				array.add(point)

    			# Create a Polyline object based on the array of points
    			polyline = arcpy.Polyline(array)

    			# Append to the list of Polyline objects
    			featureList.append(polyline)
    			# Insert the feature
    			feat.shape = polyline
    			feat.Route_ID = route_id
    			cursor.insertRow(feat)

    			del feat,cursor,array

    		except Exception as e:
    			print messages.AddMessage(e)

    	del rows

    	schrittmeldung = 'Geometrieerzeugug Siedlungszellen abgeschlossen \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	#############################################################################################################
    	# Bereinige Geometrien aus Routings - SZ
    	schrittmeldung = 'Bereinige Geometrien aus Routings \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	# Local variables:
    	path = "'"+str(routen_geometrie_sz)+"' #"

    	# Process: Integrieren
    	arcpy.Integrate_management(path, "5 Decimeters")

    	#############################################################################################################
    	#############################################################################################################
    	# Programmabschnitt Routings Teilflaechen
    	#############################################################################################################
    	#############################################################################################################

    	# Erzeuge Erzeuge Routendatenbank
    	schrittmeldung = 'Erzeuge Routendatenbank \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	arcpy.env.overwriteOutput = True

    	# Create Temp Folder
    	if not os.path.exists(out_folder_path):
    		arcpy.CreateFolder_management(workspace_projekt, "temp")

    	# Create Temp MDB File
    	out_name = "PGDB_Temp.mdb"
    	out_version = "10.0"
    	try:
    		arcpy.CreatePersonalGDB_management(out_folder_path, out_name, out_version)
    	except:
    		shutil.rmtree(out_folder_path)
    		if not os.path.exists(out_folder_path): os.makedirs(out_folder_path)


    	# run SQL code to create table in PGDB
    	sql = """CREATE TABLE routes
    				(
    				route_id int,
    				lat1 double,
    				lon1 double,
    				lat2 double,
    				lon2 double,
    				checksum double
    				);"""

    	connectionstring = 'DRIVER={Microsoft Access Driver (*.mdb)};DBQ='+temp_mdb_path # create connection string

    	conn = pyodbc.connect(connectionstring)
    	cursor = conn.cursor()
    	try:
    		cursor.execute(sql)
    		#messages.AddMessage("Befehl ausgefuehrt \n")
    	except Exception as e:
    		print sql
    		print e
    		print "sql-fehlerhaft"
    		#messages.AddMessage("sql-fehlerhaft \n")
    	conn.commit()
    	conn.close()

    	#############################################################################################################
    	# Erzeuge Liste der Teilflaechen Routings
    	schrittmeldung = 'Erzeuge Liste der Teilflaechenroutings \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	eingangstabellen = [
    		(workspace_projekt_definition,'Teilflaechen_Plangebiet_Centroide'),
    		(workspace_projekt_verkehr,'L01_Uebergabepunkte')
    	]

    	ausgabetabelle = (workspace_projekt_verkehr,'L03_Routen_TF')

    	sql = """SELECT Teilflaechen_Plangebiet_Centroide.TF_ID, Teilflaechen_Plangebiet_Centroide.POINT_Y AS TF_lat, Teilflaechen_Plangebiet_Centroide.POINT_X AS TF_lon, L01_Uebergabepunkte.Punkt_Name, L01_Uebergabepunkte.POINT_Y AS UP_lat, L01_Uebergabepunkte.POINT_X AS UP_lon
    				INTO L03_Routen_TF
    				FROM L01_Uebergabepunkte, Teilflaechen_Plangebiet_Centroide
    				ORDER BY Teilflaechen_Plangebiet_Centroide.TF_ID, L01_Uebergabepunkte.Punkt_Name;
    				"""

    	mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    	#############################################################################################################
    	# RoutingIDs - Teilflaechen erzeugen
    	schrittmeldung = 'RoutingIDs - Teilflaechen erzeugen \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	arcpy.AddField_management(routen_tf, "Routen_ID", "LONG", 9, "", "", "SZ_ID", "NULLABLE", "REQUIRED")
    	arcpy.CalculateField_management(routen_tf, "Routen_ID", "!OBJECTID!+100000", "PYTHON") #RooutingIDs fuer Teilflaechen beginnen bei 100000

    	#############################################################################################################
    	# Durchfuehrung Routings und Geometrieerzeugung - TF (kann einige Zeit dauern)
    	schrittmeldung = 'Durchfuehrung Routings und Geometrieerzeugung - TF (kann einige Zeit dauern) \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	# Process: Feature-Class erstellen
    	arcpy.CreateFeatureclass_management(workspace_projekt_verkehr, "L04_Routing_Geometrie_TF", "POLYLINE", "", "DISABLED", "DISABLED", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8,98315284119522E-09;0,001;0,001;IsHighPrecision", "", "0", "0", "0")

    	# Process: Feld hinzufügen
    	arcpy.AddField_management(routen_geometrie_tf, "Route_ID", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    	rows = arcpy.SearchCursor(routen_tf)

    	for row in rows:
    		try:
    			route_id = row.Routen_ID
    			lat_start = row.TF_lat
    			lon_start = row.TF_lon
    			lat_end = row.UP_lat
    			lon_end = row.UP_lon

    			# Routing via Openmapquest
    			waypoints = v.get_mapquest_route(route_id,lat_start,lon_start,lat_end,lon_end,mapquest_key)

    			featureList = []
    			array = arcpy.Array()
    			cursor = arcpy.InsertCursor(routen_geometrie_tf)

    			for routepart in waypoints:

    				wp_lat = routepart[2]
    				wp_lon = routepart[1]

    				point = arcpy.Point()
    				feat = cursor.newRow()

    				# Set X and Y for start and end points
    				point.X = wp_lat
    				point.Y = wp_lon
    				array.add(point)

    			# Create a Polyline object based on the array of points
    			polyline = arcpy.Polyline(array)

    			# Append to the list of Polyline objects
    			featureList.append(polyline)
    			# Insert the feature
    			feat.shape = polyline
    			feat.Route_ID = route_id
    			cursor.insertRow(feat)

    			del feat,cursor,array

    		except Exception as e:
    			print e
    			messages.AddMessage(e)

    	del rows

    	schrittmeldung = 'Geometrieerzeugug Teilflaechen abgeschlossen  \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	#############################################################################################################
    	# Bereinige Geometrien aus Routings - Teilflaechen
    	schrittmeldung = 'Bereinige Geometrien aus Routings - Teilflaechen'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	# Local variables:
    	path = "'"+str(routen_geometrie_tf)+"' #"

    	# Process: Integrieren
    	arcpy.Integrate_management(path, "5 Decimeters")

    	#############################################################################################################
    	# Beginn des Programmabschnitts zur Erzeugung von Ergebniskacheln
    	#############################################################################################################
    	# Erzeuge Zielkacheln
    	schrittmeldung = 'Erzeuge Zielkacheln \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	env.outputCoordinateSystem = arcpy.SpatialReference(4326)

    	shapeName = arcpy.Describe(umfeldabgrenzung).shapeFieldName

    	try:
    		arcpy.DeleteFeatures_management(routen_ergebniskacheln)
    	except:
    		pass

    	rows = arcpy.SearchCursor(umfeldabgrenzung)
    	for row in rows:
    		feat = row.getValue(shapeName)
    		extent = feat.extent

    	outFeatureClass = routen_ergebniskacheln

    	# Set the origin of the fishnet
    	originCoordinate = str(extent.XMin)+" "+str(extent.YMin)

    	# Set the orientation
    	yAxisCoordinate = str(extent.XMin)+" "+str(extent.YMax)

    	# Enter 0 for width and height - these values will be calcualted by the tool
    	cellSizeWidth = '0,0005'
    	cellSizeHeight = '0,0005'

    	# Number of rows and columns together with origin and opposite corner
    	# determine the size of each cell
    	numRows =  '0'
    	numColumns = '0'

    	oppositeCoorner = str(extent.XMax)+" "+str(extent.YMax)

    	# Create a point label Feature Class
    	labels = 'false'

    	# Extent is set by origin and opposite corner - no need to use a template fc
    	templateExtent = '#'

    	# Each output cell will be a polygon
    	geometryType = 'POLYGON'

    	arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate, cellSizeWidth, cellSizeHeight, numRows, numColumns, oppositeCoorner, labels, templateExtent, geometryType)

    	try:
    		arcpy.AddField_management(outFeatureClass, "GRID_ID", "LONG", 9, "", "", "GRID_ID", "NULLABLE", "REQUIRED")
    		arcpy.CalculateField_management(outFeatureClass, "GRID_ID", "!OID!", "PYTHON")
    	except:
    		pass

    	#############################################################################################################
    	# Schreibe Werte an Zielkacheln
    	schrittmeldung = 'Schreibe Werte an Zielkacheln \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	variablestring1 = "GRID_ID \"GRID_ID\" true true true 4 Long 0 0 ,First,#,"+routen_geometrie_sz+",GRID_ID,-1,-1;Route_ID \"Route_ID\" true true false 8 Double 0 0 ,First,#,"+routen_geometrie_sz+",Route_ID,-1,-1"
    	variablestring2 = "GRID_ID \"GRID_ID\" true true true 4 Long 0 0 ,First,#,"+routen_geometrie_tf+",GRID_ID,-1,-1;Route_ID \"Route_ID\" true true false 8 Double 0 0 ,First,#,"+routen_geometrie_tf+",Route_ID,-1,-1"

    	# Process: Räumliche Verbindung
    	arcpy.SpatialJoin_analysis(routen_ergebniskacheln, routen_geometrie_sz, routen_ergebniskacheln_sz_join, "JOIN_ONE_TO_MANY", "KEEP_ALL",variablestring1, "INTERSECT", "", "")
    	arcpy.SpatialJoin_analysis(routen_ergebniskacheln, routen_geometrie_tf, routen_ergebniskacheln_tf_join, "JOIN_ONE_TO_MANY", "KEEP_ALL",variablestring2, "INTERSECT", "", "")

    	#############################################################################################################
    	# Erzeuge Liste der Routen je Ergebniskachel
    	schrittmeldung = 'Erzeuge Liste der Routen je Ergebniskachel \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	eingangstabellen = [
    		(workspace_projekt_verkehr,'L05_Ergebniskacheln_sz_join'),
    		(workspace_projekt_verkehr,'L05_Ergebniskacheln_tf_join')
    	]

    	ausgabetabelle = (workspace_projekt_verkehr,'L06_Routen_je_Kachel')

    	sql = """select * into L06_Routen_je_Kachel

    				from (
    				SELECT L05_Ergebniskacheln_sz_join.GRID_ID, L05_Ergebniskacheln_sz_join.Route_ID
    				FROM L05_Ergebniskacheln_sz_join
    				GROUP BY L05_Ergebniskacheln_sz_join.GRID_ID, L05_Ergebniskacheln_sz_join.Route_ID

    				union

    				SELECT L05_Ergebniskacheln_tf_join.GRID_ID, L05_Ergebniskacheln_tf_join.Route_ID
    				FROM L05_Ergebniskacheln_tf_join
    				GROUP BY L05_Ergebniskacheln_tf_join.GRID_ID, L05_Ergebniskacheln_tf_join.Route_ID
    				)
    				as a;
    				"""

    	mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    	#############################################################################################################
    	#Aufraeumen und ueberfluessige Variablen loeschen
    	schrittmeldung = 'Aufraeumen und ueberfluessige Variablen loeschen \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	shutil.rmtree(out_folder_path)

    	gc.collect()

    	# Endmeldung
    	message = 'Script abgeschlossen'
    	print message
    	messages.AddMessage(message)

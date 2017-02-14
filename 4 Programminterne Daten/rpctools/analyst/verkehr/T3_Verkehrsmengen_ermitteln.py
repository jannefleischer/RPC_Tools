# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 03_Verkehrsmengen_ermitteln.py
#
# Description:
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
import imp
from os.path import join
from rpctools.utils.params import Tool
import rpctools.utils.tempmdb_lib as mdb
import rpctools.utils.population_lib as pop

import arcpy

import rpctools.utils.verkehr_lib as v

class VerkehrsmengenErmitteln(Tool):

    def run(self):
        messages = self.mes
        parameters = self.par

    	arcpy.env.overwriteOutput = True

    	# Variables
    	i=-1

    	i+=1 ; projektname = parameters[i].valueAsText

    	#projektname = "HCU_ZGB_OT_Salzdahlum"

    	#Eingangsparameter Wohnen
    	i+=1 ; Wohnen_Wege_EW = parameters[i].value
    	i+=1 ; Wohnen_MIV_Anteil = parameters[i].value / 100.
    	i+=1 ; Wohnen_Pers_KFZ = parameters[i].value
    	i+=1 ; Wohnen_Anteil_Besucherfahrten = parameters[i].value / 100.
    	i+=1 ; Wohnen_WF_Fahrten_je_EW = parameters[i].value

    	#Eingangsparameter Versorgung
    	i+=1 ; Versorgung_BGF_Beschaeftigter = parameters[i].value
    	i+=1 ; Versorgung_Anwesenheit = parameters[i].value
    	i+=1 ; Versorgung_Wege_Beschaeftigter = parameters[i].value
    	i+=1 ; Versorgung_MIV_Anteil = parameters[i].value / 100.
    	i+=1 ; Versorgung_Pers_KFZ = parameters[i].value
    	i+=1 ; Versorgung_Besucher_Tag = parameters[i].value
    	i+=1 ; Versorgung_Lieferwege_100m2 = parameters[i].value

    	#Eingangsparameter Gewerbe
    	i+=1 ; Gewerbe_Anwesenheit = parameters[i].value / 100.
    	i+=1 ; Gewerbe_Wege_Beschaeftigter = parameters[i].value
    	i+=1 ; Gewerbe_MIV_Anteil = parameters[i].value / 100.
    	i+=1 ; Gewerbe_Pers_KFZ = parameters[i].value
    	i+=1 ; Kundenwege_Beschaeftigte = parameters[i].value
    	i+=1 ; Gewerbe_Lieferwege_Beschaeftigte = parameters[i].value

    	#Eingangsparameter Schulen
    	i+=1 ; Schulen_Wege_Schueler = parameters[i].value
    	i+=1 ; Schulen_MIV_Anteil = parameters[i].value / 100.
    	i+=1 ; Schulen_Schueler_KFZ = parameters[i].value
    	i+=1 ; Schulen_Schueler_je_Lehrer = parameters[i].value
    	i+=1 ; Schulen_Wege_Lehrer = parameters[i].value
    	i+=1 ; Schulen_Pers_KFZ = parameters[i].value
    	i+=1 ; Schulen_Lieferwege_Schueler = parameters[i].value


    	# Workspaces
    	base_path = str(sys.path[0]).split("2_Tool")[0] # Pfad zum Basisverzeichnis RPC
    	workspace_projekt = join(base_path,'3 Benutzerdefinierte Projekte',projektname)
    	workspace_basisdaten = join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb')
    	workspace_projekt_definition = join(base_path,'3 Benutzerdefinierte Projekte',projektname,'FGDB_Definition_Projekt.gdb')
    	workspace_projekt_verkehr = join(base_path,'3 Benutzerdefinierte Projekte',projektname,'FGDB_Verkehr.gdb')

    	# Layers and Tables
    	out_folder_path = join(workspace_projekt,"temp") # Pfad zur temporaeren mdb inkl.
    	temp_mdb_path = join(out_folder_path,"PGDB_Temp.mdb")

    	siedlungszellenlayer = join(workspace_projekt_verkehr,'Siedlungszellen')
    	siedlungszellenlayer_eingangsdaten = join(workspace_projekt_verkehr,'L12_SZ_Projektumfeld_Daten_Verkehrserzeugung')
    	siedlungszellenlayer_eingangsdaten_temp1 = join(workspace_projekt_verkehr,'Siedlungszellen_Eingangsdaten_temp1')
    	siedlungszellenlayer_eingangsdaten_temp2 = join(workspace_projekt_verkehr,'Siedlungszellen_Eingangsdaten_temp2')

    	projektlayer_teilflaechen = join(workspace_projekt_definition,'Teilflaechen_Plangebiet')
    	projektlayer_eingangsdaten = join(workspace_projekt_verkehr,'L12_TF_Daten_Verkehrserzeugung')
    	projekt_bevoelkerungszahl = join(workspace_projekt_definition,'Einwohnerzahl')

    	umfeldabgrenzung = join(workspace_projekt_verkehr,"L00_Umfeldabgrenzung")
    	bestand_arbeitsplaetze = join(workspace_projekt_verkehr,"L10_Bestand_Arbeitsplaetze")
    	bestand_einzelhandelsflaechen = join(workspace_projekt_verkehr,"L11_Bestand_Einzelhandelsflaechen")
    	bestand_schulen = join(workspace_projekt_verkehr,"L11_Bestand_Schulen")

    	routen_sz = join(workspace_projekt_verkehr,"L03_Routen_SZ")
    	routen_tf = join(workspace_projekt_verkehr,"L03_Routen_TF")

    	routen_ergebniskacheln = join(workspace_projekt_verkehr,"L05_Ergebniskacheln")

    	strassenabschnitte_sz = join(temp_mdb_path,"strassenabschnitte_sz")
    	strassenabschnitte_tf = join(temp_mdb_path,"strassenabschnitte_tf")

    	#############################################################################################################
    	#
    	# Durchlauf Berechnung
    	#
    	#############################################################################################################
    	beginmeldung = 'Erzeugen der Eingangsdaten je Siedlungszelle \n'
    	messages.AddMessage(beginmeldung)
    	print beginmeldung

    	# First, make a layer from the feature class
    	arcpy.MakeFeatureLayer_management(siedlungszellenlayer, "siedlungszellenlayer_lyr")

    	# Then add a selection to the layer based on location to features in another feature class
    	arcpy.SelectLayerByLocation_management ("siedlungszellenlayer_lyr", "INTERSECT", umfeldabgrenzung)

    	arcpy.CopyFeatures_management("siedlungszellenlayer_lyr", siedlungszellenlayer_eingangsdaten)

    	arcpy.SpatialJoin_analysis(siedlungszellenlayer_eingangsdaten, bestand_arbeitsplaetze, siedlungszellenlayer_eingangsdaten_temp1, "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "INTERSECT", "", "")
    	arcpy.SpatialJoin_analysis(siedlungszellenlayer_eingangsdaten_temp1, bestand_einzelhandelsflaechen, siedlungszellenlayer_eingangsdaten_temp2, "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "INTERSECT", "", "")
    	arcpy.SpatialJoin_analysis(siedlungszellenlayer_eingangsdaten_temp2, bestand_schulen, siedlungszellenlayer_eingangsdaten, "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "INTERSECT", "", "")

    	dropFields = ["Join_Count", "TARGET_FID","Join_Count_1", "TARGET_FID_1","Join_Count_12","TARGET_FID_12","SUM_Join_Count", "GEN", "AGS", "EWZ","Anteil","Punkt_Name","Punkt_Name_1"]
    	arcpy.DeleteField_management(siedlungszellenlayer_eingangsdaten, dropFields)
    	arcpy.Delete_management(siedlungszellenlayer_eingangsdaten_temp1)
    	arcpy.Delete_management(siedlungszellenlayer_eingangsdaten_temp2)

    	#Fuege Felder fuer die Ergebniseintraege an
    	addfiellist =["fahrten_wohnen_ew_tag","fahrten_wohnen_besucher_tag","fahrten_wohnen_wf_tag",
    				  "fahrten_versorgung_beschaeftigte_tag","fahrten_versorgung_kunden_tag","fahrten_versorgung_wf_tag",
    				  "fahrten_gewerbe_beschaeftigte_tag","fahrten_gewerbe_besucher_tag","fahrten_gewerbe_wf_tag",
    				  "fahrten_schulen_schueler_tag","fahrten_schulen_lehrer_tag","fahrten_schulen_wf_tag"]

    	for f in addfiellist:
    		arcpy.AddField_management(siedlungszellenlayer_eingangsdaten, f, "Double", "", "", "")


    	#############################################################################################################
    	beginmeldung = 'Erzeugen der Eingangsdaten je Teilfaeche Plangebiet \n'
    	messages.AddMessage(beginmeldung)
    	print beginmeldung

    	#kopiere Teilflaechenlayer als Eingangsdatenlayer fuer Verkehrsmengenerzeugung und loesche nicht benoetigte felder
    	try:
    		arcpy.Delete_management(projektlayer_eingangsdaten)
    		arcpy.CopyFeatures_management(projektlayer_teilflaechen, projektlayer_eingangsdaten)
    	except:
    		arcpy.CopyFeatures_management(projektlayer_teilflaechen, projektlayer_eingangsdaten)

    	dropFields = ["Startjahr","Vornutzung1","Vornutzung2","Vornutzung3","Anteil1","Anteil2","Anteil3"]
    	for field in dropFields:
    		try:
    			arcpy.DeleteField_management(projektlayer_eingangsdaten, field)
    		except:
    			pass

    	#WOHNEN - EINWOHNERBERECHNUNG

    	pop.recalcPopulation(projektname)

    	#berechne maximale Personenzahl je Teilflaeche
    	eingangstabellen = [
    		(workspace_projekt_definition,'Einwohnerzahl')
    	]

    	ausgabetabelle = (workspace_projekt_definition,'Einwohnerzahl_max')

    	sql = """SELECT Einwohnerzahl.Teilflaeche_Plangebiet, Max(Einwohnerzahl.Einwohnerzahl) AS EW INTO Einwohnerzahl_max
    				FROM Einwohnerzahl
    				GROUP BY Einwohnerzahl.Teilflaeche_Plangebiet;
    				"""

    	mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)


    	#Fuege Felder fuer die Ergebniseintraege an
    	addfiellist = ["TF_Einwohner","Verkaufsflaeche","Arbeitsplaetze","Schueler","fahrten_wohnen_ew_tag","fahrten_wohnen_besucher_tag","fahrten_wohnen_wf_tag",
    				   "fahrten_versorgung_beschaeftigte_tag","fahrten_versorgung_kunden_tag","fahrten_versorgung_wf_tag",
    				   "fahrten_gewerbe_beschaeftigte_tag","fahrten_gewerbe_besucher_tag","fahrten_gewerbe_wf_tag",
    				   "fahrten_schulen_schueler_tag","fahrten_schulen_lehrer_tag","fahrten_schulen_wf_tag"]

    	for f in addfiellist:
    		arcpy.AddField_management(projektlayer_eingangsdaten, f, "Double", "", "", "")

    	#Fuege Einwohnerzahl an
    	bevoelkerung_max_tf = join(workspace_projekt_definition,"Einwohnerzahl_max")

    	rows = arcpy.SearchCursor(bevoelkerung_max_tf)

    	for row in rows:
    		Teilflaeche_Plangebiet = row.Teilflaeche_Plangebiet
    		EW = row.EW

    		rows2 = arcpy.UpdateCursor(projektlayer_eingangsdaten)

    		for row2 in rows2:
    			if row2.Name == Teilflaeche_Plangebiet:
    				row2.TF_Einwohner = EW
    			rows2.updateRow(row2)


    	#GEWERBE - BESCHAEFTIGTENBERECHNUNG
    	eingangstabellen = [
    		(workspace_projekt_definition,'Gewerbe_Beschaeftigte')
    	]

    	ausgabetabelle = (workspace_projekt_definition,'Gewerbe_Beschaeftigte_temp')

    	sql = """SELECT Gewerbe_Beschaeftigte.Jahr, Gewerbe_Beschaeftigte.Teilflaeche_Plangebiet, Sum(Gewerbe_Beschaeftigte.Anzahl) AS Summe INTO Gewerbe_Beschaeftigte_temp
    				FROM Gewerbe_Beschaeftigte
    				GROUP BY Gewerbe_Beschaeftigte.Jahr, Gewerbe_Beschaeftigte.Teilflaeche_Plangebiet
    				ORDER BY Gewerbe_Beschaeftigte.Jahr, Gewerbe_Beschaeftigte.Teilflaeche_Plangebiet, Sum(Gewerbe_Beschaeftigte.Anzahl);
    				"""

    	mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    	eingangstabellen = [
    		(workspace_projekt_definition,'Gewerbe_Beschaeftigte_temp')
    	]

    	ausgabetabelle = (workspace_projekt_definition,'Gewerbe_Beschaeftigte_Max')

    	sql = """SELECT Gewerbe_Beschaeftigte_temp.Teilflaeche_Plangebiet, Max(Gewerbe_Beschaeftigte_temp.Summe) AS [Max] INTO Gewerbe_Beschaeftigte_Max
    				FROM Gewerbe_Beschaeftigte_temp
    				GROUP BY Gewerbe_Beschaeftigte_temp.Teilflaeche_Plangebiet;
    				"""

    	mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    	#Fuege Beschaeftigtenzahl an
    	beschaeftigte_max_tf = join(workspace_projekt_definition,"Gewerbe_Beschaeftigte_Max")

    	rows = arcpy.SearchCursor(beschaeftigte_max_tf)

    	for row in rows:
    		Teilflaeche_Plangebiet = row.Teilflaeche_Plangebiet
    		Beschaeftigte_TF = row.Max

    		rows2 = arcpy.UpdateCursor(projektlayer_eingangsdaten)

    		for row2 in rows2:
    			if row2.Name == Teilflaeche_Plangebiet:
    				row2.Arbeitsplaetze = Beschaeftigte_TF
    			rows2.updateRow(row2)


    	#VERSORGUNG - FLAECHENBERECHNUNG

    	eingangstabellen = [
    		(workspace_projekt_definition,'Versorgung_Verkaufsflaechen')
    	]

    	ausgabetabelle = (workspace_projekt_definition,'Versorgung_Verkaufsflaechen_temp')

    	sql = """SELECT Versorgung_Verkaufsflaechen.Jahr, Versorgung_Verkaufsflaechen.Teilflaeche_Plangebiet, Sum(Versorgung_Verkaufsflaechen.Verkaufsflaeche) AS Summe INTO Versorgung_Verkaufsflaechen_temp
    				FROM Versorgung_Verkaufsflaechen
    				GROUP BY Versorgung_Verkaufsflaechen.Jahr, Versorgung_Verkaufsflaechen.Teilflaeche_Plangebiet
    				ORDER BY Versorgung_Verkaufsflaechen.Jahr, Versorgung_Verkaufsflaechen.Teilflaeche_Plangebiet, Sum(Versorgung_Verkaufsflaechen.Verkaufsflaeche);
    				"""

    	mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    	eingangstabellen = [
    		(workspace_projekt_definition,'Versorgung_Verkaufsflaechen_temp')
    	]

    	ausgabetabelle = (workspace_projekt_definition,'Versorgung_Verkaufsflaechen_Max')

    	sql = """SELECT Versorgung_Verkaufsflaechen_temp.Teilflaeche_Plangebiet, Max(Versorgung_Verkaufsflaechen_temp.Summe) AS [Max] INTO Versorgung_Verkaufsflaechen_Max
    				FROM Versorgung_Verkaufsflaechen_temp
    				GROUP BY Versorgung_Verkaufsflaechen_temp.Teilflaeche_Plangebiet;
    				"""

    	mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    	#Fuege Verkaufsflaeche an
    	verkaufsflaeche_max_tf = join(workspace_projekt_definition,"Versorgung_Verkaufsflaechen_Max")

    	rows = arcpy.SearchCursor(verkaufsflaeche_max_tf)

    	for row in rows:
    		Teilflaeche_Plangebiet = row.Teilflaeche_Plangebiet
    		Verkaufsflaeche_TF = row.Max

    		rows2 = arcpy.UpdateCursor(projektlayer_eingangsdaten)

    		for row2 in rows2:
    			if row2.Name == Teilflaeche_Plangebiet:
    				row2.Verkaufsflaeche = Verkaufsflaeche_TF
    			rows2.updateRow(row2)

    	#############################################################################################################
    	beginmeldung = 'Verkehrsmengenerzeugung Nullfall \n'
    	messages.AddMessage(beginmeldung)
    	print beginmeldung

    	rows = arcpy.SearchCursor(siedlungszellenlayer_eingangsdaten)

    	for row in rows:
    		SZ_ID = row.SZ_ID
    		EW = row.SZ_Einwohner
    		BGF = row.Verkaufsflaeche
    		Beschaeftigte = row.Arbeitsplaetze
    		Schueler = row.Schueler

    		if EW == None:
    			EW = 0.0
    		if BGF == None:
    			BGF = 0.0
    		if Beschaeftigte == None:
    			Beschaeftigte = 0.0
    		if Schueler == None:
    			Schueler = 0.0

    		#Starte Berechnungen je Siedlungszelle
    		fahrten_EW = v.verkehrserzeugung_einwohner(EW,Wohnen_Wege_EW,Wohnen_MIV_Anteil,Wohnen_Pers_KFZ,Wohnen_Anteil_Besucherfahrten,Wohnen_WF_Fahrten_je_EW)
    		fahrten_versorgung = v.verkehrserzeugung_einzelhandel(BGF,Versorgung_BGF_Beschaeftigter,Versorgung_Anwesenheit,Versorgung_Wege_Beschaeftigter,Versorgung_MIV_Anteil,Versorgung_Pers_KFZ,Versorgung_Besucher_Tag,Versorgung_Lieferwege_100m2)
    		fahrten_gewerbe = v.verkehrserzeugung_gewerbe(Beschaeftigte,Gewerbe_Anwesenheit,Gewerbe_Wege_Beschaeftigter,Gewerbe_MIV_Anteil,Gewerbe_Pers_KFZ,Kundenwege_Beschaeftigte,Gewerbe_Lieferwege_Beschaeftigte)
    		fahrten_schule = v.verkehrserzeugung_schulen(Schueler,Schulen_Wege_Schueler,Schulen_MIV_Anteil,Schulen_Schueler_KFZ,Schulen_Schueler_je_Lehrer,Schulen_Wege_Lehrer,Schulen_Pers_KFZ,Schulen_Lieferwege_Schueler)

    		rows2 = arcpy.UpdateCursor(siedlungszellenlayer_eingangsdaten)
    		for r in rows2:
    			if r.SZ_ID == SZ_ID:
    				#Ergebnisse Wohnen
    				r.FAHRTEN_WOHNEN_EW_TAG = fahrten_EW[0]
    				r.FAHRTEN_WOHNEN_BESUCHER_TAG = fahrten_EW[1]
    				r.FAHRTEN_WOHNEN_WF_TAG = fahrten_EW[2]

    				#Ergebnisse Versorgung
    				r.FAHRTEN_VERSORGUNG_BESCHAEFTIGTE_TAG = fahrten_versorgung[0]
    				r.FAHRTEN_VERSORGUNG_KUNDEN_TAG = fahrten_versorgung[1]
    				r.FAHRTEN_VERSORGUNG_WF_TAG = fahrten_versorgung[2]

    				#Ergebnisse Gewerbe
    				r.FAHRTEN_GEWERBE_BESCHAEFTIGTE_TAG = fahrten_gewerbe[0]
    				r.FAHRTEN_GEWERBE_BESUCHER_TAG = fahrten_gewerbe[1]
    				r.FAHRTEN_GEWERBE_WF_TAG = fahrten_gewerbe[2]

    				#Ergebnisse Schule
    				r.FAHRTEN_SCHULEN_SCHUELER_TAG = fahrten_schule[0]
    				r.FAHRTEN_SCHULEN_LEHRER_TAG = fahrten_schule[1]
    				r.FAHRTEN_SCHULEN_WF_TAG = fahrten_schule[2]

    			rows2.updateRow(r)

    	del rows,rows2

    	#############################################################################################################
    	beginmeldung = 'Verkehrsmengenerzeugung Planfall \n'
    	messages.AddMessage(beginmeldung)
    	print beginmeldung

    	rows = arcpy.SearchCursor(projektlayer_eingangsdaten)

    	for row in rows:
    		Name = row.Name
    		EW = row.TF_Einwohner
    		BGF = row.Verkaufsflaeche
    		Beschaeftigte = row.Arbeitsplaetze

    		if EW == None:
    			EW = 0.0
    		if BGF == None:
    			BGF = 0.0
    		if Beschaeftigte == None:
    			Beschaeftigte = 0.0
    		if Schueler == None:
    			Schueler = 0.0

    		#Starte Berechnungen je Projektteilflaeche
    		fahrten_EW = v.verkehrserzeugung_einwohner(EW,Wohnen_Wege_EW,Wohnen_MIV_Anteil,Wohnen_Pers_KFZ,Wohnen_Anteil_Besucherfahrten,Wohnen_WF_Fahrten_je_EW)
    		fahrten_versorgung = v.verkehrserzeugung_einzelhandel(BGF,Versorgung_BGF_Beschaeftigter,Versorgung_Anwesenheit,Versorgung_Wege_Beschaeftigter,Versorgung_MIV_Anteil,Versorgung_Besucher_Tag,Versorgung_Pers_KFZ,Versorgung_Lieferwege_100m2)
    		fahrten_gewerbe = v.verkehrserzeugung_gewerbe(Beschaeftigte,Gewerbe_Anwesenheit,Gewerbe_Wege_Beschaeftigter,Gewerbe_MIV_Anteil,Gewerbe_Pers_KFZ,Kundenwege_Beschaeftigte,Gewerbe_Lieferwege_Beschaeftigte)
    		fahrten_schule = v.verkehrserzeugung_schulen(Schueler,Schulen_Wege_Schueler,Schulen_MIV_Anteil,Schulen_Schueler_KFZ,Schulen_Schueler_je_Lehrer,Schulen_Wege_Lehrer,Schulen_Pers_KFZ,Schulen_Lieferwege_Schueler)

    		rows2 = arcpy.UpdateCursor(projektlayer_eingangsdaten)
    		for r in rows2:
    			if r.Name == Name:
    				#Ergebnisse Wohnen
    				r.FAHRTEN_WOHNEN_EW_TAG = fahrten_EW[0]
    				r.FAHRTEN_WOHNEN_BESUCHER_TAG = fahrten_EW[1]
    				r.FAHRTEN_WOHNEN_WF_TAG = fahrten_EW[2]
    				#print r.Name, fahrten_EW[0]

    				#Ergebnisse Versorgung
    				r.FAHRTEN_VERSORGUNG_BESCHAEFTIGTE_TAG = fahrten_versorgung[0]
    				r.FAHRTEN_VERSORGUNG_KUNDEN_TAG = fahrten_versorgung[1]
    				r.FAHRTEN_VERSORGUNG_WF_TAG = fahrten_versorgung[2]

    				#Ergebnisse Gewerbe
    				r.FAHRTEN_GEWERBE_BESCHAEFTIGTE_TAG = fahrten_gewerbe[0]
    				r.FAHRTEN_GEWERBE_BESUCHER_TAG = fahrten_gewerbe[1]
    				r.FAHRTEN_GEWERBE_WF_TAG = fahrten_gewerbe[2]

    				#Ergebnisse Schule
    				r.FAHRTEN_SCHULEN_SCHUELER_TAG = fahrten_schule[0]
    				r.FAHRTEN_SCHULEN_LEHRER_TAG = fahrten_schule[1]
    				r.FAHRTEN_SCHULEN_WF_TAG = fahrten_schule[2]

    			rows2.updateRow(r)

    	del rows,rows2

    	#############################################################################################################
    	beginmeldung = 'Verkehrsmengen an Routen anspielen  \n'
    	messages.AddMessage(beginmeldung)
    	print beginmeldung

    	#Abschnitt Nullfall
    	eingangstabellen = [
    		(workspace_projekt_verkehr,'L01_Uebergabepunkte'),
    		(workspace_projekt_verkehr,'L03_Routen_SZ'),
    		(workspace_projekt_verkehr,'L03_Routen_TF'),
    		(workspace_projekt_verkehr,'L06_Routen_je_Kachel'),
    		(workspace_projekt_verkehr,'L12_SZ_Projektumfeld_Daten_Verkehrserzeugung')
    	]

    	ausgabetabelle = (workspace_projekt_verkehr,'L13_SZ_Routen_Verkehrsmenge')

    	sql = """SELECT L03_Routen_SZ.Routen_ID, L03_Routen_SZ.SZ_ID, L03_Routen_SZ.Punkt_Name, ([QP_Wohnen]/100)*([fahrten_wohnen_ew_tag]+[fahrten_wohnen_besucher_tag]+[fahrten_wohnen_wf_tag])/2 AS Wohnen_QP, ([ZP_Wohnen]/100)*([fahrten_wohnen_ew_tag]+[fahrten_wohnen_besucher_tag]+[fahrten_wohnen_wf_tag])/2 AS Wohnen_ZP, ([QP_Versorgung]/100)*([fahrten_versorgung_beschaeftigte_tag]+[fahrten_versorgung_kunden_tag]+[fahrten_versorgung_wf_tag])/2 AS Versorgung_QP, ([QP_Schulen]/100)*([fahrten_schulen_schueler_tag]+[fahrten_schulen_lehrer_tag]+[fahrten_schulen_wf_tag])/2 AS Schulen_QP, ([ZP_Versorgung]/100)*([fahrten_versorgung_beschaeftigte_tag]+[fahrten_versorgung_kunden_tag]+[fahrten_versorgung_wf_tag])/2 AS Versorgung_ZP, ([QP_Gewerbe]/100)*([fahrten_gewerbe_beschaeftigte_tag]+[fahrten_gewerbe_besucher_tag]+[fahrten_gewerbe_wf_tag])/2 AS Gewerbe_QP, ([ZP_Gewerbe]/100)*([fahrten_gewerbe_beschaeftigte_tag]+[fahrten_gewerbe_besucher_tag]+[fahrten_gewerbe_wf_tag])/2 AS Gewerbe_ZP, ([ZP_Schulen]/100)*([fahrten_schulen_schueler_tag]+[fahrten_schulen_lehrer_tag]+[fahrten_schulen_wf_tag])/2 AS Schulen_ZP INTO L13_SZ_Routen_Verkehrsmenge
    				FROM (L01_Uebergabepunkte INNER JOIN L03_Routen_SZ ON L01_Uebergabepunkte.Punkt_Name = L03_Routen_SZ.Punkt_Name) INNER JOIN L12_SZ_Projektumfeld_Daten_Verkehrserzeugung ON L03_Routen_SZ.SZ_ID = L12_SZ_Projektumfeld_Daten_Verkehrserzeugung.SZ_ID
    				GROUP BY L03_Routen_SZ.Routen_ID, L03_Routen_SZ.SZ_ID, L03_Routen_SZ.Punkt_Name, ([QP_Wohnen]/100)*([fahrten_wohnen_ew_tag]+[fahrten_wohnen_besucher_tag]+[fahrten_wohnen_wf_tag])/2, ([ZP_Wohnen]/100)*([fahrten_wohnen_ew_tag]+[fahrten_wohnen_besucher_tag]+[fahrten_wohnen_wf_tag])/2, ([QP_Versorgung]/100)*([fahrten_versorgung_beschaeftigte_tag]+[fahrten_versorgung_kunden_tag]+[fahrten_versorgung_wf_tag])/2, ([QP_Schulen]/100)*([fahrten_schulen_schueler_tag]+[fahrten_schulen_lehrer_tag]+[fahrten_schulen_wf_tag])/2, ([ZP_Versorgung]/100)*([fahrten_versorgung_beschaeftigte_tag]+[fahrten_versorgung_kunden_tag]+[fahrten_versorgung_wf_tag])/2, ([QP_Gewerbe]/100)*([fahrten_gewerbe_beschaeftigte_tag]+[fahrten_gewerbe_besucher_tag]+[fahrten_gewerbe_wf_tag])/2, ([ZP_Gewerbe]/100)*([fahrten_gewerbe_beschaeftigte_tag]+[fahrten_gewerbe_besucher_tag]+[fahrten_gewerbe_wf_tag])/2, ([ZP_Schulen]/100)*([fahrten_schulen_schueler_tag]+[fahrten_schulen_lehrer_tag]+[fahrten_schulen_wf_tag])/2;
    				"""

    	mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    	#Abschnitt Planfall
    	eingangstabellen = [
    		(workspace_projekt_verkehr,'L01_Uebergabepunkte'),
    		(workspace_projekt_verkehr,'L03_Routen_SZ'),
    		(workspace_projekt_verkehr,'L03_Routen_TF'),
    		(workspace_projekt_verkehr,'L06_Routen_je_Kachel'),
    		(workspace_projekt_verkehr,'L12_SZ_Projektumfeld_Daten_Verkehrserzeugung'),
    		(workspace_projekt_verkehr,'L12_TF_Daten_Verkehrserzeugung')
    	]

    	ausgabetabelle = (workspace_projekt_verkehr,'L13_TF_Routen_Verkehrsmenge')

    	sql = """SELECT L03_Routen_TF.Routen_ID, L03_Routen_TF.TF_ID, L03_Routen_TF.Punkt_Name, ([QP_Wohnen]/100)*([fahrten_wohnen_ew_tag]+[fahrten_wohnen_besucher_tag]+[fahrten_wohnen_wf_tag])/2 AS Wohnen_QP, ([ZP_Wohnen]/100)*([fahrten_wohnen_ew_tag]+[fahrten_wohnen_besucher_tag]+[fahrten_wohnen_wf_tag])/2 AS Wohnen_ZP, ([QP_Versorgung]/100)*([fahrten_versorgung_beschaeftigte_tag]+[fahrten_versorgung_kunden_tag]+[fahrten_versorgung_wf_tag])/2 AS Versorgung_QP, ([QP_Schulen]/100)*([fahrten_schulen_schueler_tag]+[fahrten_schulen_lehrer_tag]+[fahrten_schulen_wf_tag])/2 AS Schulen_QP, ([ZP_Versorgung]/100)*([fahrten_versorgung_beschaeftigte_tag]+[fahrten_versorgung_kunden_tag]+[fahrten_versorgung_wf_tag])/2 AS Versorgung_ZP, ([QP_Gewerbe]/100)*([fahrten_gewerbe_beschaeftigte_tag]+[fahrten_gewerbe_besucher_tag]+[fahrten_gewerbe_wf_tag])/2 AS Gewerbe_QP, ([ZP_Gewerbe]/100)*([fahrten_gewerbe_beschaeftigte_tag]+[fahrten_gewerbe_besucher_tag]+[fahrten_gewerbe_wf_tag])/2 AS Gewerbe_ZP, ([ZP_Schulen]/100)*([fahrten_schulen_schueler_tag]+[fahrten_schulen_lehrer_tag]+[fahrten_schulen_wf_tag])/2 AS Schulen_ZP INTO L13_TF_Routen_Verkehrsmenge
    				FROM (L01_Uebergabepunkte INNER JOIN L03_Routen_TF ON L01_Uebergabepunkte.Punkt_Name = L03_Routen_TF.Punkt_Name) INNER JOIN L12_TF_Daten_Verkehrserzeugung ON L03_Routen_TF.TF_ID = L12_TF_Daten_Verkehrserzeugung.TF_ID
    				GROUP BY L03_Routen_TF.Routen_ID, L03_Routen_TF.TF_ID, L03_Routen_TF.Punkt_Name, ([QP_Wohnen]/100)*([fahrten_wohnen_ew_tag]+[fahrten_wohnen_besucher_tag]+[fahrten_wohnen_wf_tag])/2, ([ZP_Wohnen]/100)*([fahrten_wohnen_ew_tag]+[fahrten_wohnen_besucher_tag]+[fahrten_wohnen_wf_tag])/2, ([QP_Versorgung]/100)*([fahrten_versorgung_beschaeftigte_tag]+[fahrten_versorgung_kunden_tag]+[fahrten_versorgung_wf_tag])/2, ([QP_Schulen]/100)*([fahrten_schulen_schueler_tag]+[fahrten_schulen_lehrer_tag]+[fahrten_schulen_wf_tag])/2, ([ZP_Versorgung]/100)*([fahrten_versorgung_beschaeftigte_tag]+[fahrten_versorgung_kunden_tag]+[fahrten_versorgung_wf_tag])/2, ([QP_Gewerbe]/100)*([fahrten_gewerbe_beschaeftigte_tag]+[fahrten_gewerbe_besucher_tag]+[fahrten_gewerbe_wf_tag])/2, ([ZP_Gewerbe]/100)*([fahrten_gewerbe_beschaeftigte_tag]+[fahrten_gewerbe_besucher_tag]+[fahrten_gewerbe_wf_tag])/2, ([ZP_Schulen]/100)*([fahrten_schulen_schueler_tag]+[fahrten_schulen_lehrer_tag]+[fahrten_schulen_wf_tag])/2;"""

    	mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    	#############################################################################################################
    	beginmeldung = 'Routenmengen an Ausgaberaster anspielen \n'
    	messages.AddMessage(beginmeldung)
    	print beginmeldung

    	eingangstabellen = [
    		(workspace_projekt_verkehr,'L13_SZ_Routen_Verkehrsmenge'),
    		(workspace_projekt_verkehr,'L13_TF_Routen_Verkehrsmenge'),
    		(workspace_projekt_verkehr,'L06_Routen_je_Kachel')
    	]

    	ausgabetabelle = (workspace_projekt_verkehr,'L14_SZ_Grid_Verkehrsmenge')

    	sql = """SELECT L06_Routen_je_Kachel.GRID_ID, Sum([L13_TF_Routen_Verkehrsmenge]![Wohnen_QP]+[L13_TF_Routen_Verkehrsmenge]![Wohnen_ZP]+[L13_TF_Routen_Verkehrsmenge]![Versorgung_QP]+[L13_TF_Routen_Verkehrsmenge]![Versorgung_ZP]+[L13_TF_Routen_Verkehrsmenge]![Gewerbe_QP]+[L13_TF_Routen_Verkehrsmenge]![Gewerbe_ZP]+[L13_TF_Routen_Verkehrsmenge]![Schulen_QP]+[L13_TF_Routen_Verkehrsmenge]![Schulen_ZP]) AS Traffic_Plangebiet, Sum([L13_SZ_Routen_Verkehrsmenge]![Wohnen_QP]+[L13_SZ_Routen_Verkehrsmenge]![Wohnen_ZP]+[L13_SZ_Routen_Verkehrsmenge]![Versorgung_QP]+[L13_SZ_Routen_Verkehrsmenge]![Versorgung_ZP]+[L13_SZ_Routen_Verkehrsmenge]![Gewerbe_QP]+[L13_SZ_Routen_Verkehrsmenge]![Gewerbe_ZP]+[L13_SZ_Routen_Verkehrsmenge]![Schulen_QP]+[L13_SZ_Routen_Verkehrsmenge]![Schulen_ZP]) AS Traffic_Nullfall INTO L14_SZ_Grid_Verkehrsmenge
    				FROM (L06_Routen_je_Kachel LEFT JOIN L13_TF_Routen_Verkehrsmenge ON L06_Routen_je_Kachel.Route_ID = L13_TF_Routen_Verkehrsmenge.Routen_ID) LEFT JOIN L13_SZ_Routen_Verkehrsmenge ON L06_Routen_je_Kachel.Route_ID = L13_SZ_Routen_Verkehrsmenge.Routen_ID
    				GROUP BY L06_Routen_je_Kachel.GRID_ID;
    				"""

    	mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    	eingangstabellen = [
    		(workspace_projekt_verkehr,'L13_SZ_Routen_Verkehrsmenge'),
    		(workspace_projekt_verkehr,'L13_TF_Routen_Verkehrsmenge'),
    		(workspace_projekt_verkehr,'L06_Routen_je_Kachel')
    	]

    	#Berechne Feld Planfall
    	grid = join(workspace_projekt_verkehr,"L14_SZ_Grid_Verkehrsmenge")
    	arcpy.AddField_management(grid, "Traffic_Planfall", "Double", "", "", "")
    	arcpy.CalculateField_management(grid, "Traffic_Planfall", "(!Traffic_Nullfall! or 0) + (!Traffic_Plangebiet! or 0)", "PYTHON", "")

    	#Berechne Feld prozentuale Steigerung
    	grid = join(workspace_projekt_verkehr,"L14_SZ_Grid_Verkehrsmenge")
    	arcpy.AddField_management(grid, "Traffic_Steigerung", "Double", "", "", "")
    	arcpy.CalculateField_management(grid, "Traffic_Steigerung", "(!Traffic_Planfall! or 0) / (!Traffic_Nullfall! or 0)", "PYTHON", "")

    	#Join Data to Result_Grid
    	# Process: Feature-Layer erstellen
    	arcpy.MakeFeatureLayer_management(routen_ergebniskacheln, "L05_Ergebniskacheln_Layer", "", "", "OID OID VISIBLE NONE;Shape Shape VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE;GRID_ID GRID_ID VISIBLE NONE")

    	# Process: Verbindung hinzuf??gen
    	grid_final = join(workspace_projekt_verkehr,"L15_Grid_Ergebnis")
    	arcpy.AddJoin_management("L05_Ergebniskacheln_Layer", "GRID_ID", grid, "GRID_ID", "KEEP_ALL")
    	arcpy.CopyFeatures_management("L05_Ergebniskacheln_Layer", grid_final)

    	#############################################################################################################
    	#Setze Pfad auf Vorlagen - MXD und tausche Datenquelle aus
    	schrittmeldung = 'Vorbereitung Ergebnisexport \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	#Checke Pfad der mxd_template und tausche diesen aus
    	mxd_template = arcpy.mapping.MapDocument(join(base_path, "2_Tool","Verkehr","Style","template.mxd"))
    	df = arcpy.mapping.ListDataFrames(mxd_template)[0]
    	lyr = arcpy.mapping.ListLayers(mxd_template, "", df)[0]
    	templatepath = join(base_path,"2_Tool","Verkehr","Style","template.gdb")

    	for lyr in arcpy.mapping.ListLayers(mxd_template):
    		if lyr.name == "L15_Grid_Ergebnis":
    			lyr.replaceDataSource(templatepath, 'FILEGDB_WORKSPACE')
    	mxd_template.save()

    	#Kopiere Templatemxd
    	ausgabeordner = join(base_path,'3 Benutzerdefinierte Projekte',projektname,'Ergebnisausgabe','Abbildungen')
    	mxdpfad = join(ausgabeordner,'Verkehr.mxd')
    	mxd_template.saveACopy(mxdpfad)

    	#Ersetze Datenquelle
    	verkehr_mxd = arcpy.mapping.MapDocument(mxdpfad)

    	templatepath = join(base_path,"2_Tool","Verkehr","Style","template.gdb")
    	resultpath = join(base_path,'3 Benutzerdefinierte Projekte',projektname,"FGDB_Verkehr_"+projektname+".gdb")

    	verkehr_mxd.findAndReplaceWorkspacePaths(templatepath, resultpath)
    	verkehr_mxd.save()

    	df = arcpy.mapping.ListDataFrames(verkehr_mxd)[0]
    	lyr = arcpy.mapping.ListLayers(verkehr_mxd, "", df)[0]
    	ext = lyr.getExtent()
    	df.extent = ext

    	for lyr in arcpy.mapping.ListLayers(verkehr_mxd):
    		if lyr.name == "L15_Grid_Ergebnis":
    			lyr.symbology.numClasses = 8

    	verkehr_mxd.save()

    	#Exportiere Ergebnis
    	arcpy.mapping.ExportToJPEG(verkehr_mxd, join(ausgabeordner, 'Verkehr.jpg'), "PAGE_LAYOUT",resolution=300)

    	#############################################################################################################
    	#Aufraeumen und ueberfluessige Variablen loeschen
    	schrittmeldung = 'Aufraeumen und ueberfluessige Variablen loeschen \n'
    	messages.AddMessage(schrittmeldung)
    	print schrittmeldung

    	routen_ergebniskacheln_sz_join = join(workspace_projekt_verkehr,"L05_Ergebniskacheln_sz_join")
    	routen_ergebniskacheln_tf_join = join(workspace_projekt_verkehr,"L05_Ergebniskacheln_tf_join")
    	gewerbebeschaeftigtetemp = (workspace_projekt_definition,'Gewerbe_Beschaeftigte_temp')

    	deletelist = [routen_ergebniskacheln_sz_join,routen_ergebniskacheln_tf_join,gewerbebeschaeftigtetemp]

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
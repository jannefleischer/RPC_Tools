# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# bewertung_wohnflaechendichte.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# ILS gGmbH
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------

import gc
import time
import os
import sys
import arcpy
from os.path import join
from rpctools.utils.params import Tool

class BewertungWohnflaechendichte(Tool):

    param_projectname = 'projectname'
    _dbname = 'FGDB_Flaeche_und_Oekologie.gdb'

    def run(self):
        messages = self.mes
        parameters = self.par

    	projektname = self.par.projectname.value
    	workspace_ergebnisse = self.folders.get_db("FGDB_Flaeche_und_Oekologie.gdb")
    	ergebnisTabelle = join(workspace_ergebnisse,'Ergebnisse_oekologischeWertigkeit')
    	workspace_basis = self.folders.get_basedb('FGDB_Basisdaten_deutschland.gdb')
    	workspace_projekt = self.folders.get_db("FGDB_Definition_Projekt.gdb")
        workspace_oekologie = self.folders.get_basedb('FGDB_Flaeche_und_Oekologie_Tool.gdb')
        path_project = self.folders.get_projectpath(projektname)

    	arcpy.env.overwriteOutput = True
    	##Daten für den Projektraum zusammenstellen
    	#AGS aus den Grundlagendaten extrahieren
    	#Wohnfläche und Nettobauland aus den Grundlagendaten extrahieren
    	#Wohnflaeche gesamt berechenen
    	Wohneinheiten_Details = join(workspace_projekt, 'Wohnen_WE_in_Gebaeudetypen')
    	wohnflaeche_gesamt = 0
    	wohnflaecheTemp = 0
    	efh = 0
    	dh = 0
    	rh = 0
    	mfh = 0

    	cursor = arcpy.SearchCursor(Wohneinheiten_Details)

    	for row in cursor:
    		if row.Gebaeudetyp == "Einfamilienhaus":
    			efh += row.WE * float(parameters[1].valueAsText)
    		elif row.Gebaeudetyp == "Zweifamilien- oder Doppelhaus":
    			efh += row.WE * float(parameters[2].valueAsText)
    		elif row.Gebaeudetyp == "Reihenhaus":
    			efh += row.WE * float(parameters[3].valueAsText)
    		elif row.Gebaeudetyp == "Mehrfamilienhaus":
    			efh += row.WE * float(parameters[4].valueAsText)

    	wohnflaeche_gesamt = efh + dh +rh + mfh

    	pfad_flaeche = join(workspace_projekt,"Teilflaechen_Plangebiet")
    	arcpy.AddField_management(pfad_flaeche,"area_hektares","FLOAT")
    	arcpy.CalculateField_management(pfad_flaeche,"area_hektares","!shape.area@HECTARES!","PYTHON_9.3")

    	flaechengroesse = 0
    	cursor = arcpy.SearchCursor(pfad_flaeche)
    	for flaeche in cursor:
    		flaechengroesse = flaechengroesse + flaeche.area_hektares
    	flaechengroesse = str(flaechengroesse).replace(",",".")
    	#Übernahme der alten Vairable damit nicht zu viel im Folgenden geändert werden muss
    	nettobauland_gesamt = flaechengroesse
    	nettobauland_gesamt = float(nettobauland_gesamt)
    	#Den AGS aus der Lage der projektfläche im Raum ermitteln
    	projektFlaeche = join(workspace_projekt, "Teilflaechen_Plangebiet")
    	bkg = join(workspace_basis, "bkg_gemeinden")
    	#ags aus BKG Daten extrahieren, dafür Gemeinde selektieren, die von Planfläche geschnitten wird
    	#1. Feature Layer aus den bkg-daten erstellen
    	arcpy.MakeFeatureLayer_management(bkg,"bkg_lyr")
    	#2.Spatial Select wo Planfläche bkg_lyr intersected
    	arcpy.SelectLayerByLocation_management("bkg_lyr", "INTERSECT", projektFlaeche)
    	#Wenn Flaeche = 1, ags extrahieren
    	n = arcpy.GetCount_management("bkg_lyr").getOutput(0)
    	if(int(n) ==1 ):
    		gemeindeCursor = arcpy.SearchCursor("bkg_lyr")
    		for gemeinde in gemeindeCursor:
    			ags = gemeinde.AGS
    	#der AGS muss noch angepasst werden, da zur bestimmung des Kreises nur die ersten 5 Stellen gebraucht werden
    	lenAGS = len(ags)
    	if (lenAGS >5):
    		ags = str(ags)
    		ags = ags[0:5]
    		print(ags)

    	#Mittelwerte der einzelnen Kreistypen berechnen
    	#Zur schnelleren Bearbeitung wird Grundlagentabelle komplett in den Arbeitsspeicher geladen
    	table1 = "in_memory//GrundlagenDE"
    	fc = join(workspace_oekologie, "GrundlagenDE")
    	arcpy.CopyRows_management(fc, table1)
    	#Erstellung einer weiteren in_memory Tabelle für die Ergebnisse der Mittelwertsberechnungen für die Kreistypen
    	kreise =arcpy.CreateTable_management("in_memory", "kreise" )
    	arcpy.AddField_management(kreise, "Kreistyp","SHORT")
    	arcpy.AddField_management(kreise, "Mittelwert_Wohnflaechendichte","DOUBLE")
    	#Die einzelnen Kreistypen werden selected und der Mittelwert für die Wohnflächendichte wird berechnet
    	i=1
    	while(i <= 9):
    		sql = "Siedlungsstruktureller_Kreistyp = " + str(i)
    		cursor = arcpy.SearchCursor(table1,sql)
    		anzahl = 0
    		wohnflaechendichte = 0
    		for row in cursor:
    			temp = row.Wohnflaeche_in_Wohngebaeuden_in_qm / row.Gebaeude_und_Freiflaeche_Wohnen_in_ha
    			wohnflaechendichte = wohnflaechendichte + temp
    			anzahl = anzahl +1
    		average = wohnflaechendichte / anzahl
    	#Durschnittswerte der einzelnen Kreistypen in einer in_memory Tabelle ablegen
    		cursor2 = arcpy.InsertCursor(kreise)
    		row = cursor2.newRow()
    		row.Kreistyp = i
    		row.Mittelwert_Wohnflaechendichte = average
    		cursor2.insertRow(row)
    		i= i+1

    	##Zusammenstellung der Vergleichswerte
    	#Für das Projektgebiet
    	projektWohnflaechenDichte = wohnflaeche_gesamt / nettobauland_gesamt

    	#Für den Kreis
    	#Kreisdaten aus den Basisdaten Deutschland  anhand des AGS extrahieren

    	sql = "AGS LIKE '%" +ags +"%'"
    	cursor = arcpy.SearchCursor(fc,sql)
    	for row in cursor:
    		kreistyp = row.Siedlungsstruktureller_Kreistyp
    		wohnflaeche = row.Wohnflaeche_in_Wohngebaeuden_in_qm
    		freiflaeche = row.Gebaeude_und_Freiflaeche_Wohnen_in_ha
    		kreisName = row.Kreis_kreisfreie_Stadt
    	kreisWohnflaechendichte = wohnflaeche/freiflaeche
    	#kreisWohnflaechendichte = 0.26

    	#Durchschnitt fuer den Kreistyp
    	sql = "Kreistyp = " + str(kreistyp)
    	cursor3 = arcpy.SearchCursor(kreise,sql)
    	for row in cursor3:
    		kreistypWohnflaechendichte = row.Mittelwert_Wohnflaechendichte

    	print("Wohnflaechendichte Projekt : " + str(projektWohnflaechenDichte))
    	print("Wohnflaechendichte Kreis   : " + str(kreisWohnflaechendichte))
    	print("Wohnflaechendichte Kreistyp: " + str(kreistypWohnflaechendichte))

    	##Abweichungen berechnen und Graphiken erstellen
    	#Abweichung Projektgebiet - Kreis
    	abweichung = projektWohnflaechenDichte / kreisWohnflaechendichte -1
    	print("Abweichung vom Kreisdurchschnitt: " + str(abweichung))
    	#Abweichung bewerten
    	if(abweichung >= 0.05):
    		bewertung = 5
    	elif(abweichung >= 0) and (abweichung<= 0.05):
    		bewertung = 4
    	elif(abweichung >= -0.05) and (abweichung <= 0):
    		bewertung = 3
    	elif(abweichung >= -0.10) and (abweichung<=-0.05):
    		bewertung = 2
    	elif(abweichung <= -0.10):
    		bewertung = 1
    	print("Bewertung: "+str(bewertung))

    	#Ergebnisse in Ergebnisstabelle ablegen
    	#table = workspace_ergebnisse + "Ergebnisse_Wohnflaechendichte"
    	table= join(workspace_ergebnisse,'Ergebnisse_Wohnflaechendichte')
    	ergebnisse = arcpy.InsertCursor(table)
    	row = ergebnisse.newRow()

    	row.Name = projektname
    	row.Bewertung = bewertung
    	row.WohnflaechendichteProjektraum = projektWohnflaechenDichte
    	row.WohnflaechendichteProjektKreis = kreisWohnflaechendichte
    	row.WohnflaechendichteProjektKreistyp = kreistypWohnflaechendichte
    	lt = time.localtime()
    	year, monat, tag, stunde, minute = lt[0:5]
    	row.timestamp =  str(tag) + "." + str(monat) + "." + str(year) + " - " + str(stunde) + ":" + str(minute)
    	row.abweichungVonKreis = abweichung
    	ergebnisse.insertRow(row)
    	#Daten in die temp-Tabelle zur Diagrammerstellung schreiben
    	table = join(workspace_ergebnisse,"temp")
    	#table= r'C:\Users\rieffel\Dropbox\RPC\00_Entwicklungsumgebung\3 Benutzerdefinierte Projekte\Duesseldorf\FGDB_36_Flaeche_und_Oekologie_Duesseldorf.gdb\temp'
    	#Temp-Tabelle leeren
    	arcpy.DeleteRows_management(table)
    	#Daten in die  Temp Tabelle schreiben
    	temp = arcpy.InsertCursor(table)
    	row = temp.newRow()
    	row.Name = projektname
    	row.Wohnflaechendichte_in_qm = projektWohnflaechenDichte
    	temp.insertRow(row)
    	row = temp.newRow()
    	row.Name = kreisName
    	row.Wohnflaechendichte_in_qm = kreisWohnflaechendichte
    	temp.insertRow(row)
    	row = temp.newRow()
    	#Bezeichung des Kreistyps aus der RaumTypen Tabelle extrahieren
    	#table = workspace_basis + "RaumTypen"
    	table2 = join(workspace_oekologie, "RaumTypen")
    	sql = ("ID = " + str(kreistyp))
    	cursor4 = arcpy.SearchCursor(table2, sql)
    	for row1 in cursor4:
    		typName = row1.Name
    	row.Name = typName
    	row.Wohnflaechendichte_in_qm = kreistypWohnflaechendichte
    	temp.insertRow(row)
    	#Diagramm erstellen
        input_template  = self.folders.get_diagram_template('Wohndichte')
    	graph = arcpy.MakeGraph_management(input_template, table, "Diagramm")
    	output = join(path_project, "Ergebnisausgabe", "Abbildungen", "Bewertung_Wohnflaechendichte.png")
    	arcpy.SaveGraph_management(graph, output, image_width=800, image_height=600)
        self.output.add_graph(input_template, graph, "Bewertung_Wohnflaechendichte")
    	#Image.open(output).show()


    	del cursor,cursor2,cursor3, cursor4, table1,kreise, ergebnisse, table, temp, row1, table2
    	gc.collect()
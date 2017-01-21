# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# Ergebnisausgabe.py
#
# Description: Export fact sheet for every RPC project
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# HCU Hamburg
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


import os
import sys
import datetime

import arcpy
import xlsxwriter

######## 1. Einrichten: Pfade setzen, Excel-Arbeitsmappe erstellen, Styles anlegen etc. ########

# Pfade setzen
base_path = str(sys.path[0]).split("2_Tool")[0]
workspace_factsheet = join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt.gdb')
tablepath_vor = join(workspace_factsheet,'Vornutzungen_Details_Prozent')
tablepath_teil = join(workspace_factsheet,'Teilflaechen_Plangebiet')
tablepath_neu  = join(workspace_factsheet,'Flaechenbilanz_Planung_gruppiert')
tablepath_name = join(workspace_factsheet,'Projektrahmendaten')
tablepath_zeit = join(workspace_factsheet,'Gebaeude_Details')
tablepath_WE = join(workspace_factsheet,'Wohneinheiten_Details')
tablepath_Gewerbe = join(workspace_factsheet,'Gewerbe_Beschaeftigte_Max')
tablepath_EZH = join(workspace_factsheet,'Versorgung_Verkaufsflaechen_Max')
logo = join((str(sys.path[0]).split("2_Tool")[0]),"1_Basisdaten","logo_rpc.png")
ausgabeordner = join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Excel')
excelpfad = join(ausgabeordner,'11_Definition_Projekt.xlsx')

try:
    os.remove(excelpfad)
except:
    pass

# Workbook und Tabellenblätter anlegen
wb = xlsxwriter.Workbook(excelpfad)
ws1 = wb.add_worksheet('Übersicht'.decode('utf-8'))

#Spaltenbreiten anpassen
ws1.set_column(0, 0, 8)
ws1.set_column(1, 1, 26)
ws1.set_column(8, 8, 4)

# Styles anlegen
head = wb.add_format({'bold': True, 'font_size': '24', 'align': 'left','valign': 'vcenter', 'bg_color': 'white', 'border': '0'})
normal = wb.add_format({'font_size': '14', 'bg_color': 'white', 'border': '0'})
rechts = wb.add_format({'font_size': '14', 'align' : 'right', 'bg_color': 'white', 'border': '0'})
bold = wb.add_format({'bold': True, 'font_size': '14', 'bg_color': 'white', 'border': '0'})
percent = wb.add_format({'num_format': '0.0%', 'bg_color': 'white', 'border': '0'})
background = wb.add_format({'bg_color': 'white', 'border': '0'})

# Hintergrund weiß färben
for x in range(0,50):
    for y in range(0,50):
        ws1.write(x,y,"", background)

# Uhrzeit des Datenzugriffs festhalten
now = datetime.datetime.now()



######## 2. Daten aus bestehenden Tabellen einlesen und in neue Kategorien umbrechen ########

# Angelegte Teilflächen einlesen
teilgebiete = dict()
rows = arcpy.SearchCursor(tablepath_teil)
for row in rows:
    name = row.getValue("Name")
    flaeche = row.getValue("Flaeche_ha")
    teilgebiete[name] = flaeche
gesamtflaeche_vor = sum([i for i in teilgebiete.values()])
del rows

# Flächenbilanz der Vornutzungen ermitteln, für Balkendiagramm auf neue Kategorien umlegen
rows = arcpy.SearchCursor(tablepath_vor)
land_vor, brach_vor, laerm_vor, gewerbe_vor, erschlie_vor, sozial_vor, ezh_vor, wohnen_vor, gruen_vor, natur_vor, sonstige_vor = 0,0,0,0,0,0,0,0,0,0,0
for row in rows:
	typ = row.getValue("Vornutzungstyp")
	wert = row.getValue("Prozent_der_Flaeche")
	teil = row.getValue("Teilflaeche_Plangebiet")
	multi = teilgebiete[teil] / gesamtflaeche_vor
	if typ == 'Landwirtschaftlicher Betrieb' or typ == 'Ackerflaeche': land_vor = land_vor + (wert / 100 * multi)
	if typ == 'Brachflaeche': brach_vor = brach_vor + (wert / 100 * multi)
	if typ == 'Laermintensives Gewerbe' or typ == 'Normales Gewerbe' or typ == 'Wenig stoerendes Gewerbe': gewerbe_vor = gewerbe_vor + (wert / 100 * multi)
	if typ == 'Soziale Infrastuktur': sozial_vor = sozial_vor + (wert / 100 * multi)
	if typ == 'Einzelhandel': ezh_vor = ezh_vor + (wert / 100 * multi)
	if typ == 'Wohnen': wohnen_vor = wohnen_vor + (wert / 100 * multi)
	if typ == 'Oeffentliche Gruenflaeche': gruen_vor = gruen_vor + (wert / 100 * multi)
	if typ == 'Wald' or typ == 'Wiese': natur_vor = natur_vor + (wert / 100 * multi)
del rows

# Flächenbilanz der neuen Nutzung ermitteln, für Balkendiagramm auf neue Kategorien umlegen
rows = arcpy.SearchCursor(tablepath_neu)
land_neu, brach_neu, laerm_neu, gewerbe_neu, erschlie_neu, sozial_neu, ezh_neu, wohnen_neu, gruen_neu, natur_neu, sonstige_neu = 0,0,0,0,0,0,0,0,0,0,0

gesamtflaeche_neu = 0
for row in rows:
    gesamtflaeche_neu = gesamtflaeche_neu + row.getValue("Flaeche_ha")
del rows

rows = arcpy.SearchCursor(tablepath_neu)
for row in rows:
	typ = row.getValue("Flaechennutzung_S2")
	wert = row.getValue("Flaeche_ha")
	anteil = wert / gesamtflaeche_neu
	if typ == 'Gewerbeflaeche (Industrie)': gewerbe_neu = gewerbe_neu + anteil
	if typ == 'Laermschutzanlagen': laerm_neu = laerm_neu + anteil
	if typ == 'Oeffentlich - Innere Erschliessung' or typ == 'Oeffentlich - Aeussere Erschliessung' or typ == 'Privat - Innere Erschliessung': erschlie_neu = erschlie_neu + anteil
	if typ == 'Gemeinbedarfsflaeche' or typ == 'Spielplaetze': sozial_neu = sozial_neu + anteil
	if typ == 'Gewerbeflaeche (Versorgung)': ezh_neu = ezh_neu + anteil
	if typ == 'Nettowohnbauland': wohnen_neu = wohnen_neu + anteil
	if typ == 'Allgemeine Gruenflaechen' or typ == 'Strassenbegleitgruen': gruen_neu = gruen_neu + anteil
	if typ == 'Ausgleichs- und Ersatzflaechen': natur_neu = natur_neu + anteil
	if typ == 'Sonstige Flaechen': sonstige_neu = sonstige_neu + anteil
del rows

# Gemeindename einesen
rows = arcpy.SearchCursor(tablepath_name)
for row in rows:
    stadt = row.getValue("Gemeindename")
del rows

# Realisierungszeitraum einlesen
rows = arcpy.SearchCursor(tablepath_zeit)
Jahre = []
for row in rows:
    Jahr = row.getValue("Jahr")
    Jahre.append(Jahr)
start = str(min(Jahre))
end = str(max(Jahre))
del rows

# Zahl der Wohneinheiten einlesen
rows = arcpy.SearchCursor(tablepath_WE)
WE = 0
for row in rows:
    WE_teil = row.getValue("Anzahl_WE")
    WE = WE + WE_teil
del rows

# Zahl der Beschäftigen einlesen
rows = arcpy.SearchCursor(tablepath_Gewerbe)
Gewerbe = 0
for row in rows:
    Gewerbe_teil = row.getValue("Max")
    Gewerbe = Gewerbe + Gewerbe_teil
del rows
Gewerbe = 'ca. ' + "%.0f" % Gewerbe

# Verkaufsfläche einlesen
rows = arcpy.SearchCursor(tablepath_EZH)
EZH = 0
for row in rows:
    EZH_teil = row.getValue("Max")
    EZH = EZH + EZH_teil
del rows



######## 3. Textfelder in Datenblatt schreiben ########

#Rohdaten in Tabellenblatt schreiben
ws1.merge_range('C2:J4', projektname + ' in ' + stadt + '', head) #verbundene Zellen für die Überschrift
ws1.write(6, 1, 'REGIOPROJEKTCHECK', bold)
ws1.write(7, 1, 'Folgeabschätzung von Bauprojekten'.decode('utf-8'), normal)
ws1.write(8, 1, 'Exportdatum', normal)
ws1.write(8, 8, now.strftime("%Y-%m-%d %H:%M"), rechts)
ws1.write(11, 1, 'RAHMENDATEN', bold)
ws1.write(12, 1, 'Fläche des Plangebiets'.decode('utf-8'), normal)
ws1.write(12, 7, gesamtflaeche_vor, rechts)
ws1.write(12, 8, 'ha', rechts)
ws1.write(13, 1, 'Realisierungszeitraum', normal)
ws1.write(13, 8, start + ' - ' + end, rechts)
ws1.write(15, 1, 'Wohnnutzung (Wohneinheiten)', normal)
ws1.write(15, 7, WE, rechts)
ws1.write(15, 8, 'WE', rechts)
ws1.write(16, 1, 'Gewerbe (Arbeitsplätze)'.decode('utf-8'), normal)
ws1.write(16, 8, Gewerbe, rechts)
ws1.write(17, 1, 'Einzelhandel (Verkaufsfläche)'.decode('utf-8'), normal)
ws1.write(17, 7, EZH, rechts)
ws1.write(17, 8, 'm²'.decode('utf-8'), rechts)



######## 4. Daten für Flächenbilanz in temporäres Arbeitsblatt schreiben (Notwendig für die Diagrammerstellung) ########

data_neu = [land_neu, brach_neu, laerm_neu, gewerbe_neu, erschlie_neu, sozial_neu, ezh_neu, wohnen_neu, gruen_neu, natur_neu, sonstige_neu]
data_vor = [land_vor, brach_vor, laerm_vor, gewerbe_vor, erschlie_vor, sozial_vor, ezh_vor, wohnen_vor, gruen_vor, natur_vor, sonstige_vor]
category_names = ['Landwirtschaft', 'Brachfläche'.decode('utf-8'), 'Lärmschutzanlage'.decode('utf-8'), 'Gewerbe', 'Erschließung'.decode('utf-8'), 'Soziale Infrastruktur', 'Einzelhandel', 'Wohnen', 'Grünflaeche'.decode('utf-8'), 'Natur', 'Sonstige']
category_colors = ['#73583d', '#7f7f7f', '#595959', '#c4bd97', '#ffc000', '#e46c0a', '#b3a2c7', '#953735', '#c3d69b', '#4f6228', '#f2f2f2']

ws2 = wb.add_worksheet('raw_data')
ws2.write(0,2,'Vornutzung')
ws2.write(0,1,'Neue Nutzung')
ws2.write_column('A2', category_names)
for n,i in enumerate(data_vor): # nur Werte >0 in die Tabelle schreiben um Labels mit 0,0% zu vermeiden
	if i > 0:
		ws2.write(n+1,2,data_vor[n], percent)
for n,i in enumerate(data_neu):
	if i > 0:
		ws2.write(n+1,1,data_neu[n], percent)



######## 5. Diagramm Flächenbilanz erstellen ########

# Chartobjekt erstellen, Diagramm formatieren
chart = wb.add_chart({'type': 'bar', 'subtype': 'percent_stacked'})
chart.set_size({'width': 1170, 'height': 300})
chart.set_chartarea({'border': {'none': True}})
chart.set_title({
	'name': 'FLÄCHENBILANZ'.decode('utf-8'),
	'name_font': {
		'size': 14
	},
	'layout': {
		'x': 0.003,
		'y': 0.05,
	}
})

chart.set_x_axis({
	'num_font': {
		'color': '#7f7f7f',
	},
	'major_gridlines': {
		'visible': True,
		'line': {
			'width': 0.75,
			'dash_type': 'dash',
			'color': '#bfbfbf',
		}
	}
})

chart.set_y_axis({
	'num_font': {
		'color': '#7f7f7f',
	}
})

chart.set_legend({'position': 'bottom'})

# Datenbezüge definieren
for i in range(0, 10):
	chart.add_series({
		'name':         '=raw_data!$A$'+str(i+2)+'',
		'categories':   '=raw_data!$B$1:$C$1',
		'values':       '=raw_data!$B$'+str(i+2)+':$C$'+str(i+2)+'',
		'fill': 		{'color': ''+category_colors[i]+''},
		'num_font':     {'color': 'white'},
		'data_labels': 	{'value':  True},
		'gap':        40,
	})
ws1.insert_chart('B21', chart)

# Datenblatt mit Rohdaten ausblenden
ws2.hide()



######## 6. Miniaturkarte und Logo einfügen ########

# Karte in Excelmappe einfuegen
minimap = join(join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Abbildungen', '11_Minimap.jpg'))
ws1.insert_image('L5', minimap, {'x_scale': 0.29, 'y_scale': 0.25}) #Korrigiert Verzerrung die bei 1x1 auftritt
ws1.write(3, 11, 'ÜBERSICHTSKARTE'.decode('utf-8'), bold)

# Logo einfuegen
ws1.insert_image('B2', logo, {'x_scale': 1, 'y_scale': 0.93}) #Korrigiert Verzerrung die bei 1x1 auftritt



###### 7. Aufräumen, abschließen ######

# Workbook speichern, Fehler bei bereits geöffnetem Excel-Workbook abfangen
try:
	wb.close()
except IOError:
	schrittmeldung = 'Die Ergebnisstabelle konnte nicht gespreichert werden, da eine ältere Version der Datei momentan in Excel geöffnet ist. Bitte schließen Sie diese Tabelle und führen Sie den Arbeitsschritt erneut aus. \n'
	arcpy.AddMessage(schrittmeldung)
	print schrittmeldung

# Endmeldung
schrittmeldung = 'Script abgeschlossen'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

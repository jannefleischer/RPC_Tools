# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 01_Mengenermittlung.py
#
# Description:
#
#Author:
#Achim Tack / Gertz Gutsche Rümenapp
# ---------------------------------------------------------------------------

#############################################################################################################
# Import arcpy modules
import arcpy, os, inspect, pyodbc, shutil, gc, sys, datetime,xlsxwriter, codecs
from xlsxwriter.utility import xl_rowcol_to_cell
import bevoelkerung_lib as b
gc.collect()

arcpy.env.overwriteOutput = True

# Variablen definieren
projektname = 'LKH_Bultweg' # haendische Ueberbrueckung bei manueller Scriptnutzung

#Pfade einrichten
base_path = str(sys.path[0]).split("2_Tool")[0]

workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
workspace_projekt_bevoelkerung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_22_BevModellierung_'+projektname+'.gdb')
workspace_tool_bevoelkerung = os.path.join(base_path,"2_Tool","22_Bevoelkerungsmodellierung","FGDB_22_Bevoelkerungsmodellierung_Tool.gdb")

input_table = os.path.join(workspace_projekt_bevoelkerung,'T02RECH_Input')

#############################################################################################################
# Schritt 6 - Datenexport in Excel-Datei
schrittmeldung = 'Datenexport in Excel-Datei  \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

# Pfade setzen
tablepath = os.path.join(workspace_projekt_bevoelkerung,'T03ERG_Bevoelkerung_Projekt')

logo = os.path.join((str(sys.path[0]).split("2_Tool")[0]),"1_Basisdaten","logo_rpc.png")
ausgabeordner = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Excel')
excelpfad = os.path.join(ausgabeordner,'22_Bevoelkerungsmodellierung_Baugebiet.xlsx')

try:
    os.remove(excelpfad)
except:
    pass

# Workbook und Tabellenblätter anlegen
wb = xlsxwriter.Workbook(excelpfad)
ws1 = wb.add_worksheet('Info')
ws2 = wb.add_worksheet('Rohdaten')
ws3 = wb.add_worksheet('Auswertungen')
ws4 = wb.add_worksheet('Grafiken')

#Charts anlegen
chart_bevoelkerung_altersgruppen = wb.add_chart({'type': 'area', 'subtype': 'stacked'})
chart_bevoelkerung_altersgruppen.set_style(40)
chart_bevoelkerung_altersgruppen.set_size({'width': 800, 'height': 600})
chart_bevoelkerung_altersgruppen.set_chartarea({'border': {'none': True},'fill': {'none': True}})
chart_bevoelkerung_altersgruppen.set_legend({'position': 'bottom'})
chart_bevoelkerung_altersgruppen.set_title({'name': 'Bevoelkerungsentwicklung nach Altersgruppen','name_font':  {'name': 'Tahoma', 'size': 9}})

#Styles anlegen
bold = wb.add_format({'bold': True})

#Feldnamen auslesen
fieldnames = [f.name for f in arcpy.ListFields(tablepath)]

################################
#Werteblatt einfuegen

#Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
rows = arcpy.SearchCursor(tablepath)
j = 1
for row in rows:
    i = 0
    for fieldname in fieldnames:
        wert = row.getValue(fieldname)
        ws2.write(j, i, wert)
        i = i+1

    j = j+1

#Felder als Header in Worksheet einfuegen
i = 0
for fieldname in fieldnames:
    column_with = len(fieldname)+2
    ws2.set_column(i, i, column_with)
    ws2.write(0, i, fieldname, bold)
    i = i+1

################################
#Auswertungsblatt einfuegen

#Jahre auslesen
rows = arcpy.SearchCursor(tablepath)
Jahre = []
for row in rows:
    Jahr = row.Jahr
    Jahre.append(Jahr)
Jahre = list(set(Jahre))
Jahre.sort()
del rows, row

#Jahre in Excel eintragen
i = 2
j = 2
for Jahr in Jahre:
    ws3.write(i, j, Jahr, bold) #jaehrliche Darstellung
    j = j+1

#Altersgruppen in Excel eintragen
altersgruppen =["0-5 Jahre","6-10 Jahre","11-18 Jahre","19-25 Jahre","26-45 Jahre","46-65 Jahre","66-75 Jahre","75-100 Jahre"]

i = 3
j = 1
for altersgruppe in altersgruppen:
    ws3.write(i, j, altersgruppe, bold)
    i = i+1

#Werte in Excel eintragen (Summewenns-Formel)
i = 2
for altersgruppe in altersgruppen:
    gruppe_untergrenze = altersgruppe.split("-")[0]
    gruppe_obergrenze = altersgruppe.split("-")[1].split(" ")[0]

    j = 2
    i = i+1
    k = 0
    for Jahr in Jahre:
        j = j+1
        k = k+1
        jahresvariable = xl_rowcol_to_cell(2, j-1)
        formulastring1 = '=SUMIFS(Rohdaten!$F:$F,Rohdaten!$C:$C,'+jahresvariable+',Rohdaten!$D:$D,">'+gruppe_untergrenze+'",Rohdaten!$D:$D,"<'+gruppe_obergrenze+'")'
        ws3.write_formula(i, j-1, formulastring1)

    # Werte in Chartobjekte schreiben
    chart_bevoelkerung_altersgruppen.add_series({
        'name':       altersgruppe,
        'categories': ['Auswertungen', 2, 2, 2,j-1],
        'values':     ['Auswertungen', 2+i, 2, 2+i,j-1],
    })

# Ueberschriften einfuegen

# Erste Leerspalte anpassen
ws2.set_column(0, 0, 3)

# Ueberschriften einfuegen
ws3.write(0, 1, 'Bevoelkerungsentwicklung', bold)
ws3.write(1, 1, 'nach Altersgruppen')

#Spaltenbreiten anpassen
ws3.set_column(1, 1, 25)

################################
#Beschreibungsblatt einfuegen
now = datetime.datetime.now()

Beschreibungstext = """Bevoelkerungsstruktur im Zeitverlauf fuer das Untersuchungsgebiet. Sie finden die Werte im naechsten Tabellenblatt"""

ws1.write(6, 1, 'REGIOPROJEKTCHECK', bold)
ws1.write(7, 1, 'Folgeabschaetzung von Bauprojekten')

ws1.write(9, 1, 'Untersuchtes Projekt:', bold)
ws1.write(9, 2, projektname)
ws1.write(10, 1, 'Wirkungsfeld:', bold)
ws1.write(10, 2, 'Baugebietsinterne Bevoelkerungsmodellierung')
ws1.write(11, 1, 'Exportdatum:', bold)
ws1.write(11, 2, now.strftime("%Y-%m-%d %H:%M"))

ws1.write(13, 1, 'Inhalt:', bold)
ws1.write(13, 2, Beschreibungstext)

#Logo einfuegen
ws1.insert_image('A2', logo)

#Spaltenbreiten anpassen
ws1.set_column(0, 0, 3)
ws1.set_column(1, 1, 35)

################################
#Grafikblatt einfuegen
ws4.insert_chart('B2', chart_bevoelkerung_altersgruppen)


#Workbook speichern
wb.close()

gc.collect()
print "fertig"
arcpy.AddMessage('Baugebietsinterne Bevoelkerungsmodellierung abgeschlossen')
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

#Altersjahre in Excel eintragen

i = 3
j = 1
for altersjahr in range(0,99):
    ws3.write(i, j, altersjahr, bold)
    i = i+1

#Werte in Excel eintragen (Summewenns-Formel)
i = 2
for alter in range(0,99):

    j = 2
    i = i+1
    k = 0
    for Jahr in Jahre:
        j = j+1
        k = k+1
        jahresvariable = xl_rowcol_to_cell(2, j-1)
        altersvariable = xl_rowcol_to_cell(3+alter, 1)
        formulastring1 = '=SUMIFS(Rohdaten!$F:$F,Rohdaten!$C:$C,Auswertungen!'+jahresvariable+',Rohdaten!$D:$D,Auswertungen!'+altersvariable+')'
        #formulastring1 = '=SUM('+jahresvariable+','+altersvariable+')'
        print formulastring1
        ws3.write_formula(i, j-1, formulastring1)

# Ueberschriften einfuegen

# Erste Leerspalte anpassen
ws2.set_column(0, 0, 3)

# Ueberschriften einfuegen
ws3.write(0, 1, 'Bevoelkerungsentwicklung', bold)
ws3.write(1, 1, 'nach Altersjahren')

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


#Workbook speichern
wb.close()

gc.collect()
print "fertig"
arcpy.AddMessage('Baugebietsinterne Bevoelkerungsmodellierung abgeschlossen')
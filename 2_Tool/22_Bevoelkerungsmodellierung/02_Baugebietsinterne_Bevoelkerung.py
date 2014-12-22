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
import arcpy, os, inspect, pyodbc, shutil, gc, sys, datetime, xlsxwriter, imp
from xlsxwriter.utility import xl_rowcol_to_cell

sheetlibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '11_Definition_Projekt','sheet_lib.py'))
sl = imp.load_source('sheet_lib', sheetlibpath)

mdblibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '11_Definition_Projekt','tempmdb_lib.py'))
mdb = imp.load_source('tempmdb_lib', mdblibpath)

gc.collect()

arcpy.env.overwriteOutput = True

# Variablen definieren
projektname = arcpy.GetParameterAsText(0)

#Pfade einrichten
base_path = str(sys.path[0]).split("2_Tool")[0]

workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
workspace_projekt_bevoelkerung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_22_BevModellierung_'+projektname+'.gdb')
workspace_tool_bevoelkerung = os.path.join(base_path,"2_Tool","22_Bevoelkerungsmodellierung","FGDB_22_Bevoelkerungsmodellierung_Tool.gdb")

input_table = os.path.join(workspace_projekt_bevoelkerung,'T02RECH_Input')

#############################################################################################################
#
# Durchlauf Baugebietsinterne Bevoelkerungsmodellierung
#
#############################################################################################################
beginmeldung = 'Starte Bevoelkerungsmodellierung \n'
arcpy.AddMessage(beginmeldung)
print beginmeldung
#############################################################################################################
# Schritt 1 - Erzeuge Eingangsdaten aus Gebaeude und Wohnungsinformationen
schrittmeldung = 'Erzeuge Eingangsdaten aus Gebaeude und Wohnungsinformationen \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

wohneinheiten_tabelle = os.path.join(workspace_projekt_definition,"Wohneinheiten_Details")

wohneinheiten = []

rows = arcpy.SearchCursor(wohneinheiten_tabelle)

for row in rows:
    Teilflaeche_Plangebiet = row.Teilflaeche_Plangebiet
    Jahr = row.Jahr
    Gebaeudetyp = row.Gebaeudetyp
    Miete_Eigentum = row.Miete_Eigentum
    Anzahl_WE = row.Anzahl_WE

    #Gebaeudetyp wird in die Grobtypen "individuell' und 'geschoss' vereinfacht
    Gebaeudetyp = Gebaeudetyp.replace('Einfamilienhaus','Individuell').replace('Zweifamilien- oder Doppelhaus','Individuell').replace('Reihenhaus','Individuell')
    Gebaeudetyp = Gebaeudetyp.replace('Mehrfamilienhaus mit Gewerbeeinheiten','Geschoss').replace('Mehrfamilienhaus','Geschoss')

    werte = (Teilflaeche_Plangebiet,Jahr,Gebaeudetyp,Miete_Eigentum,Anzahl_WE)
    print werte
    wohneinheiten.append(werte)

wohneinheiten_bev = []

betrachtungszeitraum_tabelle = os.path.join(workspace_projekt_definition,"Projektrahmendaten")

rows = arcpy.SearchCursor(betrachtungszeitraum_tabelle)
for row in rows:
    betrachtungszeitraum_min = row.Beginn_Betrachtungszeitraum
    betrachtungszeitraum_max = row.Ende_Betrachtungszeitraum

print betrachtungszeitraum_min, betrachtungszeitraum_max

for i in range(betrachtungszeitraum_min,betrachtungszeitraum_max): #betrachtungszeitraum

    for row in wohneinheiten:

        try:

            Teilflaeche_Plangebiet = row[0]
            Jahr = i
            Miete_Eigentum = row[3]
            Bebauungsart = row[2]
            Alter_WE = i - int(row[1])
            Anzahl_WE = int(row[4])

            if Alter_WE >=0:
                Alter_WE = Alter_WE + 1
                werte = (Teilflaeche_Plangebiet,Jahr,Miete_Eigentum,Bebauungsart,Alter_WE,Anzahl_WE)
                wohneinheiten_bev.append(werte)
            else:
                pass

        except:
            pass


#############################################################################################################
# Schritt 2 - Kopiere Eingangsdaten in FGDB_22_BevModellierung
schrittmeldung = 'Kopiere Eingangsdaten in FGDB_22_BevModellierung \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

template = os.path.join(workspace_tool_bevoelkerung,'T02DEF_Template_Input')
arcpy.CreateTable_management(workspace_projekt_bevoelkerung, 'T02RECH_Input', template, '')

rows = arcpy.InsertCursor(input_table)

for e in wohneinheiten_bev:

    row = rows.newRow()
    row.setValue("Teilflaeche_Plangebiet", e[0])
    row.setValue("Jahr", e[1])
    row.setValue("Miete_Eigentum", e[2])
    row.setValue("Bebauungsart", e[3])
    row.setValue("Alter_WE", e[4])
    row.setValue("Anzahl_WE", e[5])
    rows.insertRow(row)


#############################################################################################################
# Schritt 3 - Erzeuge Baugebietsbevoelkerung
schrittmeldung = 'Erzeuge Baugebietsbevoelkerung \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

eingangstabellen = [
    (workspace_tool_bevoelkerung,'T01DEF_Kennwerte'),
    (workspace_projekt_bevoelkerung,'T02RECH_Input')
]

ausgabetabelle = (workspace_projekt_bevoelkerung,'T03ERG_Bevoelkerung_Projekt')

sql = """SELECT T02RECH_Input.Teilflaeche_Plangebiet, T02RECH_Input.Jahr, T01DEF_Kennwerte.AlterEW, T01DEF_Kennwerte.Geschlecht, Sum(T01DEF_Kennwerte.Personenanzahl*T02RECH_Input.Anzahl_WE) AS Bewohner INTO T03ERG_Bevoelkerung_Projekt
FROM T01DEF_Kennwerte INNER JOIN T02RECH_Input ON (T01DEF_Kennwerte.AlterWE = T02RECH_Input.Alter_WE) AND (T01DEF_Kennwerte.Bebauungsart = T02RECH_Input.Bebauungsart) AND (T01DEF_Kennwerte.Miete_Eigentum = T02RECH_Input.Miete_Eigentum)
GROUP BY T02RECH_Input.Teilflaeche_Plangebiet, T02RECH_Input.Jahr, T01DEF_Kennwerte.AlterEW, T01DEF_Kennwerte.Geschlecht;
"""

mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)


#############################################################################################################
#Aufraeumen und ueberfluessige Variablen loeschen
schrittmeldung = 'Aufraeumen und ueberfluessige Variablen loeschen \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

deletelist = [input_table]

for element in deletelist:
    try:
        e = str(element)
        arcpy.Delete_management(e)
    except:
        print element, "konnte nicht geloescht werden"

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
sl.infosheet(projektname, str("Bevoelkerungsmodellierung Projekt").decode('utf-8'), wb)
ws5 = wb.add_worksheet('Methodik')
ws3 = wb.add_worksheet('Auswertungen')
ws4 = wb.add_worksheet('Grafiken')
ws2 = wb.add_worksheet('Rohdaten')

#Charts anlegen
chart_bevoelkerung_altersgruppen = wb.add_chart({'type': 'area', 'subtype': 'stacked'})
chart_bevoelkerung_altersgruppen.set_style(40)
chart_bevoelkerung_altersgruppen.set_size({'width': 800, 'height': 600})
chart_bevoelkerung_altersgruppen.set_chartarea({'border': {'none': True},'fill': {'none': True}})
chart_bevoelkerung_altersgruppen.set_legend({'position': 'bottom'})
chart_bevoelkerung_altersgruppen.set_title({'name': 'Bevoelkerungsentwicklung nach Altersgruppen','name_font':  {'name': 'Tahoma', 'size': 9}})

#Styles anlegen
bold = wb.add_format({'bold': True})
bold.set_align('vtop')
bold.set_bg_color('white')
bold.set_border(0)

wrap = wb.add_format()
wrap.set_text_wrap()
wrap.set_align('vtop')
wrap.set_bg_color('white')
wrap.set_border(0)

normal = wb.add_format()
normal.set_bg_color('white')
normal.set_border(0)

#Hintergrund weiss faerben
format = wb.add_format()
format.set_bg_color('white')
format.set_border(0)

for x in range(0,400):
    for y in range(0,400):
        ws2.write(x,y,"", format)
        ws3.write(x,y,"", format)
        ws4.write(x,y,"", format)
        ws5.write(x,y,"", format)

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
        ws2.write(j, i, wert,normal)
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
        formulastring1 = '=SUMIFS(Rohdaten!$F:$F,Rohdaten!$C:$C,'+jahresvariable+',Rohdaten!$D:$D,">='+gruppe_untergrenze+'",Rohdaten!$D:$D,"<='+gruppe_obergrenze+'")'
        ws3.write_formula(i, j-1, formulastring1,normal)

    # Werte in Chartobjekte schreiben
    chart_bevoelkerung_altersgruppen.add_series({
        'name':       altersgruppe,
        'categories': ['Auswertungen', 2, 2, 2,j-1],
        'values':     ['Auswertungen', i, 2, i,j-1],
    })

# Erste Leerspalte anpassen
ws2.set_column(0, 0, 3)

# Ueberschriften einfuegen
ws3.write(0, 1, 'Bevoelkerungsentwicklung', bold)
ws3.write(1, 1, 'nach Altersgruppen',normal)

#Spaltenbreiten anpassen
ws3.set_column(1, 1, 25)

################################
#Grafikblatt einfuegen
ws4.insert_chart('B2', chart_bevoelkerung_altersgruppen)

################################
#Methodikblatt einfuegen
methodik_grafik = os.path.join(base_path,"2_Tool","22_Bevoelkerungsmodellierung","Erlaeuterungstexte","22_Modellierung_Baugebietsbevoelkerung.png")
ws5.insert_image('B2', methodik_grafik, {'x_scale': 0.32, 'y_scale': 0.32}) #Korrigiert Verzerrung die bei 1x1 auftritt

################################
#Workbook speichern
try:
    wb.close()
except:
    arcpy.AddMessage("Es liegt ein Fehler beim Speichern der Ausgabedatei vor. Ist diese ggf. noch geoeffnet?")

gc.collect()
print "fertig"
arcpy.AddMessage('Baugebietsinterne Bevoelkerungsmodellierung abgeschlossen')
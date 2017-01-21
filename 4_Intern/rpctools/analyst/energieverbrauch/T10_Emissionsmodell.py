# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 10_Emissionsmodell.py
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
import gc
import sys
import imp
import arcpy
import xlsxwriter

def main(parameters, messages):

    sheetlibpath = os.path.abspath(join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','sheet_lib.py'))
    sheetlibpath = os.path.abspath(join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','sheet_lib.py'))
    sl = imp.load_source('sheet_lib', sheetlibpath)

    mdblibpath = os.path.abspath(join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','tempmdb_lib.py'))
    mdb = imp.load_source('tempmdb_lib', mdblibpath)

    poplibpath = os.path.abspath(join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','population_lib.py'))
    pop = imp.load_source('population_lib', poplibpath)

    gc.collect()

    arcpy.env.overwriteOutput = True

    # Variablen definieren
    projektname = parameters[0].valueAsText
    #projektname = 'LKH_Bultweg' # haendische Ueberbrueckung bei manueller Scriptnutzung

    #Pfade einrichten
    base_path = str(sys.path[0]).split("2_Tool")[0]

    workspace_projekt_definition = join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt.gdb')
    workspace_projekt_emissionen = join(base_path,'3_Projekte',projektname,'FGDB_Energie_und_Emissionen.gdb')
    workspace_tool_emissionen = join(base_path,"2_Tool","E_Energieverbrauch","FGDB_Energieverbrauch_Tool.gdb")

    #############################################################################################################
    #
    # Durchlauf Mengenermittlung
    #
    #############################################################################################################
    beginmeldung = 'Starte Emissionsmodell \n'
    messages.AddMessage(beginmeldung)
    print beginmeldung

    #############################################################################################################
    # Schritt 1: Einwohnerzahl erzeugen
    pop.recalcPopulation(projektname)

    #############################################################################################################
    # Schritt 2 - Aggregiere Gebaeudedaten - Wohnen
    schrittmeldung = 'Aggregiere Gebaeudedaten - Wohnen \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung

    eingangstabellen = [
        (workspace_projekt_definition,'Wohneinheiten_Details')
    ]

    ausgabetabelle = (workspace_projekt_emissionen,'T02RECH_01_Wohnen_Flaechen')

    sql = """SELECT Wohneinheiten_Details.Teilflaeche_Plangebiet, Max(Wohneinheiten_Details.Jahr) AS Jahr, Wohneinheiten_Details.Gebaeudetyp, Sum([Wohnflaeche_qm]*[Anzahl_WE]) AS Flaeche INTO T02RECH_01_Wohnen_Flaechen
            FROM Wohneinheiten_Details
            GROUP BY Wohneinheiten_Details.Teilflaeche_Plangebiet, Wohneinheiten_Details.Gebaeudetyp
            ORDER BY Wohneinheiten_Details.Teilflaeche_Plangebiet, Max(Wohneinheiten_Details.Jahr), Wohneinheiten_Details.Gebaeudetyp;
            """

    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    #############################################################################################################
    # Schritt 3 - Berechne CO2-Emissionen Bevoelkerung Stromverbrauch
    schrittmeldung = 'Berechne CO2-Emissionen Bevoelkerung Stromverbrauch \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung

    eingangstabellen = [
        (workspace_projekt_definition,'Einwohnerzahl'),
        (workspace_tool_emissionen,'T01DEF_02_Wohnen_Energie')
    ]

    ausgabetabelle = (workspace_projekt_emissionen,'T02RECH_02_Wohnen_Energie')

    sql = """SELECT Einwohnerzahl.Jahr, Sum([Einwohnerzahl]*[KG_CO2_Jahr])/1000 AS Emissionen_CO2_Jahr INTO T02RECH_02_Wohnen_Energie
            FROM Einwohnerzahl, T01DEF_02_Wohnen_Energie
            GROUP BY Einwohnerzahl.Jahr
            ORDER BY Einwohnerzahl.Jahr;
            """

    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    #############################################################################################################
    # Schritt 3 - Berechne CO2-Emissionen Bevoelkerung Heizenergie
    schrittmeldung = 'Berechne CO2-Emissionen Bevoelkerung Heizenergie \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung

    eingangstabellen = [
        (workspace_projekt_emissionen,'T02RECH_01_Wohnen_Flaechen'),
        (workspace_tool_emissionen,'T01DEF_01_Wohnen_Heizung')
    ]

    ausgabetabelle = (workspace_projekt_emissionen,'T02RECH_02_Wohnen_Heizung')

    sql = """SELECT T02RECH_01_Wohnen_Flaechen.Jahr, T02RECH_01_Wohnen_Flaechen.Teilflaeche_Plangebiet, T02RECH_01_Wohnen_Flaechen.Gebaeudetyp, Sum([Flaeche]*[KG_CO2_Jahr])/1000 AS Emissionen_CO2_Jahr INTO T02RECH_02_Wohnen_Heizung
            FROM T02RECH_01_Wohnen_Flaechen INNER JOIN T01DEF_01_Wohnen_Heizung ON T02RECH_01_Wohnen_Flaechen.Gebaeudetyp = T01DEF_01_Wohnen_Heizung.Gebaeudetyp
            GROUP BY T02RECH_01_Wohnen_Flaechen.Jahr, T02RECH_01_Wohnen_Flaechen.Teilflaeche_Plangebiet, T02RECH_01_Wohnen_Flaechen.Gebaeudetyp
            ORDER BY T02RECH_01_Wohnen_Flaechen.Jahr, T02RECH_01_Wohnen_Flaechen.Teilflaeche_Plangebiet, T02RECH_01_Wohnen_Flaechen.Gebaeudetyp;
            """

    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    #############################################################################################################
    # Schritt 4 - Berechne CO2-Emissionen Gewerbe
    schrittmeldung = 'Berechne CO2-Emissionen Gewerbe \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung

    eingangstabellen = [
        (workspace_projekt_definition,'Gewerbe_Beschaeftigte'),
        (workspace_tool_emissionen,'T01DEF_03_Gewerbe')
    ]

    ausgabetabelle = (workspace_projekt_emissionen,'T02RECH_03_Gewerbe_Ergebnis')

    sql = """SELECT Max(Gewerbe_Beschaeftigte.Jahr) AS Jahr, Gewerbe_Beschaeftigte.Teilflaeche_Plangebiet, Gewerbe_Beschaeftigte.Branche, [Anzahl]*[CO2_je_Beschaeftigtem] AS Emissionen_CO2_Jahr INTO T02RECH_03_Gewerbe_Ergebnis
            FROM Gewerbe_Beschaeftigte INNER JOIN T01DEF_03_Gewerbe ON Gewerbe_Beschaeftigte.Branche = T01DEF_03_Gewerbe.Wirtschaftsabschnitt
            GROUP BY Gewerbe_Beschaeftigte.Teilflaeche_Plangebiet, Gewerbe_Beschaeftigte.Branche, [Anzahl]*[CO2_je_Beschaeftigtem]
            ORDER BY Max(Gewerbe_Beschaeftigte.Jahr), Gewerbe_Beschaeftigte.Teilflaeche_Plangebiet, Gewerbe_Beschaeftigte.Branche;
            """

    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    #############################################################################################################
    # Schritt 5 - Berechne CO2-Emissionen Einzelhandel
    schrittmeldung = 'Berechne CO2-Emissionen Einzelhandel \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung

    eingangstabellen = [
        (workspace_projekt_definition,'Versorgung_Verkaufsflaechen')
    ]

    ausgabetabelle = (workspace_projekt_emissionen,'T02RECH_04_Versorgung_Ergebnis')

    sql = """SELECT Max(Versorgung_Verkaufsflaechen.Jahr) AS Jahr, Versorgung_Verkaufsflaechen.Teilflaeche_Plangebiet, Max([Verkaufsflaeche]*0.335) AS Emissionen_CO2_Jahr INTO T02RECH_04_Versorgung_Ergebnis
            FROM Versorgung_Verkaufsflaechen
            GROUP BY Versorgung_Verkaufsflaechen.Teilflaeche_Plangebiet;
            """

    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    #############################################################################################################
    # Schritt 6 - Datenexport in Excel-Datei
    schrittmeldung = 'Datenexport in Excel-Datei  \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung

    # Pfade setzen
    logo = join((str(sys.path[0]).split("2_Tool")[0]),"1_Basisdaten","logo_rpc.png")
    ausgabeordner = join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Excel')
    excelpfad = join(ausgabeordner,'Energieverbrauch.xlsx')

    try:
        os.remove(excelpfad)
    except:
        pass

    # Workbook und Tabellenblätter anlegen
    wb = xlsxwriter.Workbook(excelpfad)
    sl.infosheet(projektname, str("Emissionen").decode('utf-8'), wb)
    ws8 = wb.add_worksheet('Methodik')
    ws6 = wb.add_worksheet('Auswertungen')
    ws7 = wb.add_worksheet('Grafiken')
    ws2 = wb.add_worksheet('Rohdaten_Wohnen_Energie')
    ws3 = wb.add_worksheet('Rohdaten_Wohnen_Heizung')
    ws4 = wb.add_worksheet('Rohdaten_Gewerbe')
    ws5 = wb.add_worksheet('Rohdaten_Einzelhandel')
    ws9 = wb.add_worksheet('Haftungsausschluss')

    #Charts anlegen
    chart_co2_jahr = wb.add_chart({'type': 'column', 'subtype': 'stacked'})
    chart_co2_jahr.set_style(40)
    chart_co2_jahr.set_size({'width': 800, 'height': 600})
    chart_co2_jahr.set_chartarea({'border': {'none': True},'fill': {'none': True}})
    chart_co2_jahr.set_legend({'position': 'bottom'})
    chart_co2_jahr.set_title({'name': 'CO2 nach Themenfeld - jaehrlich','name_font':  {'name': 'Tahoma', 'size': 9}})

    #Styles anlegen
    bold = wb.add_format({'bold': True})
    bold.set_bg_color('white')
    bold.set_border(0)

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
            ws6.write(x,y,"", format)
            ws7.write(x,y,"", format)
            ws8.write(x,y,"", format)
            ws9.write(x,y,"", format)

    ################################
    #Werteblatt 1 einfuegen

    ausgabetabelle = join(workspace_projekt_emissionen,'T02RECH_02_Wohnen_Energie')

    #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
    rows = arcpy.SearchCursor(ausgabetabelle)
    fieldnames = [f.name for f in arcpy.ListFields(ausgabetabelle)]
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
    #Werteblatt 2 einfuegen

    ausgabetabelle = join(workspace_projekt_emissionen,'T02RECH_02_Wohnen_Heizung')

    #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
    rows = arcpy.SearchCursor(ausgabetabelle)
    fieldnames = [f.name for f in arcpy.ListFields(ausgabetabelle)]
    j = 1
    for row in rows:
        i = 0
        for fieldname in fieldnames:
            wert = row.getValue(fieldname)
            ws3.write(j, i, wert,normal)
            i = i+1

        j = j+1

    #Felder als Header in Worksheet einfuegen
    i = 0
    for fieldname in fieldnames:
        column_with = len(fieldname)+2
        ws3.set_column(i, i, column_with)
        ws3.write(0, i, fieldname, bold)
        i = i+1


    ################################
    #Werteblatt 4 einfuegen

    ausgabetabelle = join(workspace_projekt_emissionen,'T02RECH_03_Gewerbe_Ergebnis')

    #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
    rows = arcpy.SearchCursor(ausgabetabelle)
    fieldnames = [f.name for f in arcpy.ListFields(ausgabetabelle)]
    j = 1
    for row in rows:
        i = 0
        for fieldname in fieldnames:
            wert = row.getValue(fieldname)
            ws4.write(j, i, wert,normal)
            i = i+1

        j = j+1

    #Felder als Header in Worksheet einfuegen
    i = 0
    for fieldname in fieldnames:
        column_with = len(fieldname)+2
        ws4.set_column(i, i, column_with)
        ws4.write(0, i, fieldname, bold)
        i = i+1


    ################################
    #Werteblatt 5 einfuegen

    ausgabetabelle = join(workspace_projekt_emissionen,'T02RECH_04_Versorgung_Ergebnis')

    #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
    rows = arcpy.SearchCursor(ausgabetabelle)
    fieldnames = [f.name for f in arcpy.ListFields(ausgabetabelle)]
    j = 1
    for row in rows:
        i = 0
        for fieldname in fieldnames:
            wert = row.getValue(fieldname)
            ws5.write(j, i, wert,normal)
            i = i+1

        j = j+1

    #Felder als Header in Worksheet einfuegen
    i = 0
    for fieldname in fieldnames:
        column_with = len(fieldname)+2
        ws5.set_column(i, i, column_with)
        ws5.write(0, i, fieldname, bold)
        i = i+1


    ################################
    #Auswertungsblatt einfuegen

    formulastring1 = 'MAX(Rohdaten_Wohnen_Energie!D:D)+SUM(Rohdaten_Wohnen_Heizung!E:E)'
    ws6.write_formula(3,2, formulastring1,normal)
    ws6.write(3,1, "Wohnen",normal)

    formulastring2 = 'SUM(Rohdaten_Gewerbe!E:E)'
    ws6.write_formula(4,2, formulastring2,normal)
    ws6.write(4,1, "Gewerbe",normal)

    formulastring3 = 'Rohdaten_Einzelhandel!D2'
    ws6.write_formula(5,2, formulastring3,normal)
    ws6.write(5,1, "Einzelhandel",normal)


    # Werte in Chartobjekte schreiben
    chart_co2_jahr.add_series({
        'values': '=Auswertungen!C4:C6',
        'categories': '=Auswertungen!B4:B6',
        'name':'CO2 jahr',
    })

    ################
    # Ueberschriften einfuegen

    # Erste Leerspalte anpassen
    ws6.set_column(0, 0, 3)

    # Ueberschriften einfuegen
    ws6.write(0, 1, 'CO2-Emissionen nach Themenfeldern', bold)
    ws6.write(1, 1, 'Werte in Tonnen pro Jahr',normal)

    #Spaltenbreiten anpassen
    ws6.set_column(1, 1, 40)


    ################################
    #Grafikblatt einfuegen
    ws7.insert_chart('B2', chart_co2_jahr)

    ################################
    #Methodikblatt einfuegen
    methodik_grafik = join(base_path,"2_Tool","E_Energieverbrauch","Erlaeuterungstexte","Methodik_Energieverbrauch.png")
    ws8.insert_image('B2', methodik_grafik, {'x_scale': 0.32, 'y_scale': 0.32}) #Korrigiert Verzerrung die bei 1x1 auftritt

    ################################
    #Haftungsausschluss einfuegen
    haftung_grafik = join(base_path,"2_Tool","E_Energieverbrauch","Erlaeuterungstexte","Haftungsausschluss.png")
    ws9.insert_image('B2', haftung_grafik, {'x_scale': 0.32, 'y_scale': 0.32}) #Korrigiert Verzerrung die bei 1x1 auftritt

    ################################
    #Workbook speichern
    try:
        wb.close()
    except Exception as r:
        messages.AddMessage("Es liegt ein Fehler beim Speichern der Ausgabedatei vor. Ist diese ggf. noch geoeffnet?")
        messages.AddMessage(r)

    # Endmeldung
    print 'Berechnung abgeschlossen'
    messages.AddMessage('Berechnung abgeschlossen')
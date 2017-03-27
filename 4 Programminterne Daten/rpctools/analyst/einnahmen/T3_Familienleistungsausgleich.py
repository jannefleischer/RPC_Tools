# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 03_Familienleistungsausgleich.py
#
# Description: Erstellung der Einkommensteuerberechnung
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# GGR Planung
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


#############################################################################################################
#
# Beginne Hauptteil
#
#############################################################################################################

# Import arcpy modules
import os
import gc
import sys
import imp
from os.path import join, isdir, abspath, dirname, basename
import arcpy
import xlsxwriter
import inspect, pyodbc, gc, sys, datetime, urllib2, json

from rpctools.utils.params import Tool
import rpctools.utils.sheet_lib as sl
import rpctools.utils.tempmdb_lib as mdb



class Familienleistungsausgleich(Tool):

    _dbname = 'FGDB_Einnahmen.gdb'

    def run(self):
        parameters = self.par

        arcpy.env.overwriteOutput = True

        # Variablen definieren
        projektname = self.par.name.value

        #Pfade einrichten
        base_path = str(sys.path[0]).split("2 Planungsprojekte analysieren")[0]

        workspace_basisdaten = self.folders.get_basedb('FGDB_Basisdaten_deutschland.gdb')
        workspace_projekt_definition = self.folders.get_db('FGDB_Definition_Projekt.gdb', projektname)
        workspace_projekt_bevoelkerung = self.folders.get_db('FGDB_BevModellierung.gdb', projektname)
        workspace_projekt_einnahmen = self.folders.get_db('FGDB_Einnahmen.gdb', projektname)
        workspace_tool_definition = self.folders.get_basedb('FGDB_Definition_Projekt_Tool.gdb')
        workspace_tool_einnahmen = self.folders.get_basedb('FGDB_Einnahmen_Tool.gdb')

        Teilflaechen_Plangebiet_Centroide = join(workspace_projekt_definition, "Teilflaechen_Plangebiet_Centroide")
        Teilflaechen_Plangebiet_CentroideGK3 = join(workspace_projekt_definition, "Teilflaechen_Plangebiet_CentroideGK3")
        gemeindenWirkraumEW_Centroide = join(workspace_projekt_definition,"gemeindenWirkraumEW_Centroide")
        gemeindenWirkraumAP_Centroide = join(workspace_projekt_definition,"gemeindenWirkraumAP_Centroide")

        input_table = join(workspace_projekt_bevoelkerung,'T02RECH_Input')

        #############################################################################################################
        #
        # Durchlauf Auswirkungen im Umland
        #
        #############################################################################################################
        beginmeldung = 'Durchlauf Familienleistungsausgleich \n'
        arcpy.AddMessage(beginmeldung)
        print beginmeldung

        #############################################################################################################
        # Schritt 1
        schrittmeldung = 'Ermittle Familienleistungsausgleich \n'
        arcpy.AddMessage(schrittmeldung)
        print schrittmeldung

        # Erzeuge FLA_Zwischentabelle
        eingangstabellen = [
            (workspace_projekt_einnahmen,'EKST_06_Bilanz'),
            (workspace_tool_einnahmen,'FLA_Landesfaktoren')
        ]

        ausgabetabelle = (workspace_projekt_einnahmen,'FLA_Zwischentabelle')

        sql = """SELECT EKST_06_Bilanz.AGS, Left([AGS],2) AS AGS_Land, EKST_06_Bilanz.Betrachtungsjahr, EKST_06_Bilanz.Bilanz_EST_EUR AS EST_EUR INTO FLA_Zwischentabelle
        FROM EKST_06_Bilanz;
        """

        mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

        # Erzeuge FLA_Ergebnis
        eingangstabellen = [
            (workspace_projekt_einnahmen,'FLA_Zwischentabelle'),
            (workspace_tool_einnahmen,'FLA_Landesfaktoren')
        ]

        ausgabetabelle = (workspace_projekt_einnahmen,'FLA_01_Ergebnis')

        sql = """SELECT FLA_Zwischentabelle.AGS, FLA_Zwischentabelle.Betrachtungsjahr, [EST_EUR]*[FLA_Faktor] AS FLA_EURO INTO FLA_01_Ergebnis
        FROM FLA_Landesfaktoren INNER JOIN FLA_Zwischentabelle ON FLA_Landesfaktoren.AGS_Land = FLA_Zwischentabelle.AGS_Land;
        """

        mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

        #############################################################################################################
        # Schritt 6 - Datenexport in Excel-Datei
        schrittmeldung = 'Datenexport in Excel-Datei  \n'
        arcpy.AddMessage(schrittmeldung)
        print schrittmeldung

        # Pfade setzen
        logo = join((str(sys.path[0]).split("2 Planungsprojekte analysieren")[0]),"1_Basisdaten","logo_rpc.png")
        ausgabeordner = join(base_path,'3 Benutzerdefinierte Projekte',projektname,'Ergebnisausgabe','Excel')
        if not os.path.exists(ausgabeordner): os.makedirs(ausgabeordner)
        excelpfad = join(ausgabeordner,'Einnahmen_Familienleistungsausgleich.xlsx')

        try:
            os.remove(excelpfad)
        except:
            pass

        # Workbook und Tabellenblätter anlegen
        wb = xlsxwriter.Workbook(excelpfad)
        sl.infosheet(projektname, str("Familienleistungsausgleich").decode('utf-8'), wb)
        ws1 = wb.add_worksheet('Methodik')
        ws2 = wb.add_worksheet('Auswertungen')
        ws3 = wb.add_worksheet('Grafiken')
        ws4 = wb.add_worksheet('Rohdaten_FLA')
        ws5 = wb.add_worksheet('Haftungsausschluss')

        #Charts anlegen


        #Styles anlegen
        bold = wb.add_format({'bold': True})
        bold.set_bg_color('white')
        bold.set_border(0)

        normal = wb.add_format()
        normal.set_bg_color('white')
        normal.set_border(0)

        money = wb.add_format()
        money.set_num_format('#,##0')
        money.set_bg_color('white')
        money.set_border(0)

        #Hintergrund weiss faerben
        format = wb.add_format()
        format.set_bg_color('white')
        format.set_border(0)

        for x in range(0,400):
            for y in range(0,400):
                ws1.write(x,y,"", format)
                ws2.write(x,y,"", format)
                ws3.write(x,y,"", format)
                ws4.write(x,y,"", format)
                ws5.write(x,y,"", format)


        ################################
        #Werteblatt 1 einfuegen

        ausgabetabelle = join(workspace_projekt_einnahmen,'FLA_01_Ergebnis')

        #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen

        fieldnames = [f.name for f in arcpy.ListFields(ausgabetabelle)]
        rows = arcpy.da.SearchCursor(ausgabetabelle, fieldnames)
        j = 1
        for row in rows:
            i = 0
            for fieldname in fieldnames:
                wert = row[i]
                ws4.write(j, i, wert)
                i = i+1

            j = j+1

        #Felder als Header in Worksheet einfuegen
        i = 0
        for fieldname in fieldnames:
            column_with = len(fieldname)+2
            ws4.set_column(i, i, column_with)
            ws4.write(0, i, fieldname, bold)
            i = i+1

        #Eurobetrag formatieren
        ws4.set_column('A:A', 9,normal)
        ws4.set_column('B:B', 9,normal)
        ws4.set_column('C:C', 16,normal)
        ws4.set_column('D:D', 18, money)

        ################################
        #Methodikblatt einfuegen
        methodik_grafik = join(base_path,"2_Tool","Einnahmen","Erlaeuterungstexte","Methodik_03_Familienleistungsausgleich.png")
        ws1.insert_image('B2', methodik_grafik, {'x_scale': 0.6, 'y_scale': 0.6}) #Korrigiert Verzerrung die bei 1x1 auftritt

        ################################
        #Haftungsausschluss einfuegen
        haftung_grafik = join(base_path,"2_Tool","Einnahmen","Erlaeuterungstexte","Haftungsausschluss.png")
        ws5.insert_image('B2', haftung_grafik, {'x_scale': 0.32, 'y_scale': 0.32}) #Korrigiert Verzerrung die bei 1x1 auftritt

        ################################
        #Auswertungen formatieren

        #Ueberschrift
        ws2.write(1,1,"Mehr- bzw. Mindereinnahmen im Zeitverlauf",bold)

        AGSListe = []
        JahrListe = []

        fields = "AGS"
        rows = arcpy.da.SearchCursor(ausgabetabelle, fields)
        for row in rows:
            AGSListe.append(row[0])

        fields = "Betrachtungsjahr"
        rows = arcpy.da.SearchCursor(ausgabetabelle, fields)
        for row in rows:
            JahrListe.append(row[0])

        AGSListe = sorted(set(AGSListe))
        JahrListe = sorted(set(JahrListe))

        print JahrListe
        print AGSListe

        #schreibe Jahre
        i = 0
        for j in JahrListe:
            ws2.write(3,i+2,j,bold)
            i+=1

        #schreibe AGS
        i = 0
        for a in AGSListe:
            ws2.write(i+4,1,a,bold)
            i+=1

        #schreibe Werte
        i=0
        f=0
        alphabet = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'aa','ab','ac','ad','ae','af','ag','ah','ai','aj','ak','al','am','an','ao','ap','aq','ar', 'as', 'at', 'au', 'av', 'aw', 'ax', 'ay', 'az'
        ]
        for j in JahrListe:
            for a in AGSListe:
                formula = "=SUMIFS(Rohdaten_FLA!$D:$D,Rohdaten_FLA!$B:$B,Auswertungen!B"+str(i+5)+",Rohdaten_FLA!$C:$C,Auswertungen!"+alphabet[f+2]+"4)"
                ws2.write_formula(i+4, f+2, formula, money)
                i+=1
            i=0
            f+=1


        #Schreibe AGS als Ueberschrift
        ws2.write(3,1,"AGS",bold)


        ################################
        #Grafiken einfuegen

        print len(JahrListe)
        print len(AGSListe)

        chart = wb.add_chart({'type': 'line', 'subtype': 'stacked'})
        chart.set_style(40)
        chart.set_size({'width': 800, 'height': 600})
        chart.set_chartarea({'border': {'none': True},'fill': {'none': True}})
        chart.set_legend({'position': 'bottom'})
        chart.set_title({'name': 'Familienleistungsausgleich in Euro','name_font':  {'name': 'Tahoma', 'size': 9}})


        i=0

        for ags in AGSListe:

            i+=1

            chart.add_series({
                    'name': ['Auswertungen', 3+i, 1, 3+i, 1],
                    'categories': ['Auswertungen', 3, 2, 3, len(JahrListe)+1],
                    'values':     ['Auswertungen', 3+i, 2, 3+i, len(JahrListe)+1], # Format: Zeile, Spalte Anfang, Zeile , Spalte Ende
                })

        ws3.insert_chart('B2', chart)


        ################################
        #Workbook speichern
        try:
            wb.close()
        except Exception as r:
            arcpy.AddMessage("Es liegt ein Fehler beim Speichern der Ausgabedatei vor. Ist diese ggf. noch geoeffnet?")
            arcpy.AddMessage(r)


        #############################################################################################################
        # Schritt 4
        schrittmeldung = 'temporaere Tabellen loeschen \n'
        arcpy.AddMessage(schrittmeldung)
        print schrittmeldung

        deleteList = ['FLA_Zwischentabelle']

        for e in deleteList:
            f = join(workspace_projekt_einnahmen,e)
            try:
                arcpy.Delete_management(f)
            except:
                pass

        gc.collect()
        print "fertig"
        arcpy.AddMessage('03_Familienleistungsausgleich abgeschlossen')
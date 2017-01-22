# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 32_KFA_01.py
#
# Description: Berechnung des Kommunalen Finanzausgleichs für das zu untersuchende Projekt
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# ILS / GGR Planung
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

from rpctools.utils.params import Tool
import rpctools.utils.sheet_lib as sl
import rpctools.utils.tempmdb_lib as mdb


class KRU(Tool):

    _dbname = 'FGDB_Einnahmen.gdb'

    def run(self):

        parameters = self.par

        arcpy.env.overwriteOutput = True

        # Variablen definieren
        projektname = parameters[0].value

        #Pfade einrichten
        base_path = str(sys.path[0]).split("2_Tool")[0]
        workspace_projekt_definition = join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt.gdb')
        workspace_projekt_einnahmen = join(base_path,'3_Projekte',projektname,'FGDB_Einnahmen.gdb')
        workspace_tool_definition = join(base_path,"2_Tool","3_Art und Mass der Nutzung","FGDB_Definition_Projekt_Tool.gdb")
        workspace_tool_einnahmen = join(base_path,"2_Tool","B_Einnahmen","FGDB_Einnahmen_Tool.gdb")

        #############################################################################################################
        # Vereinigungsmenge aus Umland erzeugen AGS aus EW und AP zusammen führen) inkl. eigene Kommune

        schrittmeldung = 'Zwischentabelle AGS8 zu AGS5 erzeugen\n'
        arcpy.AddMessage(schrittmeldung)
        print schrittmeldung

        # Erzeuge KRU_AGS5_zu_AGS8_temp
        eingangstabellen = [
            (workspace_projekt_einnahmen,'KFA_02_Statische_Daten')
        ]

        ausgabetabelle = (workspace_projekt_einnahmen,'KRU_AGS5_zu_AGS8_temp')

        sql = """SELECT KFA_02_Statische_Daten.AGs AS AGS8, Left([AGs],5) AS AGS5 INTO KRU_AGS5_zu_AGS8_temp
        FROM KFA_02_Statische_Daten
        GROUP BY KFA_02_Statische_Daten.AGs, KFA_02_Statische_Daten.Kreisfrei
        HAVING (((KFA_02_Statische_Daten.Kreisfrei)=0));
        """

        mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)


        #############################################################################################################
        # Vereinigungsmenge aus Umland erzeugen AGS aus EW und AP zusammen führen) inkl. eigene Kommune

        schrittmeldung = 'KRU_02_delta_Kreisumlage \n'
        arcpy.AddMessage(schrittmeldung)
        print schrittmeldung

        # Erzeuge KRU_02_delta_Kreisumlage
        eingangstabellen = [
            (workspace_projekt_einnahmen,'KFA_05_Zuweisungen'),
            (workspace_projekt_einnahmen,'KRU_AGS5_zu_AGS8_temp'),
            (workspace_projekt_einnahmen,'KRU_01_Kreisumlagesaetze_Wirkraum')
        ]

        ausgabetabelle = (workspace_projekt_einnahmen,'KRU_02_delta_Kreisumlage')

        sql = """SELECT KFA_05_Zuweisungen.AGS, KFA_05_Zuweisungen.AGS_VG, KFA_05_Zuweisungen.AGS_Regenesis, KFA_05_Zuweisungen.Jahr, ([deltaSKMZ]+[Zuweisungen]*[Faktor_Zuweisungen_KU])*[Umlagensatz_in_vH]/100 *-1 AS deltaKreisumlage INTO KRU_02_delta_Kreisumlage
        FROM (KFA_05_Zuweisungen INNER JOIN KRU_AGS5_zu_AGS8_temp ON KFA_05_Zuweisungen.AGS = KRU_AGS5_zu_AGS8_temp.AGS8) INNER JOIN KRU_01_Kreisumlagesaetze_Wirkraum ON KRU_AGS5_zu_AGS8_temp.AGS5 = KRU_01_Kreisumlagesaetze_Wirkraum.AGS5
        ORDER BY KFA_05_Zuweisungen.AGS, KFA_05_Zuweisungen.AGS_VG, KFA_05_Zuweisungen.AGS_Regenesis, KFA_05_Zuweisungen.Jahr;
        """

        mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

        #############################################################################################################
        # Schritt 6 - Datenexport in Excel-Datei
        schrittmeldung = 'Datenexport in Excel-Datei  \n'
        arcpy.AddMessage(schrittmeldung)
        print schrittmeldung

        # Pfade setzen
        logo = join((str(sys.path[0]).split("2_Tool")[0]),"1_Basisdaten","logo_rpc.png")
        ausgabeordner = join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Excel')
        if not os.path.exists(ausgabeordner): os.makedirs(ausgabeordner)
        excelpfad = join(ausgabeordner,'Einnahmen_Kreisumlage.xlsx')

        try:
            os.remove(excelpfad)
        except:
            pass

        # Workbook und Tabellenblätter anlegen
        wb = xlsxwriter.Workbook(excelpfad)
        sl.infosheet(projektname, str("Kreisumlage").decode('utf-8'), wb)
        ws1 = wb.add_worksheet('Methodik')
        ws2 = wb.add_worksheet('Auswertungen')
        ws3 = wb.add_worksheet('Grafiken')
        ws4 = wb.add_worksheet('Rohdaten_KRU')
        ws5 = wb.add_worksheet('Haftungsausschluss')

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

        ausgabetabelle = join(workspace_projekt_einnahmen,'KRU_02_delta_Kreisumlage')

        #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
        rows = arcpy.SearchCursor(ausgabetabelle)
        fieldnames = [f.name for f in arcpy.ListFields(ausgabetabelle)]
        j = 1
        for row in rows:
            i = 0
            for fieldname in fieldnames:
                wert = row.getValue(fieldname)
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
        ws4.set_column('D:D', 22, money)

        ################################
        #Methodikblatt einfuegen
        methodik_grafik = join(base_path,"2_Tool","B_Einnahmen","Erlaeuterungstexte","Methodik_07_KRU.png")
        ws1.insert_image('B2', methodik_grafik, {'x_scale': 0.6, 'y_scale': 0.6}) #Korrigiert Verzerrung die bei 1x1 auftritt

        ################################
        #Haftungsausschluss einfuegen
        haftung_grafik = join(base_path,"2_Tool","B_Einnahmen","Erlaeuterungstexte","Haftungsausschluss.png")
        ws5.insert_image('B2', haftung_grafik, {'x_scale': 0.32, 'y_scale': 0.32}) #Korrigiert Verzerrung die bei 1x1 auftritt

        ################################
        #Auswertungen formatieren

        #Ueberschrift
        ws2.write(1,1,"Mehr- bzw. Mindereinnahmen im Zeitverlauf",bold)

        AGSListe = []
        JahrListe = []

        rows = arcpy.SearchCursor(ausgabetabelle)
        for row in rows:
            AGSListe.append(row.getValue("AGS"))

        rows = arcpy.SearchCursor(ausgabetabelle)
        for row in rows:
            JahrListe.append(row.getValue("Jahr"))

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
                try:
                    formula = "=SUMIFS(Rohdaten_KRU!$F:$F,Rohdaten_KRU!$B:$B,Auswertungen!B"+str(i+5)+",Rohdaten_KRU!$E:$E,Auswertungen!"+alphabet[f+2]+"4)"
                    ws2.write_formula(i+4, f+2, formula, money)
                    i+=1
                except Exception as e:
                    print e
            i=0
            f+=1

        ################################
        #Grafiken einfuegen

        print len(JahrListe)
        print len(AGSListe)

        chart = wb.add_chart({'type': 'line', 'subtype': 'stacked'})
        chart.set_style(40)
        chart.set_size({'width': 800, 'height': 600})
        chart.set_chartarea({'border': {'none': True},'fill': {'none': True}})
        chart.set_legend({'position': 'bottom'})
        chart.set_title({'name': 'Kreisumlage in Euro','name_font':  {'name': 'Tahoma', 'size': 9}})

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
            arcpy.AddMessage(e)

        #############################################################################################################
        # Schritt 4
        schrittmeldung = 'temporaere Tabellen loeschen \n'
        arcpy.AddMessage(schrittmeldung)
        print schrittmeldung

        deleteList = ['KRU_AGS5_zu_AGS8_temp']

        for e in deleteList:
            f = join(workspace_projekt_einnahmen,e)
            try:
                arcpy.Delete_management(f)
            except:
                pass

        gc.collect()
        print "fertig"
        arcpy.AddMessage('06_Kommunaler Finanzausgleich abgeschlossen')
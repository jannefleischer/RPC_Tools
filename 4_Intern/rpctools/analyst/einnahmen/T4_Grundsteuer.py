# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 02_Einkommensteuer.py
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

# Import modules
import os
import gc
import sys
import imp

import arcpy
import xlsxwriter

from rpctools.utils.params import Tool
import rpctools.utils.sheet_lib as sl
import rpctools.utils.tempmdb_lib as tempmdb_lib
import rpctools.utils.population_lib as population_lib



class Grundsteuer(Tool):

    _dbname = 'FGDB_Einnahmen.gdb'

    def run(self):
        parameters = self.par

        arcpy.env.overwriteOutput = True

        # Variablen definieren
        projektname = parameters[0].value
        gemeindegroessenklasse64 = parameters[1].value
        grundsteuerhebesatz = parameters[2].value

        monatsrohmiete_EFH = parameters[3].value
        monatsrohmiete_DHH = parameters[4].value
        monatsrohmiete_RH = parameters[5].value
        monatsrohmieteMFH = parameters[6].value
        monatsrohmieteMFH_G = parameters[6].value
        jahresrohmiete_garage = parameters[7].value
        jahresrohmiete_carport = parameters[8].value

        #projektname = "HCU_LKH_Bultweg"

        #Pfade einrichten
        base_path = str(sys.path[0]).split("2_Tool")[0]

        workspace_basisdaten = join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb')
        workspace_projekt_definition = join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt.gdb')
        workspace_projekt_bevoelkerung = join(base_path,'3_Projekte',projektname,'FGDB_BevModellierung.gdb')
        workspace_projekt_einnahmen = join(base_path,'3_Projekte',projektname,'FGDB_Einnahmen.gdb')
        workspace_tool_definition = join(base_path,"2_Tool","3_Art und Mass der Nutzung","FGDB_Definition_Projekt_Tool.gdb")
        workspace_tool_einnahmen = join(base_path,"2_Tool","B_Einnahmen","FGDB_Einnahmen_Tool.gdb")

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
        beginmeldung = 'Durchlauf Grundsteuer \n'
        arcpy.AddMessage(beginmeldung)
        print beginmeldung

        #############################################################################################################
        # Schritt 1
        schrittmeldung = 'Einlesen Eingangstabellen\n'
        arcpy.AddMessage(schrittmeldung)
        print schrittmeldung

        #Einlesen der Tabellen
        #Jahr I Gebäudetyp I Miete/Eigentum I Anzahl WE
        #Gebäudetyp I Wohnfläche_m²_proWE I Anzahl_Garagen_proWE I Anzahl_Carports_proWE

        #Pruefe, ob Tabellen aus EKS-Berechnung vorhanden sind
        EKST_03_WE_NBG = join(workspace_projekt_einnahmen,'EKST_03_WE_NBG')
        rowcount = arcpy.GetCount_management(EKST_03_WE_NBG)
        if rowcount == 0:
            arcpy.AddMessage("Das Modul Einkommensteuer wurde noch nicht vollstaendig ausgefuehrt.\rDie fuer das Modul Grundsteuer benoetigten Tabellen sind daher noch nicht vorhanden.")
            sys.exit("")


        EKST_03_WE_NBG = join(workspace_projekt_einnahmen,'EKST_03_WE_NBG')

        #############################################################################################################
        # Schritt 2
        schrittmeldung = 'Ermittle Jahresrohmieten\n'
        arcpy.AddMessage(schrittmeldung)
        print schrittmeldung

        #Ubertrage Nutzereingaben in GRST_Rohmieten


        GRST_Rohmieten = join(workspace_projekt_einnahmen,'GRST_Rohmieten')

        arcpy.TruncateTable_management(GRST_Rohmieten)
        in_cur = arcpy.InsertCursor(GRST_Rohmieten)
        row = in_cur.newRow()
        row.Gebaeudetyp = 'Einfamilienhaus'
        row.Rohmiete = float(monatsrohmiete_EFH) * 12
        in_cur.insertRow(row)

        row = in_cur.newRow()
        row.Gebaeudetyp = 'Zweifamilien- oder Doppelhaus'
        row.Rohmiete = float(monatsrohmiete_DHH) * 12
        in_cur.insertRow(row)

        row = in_cur.newRow()
        row.Gebaeudetyp = 'Reihenhaus'
        row.Rohmiete = float(monatsrohmiete_RH) * 12
        in_cur.insertRow(row)

        row = in_cur.newRow()
        row.Gebaeudetyp = 'Mehrfamilienhaus'
        row.Rohmiete = float(monatsrohmieteMFH) * 12
        in_cur.insertRow(row)

        row = in_cur.newRow()
        row.Gebaeudetyp = 'Mehrfamilienhaus mit Gewerbeeinheiten'
        row.Rohmiete = float(monatsrohmieteMFH) * 12
        in_cur.insertRow(row)

        ##row = in_cur.newRow()
        ##row.Gebaeudetyp = 'Bürogebäude'
        ##row.Jahresrohmiete = 0
        ##in_cur.insertRow(row)
        ##
        ##row = in_cur.newRow()
        ##row.Gebaeudetyp = 'Gewerbegebäude'
        ##row.Jahresrohmiete = 0
        ##in_cur.insertRow(row)
        ##
        ##row = in_cur.newRow()
        ##row.Gebaeudetyp = 'Einzelhandelsgebäude'
        ##row.Jahresrohmiete = 0
        ##in_cur.insertRow(row)


        # erzeuge Tabelle Gebäudetyp I Jahresrohmiete = Wohnfläche * Monatsrohmiete *12 + Anzahl_Garagen * Jahresrohmiete_Garagen + Anzahl_Carports * Jahresrohmiete_Carports

        # Fixe Tabelle Gebäudetyp I Gemeindegrößenklasse64 I Vervielfältiger (als double)

        eingangstabellen = [
            (workspace_tool_definition,'Gebaeudetyp'),
            (workspace_projekt_einnahmen,'EKST_03_WE_NBG'),
            (workspace_projekt_einnahmen,'GRST_Rohmieten')
        ]

        ausgabetabelle = (workspace_projekt_einnahmen,'GRST_Jahresrohmiete')

        sql = """SELECT Gebaeudetyp.Gebaeudetyp, [Wohnfl_m2_pro_WE]*[Rohmiete]+[Garagen_pro_WE]*jahresrohmiete_garage+[Carport_pro_WE]*jahresrohmiete_carport AS Jahresrohmiete INTO GRST_Jahresrohmiete
        FROM GRST_Rohmieten RIGHT JOIN Gebaeudetyp ON GRST_Rohmieten.Gebaeudetyp = Gebaeudetyp.Gebaeudetyp;"""

        sql = sql.replace("jahresrohmiete_garage",str(jahresrohmiete_garage)).replace("jahresrohmiete_carport",str(jahresrohmiete_carport))

        mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

        #############################################################################################################
        # Schritt 3
        schrittmeldung = 'Einheitswert\n'
        arcpy.AddMessage(schrittmeldung)
        print schrittmeldung

        # erzeuge Tabelle Gebäudetyp I Einheitswert_bis38346_EUR I Einheitswert_ab38346_EUR
        # Einheitswert = Jahresrohmiete (aus Nr. 2) * Vervielfältiger je Gebäudetyp
        # Achtung! Ergebnisse BIS 38346 gehen komplett in diese Spalte. Liegt das Ergebnis darüber gehen 38346 in die Spalte und der Restbetrag in die Spalte Einheitswert_ab38346_EUR
        # Beispiel: 90000 = 1 * 38346_EUR in Spalte Einheitswert_bis38346_EUR und 90000-38346 in Einheitswert_ab38346_EUR

        # Fixe Tabelle Gebäudetyp I Steuermesszahl_bis38346_EUR I Steuermesszahl_ueber38346_EUR

        #Erstelle temporaere Zwischentabelle
        eingangstabellen = [
            (workspace_tool_einnahmen,'GRST_Vervielfaeltiger'),
            (workspace_projekt_einnahmen,'GRST_Jahresrohmiete'),
        ]

        ausgabetabelle = (workspace_projekt_einnahmen,'GRST_Einheitswert_temp')

        sql = """
        SELECT GRST_Jahresrohmiete.Gebaeudetyp, [Jahresrohmiete]*[Vervielfaeltiger] AS Einheitswert INTO GRST_Einheitswert_temp
        FROM GRST_Jahresrohmiete INNER JOIN GRST_Vervielfaeltiger ON GRST_Jahresrohmiete.Gebaeudetyp = GRST_Vervielfaeltiger.Gebaeudetyp
        WHERE (((GRST_Vervielfaeltiger.Gemeindegroessenklasse64)='2000 bis 5000 EW'))
        GROUP BY GRST_Jahresrohmiete.Gebaeudetyp, [Jahresrohmiete]*[Vervielfaeltiger];
        """

        sql = sql.replace("2000 bis 5000 EW",str(gemeindegroessenklasse64))
        mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

        #Erstelle leere Tabelle GRST_Einheitswert
        eingangstabellen = [
            (workspace_projekt_einnahmen,'GRST_Einheitswert_temp')
        ]

        ausgabetabelle = (workspace_projekt_einnahmen,'GRST_Einheitswert')

        sql = """
        SELECT GRST_Einheitswert_temp.Gebaeudetyp, Round([Einheitswert],0) AS Einheitswert_Summe, 1 AS Einheitswert_bis38346_EUR, 1 AS Einheitswert_ueber38346_EUR INTO GRST_Einheitswert
        FROM GRST_Einheitswert_temp;
        """

        mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

        #Fuelle Werte in Einheitswerttabelle aus

        einheitswert = join(workspace_projekt_einnahmen,'GRST_Einheitswert')
        fields = ["Einheitswert_Summe", "Gebaeudetyp"]
        rows1 = arcpy.da.SearchCursor(einheitswert, fields)
        for row1 in rows1:
            einheitswert_value = row1[0]
            gebauedetyp = row1[1]

            if int(einheitswert_value) <= 38346:
                Steuermesszahl_bis38346_EUR = einheitswert_value
                Steuermesszahl_ueber38346_EUR = 0

            if int(einheitswert_value) > 38346:
                Steuermesszahl_bis38346_EUR = 38346
                Steuermesszahl_ueber38346_EUR = einheitswert_value - 38346

            where = '"Gebaeudetyp" = '+ "'"+gebauedetyp+"'"
            fields = ["Einheitswert_bis38346_EUR","Einheitswert_ueber38346_EUR"]
            rows2 = arcpy.da.UpdateCursor(einheitswert, fields, where)
            for row2 in rows2:
                row2[0] = Steuermesszahl_bis38346_EUR
                row2[1] = Steuermesszahl_ueber38346_EUR
                rows2.updateRow(row2)


        #############################################################################################################
        # Schritt 4
        schrittmeldung = 'Steuermessbetrag und Steuerschuld\n'
        arcpy.AddMessage(schrittmeldung)
        print schrittmeldung

        #erzeuge Tabelle Gebäudetyp I Steuerschuld_Jahr = (Einheitswert_bis38346_EUR * Steuermesszahl_bis38346_EUR + Einheitswert_ab38346_EUR * Steuermesszahl_ueber38346_EUR) * Hebesatz / 100

        #Erstelle Tabelle Steuermessbetrag
        eingangstabellen = [
            (workspace_projekt_einnahmen,'GRST_Einheitswert'),
            (workspace_tool_einnahmen,'GRST_Steuermesszahlen')
        ]

        ausgabetabelle = (workspace_projekt_einnahmen,'GRST_Steuermessbetrag')

        sql = """SELECT GRST_Einheitswert.Gebaeudetyp, ([Einheitswert_bis38346_EUR]*[Steuermesszahl_bis_38346_EUR]+[Einheitswert_ueber38346_EUR]*[Steuermesszahl_ab_38346_EUR])*HEBESATZ/100 AS Steuerschuld_pro_Jahr INTO GRST_Steuermessbetrag
        FROM GRST_Einheitswert INNER JOIN GRST_Steuermesszahlen ON GRST_Einheitswert.Gebaeudetyp = GRST_Steuermesszahlen.Gebaeudetyp;
        """

        sql = sql.replace("HEBESATZ",str(grundsteuerhebesatz))
        mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

        #############################################################################################################
        # Schritt 5
        schrittmeldung = 'Grundsteuereinnahmen\n'
        arcpy.AddMessage(schrittmeldung)
        print schrittmeldung

        # erzeuge Tabelle Jahr I Grundsteuereinnahmen = (Anzahl_WE je Gebäudetyp aus Tabelle im Schrit 1 * Steuerschuld aus voriger Tabelle )

        #Erstelle Tabelle GRST_Grundsteuereinnahmen_temp
        eingangstabellen = [
            (workspace_projekt_einnahmen,'GRST_Steuermessbetrag'),
            (workspace_projekt_einnahmen,'EKST_03_WE_NBG')
        ]

        ausgabetabelle = (workspace_projekt_einnahmen,'GRST_Grundsteuereinnahmen_temp')

        sql = """SELECT EKST_03_WE_NBG.Jahr, EKST_03_WE_NBG.Gebaeudetyp, Sum([Anzahl_WE]*[Steuerschuld_pro_Jahr]) AS GrStEinnahmen INTO GRST_Grundsteuereinnahmen_temp
        FROM EKST_03_WE_NBG INNER JOIN GRST_Steuermessbetrag ON EKST_03_WE_NBG.Gebaeudetyp = GRST_Steuermessbetrag.Gebaeudetyp
        GROUP BY EKST_03_WE_NBG.Jahr, EKST_03_WE_NBG.Gebaeudetyp
        ORDER BY EKST_03_WE_NBG.Jahr;
        """

        mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)


        #Erstelle Tabelle GRST_Grundsteuereinnahmen
        eingangstabellen = [
            (workspace_projekt_einnahmen,'GRST_Grundsteuereinnahmen_temp')
        ]

        ausgabetabelle = (workspace_projekt_einnahmen,'GRST_Grundsteuereinnahmen')

        sql = """SELECT GRST_Grundsteuereinnahmen_temp.Jahr, Sum(GRST_Grundsteuereinnahmen_temp.GrStEinnahmen) AS GrStEinnahmen INTO GRST_Grundsteuereinnahmen
        FROM GRST_Grundsteuereinnahmen_temp
        GROUP BY GRST_Grundsteuereinnahmen_temp.Jahr;
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
        excelpfad = join(ausgabeordner,'Einnahmen_Grundsteuer.xlsx')

        try:
            os.remove(excelpfad)
        except:
            pass

        # Workbook und Tabellenblätter anlegen
        wb = xlsxwriter.Workbook(excelpfad)
        sl.infosheet(projektname, str("Grundsteuer").decode('utf-8'), wb)
        ws1 = wb.add_worksheet('Methodik')
        ws3 = wb.add_worksheet('Grafiken')
        ws4 = wb.add_worksheet('Rohdaten_Grundsteuer')
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
                ws3.write(x,y,"", format)
                ws4.write(x,y,"", format)
                ws5.write(x,y,"", format)

        ################################
        #Werteblatt 1 einfuegen

        ausgabetabelle = join(workspace_projekt_einnahmen,'GRST_Grundsteuereinnahmen')

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
        ws4.set_column('A:A', 9, normal)
        ws4.set_column('B:B', 9, normal)
        ws4.set_column('C:C', 18, money)

        ################################
        #Grafiken einfuegen

        chart = wb.add_chart({'type': 'line', 'subtype': 'stacked'})
        chart.set_style(40)
        chart.set_size({'width': 800, 'height': 600})
        chart.set_chartarea({'border': {'none': True},'fill': {'none': True}})
        chart.set_legend({'position': 'bottom'})
        chart.set_title({'name': 'Grundsteuer in Euro','name_font':  {'name': 'Tahoma', 'size': 9}})


        jahre = 0
        rows = arcpy.SearchCursor(ausgabetabelle)
        for row in rows:
            jahre +=1

        chart.add_series({
                'name': 'Grundsteuer',
                'categories': ['Rohdaten_Grundsteuer', 1, 1, jahre+1, 1],
                'values':     ['Rohdaten_Grundsteuer', 1, 2, jahre+1, 2], # Format: Zeile, Spalte Anfang, Zeile , Spalte Ende
            })

        ws3.insert_chart('B2', chart)

        ################################
        #Methodikblatt einfuegen
        methodik_grafik = join(base_path,"2_Tool","B_Einnahmen","Erlaeuterungstexte","Methodik_04_Grundsteuer.png")
        ws1.insert_image('B2', methodik_grafik, {'x_scale': 0.6, 'y_scale': 0.6}) #Korrigiert Verzerrung die bei 1x1 auftritt

        ################################
        #Haftungsausschluss einfuegen
        haftung_grafik = join(base_path,"2_Tool","B_Einnahmen","Erlaeuterungstexte","Haftungsausschluss.png")
        ws5.insert_image('B2', haftung_grafik, {'x_scale': 0.32, 'y_scale': 0.32}) #Korrigiert Verzerrung die bei 1x1 auftritt

        ################################
        #Workbook speichern
        try:
            wb.close()
        except Exception as e:
            arcpy.AddMessage("Es liegt ein Fehler beim Speichern der Ausgabedatei vor. Ist diese ggf. noch geoeffnet?")
            arcpy.AddMessage(e)

        #############################################################################################################
        # Schritt 4
        schrittmeldung = 'Temporaere Tabellen loeschen \n'
        arcpy.AddMessage(schrittmeldung)
        print schrittmeldung

        deleteList = ['GRST_Einheitswert_temp', 'GRST_Grundsteuereinnahmen_temp']

        for e in deleteList:
            f = join(workspace_projekt_einnahmen,e)
            try:
                arcpy.Delete_management(f)
            except:
                pass

        gc.collect()
        print "fertig"
        arcpy.AddMessage('04_Grundsteuer abgeschlossen')
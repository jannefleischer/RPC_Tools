# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 05Gewerbesteuer.py
#
# Description: Erstellung der Einkommensteuerberechnung
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
import urllib2
import json
from os.path import join, isdir, abspath, dirname, basename
import arcpy
import xlsxwriter
from rpctools.utils.params import Message
from rpctools.utils.params import Tool
import rpctools.utils.sheet_lib as sl
import rpctools.utils.tempmdb_lib as mdb


class Gewerbesteuer(Tool):

    _dbname = 'FGDB_Einnahmen.gdb'

    def run(self):
        parameters = self.par


        arcpy.env.overwriteOutput = True

        # Variablen definieren
        projektname = self.par.name.value
        hebesatzProjektkommune = self.par.hebesatz.value
        #projektname = "HCU_LKH_Bultweg"

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
        beginmeldung = 'Durchlauf Gewerbesteuer \n'
        Message.AddMessage(beginmeldung)
        print beginmeldung

        #############################################################################################################
        # Schritt 1
        schrittmeldung = 'Ermittle Gewerbesteuer und Anzahl Arbeitsplaetze \n'
        Message.AddMessage(schrittmeldung)
        print schrittmeldung


        GWST_01_Basisdaten = join(workspace_projekt_einnahmen,'GWST_01_Basisdaten')
        arcpy.TruncateTable_management(GWST_01_Basisdaten)

        umlandtabelle = join(workspace_projekt_einnahmen, "AWU_WanderungsfaktorAP")
        fields = ["AGS", "AGS_VG", "AGS_Regenesis"]
        rows = arcpy.da.SearchCursor(umlandtabelle, fields)
        for row in rows:
            ags = row[0]
            ags_vg = row[1]
            ags_regenesis = row[2]

            arcpy.AddMessage(ags_regenesis)

            try:
                i = 0
                try:
                    AnteilGWS10 = getAnteilGWS(ags_regenesis, 2010)*1000
                    i+=1
                except:
                    AnteilGWS10 = 0
                try:
                    AnteilGWS11 = getAnteilGWS(ags_regenesis, 2011)*1000
                    i+=1
                except:
                    AnteilGWS11 = 0
                try:
                    AnteilGWS12 = getAnteilGWS(ags_regenesis, 2012)*1000
                    i+=1
                except:
                    AnteilGWS12 = 0

                try:
                    AnteilGWS = (AnteilGWS10+AnteilGWS11+AnteilGWS12)/i

                except Exception as r:
                    message = "\n Die zur Abfrage der Gewerbesteuer notwendige Webseite 'http://api.regenesis.pudo.org/' liefert derzeit keine Werte zurueck. Die Berechnung wird daher unterbrochen. Bitte probieren Sie es spaeter noch einmal. \n"
                    print message
                    arcpy.AddMessage(message)
                    arcpy.AddMessage(r)
                    sys.exit()

                i = 0
                try:
                    HebeSGWS10 = getHebesatzGWS(ags_regenesis, 2010)
                    i+=1
                except:
                    HebeSGWS10 = 0
                try:
                    HebeSGWS11 = getHebesatzGWS(ags_regenesis, 2011)
                    i+=1
                except:
                    HebeSGWS11 = 0
                try:
                    HebeSGWS12 = getHebesatzGWS(ags_regenesis, 2012)
                    i+=1
                except:
                    HebeSGWS12 = 0

                HebeSGWS = (HebeSGWS10+HebeSGWS11+HebeSGWS12)/i

                try:
                    AnzAP = getAnzAP(ags_regenesis)

                except Exception as r:
                    AnzAP = 1
                    arcpy.AddMessage(r)

                rows_insert = arcpy.InsertCursor(GWST_01_Basisdaten)
                row_in = rows_insert.newRow()
                row_in.AGS = ags
                row_in.KAGWST3Jahre = AnteilGWS
                row_in.AP2011 = AnzAP
                row_in.GWSTHebesatz = HebeSGWS
                rows_insert.insertRow(row_in)

            except Exception as e:
                message = "Gewerbesteuer fuer AGS: "+ags_regenesis+" kann nicht ermittelt werden: " + str(e)
                messages.AddMessage(message)
                sys.exit()

        arcpy.AddMessage("\n")

        #############################################################################################################
        # Schritt 1
        schrittmeldung = 'Aufsummieren der Gewerbesteuer pro Arbeitsplatz \n'
        messages.AddMessage(schrittmeldung)
        print schrittmeldung

        # Erzeuge GWST_02_GWSTproAPRefZiel
        eingangstabellen = [
            (workspace_projekt_einnahmen,'GWST_01_Basisdaten'),
            (workspace_projekt_einnahmen,'AWU_WanderungsfaktorAP')
        ]

        ausgabetabelle = (workspace_projekt_einnahmen,'GWST_02_GWSTproAPRefZiel')

        sql = """SELECT GWST_01_Basisdaten.AGS, GWST_01_Basisdaten.AGS_Regenesis, ([KAGWST3Jahre]/[AP2011]/[GWSTHebesatz]*100)*[AWU_Wanderungsfaktor] AS GWSTGrundbetragProAPReferenz INTO GWST_02_GWSTproAPRefZiel
                    FROM GWST_01_Basisdaten INNER JOIN AWU_WanderungsfaktorAP ON GWST_01_Basisdaten.AGS = AWU_WanderungsfaktorAP.AGS;
                    """

        mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

        # Ermittle Summe ueber Tabelle
        GWST_02_GWSTproAP = join(workspace_projekt_einnahmen,'GWST_02_GWSTproAPRefZiel')

        GWSTGrundbetragProAPReferenzZielort = 0
        rows = arcpy.SearchCursor(GWST_02_GWSTproAP)
        for row in rows:
            GWSTGrundbetragProAPReferenzZielort = GWSTGrundbetragProAPReferenzZielort + row.GWSTGrundbetragProAPReferenz

        # Erzeuge GWST_02_GWSTproAPRefHerkunft
        eingangstabellen = [
            (workspace_projekt_einnahmen,'GWST_01_Basisdaten')
        ]

        ausgabetabelle = (workspace_projekt_einnahmen,'GWST_02_GWSTproAPRefHerkunft')

        sql = """SELECT GWST_01_Basisdaten.AGS, GWST_01_Basisdaten.AGS_Regenesis, [KAGWST3Jahre]/[AP2011]/[GWSTHebesatz]*100 AS GWSTGrundbetragProAPRefHerkunft INTO GWST_02_GWSTproAPRefHerkunft
                    FROM GWST_01_Basisdaten;
                    """

        mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

        #############################################################################################################
        # Schritt 1
        schrittmeldung = 'Erzeuge Arbeitsplatzuebersicht \n'
        messages.AddMessage(schrittmeldung)
        print schrittmeldung

        # Erzeuge GWST_03_AP_NBG
        eingangstabellen = [
            (workspace_projekt_definition,'Gewerbe_Beschaeftigte')
        ]

        ausgabetabelle = (workspace_projekt_einnahmen,'GWST_03_AP_NBG')

        sql = """SELECT Gewerbe_Beschaeftigte.Jahr, Gewerbe_Beschaeftigte.Branche, Sum(Gewerbe_Beschaeftigte.Anzahl) AS SummevonAnzahl INTO GWST_03_AP_NBG
                    FROM Gewerbe_Beschaeftigte
                    GROUP BY Gewerbe_Beschaeftigte.Jahr, Gewerbe_Beschaeftigte.Branche
                    ORDER BY Gewerbe_Beschaeftigte.Jahr, Gewerbe_Beschaeftigte.Branche;
                    """

        mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)


        #############################################################################################################
        # Schritt 4
        schrittmeldung = 'Erzeuge GWST_04_Zuwachs \n'
        messages.AddMessage(schrittmeldung)
        print schrittmeldung

        # Erzeuge GWST_04_Zuwachs
        eingangstabellen = [
            (workspace_projekt_einnahmen,'GWST_03_AP_NBG')
        ]

        ausgabetabelle = (workspace_projekt_einnahmen,'GWST_04_Zuwachs')

        sql = """
                    SELECT GWST_03_AP_NBG.Jahr, 'AAAA' AS AGS, Sum([SummevonAnzahl]*GWSTGrundbetragProAPReferenzZielort*hebesatzProjektkommune/100) AS GWST_EUR INTO GWST_04_Zuwachs
                    FROM GWST_03_AP_NBG
                    GROUP BY GWST_03_AP_NBG.Jahr, 'AAAA'
                    ORDER BY GWST_03_AP_NBG.Jahr;
                    """

        sql = sql.replace("GWSTGrundbetragProAPReferenzZielort",str(GWSTGrundbetragProAPReferenzZielort)).replace("AAAA",ags).replace("hebesatzProjektkommune",hebesatzProjektkommune)
        mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)


        #############################################################################################################
        # Schritt 4
        schrittmeldung = 'Erzeuge GWST_05_Verlust \n'
        messages.AddMessage(schrittmeldung)
        print schrittmeldung

        # Erzeuge GWST_05_Verlust
        eingangstabellen = [
            (workspace_projekt_einnahmen,'GWST_01_Basisdaten'),
            (workspace_projekt_einnahmen,'GWST_03_AP_NBG'),
            (workspace_projekt_einnahmen,'AWU_WanderungsfaktorAP')

        ]

        ausgabetabelle = (workspace_projekt_einnahmen,'GWST_05_Verlust')

        sql = """
                    SELECT GWST_03_AP_NBG.Jahr, AWU_WanderungsfaktorAP.AGS, Sum(([SummevonAnzahl]*[AWU_Wanderungsfaktor]*[KAGWST3Jahre]/[AP2011])*-1) AS GWST_EUR INTO GWST_05_Verlust
                    FROM GWST_03_AP_NBG, AWU_WanderungsfaktorAP INNER JOIN GWST_01_Basisdaten ON AWU_WanderungsfaktorAP.AGS = GWST_01_Basisdaten.AGS
                    GROUP BY GWST_03_AP_NBG.Jahr, AWU_WanderungsfaktorAP.AGS;
                    """

        mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

        # INSERT GWST_05_Verlust into GWST_04_Zuwachs
        eingangstabellen = [
            (workspace_projekt_einnahmen,'GWST_04_Zuwachs'),
            (workspace_projekt_einnahmen,'GWST_05_Verlust')

        ]

        ausgabetabelle = (workspace_projekt_einnahmen,'GWST_04_Zuwachs')

        sql = """
                    INSERT INTO GWST_04_Zuwachs ( Jahr, AGS, GWST_EUR )
                    SELECT GWST_05_Verlust.Jahr, GWST_05_Verlust.AGS, GWST_05_Verlust.GWST_EUR
                    FROM GWST_05_Verlust;
                    """

        mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)


        #############################################################################################################
        # Schritt 4
        schrittmeldung = 'Erzeuge GWST_06_Summen \n'
        messages.AddMessage(schrittmeldung)
        print schrittmeldung

        # Erzeuge GWST_06_Summen
        eingangstabellen = [
            (workspace_projekt_einnahmen,'GWST_04_Zuwachs')
        ]

        ausgabetabelle = (workspace_projekt_einnahmen,'GWST_06_Bilanz')

        sql = """SELECT GWST_04_Zuwachs.AGS, GWST_04_Zuwachs.Jahr, Sum(GWST_04_Zuwachs.GWST_EUR) AS SummevonGWST_EUR INTO GWST_06_Bilanz
                    FROM GWST_04_Zuwachs
                    GROUP BY GWST_04_Zuwachs.AGS, GWST_04_Zuwachs.Jahr;
                    """

        mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

        #############################################################################################################
        # Schritt 6 - Datenexport in Excel-Datei
        schrittmeldung = 'Datenexport in Excel-Datei  \n'
        messages.AddMessage(schrittmeldung)
        print schrittmeldung

        # Pfade setzen
        logo = join((str(sys.path[0]).split("2 Planungsprojekte analysieren")[0]),"1_Basisdaten","logo_rpc.png")
        ausgabeordner = join(base_path,'3 Benutzerdefinierte Projekte',projektname,'Ergebnisausgabe','Excel')
        if not os.path.exists(ausgabeordner): os.makedirs(ausgabeordner)
        excelpfad = join(ausgabeordner,'Einnahmen_Gewerbesteuer.xlsx')

        try:
            os.remove(excelpfad)
        except:
            pass

        # Workbook und Tabellenbl??tter anlegen
        wb = xlsxwriter.Workbook(excelpfad)
        sl.infosheet(projektname, str("Gewerbesteuer").decode('utf-8'), wb)
        ws1 = wb.add_worksheet('Methodik')
        ws2 = wb.add_worksheet('Auswertungen')
        ws3 = wb.add_worksheet('Grafiken')
        ws4 = wb.add_worksheet('Rohdaten_Gewerbesteuer')
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

        ausgabetabelle = join(workspace_projekt_einnahmen,'GWST_06_Bilanz')

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
        methodik_grafik = join(base_path,"2_Tool","Einnahmen","Erlaeuterungstexte","Methodik_05_Gewerbesteuer.png")
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
        fields = ["AGS", "Jahr"]
        rows = arcpy.da.SearchCursor(ausgabetabelle, fields)
        for row in rows:
            AGSListe.append(row[0])

        rows = arcpy.da.SearchCursor(ausgabetabelle, fields)
        for row in rows:
            JahrListe.append(row[1])

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
                    formula = "=SUMIFS(Rohdaten_Gewerbesteuer!$D:$D,Rohdaten_Gewerbesteuer!$B:$B,Auswertungen!B"+str(i+5)+",Rohdaten_Gewerbesteuer!$C:$C,Auswertungen!"+alphabet[f+2]+"4)"
                    ws2.write_formula(i+4, f+2, formula, money)
                    i+=1
                except Exception as e:
                    print e
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
        chart.set_title({'name': 'Gewerbesteuer in Euro','name_font':  {'name': 'Tahoma', 'size': 9}})

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
            messages.AddMessage("Es liegt ein Fehler beim Speichern der Ausgabedatei vor. Ist diese ggf. noch geoeffnet?")
            messages.AddMessage(r)


        #############################################################################################################
        # Schritt 4
        schrittmeldung = 'temporaere Tabellen loeschen \n'
        messages.AddMessage(schrittmeldung)
        print schrittmeldung

        deleteList = []

        for e in deleteList:
            f = join(workspace_projekt_definition,e)
            try:
                arcpy.Delete_management(f)
            except:
                pass

        gc.collect()
        print "fertig"
        Message.AddMessage('05_Gewerbesteuer abgeschlossen')


#############################################################################################################
#
# Funktionen
#
#############################################################################################################

def ags_samtgemeinde(ags_in):
    base_path = str(sys.path[0]).split("2 Planungsprojekte analysieren")[0]
    workspace_basisdaten = self.folders.get_basedb('FGDB_Basisdaten_deutschland.gdb')

    VG250 = join(workspace_basisdaten,'VG250')
    where = '"AGS"'+" ='"+ ags_in + "'"

    rows = arcpy.SearchCursor(VG250, where)

    for row in rows:
        # Weiche f??r Bundesl??nder
        if ags_in[0:2] == "03":
            ags_sg = row.SN_L + row.SN_R + row.SN_K + row.SN_V1[1] + row.SN_V2 + row.SN_G

        elif ags_in[0:2] == "07":
            ags_sg = row.SN_L + row.SN_R + row.SN_K + row.SN_V2

        else:
            arcpy.AddMessage("Es trat ein Fehler in der Ermittlung der AGS der Samtgemeinde auf. Das Programm musste abgebrochen werden.")
            sys.exit()

    message = "AGS_SG ermittelt: " + ags_sg
    arcpy.AddMessage(message)
    return ags_sg


def ags_regionalschluessel(ags_in):
    base_path = str(sys.path[0]).split("2 Planungsprojekte analysieren")[0]
    workspace_basisdaten = self.folders.get_basedb('FGDB_Basisdaten_deutschland.gdb')

    VG250 = join(workspace_basisdaten,'VG250')
    where = '"AGS"'+" ='"+ ags_in + "'"
    fields = "RS"
    rows = arcpy.da.SearchCursor(VG250, fields, where)

    for row in rows:
        regionalschluessel = row[0]

    if regionalschluessel[2:] == "0000000000":
        regionalschluessel = regionalschluessel[0:2]

    return regionalschluessel


def getAnteilGWS(ags_input,jahr):
    query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags_input+"|jahr.text:"+str(jahr)

    #arcpy.AddMessage(query)

    queryresult = urllib2.urlopen(query)
    jsonContent = queryresult.read()
    data = json.loads(jsonContent)

    if len(data) == 0:

        ags_sg = ags_samtgemeinde(ags_input)
        query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags_sg+"|jahr.text:"+str(jahr)
        queryresult = urllib2.urlopen(query)
        jsonContent = queryresult.read()
        data = json.loads(jsonContent)

    AnteilGWS = int(data[0][u'stenw5'])
    return(AnteilGWS)


def getHebesatzGWS(ags_input,jahr):
    query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags_input+"|jahr.text:"+str(jahr)

    #arcpy.AddMessage(query)

    queryresult = urllib2.urlopen(query)
    jsonContent = queryresult.read()
    data = json.loads(jsonContent)

    if len(data) == 0:

        ags_sg = ags_samtgemeinde(ags_input)
        query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags_sg+"|jahr.text:"+str(jahr)
        queryresult = urllib2.urlopen(query)
        jsonContent = queryresult.read()
        data = json.loads(jsonContent)

    HebesatzGWS = int(data[0][u'stenw3'])

    return(HebesatzGWS)


def getAnzAP(ags_input):
    query = "http://api.regenesis.pudo.org/cube/13111gj001/facts?cut=gemein.name:"+str(ags_input)

    #arcpy.AddMessage(query)
    print query

    queryresult = urllib2.urlopen(query)
    jsonContent = queryresult.read()
    data = json.loads(jsonContent)

    if len(data) == 0:
        ags_sg = ags_samtgemeinde(ags_input)
        query = "http://api.regenesis.pudo.org/cube/13111gj001/facts?cut=gemein.name:"+str(ags_sg)
        queryresult = urllib2.urlopen(query)
        jsonContent = queryresult.read()
        data = json.loads(jsonContent)

    AnzAP = data[3][u'erw032']
    return(AnzAP)

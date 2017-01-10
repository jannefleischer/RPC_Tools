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
import xlsxwriter, urllib2, json
import time

def main(parameters, messages):
    
    sheetlibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','sheet_lib.py'))
    sl = imp.load_source('sheet_lib', sheetlibpath)
    
    mdblibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','tempmdb_lib.py'))
    mdb = imp.load_source('tempmdb_lib', mdblibpath)
    
    gc.collect()
    
    arcpy.env.overwriteOutput = True
    
    # Variablen definieren
    projektname = parameters[0].value
    
    #projektname = 'HCU_LKH_Brackel'
    
    #Pfade einrichten
    base_path = str(sys.path[0]).split("2_Tool")[0]
    workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb')
    workspace_projekt_einnahmen = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Einnahmen_'+projektname+'.gdb')
    
    projektRahmendaten = os.path.join(base_path ,"3_Projekte",  projektname ,"FGDB_Definition_Projekt_" + projektname +".gdb","Projektrahmendaten")
    projektFlaeche = os.path.join(base_path ,"3_Projekte",  projektname ,"FGDB_Definition_Projekt_" + projektname +".gdb","Teilflaechen_Plangebiet")
    kfa_01_jaehrlich = os.path.join(workspace_projekt_einnahmen, "KFA_01_Jahresdaten")
    kfa_02_statisch = os.path.join(workspace_projekt_einnahmen, "KFA_02_Statische_Daten")
    projektBevoelkerung = os.path.join(projektRahmendaten, "Einwohnerzahl")
    
    
    
    #############################################################################################################
    #Funktionen
    
    def getAGS(projektname):
        import arcpy,sys,os
        base_path = str(sys.path[0]).split("2_Tool")[0]
        projektFlaeche = os.path.join(base_path ,"3_Projekte",  projektname ,"FGDB_Definition_Projekt_" + projektname +".gdb","Teilflaechen_Plangebiet")
        bkg_gemeinden = os.path.join( base_path, "1_Basisdaten","FGBD_Basisdaten_deutschland.gdb","bkg_gemeinden")
        #ags aus BKG Daten extrahieren, dafür Gemeinde selektieren, die von Planfläche geschnitten wird
        #1. Feature Layer aus den bkg-daten erstellen
        try:
            arcpy.Delete_management("bkg_gemeinden_lyr")
        except:
            print""
        arcpy.MakeFeatureLayer_management(bkg_gemeinden,"bkg_gemeinden_lyr")
        #2.Spatial Select wo Planfläche vgm_lyr intersected
        arcpy.SelectLayerByLocation_management("bkg_gemeinden_lyr", "INTERSECT", projektFlaeche)
        #Wenn Flaeche = 1, ags extrahieren
        n = arcpy.GetCount_management("bkg_gemeinden_lyr").getOutput(0)
        print n
    
        if(int(n) == 1 ):
            gemeindeCursor = arcpy.SearchCursor("bkg_gemeinden_lyr")
            for gemeinde in gemeindeCursor:
                verbandsgemeinde = gemeinde.BEMERK
                ags = gemeinde.AGS
                RS = gemeinde.RS
    
        else:
            arcpy.AddMessage("Die Projektflaechen liegen innerhalb mehrerer Gemeinden, das Tool unterstuetzt zur Zeit keine interkommunalen Projekte.")
            ## TODO Dateien loeschen und Projektregistrierung loeschen)
            sys.exit()
    
        #Weiche nach Bundeslaendern und gemeinschaftsangehoerigen Gemeinden
        if verbandsgemeinde[0:3] != "gem":
            ags_vg = ""
            ags_regenesis = ags
    
        elif ags[0:2] == "03": #Niedersachsen
            print "NS"
            ags_vg = RS[0:5] + RS[9:]
            ags_regenesis = RS[0:5] + RS[6] + RS[7:]
            arcpy.AddMessage(ags_vg)
    
    
        elif ags[0:2] == "07": #Rheinland-Pfalz
            print "RP"
            ags_vg = RS[0:5] + RS[7:9]
            ags_regenesis = RS[0:5] + RS[7:]
            arcpy.AddMessage(ags_vg)
    
        return ags, ags_vg, ags_regenesis
    
    def ags_samtgemeinde(ags_in):
        base_path = str(sys.path[0]).split("2_Tool")[0]
        workspace_basisdaten = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb')
    
        VG250 = os.path.join(workspace_basisdaten,'VG250')
        where = '"AGS"'+" ='"+ ags_in + "'"
    
        rows = arcpy.SearchCursor(VG250, fields, where)
    
        for row in rows:
            ags_out = row.SN_L + row.SN_R + row.SN_K + row.SN_V1[1] + row.SN_V2 + row.SN_G
    
        return ags_out
    
    
    def getKreisfrei(ags):
        #kreisfrei = "ja" wenn die letzten drei Stellen der AGS Nullen sind
        if ags[-3:] == '000':
            kreisfrei = "1"
        else:
            kreisfrei = "0"
    
        return(kreisfrei)
    
    
    def getEWZ(ags_input):
        query = "http://www.statistik-portal.de/Statistik-Portal/gemeindeverz.asp?G="+ags_input
        try:
            queryresult = urllib2.urlopen(query).read()
            time.sleep(1)
            AnzHH = queryresult.split('<tr><th>Einwohner</th><td>')[1].split("</td></tr>")[0].replace('.','')
        except:
            AnzHH = 1
    
        time.sleep(0.2)
        return(AnzHH)
    
    
    def getAnzHH(ags_input):
        #TODO: Haushalte, nicht Einwohner!
    
        query = "http://www.statistik-portal.de/Statistik-Portal/gemeindeverz.asp?G="+ags_input
        try:
            queryresult = urllib2.urlopen(query).read()
            time.sleep(1)
            AnzHH = queryresult.split('<tr><th>Einwohner</th><td>')[1].split("</td></tr>")[0].replace('.','')
        except:
            AnzHH = 1
    
        time.sleep(0.2)
        return(AnzHH)
    
    
    def getHebesatzGrStA(ags_input):
        query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags_input+"|jahr.text:2012"
        queryresult = urllib2.urlopen(query)
        jsonContent = queryresult.read()
        data = json.loads(jsonContent)
    
        if data == []:
    
            ags = ags_samtgemeinde(ags_input)
    
            print "Es wird die AGS der Verwaltungsgemeinschaft verwendet: " + str(ags)
    
            query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags+"|jahr.text:2012"
            queryresult = urllib2.urlopen(query)
            jsonContent = queryresult.read()
            data = json.loads(jsonContent)
    
    
        HebesatzGrStA = data[0][u'stenw1']
    
        return(HebesatzGrStA)
    
    
    def getHebesatzGrStB(ags_input):
        query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags_input+"|jahr.text:2012"
        queryresult = urllib2.urlopen(query)
        jsonContent = queryresult.read()
        data = json.loads(jsonContent)
    
        if data == []:
            ags = ags_samtgemeinde(ags_input)
    
            print "Es wird die AGS der Verwaltungsgemeinschaft verwendet: " + str(ags)
    
            query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags+"|jahr.text:2012"
            queryresult = urllib2.urlopen(query)
            jsonContent = queryresult.read()
            data = json.loads(jsonContent)
    
        HebesatzGrStB = data[0][u'stenw2']
    
        return(HebesatzGrStB)
    
    
    def getHebesatzGewSt(ags_input):
        query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags_input+"|jahr.text:2012"
        queryresult = urllib2.urlopen(query)
        jsonContent = queryresult.read()
        data = json.loads(jsonContent)
    
        if data == []:
            ags = ags_samtgemeinde(ags_input)
    
            print "Es wird die AGS der Verwaltungsgemeinschaft verwendet: " + str(ags)
    
            query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags+"|jahr.text:2012"
            queryresult = urllib2.urlopen(query)
            jsonContent = queryresult.read()
            data = json.loads(jsonContent)
    
        HebesatzGewSt = data[0][u'stenw3']
    
        return(HebesatzGewSt)
    
    
    #############################################################################################################
    #
    # Beginne Hauptteil
    #
    #############################################################################################################
    
    sheetlibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','sheet_lib.py'))
    sl = imp.load_source('sheet_lib', sheetlibpath)
    
    mdblibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','tempmdb_lib.py'))
    mdb = imp.load_source('tempmdb_lib', mdblibpath)
    
    gc.collect()
    
    arcpy.env.overwriteOutput = True
    
    # Variablen definieren
    projektname = parameters[0].value
    
    #Pfade einrichten
    base_path = str(sys.path[0]).split("2_Tool")[0]
    
    workspace_basisdaten = os.path.join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb')
    workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb')
    workspace_projekt_einnahmen = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Einnahmen_'+projektname+'.gdb')
    workspace_tool_definition = os.path.join(base_path,"2_Tool","3_Art und Mass der Nutzung","FGDB_Definition_Projekt_Tool.gdb")
    workspace_tool_einnahmen = os.path.join(base_path,"2_Tool","B_Einnahmen","FGDB_Einnahmen_Tool.gdb")
    
    Teilflaechen_Plangebiet_Centroide = os.path.join(workspace_projekt_definition, "Teilflaechen_Plangebiet_Centroide")
    Teilflaechen_Plangebiet_CentroideGK3 = os.path.join(workspace_projekt_definition, "Teilflaechen_Plangebiet_CentroideGK3")
    gemeindenWirkraumEW_Centroide = os.path.join(workspace_projekt_definition,"gemeindenWirkraumEW_Centroide")
    gemeindenWirkraumAP_Centroide = os.path.join(workspace_projekt_definition,"gemeindenWirkraumAP_Centroide")
    
    #############################################################################################################
    # Vereinigungsmenge aus Umland erzeugen AGS aus EW und AP zusammen führen) inkl. eigene Kommune
    
    schrittmeldung = 'Vereinigungsmenge aus Umland erzeugen \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung
    
    # Erzeuge KFA_01_Wirkraum_temp
    eingangstabellen = [
        (workspace_projekt_einnahmen,'AWU_WanderungsfaktorAP')
    ]
    
    ausgabetabelle = (workspace_projekt_einnahmen,'KFA_01_Wirkraum_temp')
    
    sql = """SELECT AWU_WanderungsfaktorAP.AGS, AWU_WanderungsfaktorAP.AGS_VG, AWU_WanderungsfaktorAP.AGS_Regenesis INTO KFA_01_Wirkraum_temp
    FROM AWU_WanderungsfaktorAP
    GROUP BY AWU_WanderungsfaktorAP.AGS, AWU_WanderungsfaktorAP.AGS_VG, AWU_WanderungsfaktorAP.AGS_Regenesis;
    """
    
    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
    
    
    # Fuege Werte an  KFA_01_Wirkraum_temp an
    eingangstabellen = [
        (workspace_projekt_einnahmen,'KFA_01_Wirkraum_temp'),
        (workspace_projekt_einnahmen,'AWU_WanderungsfaktorEW')
    ]
    
    ausgabetabelle = (workspace_projekt_einnahmen,'KFA_01_Wirkraum_temp')
    
    sql = """INSERT INTO KFA_01_Wirkraum_temp ( AGS, AGS_VG, AGS_Regenesis )
    SELECT AWU_WanderungsfaktorEW.AGS, AWU_WanderungsfaktorEW.AGS_VG, AWU_WanderungsfaktorEW.AGS_Regenesis
    FROM AWU_WanderungsfaktorEW;
    """
    
    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
    
    # Fuege Werte an  KFA_01_Wirkraum_temp an
    eingangstabellen = [
        (workspace_projekt_einnahmen,'KFA_01_Wirkraum_temp')
    ]
    
    ausgabetabelle = (workspace_projekt_einnahmen,'KFA_01_Wirkraum')
    
    sql = """SELECT KFA_01_Wirkraum_temp.AGS, KFA_01_Wirkraum_temp.AGS_VG, KFA_01_Wirkraum_temp.AGS_Regenesis INTO KFA_01_Wirkraum
    FROM KFA_01_Wirkraum_temp
    GROUP BY KFA_01_Wirkraum_temp.AGS,KFA_01_Wirkraum_temp.AGS_VG, KFA_01_Wirkraum_temp.AGS_Regenesis
    ORDER BY KFA_01_Wirkraum_temp.AGS;
    """
    
    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
    
    # Erzeuge Tabelle KRU_01_Kreisumlagesaetze_Wirkraum
    
    #TODO: Tabelle KRU_01_Kreisumlagesaetze_Wirkraum
    #Spalte 1 AGS5 gruppieren und Filtern über kreisfrei anhand von Nullen der AGS
    #Spalte 2 "0" rein schreiben - Name der Spalte "Umlagensatz_in_vH" Double
    eingangstabellen = [
        (workspace_projekt_einnahmen,'KFA_01_Wirkraum')
    ]
    
    ausgabetabelle = (workspace_projekt_einnahmen,'KRU_01_Kreisumlagesaetze_Wirkraum')
    
    sql = """SELECT Left([AGS],5) AS AGS5 INTO KRU_01_Kreisumlagesaetze_Wirkraum FROM KFA_01_Wirkraum GROUP BY Left([AGS],5);"""
    
    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
    
    
    # Kreisfreie Kommunen entfernen durch Filterung auf 000 hinten in der AGS
    KRU_01_Kreisumlagesaetze_Wirkraum = os.path.join(workspace_projekt_einnahmen,'KRU_01_Kreisumlagesaetze_Wirkraum')
    arcpy.AddField_management(KRU_01_Kreisumlagesaetze_Wirkraum, "Umlagensatz_in_vH", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED")
    fields = "AGS5"
    rows = arcpy.da.UpdateCursor(KRU_01_Kreisumlagesaetze_Wirkraum, fields)
    for row in rows:
        AGS5 = row[0]
        if AGS5[-3:] == "000":
            rows.deleteRow()
    del rows
    
    
    #############################################################################################################
    # Schritt 2
    schrittmeldung = 'Tabelle KFA_02 erzeugen \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung
    
    kfa_02_statisch = os.path.join(workspace_projekt_einnahmen,'KFA_02_Statische_Daten')
    
    #Tabelle leeren
    arcpy.TruncateTable_management(kfa_02_statisch)
    
    KFA_01_Wirkraum = os.path.join(workspace_projekt_einnahmen,'KFA_01_Wirkraum')
    rows = arcpy.SearchCursor(KFA_01_Wirkraum)
    
    for row in rows:
        ags = row.AGS
        ags_vg = row.AGS_VG
        ags_regenesis = row.AGS_Regenesis
    
        arcpy.AddMessage(ags_regenesis)
    
        EWZ = getEWZ(ags)
        print "EWZ: " + str(EWZ)
    
        kreisfrei = getKreisfrei(ags) # zur Bestimmung der Kreisfreiheit wird die Original-AGS verwendet
        print "Kreisfrei: " + str(kreisfrei)
    
        HebesatzGrStA = getHebesatzGrStA(ags_regenesis)
        print "HebesatzGrStA: " + str(HebesatzGrStA)
    
        HebesatzGrStB = getHebesatzGrStB(ags_regenesis)
        print "HebesatzGrStB: " + str(HebesatzGrStB)
    
        HebesatzGewSt = getHebesatzGewSt(ags_regenesis)
        print "HebesatzGewSt: " + str(HebesatzGewSt)
    
        #Insert Values into Table "kfa_02_statisch"
        rows1 = arcpy.InsertCursor(kfa_02_statisch)
        row1 = rows1.newRow()
        row1.AGS = ags
        row1.AGS_VG = ags_vg
        row1.AGS_Regenesis = ags_regenesis
        row1.EW = int(EWZ)
        row1.HebGrStA = int(HebesatzGrStA)
        row1.HebGrStB = int(HebesatzGrStB)
        row1.HebGewSt = int(HebesatzGewSt)
        row1.Kreisfrei = int(kreisfrei)
        rows1.insertRow(row1)
    
        del row1, rows1
    
    del row, rows
    
    
    
    #############################################################################################################
    # Schritt 2
    schrittmeldung = '\nTabelle KFA_03_Jahresdaten erzeugen \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung
    
    KFA_03_Jahresdaten = os.path.join(workspace_projekt_einnahmen,'KFA_03_Jahresdaten')
    KFA_01_Wirkraum = os.path.join(workspace_projekt_einnahmen,'KFA_01_Wirkraum')
    
    #Tabelle leeren
    arcpy.TruncateTable_management(KFA_03_Jahresdaten)
    
    # Betrachtungszeitraum ermitteln
    rows = arcpy.SearchCursor(projektRahmendaten)
    for row in rows:
        beginnZeitraum = int(row.Beginn_Betrachtungszeitraum)
        endeZeitraum = int(row.Ende_Betrachtungszeitraum)
    del row, rows
    
    # Iteration ueber Betrachtungszeitraum und fuellen der Tabelle mit Nullwerten
    jahre = endeZeitraum - beginnZeitraum
    rows_out = arcpy.InsertCursor(KFA_03_Jahresdaten)
    
    for i in range(0,jahre+1):
    
        rows_in = arcpy.SearchCursor(KFA_01_Wirkraum)
    
        for gemeinde in rows_in:
    
            ags = gemeinde.AGS
            ags_vg = gemeinde.AGS_VG
            ags_regenesis = gemeinde.AGS_Regenesis
    
            row_out = rows_out.newRow()
            row_out.Jahr = i + beginnZeitraum
            row_out.AGS = ags
            row_out.AGS_VG = ags_vg
            row_out.AGS_Regenesis = ags_regenesis
    
            row_out.DeltaEW = 0
            row_out.DeltaGrSt = 0
            row_out.DeltaGewSt = 0
            row_out.DeltaUmsSt = 0
            row_out.DeltaEinkSt = 0
            row_out.DeltaFaLeiA = 0
    
            rows_out.insertRow(row_out)
            del row_out
    
    del rows_out
    
    
    #####################################################################
    schrittmeldung = ' - Delta Einwohner'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung
    
    eingangstabellen = [
        (workspace_projekt_einnahmen,'AWU_WanderungsfaktorEW'),
        (workspace_projekt_definition,'Einwohnerzahl'),
        (workspace_projekt_einnahmen,'KFA_03_Jahresdaten'),
    ]
    
    ausgabetabelle = (workspace_projekt_einnahmen,'KFA_03_Jahresdaten_temp')
    
    sql = """SELECT KFA_03_Jahresdaten.Jahr, KFA_03_Jahresdaten.AGS, KFA_03_Jahresdaten.AGS_VG, KFA_03_Jahresdaten.AGS_Regenesis,  ([Einwohnerzahl]*[AWU_Wanderungsfaktor])*-1 AS DeltaEW, KFA_03_Jahresdaten.DeltaGrSt, KFA_03_Jahresdaten.DeltaGewSt, KFA_03_Jahresdaten.DeltaUmsSt, KFA_03_Jahresdaten.DeltaEinkSt, KFA_03_Jahresdaten.DeltaFaLeiA INTO KFA_03_Jahresdaten_temp
    FROM (KFA_03_Jahresdaten LEFT JOIN AWU_WanderungsfaktorEW ON KFA_03_Jahresdaten.AGS = AWU_WanderungsfaktorEW.AGS) LEFT JOIN Einwohnerzahl ON KFA_03_Jahresdaten.Jahr = Einwohnerzahl.Jahr;
    """
    
    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
    
    #DeltwEinwohner aufsummieren
    eingangstabellen = [
        (workspace_projekt_einnahmen,'KFA_03_Jahresdaten_temp')
        ]
    
    ausgabetabelle = (workspace_projekt_einnahmen,'KFA_03_Jahresdaten')
    
    sql = """SELECT KFA_03_Jahresdaten_temp.Jahr, KFA_03_Jahresdaten_temp.AGS, KFA_03_Jahresdaten_temp.AGS_VG, KFA_03_Jahresdaten_temp.AGS_Regenesis, Sum(KFA_03_Jahresdaten_temp.DeltaEW) AS DeltaEW, Sum(KFA_03_Jahresdaten_temp.DeltaGrSt) AS DeltaGrSt, Sum(KFA_03_Jahresdaten_temp.DeltaGewSt) AS DeltaGewSt, Sum(KFA_03_Jahresdaten_temp.DeltaUmsSt) AS DeltaUmsSt, Sum(KFA_03_Jahresdaten_temp.DeltaEinkSt) AS DeltaEinkSt, Sum(KFA_03_Jahresdaten_temp.DeltaFaLeiA) AS DeltaFaLeiA INTO KFA_03_Jahresdaten
    FROM KFA_03_Jahresdaten_temp
    GROUP BY KFA_03_Jahresdaten_temp.Jahr, KFA_03_Jahresdaten_temp.AGS, KFA_03_Jahresdaten_temp.AGS_VG, KFA_03_Jahresdaten_temp.AGS_Regenesis;
    """
    
    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
    
    
    #Nullwerte von Delta-Einwohner auf 0 setzen
    
    KFA_03_Jahresdaten = os.path.join(workspace_projekt_einnahmen,'KFA_03_Jahresdaten')
    where_clause = '"DeltaEW" IS NULL'
    cur = arcpy.UpdateCursor(KFA_03_Jahresdaten, where_clause)
    
    for row in cur:
        row.DeltaEW = 0
        cur.updateRow(row)
    
    try:
        del row, cur
    except:
        pass
    
    #DeltaEinwohner eigene Kommune addieren
    ags = getAGS(projektname)[0]
    
    eingangstabellen = [(workspace_projekt_definition,'Einwohnerzahl')]
    
    ausgabetabelle = (workspace_projekt_einnahmen,'KFA_Bevoelkerung_temp')
    
    sql = """SELECT Einwohnerzahl.Jahr, Sum(Einwohnerzahl.Einwohnerzahl) AS EW INTO KFA_Bevoelkerung_temp
    FROM Einwohnerzahl
    GROUP BY Einwohnerzahl.Jahr;
    """
    
    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
    
    KFA_Bevoelkerung_temp = os.path.join(workspace_projekt_einnahmen,'KFA_Bevoelkerung_temp')
    
    fields = ['EW','Jahr']
    cursor = arcpy.da.SearchCursor(KFA_Bevoelkerung_temp, fields)
    for row in cursor:
        ew = row[0]
        jahr = row[1]
    
        where_clause = '"Jahr"= ' + str(jahr) + " AND AGS = '" + ags + "'"
    
        rows_update = arcpy.UpdateCursor(KFA_03_Jahresdaten,where_clause)
        for row_update in rows_update:
            row_update.setValue("DeltaEW", row_update.getValue("DeltaEW") + ew)
            rows_update.updateRow(row_update)
    
        try:
            del rows_update, row_update, where_clause
        except:
            pass
    
    del cursor, row
    
    
    ##rows_bev = arcpy.SearchCursor(KFA_Bevoelkerung_temp)
    ##
    ##for row_bev in rows_bev:
    ##    ew = row_bev.EW
    ##    jahr = row_bev.Jahr
    ##
    ##    where_clause = '"Jahr"= ' + str(jahr) + " AND AGS = '" + ags + "'"
    ##
    ##    rows_update = arcpy.UpdateCursor(KFA_03_Jahresdaten,where_clause)
    ##    for row_update in rows_update:
    ##        row_update.setValue("DeltaEW", row_update.getValue("DeltaEW") + ew)
    ##        rows_update.updateRow(row_update)
    ##try:
    ##    del rows_update, row_update, rows_bev, row_bev
    ##except:
    ##    pass
    
    
    #####################################################################
    schrittmeldung = ' - Delta Grundsteuer'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung
    
    GRST_Grundsteuereinnahmen = os.path.join(workspace_projekt_einnahmen,'GRST_Grundsteuereinnahmen')
    
    fields = ['GrStEinnahmen','Jahr']
    cursor = arcpy.da.SearchCursor(GRST_Grundsteuereinnahmen, fields)
    for row in cursor:
        GrStEinnahmen = row[0]
        jahr = row[1]
    
        updateFields = ['DeltaGrSt']
        where_clause = '"Jahr"= ' + str(jahr) + " AND AGS = '" + ags + "'"
        updateCursor = arcpy.da.UpdateCursor(KFA_03_Jahresdaten, updateFields, where_clause)
        for updateRow in updateCursor:
            updateRow[0] = GrStEinnahmen
            updateCursor.updateRow(updateRow)
    
    
    #####################################################################
    schrittmeldung = ' - Delta Gewerbesteuer'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung
    
    GWST_06_Bilanz = os.path.join(workspace_projekt_einnahmen,'GWST_06_Bilanz')
    
    fields = ['SummevonGWST_EUR','Jahr', 'AGS']
    cursor = arcpy.da.SearchCursor(GWST_06_Bilanz, fields)
    for row in cursor:
        GWST = row[0]
        jahr = row[1]
        ags = row[2]
    
        updateFields = ['DeltaGewSt']
        where_clause = '"Jahr"= ' + str(jahr) + " AND AGS = '" + ags + "'"
        updateCursor = arcpy.da.UpdateCursor(KFA_03_Jahresdaten, updateFields, where_clause)
        for updateRow in updateCursor:
            updateRow[0] = GWST
            updateCursor.updateRow(updateRow)
    
    
    #####################################################################
    schrittmeldung = ' - Delta Einkommensteuer'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung
    
    EKST_06_Bilanz = os.path.join(workspace_projekt_einnahmen,'EKST_06_Bilanz')
    
    fields = ['Bilanz_EST_EUR','Betrachtungsjahr','AGS']
    cursor = arcpy.da.SearchCursor(EKST_06_Bilanz, fields)
    for row in cursor:
        EKST = row[0]
        jahr = row[1]
        ags = row[2]
    
        updateFields = ['DeltaEinkSt']
        where_clause_update = '"Jahr"= ' + str(jahr) + " AND AGS = '" + ags + "'"
        updateCursor = arcpy.da.UpdateCursor(KFA_03_Jahresdaten, updateFields, where_clause_update)
    
        for updateRow in updateCursor:
            updateRow[0] = EKST
            updateCursor.updateRow(updateRow)
    
    
    #####################################################################
    schrittmeldung = ' - Delta Familienleistungsausgleich \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung
    
    FLA_01_Ergebnis = os.path.join(workspace_projekt_einnahmen,'FLA_01_Ergebnis')
    
    fields = ['FLA_Euro','Betrachtungsjahr','AGS']
    cursor = arcpy.da.SearchCursor(FLA_01_Ergebnis, fields)
    for row in cursor:
        FLA = row[0]
        jahr = row[1]
        ags = row[2]
    
        updateFields = ['DeltaFaLeiA']
        where_clause_update = '"Jahr"= ' + str(jahr) + " AND AGS = '" + ags + "'"
        updateCursor = arcpy.da.UpdateCursor(KFA_03_Jahresdaten, updateFields, where_clause_update)
    
        for updateRow in updateCursor:
            updateRow[0] = FLA
            updateCursor.updateRow(updateRow)
    
    #####################################################################
    schrittmeldung = 'Berechne Steuerkraftmesszahl \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung
    
    #Erstelle leere Tabelle KFA_03_Jahresdaten
    eingangstabellen = [
        (workspace_projekt_einnahmen,'KFA_03_Jahresdaten'),
        (workspace_projekt_einnahmen,'KFA_02_Statische_Daten')
    ]
    
    ausgabetabelle = (workspace_projekt_einnahmen,'KFA_03_Steuerkraftmesszahl')
    
    sql = """SELECT KFA_03_Jahresdaten.AGS, KFA_03_Jahresdaten.AGS_VG, KFA_03_Jahresdaten.AGS_Regenesis, KFA_03_Jahresdaten.Jahr, KFA_02_Statische_Daten.EW AS EW_Referenz, KFA_02_Statische_Daten.HebGrStA, KFA_02_Statische_Daten.HebGrStB, KFA_02_Statische_Daten.HebGewSt, KFA_03_Jahresdaten.DeltaEW, KFA_03_Jahresdaten.DeltaGrST, KFA_03_Jahresdaten.DeltaGewSt, KFA_03_Jahresdaten.DeltaUmsSt, KFA_03_Jahresdaten.DeltaEinkSt, KFA_03_Jahresdaten.DeltaFaLeiA, KFA_02_Statische_Daten.Kreisfrei INTO KFA_03_Steuerkraftmesszahl
    FROM KFA_03_Jahresdaten INNER JOIN KFA_02_Statische_Daten ON KFA_03_Jahresdaten.AGS = KFA_02_Statische_Daten.AGs;
    """
    
    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
    
    KFA_03_Steuerkraftmesszahl = os.path.join(workspace_projekt_einnahmen,'KFA_03_Steuerkraftmesszahl')
    
    arcpy.AddField_management(KFA_03_Steuerkraftmesszahl, "deltaSKMZ", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED")
    arcpy.AddField_management(KFA_03_Steuerkraftmesszahl, "Ausgleichsfaktor", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED")
    arcpy.AddField_management(KFA_03_Steuerkraftmesszahl, "Grundbetrag", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED")
    arcpy.AddField_management(KFA_03_Steuerkraftmesszahl, "Faktor_Zuweisungen_KU", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED")
    
    
    fields = ['AGS','Jahr','EW_Referenz','Kreisfrei','HebGrStA','HebGrStB','HebGewSt','DeltaGrST','DeltaGewSt','DeltaUmsSt','DeltaEinkSt','DeltaFaLeiA']
    cursor = arcpy.da.SearchCursor(KFA_03_Steuerkraftmesszahl, fields)
    for row in cursor:
        ags = row[0]
        jahr = row[1]
        EW_Referenz = row[2]
        kreisfrei = row[3]
        HebGrStA = row[4]
        HebGrStB = row[5]
        HebGewSt = row[6]
        DeltaGrST = row[7]
        DeltaGewSt = row[8]
        DeltaUmsSt = row[9]
        DeltaEinkSt = row[10]
        DeltaFaLeiA = row[11]
    
        KFA_Rahmendaten = os.path.join(workspace_tool_einnahmen,'KFA_Rahmendaten')
    
        if kreisfrei == 1:
            where_clause = '"Kreisfrei"= 1 AND "AGS_Land" = ' + "'" + ags[:2] + "' AND "+ '"Einwohner_von" <=' + str(EW_Referenz)+ " AND "+ '"Einwohner_bis" >='+str(EW_Referenz)
        else:
            where_clause = '"Kreisangehoerig"= 1 AND "AGS_Land" = ' + "'" + ags[:2] + "' AND "+ '"Einwohner_von" <=' + str(EW_Referenz)+ " AND "+ '"Einwohner_bis" >='+str(EW_Referenz)
    
        fields = [
        'Grundbetrag','Ausgleichsfaktor','Nivellierter_Hebesatz_GrSt_B','Faktor_Grundsteuer_B',
        'Nivellierter_Hebesatz_GewSt_netto','Faktor_Gewerbesteuer','Faktor_Umsatzsteuer',
        'Faktor_Anteil_Einkommensteuer','Faktor_Familienleistungsausgleich',
        'Faktor_Zuweisungen_in_Kreisumlage']
    
        cursor = arcpy.da.SearchCursor(KFA_Rahmendaten, fields, where_clause)
        for row in cursor:
            grundbetrag = row[0]
            ausgleichsfaktor = row[1]
            Nivellierter_Hebesatz_GrSt_B = row[2]
            Faktor_Grundsteuer_B = row[3]
            Nivellierter_Hebesatz_GewSt_netto = row[4]
            Faktor_Gewerbesteuer = row[5]
            Faktor_Umsatzsteuer = row[6]
            Faktor_Anteil_Einkommensteuer = row[7]
            Faktor_Familienleistungsausgleich = row[8]
            Faktor_Zuweisungen_in_Kreisumlage = row[9]
    
        deltaSKMZ = DeltaGrST/HebGrStB*Nivellierter_Hebesatz_GrSt_B*Faktor_Grundsteuer_B+DeltaGewSt/HebGewSt*Nivellierter_Hebesatz_GewSt_netto*Faktor_Gewerbesteuer+DeltaUmsSt*Faktor_Umsatzsteuer+DeltaEinkSt*Faktor_Anteil_Einkommensteuer+DeltaFaLeiA*Faktor_Familienleistungsausgleich
    
        updateFields = ['deltaSKMZ','Grundbetrag','Ausgleichsfaktor','Faktor_Zuweisungen_KU']
        where_clause_update = '"AGS"= '+"'"+ ags +"'"+' AND "Jahr" = '+str(jahr)
        updateCursor = arcpy.da.UpdateCursor(KFA_03_Steuerkraftmesszahl, updateFields, where_clause_update)
    
        for updateRow in updateCursor:
            updateRow[0] = deltaSKMZ
            updateRow[1] = grundbetrag
            updateRow[2] = ausgleichsfaktor
            updateRow[3] = Faktor_Zuweisungen_in_Kreisumlage
            updateCursor.updateRow(updateRow)
    
    #####################################################################
    schrittmeldung = 'Berechne Veredelungsfaktor je Gemeinde \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung
    
    eingangstabellen = [
        (workspace_tool_einnahmen,'KFA_Veredelungsfaktor'),
        (workspace_projekt_einnahmen,'KFA_02_Statische_Daten')
    ]
    
    ausgabetabelle = (workspace_projekt_einnahmen,'KFA_Veredelung_temp')
    
    sql = """SELECT Left([AGs],2) AS AGS_2, KFA_02_Statische_Daten.AGS, KFA_02_Statische_Daten.AGS_VG, KFA_02_Statische_Daten.AGS_Regenesis, KFA_02_Statische_Daten.EW, KFA_02_Statische_Daten.Kreisfrei INTO KFA_Veredelung_temp
    FROM KFA_02_Statische_Daten;
    """
    
    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
    
    
    #Veredelungsfaktor je Gemeinde erzeugen
    KFA_04_VeredelungsfaktorenGemeinden = os.path.join(workspace_projekt_einnahmen,'KFA_04_VeredelungsfaktorenGemeinden')
    arcpy.TruncateTable_management(KFA_04_VeredelungsfaktorenGemeinden)
    
    KFA_02_Statische_Daten = os.path.join(workspace_projekt_einnahmen,'KFA_02_Statische_Daten')
    
    fields = ['AGS','AGS_VG','EW']
    cursor = arcpy.da.SearchCursor(KFA_02_Statische_Daten, fields)
    for row in cursor:
        ags = row[0]
        ags_vg = row[1]
        ewz = int(row[2])
    
        dataset = []
    
        fields1 = ['Stuetzwert_EWZ','Stuetzwert_Veredelungsfaktor']
        table = os.path.join(workspace_tool_einnahmen,'KFA_Veredelungsfaktor')
        where = '"AGS_Land"'+" ='"+ ags[:2] + "'"
    
        cursor2 = arcpy.da.SearchCursor(table, fields1, where)
        for row2 in cursor2:
            ew = row2[0]
            vf = row2[1]
            werte = (ew, vf)
            dataset.append(werte)
    
        #Werte nach Einwohnerzahl aufsteigend sortieren
        dataset.sort(key=lambda x: x[0])
    
        #nächsten Wert zur aktuellen Einwohnerzahl finden
        closest_value = min(dataset, key=lambda x:abs(x[0]-ewz))
        index = dataset.index(closest_value)
    
        #Steigung berechnen
        if closest_value[0]<ewz:
            index_min = index
            index_max = index+1
        else:
            index_min = index-1
            index_max = index
    
        p1 = dataset[index_min]
        p2 = dataset[index_max]
    
        s = (p2[1]-p1[1])/(p2[0]-p1[0])
    
        #Veredelungsfaktor berechnen
        vf = p1[1]+(ewz-p1[0])*s
    
        cur_vf = arcpy.InsertCursor(KFA_04_VeredelungsfaktorenGemeinden)
        row = cur_vf.newRow()
        row.AGS = str(ags)
        row.AGS_VG = str(ags_vg)
        row.EWZ = int(ewz)
        row.VeredelungsFaktor = float(vf)
        cur_vf.insertRow(row)
    
    
    #####################################################################
    schrittmeldung = 'Berechne KFA_05_Zuweisungen \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung
    
    eingangstabellen = [
        (workspace_projekt_einnahmen,'KFA_03_Steuerkraftmesszahl'),
        (workspace_projekt_einnahmen,'KFA_04_VeredelungsfaktorenGemeinden')
    ]
    
    ausgabetabelle = (workspace_projekt_einnahmen,'KFA_05_Zuweisungen')
    
    sql = """SELECT KFA_03_Steuerkraftmesszahl.AGS, KFA_03_Steuerkraftmesszahl.AGS_VG, KFA_03_Steuerkraftmesszahl.AGS_Regenesis, KFA_03_Steuerkraftmesszahl.Jahr, [DeltaEW]*[VeredelungsFaktor]*[Grundbetrag] AS deltaBedarf, KFA_03_Steuerkraftmesszahl.deltaSKMZ, [DeltaEW]*[VeredelungsFaktor]*[Grundbetrag]-[deltaSKMZ] AS deltaBedarf_minus_deltaSteuerkraft, ([deltaEW]*[Veredelungsfaktor]*[Grundbetrag]-[deltaSKMZ])*[Ausgleichsfaktor] AS Zuweisungen, KFA_03_Steuerkraftmesszahl.Faktor_Zuweisungen_KU INTO KFA_05_Zuweisungen
    FROM KFA_03_Steuerkraftmesszahl INNER JOIN KFA_04_VeredelungsfaktorenGemeinden ON KFA_03_Steuerkraftmesszahl.AGS = KFA_04_VeredelungsfaktorenGemeinden.AGS
    ORDER BY KFA_03_Steuerkraftmesszahl.AGS, KFA_03_Steuerkraftmesszahl.Jahr;
    """
    
    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)
    
    #############################################################################################################
    # Schritt 6 - Datenexport in Excel-Datei
    schrittmeldung = 'Datenexport in Excel-Datei  \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung
    
    # Pfade setzen
    logo = os.path.join((str(sys.path[0]).split("2_Tool")[0]),"1_Basisdaten","logo_rpc.png")
    ausgabeordner = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Excel')
    if not os.path.exists(ausgabeordner): os.makedirs(ausgabeordner)
    excelpfad = os.path.join(ausgabeordner,'Einnahmen_Kommunaler_Finanzausgleich.xlsx')
    
    try:
        os.remove(excelpfad)
    except:
        pass
    
    # Workbook und Tabellenblätter anlegen
    wb = xlsxwriter.Workbook(excelpfad)
    sl.infosheet(projektname, str("Kommunaler Finanzausgleich").decode('utf-8'), wb)
    ws1 = wb.add_worksheet('Methodik')
    ws2 = wb.add_worksheet('Auswertungen')
    ws3 = wb.add_worksheet('Grafiken')
    ws4 = wb.add_worksheet('Rohdaten_KFA')
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
    
    ausgabetabelle = os.path.join(workspace_projekt_einnahmen,'KFA_05_Zuweisungen')
    
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
    ws4.set_column('A:A', 9, normal)
    ws4.set_column('B:B', 9, normal)
    ws4.set_column('C:C', 16, normal)
    ws4.set_column('D:D', 12, money)
    ws4.set_column('E:E', 12, money)
    ws4.set_column('F:F', 35, money)
    ws4.set_column('G:G', 12, money)
    ws4.set_column('G:G', 25, money)
    ws4.set_column('H:H', 16, normal)
    
    ################################
    #Methodikblatt einfuegen
    methodik_grafik = os.path.join(base_path,"2_Tool","B_Einnahmen","Erlaeuterungstexte","Methodik_06_KFA.png")
    ws1.insert_image('B2', methodik_grafik, {'x_scale': 0.6, 'y_scale': 0.6}) #Korrigiert Verzerrung die bei 1x1 auftritt
    
    ################################
    #Haftungsausschluss einfuegen
    haftung_grafik = os.path.join(base_path,"2_Tool","B_Einnahmen","Erlaeuterungstexte","Haftungsausschluss.png")
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
                formula = "=SUMIFS(Rohdaten_KFA!$I:$I,Rohdaten_KFA!$B:$B,Auswertungen!B"+str(i+5)+",Rohdaten_KFA!$E:$E,Auswertungen!"+alphabet[f+2]+"4)"
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
    chart.set_title({'name': 'Kommunaler Finanzausgleich in Euro','name_font':  {'name': 'Tahoma', 'size': 9}})
    
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
    
    deleteList = ['KFA_01_Wirkraum_temp','KFA_03_Jahresdaten_temp','KFA_Bevoelkerung_temp','KFA_Veredelung_temp','KFA_01_Wirkraum_temp','KFA_03_Jahresdaten_temp','KRU_01_Kreisumlagesaetze_Wirkraum_temp']
    
    for e in deleteList:
        f = os.path.join(workspace_projekt_einnahmen,e)
        try:
            arcpy.Delete_management(f)
        except:
            pass
    
    gc.collect()
    print "fertig"
    arcpy.AddMessage('06_Kommunaler Finanzausgleich abgeschlossen')
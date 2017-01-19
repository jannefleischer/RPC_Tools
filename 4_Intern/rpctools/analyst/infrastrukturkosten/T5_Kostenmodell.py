# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 10_Kostenmodell.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# GGR Planung
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


# Import arcpy modules
import arcpy, os, inspect, pyodbc, shutil, gc, sys, datetime, xlsxwriter, imp
from xlsxwriter.utility import xl_rowcol_to_cell

def main(parameters, messages):

    sheetlibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','sheet_lib.py'))
    sl = imp.load_source('sheet_lib', sheetlibpath)

    mdblibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','tempmdb_lib.py'))
    mdb = imp.load_source('tempmdb_lib', mdblibpath)

    gc.collect()

    arcpy.env.overwriteOutput = True


    #-----------------------
    #Kostenaufteilungsregeln speichern
    #-----------------------

    projektname = parameters[0].valueAsText

    i=7
    #"01 Planungskosten"
    i+=1 ; KB1_KP1 = parameters[i].valueAsText

    #"02 Grün-, Ausgleichs- und Ersatzflächen"
    i+=1 ; KB2_KP1 = parameters[i].valueAsText
    i+=1 ; KB2_KP2 = parameters[i].valueAsText
    i+=1 ; KB2_KP3 = parameters[i].valueAsText

    #"03 Innere Verkehrserschliessung"
    i+=1 ; KB3_KP1 = parameters[i].valueAsText
    i+=1 ; KB3_KP2 = parameters[i].valueAsText
    i+=1 ; KB3_KP3 = parameters[i].valueAsText

    #"04 Äußere Verkehrserschliessung"
    i+=1 ; KB4_KP1 = parameters[i].valueAsText
    i+=1 ; KB4_KP2 = parameters[i].valueAsText
    i+=1 ; KB4_KP3 = parameters[i].valueAsText

    #"05 Wasserversorgung"
    i+=1 ; KB5_KP1 = parameters[i].valueAsText
    i+=1 ; KB5_KP2 = parameters[i].valueAsText
    i+=1 ; KB5_KP3 = parameters[i].valueAsText

    #"06 Abwasserentsorgung"
    i+=1 ; KB6_KP1 = parameters[i].valueAsText
    i+=1 ; KB6_KP2 = parameters[i].valueAsText
    i+=1 ; KB6_KP3 = parameters[i].valueAsText

    #"07 Lärmschutz"
    i+=1 ; KB7_KP1 = parameters[i].valueAsText
    i+=1 ; KB7_KP2 = parameters[i].valueAsText


    base_path = str(sys.path[0]).split("2_Tool")[0]
    kosten_tool = os.path.join(base_path,'2_Tool',"A_Infrastrukturkosten","FGDB_Kosten_Tool.gdb")
    kosten_projekt = os.path.join(base_path,'3_Projekte',projektname,"FGDB_Kosten_"+projektname+".gdb")

    tablepath_costrules_project = os.path.join(kosten_projekt,'Projektspez_Kostenauft')

    kostenbereiche = [('01 - Planungsaufwand',1),('02 - Gruen-, Ausgleichs- und Ersatzflaechen',2),('03 - Innere Verkehrserschliessung',3),('04 - Aeussere Verkehrserschliessung',4),('05 - Wasserversorgung',5),('06 - Abwasserentsorgung',6),('07 - Laermschutz',7),('08 - Zusatzkosten',8)]
    kostenphasen = [('1 - Erstmalige Herstellung',1),('2 - Betrieb und Unterhaltung',2),('3 - Erneuerung',3)]

    for kostenbereich in kostenbereiche:

        kb_name = kostenbereich[0]
        kb = kostenbereich[1]

        for kostenphase in kostenphasen:

            try:

                kp_name = kostenphase[0]
                kp = kostenphase[1]

                rows = arcpy.UpdateCursor(tablepath_costrules_project, "", "", "","")

                for row in rows:
                    if row.Kostenbereich == kb_name and row.Kostenphase == kp_name:
                        ziel = "KB"+str(kb)+"_"+"KP"+str(kp)
                        ziel_value = eval(ziel)

                        messages.AddMessage(row.Kostenbereich + row.Kostenphase + ": " + ziel_value)

                        row.Kostenaufteilungsregel = ziel_value
                        rows.updateRow(row)

                del rows, row
            except Exception as e:
                messages.AddMessage(e)

    #-----------------------


    # Variablen definieren
    i=-1
    i+=1;projektname = parameters[i].valueAsText
    i+=1;sonderkostenfaktor = (float(parameters[i].valueAsText)+100)/100
    i+=1;entwaesserungssystem = parameters[i].valueAsText
    i+=1;rueckhaltebecken_typ = parameters[i].valueAsText
    i+=1;rueckhaltebecken_m3 = parameters[i].valueAsText
    i+=1;zus_kanalmeter = parameters[i].valueAsText

    i+=1;zus_herstellungskosten = parameters[i].valueAsText
    i+=1;zus_betriebskosten = parameters[i].valueAsText

    #Pfade einrichten
    base_path = str(sys.path[0]).split("2_Tool")[0]

    workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb')
    workspace_projekt_kosten = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Kosten_'+projektname+'.gdb')
    workspace_tool_kosten = os.path.join(base_path,"2_Tool","A_Infrastrukturkosten","FGDB_Kosten_Tool.gdb")

    flaechenbilanz_planung = os.path.join(workspace_projekt_definition,'Flaechenbilanz')
    flaechenbilanz_planung_gruppiert = os.path.join(workspace_projekt_definition,'Flaechenbilanz_gruppiert')
    element_und_preisliste = os.path.join(workspace_tool_kosten,'T03MEG_Element_und_Preisliste')
    infrastrukturmenge = os.path.join(workspace_projekt_kosten,"MEG_Mengenermittlung")
    teilflaechenlayer = os.path.join(workspace_projekt_definition,'Teilflaechen_Plangebiet')
    projektrahmendaten = os.path.join(workspace_projekt_definition,'projektrahmendaten')

    #Update Sonderkostenfaktor in Projektrahmendaten
    cursor = arcpy.UpdateCursor(projektrahmendaten)
    for row in cursor:
        row.PROJEKTSPEZIFISCHER_SONDERKOSTENFAKTOR = sonderkostenfaktor
        cursor.updateRow(row)


    #############################################################################################################
    #
    # Durchlauf Mengenermittlung
    #
    #############################################################################################################
    beginmeldung = 'Starte Mengenermittlung \n'
    messages.AddMessage(beginmeldung)
    print beginmeldung
    #############################################################################################################
    # Schritt 1 - Aggregiere Teilflaechen nach Flaechentypen
    schrittmeldung = 'Aggregiere Teilflaechen nach Flaechentypen \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung

    eingangstabellen = [
        (workspace_projekt_definition,'Flaechenbilanz')
    ]

    ausgabetabelle = (workspace_projekt_definition,'Flaechenbilanz_gruppiert')

    sql = """SELECT Flaechenbilanz.Teilflaeche_Plangebiet,Flaechenbilanz.Startjahr, Flaechenbilanz.Flaechennutzung_S1, Flaechenbilanz.Flaechennutzung_S2, Sum(Flaechenbilanz.Flaeche_ha) AS Flaeche_ha
                INTO Flaechenbilanz_gruppiert
                FROM Flaechenbilanz
                GROUP BY Flaechenbilanz.Teilflaeche_Plangebiet, Flaechenbilanz.Startjahr, Flaechenbilanz.Flaechennutzung_S1, Flaechenbilanz.Flaechennutzung_S2;
                """

    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    #############################################################################################################
    # Schritt 2 - Erzeuge Elementmengen
    schrittmeldung = 'Erzeuge Elementmengen \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung

    import ast #string to python parser - wird weiter unten gebraucht
    import sets

    #erzeuge Zieltabelle

    template = os.path.join(workspace_tool_kosten,"T01MEG_Template_Mengenermittlung")

    arcpy.CreateTable_management(workspace_projekt_kosten, "MEG_Mengenermittlung", template, "")

    #erzeuge eine liste aller teilflaechen und loesche duplikate
    teilflaechen_plangebiet = arcpy.SearchCursor(flaechenbilanz_planung_gruppiert, "", "","")

    teilflaechen = []

    for t in teilflaechen_plangebiet:
        teilflaeche = t.Teilflaeche_Plangebiet
        teilflaechen.append(teilflaeche)

    teilflaechen = set(teilflaechen)

    #iteriere durch die teilflaechen und starte eigentliche mengenerzeugung

    for t in teilflaechen:
        teilflaeche = t
        where_clause = """"Name" ='"""+teilflaeche+"'"
        teilflaechenabfrage = arcpy.SearchCursor(teilflaechenlayer, where_clause, "", "","")

        for s in teilflaechenabfrage:
            startjahr = s.Startjahr

        rows = arcpy.SearchCursor(element_und_preisliste)

        for row in rows:
            try:
                kostenbereich = row.Kostenbereich
                element_name = row.Element
                fl_typen = str(row.Benutzte_FL_Typen)
                fl_typen = ast.literal_eval(fl_typen)
                einheit = row.Einheit
                kriterium = row.Kriterium

                if kriterium == "Immer" or kriterium == entwaesserungssystem: #frage ab, welches entwaesserungssystem gewaehlt wurde

                    rel_flaeche = 0 #(kosten-)relevante flaechen fuer dieses element
                    for e in fl_typen:
                        type = e[0]
                        multiplikator = e[1]

                        where_clause = """"Flaechennutzung_S2" = '"""+type+"""' AND "Teilflaeche_Plangebiet" ='"""+teilflaeche+"'"
                        flaechen = arcpy.SearchCursor(flaechenbilanz_planung_gruppiert, where_clause, "", "","")
                        for flaeche in flaechen:
                            wert =  float(flaeche.Flaeche_ha)*float(multiplikator)
                            rel_flaeche = rel_flaeche + wert

                    X = rel_flaeche
                    Formel_Fl_zu_Menge = str(row.Formel_Fl_zu_Menge)
                    rel_menge = 0
                    rel_menge = int(eval(Formel_Fl_zu_Menge))

                    if rel_menge >0:
                        #print teilflaeche,startjahr, kostenbereich,element_name,rel_menge
                        rows = arcpy.InsertCursor(infrastrukturmenge)
                        row = rows.newRow()
                        row.Teilflaeche_Plangebiet = teilflaeche
                        row.Kostenbereich = kostenbereich
                        row.Element = element_name
                        row.Menge = rel_menge
                        row.Einheit = einheit
                        row.Startjahr = startjahr
                        rows.insertRow(row)
                        del rows, row
                    else:
                        pass
            except Exception as e:
                print e
                pass

    #############################################################################################################
    # Schritt 2a - Berechne Regenwasserretention
    schrittmeldung = 'Berechne Regenwasserretention \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung

    # Aktualisiere Elementmengentabelle
    try:
        if rueckhaltebecken_m3 <> None:
            rows = arcpy.InsertCursor(infrastrukturmenge)
            row = rows.newRow()
            row.Teilflaeche_Plangebiet = "Allgemein"
            row.Kostenbereich = "06 - Abwasserentsorgung"
            row.Element = rueckhaltebecken_typ
            row.Menge = int(rueckhaltebecken_m3)
            row.Einheit = 'm3'
            row.Startjahr = startjahr
            rows.insertRow(row)
    except Exception as e:
        pass

    # Erzeuge konkreten Kostenkennwert je m³ fuer den gewaehlten Rueckhaltebeckentyp
    if rueckhaltebecken_m3 <> None:
        if rueckhaltebecken_typ == "Rueckhaltebecken - offen":
            if int(rueckhaltebecken_m3) <= 500:
                kosten_m3 = 740
            elif int(rueckhaltebecken_m3) > 500 and int(rueckhaltebecken_m3) <= 2000:
                kosten_m3 = 16545*pow(int(rueckhaltebecken_m3),-0.5)
            else:
                kosten_m3 = 370

        elif rueckhaltebecken_typ == "Rueckhaltebecken - geschlossen":
            if int(rueckhaltebecken_m3) <= 100:
                kosten_m3 = 1650
            elif int(rueckhaltebecken_m3) > 100 and int(rueckhaltebecken_m3) <= 2000:
                kosten_m3 = 12024*pow(int(rueckhaltebecken_m3),-0.43)
            else:
                kosten_m3 = 455

        elif rueckhaltebecken_typ == "Rueckhaltebecken - Stauraumkanal":
            if int(rueckhaltebecken_m3) <= 90:
                kosten_m3 = 1742
            elif int(rueckhaltebecken_m3) > 90 and int(rueckhaltebecken_m3) <= 1550:
                kosten_m3 = 13801*pow(int(rueckhaltebecken_m3),-0.46)
            else:
                kosten_m3 = 470

        elif rueckhaltebecken_typ == "Rueckhaltebecken - Retentionsbodenfilter":
            if int(rueckhaltebecken_m3) <= 500:
                kosten_m3 = 500
            elif int(rueckhaltebecken_m3) > 500 and int(rueckhaltebecken_m3) <= 2000:
                kosten_m3 = 7235*pow(int(rueckhaltebecken_m3),-0.43)
            else:
                kosten_m3 = 275
        try:
            message =  rueckhaltebecken_typ+" "+str(kosten_m3)
            #messages.AddMessage(message)
        except:
            pass

    # Loesche ggf. bereits vorhandenen Typ in T03MEG_Element_und_Preisliste und aktualisiere den Wert
    if rueckhaltebecken_m3 is not None:
        where_clause = """"Element" ='"""+rueckhaltebecken_typ+"'"
        rows = arcpy.UpdateCursor(element_und_preisliste,where_clause)
        for row in rows:
            row.Herstellungskosten_einmalig = kosten_m3
            row.Betriebs_und_Unterhaltungskosten_jaehrlich = kosten_m3/100
            row.Erneuerungskosten_pro_Zyklus = kosten_m3/10
            row.Dauer_Erneuerungszyklus = 50
            rows.updateRow(row)

    #############################################################################################################
    # Schritt 2b - Ergaenze zusaetzliche Kanalmeter
    schrittmeldung = 'Ergaenze zusaetzliche Kanalmeter \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung

    #Loesche ggf. aus vorigen Berechnungen angelegte Kanallaengen
    try:
        where_clause = """"Element" ='Mischwasserkanal DN 600' and "Kostenbereich" = '06 - Abwasserentsorgung'"""
        rows = arcpy.UpdateCursor(element_und_preisliste,where_clause)
        for row in rows:
            rows.deleteRow()
        del row, rows
    except:
        pass

    try:
        where_clause = """"Element" ='Trennsystem DN 300 SW - DN 600 RW' and "Kostenbereich" = '06 - Abwasserentsorgung'"""
        rows = arcpy.UpdateCursor(element_und_preisliste,where_clause)
        for row in rows:
            rows.deleteRow()
        del row, rows
    except:
        pass

    try:
        where_clause = """"Element" ='Schmutzwasserkanal DN 300' and "Kostenbereich" = '06 - Abwasserentsorgung'"""
        rows = arcpy.UpdateCursor(element_und_preisliste,where_clause)
        for row in rows:
            rows.deleteRow()
        del row, rows
    except:
        pass

    # Aktualisiere Elementmengentabelle entsprechend des gewaehlten Entwaesserungssystems
    try:
        if zus_kanalmeter <> None:
            if entwaesserungssystem == "Mischwassersystem":
                rows = arcpy.InsertCursor(infrastrukturmenge)
                row = rows.newRow()
                row.Teilflaeche_Plangebiet = "Allgemein"
                row.Kostenbereich = "06 - Abwasserentsorgung"
                row.Element = "Mischwasserkanal DN 600"
                row.Menge = int(zus_kanalmeter)
                row.Einheit = 'm'
                row.Startjahr = startjahr
                rows.insertRow(row)
            elif entwaesserungssystem == "Trennwassersystem":
                rows = arcpy.InsertCursor(infrastrukturmenge)
                row = rows.newRow()
                row.Teilflaeche_Plangebiet = "Allgemein"
                row.Kostenbereich = "06 - Abwasserentsorgung"
                row.Element = "Trennsystem DN 300 SW - DN 600 RW"
                row.Menge = int(zus_kanalmeter)
                row.Einheit = 'm'
                row.Startjahr = startjahr
                rows.insertRow(row)
            else:
                rows = arcpy.InsertCursor(infrastrukturmenge)
                row = rows.newRow()
                row.Teilflaeche_Plangebiet = "Allgemein"
                row.Kostenbereich = "06 - Abwasserentsorgung"
                row.Element = "Schmutzwasserkanal DN 300"
                row.Menge = int(zus_kanalmeter)
                row.Einheit = 'm'
                row.Startjahr = startjahr
                rows.insertRow(row)
    except:
        pass

    #############################################################################################################
    # Schritt 3 - Ergaenze Herstellungskostentabelle um Zusatzwerte
    schrittmeldung = 'Ergaenze Herstellungskostentabelle um Zusatzwerte \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung

    # Loesche ggf. bereits vorhandenen Typ in T03MEG_Element_und_Preisliste und aktualisiere den Wert
    try:
        if zus_herstellungskosten <> None:
            where_clause = """"Element" ='Zusatzkosten'"""
            rows = arcpy.UpdateCursor(element_und_preisliste,where_clause)
            for row in rows:
                row.Herstellungskosten_einmalig = int(zus_herstellungskosten)
                row.Betriebs_und_Unterhaltungskosten_jaehrlich = int(zus_betriebskosten)
                row.Erneuerungskosten_pro_Zyklus = int(zus_herstellungskosten)/10
                row.Dauer_Erneuerungszyklus = 40
                rows.updateRow(row)

            rows = arcpy.InsertCursor(infrastrukturmenge)
            row = rows.newRow()
            row.Teilflaeche_Plangebiet = "Allgemein"
            row.Kostenbereich = "08 - Zusatzkosten"
            row.Element = "Zusatzkosten"
            row.Menge = 1
            row.Einheit = '€'
            row.Startjahr = startjahr
            rows.insertRow(row)

    except:
        pass

    #############################################################################################################
    # Schritt 3 - Erzeuge Herstellungskostentabelle
    schrittmeldung = 'Berechne Herstellungskosten \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung

    eingangstabellen = [
        (workspace_projekt_kosten,'MEG_Mengenermittlung'),
        (workspace_tool_kosten,'T01DEF_Untersuchungsjahre'),
        (workspace_tool_kosten,'T03MEG_Element_und_Preisliste'),
        (workspace_tool_kosten,'T01DEF_Regionalfaktoren'),
        (workspace_projekt_definition,'Projektrahmendaten')
    ]

    ausgabetabelle = (workspace_projekt_kosten,'T04KOM_01_Herstellungskosten')

    sql = """SELECT MEG_Mengenermittlung.Teilflaeche_Plangebiet, T01DEF_Untersuchungsjahre.Jahr, MEG_Mengenermittlung.Kostenbereich, T03MEG_Element_und_Preisliste.Element AS Element, T03MEG_Element_und_Preisliste.Einheit, [Menge]*[Herstellungskosten_einmalig]*[Projektspezifischer_Sonderkostenfaktor]*[Faktor_BKI] AS Herstellungskosten INTO T04KOM_01_Herstellungskosten
                FROM (MEG_Mengenermittlung INNER JOIN T01DEF_Untersuchungsjahre ON MEG_Mengenermittlung.Startjahr = T01DEF_Untersuchungsjahre.Jahr) INNER JOIN T03MEG_Element_und_Preisliste ON (MEG_Mengenermittlung.Element = T03MEG_Element_und_Preisliste.Element) AND (MEG_Mengenermittlung.Kostenbereich = T03MEG_Element_und_Preisliste.Kostenbereich), Projektrahmendaten INNER JOIN T01DEF_Regionalfaktoren ON Projektrahmendaten.AGS = T01DEF_Regionalfaktoren.AGS
                WHERE (((T01DEF_Untersuchungsjahre.Jahr) Between [Beginn_Betrachtungszeitraum] And [Ende_Betrachtungszeitraum]))
                GROUP BY MEG_Mengenermittlung.Teilflaeche_Plangebiet, T01DEF_Untersuchungsjahre.Jahr, MEG_Mengenermittlung.Kostenbereich, T03MEG_Element_und_Preisliste.Element, T03MEG_Element_und_Preisliste.Einheit, [Menge]*[Herstellungskosten_einmalig]*[Projektspezifischer_Sonderkostenfaktor]*[Faktor_BKI]
                ORDER BY MEG_Mengenermittlung.Teilflaeche_Plangebiet, T01DEF_Untersuchungsjahre.Jahr, MEG_Mengenermittlung.Kostenbereich;
                """

    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    #############################################################################################################
    # Schritt 4 - Erzeuge Betriebs- und Unterhaltungskostentabelle
    schrittmeldung = 'Berechne Betriebs- und Unterhaltungskosten \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung

    eingangstabellen = [
        (workspace_projekt_kosten,'MEG_Mengenermittlung'),
        (workspace_tool_kosten,'T01DEF_Untersuchungsjahre'),
        (workspace_tool_kosten,'T03MEG_Element_und_Preisliste'),
        (workspace_tool_kosten,'T01DEF_Regionalfaktoren'),
        (workspace_projekt_definition,'Projektrahmendaten')
    ]

    ausgabetabelle = (workspace_projekt_kosten,'T04KOM_02_Betrieb_Unterhaltung')

    sql = """SELECT MEG_Mengenermittlung.Teilflaeche_Plangebiet, T01DEF_Untersuchungsjahre.Jahr, MEG_Mengenermittlung.Kostenbereich, MEG_Mengenermittlung.Element, Sum([Menge]*[Betriebs_und_Unterhaltungskosten_jaehrlich]) AS Betriebskosten INTO T04KOM_02_Betrieb_Unterhaltung
                FROM T01DEF_Untersuchungsjahre, Projektrahmendaten, MEG_Mengenermittlung INNER JOIN T03MEG_Element_und_Preisliste ON (MEG_Mengenermittlung.Element = T03MEG_Element_und_Preisliste.Element) AND (MEG_Mengenermittlung.Kostenbereich = T03MEG_Element_und_Preisliste.Kostenbereich)
                WHERE (((MEG_Mengenermittlung.Startjahr)<=[Jahr]) AND ((T01DEF_Untersuchungsjahre.Jahr) Between [Beginn_Betrachtungszeitraum] And [Ende_Betrachtungszeitraum]))
                GROUP BY MEG_Mengenermittlung.Teilflaeche_Plangebiet, T01DEF_Untersuchungsjahre.Jahr, MEG_Mengenermittlung.Kostenbereich, MEG_Mengenermittlung.Element
                ORDER BY MEG_Mengenermittlung.Teilflaeche_Plangebiet, T01DEF_Untersuchungsjahre.Jahr, MEG_Mengenermittlung.Kostenbereich;
                """

    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    #############################################################################################################
    # Schritt 5 - Erzeuge Erneuerungskostentabelle
    schrittmeldung = 'Berechne Erneuerungskosten \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung

    eingangstabellen = [
        (workspace_projekt_kosten,'MEG_Mengenermittlung'),
        (workspace_tool_kosten,'T01DEF_Untersuchungsjahre'),
        (workspace_tool_kosten,'T01DEF_Erneuerungszyklen'),
        (workspace_tool_kosten,'T03MEG_Element_und_Preisliste'),
        (workspace_tool_kosten,'T01DEF_Regionalfaktoren'),
        (workspace_projekt_definition,'Projektrahmendaten')
    ]

    ausgabetabelle = (workspace_projekt_kosten,'T04KOM_03_Erneuerung')

    sql = """SELECT MEG_Mengenermittlung.Teilflaeche_Plangebiet, [Startjahr]+[NrErneuerungszyklus]*[Dauer_Erneuerungszyklus] AS Jahr, MEG_Mengenermittlung.Kostenbereich, MEG_Mengenermittlung.Element, T01DEF_Erneuerungszyklen.NrErneuerungszyklus, [Erneuerungskosten_pro_Zyklus]*[Menge]*[Projektspezifischer_Sonderkostenfaktor] AS Erneuerungskosten INTO T04KOM_03_Erneuerung
                FROM T01DEF_Erneuerungszyklen, Projektrahmendaten, T03MEG_Element_und_Preisliste INNER JOIN MEG_Mengenermittlung ON (T03MEG_Element_und_Preisliste.Kostenbereich=MEG_Mengenermittlung.Kostenbereich) AND (T03MEG_Element_und_Preisliste.Element=MEG_Mengenermittlung.Element)
                WHERE ((([Startjahr]+[NrErneuerungszyklus]*[Dauer_Erneuerungszyklus])<=[Ende_Betrachtungszeitraum]) And (([Erneuerungskosten_pro_Zyklus]*[Menge]*[Projektspezifischer_Sonderkostenfaktor])>0))
                ORDER BY MEG_Mengenermittlung.Kostenbereich;
                """

    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    #############################################################################################################
    # Schritt 6 - Kosten nach Kostenphasen
    schrittmeldung = 'Berechne Kosten nach Kostenphasen \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung

    eingangstabellen = [
        (workspace_projekt_kosten,'T04KOM_03_Erneuerung'),
        (workspace_projekt_kosten,'T04KOM_02_Betrieb_Unterhaltung'),
        (workspace_projekt_kosten,'T04KOM_01_Herstellungskosten')
    ]

    ausgabetabelle = (workspace_projekt_kosten,'T04KOM_04_Kosten_nach_Kostenphasen')

    sql = """SELECT * INTO T04KOM_04_Kosten_nach_Kostenphasen
                FROM(
                SELECT '1 - Erstmalige Herstellung' AS Kostenphase, [T04KOM_01_Herstellungskosten].Teilflaeche_Plangebiet, [T04KOM_01_Herstellungskosten].Jahr, [T04KOM_01_Herstellungskosten].Kostenbereich, [T04KOM_01_Herstellungskosten].Element, [T04KOM_01_Herstellungskosten].Herstellungskosten AS Kosten
                FROM [T04KOM_01_Herstellungskosten]
                union
                SELECT '2 - Betrieb und Unterhaltung' AS Kostenphase, T04KOM_02_Betrieb_Unterhaltung.Teilflaeche_Plangebiet, T04KOM_02_Betrieb_Unterhaltung.Jahr, T04KOM_02_Betrieb_Unterhaltung.Kostenbereich, T04KOM_02_Betrieb_Unterhaltung.Element, T04KOM_02_Betrieb_Unterhaltung.Betriebskosten AS Kosten
                FROM T04KOM_02_Betrieb_Unterhaltung
                union
                SELECT '3 - Erneuerung' AS Kostenphase, T04KOM_03_Erneuerung.Teilflaeche_Plangebiet, T04KOM_03_Erneuerung.Jahr, T04KOM_03_Erneuerung.Kostenbereich, T04KOM_03_Erneuerung.Element, T04KOM_03_Erneuerung.Erneuerungskosten AS Kosten
                FROM T04KOM_03_Erneuerung)
                as a;
                """

    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    #############################################################################################################
    # Schritt 6 - Kostenaufteilung
    schrittmeldung = 'Berechne Kostenaufteilung \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung

    eingangstabellen = [
        (workspace_tool_kosten,'T01DEF_Kostenaufteilungsregeln'),
        (workspace_tool_kosten,'T01DEF_Kostentraeger'),
        (workspace_projekt_kosten,'Projektspez_Kostenauft'),
        (workspace_projekt_kosten,'T04KOM_04_Kosten_nach_Kostenphasen')
    ]

    ausgabetabelle = (workspace_projekt_kosten,'T05KAM_01_Kostenaufteilung')

    sql = """SELECT T04KOM_04_Kosten_nach_Kostenphasen.Teilflaeche_Plangebiet, T04KOM_04_Kosten_nach_Kostenphasen.Kostenphase, T04KOM_04_Kosten_nach_Kostenphasen.Jahr, T04KOM_04_Kosten_nach_Kostenphasen.Kostenbereich, Projektspez_Kostenauft.Kostenaufteilungsregel, T01DEF_Kostentraeger.Kostentraeger, T01DEF_Kostenaufteilungsregeln.Anteil, Sum([Kosten]*[Anteil]) AS Kosten_Summe INTO T05KAM_01_Kostenaufteilung
                FROM ((Projektspez_Kostenauft INNER JOIN T04KOM_04_Kosten_nach_Kostenphasen ON (Projektspez_Kostenauft.Kostenbereich = T04KOM_04_Kosten_nach_Kostenphasen.Kostenbereich) AND (Projektspez_Kostenauft.Kostenphase = T04KOM_04_Kosten_nach_Kostenphasen.Kostenphase)) INNER JOIN T01DEF_Kostenaufteilungsregeln ON Projektspez_Kostenauft.Kostenaufteilungsregel = T01DEF_Kostenaufteilungsregeln.Kostenregelname) INNER JOIN T01DEF_Kostentraeger ON T01DEF_Kostenaufteilungsregeln.Kostentraeger = T01DEF_Kostentraeger.OBJECTID
                GROUP BY T04KOM_04_Kosten_nach_Kostenphasen.Teilflaeche_Plangebiet, T04KOM_04_Kosten_nach_Kostenphasen.Kostenphase, T04KOM_04_Kosten_nach_Kostenphasen.Jahr, T04KOM_04_Kosten_nach_Kostenphasen.Kostenbereich, Projektspez_Kostenauft.Kostenaufteilungsregel, T01DEF_Kostentraeger.Kostentraeger, T01DEF_Kostenaufteilungsregeln.Anteil
                ORDER BY T04KOM_04_Kosten_nach_Kostenphasen.Teilflaeche_Plangebiet, T04KOM_04_Kosten_nach_Kostenphasen.Kostenphase, T04KOM_04_Kosten_nach_Kostenphasen.Jahr, T04KOM_04_Kosten_nach_Kostenphasen.Kostenbereich;
                """
    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)


    #############################################################################################################
    # Schritt 6 - Datenexport in Excel-Datei
    schrittmeldung = 'Datenexport in Excel-Datei  \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung

    #projektname = 'LKH_Bultweg' # haendische Ueberbrueckung bei manueller Scriptnutzung

    # Pfade setzen
    base_path = str(sys.path[0]).split("2_Tool")[0]
    workspace_projekt_kosten = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Kosten_'+projektname+'.gdb')
    tablepath = os.path.join(workspace_projekt_kosten,'T05KAM_01_Kostenaufteilung')
    infrastrukturpath = os.path.join(workspace_projekt_kosten,'MEG_Mengenermittlung')

    logo = os.path.join((str(sys.path[0]).split("2_Tool")[0]),"1_Basisdaten","logo_rpc.png")
    ausgabeordner = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Excel')
    excelpfad = os.path.join(ausgabeordner,'Infrastrukturkosten.xlsx')

    try:
        os.remove(excelpfad)
    except:
        pass

    # Workbook und Tabellenblätter anlegen
    wb = xlsxwriter.Workbook(excelpfad)
    sl.infosheet(projektname, str("Infrastrukturkosten").decode('utf-8'), wb)
    ws6 = wb.add_worksheet('Methodik')
    ws3 = wb.add_worksheet('Auswertungen')
    ws4 = wb.add_worksheet('Grafiken')
    ws2 = wb.add_worksheet('Rohdaten')
    ws5 = wb.add_worksheet('Infrastrukturmengen')
    ws7 = wb.add_worksheet('Haftungsausschluss')

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
            ws6.write(x,y,"", format)
            ws7.write(x,y,"", format)

    #Charts anlegen
    chart_kosten_jahr = wb.add_chart({'type': 'column', 'subtype': 'stacked'})
    chart_kosten_jahr.set_style(40)
    chart_kosten_jahr.set_size({'width': 800, 'height': 600})
    chart_kosten_jahr.set_chartarea({'border': {'none': True},'fill': {'none': True}})
    chart_kosten_jahr.set_legend({'position': 'bottom'})
    chart_kosten_jahr.set_title({'name': 'Kosten nach Kostenbereich - jaehrlich','name_font':  {'name': 'Tahoma', 'size': 9}})

    chart_kosten_kum = wb.add_chart({'type': 'area', 'subtype': 'stacked'})
    chart_kosten_kum.set_style(40)
    chart_kosten_kum.set_size({'width': 800, 'height': 600})
    chart_kosten_kum.set_chartarea({'border': {'none': True},'fill': {'none': True}})
    chart_kosten_kum.set_legend({'position': 'bottom'})
    chart_kosten_kum.set_title({'name': 'Kosten nach Kostenbereich - kumuliert','name_font':  {'name': 'Tahoma', 'size': 9}})

    chart_kostenphase_kum = wb.add_chart({'type': 'area', 'subtype': 'stacked'})
    chart_kostenphase_kum.set_style(40)
    chart_kostenphase_kum.set_size({'width': 800, 'height': 600})
    chart_kostenphase_kum.set_chartarea({'border': {'none': True},'fill': {'none': True}})
    chart_kostenphase_kum.set_legend({'position': 'bottom'})
    chart_kostenphase_kum.set_title({'name': 'Kosten nach Kostenphasen - kumuliert','name_font':  {'name': 'Tahoma', 'size': 9}})

    chart_kostentraeger_kum = wb.add_chart({'type': 'area', 'subtype': 'stacked'})
    chart_kostentraeger_kum.set_style(40)
    chart_kostentraeger_kum.set_size({'width': 800, 'height': 600})
    chart_kostentraeger_kum.set_chartarea({'border': {'none': True},'fill': {'none': True}})
    chart_kostentraeger_kum.set_legend({'position': 'bottom'})
    chart_kostentraeger_kum.set_title({'name': 'Kosten nach Kostentraegern - kumuliert','name_font':  {'name': 'Tahoma', 'size': 9}})


    ################################
    #Werteblatt Kostenwerte einfuegen

    #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
    rows = arcpy.SearchCursor(tablepath)

    #Feldnamen auslesen
    fieldnames = [f.name for f in arcpy.ListFields(tablepath)]

    j = 1
    for row in rows:
        i = 0
        for fieldname in fieldnames:
            try:
                wert = int(row.getValue(fieldname))
            except:
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

    #Werteblatt Infrastrukturmengen einfuegen

    #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
    rows = arcpy.SearchCursor(infrastrukturpath)

    #Feldnamen auslesen
    fieldnames = [f.name for f in arcpy.ListFields(infrastrukturpath)]

    j = 1
    for row in rows:
        i = 0
        for fieldname in fieldnames:
            try:
                wert = int(row.getValue(fieldname))
            except:
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

    ################
    #Kosten nach Kostenbereich

    #Jahre auslesen
    rows = arcpy.SearchCursor(tablepath)
    Jahre = []
    for row in rows:
        Jahr = row.Jahr
        Jahre.append(Jahr)
    Jahre = list(set(Jahre))
    Jahre.sort()

    #Kostenbereiche auslesen
    rows = arcpy.SearchCursor(tablepath)
    Kostenbereiche = []
    for row in rows:
        Kostenbereich = row.Kostenbereich
        Kostenbereiche.append(Kostenbereich)
    Kostenbereiche = list(set(Kostenbereiche))
    Kostenbereiche.sort()
    Kostenbereiche_Anzahl = len(Kostenbereiche)


    Zeilenabstand = Kostenbereiche_Anzahl+5

    #Jahre in Excel eintragen
    i = 2
    j = 2
    for Jahr in Jahre:
        ws3.write(Zeilenabstand*0+i, j, Jahr, bold) #jaehrliche Darstellung
        ws3.write(Zeilenabstand*1+i, j, Jahr, bold) #kumulierte Darstellung
        j = j+1

    #Kostenbereiche in Excel eintragen
    i = 3
    j = 1
    for Kostenbereich in Kostenbereiche:
        ws3.write(Zeilenabstand*0+i, j, Kostenbereich, bold) #jaehrliche Darstellung
        ws3.write(Zeilenabstand*1+i, j, Kostenbereich, bold) #kumulierte Darstellung
        i = i+1

    #Ergebnisse in Excel eintragen
    #hinweis: formeln muessen auf englisch geschrieben werden - uebersetzung mit http://de.excel-translator.de/
    #cell = xl_rowcol_to_cell(1, 2)  # C2

    i = 2
    l = 0
    for Kostenbereich in Kostenbereiche:
        i = i+1
        j = 1
        k = 0
        l = l+1
        for Jahr in Jahre:
            k = k+1
            j = j+1
            jahresvariable = xl_rowcol_to_cell(i-l, j)
            kostenbereichsvariable = xl_rowcol_to_cell(i, j-k)
            formulastring1 = '=SUMIFS(Rohdaten!$I:$I,Rohdaten!$D:$D,Auswertungen!'+jahresvariable+',Rohdaten!$E:$E,Auswertungen!'+kostenbereichsvariable+')'
            ws3.write_formula(i,j, formulastring1,normal)

            v1 = xl_rowcol_to_cell(Zeilenabstand+i, j-1)
            v2 = xl_rowcol_to_cell(i, j)
            formulastring2 = '='+v1+'+'+v2
            ws3.write_formula(Zeilenabstand+i,j, formulastring2,normal)

            jmax = j

        # nun noch die erste spalte aktualisieren
        j = 2
        v1 = xl_rowcol_to_cell(i, j)
        formulastring1 = '='+v1
        ws3.write_formula(Zeilenabstand+i,j, formulastring1,normal)

        # Werte in Chartobjekte schreiben
        name = xl_rowcol_to_cell(Zeilenabstand*0+i,1)
        chart_kosten_jahr.add_series({
            'name': ['Auswertungen', Zeilenabstand*0+i, 1, Zeilenabstand*0+i,1],
            'categories': ['Auswertungen', Zeilenabstand*0+2, 2, Zeilenabstand*0+2,jmax],
            'values':     ['Auswertungen', Zeilenabstand*0+i, 2, Zeilenabstand*0+i,jmax],
        })

        name = xl_rowcol_to_cell(Zeilenabstand*1+i,1)
        chart_kosten_kum.add_series({
            'name': ['Auswertungen', Zeilenabstand*1+i, 1, Zeilenabstand*1+i,1],
            'categories': ['Auswertungen', Zeilenabstand*1+2, 2, Zeilenabstand*1+2,jmax],
            'values':     ['Auswertungen', Zeilenabstand*1+i, 2, Zeilenabstand*1+i,jmax],
        })




    ################
    #Kosten nach Kostenphase

    #Jahre auslesen
    rows = arcpy.SearchCursor(tablepath)
    Jahre = []
    for row in rows:
        Jahr = row.Jahr
        Jahre.append(Jahr)
    Jahre = list(set(Jahre))
    Jahre.sort()

    #Kostenbereiche auslesen
    rows = arcpy.SearchCursor(tablepath)
    Kostenphasen = []
    for row in rows:
        Kostenphase = row.Kostenphase
        Kostenphasen.append(Kostenphase)
    Kostenphasen = list(set(Kostenphasen))
    Kostenphasen.sort()
    Kostenphasen_Anzahl = len(Kostenphasen)


    #Jahre in Excel eintragen
    i = 2
    j = 2
    for Jahr in Jahre:
        ws3.write(Zeilenabstand*2+i, j, Jahr, bold) #jaehrliche Darstellung
        ws3.write(Zeilenabstand*3+i, j, Jahr, bold) #kumulierte Darstellung
        j = j+1

    #Kostenphasen in Excel eintragen
    i = 3
    j = 1
    for Kostenphase in Kostenphasen:
        ws3.write(Zeilenabstand*2+i, j, Kostenphase, bold) #jaehrliche Darstellung
        ws3.write(Zeilenabstand*3+i, j, Kostenphase, bold) #kumulierte Darstellung
        i = i+1

    #Ergebnisse in Excel eintragen
    #hinweis: formeln muessen auf englisch geschrieben werden - uebersetzung mit http://de.excel-translator.de/
    #cell = xl_rowcol_to_cell(1, 2)  # C2

    i = 2
    l = 0
    for Kostenphase in Kostenphasen:
        i = i+1
        j = 1
        k = 0
        l = l+1
        for Jahr in Jahre:
            k = k+1
            j = j+1
            jahresvariable = xl_rowcol_to_cell(i-l, j)
            Kostenphasenvariable = xl_rowcol_to_cell(Zeilenabstand*2+i, j-k)
            formulastring1 = '=SUMIFS(Rohdaten!$I:$I,Rohdaten!$D:$D,Auswertungen!'+jahresvariable+',Rohdaten!$C:$C,Auswertungen!'+Kostenphasenvariable+')'
            ws3.write_formula(Zeilenabstand*2+i,j, formulastring1,normal)

            v1 = xl_rowcol_to_cell(Zeilenabstand*2+i, j)
            v2 = xl_rowcol_to_cell(Zeilenabstand*3+i, j-1)
            formulastring2 = '='+v1+'+'+v2
            ws3.write_formula(Zeilenabstand*3+i,j, formulastring2,normal)

        # nun noch die erste spalte aktualisieren
        j = 2
        v1 = xl_rowcol_to_cell(Zeilenabstand*2+i, j)
        formulastring1 = '='+v1
        ws3.write_formula(Zeilenabstand*3+i,j, formulastring1,normal)

        # Werte in Chartobjekte schreiben
        chart_kostenphase_kum.add_series({
            'name': ['Auswertungen', Zeilenabstand*3+i, 1, Zeilenabstand*3+i,1],
            'categories': ['Auswertungen', Zeilenabstand*3+2, 2, Zeilenabstand*3+2,jmax],
            'values':     ['Auswertungen', Zeilenabstand*3+i, 2, Zeilenabstand*3+i,jmax],
        })

    ################
    #Kosten nach Kostentraeger

    #Jahre auslesen
    rows = arcpy.SearchCursor(tablepath)
    Jahre = []
    for row in rows:
        Jahr = row.Jahr
        Jahre.append(Jahr)
    Jahre = list(set(Jahre))
    Jahre.sort()
    try:
        del rows, row
    except:
        pass

    #Kostenbereiche auslesen
    rows = arcpy.SearchCursor(tablepath)
    Kostentraegers = []
    for row in rows:
        Kostentraeger = row.Kostentraeger
        Kostentraegers.append(Kostentraeger)
    Kostentraegers = list(set(Kostentraegers))
    Kostentraegers.sort()
    Kostentraegers_Anzahl = len(Kostentraegers)
    try:
        del rows, row
    except:
        pass

    #Jahre in Excel eintragen
    i = 2
    j = 2
    for Jahr in Jahre:
        ws3.write(Zeilenabstand*4+i, j, Jahr, bold) #jaehrliche Darstellung
        ws3.write(Zeilenabstand*5+i, j, Jahr, bold) #kumulierte Darstellung
        j = j+1

    #Kostenphasen in Excel eintragen
    i = 3
    j = 1
    for Kostentraeger in Kostentraegers:
        ws3.write(Zeilenabstand*4+i, j, Kostentraeger, bold) #jaehrliche Darstellung
        ws3.write(Zeilenabstand*5+i, j, Kostentraeger, bold) #kumulierte Darstellung
        i = i+1

    #Ergebnisse in Excel eintragen
    #hinweis: formeln muessen auf englisch geschrieben werden - uebersetzung mit http://de.excel-translator.de/
    #cell = xl_rowcol_to_cell(1, 2)  # C2

    i = 2
    l = 0
    for Kostentraeger in Kostentraegers:
        i = i+1
        j = 1
        k = 0
        l = l+1
        for Jahr in Jahre:
            k = k+1
            j = j+1
            jahresvariable = xl_rowcol_to_cell(i-l, j)
            Kostentraeger = xl_rowcol_to_cell(Zeilenabstand*4+i, j-k)
            formulastring1 = '=SUMIFS(Rohdaten!$I:$I,Rohdaten!$D:$D,Auswertungen!'+jahresvariable+',Rohdaten!$G:$G,Auswertungen!'+Kostentraeger+')'
            ws3.write_formula(Zeilenabstand*4+i,j, formulastring1,normal)

            v1 = xl_rowcol_to_cell(Zeilenabstand*4+i, j)
            v2 = xl_rowcol_to_cell(Zeilenabstand*5+i, j-1)
            formulastring2 = '='+v1+'+'+v2
            ws3.write_formula(Zeilenabstand*5+i,j, formulastring2,normal)

        # nun noch die erste spalte aktualisieren
        j = 2
        v1 = xl_rowcol_to_cell(Zeilenabstand*4+i, j)
        formulastring1 = '='+v1
        ws3.write_formula(Zeilenabstand*5+i,j, formulastring1,normal)

        # Werte in Chartobjekte schreiben
        name = xl_rowcol_to_cell(Zeilenabstand*5+i,1)
        chart_kostentraeger_kum.add_series({
            'name': ['Auswertungen', Zeilenabstand*5+i, 1, Zeilenabstand*5+i,1],
            'categories': ['Auswertungen', Zeilenabstand*5+2, 2, Zeilenabstand*5+2,jmax],
            'values':     ['Auswertungen', Zeilenabstand*5+i, 2, Zeilenabstand*5+i,jmax],
        })

    ################
    # Ueberschriften einfuegen

    # Erste Leerspalte anpassen
    ws2.set_column(0, 0, 3)

    # Ueberschriften einfuegen
    ws3.write(0, 1, 'Kosten nach Kostenbereichen', bold)
    ws3.write(1, 1, 'jaehrlich')

    ws3.write(Zeilenabstand, 1, 'Kosten nach Kostenbereichen', bold)
    ws3.write(Zeilenabstand+1, 1, 'kumuliert')

    ws3.write(Zeilenabstand*2, 1, 'Kosten nach Kostenphasen', bold)
    ws3.write(Zeilenabstand*2+1, 1, 'jaehrlich')

    ws3.write(Zeilenabstand*3, 1, 'Kosten nach Kostenphasen', bold)
    ws3.write(Zeilenabstand*3+1, 1, 'kumuliert')

    ws3.write(Zeilenabstand*4, 1, 'Kosten nach Kostentraegern', bold)
    ws3.write(Zeilenabstand*4+1, 1, 'jaehrlich')

    ws3.write(Zeilenabstand*5, 1, 'Kosten nach Kostentraegern', bold)
    ws3.write(Zeilenabstand*5+1, 1, 'kumuliert')

    rows = arcpy.SearchCursor(tablepath)

    #Spaltenbreiten anpassen
    ws3.set_column(1, 1, 40)

    ################################
    #Grafikblatt einfuegen
    ws4.insert_chart('B2', chart_kosten_jahr)
    ws4.insert_chart('B35', chart_kosten_kum)
    ws4.insert_chart('B67', chart_kostenphase_kum)
    ws4.insert_chart('B97', chart_kostentraeger_kum)

    ################################
    #Methodikblatt einfuegen
    methodik_grafik = os.path.join(base_path,"2_Tool","A_Infrastrukturkosten","Erlaeuterungstexte","Methodik_KommunaleInfrastrukturkosten.png")
    ws6.insert_image('B2', methodik_grafik, {'x_scale': 0.32, 'y_scale': 0.32}) #Korrigiert Verzerrung die bei 1x1 auftritt

    ################################
    #Haftungsausschluss einfuegen
    haftung_grafik = os.path.join(base_path,"2_Tool","A_Infrastrukturkosten","Erlaeuterungstexte","Haftungsausschluss.png")
    ws7.insert_image('B2', haftung_grafik, {'x_scale': 0.32, 'y_scale': 0.32}) #Korrigiert Verzerrung die bei 1x1 auftritt

    ################################
    #Workbook speichern
    try:
        wb.close()
    except Exception as e:
        messages.AddMessage(e)
        messages.AddMessage("Es liegt ein Fehler beim Speichern der Ausgabedatei vor. Ist diese ggf. noch geoeffnet?")

    # Endmeldung
    print 'Berechnung abgeschlossen'
    messages.AddMessage('Berechnung abgeschlossen')
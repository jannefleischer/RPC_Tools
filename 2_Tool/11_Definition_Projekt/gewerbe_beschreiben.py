__author__ = 'Mayr'

import lib_gewerbemodell as g
import arcpy,sys,os,xlsxwriter,imp
from xlsxwriter.utility import xl_rowcol_to_cell, xl_range, xl_col_to_name

sheetlibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '11_Definition_Projekt','sheet_lib.py'))
sl = imp.load_source('sheet_lib', sheetlibpath)

schrittmeldung = 'Eingaben werden gelesen \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

#Parameter aus Tool auslesen
i=0
projektname = arcpy.GetParameterAsText(i)
i+=1
teilflaeche = arcpy.GetParameterAsText(i)
i+=1
startjahr = arcpy.GetParameterAsText(i)
i+=1
aufsiedlungsdauer = arcpy.GetParameterAsText(i)
i+=1
gebtyp = arcpy.GetParameterAsText(i)
i+=1
zuzugsquote = arcpy.GetParameterAsText(i)
i+=1
eigentumsquote = arcpy.GetParameterAsText(i)
i+=1
Ant_Betr_VerarbGew = arcpy.GetParameterAsText(i)
i+=1
Ant_Betr_BauGew = arcpy.GetParameterAsText(i)
i+=1
Ant_Betr_HanKfZ = arcpy.GetParameterAsText(i)
i+=1
Ant_Betr_VerLag = arcpy.GetParameterAsText(i)
i+=1
Ant_Betr_FrWiTeDi = arcpy.GetParameterAsText(i)
i+=1
Ant_Betr_SoDi = arcpy.GetParameterAsText(i)


######################################################
#Prüfung der Branchenstruktur auf 100%
SummeBranchen = int(Ant_Betr_VerarbGew) + int(Ant_Betr_BauGew) + int(Ant_Betr_HanKfZ) + int(Ant_Betr_VerLag) + int(Ant_Betr_FrWiTeDi) + int(Ant_Betr_SoDi)

if SummeBranchen < 100:
    schrittmeldung = 'Die Summe der Branchenanteile liegt unter 100 Prozent. Bitte ueberpruefen Sie Ihre Angaben \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung
elif SummeBranchen > 100:
    schrittmeldung = 'Die Summe der Branchenanteile liegt ueber 100 Prozent. Bitte ueberpruefen Sie Ihre Angaben \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung
else:
    ######################################################
    #Zeitstempel definieren
    import time
    import datetime
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


    ######################################################
    #Flaechenbilanz berechnen

    schrittmeldung = 'Flaechenbilanz wird erstellt \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    #Pfade anlegen
    base_path = str(sys.path[0]).split("2_Tool")[0]
    tabelle_flaechenbilanzgrundlage = os.path.join(base_path,'2_Tool','11_Definition_Projekt','FGDB_11_Definition_Projekt_Tool.gdb','gewerbe_flaechenutzungsbilanz')
    tabelle_flaechennutzung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb','Flaechenbilanz_Planung_Prozent')
    shape_teilflaeche = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb','Teilflaechen_Plangebiet')

    #Projektflaeche auslesen
    rows_flaechengroesse = arcpy.SearchCursor(shape_teilflaeche)

    for row in rows_flaechengroesse:
        if row.Name == teilflaeche:
            flaechengroesse = row.Flaeche_ha

    #In Abhaengigkeit vom Gebietstyp die Flaechenbilanz definieren
    # Dazu zunächst die Anteilswerte aus Grundlagentabelle auslesen
    rows_flaechenbilanzgrundlage = arcpy.SearchCursor(tabelle_flaechenbilanzgrundlage)

    for row in rows_flaechenbilanzgrundlage:
        if row.Flaechennutzung_S1 == "Gruenflaeche":
            if row.Flaechennutzung_S2 == "Allgemeine Gruenflaechen":
                if gebtyp == "Industriegebiet":
                    ant_s2_allgGruen = row.Industriegebiet
                elif gebtyp == "Logistikgebiet":
                    ant_s2_allgGruen = row.Logistikgebiet
                elif gebtyp == "Klassisches Gewerbegebiet":
                    ant_s2_allgGruen = row.Klass_Gewerbe
                elif gebtyp == "Kleinteiliges Gewerbegebiet":
                    ant_s2_allgGruen = row.Klein_Gewerbe
                elif gebtyp == "Hoeherwertiges Gewerbegebiet":
                    ant_s2_allgGruen = row.Hoeher_Gewerbe
                elif gebtyp == "Technologiepark, Wissenschaftspark":
                    ant_s2_allgGruen = row.TechWissPark
            if row.Flaechennutzung_S2 == "Strassenbegleitgruen":
                if gebtyp == "Industriegebiet":
                    ant_s2_strBeglGruen = row.Industriegebiet
                elif gebtyp == "Logistikgebiet":
                    ant_s2_strBeglGruen = row.Logistikgebiet
                elif gebtyp == "Klassisches Gewerbegebiet":
                    ant_s2_strBeglGruen = row.Klass_Gewerbe
                elif gebtyp == "Kleinteiliges Gewerbegebiet":
                    ant_s2_strBeglGruen = row.Klein_Gewerbe
                elif gebtyp == "Hoeherwertiges Gewerbegebiet":
                    ant_s2_strBeglGruen = row.Hoeher_Gewerbe
                elif gebtyp == "Technologiepark, Wissenschaftspark":
                    ant_s2_strBeglGruen = row.TechWissPark
        if row.Flaechennutzung_S1 == "Erschliessungsflaeche":
            if row.Flaechennutzung_S2 == "Oeffentlich - Innere Erschliessung":
                if gebtyp == "Industriegebiet":
                    ant_s2_InErsch = row.Industriegebiet
                elif gebtyp == "Logistikgebiet":
                    ant_s2_InErsch = row.Logistikgebiet
                elif gebtyp == "Klassisches Gewerbegebiet":
                    ant_s2_InErsch = row.Klass_Gewerbe
                elif gebtyp == "Kleinteiliges Gewerbegebiet":
                    ant_s2_InErsch = row.Klein_Gewerbe
                elif gebtyp == "Hoeherwertiges Gewerbegebiet":
                    ant_s2_InErsch = row.Hoeher_Gewerbe
                elif gebtyp == "Technologiepark, Wissenschaftspark":
                    ant_s2_InErsch = row.TechWissPark
        if row.Flaechennutzung_S1 == "Nettobauland":
            if row.Flaechennutzung_S2 == "Gewerbeflaeche":
                if gebtyp == "Industriegebiet":
                    ant_s2_GewBauland = row.Industriegebiet
                elif gebtyp == "Logistikgebiet":
                    ant_s2_GewBauland = row.Logistikgebiet
                elif gebtyp == "Klassisches Gewerbegebiet":
                    ant_s2_GewBauland = row.Klass_Gewerbe
                elif gebtyp == "Kleinteiliges Gewerbegebiet":
                    ant_s2_GewBauland = row.Klein_Gewerbe
                elif gebtyp == "Hoeherwertiges Gewerbegebiet":
                    ant_s2_GewBauland = row.Hoeher_Gewerbe
                elif gebtyp == "Technologiepark, Wissenschaftspark":
                    ant_s2_GewBauland = row.TechWissPark

    # und dann die definierten Anteile mit der Projektflaeche multiplizieren
    s2_allgGrue = flaechengroesse * ant_s2_allgGruen / 100
    s2_strBeglGrue = flaechengroesse * ant_s2_strBeglGruen / 100
    s2_InErsch = flaechengroesse * ant_s2_InErsch / 100
    s2_GewBauland = flaechengroesse * ant_s2_GewBauland / 100

    # und zuletzt noch die Werte in die Tabelle schreiben
    Insert = arcpy.InsertCursor(tabelle_flaechennutzung)
    row = Insert.newRow()
    row.Teilflaeche_Plangebiet = teilflaeche
    row.Flaechennutzung_S1 = "Gruenflaeche"
    row.Flaechennutzung_S2 = "Allgemeine Gruenflaechen"
    row.Flaeche_ha = s2_allgGrue
    row.Startjahr = startjahr
    row.Anteil = ant_s2_allgGruen
    row.ID_ts = timestamp
    Insert.insertRow(row)

    Insert = arcpy.InsertCursor(tabelle_flaechennutzung)
    row = Insert.newRow()
    row.Teilflaeche_Plangebiet = teilflaeche
    row.Flaechennutzung_S1 = "Gruenflaeche"
    row.Flaechennutzung_S2 = "Strassenbegleitgruen"
    row.Flaeche_ha = s2_strBeglGrue
    row.Startjahr = startjahr
    row.Anteil = ant_s2_strBeglGruen
    row.ID_ts = timestamp
    Insert.insertRow(row)

    Insert = arcpy.InsertCursor(tabelle_flaechennutzung)
    row = Insert.newRow()
    row.Teilflaeche_Plangebiet = teilflaeche
    row.Flaechennutzung_S1 = "Erschliessungsflaeche"
    row.Flaechennutzung_S2 = "Oeffentlich - Innere Erschliessung"
    row.Flaeche_ha = s2_InErsch
    row.Startjahr = startjahr
    row.Anteil = ant_s2_InErsch
    row.ID_ts = timestamp
    Insert.insertRow(row)

    Insert = arcpy.InsertCursor(tabelle_flaechennutzung)
    row = Insert.newRow()
    row.Teilflaeche_Plangebiet = teilflaeche
    row.Flaechennutzung_S1 = "Nettobauland"
    row.Flaechennutzung_S2 = "Gewerbeflaeche"
    row.Flaeche_ha = s2_GewBauland
    row.Startjahr = startjahr
    row.Anteil = ant_s2_GewBauland
    row.ID_ts = timestamp
    Insert.insertRow(row)

    ######################################################
    # Anzahl der Betriebe nach Branchen bestimmen
    schrittmeldung = 'Branchenstrukturberechnung wird vorbereitet \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    # erstmal Pfade definieren
    tabelle_BFG = os.path.join(base_path,'2_Tool','11_Definition_Projekt','FGDB_11_Definition_Projekt_Tool.gdb','gewerbe_betriebsflaechengroesse')
    tabelle_betriebsstruktur = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb','Gewerbe_Betriebsstruktur')

    # dann zunächst die Betriebsanteile mit den definierten Parzellengrößen gewichten
    rows_BFG = arcpy.SearchCursor(tabelle_BFG)

    for row in rows_BFG:
        if row.Branche == "C":
            BFG_Betr_VerarbGew = float(row.Betriebsflaechengroesse_ha)
        if row.Branche == "F":
            BFG_Betr_BauGew = float(row.Betriebsflaechengroesse_ha)
        if row.Branche == "G":
            BFG_Betr_HanKfZ = float(row.Betriebsflaechengroesse_ha)
        if row.Branche == "H":
            BFG_Betr_VerLag = float(row.Betriebsflaechengroesse_ha)
        if row.Branche == "M":
            BFG_Betr_FrWiTeDi = float(row.Betriebsflaechengroesse_ha)
        if row.Branche == "N":
            BFG_Betr_SoDi = float(row.Betriebsflaechengroesse_ha)

    Flaeche_Betr_VerarbGew_temp = float(Ant_Betr_VerarbGew) * BFG_Betr_VerarbGew
    Flaeche_Betr_BauGew_temp = float(Ant_Betr_BauGew) * BFG_Betr_BauGew
    Flaeche_Betr_HanKfZ_temp = float(Ant_Betr_HanKfZ) * BFG_Betr_HanKfZ
    Flaeche_Betr_VerLag_temp = float(Ant_Betr_VerLag) * BFG_Betr_VerLag
    Flaeche_Betr_FrWiTeDi_temp = float(Ant_Betr_FrWiTeDi) * BFG_Betr_FrWiTeDi
    Flaeche_Betr_SoDi_temp = float(Ant_Betr_SoDi) * BFG_Betr_SoDi

    Flaeche_Gesamt_Temp = Flaeche_Betr_VerarbGew_temp + Flaeche_Betr_BauGew_temp + Flaeche_Betr_HanKfZ_temp + Flaeche_Betr_VerLag_temp + Flaeche_Betr_FrWiTeDi_temp + Flaeche_Betr_SoDi_temp

    #daraus die Flächenanteile ermitteln
    schrittmeldung = 'Gewerbeflaeche nach Branchen wird berechnet \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    gewerbebauland = float(s2_GewBauland)
    Flaeche_Betr_VerarbGew = float(Flaeche_Betr_VerarbGew_temp) / float(Flaeche_Gesamt_Temp) * float(gewerbebauland)
    Flaeche_Betr_BauGew = float(Flaeche_Betr_BauGew_temp) / float(Flaeche_Gesamt_Temp) * float(gewerbebauland)
    Flaeche_Betr_HanKfZ = float(Flaeche_Betr_HanKfZ_temp) / float(Flaeche_Gesamt_Temp) * float(gewerbebauland)
    Flaeche_Betr_VerLag = float(Flaeche_Betr_VerLag_temp) / float(Flaeche_Gesamt_Temp) * float(gewerbebauland)
    Flaeche_Betr_FrWiTeDi = float(Flaeche_Betr_FrWiTeDi_temp) / float(Flaeche_Gesamt_Temp) * float(gewerbebauland)
    Flaeche_Betr_SoDi = float(Flaeche_Betr_SoDi_temp) / float(Flaeche_Gesamt_Temp) * float(gewerbebauland)

    #und über die BFG wieder zur Anzahl der Betriebe
    schrittmeldung = 'Betriebszahl nach Branchen wird berechnet \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung
    BFGfaktor = 1.00
    if gebtyp == "Industriegebiet":
        BFGfaktor = 1.50
    elif gebtyp == "Logistikgebiet":
        BFGfaktor = 1.50
    elif gebtyp == "Klassisches Gewerbegebiet":
        BFGfaktor = 1.00
    elif gebtyp == "Kleinteiliges Gewerbegebiet":
        BFGfaktor = 0.70
    elif gebtyp == "Hoeherwertiges Gewerbegebiet":
        BFGfaktor = 0.90
    elif gebtyp == "Technologiepark, Wissenschaftspark":
        BFGfaktor = 0.85
    Anz_Betr_VerarbGew = Flaeche_Betr_VerarbGew / (BFG_Betr_VerarbGew * BFGfaktor)
    Anz_Betr_BauGew = Flaeche_Betr_BauGew / (BFG_Betr_BauGew * BFGfaktor)
    Anz_Betr_HanKfZ = Flaeche_Betr_HanKfZ / (BFG_Betr_HanKfZ * BFGfaktor)
    Anz_Betr_VerLag = Flaeche_Betr_VerLag / (BFG_Betr_VerLag * BFGfaktor)
    Anz_Betr_FrWiTeDi = Flaeche_Betr_FrWiTeDi / (BFG_Betr_FrWiTeDi * BFGfaktor)
    Anz_Betr_SoDi = Flaeche_Betr_SoDi / (BFG_Betr_SoDi * BFGfaktor)

    #Betriebsflaechen nach Branchen in Tabelle schreiben
    tabelle_betriebsflaeche = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb','Gewerbe_Betriebsflaechen')
    tabelle_betriebsflaeche_Insert = arcpy.InsertCursor(tabelle_betriebsflaeche)

    rowBFins = tabelle_betriebsflaeche_Insert.newRow()

    rowBFins.teilflaeche = str(teilflaeche)
    rowBFins.gebietstyp = str(gebtyp)
    rowBFins.Betriebsflaeche_C = float(Flaeche_Betr_VerarbGew)
    rowBFins.Betriebsflaeche_F = float(Flaeche_Betr_BauGew)
    rowBFins.Betriebsflaeche_G = float(Flaeche_Betr_HanKfZ)
    rowBFins.Betriebsflaeche_H = float(Flaeche_Betr_VerLag)
    rowBFins.Betriebsflaeche_M = float(Flaeche_Betr_FrWiTeDi)
    rowBFins.Betriebsflaeche_N = float(Flaeche_Betr_SoDi)
    rowBFins.timestamp = str(timestamp)

    tabelle_betriebsflaeche_Insert.insertRow(rowBFins)


    #und nun noch die Beschäftigten berechnen
    schrittmeldung = 'Beschaeftigtenzahl nach Branchen wird berechnet \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    tabelle_FKZ = os.path.join(base_path,'2_Tool','11_Definition_Projekt','FGDB_11_Definition_Projekt_Tool.gdb','gewerbe_flaechenkennziffern')
    rows_FKZ = arcpy.SearchCursor(tabelle_FKZ)

    for row in rows_FKZ:
        if row.Branche == "C":
            FKZ_VerarbGew = float(row.Beschaeftigte_je_Hektar)
        if row.Branche == "F":
            FKZ_BauGew = float(row.Beschaeftigte_je_Hektar)
        if row.Branche == "G":
            FKZ_HanKfZ = float(row.Beschaeftigte_je_Hektar)
        if row.Branche == "H":
            FKZ_VerLag = float(row.Beschaeftigte_je_Hektar)
        if row.Branche == "M":
            FKZ_FrWiTeDi = float(row.Beschaeftigte_je_Hektar)
        if row.Branche == "N":
            FKZ_SoDi = float(row.Beschaeftigte_je_Hektar)

    Besch_VerarbGew = float(Flaeche_Betr_VerarbGew) * float(FKZ_VerarbGew)
    Besch_BauGew = float(Flaeche_Betr_BauGew) * float(FKZ_BauGew)
    Besch_HanKfZ = float(Flaeche_Betr_HanKfZ) * float(FKZ_HanKfZ)
    Besch_VerLag = float(Flaeche_Betr_VerLag) * float(FKZ_VerLag)
    Besch_FrWiTeDi = float(Flaeche_Betr_FrWiTeDi) * float(FKZ_FrWiTeDi)
    Besch_SoDi = float(Flaeche_Betr_SoDi) * float(FKZ_SoDi)

    ################################################
    ### Aufsiedlugnsdauer einrechnen
    schrittmeldung = 'Aufsiedlungsdauer wird auf Flaechen-, Betriebs- Beschaeftigtenstruktur umgelegt \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    #### Aufsiedlugnsdauer Betriebe
    # zuletzt die Anzahl noch in die Ausgabetabelle schreiben und dabei mit der Aufsiedlungszeit verrechnen
    tabelle_parameter_aufsiedlungsdauer = os.path.join(base_path,'2_Tool','11_Definition_Projekt','FGDB_11_Definition_Projekt_Tool.gdb','gewerbe_aufsiedlungsdauer')
    tabelle_gewerbe_betriebsstruktur_Insert = arcpy.InsertCursor(tabelle_betriebsstruktur)

    #für Branche C
    anzahl_betriebe_start = Anz_Betr_VerarbGew
    aufsiedlungsdauer = str(aufsiedlungsdauer)

    sql = "Dauer_Jahre = " + str(aufsiedlungsdauer)

    tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer, sql)
    for row2 in tabelle_parameter_aufsiedlungsdauer_Search:
        parameter_jahr1 = row2.Jahr1
        parameter_jahr2 = row2.Jahr2
        parameter_jahr3 = row2.Jahr3
        parameter_jahr4 = row2.Jahr4
        parameter_jahr5 = row2.Jahr5
        parameter_jahr6 = row2.Jahr6
        parameter_jahr7 = row2.Jahr7
        parameter_jahr8 = row2.Jahr8
        parameter_jahr9 = row2.Jahr9
        parameter_jahr10 = row2.Jahr10
        parameter_jahr11 = row2.Jahr11
        parameter_jahr12 = row2.Jahr12
        parameter_jahr13 = row2.Jahr13
        parameter_jahr14 = row2.Jahr14
        parameter_jahr15 = row2.Jahr15
        parameter_jahr16 = row2.Jahr16
        parameter_jahr17 = row2.Jahr17
        parameter_jahr18 = row2.Jahr18
        parameter_jahr19 = row2.Jahr19
        parameter_jahr20 = row2.Jahr20
        parameter_jahr21 = row2.Jahr21
        parameter_jahr22 = row2.Jahr22
        parameter_jahr23 = row2.Jahr23
        parameter_jahr24 = row2.Jahr24
        parameter_jahr25 = row2.Jahr25
        parameter_jahr26 = row2.Jahr26
        parameter_jahr27 = row2.Jahr27
        parameter_jahr28 = row2.Jahr28
        parameter_jahr29 = row2.Jahr29
        parameter_jahr30 = row2.Jahr30
    del row2, tabelle_parameter_aufsiedlungsdauer_Search

    row3 = tabelle_gewerbe_betriebsstruktur_Insert.newRow()

    row3.anzahl_betriebe_jahr_0 = anzahl_betriebe_start * parameter_jahr1
    row3.anzahl_betriebe_jahr_1 = anzahl_betriebe_start * parameter_jahr2
    row3.anzahl_betriebe_jahr_2 = anzahl_betriebe_start * parameter_jahr3
    row3.anzahl_betriebe_jahr_3 = anzahl_betriebe_start * parameter_jahr4
    row3.anzahl_betriebe_jahr_4 = anzahl_betriebe_start * parameter_jahr5
    row3.anzahl_betriebe_jahr_5 = anzahl_betriebe_start * parameter_jahr6
    row3.anzahl_betriebe_jahr_6 = anzahl_betriebe_start * parameter_jahr7
    row3.anzahl_betriebe_jahr_7 = anzahl_betriebe_start * parameter_jahr8
    row3.anzahl_betriebe_jahr_8 = anzahl_betriebe_start * parameter_jahr9
    row3.anzahl_betriebe_jahr_9 = anzahl_betriebe_start * parameter_jahr10
    row3.anzahl_betriebe_jahr_10 = anzahl_betriebe_start * parameter_jahr11
    row3.anzahl_betriebe_jahr_11 = anzahl_betriebe_start * parameter_jahr12
    row3.anzahl_betriebe_jahr_12 = anzahl_betriebe_start * parameter_jahr13
    row3.anzahl_betriebe_jahr_13 = anzahl_betriebe_start * parameter_jahr14
    row3.anzahl_betriebe_jahr_14 = anzahl_betriebe_start * parameter_jahr15
    row3.anzahl_betriebe_jahr_15 = anzahl_betriebe_start * parameter_jahr16
    row3.anzahl_betriebe_jahr_16 = anzahl_betriebe_start * parameter_jahr17
    row3.anzahl_betriebe_jahr_17 = anzahl_betriebe_start * parameter_jahr18
    row3.anzahl_betriebe_jahr_18 = anzahl_betriebe_start * parameter_jahr19
    row3.anzahl_betriebe_jahr_19 = anzahl_betriebe_start * parameter_jahr20
    row3.anzahl_betriebe_jahr_20 = anzahl_betriebe_start * parameter_jahr21
    row3.anzahl_betriebe_jahr_21 = anzahl_betriebe_start * parameter_jahr22
    row3.anzahl_betriebe_jahr_22 = anzahl_betriebe_start * parameter_jahr23
    row3.anzahl_betriebe_jahr_23 = anzahl_betriebe_start * parameter_jahr24
    row3.anzahl_betriebe_jahr_24 = anzahl_betriebe_start * parameter_jahr25
    row3.anzahl_betriebe_jahr_25 = anzahl_betriebe_start * parameter_jahr26
    row3.anzahl_betriebe_jahr_26 = anzahl_betriebe_start * parameter_jahr27
    row3.anzahl_betriebe_jahr_27 = anzahl_betriebe_start * parameter_jahr28
    row3.anzahl_betriebe_jahr_28 = anzahl_betriebe_start * parameter_jahr29
    row3.anzahl_betriebe_jahr_29 = anzahl_betriebe_start * parameter_jahr30
    row3.anzahl_betriebe_jahr_30 = anzahl_betriebe_start * parameter_jahr30
    row3.projekt = projektname
    row3.teilflaeche = teilflaeche
    row3.branche = "C"
    row3.ID_ts = timestamp

    tabelle_gewerbe_betriebsstruktur_Insert.insertRow(row3)

    #für Branche F
    anzahl_betriebe_start = Anz_Betr_BauGew
    aufsiedlungsdauer = str(aufsiedlungsdauer)

    sql = "Dauer_Jahre = " + str(aufsiedlungsdauer)
    row3 = tabelle_gewerbe_betriebsstruktur_Insert.newRow()

    row3.anzahl_betriebe_jahr_0 = anzahl_betriebe_start * parameter_jahr1
    row3.anzahl_betriebe_jahr_1 = anzahl_betriebe_start * parameter_jahr2
    row3.anzahl_betriebe_jahr_2 = anzahl_betriebe_start * parameter_jahr3
    row3.anzahl_betriebe_jahr_3 = anzahl_betriebe_start * parameter_jahr4
    row3.anzahl_betriebe_jahr_4 = anzahl_betriebe_start * parameter_jahr5
    row3.anzahl_betriebe_jahr_5 = anzahl_betriebe_start * parameter_jahr6
    row3.anzahl_betriebe_jahr_6 = anzahl_betriebe_start * parameter_jahr7
    row3.anzahl_betriebe_jahr_7 = anzahl_betriebe_start * parameter_jahr8
    row3.anzahl_betriebe_jahr_8 = anzahl_betriebe_start * parameter_jahr9
    row3.anzahl_betriebe_jahr_9 = anzahl_betriebe_start * parameter_jahr10
    row3.anzahl_betriebe_jahr_10 = anzahl_betriebe_start * parameter_jahr11
    row3.anzahl_betriebe_jahr_11 = anzahl_betriebe_start * parameter_jahr12
    row3.anzahl_betriebe_jahr_12 = anzahl_betriebe_start * parameter_jahr13
    row3.anzahl_betriebe_jahr_13 = anzahl_betriebe_start * parameter_jahr14
    row3.anzahl_betriebe_jahr_14 = anzahl_betriebe_start * parameter_jahr15
    row3.anzahl_betriebe_jahr_15 = anzahl_betriebe_start * parameter_jahr16
    row3.anzahl_betriebe_jahr_16 = anzahl_betriebe_start * parameter_jahr17
    row3.anzahl_betriebe_jahr_17 = anzahl_betriebe_start * parameter_jahr18
    row3.anzahl_betriebe_jahr_18 = anzahl_betriebe_start * parameter_jahr19
    row3.anzahl_betriebe_jahr_19 = anzahl_betriebe_start * parameter_jahr20
    row3.anzahl_betriebe_jahr_20 = anzahl_betriebe_start * parameter_jahr21
    row3.anzahl_betriebe_jahr_21 = anzahl_betriebe_start * parameter_jahr22
    row3.anzahl_betriebe_jahr_22 = anzahl_betriebe_start * parameter_jahr23
    row3.anzahl_betriebe_jahr_23 = anzahl_betriebe_start * parameter_jahr24
    row3.anzahl_betriebe_jahr_24 = anzahl_betriebe_start * parameter_jahr25
    row3.anzahl_betriebe_jahr_25 = anzahl_betriebe_start * parameter_jahr26
    row3.anzahl_betriebe_jahr_26 = anzahl_betriebe_start * parameter_jahr27
    row3.anzahl_betriebe_jahr_27 = anzahl_betriebe_start * parameter_jahr28
    row3.anzahl_betriebe_jahr_28 = anzahl_betriebe_start * parameter_jahr29
    row3.anzahl_betriebe_jahr_29 = anzahl_betriebe_start * parameter_jahr30
    row3.anzahl_betriebe_jahr_30 = anzahl_betriebe_start * parameter_jahr30
    row3.projekt = projektname
    row3.teilflaeche = teilflaeche
    row3.branche = "F"
    row3.ID_ts = timestamp

    tabelle_gewerbe_betriebsstruktur_Insert.insertRow(row3)


    #für Branche G
    anzahl_betriebe_start = Anz_Betr_HanKfZ
    aufsiedlungsdauer = str(aufsiedlungsdauer)

    sql = "Dauer_Jahre = " + str(aufsiedlungsdauer)
    row3 = tabelle_gewerbe_betriebsstruktur_Insert.newRow()

    row3.anzahl_betriebe_jahr_0 = anzahl_betriebe_start * parameter_jahr1
    row3.anzahl_betriebe_jahr_1 = anzahl_betriebe_start * parameter_jahr2
    row3.anzahl_betriebe_jahr_2 = anzahl_betriebe_start * parameter_jahr3
    row3.anzahl_betriebe_jahr_3 = anzahl_betriebe_start * parameter_jahr4
    row3.anzahl_betriebe_jahr_4 = anzahl_betriebe_start * parameter_jahr5
    row3.anzahl_betriebe_jahr_5 = anzahl_betriebe_start * parameter_jahr6
    row3.anzahl_betriebe_jahr_6 = anzahl_betriebe_start * parameter_jahr7
    row3.anzahl_betriebe_jahr_7 = anzahl_betriebe_start * parameter_jahr8
    row3.anzahl_betriebe_jahr_8 = anzahl_betriebe_start * parameter_jahr9
    row3.anzahl_betriebe_jahr_9 = anzahl_betriebe_start * parameter_jahr10
    row3.anzahl_betriebe_jahr_10 = anzahl_betriebe_start * parameter_jahr11
    row3.anzahl_betriebe_jahr_11 = anzahl_betriebe_start * parameter_jahr12
    row3.anzahl_betriebe_jahr_12 = anzahl_betriebe_start * parameter_jahr13
    row3.anzahl_betriebe_jahr_13 = anzahl_betriebe_start * parameter_jahr14
    row3.anzahl_betriebe_jahr_14 = anzahl_betriebe_start * parameter_jahr15
    row3.anzahl_betriebe_jahr_15 = anzahl_betriebe_start * parameter_jahr16
    row3.anzahl_betriebe_jahr_16 = anzahl_betriebe_start * parameter_jahr17
    row3.anzahl_betriebe_jahr_17 = anzahl_betriebe_start * parameter_jahr18
    row3.anzahl_betriebe_jahr_18 = anzahl_betriebe_start * parameter_jahr19
    row3.anzahl_betriebe_jahr_19 = anzahl_betriebe_start * parameter_jahr20
    row3.anzahl_betriebe_jahr_20 = anzahl_betriebe_start * parameter_jahr21
    row3.anzahl_betriebe_jahr_21 = anzahl_betriebe_start * parameter_jahr22
    row3.anzahl_betriebe_jahr_22 = anzahl_betriebe_start * parameter_jahr23
    row3.anzahl_betriebe_jahr_23 = anzahl_betriebe_start * parameter_jahr24
    row3.anzahl_betriebe_jahr_24 = anzahl_betriebe_start * parameter_jahr25
    row3.anzahl_betriebe_jahr_25 = anzahl_betriebe_start * parameter_jahr26
    row3.anzahl_betriebe_jahr_26 = anzahl_betriebe_start * parameter_jahr27
    row3.anzahl_betriebe_jahr_27 = anzahl_betriebe_start * parameter_jahr28
    row3.anzahl_betriebe_jahr_28 = anzahl_betriebe_start * parameter_jahr29
    row3.anzahl_betriebe_jahr_29 = anzahl_betriebe_start * parameter_jahr30
    row3.anzahl_betriebe_jahr_30 = anzahl_betriebe_start * parameter_jahr30
    row3.projekt = projektname
    row3.teilflaeche = teilflaeche
    row3.branche = "G"
    row3.ID_ts = timestamp

    tabelle_gewerbe_betriebsstruktur_Insert.insertRow(row3)


    #für Branche H
    anzahl_betriebe_start = Anz_Betr_VerLag
    aufsiedlungsdauer = str(aufsiedlungsdauer)

    sql = "Dauer_Jahre = " + str(aufsiedlungsdauer)
    row3 = tabelle_gewerbe_betriebsstruktur_Insert.newRow()

    row3.anzahl_betriebe_jahr_0 = anzahl_betriebe_start * parameter_jahr1
    row3.anzahl_betriebe_jahr_1 = anzahl_betriebe_start * parameter_jahr2
    row3.anzahl_betriebe_jahr_2 = anzahl_betriebe_start * parameter_jahr3
    row3.anzahl_betriebe_jahr_3 = anzahl_betriebe_start * parameter_jahr4
    row3.anzahl_betriebe_jahr_4 = anzahl_betriebe_start * parameter_jahr5
    row3.anzahl_betriebe_jahr_5 = anzahl_betriebe_start * parameter_jahr6
    row3.anzahl_betriebe_jahr_6 = anzahl_betriebe_start * parameter_jahr7
    row3.anzahl_betriebe_jahr_7 = anzahl_betriebe_start * parameter_jahr8
    row3.anzahl_betriebe_jahr_8 = anzahl_betriebe_start * parameter_jahr9
    row3.anzahl_betriebe_jahr_9 = anzahl_betriebe_start * parameter_jahr10
    row3.anzahl_betriebe_jahr_10 = anzahl_betriebe_start * parameter_jahr11
    row3.anzahl_betriebe_jahr_11 = anzahl_betriebe_start * parameter_jahr12
    row3.anzahl_betriebe_jahr_12 = anzahl_betriebe_start * parameter_jahr13
    row3.anzahl_betriebe_jahr_13 = anzahl_betriebe_start * parameter_jahr14
    row3.anzahl_betriebe_jahr_14 = anzahl_betriebe_start * parameter_jahr15
    row3.anzahl_betriebe_jahr_15 = anzahl_betriebe_start * parameter_jahr16
    row3.anzahl_betriebe_jahr_16 = anzahl_betriebe_start * parameter_jahr17
    row3.anzahl_betriebe_jahr_17 = anzahl_betriebe_start * parameter_jahr18
    row3.anzahl_betriebe_jahr_18 = anzahl_betriebe_start * parameter_jahr19
    row3.anzahl_betriebe_jahr_19 = anzahl_betriebe_start * parameter_jahr20
    row3.anzahl_betriebe_jahr_20 = anzahl_betriebe_start * parameter_jahr21
    row3.anzahl_betriebe_jahr_21 = anzahl_betriebe_start * parameter_jahr22
    row3.anzahl_betriebe_jahr_22 = anzahl_betriebe_start * parameter_jahr23
    row3.anzahl_betriebe_jahr_23 = anzahl_betriebe_start * parameter_jahr24
    row3.anzahl_betriebe_jahr_24 = anzahl_betriebe_start * parameter_jahr25
    row3.anzahl_betriebe_jahr_25 = anzahl_betriebe_start * parameter_jahr26
    row3.anzahl_betriebe_jahr_26 = anzahl_betriebe_start * parameter_jahr27
    row3.anzahl_betriebe_jahr_27 = anzahl_betriebe_start * parameter_jahr28
    row3.anzahl_betriebe_jahr_28 = anzahl_betriebe_start * parameter_jahr29
    row3.anzahl_betriebe_jahr_29 = anzahl_betriebe_start * parameter_jahr30
    row3.anzahl_betriebe_jahr_30 = anzahl_betriebe_start * parameter_jahr30
    row3.projekt = projektname
    row3.teilflaeche = teilflaeche
    row3.branche = "H"
    row3.ID_ts = timestamp

    tabelle_gewerbe_betriebsstruktur_Insert.insertRow(row3)

    #für Branche M
    anzahl_betriebe_start = Anz_Betr_FrWiTeDi
    aufsiedlungsdauer = str(aufsiedlungsdauer)

    sql = "Dauer_Jahre = " + str(aufsiedlungsdauer)
    row3 = tabelle_gewerbe_betriebsstruktur_Insert.newRow()

    row3.anzahl_betriebe_jahr_0 = anzahl_betriebe_start * parameter_jahr1
    row3.anzahl_betriebe_jahr_1 = anzahl_betriebe_start * parameter_jahr2
    row3.anzahl_betriebe_jahr_2 = anzahl_betriebe_start * parameter_jahr3
    row3.anzahl_betriebe_jahr_3 = anzahl_betriebe_start * parameter_jahr4
    row3.anzahl_betriebe_jahr_4 = anzahl_betriebe_start * parameter_jahr5
    row3.anzahl_betriebe_jahr_5 = anzahl_betriebe_start * parameter_jahr6
    row3.anzahl_betriebe_jahr_6 = anzahl_betriebe_start * parameter_jahr7
    row3.anzahl_betriebe_jahr_7 = anzahl_betriebe_start * parameter_jahr8
    row3.anzahl_betriebe_jahr_8 = anzahl_betriebe_start * parameter_jahr9
    row3.anzahl_betriebe_jahr_9 = anzahl_betriebe_start * parameter_jahr10
    row3.anzahl_betriebe_jahr_10 = anzahl_betriebe_start * parameter_jahr11
    row3.anzahl_betriebe_jahr_11 = anzahl_betriebe_start * parameter_jahr12
    row3.anzahl_betriebe_jahr_12 = anzahl_betriebe_start * parameter_jahr13
    row3.anzahl_betriebe_jahr_13 = anzahl_betriebe_start * parameter_jahr14
    row3.anzahl_betriebe_jahr_14 = anzahl_betriebe_start * parameter_jahr15
    row3.anzahl_betriebe_jahr_15 = anzahl_betriebe_start * parameter_jahr16
    row3.anzahl_betriebe_jahr_16 = anzahl_betriebe_start * parameter_jahr17
    row3.anzahl_betriebe_jahr_17 = anzahl_betriebe_start * parameter_jahr18
    row3.anzahl_betriebe_jahr_18 = anzahl_betriebe_start * parameter_jahr19
    row3.anzahl_betriebe_jahr_19 = anzahl_betriebe_start * parameter_jahr20
    row3.anzahl_betriebe_jahr_20 = anzahl_betriebe_start * parameter_jahr21
    row3.anzahl_betriebe_jahr_21 = anzahl_betriebe_start * parameter_jahr22
    row3.anzahl_betriebe_jahr_22 = anzahl_betriebe_start * parameter_jahr23
    row3.anzahl_betriebe_jahr_23 = anzahl_betriebe_start * parameter_jahr24
    row3.anzahl_betriebe_jahr_24 = anzahl_betriebe_start * parameter_jahr25
    row3.anzahl_betriebe_jahr_25 = anzahl_betriebe_start * parameter_jahr26
    row3.anzahl_betriebe_jahr_26 = anzahl_betriebe_start * parameter_jahr27
    row3.anzahl_betriebe_jahr_27 = anzahl_betriebe_start * parameter_jahr28
    row3.anzahl_betriebe_jahr_28 = anzahl_betriebe_start * parameter_jahr29
    row3.anzahl_betriebe_jahr_29 = anzahl_betriebe_start * parameter_jahr30
    row3.anzahl_betriebe_jahr_30 = anzahl_betriebe_start * parameter_jahr30
    row3.projekt = projektname
    row3.teilflaeche = teilflaeche
    row3.branche = "M"
    row3.ID_ts = timestamp

    tabelle_gewerbe_betriebsstruktur_Insert.insertRow(row3)

    #für Branche N
    anzahl_betriebe_start = Anz_Betr_SoDi
    aufsiedlungsdauer = str(aufsiedlungsdauer)

    sql = "Dauer_Jahre = " + str(aufsiedlungsdauer)
    row3 = tabelle_gewerbe_betriebsstruktur_Insert.newRow()

    row3.anzahl_betriebe_jahr_0 = anzahl_betriebe_start * parameter_jahr1
    row3.anzahl_betriebe_jahr_1 = anzahl_betriebe_start * parameter_jahr2
    row3.anzahl_betriebe_jahr_2 = anzahl_betriebe_start * parameter_jahr3
    row3.anzahl_betriebe_jahr_3 = anzahl_betriebe_start * parameter_jahr4
    row3.anzahl_betriebe_jahr_4 = anzahl_betriebe_start * parameter_jahr5
    row3.anzahl_betriebe_jahr_5 = anzahl_betriebe_start * parameter_jahr6
    row3.anzahl_betriebe_jahr_6 = anzahl_betriebe_start * parameter_jahr7
    row3.anzahl_betriebe_jahr_7 = anzahl_betriebe_start * parameter_jahr8
    row3.anzahl_betriebe_jahr_8 = anzahl_betriebe_start * parameter_jahr9
    row3.anzahl_betriebe_jahr_9 = anzahl_betriebe_start * parameter_jahr10
    row3.anzahl_betriebe_jahr_10 = anzahl_betriebe_start * parameter_jahr11
    row3.anzahl_betriebe_jahr_11 = anzahl_betriebe_start * parameter_jahr12
    row3.anzahl_betriebe_jahr_12 = anzahl_betriebe_start * parameter_jahr13
    row3.anzahl_betriebe_jahr_13 = anzahl_betriebe_start * parameter_jahr14
    row3.anzahl_betriebe_jahr_14 = anzahl_betriebe_start * parameter_jahr15
    row3.anzahl_betriebe_jahr_15 = anzahl_betriebe_start * parameter_jahr16
    row3.anzahl_betriebe_jahr_16 = anzahl_betriebe_start * parameter_jahr17
    row3.anzahl_betriebe_jahr_17 = anzahl_betriebe_start * parameter_jahr18
    row3.anzahl_betriebe_jahr_18 = anzahl_betriebe_start * parameter_jahr19
    row3.anzahl_betriebe_jahr_19 = anzahl_betriebe_start * parameter_jahr20
    row3.anzahl_betriebe_jahr_20 = anzahl_betriebe_start * parameter_jahr21
    row3.anzahl_betriebe_jahr_21 = anzahl_betriebe_start * parameter_jahr22
    row3.anzahl_betriebe_jahr_22 = anzahl_betriebe_start * parameter_jahr23
    row3.anzahl_betriebe_jahr_23 = anzahl_betriebe_start * parameter_jahr24
    row3.anzahl_betriebe_jahr_24 = anzahl_betriebe_start * parameter_jahr25
    row3.anzahl_betriebe_jahr_25 = anzahl_betriebe_start * parameter_jahr26
    row3.anzahl_betriebe_jahr_26 = anzahl_betriebe_start * parameter_jahr27
    row3.anzahl_betriebe_jahr_27 = anzahl_betriebe_start * parameter_jahr28
    row3.anzahl_betriebe_jahr_28 = anzahl_betriebe_start * parameter_jahr29
    row3.anzahl_betriebe_jahr_29 = anzahl_betriebe_start * parameter_jahr30
    row3.anzahl_betriebe_jahr_30 = anzahl_betriebe_start * parameter_jahr30
    row3.projekt = projektname
    row3.teilflaeche = teilflaeche
    row3.branche = "N"
    row3.ID_ts = timestamp

    tabelle_gewerbe_betriebsstruktur_Insert.insertRow(row3)



    #### Aufsiedlugnsdauer Beschäftigte
    # zuletzt die Anzahl noch in die Ausgabetabelle schreiben und dabei mit der Aufsiedlungszeit verrechnen
    tabelle_parameter_aufsiedlungsdauer = os.path.join(base_path,'2_Tool','11_Definition_Projekt','FGDB_11_Definition_Projekt_Tool.gdb','gewerbe_aufsiedlungsdauer')
    tabelle_beschaeftigte = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb','Gewerbe_Beschaeftigte')
    tabelle_beschaeftigte_insert = arcpy.InsertCursor(tabelle_beschaeftigte)
    tabelle_projektrahmendaten = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb','Projektrahmendaten')

    #Beschaeftigte Branche C / Besch_VerarbGew
    anzahl_Besch_max = float(Besch_VerarbGew)
    aufsiedlungsdauer = str(aufsiedlungsdauer)
    tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer)

    rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
    for row in rows_projektrahmen:
        ende = row.Ende_Betrachtungszeitraum
        ende = long(ende) + 1

    anfang = long(startjahr)
    dauer = long(aufsiedlungsdauer)
    jahr = long(startjahr) - 1
    Besch_Jahr = 0
    Besch_Jahr_neu = 0
    row3 = tabelle_beschaeftigte_insert.newRow()
    jahrcount = -1
    jahraufsiedlung = 1
    vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

    for jahr in range(anfang, ende):
        jahrcount = jahrcount + 1
        jahr = jahr + 1
        if jahr < vollaufsiedlung:
            parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
            Besch_Jahr = float(anzahl_Besch_max) * float(parameter_jahr)
            Besch_Jahr = float(Besch_Jahr)
            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
            Besch_Jahr_neu = float(Besch_Jahr_neu)
            jahraufsiedlung = jahraufsiedlung + 1

        else:
            Besch_Jahr = float(anzahl_Besch_max)
            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
            Besch_Jahr_neu = float(Besch_Jahr_neu)

        row3.jahr = long(jahrcount) + long(startjahr)
        row3.Teilflaeche_Plangebiet = str(teilflaeche)
        row3.Branche = "C"
        row3.Anzahl = float(Besch_Jahr)
        row3.Anzahl_neu = float(Besch_Jahr_neu)
        row3.ID_ts = timestamp
        tabelle_beschaeftigte_insert.insertRow(row3)


    #Beschaeftigte Branche F / Besch_BauGew
    anzahl_Besch_max = float(Besch_BauGew)
    aufsiedlungsdauer = str(aufsiedlungsdauer)
    tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer)

    rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
    for row in rows_projektrahmen:
        ende = row.Ende_Betrachtungszeitraum
        ende = long(ende) + 1

    anfang = long(startjahr)
    dauer = long(aufsiedlungsdauer)
    jahr = long(startjahr) - 1
    Besch_Jahr = 0
    Besch_Jahr_neu = 0
    row3 = tabelle_beschaeftigte_insert.newRow()
    jahrcount = -1
    jahraufsiedlung = 1
    vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

    for jahr in range(anfang, ende):
        jahrcount = jahrcount + 1
        jahr = jahr + 1
        if jahr < vollaufsiedlung:
            parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
            Besch_Jahr = float(anzahl_Besch_max) * float(parameter_jahr)
            Besch_Jahr = float(Besch_Jahr)
            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
            Besch_Jahr_neu = float(Besch_Jahr_neu)
            jahraufsiedlung = jahraufsiedlung + 1

        else:
            Besch_Jahr = float(anzahl_Besch_max)
            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
            Besch_Jahr_neu = float(Besch_Jahr_neu)

        row3.jahr = long(jahrcount) + long(startjahr)
        row3.Teilflaeche_Plangebiet = str(teilflaeche)
        row3.Branche = "F"
        row3.Anzahl = float(Besch_Jahr)
        row3.Anzahl_neu = float(Besch_Jahr_neu)
        row3.ID_ts = timestamp
        tabelle_beschaeftigte_insert.insertRow(row3)


    #Beschaeftigte Branche G / Besch_HanKfZ
    anzahl_Besch_max = float(Besch_HanKfZ)
    aufsiedlungsdauer = str(aufsiedlungsdauer)
    tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer)

    rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
    for row in rows_projektrahmen:
        ende = row.Ende_Betrachtungszeitraum
        ende = long(ende) + 1

    anfang = long(startjahr)
    dauer = long(aufsiedlungsdauer)
    jahr = long(startjahr) - 1
    Besch_Jahr = 0
    Besch_Jahr_neu = 0
    row3 = tabelle_beschaeftigte_insert.newRow()
    jahrcount = -1
    jahraufsiedlung = 1
    vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

    for jahr in range(anfang, ende):
        jahrcount = jahrcount + 1
        jahr = jahr + 1
        if jahr < vollaufsiedlung:
            parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
            Besch_Jahr = float(anzahl_Besch_max) * float(parameter_jahr)
            Besch_Jahr = float(Besch_Jahr)
            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
            Besch_Jahr_neu = float(Besch_Jahr_neu)
            jahraufsiedlung = jahraufsiedlung + 1

        else:
            Besch_Jahr = float(anzahl_Besch_max)
            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
            Besch_Jahr_neu = float(Besch_Jahr_neu)

        row3.jahr = long(jahrcount) + long(startjahr)
        row3.Teilflaeche_Plangebiet = str(teilflaeche)
        row3.Branche = "G"
        row3.Anzahl = float(Besch_Jahr)
        row3.Anzahl_neu = float(Besch_Jahr_neu)
        row3.ID_ts = timestamp
        tabelle_beschaeftigte_insert.insertRow(row3)

    Besch_FrWiTeDi = float(Flaeche_Betr_FrWiTeDi) * float(FKZ_FrWiTeDi)
    Besch_SoDi = float(Flaeche_Betr_SoDi) * float(FKZ_SoDi)
    #Beschaeftigte Branche H / Besch_VerLag
    anzahl_Besch_max = float(Besch_VerLag)
    aufsiedlungsdauer = str(aufsiedlungsdauer)
    tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer)

    rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
    for row in rows_projektrahmen:
        ende = row.Ende_Betrachtungszeitraum
        ende = long(ende) + 1

    anfang = long(startjahr)
    dauer = long(aufsiedlungsdauer)
    jahr = long(startjahr) - 1
    Besch_Jahr = 0
    Besch_Jahr_neu = 0
    row3 = tabelle_beschaeftigte_insert.newRow()
    jahrcount = -1
    jahraufsiedlung = 1
    vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

    for jahr in range(anfang, ende):
        jahrcount = jahrcount + 1
        jahr = jahr + 1
        if jahr < vollaufsiedlung:
            parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
            Besch_Jahr = float(anzahl_Besch_max) * float(parameter_jahr)
            Besch_Jahr = float(Besch_Jahr)
            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
            Besch_Jahr_neu = float(Besch_Jahr_neu)
            jahraufsiedlung = jahraufsiedlung + 1

        else:
            Besch_Jahr = float(anzahl_Besch_max)
            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
            Besch_Jahr_neu = float(Besch_Jahr_neu)

        row3.jahr = long(jahrcount) + long(startjahr)
        row3.Teilflaeche_Plangebiet = str(teilflaeche)
        row3.Branche = "H"
        row3.Anzahl = float(Besch_Jahr)
        row3.Anzahl_neu = float(Besch_Jahr_neu)
        row3.ID_ts = timestamp
        tabelle_beschaeftigte_insert.insertRow(row3)


    Besch_SoDi = float(Flaeche_Betr_SoDi) * float(FKZ_SoDi)
    #Beschaeftigte Branche M / Besch_FrWiTeDi
    anzahl_Besch_max = float(Besch_FrWiTeDi)
    aufsiedlungsdauer = str(aufsiedlungsdauer)
    tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer)

    rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
    for row in rows_projektrahmen:
        ende = row.Ende_Betrachtungszeitraum
        ende = long(ende) + 1

    anfang = long(startjahr)
    dauer = long(aufsiedlungsdauer)
    jahr = long(startjahr) - 1
    Besch_Jahr = 0
    Besch_Jahr_neu = 0
    row3 = tabelle_beschaeftigte_insert.newRow()
    jahrcount = -1
    jahraufsiedlung = 1
    vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

    for jahr in range(anfang, ende):
        jahrcount = jahrcount + 1
        jahr = jahr + 1
        if jahr < vollaufsiedlung:
            parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
            Besch_Jahr = float(anzahl_Besch_max) * float(parameter_jahr)
            Besch_Jahr = float(Besch_Jahr)
            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
            Besch_Jahr_neu = float(Besch_Jahr_neu)
            jahraufsiedlung = jahraufsiedlung + 1

        else:
            Besch_Jahr = float(anzahl_Besch_max)
            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
            Besch_Jahr_neu = float(Besch_Jahr_neu)

        row3.jahr = long(jahrcount) + long(startjahr)
        row3.Teilflaeche_Plangebiet = str(teilflaeche)
        row3.Branche = "M"
        row3.Anzahl = float(Besch_Jahr)
        row3.Anzahl_neu = float(Besch_Jahr_neu)
        row3.ID_ts = timestamp
        tabelle_beschaeftigte_insert.insertRow(row3)


    #Beschaeftigte Branche N / Besch_SoDi
    anzahl_Besch_max = float(Besch_SoDi)
    aufsiedlungsdauer = str(aufsiedlungsdauer)
    tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer)

    rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
    for row in rows_projektrahmen:
        ende = row.Ende_Betrachtungszeitraum
        ende = long(ende) + 1

    anfang = long(startjahr)
    dauer = long(aufsiedlungsdauer)
    jahr = long(startjahr) - 1
    Besch_Jahr = 0
    Besch_Jahr_neu = 0
    row3 = tabelle_beschaeftigte_insert.newRow()
    jahrcount = -1
    jahraufsiedlung = 1
    vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

    for jahr in range(anfang, ende):
        jahrcount = jahrcount + 1
        jahr = jahr + 1
        if jahr < vollaufsiedlung:
            parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
            Besch_Jahr = float(anzahl_Besch_max) * float(parameter_jahr)
            Besch_Jahr = float(Besch_Jahr)
            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
            Besch_Jahr_neu = float(Besch_Jahr_neu)
            jahraufsiedlung = jahraufsiedlung + 1

        else:
            Besch_Jahr = float(anzahl_Besch_max)
            Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
            Besch_Jahr_neu = float(Besch_Jahr_neu)

        row3.jahr = long(jahrcount) + long(startjahr)
        row3.Teilflaeche_Plangebiet = str(teilflaeche)
        row3.Branche = "N"
        row3.Anzahl = float(Besch_Jahr)
        row3.Anzahl_neu = float(Besch_Jahr_neu)
        row3.ID_ts = timestamp
        tabelle_beschaeftigte_insert.insertRow(row3)

    ##############################
    ## Gebaeude berechnen

    schrittmeldung = 'Gebaeudedaten werden berechnet \n'
    arcpy.AddMessage(schrittmeldung)
    print str(schrittmeldung)

    tabelle_gebaeudegrundlagen = os.path.join(base_path,'2_Tool','11_Definition_Projekt','FGDB_11_Definition_Projekt_Tool.gdb','gewerbe_gebaeude')
    tabelle_gebaeudedetails = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb','Gebaeude_Details')
    tabelle_gebaeudedetails_insert = arcpy.InsertCursor(tabelle_gebaeudedetails)

    rows_GGF = arcpy.SearchCursor(tabelle_gebaeudegrundlagen)
    GGF_halle = 0
    GGF_verwaltung = 0
    GeVo_halle = 0
    GeVo_verwlatung = 0

    for row in rows_GGF:
        if row.Branche == "C":
            GGF_halle_VerarbGew = float(row.anteil_halle) * float(Flaeche_Betr_VerarbGew)
            GGF_verwaltung_VerarbGew = float(row.anteil_verwaltung) * float(Flaeche_Betr_VerarbGew)
            GeVo_halle_VerarbGew = float(GGF_halle_VerarbGew) * float(row.hoehe_halle)
            GeVo_verwaltung_VerarbGew = float(GGF_verwaltung_VerarbGew) * float(row.hoehe_verwaltung)
            GGF_halle = float(GGF_halle) + float(GGF_halle_VerarbGew)
            GGF_verwaltung = float(GGF_verwaltung) + float(GGF_verwaltung_VerarbGew)
            GeVo_halle = float(GeVo_halle) + float(GeVo_halle_VerarbGew)
            GeVo_verwlatung = float(GeVo_verwlatung) + float(GeVo_verwaltung_VerarbGew)
        if row.Branche == "F":
            GGF_halle_BauGew = float(row.anteil_halle) * float(Flaeche_Betr_BauGew)
            GGF_verwaltung_BauGew = float(row.anteil_verwaltung) * float(Flaeche_Betr_BauGew)
            GeVo_halle_BauGew = float(GGF_halle_BauGew) * float(row.hoehe_halle)
            GeVo_verwaltung_BauGew = float(GGF_verwaltung_BauGew) * float(row.hoehe_verwaltung)
            GGF_halle = float(GGF_halle) + float(GGF_halle_BauGew)
            GGF_verwaltung = float(GGF_verwaltung) + float(GGF_verwaltung_BauGew)
            GeVo_halle = float(GeVo_halle) + float(GeVo_halle_BauGew)
            GeVo_verwlatung = float(GeVo_verwlatung) + float(GeVo_verwaltung_BauGew)
        if row.Branche == "G":
            GGF_halle_HanKfZ = float(row.anteil_halle) * float(Flaeche_Betr_HanKfZ)
            GGF_verwaltung_HanKfZ = float(row.anteil_verwaltung) * float(Flaeche_Betr_HanKfZ)
            GeVo_halle_HanKfZ = float(GGF_halle_HanKfZ) * float(row.hoehe_halle)
            GeVo_verwaltung_HanKfZ = float(GGF_verwaltung_HanKfZ) * float(row.hoehe_verwaltung)
            GGF_halle = float(GGF_halle) + float(GGF_halle_HanKfZ)
            GGF_verwaltung = float(GGF_verwaltung) + float(GGF_verwaltung_HanKfZ)
            GeVo_halle = float(GeVo_halle) + float(GeVo_halle_HanKfZ)
            GeVo_verwlatung = float(GeVo_verwlatung) + float(GeVo_verwaltung_HanKfZ)
        if row.Branche == "H":
            GGF_halle_VerLag = float(row.anteil_halle) * float(Flaeche_Betr_VerLag)
            GGF_verwaltung_VerLag = float(row.anteil_verwaltung) * float(Flaeche_Betr_VerLag)
            GeVo_halle_VerLag = float(GGF_halle_VerLag) * float(row.hoehe_halle)
            GeVo_verwaltung_VerLag = float(GGF_verwaltung_VerLag) * float(row.hoehe_verwaltung)
            GGF_halle = float(GGF_halle) + float(GGF_halle_VerLag)
            GGF_verwaltung = float(GGF_verwaltung) + float(GGF_verwaltung_VerLag)
            GeVo_halle = float(GeVo_halle) + float(GeVo_halle_VerLag)
            GeVo_verwlatung = float(GeVo_verwlatung) + float(GeVo_verwaltung_VerLag)
        if row.Branche == "M":
            GGF_halle_FrWiTeDi = float(row.anteil_halle) * float(Flaeche_Betr_FrWiTeDi)
            GGF_verwaltung_FrWiTeDi = float(row.anteil_verwaltung) * float(Flaeche_Betr_FrWiTeDi)
            GeVo_halle_FrWiTeDi = float(GGF_halle_FrWiTeDi) * float(row.hoehe_halle)
            GeVo_verwaltung_FrWiTeDi = float(GGF_verwaltung_FrWiTeDi) * float(row.hoehe_verwaltung)
            GGF_halle = float(GGF_halle) + float(GGF_halle_FrWiTeDi)
            GGF_verwaltung = float(GGF_verwaltung) + float(GGF_verwaltung_FrWiTeDi)
            GeVo_halle = float(GeVo_halle) + float(GeVo_halle_FrWiTeDi)
            GeVo_verwlatung = float(GeVo_verwlatung) + float(GeVo_verwaltung_FrWiTeDi)
        if row.Branche == "N":
            GGF_halle_SoDi = float(row.anteil_halle) * float(Flaeche_Betr_SoDi)
            GGF_verwaltung_SoDi = float(row.anteil_verwaltung) * float(Flaeche_Betr_SoDi)
            GeVo_halle_SoDi = float(GGF_halle_SoDi) * float(row.hoehe_halle)
            GeVo_verwaltung_SoDi = float(GGF_verwaltung_SoDi) * float(row.hoehe_verwaltung)
            GGF_halle = float(GGF_halle) + float(GGF_halle_SoDi)
            GGF_verwaltung = float(GGF_verwaltung) + float(GGF_verwaltung_SoDi)
            GeVo_halle = float(GeVo_halle) + float(GeVo_halle_SoDi)
            GeVo_verwlatung = float(GeVo_verwlatung) + float(GeVo_verwaltung_SoDi)


    ## Gebaeude für Hallen nach Aufsiedlugnszeit berechnen
    aufsiedlungsdauer = str(aufsiedlungsdauer)
    rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
    for row in rows_projektrahmen:
        ende = row.Ende_Betrachtungszeitraum
        ende = long(ende) + 1

    anfang = long(startjahr)
    dauer = long(aufsiedlungsdauer)
    jahr = long(startjahr) - 1
    GGF_jahr = 0
    GeVo_jahr = 0
    grundstuecksflaeche_jahr = 0

    rowGeb = tabelle_gebaeudedetails_insert.newRow()
    jahrcount = -1
    jahraufsiedlung = 1
    vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

    for jahr in range(anfang, ende):
        jahrcount = jahrcount + 1
        jahr = jahr + 1
        if jahr < vollaufsiedlung:
            parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
            GGF_jahr = float(GGF_halle) * float(parameter_jahr) * 10000
            GeVo_jahr = float(GeVo_halle) * float(parameter_jahr) * 10000
            grundstuecksflaeche_jahr = float(gewerbebauland) * float(parameter_jahr) * 10000
            jahraufsiedlung = jahraufsiedlung + 1
        else:
            GGF_jahr = float(GGF_halle) * 10000
            GeVo_jahr = float(GeVo_halle) * 10000
            grundstuecksflaeche_jahr = float(gewerbebauland) * 10000

        rowGeb.jahr = long(jahrcount) + long(startjahr)
        rowGeb.Teilflaeche_Plangebiet = str(teilflaeche)
        rowGeb.Gebaeudetyp = "Hallen"
        rowGeb.Grundstuecksflaeche_qm = float(grundstuecksflaeche_jahr)
        rowGeb.Ueberbaute_Flaeche = float(GGF_jahr)
        rowGeb.Bruttorauminhalt_m3 = float(GeVo_jahr)
        rowGeb.Geb_ID = timestamp

        tabelle_gebaeudedetails_insert.insertRow(rowGeb)

    ## Gebaeude für Bürogebaude nach Aufsiedlugnszeit berechnen
    aufsiedlungsdauer = str(aufsiedlungsdauer)
    rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
    for row in rows_projektrahmen:
        ende = row.Ende_Betrachtungszeitraum
        ende = long(ende) + 1

    anfang = long(startjahr)
    dauer = long(aufsiedlungsdauer)
    jahr = long(startjahr) - 1
    GGF_jahr = 0
    GeVo_jahr = 0
    grundstuecksflaeche_jahr = 0


    rowGeb = tabelle_gebaeudedetails_insert.newRow()
    jahrcount = -1
    jahraufsiedlung = 1
    vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

    for jahr in range(anfang, ende):
        jahrcount = jahrcount + 1
        jahr = jahr + 1
        if jahr < vollaufsiedlung:
            parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
            GGF_jahr = float(GGF_verwaltung) * float(parameter_jahr) * 10000
            GeVo_jahr = float(GeVo_verwlatung) * float(parameter_jahr) * 10000
            grundstuecksflaeche_jahr = float(gewerbebauland) * float(parameter_jahr) * 10000
            jahraufsiedlung = jahraufsiedlung + 1
        else:
            GGF_jahr = float(GGF_verwaltung) * 10000
            GeVo_jahr = float(GeVo_verwlatung) * 10000
            grundstuecksflaeche_jahr = float(gewerbebauland) * 10000

        rowGeb.jahr = long(jahrcount) + long(startjahr)
        rowGeb.Teilflaeche_Plangebiet = str(teilflaeche)
        rowGeb.Gebaeudetyp = "Buerogebaeude"
        rowGeb.Grundstuecksflaeche_qm = float(grundstuecksflaeche_jahr)
        rowGeb.Ueberbaute_Flaeche = float(GGF_jahr)
        rowGeb.Bruttorauminhalt_m3 = float(GeVo_jahr)
        rowGeb.Geb_ID = timestamp

        tabelle_gebaeudedetails_insert.insertRow(rowGeb)

    ###############################
    ## Tabelle Gewerbe_teilflaechen fuellen

    schrittmeldung = 'Projektinformationen werden zusammengefasst und in Datenbank geschrieben \n'
    arcpy.AddMessage(schrittmeldung)
    print str(schrittmeldung)

    tabelle_teilflaeche = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb','Gewerbe_Teilflaechen')
    tabelle_teilflaeche_insert = arcpy.InsertCursor(tabelle_teilflaeche)
    rowTF = tabelle_teilflaeche_insert.newRow()

    # Zeile für Branche C / VerarbGew
    rowTF.teilflaeche = str(teilflaeche)
    rowTF.gebietstyp = str(gebtyp)
    rowTF.branche = "C"
    rowTF.aufsiedlungsdauer = long(aufsiedlungsdauer)
    rowTF.zuzugsquote = long(zuzugsquote)
    rowTF.nettobauland = float(gewerbebauland)
    rowTF.bruttoflaeche = float(flaechengroesse)
    rowTF.beschaeftigte = float(Besch_VerarbGew)
    rowTF.anzahlBetriebe = int(Anz_Betr_VerarbGew)
    rowTF.timestamp = timestamp

    tabelle_teilflaeche_insert.insertRow(rowTF)

    # Zeile für Branche F / BauGew
    rowTF.teilflaeche = str(teilflaeche)
    rowTF.gebietstyp = str(gebtyp)
    rowTF.branche = "F"
    rowTF.aufsiedlungsdauer = long(aufsiedlungsdauer)
    rowTF.zuzugsquote = long(zuzugsquote)
    rowTF.nettobauland = float(gewerbebauland)
    rowTF.bruttoflaeche = float(flaechengroesse)
    rowTF.beschaeftigte = float(Besch_BauGew)
    rowTF.anzahlBetriebe = int(Anz_Betr_BauGew)
    rowTF.timestamp = timestamp

    tabelle_teilflaeche_insert.insertRow(rowTF)

    # Zeile für Branche G / HanKfZ
    rowTF.teilflaeche = str(teilflaeche)
    rowTF.gebietstyp = str(gebtyp)
    rowTF.branche = "G"
    rowTF.aufsiedlungsdauer = long(aufsiedlungsdauer)
    rowTF.zuzugsquote = long(zuzugsquote)
    rowTF.nettobauland = float(gewerbebauland)
    rowTF.bruttoflaeche = float(flaechengroesse)
    rowTF.beschaeftigte = float(Besch_HanKfZ)
    rowTF.anzahlBetriebe = int(Anz_Betr_HanKfZ)
    rowTF.timestamp = timestamp

    tabelle_teilflaeche_insert.insertRow(rowTF)

    # Zeile für Branche H / VerLag
    rowTF.teilflaeche = str(teilflaeche)
    rowTF.gebietstyp = str(gebtyp)
    rowTF.branche = "H"
    rowTF.aufsiedlungsdauer = long(aufsiedlungsdauer)
    rowTF.zuzugsquote = long(zuzugsquote)
    rowTF.nettobauland = float(gewerbebauland)
    rowTF.bruttoflaeche = float(flaechengroesse)
    rowTF.beschaeftigte = float(Besch_VerLag)
    rowTF.anzahlBetriebe = int(Anz_Betr_VerLag)
    rowTF.timestamp = timestamp

    tabelle_teilflaeche_insert.insertRow(rowTF)

    # Zeile für Branche M / FrWiTeDi
    rowTF.teilflaeche = str(teilflaeche)
    rowTF.gebietstyp = str(gebtyp)
    rowTF.branche = "M"
    rowTF.aufsiedlungsdauer = long(aufsiedlungsdauer)
    rowTF.zuzugsquote = long(zuzugsquote)
    rowTF.nettobauland = float(gewerbebauland)
    rowTF.bruttoflaeche = float(flaechengroesse)
    rowTF.beschaeftigte = float(Besch_FrWiTeDi)
    rowTF.anzahlBetriebe = int(Anz_Betr_FrWiTeDi)
    rowTF.timestamp = timestamp

    tabelle_teilflaeche_insert.insertRow(rowTF)

    # Zeile für Branche N / SoDi
    rowTF.teilflaeche = str(teilflaeche)
    rowTF.gebietstyp = str(gebtyp)
    rowTF.branche = "N"
    rowTF.aufsiedlungsdauer = long(aufsiedlungsdauer)
    rowTF.zuzugsquote = long(zuzugsquote)
    rowTF.nettobauland = float(gewerbebauland)
    rowTF.bruttoflaeche = float(flaechengroesse)
    rowTF.beschaeftigte = float(Besch_SoDi)
    rowTF.anzahlBetriebe = int(Anz_Betr_SoDi)
    rowTF.timestamp = timestamp

    tabelle_teilflaeche_insert.insertRow(rowTF)

    schrittmeldung = 'Die Berechnungen sind abgeschlossen  \n'
    arcpy.AddMessage(schrittmeldung)
    print str(schrittmeldung)










##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
## Ergebnisausgabe
    schrittmeldung = 'Die Ergebnisausgabe wird erzeugt. Dies kann wenige Minuten in Anspruch nehmen. \n'
    arcpy.AddMessage(schrittmeldung)
    print str(schrittmeldung)

    # Pfade setzen
    base_path = str(sys.path[0]).split("2_Tool")[0]
    workspace_projekt_gewerbe = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
    tablepath_gewerbe = os.path.join(workspace_projekt_gewerbe,'Gewerbe_Teilflaechen')
    tablepath_Beschaeftigte = os.path.join(workspace_projekt_gewerbe,'Gewerbe_Beschaeftigte')
    tablepath_Flaechenbilanz = os.path.join(workspace_projekt_gewerbe,'Flaechenbilanz_Planung_Prozent')
    tablepath_Gebaeude = os.path.join(workspace_projekt_gewerbe,'Gebaeude_Details')
    tablepath_Betriebe = os.path.join(workspace_projekt_gewerbe,'Gewerbe_Betriebsstruktur')
    grafikpath_erlauterungstext = os.path.join(base_path,'2_Tool','11_Definition_Projekt','Erlauterungstexte')

    logo = os.path.join((str(sys.path[0]).split("2_Tool")[0]),"1_Basisdaten","logo_rpc.png")
    ausgabeordner = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Excel')
    excelpfad = os.path.join(ausgabeordner,'11_Projektdefinition_Gewerbe.xlsx')

    try:
        os.remove(excelpfad)
    except:
        pass

    # Workbook und Tabellenblätter anlegen
    wb = xlsxwriter.Workbook(excelpfad)
    sl.infosheet(projektname, str("Projektinformation").decode('utf-8'), wb)
    ws2 = wb.add_worksheet('Erlaeuterungen')
    ws3 = wb.add_worksheet('Tabellen')
    ws4 = wb.add_worksheet('Grafiken')
    ws5 = wb.add_worksheet('Rohdaten')

    ##Styles anlegen
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

    formatDez = wb.add_format()
    formatDez.set_num_format(0x02)
    formatDez.set_bg_color('white')
    formatDez.set_border(0)

    formatDez1 = wb.add_format()
    formatDez1.set_num_format(0x01)
    formatDez1.set_bg_color('white')
    formatDez1.set_border(0)

    ###Hintergrund weiss faerben
    format = wb.add_format()
    format.set_bg_color('white')
    format.set_border(0)


    for x in range(0,200):
        for y in range(0,200):
            ws2.write(x,y,"", format)
            ws3.write(x,y,"", format)
            ws4.write(x,y,"", format)
            ws5.write(x,y,"", format)

    ###Spaltenbreiten definieren
    ws2.set_column(0, 0, 86)
    for x in range(0,200):
        ws3.set_column(x, 0, 10)
    ws4.set_column(0, 0, 75)

    ### ToDo: Für Überschriften im Tabellenblatt noch Zellen zusammenfügen und grau einfärben

    ########
    ## Erläuterungstexte einfügen
    # Pfade zu Grafiken herstellen und einfügen
    Erlaeuterung = os.path.join(grafikpath_erlauterungstext, 'Gewerbe.png')
    # ws2.insert_image(0, 0, Erlaeuterung, {'x_scale': 0.32, 'y_scale': 0.32})

    ###### Tabellenblatt 5: Rohdaten einladen
    ## Rohdaten tablepath_gewerbe
    #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
    rows = arcpy.SearchCursor(tablepath_gewerbe)
    #Feldnamen auslesen
    fieldnames = [f.name for f in arcpy.ListFields(tablepath_gewerbe)]

    j = 1
    for row in rows:
        i = 0
        for fieldname in fieldnames:
            try:
                wert = string(row.getValue(fieldname))
            except:
                wert = row.getValue(fieldname)
            ws5.write(j, i, wert,formatDez)
            i = i+1

        j = j+1


    #Felder als Header in Worksheet einfuegen
    i = 0
    for fieldname in fieldnames:
        column_with = len(fieldname)+2
        ws5.set_column(i, i, column_with)
        ws5.write(0, i, fieldname, bold)
        i = i+1


    ## Rohdaten tablepath_Beschaeftigte
    #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
    rows = arcpy.SearchCursor(tablepath_Beschaeftigte)
    #Feldnamen auslesen
    fieldnames = [f.name for f in arcpy.ListFields(tablepath_Beschaeftigte)]

    irestart = i + 2

    j = 1
    for row in rows:
        i = irestart
        for fieldname in fieldnames:
            try:
                wert = string(row.getValue(fieldname))
            except:
                wert = row.getValue(fieldname)
            ws5.write(j, i, wert,formatDez)
            i = i+1

        j = j+1

    #Felder als Header in Worksheet einfuegen
    i = irestart
    for fieldname in fieldnames:
        column_with = len(fieldname)+2
        ws5.set_column(i, i, column_with)
        ws5.write(0, i, fieldname, bold)
        i = i+1


    ## Rohdaten tablepath_Flaechenbilanz
    #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
    rows = arcpy.SearchCursor(tablepath_Flaechenbilanz)
    #Feldnamen auslesen
    fieldnames = [f.name for f in arcpy.ListFields(tablepath_Flaechenbilanz)]

    irestart = i + 2

    j = 1
    for row in rows:
        i = irestart
        for fieldname in fieldnames:
            try:
                wert = string(row.getValue(fieldname))
            except:
                wert = row.getValue(fieldname)
            ws5.write(j, i, wert,formatDez)
            i = i+1

        j = j+1

    #Felder als Header in Worksheet einfuegen
    i = irestart
    for fieldname in fieldnames:
        column_with = len(fieldname)+2
        ws5.set_column(i, i, column_with)
        ws5.write(0, i, fieldname, bold)
        i = i+1


    ## Rohdaten tablepath_Gebaeude
    #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
    rows = arcpy.SearchCursor(tablepath_Gebaeude)
    #Feldnamen auslesen
    fieldnames = [f.name for f in arcpy.ListFields(tablepath_Gebaeude)]

    irestart = i + 2

    j = 1
    for row in rows:
        i = irestart
        for fieldname in fieldnames:
            try:
                wert = string(row.getValue(fieldname))
            except:
                wert = row.getValue(fieldname)
            ws5.write(j, i, wert,formatDez)
            i = i+1

        j = j+1

    #Felder als Header in Worksheet einfuegen
    i = irestart
    for fieldname in fieldnames:
        column_with = len(fieldname)+2
        ws5.set_column(i, i, column_with)
        ws5.write(0, i, fieldname, bold)
        i = i+1



    ## Rohdaten tablepath_Betriebe
    #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
    rows = arcpy.SearchCursor(tablepath_Betriebe)
    #Feldnamen auslesen
    fieldnames = [f.name for f in arcpy.ListFields(tablepath_Betriebe)]

    irestart = i + 2

    j = 1
    for row in rows:
        i = irestart
        for fieldname in fieldnames:
            try:
                wert = string(row.getValue(fieldname))
            except:
                wert = row.getValue(fieldname)
            ws5.write(j, i, wert,formatDez)
            i = i+1

        j = j+1

    #Felder als Header in Worksheet einfuegen
    i = irestart
    for fieldname in fieldnames:
        column_with = len(fieldname)+2
        ws5.set_column(i, i, column_with)
        ws5.write(0, i, fieldname, bold)
        i = i+1


    ###### Tabellenblatt 3: Tabellen erstellen
    ## Tabelle Projektuebersicht
    j = 0
    i = 0
    ws3.write(j, i, 'Projektuebersicht', bold)
    j = j + 1
    ws3.write(j, i, 'Teilflaeche', bold)
    i = i + 1
    ws3.write(j, i, 'Gebietstyp', bold)
    i = i + 1
    ws3.write(j, i, 'Aufsiedlungsdauer [Jahre]', bold)
    i = i + 1
    ws3.write(j, i, 'Zuzugsquote [%]', bold)
    i = i + 1
    ws3.write(j, i, 'Nettobauland [Hektar]', bold)
    i = i + 1
    ws3.write(j, i, 'Bruttobauland [Hektar]', bold)
    i = i + 1
    ws3.write(j, i, 'Beschaeftigte', bold)
    i = i + 1
    ws3.write(j, i, 'Betriebe', bold)
    i = i + 1
    ws3.write(j, i, 'Branche', bold)
    j = j + 1
    i = 0
    for x in range(2,8):
        cell = xl_rowcol_to_cell(j-1,i+1)
        ws3.write(j, i, '=Rohdaten!'+cell+'', normal)
        i = i + 1
        cell = xl_rowcol_to_cell(j-1,i+1)
        ws3.write(j, i, '=Rohdaten!'+cell+'', normal)
        i = i + 1
        cell = xl_rowcol_to_cell(j-1,i+1)
        ws3.write(j, i, '=Rohdaten!'+cell+'', formatDez1)
        i = i + 1
        cell = xl_rowcol_to_cell(j-1,i+1)
        ws3.write(j, i, '=Rohdaten!'+cell+'', formatDez1)
        i = i + 1
        cell = xl_rowcol_to_cell(j-1,i+1)
        ws3.write(j, i, '=Rohdaten!'+cell+'', formatDez)
        i = i + 1
        cell = xl_rowcol_to_cell(j-1,i+1)
        ws3.write(j, i, '=Rohdaten!'+cell+'', formatDez)
        i = i + 1
        cell = xl_rowcol_to_cell(j-1,i+1)
        ws3.write(j, i, '=Rohdaten!'+cell+'', formatDez1)
        i = i + 1
        cell = xl_rowcol_to_cell(j-1,i+1)
        ws3.write(j, i, '=Rohdaten!'+cell+'', formatDez)
        i = i + 1
        cell = xl_rowcol_to_cell(j-1,i+1)
        ws3.write(j, i, '=Rohdaten!'+cell+'', normal)
        i = 0
        j = j + 1

    ## Tabelle Beschäftigte
    j = j + 2
    i = 0
    ws3.write(j, i, 'Beschaeftigte', bold)
    j = j + 1
    ws3.write(j, i, 'Branche', bold)
    i = i + 1
    ws3.write(j, i, '=MIN(Rohdaten!O:O)', bold)
    for x in range(2, 32):
        i = i + 1
        jahrcell = xl_rowcol_to_cell(j,i-1)
        ws3.write(j, i, '='+jahrcell+'+1', bold)
    j = j + 1
    i = 1
    ws3.write(j, 0, 'C', normal)
    zellebranche = xl_rowcol_to_cell(j,0)
    zeilejahr = j - 1
    for x in range(2, 33):
        spaltejahr = x - 1
        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
        ws3.write(j, i, '=SUMIFS(Rohdaten!$R:$R,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
        i = i + 1
    j = j + 1
    i = 1
    ws3.write(j, 0, 'F', normal)
    zellebranche = xl_rowcol_to_cell(j,0)
    for x in range(2, 33):
        spaltejahr = x - 1
        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
        ws3.write(j, i, '=SUMIFS(Rohdaten!$R:$R,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
        i = i + 1
    j = j + 1
    i = 1
    ws3.write(j, 0, 'G', normal)
    zellebranche = xl_rowcol_to_cell(j,0)
    for x in range(2, 33):
        spaltejahr = x - 1
        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
        ws3.write(j, i, '=SUMIFS(Rohdaten!$R:$R,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
        i = i + 1
    j = j + 1
    i = 1
    ws3.write(j, 0, 'H', normal)
    zellebranche = xl_rowcol_to_cell(j,0)
    for x in range(2, 33):
        spaltejahr = x - 1
        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
        ws3.write(j, i, '=SUMIFS(Rohdaten!$R:$R,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
        i = i + 1
    j = j + 1
    i = 1
    ws3.write(j, 0, 'M', normal)
    zellebranche = xl_rowcol_to_cell(j,0)
    for x in range(2, 33):
        spaltejahr = x - 1
        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
        ws3.write(j, i, '=SUMIFS(Rohdaten!$R:$R,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
        i = i + 1
    j = j + 1
    i = 1
    ws3.write(j, 0, 'N', normal)
    zellebranche = xl_rowcol_to_cell(j,0)
    for x in range(2, 33):
        spaltejahr = x - 1
        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
        ws3.write(j, i, '=SUMIFS(Rohdaten!$R:$R,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
        i = i + 1
    j = j + 1


    ## Tabelle Neue Beschaeftigte
    j = j + 2
    i = 0
    ws3.write(j, i, 'Neue Beschaeftigte', bold)
    j = j + 1
    ws3.write(j, i, 'Branche', bold)
    i = i + 1
    jahrcellbetrieb = xl_rowcol_to_cell(j,i)
    ws3.write(j, i, '=MIN(Rohdaten!O:O)', bold)
    i = 1
    for x in range(2, 32):
        i = i + 1
        jahrcell = xl_rowcol_to_cell(j,i-1)
        ws3.write(j, i, '='+jahrcell+'+1', bold)
    j = j + 1
    i = 1
    ws3.write(j, 0, 'C', normal)
    zellebranche = xl_rowcol_to_cell(j,0)
    zeilejahr = j - 1
    for x in range(2, 33):
        spaltejahr = x - 1
        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
        ws3.write(j, i, '=SUMIFS(Rohdaten!$S:$S,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
        i = i + 1
    j = j + 1
    i = 1
    ws3.write(j, 0, 'F', normal)
    zellebranche = xl_rowcol_to_cell(j,0)
    for x in range(2, 32):
        spaltejahr = x - 1
        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
        ws3.write(j, i, '=SUMIFS(Rohdaten!$S:$S,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
        i = i + 1
    j = j + 1
    i = 1
    ws3.write(j, 0, 'G', normal)
    zellebranche = xl_rowcol_to_cell(j,0)
    for x in range(2, 33):
        spaltejahr = x - 1
        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
        ws3.write(j, i, '=SUMIFS(Rohdaten!$S:$S,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
        i = i + 1
    j = j + 1
    i = 1
    ws3.write(j, 0, 'H', normal)
    zellebranche = xl_rowcol_to_cell(j,0)
    for x in range(2, 33):
        spaltejahr = x - 1
        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
        ws3.write(j, i, '=SUMIFS(Rohdaten!$S:$S,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
        i = i + 1
    j = j + 1
    i = 1
    ws3.write(j, 0, 'M', normal)
    zellebranche = xl_rowcol_to_cell(j,0)
    for x in range(2, 33):
        spaltejahr = x - 1
        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
        ws3.write(j, i, '=SUMIFS(Rohdaten!$S:$S,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
        i = i + 1
    j = j + 1
    i = 1
    ws3.write(j, 0, 'N', normal)
    zellebranche = xl_rowcol_to_cell(j,0)
    for x in range(2, 33):
        spaltejahr = x - 1
        jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
        ws3.write(j, i, '=SUMIFS(Rohdaten!$S:$S,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
        i = i + 1
    j = j + 1


    ## Tabelle Betriebe
    j = j + 2
    i = 0
    ws3.write(j, i, 'Betriebe', bold)
    j = j + 1
    ws3.write(j, i, 'Branche', bold)
    i = i + 1
    ws3.write(j, i, '='+jahrcellbetrieb+'', bold)
    i = 1
    for x in range(2, 32):
        i = i + 1
        jahrcell = xl_rowcol_to_cell(j,i-1)
        ws3.write(j, i, '='+jahrcell+'+1', bold)
    bracol = xl_col_to_name(46)
    colcount = 46
    jahrcol = xl_col_to_name(colcount)
    j = j + 1
    i = 1

    ws3.write(j, 0, 'C', normal)
    zellebranche = xl_rowcol_to_cell(j,0)
    for x in range(2, 33):
        colcount = colcount + 1
        jahrcol = xl_col_to_name(colcount)
        spaltejahr = x - 1
        ws3.write(j, i, '=SUMIF(Rohdaten!'+bracol+':'+bracol+',Tabellen!'+zellebranche+',Rohdaten!'+jahrcol+':'+jahrcol+')', formatDez)
        i = i + 1
    j = j + 1
    i = 1

    ws3.write(j, 0, 'F', normal)
    zellebranche = xl_rowcol_to_cell(j,0)
    colcount = 46
    for x in range(2, 33):
        colcount = colcount + 1
        jahrcol = xl_col_to_name(colcount)
        spaltejahr = x - 1
        ws3.write(j, i, '=SUMIF(Rohdaten!'+bracol+':'+bracol+',Tabellen!'+zellebranche+',Rohdaten!'+jahrcol+':'+jahrcol+')', formatDez)
        i = i + 1
    j = j + 1
    i = 1

    ws3.write(j, 0, 'G', normal)
    zellebranche = xl_rowcol_to_cell(j,0)
    colcount = 46
    for x in range(2, 33):
        colcount = colcount + 1
        jahrcol = xl_col_to_name(colcount)
        spaltejahr = x - 1
        ws3.write(j, i, '=SUMIF(Rohdaten!'+bracol+':'+bracol+',Tabellen!'+zellebranche+',Rohdaten!'+jahrcol+':'+jahrcol+')', formatDez)
        i = i + 1
    j = j + 1
    i = 1

    ws3.write(j, 0, 'H', normal)
    zellebranche = xl_rowcol_to_cell(j,0)
    colcount = 46
    for x in range(2, 33):
        colcount = colcount + 1
        jahrcol = xl_col_to_name(colcount)
        spaltejahr = x - 1
        ws3.write(j, i, '=SUMIF(Rohdaten!'+bracol+':'+bracol+',Tabellen!'+zellebranche+',Rohdaten!'+jahrcol+':'+jahrcol+')', formatDez)
        i = i + 1
    j = j + 1
    i = 1

    ws3.write(j, 0, 'M', normal)
    zellebranche = xl_rowcol_to_cell(j,0)
    colcount = 46
    for x in range(2, 33):
        colcount = colcount + 1
        jahrcol = xl_col_to_name(colcount)
        spaltejahr = x - 1
        ws3.write(j, i, '=SUMIF(Rohdaten!'+bracol+':'+bracol+',Tabellen!'+zellebranche+',Rohdaten!'+jahrcol+':'+jahrcol+')', formatDez)
        i = i + 1
    j = j + 1
    i = 1

    ws3.write(j, 0, 'N', normal)
    zellebranche = xl_rowcol_to_cell(j,0)
    colcount = 46
    for x in range(2, 33):
        colcount = colcount + 1
        jahrcol = xl_col_to_name(colcount)
        spaltejahr = x - 1
        ws3.write(j, i, '=SUMIF(Rohdaten!'+bracol+':'+bracol+',Tabellen!'+zellebranche+',Rohdaten!'+jahrcol+':'+jahrcol+')', formatDez)
        i = i + 1
    j = j + 1
    i = 1

###### Charts anlegen
    # Chart Branchenstruktur anlegen
    chart_Branchenstruktur = wb.add_chart({'type': 'bar', 'subtype': 'percent_stacked'})
    chart_Branchenstruktur.set_style(40)
    chart_Branchenstruktur.set_size({'width': 529, 'height': 226})
    chart_Branchenstruktur.set_chartarea({'border': {'none': True},'fill': {'none': True}})
    chart_Branchenstruktur.set_legend({'position': 'right'})
    chart_Branchenstruktur.set_title({'name': 'Branchenstruktur','name_font':  {'name': 'Calibri', 'size': 12}})

    # Werte in Chartobjekte schreiben
    chart_Branchenstruktur.add_series({
        'values': "=Tabellen!$G$3:$H$3",
        'categories': "=Tabellen!$G$2:$H$2",
        'name': "=Tabellen!$I$3",
    })
    chart_Branchenstruktur.add_series({
        'values': "=Tabellen!$G$4:$H$4",
        'categories': "=Tabellen!$G$2:$H$2",
        'name': "=Tabellen!$I$4",
    })
    chart_Branchenstruktur.add_series({
        'values': "=Tabellen!$G$5:$H$5",
        'categories': "=Tabellen!$G$2:$H$2",
        'name': "=Tabellen!$I$5",
    })
    chart_Branchenstruktur.add_series({
        'values': "=Tabellen!$G$6:$H$6",
        'categories': "=Tabellen!$G$2:$H$2",
        'name': "=Tabellen!$I$6",
    })
    chart_Branchenstruktur.add_series({
        'values': "=Tabellen!$G$7:$H$7",
        'categories': "=Tabellen!$G$2:$H$2",
        'name': "=Tabellen!$I$7",
    })
    chart_Branchenstruktur.add_series({
        'values': "=Tabellen!$G$8:$H$8",
        'categories': "=Tabellen!$G$2:$H$2",
        'name': "=Tabellen!$I$8",
    })

    # Chart Beschaeftigte anlegen
    chart_Beschaeftigte = wb.add_chart({'type': 'bar'})
    chart_Beschaeftigte.set_style(40)
    chart_Beschaeftigte.set_size({'width': 529, 'height': 283})
    chart_Beschaeftigte.set_chartarea({'border': {'none': True},'fill': {'none': True}})
    chart_Beschaeftigte.set_title({'name': 'Beschaeftigte nach Branche','name_font':  {'name': 'Calibri', 'size': 12}})
    chart_Beschaeftigte.set_legend({'none': True})

    # Werte in Chartobjekte schreiben
    chart_Beschaeftigte.add_series({
        'values': "=Tabellen!$G$3:$G$8",
        'categories': "=Tabellen!$I$3:$I$8",
    })

    # Chart Betriebe anlegen
    chart_Betriebe = wb.add_chart({'type': 'bar'})
    chart_Betriebe.set_style(40)
    chart_Betriebe.set_size({'width': 529, 'height': 283})
    chart_Betriebe.set_chartarea({'border': {'none': True},'fill': {'none': True}})
    chart_Betriebe.set_title({'name': 'Betriebe nach Branche','name_font':  {'name': 'Calibri', 'size': 12}})
    chart_Betriebe.set_legend({'none': True})

    # Werte in Chartobjekte schreiben
    chart_Betriebe.add_series({
        'values': "=Tabellen!$H$3:$H$8",
        'categories': "=Tabellen!$I$3:$I$8",
        'name': "=Tabellen!$I$8",
    })


    # Chart Beschaeftigte kum anlegen
    chart_Besch_kum = wb.add_chart({'type': 'area', 'subtype': 'stacked'})
    chart_Besch_kum.set_style(40)
    chart_Besch_kum.set_size({'width': 529, 'height': 283})
    chart_Besch_kum.set_chartarea({'border': {'none': True},'fill': {'none': True}})
    chart_Besch_kum.set_legend({'position': 'bottom'})
    chart_Besch_kum.set_title({'name': 'Beschaeftigte im Zeitverlauf','name_font':  {'name': 'Calibri', 'size': 12}})

    # Werte in Chartobjekte schreiben
    chart_Besch_kum.add_series({
        'values': "=Tabellen!$B$13:$AF$13",
        'categories': "=Tabellen!$B$12:$AF$12",
        'name': "=Tabellen!$A$13",
    })
    chart_Besch_kum.add_series({
        'values': "=Tabellen!$B$14:$AF$14",
        'categories': "=Tabellen!$B$12:$AF$12",
        'name': "=Tabellen!$A$14",
    })
    chart_Besch_kum.add_series({
        'values': "=Tabellen!$B$15:$AF$15",
        'categories': "=Tabellen!$B$12:$AF$12",
        'name': "=Tabellen!$A$15",
    })
    chart_Besch_kum.add_series({
        'values': "=Tabellen!$B$16:$AF$16",
        'categories': "=Tabellen!$B$12:$AF$12",
        'name': "=Tabellen!$A$16",
    })
    chart_Besch_kum.add_series({
        'values': "=Tabellen!$B$17:$AF$17",
        'categories': "=Tabellen!$B$12:$AF$12",
        'name': "=Tabellen!$A$17",
    })
    chart_Besch_kum.add_series({
        'values': "=Tabellen!$B$18:$AF$18",
        'categories': "=Tabellen!$B$12:$AF$12",
        'name': "=Tabellen!$A$18",
    })




    # Chart Betriebe kum anlegen
    chart_Betriebe_kum = wb.add_chart({'type': 'area', 'subtype': 'stacked'})
    chart_Betriebe_kum.set_style(40)
    chart_Betriebe_kum.set_size({'width': 529, 'height': 283})
    chart_Betriebe_kum.set_chartarea({'border': {'none': True},'fill': {'none': True}})
    chart_Betriebe_kum.set_legend({'position': 'bottom'})
    chart_Betriebe_kum.set_title({'name': 'Betriebe im Zeitverlauf','name_font':  {'name': 'Calibri', 'size': 12}})

    # Werte in Chartobjekte schreiben
    chart_Betriebe_kum.add_series({
        'values': "=Tabellen!$B$33:$AF$33",
        'categories': "=Tabellen!$B$32:$AF$32",
        'name': "=Tabellen!$A$33",
    })
    chart_Betriebe_kum.add_series({
        'values': "=Tabellen!$B$34:$AF$34",
        'categories': "=Tabellen!$B$32:$AF$32",
        'name': "=Tabellen!$A$34",
    })
    chart_Betriebe_kum.add_series({
        'values': "=Tabellen!$B$35:$AF$35",
        'categories': "=Tabellen!$B$32:$AF$32",
        'name': "=Tabellen!$A$35",
    })
    chart_Betriebe_kum.add_series({
        'values': "=Tabellen!$B$36:$AF$36",
        'categories': "=Tabellen!$B$32:$AF$32",
        'name': "=Tabellen!$A$36",
    })
    chart_Betriebe_kum.add_series({
        'values': "=Tabellen!$B$37:$AF$37",
        'categories': "=Tabellen!$B$32:$AF$32",
        'name': "=Tabellen!$A$37",
    })
    chart_Betriebe_kum.add_series({
        'values': "=Tabellen!$B$38:$AF$38",
        'categories': "=Tabellen!$B$32:$AF$32",
        'name': "=Tabellen!$A$38",
    })



    # Charts in Tabelle schreiben
    ws4.insert_chart('A2', chart_Branchenstruktur)
    ws4.insert_chart('A14', chart_Beschaeftigte)
    ws4.insert_chart('A29', chart_Betriebe)
    ws4.insert_chart('A44', chart_Besch_kum)
    ws4.insert_chart('A59', chart_Betriebe_kum)

    ######
    #Workbook speichern
    try:
        wb.close()
    except:
        arcpy.AddMessage("Es liegt ein Fehler beim Speichern der Ausgabedatei vor. Ist diese ggf. noch geoeffnet?")

    schrittmeldung = 'Die Ergebnisausgabe wurde erzeugt. Das Tool wurde erfolgreich angewendet.  \n'
    arcpy.AddMessage(schrittmeldung)
    print str(schrittmeldung)



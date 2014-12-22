# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 32_Einnahme_KFA_NRW.py
#
# Description:
#
#Author:
#Philippe Rieffel
# ---------------------------------------------------------------------------

import arcpy, Einnahmen_lib as e, time, gc,os, sys
#Überflüssige Variablen entfernen
gc.collect()

#Projektparameter festlegen
#Parameter für das Eingabefenster definieren
projektname = arcpy.GetParameterAsText(0)
startjahr = arcpy.GetParameterAsText(1)
endjahr = arcpy.GetParameterAsText(2)


#aktueller Pfad
wcd = os.getcwd()
rootPfad = str(sys.path[0]).split("2_Tool")[0]

#Pfade einrichten
workspace_basis = os.path.join(rootPfad,"1_Basisdaten","FGBD_01_Basisdaten_deutschland.gdb")
workspace_projekt = os.path.join(rootPfad,"3_Projekte", projektname,"FGDB_11_Definition_Projekt_",projektname+'.gdb')
workspace_ergebnisse = os.path.join(rootPfad,"3_Projekte",projektname,"FGDB_21_Einnahmen_Projekt_"+projektname+".gdb")
pfad_ewz_prognose = os.path.join(rootPfad,"3_Projekte",projektname,"FGDB_22_BevModellierung_"+projektname+".gdb","bevoelkerung")
pfad_wanderungsraten = os.path.join(rootPfad,"3_Projekte",projektname,"FGDB_22_BevModellierung_"+projektname+".gdb","wanderungsraten")


#01: AGS aus Lage der Projektfläche ermitteln
#Den AGS aus der Lage der projektfläche im Raum ermitteln
projektFlaeche = rootPfad + "\\3_Projekte\\" + projektname + "\\FGDB_11_Definition_Projekt_" + projektname + ".gdb\\Teilflaechen_Plangebiet"
bkg = rootPfad + "\\1_Basisdaten\\FGBD_01_Basisdaten_deutschland.gdb\\bkg_gemeinden"

#ags aus BKG Daten extrahieren, dafür Gemeinde selektieren, die von Planfläche geschnitten wird
#1. Feature Layer aus den bkg-daten erstellen
arcpy.MakeFeatureLayer_management(bkg,"bkg_lyr")

#2.Spatial Select wo Planfläche bkg_lyr intersected
arcpy.SelectLayerByLocation_management("bkg_lyr", "INTERSECT", projektFlaeche)

#Wenn Flaeche = 1, ags extrahieren
n = arcpy.GetCount_management("bkg_lyr").getOutput(0)
if(int(n) ==1 ):
    gemeindeCursor = arcpy.SearchCursor("bkg_lyr")
    for gemeinde in gemeindeCursor:
        ags = gemeinde.AGS
arcpy.AddMessage(ags)

#Ueber die prognosejahre iterieren
iteratorjahr = startjahr
while iteratorjahr <=endjahr:
    jahr = iteratorjahr

    #Einwohnerzahltabelle öffnen, maennliche ezw extrahieren
    geschlecht = "gesm"
    where_clause = '"jahr" = ' + str(iteratorjahr) + " AND " + '"geschlecht" = ' + "'" + geschlecht + "'"
    ewz_prognose = arcpy.SearchCursor(pfad_ewz_prognose,where_clause)
    for row in ewz_prognose:
        bev_m_alt000b03 = row.alt000b03
        bev_m_alt003b06 =row.alt003b06
        bev_m_alt006b10 =row.alt006b10
        bev_m_alt010b15 =row.alt010b15
        bev_m_alt015b18 =row.alt015b18
        bev_m_alt018b20 =row.alt018b20
        bev_m_alt020b25 =row.alt020b25
        bev_m_alt025b30 =row.alt025b30
        bev_m_alt030b35 =row.alt030b35
        bev_m_alt035b40 =row.alt035b40
        bev_m_alt040b45 =row.alt040b45
        bev_m_alt045b50 =row.alt045b50
        bev_m_alt050b55 =row.alt050b55
        bev_m_alt055b60 =row.alt055b60
        bev_m_alt060b65 =row.alt060b65
        bev_m_alt065b75 =row.alt065b75
        bev_m_alt075um =row.alt075um
    del ewz_prognose, row

    #Wanderungsraten extrahieren um Zugezogene zu ermitteln
    where_clause = '"geschlecht" = ' + "'" + geschlecht + "'"
    wanderungsraten = arcpy.SearchCursor(pfad_wanderungsraten, where_clause)
    for row in wanderungsraten:
        wand_m_alt000b03 =row.alt000b03
        wand_m_alt003b06 =row.alt003b06
        wand_m_alt006b10 =row.alt006b10
        wand_m_alt010b15 =row.alt010b15
        wand_m_alt015b18 =row.alt015b18
        wand_m_alt018b20 =row.alt018b20
        wand_m_alt020b25 =row.alt020b25
        wand_m_alt025b30 =row.alt025b30
        wand_m_alt030b35 =row.alt030b35
        wand_m_alt035b40 =row.alt035b40
        wand_m_alt040b45 =row.alt040b45
        wand_m_alt045b50 =row.alt045b50
        wand_m_alt050b55 =row.alt050b55
        wand_m_alt055b60 =row.alt055b60
        wand_m_alt060b65 =row.alt060b65
        wand_m_alt065b75 =row.alt065b75
        wand_m_alt075um =row.alt075um
    del wanderungsraten, row

    #Einwohnerzahltabelle öffnen, weibliche ezw extrahieren
    geschlecht = "gesw"
    where_clause = '"jahr" = ' + str(iteratorjahr) + " AND " + '"geschlecht" = ' + "'" + geschlecht + "'"
    ewz_prognose = arcpy.SearchCursor(pfad_ewz_prognose,where_clause)
    for row in ewz_prognose:
        bev_w_alt000b03 = row.alt000b03
        bev_w_alt003b06 =row.alt003b06
        bev_w_alt006b10 =row.alt006b10
        bev_w_alt010b15 =row.alt010b15
        bev_w_alt015b18 =row.alt015b18
        bev_w_alt018b20 =row.alt018b20
        bev_w_alt020b25 =row.alt020b25
        bev_w_alt025b30 =row.alt025b30
        bev_w_alt030b35 =row.alt030b35
        bev_w_alt035b40 =row.alt035b40
        bev_w_alt040b45 =row.alt040b45
        bev_w_alt045b50 =row.alt045b50
        bev_w_alt050b55 =row.alt050b55
        bev_w_alt055b60 =row.alt055b60
        bev_w_alt060b65 =row.alt060b65
        bev_w_alt065b75 =row.alt065b75
        bev_w_alt075um =row.alt075um
    del ewz_prognose, row

    #Wanderungsraten extrahieren um Zugezogene zu ermitteln
    where_clause = '"geschlecht" = ' + "'" + geschlecht + "'"
    wanderungsraten = arcpy.SearchCursor(pfad_wanderungsraten, where_clause)
    for row in wanderungsraten:
        wand_w_alt000b03 =row.alt000b03
        wand_w_alt003b06 =row.alt003b06
        wand_w_alt006b10 =row.alt006b10
        wand_w_alt010b15 =row.alt010b15
        wand_w_alt015b18 =row.alt015b18
        wand_w_alt018b20 =row.alt018b20
        wand_w_alt020b25 =row.alt020b25
        wand_w_alt025b30 =row.alt025b30
        wand_w_alt030b35 =row.alt030b35
        wand_w_alt035b40 =row.alt035b40
        wand_w_alt040b45 =row.alt040b45
        wand_w_alt045b50 =row.alt045b50
        wand_w_alt050b55 =row.alt050b55
        wand_w_alt055b60 =row.alt055b60
        wand_w_alt060b65 =row.alt060b65
        wand_w_alt065b75 =row.alt065b75
        wand_w_alt075um =row.alt075um
    del wanderungsraten, row

    #Alle Altersgruppen und Geschlechter zur gesamten Einwohnerzahl fuer dieses Jahr zusammenrechnen
    ewz = bev_m_alt000b03 + bev_m_alt003b06 + bev_m_alt006b10 + bev_m_alt010b15 + bev_m_alt015b18 + bev_m_alt018b20 + bev_m_alt020b25 + bev_m_alt025b30 + bev_m_alt030b35 + bev_m_alt035b40 + bev_m_alt040b45 + bev_m_alt045b50 + bev_m_alt050b55 + bev_m_alt055b60 + bev_m_alt060b65 + bev_m_alt065b75 + bev_m_alt075um +bev_w_alt000b03 + bev_w_alt003b06 + bev_w_alt006b10 + bev_w_alt010b15 + bev_w_alt015b18 + bev_w_alt018b20 + bev_w_alt020b25 + bev_w_alt025b30 + bev_w_alt030b35 + bev_w_alt035b40 + bev_w_alt040b45 + bev_w_alt045b50 + bev_w_alt050b55 + bev_w_alt055b60 + bev_w_alt060b65 + bev_w_alt065b75 + bev_w_alt075um

    #Mit Hilfe der Wanderungsraten die Zugezogenen ermitteln
    zgz = (bev_m_alt000b03*wand_m_alt000b03) + (bev_m_alt003b06*wand_m_alt003b06) + (bev_m_alt006b10*wand_m_alt006b10) + (bev_m_alt010b15*wand_m_alt010b15) + (bev_m_alt015b18*wand_m_alt015b18) + (bev_m_alt018b20*wand_m_alt018b20) + (bev_m_alt020b25*wand_m_alt020b25) + (bev_m_alt025b30*wand_m_alt025b30) + (bev_m_alt030b35*wand_m_alt030b35) + (bev_m_alt035b40*wand_m_alt035b40) + (bev_m_alt040b45*wand_m_alt040b45) + (bev_m_alt045b50*wand_m_alt045b50) + (bev_m_alt050b55*wand_m_alt050b55) + (bev_m_alt055b60*wand_m_alt055b60) + (bev_m_alt060b65*wand_m_alt060b65) + (bev_m_alt065b75*wand_m_alt065b75) + (bev_m_alt075um**wand_m_alt075um) + (bev_w_alt000b03*wand_w_alt000b03) + (bev_w_alt003b06*wand_w_alt003b06) + (bev_w_alt006b10*wand_w_alt006b10) + (bev_w_alt010b15*wand_w_alt010b15) + (bev_w_alt015b18*wand_w_alt015b18) + (bev_w_alt018b20*wand_w_alt018b20) + (bev_w_alt020b25*wand_w_alt020b25) + (bev_w_alt025b30*wand_w_alt025b30) + (bev_w_alt030b35*wand_w_alt030b35) + (bev_w_alt035b40*wand_w_alt035b40) + (bev_w_alt040b45*wand_w_alt040b45) + (bev_w_alt045b50*wand_w_alt045b50) + (bev_w_alt050b55*wand_w_alt050b55) + (bev_w_alt055b60*wand_w_alt055b60) + (bev_w_alt060b65*wand_w_alt060b65) + (bev_w_alt065b75*wand_w_alt065b75) + (bev_w_alt075um**wand_w_alt075um)
    if zgz < 0:
        zgz = 0

    #Schuelerzahl ergibt sich aus der Altersgruppe 6-18
    schueler = bev_m_alt006b10 + bev_m_alt010b15 + bev_m_alt015b18 + bev_w_alt006b10 + bev_w_alt010b15 + bev_w_alt015b18

    #Berechnungsschritte laut Modell
    Steuerkraftmesszahl = e.einkommenssteuerkraftmesszahl(ags, jahr) + e.grundsteuerkraftmesszahlA(ags, jahr) + e.grundsteuerkraftmesszahlB(ags, jahr) + e.umsatzsteuerkraftmesszahl(ags, jahr) + e.gewerbesteuerkraftmesszahl(ags, jahr) + e.gewerbesteuerumlagenmesszahl(ags, jahr)

    Ausgangsmesszahl = float(e.hauptansatz(ewz, zgz)) + e.schueleransatz (schueler) + e.soziallastenansatz(ags, jahr) + e.zentralitaetsansatz(ags, jahr)

    test = Ausgangsmesszahl - Steuerkraftmesszahl

    Schluesselzuweisungen = test * 0.9
    Einnahmen = Schluesselzuweisungen + e.investitionszuweisungen()

    #Ausgabeblock für das Statusfenster (temporär)
    Einnahmen = round(Einnahmen)
    arcpy.AddMessage("Steuerkraftmesszahl: " + str(Steuerkraftmesszahl))
    arcpy.AddMessage("Ausgangsmesszahl: " + str(Ausgangsmesszahl))
    arcpy.AddMessage("Ausgangsmesszahl - Steuerkraftmesszahl: "+str(test))
    arcpy.AddMessage("=========================================================================")
    arcpy.AddMessage("Einnahmen aus dem kommunalen Finanzausgleich NRW: " + str(Einnahmen) + " Euro")
    arcpy.AddMessage("=========================================================================")

    #Das Ergebnis der "Ergebnisse" Tabelle hinzufügen
    sql = "ags = " + ags + "AND parameter_jahr = " + jahr
    table1 = rootPfad + "\\3_Projekte\\" + projektname +"\\FGDB_32_Einnahmen_Projekt_"+projektname+".gdb\\Ergebnisse_KFA"
    #Überprüfen, ob schon ein Ergebniswert mit der Kombination aus ags und Jahr existiert
    #Pro AGS und Jahr soll immer nur ein Ergebnis (neuestes Ergebnis) vorliegen
    checkrows = arcpy.SearchCursor(table1, sql)
    anzahl = 0
    for row in checkrows:
        anzahl = anzahl + 1
    #arcpy.AddMessage("Anzahl = " + str(anzahl))
    #wenn anzahl = 1, exisistiert ein Ergebnis, das Ergebnis wird überschrieben
    #die "parameter" Spalten enthalten die Werte, die am Anfang in das Werkzeug eingegeben werden, zur besseren Nachvollziehbarkeit
    if anzahl == 1:
        Ergebnisse = arcpy.UpdateCursor(table1, sql)
        for Ergebnis in Ergebnisse:
            Ergebnis.Einnahmen = Einnahmen
            lt = time.localtime()
            year, monat, tag, stunde, minute = lt[0:5]
            Ergebnis.timestamp =  str(tag) + "." + str(monat) + "." + str(year) + " - " + str(stunde) + ":" + str(minute)
            Ergebnis.ags = ags
            Ergebnis.parameter_jahr = jahr
            Ergebnis.parameter_schuelerzahl = schueler
            Ergebnis.parameter_einwohnerzahl = ewz
            Ergebnis.parameter_zugezogene = zgz
            Ergebnisse.updateRow(Ergebnis)
            arcpy.AddMessage("Eintrag in Ergebnistabelle aktualisiert")
            del Ergebnis, Ergebnisse
    #wenn Anzahl = 0 existiert noch kein Ergebnis, eine neue Zeile wird angelegt
    #die "parameter" Spalten enthalten die Werte, die am Anfang in das Werkzeug eingegeben werden, zur besseren Nachvollziehbarkeit
    elif anzahl == 0:
        Ergebnisse = arcpy.InsertCursor(table1)
        Ergebnis = Ergebnisse.newRow()
        Ergebnis.ags = ags
        Ergebnis.Einnahmen = Einnahmen
        lt = time.localtime()
        year, monat, tag, stunde, minute = lt[0:5]
        Ergebnis.timestamp =  str(tag) + "." + str(monat) + "." + str(year) + " - " + str(stunde) + ":" + str(minute)
        Ergebnis.parameter_jahr = jahr
        Ergebnis.parameter_schuelerzahl = schueler
        Ergebnis.parameter_einwohnerzahl = ewz
        Ergebnis.parameter_zugezogene = zgz
        Ergebnisse.insertRow(Ergebnis)
        arcpy.AddMessage("Eintrag in Ergebnistablle angelegt")
        del Ergebnis, Ergebnisse
    else:
    #Wenn Anzahl weder 0 noch 1 liegen in der Ergebnistabelle mehrere Werte zu einem AGs vor, das ist so nicht gewollt und bedarf manuellen Eingreifens
        arcpy.AddMessage("In der Ergebnistabelle liegen widersprüchliche Daten vor. Bitte überprüfen Sie die Ergebnistablle unter " + str(workspace_ergebnisse) + " auf Fehler" )


    iteratorjahr += 1
    gc.collect()

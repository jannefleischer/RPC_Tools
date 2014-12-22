# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rieffel
#
# Created:     03.07.2013
# Copyright:   (c) rieffel 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()
import arcpy, Einnahmen_lib, os
try:
    i = 0
    #Projektnamen
    projektname = arcpy.GetParameterAsText(i)
    i=i+1
    #Pfad anlegen
    base_path = str(sys.path[0]).split("2_Tool")[0]
    wcd = os.getcwd()
    rootPfad = wcd.split("2_")[0] +"\\00_Entwicklungsumgebung"

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
    #arcpy.AddMessage(base_path)
##    arcpy.AddMessage("1")

##    #Eingabe: Kommune  (AGS?)
##    ags = arcpy.GetParameterAsText(i)
##    i=i+1
##    #Eingabe: Flächengröße
##    flaechengroesse = arcpy.GetParameterAsText(i)
##    i=i+1

#Ermittlung Flaechengroesse
    flaechengroesse = 0
    flaechen = arcpy.SearchCursor(projektFlaeche)
    for flaeche in flaechen:
        groesse = flaeche.Flaeche_HA
        flaechengroesse = flaechengroesse + groesse
##    arcpy.AddMessage("2")

#Ermittlung Nettobauland
    Flaechenbilanz_Planung = rootPfad + "\\3_Projekte\\" + projektname + "\\FGDB_11_Definition_Projekt_" + projektname + ".gdb\\" + "Flaechenbilanz_Planung_Prozent"
    nettobauland_gesamt = 0
    sql = "Flaechennutzung_S1 = 'Nettobauland'"
    cursor = arcpy.SearchCursor(Flaechenbilanz_Planung,sql)
##    arcpy.AddMessage("3")
    for row in cursor:
        nettobauland_temp = row.Flaeche_ha
        nettobauland_gesamt = nettobauland_gesamt + nettobauland_temp
    nettobauland = nettobauland_gesamt
    #arcpy.AddMessage("4")
##        #Eingabe: Nettobauland
##        nettobauland = arcpy.GetParameterAsText(i)
##        i=i+1
    #Ermittlung zuvor landwirtschaftlich genutzter Fläche
    vornutzungDetailsProzent = rootPfad + "\\3_Projekte\\" +projektname + "\\FGDB_11_Definition_Projekt_" + projektname + ".gdb\\Vornutzungen_Details_Prozent"
    sql = "Vornutzungstyp = 'Ackerflaeche'"
    cursor = arcpy.SearchCursor(vornutzungDetailsProzent, sql)
    anteil = 0
    teilflaeche = ""
    landwirtschaftlicheVornutzung = 0
    for row in cursor:
        anteil = row.Prozent_der_Flaeche
        anteil = anteil / 100
        teilflaeche = row.Teilflaeche_Plangebiet
        sql = "Teilflaeche_Plangebiet = '"+teilflaeche+"'"
        cursor2 = arcpy.SearchCursor(Flaechenbilanz_Planung,sql)
        for row in cursor2:
            temp = row.Flaeche_ha * anteil
            landwirtschaftlicheVornutzung = landwirtschaftlicheVornutzung + temp
    #arcpy.AddMessage("5")

    #Eingabe: zuvor landwirtschaftliche Nutzung
##    landwirtschaftlicheVornutzung = arcpy.GetParameterAsText(i)
##    i=i+1

    #Berechnung: davon zuvor bauliche Nutzung (Grundsteuer B)
    baulicheVornutzung = float(flaechengroesse) - float(landwirtschaftlicheVornutzung)

    #Eingabe: Stand der Aufsiedlung
    standAufsiedlung = arcpy.GetParameterAsText(i)
    i=i+1

    #Monatsrohmieten 1964, falls nicht bekannt 2010 (m2 Preise)
    #Eingabe: Wohnungen
    mieteWohnungen = arcpy.GetParameterAsText(i)
    i=i+1
    #Eingabe: Einfamilienhäuser
    mieteEinfamilienhaeuser = arcpy.GetParameterAsText(i)
    i=i+1
    #Eingabe: Zweifamilienhäuser
    mieteZweifamilienhaeuser = arcpy.GetParameterAsText(i)
    i=i+1
    #Eingabe: Reihenhäuser
    mieteReihenhaeuser = arcpy.GetParameterAsText(i)
    i=i+1

    #Eingabe: Baulandpreis unbebaute Grundstücke (Wohnbauland 1964, falls nicht bekannt 2010)
    baulandpreisUnbebaut = arcpy.GetParameterAsText(i)
    i=i+1

    ##Gebäudezusammensetzung
    #Eingabe: Gebäudeanzahl Einfamilienhaus
    gebaeudeanzahlEinfamilienhaus = arcpy.GetParameterAsText(i)
    i=i+1
    #Eingabe: Grundstücksfläche je Gebäude Einfamilienhaus
    grundstuecksflaecheEinfamilienhaus = arcpy.GetParameterAsText(i)
    i=i+1
    #Berechnung: Mieten 1964 Einfamilienhaus (Anzeigen und Berechnen in der Eingabemaske(Validierung)
    miete1964Einfamilienhaus = arcpy.GetParameterAsText(i)
    i=i+1
    #Eingabe: Gebäudeanzahl Zweifamilienhaus
    gebaeudeanzahlZweifamilienhaus =  arcpy.GetParameterAsText(i)
    i=i+1
    #Eingabe: Grundstücksfläche je Gebäude Zweifamilienhaus
    grundstuecksflaecheZweifamilienhaus = arcpy.GetParameterAsText(i)
    i=i+1
    #Berechnung: Mieten 1964 Zweifamilienhaus (Anzeigen und Berechnen in der Eingabemaske(Validierung)
    miete1964Zweifamilienhaus = arcpy.GetParameterAsText(i)
    i=i+1
    #Eingabe: Gebäudeanzahl Reihenhaus
    gebaeudeanzahlReihenhaus = arcpy.GetParameterAsText(i)
    i=i+1
    #Eingabe: Grundstücksfläche je Gebäude Reihenhaus
    grundstuecksflaecheReihenhaus = arcpy.GetParameterAsText(i)
    i=i+1
    #Berechnung: Mieten 1964 Reihenhaus (Anzeigen  und Berechnen in der Eingabemaske (Validierung)
    miete1964Reihenhaus = arcpy.GetParameterAsText(i)
    i=i+1
    #Eingabe: Gebäudeanzahl Mehrfamilienhaus
    gebaeudeanzahlMehrfamilienhaus = arcpy.GetParameterAsText(i)
    i=i+1
    #Eingabe: Grundstücksfläche je Gebäude Mehrfamilienhaus
    grundstuecksflaecheMehrfamilienhaus = arcpy.GetParameterAsText(i)
    i=i+1
    #Berechnung: Mieten 1964 Mehrfamilienhaus (Anzeigen und Berechnen in der Eingabemaske (Validierung)
    miete1964Mehrfamilienhaus = arcpy.GetParameterAsText(i)
    i=i+1
    #Eingabe : Anzahl der Garagen
    anzahlGaragen = arcpy.GetParameterAsText(i)
    i=i+1
    #Eingabe: Miete je Garage
    mieteGarage = arcpy.GetParameterAsText(i)
    i=i+1

    ##Berechnung: Größe unbebaute Fläche (baureifes Bauland)
    #Nettobauland - ((Häuser * Hausflächen) * Aufsiedlungsstand/100/10000))
    unbebauteFlaeche = float(nettobauland) - ((float(gebaeudeanzahlEinfamilienhaus) * float(grundstuecksflaecheEinfamilienhaus))+(float(gebaeudeanzahlZweifamilienhaus)*float(grundstuecksflaecheZweifamilienhaus))+(float(gebaeudeanzahlMehrfamilienhaus)*float(grundstuecksflaecheMehrfamilienhaus))+(float(gebaeudeanzahlReihenhaus)*float(grundstuecksflaecheReihenhaus)))* float(standAufsiedlung)/100/10000
    #arcpy.AddMessage("6")
    ##GewerblichesVorhaben
    #Eingabe: Art des Gebäudes (Als DropdownListe in der Validierung umsetzen)
    gewerbeGebaeudeArt = arcpy.GetParameterAsText(i)
    i=i+1
    gewerbeGebaeudeArt = gewerbeGebaeudeArt.encode("utf-8")
    #EIngabe: Anteil der versiegelten Fläche
    GewerbeVersiegelteFlaeche = arcpy.GetParameterAsText(i)
    i=i+1
    #Eingabe: Grundfläche des Gebäudes
    GewerbeGrundflaeche = arcpy.GetParameterAsText(i)
    i=i+1
    #Eingabe: Zahl der Etagen
    GewerbeEtagenzahl = arcpy.GetParameterAsText(i)
    i=i+1
    #Berechnung: Nutzfläche (grundfläche * Etagen)
    GewerbeNutzflaeche = float(GewerbeGrundflaeche) * float(GewerbeEtagenzahl)
    #Extraktion: Geschosshöhe (nach Gebäudeart)
    if(gewerbeGebaeudeArt == "Buero- und Verwaltungsgebaeude"):
        Gewerbegeschosshoehe = 4
    elif(gewerbeGebaeudeArt == "Fabrik- und Werkstattgebaeude"):
        Gewerbegeschosshoehe = 7.8
    elif(gewerbeGebaeudeArt == "Handelsgebaeude"):
        Gewerbegeschosshoehe =7.9
    #arcpy.AddMessage("7")


    #Extraktion: Raummeterpreise und Wertezahlen hardcoden, in der EingabeMaske als parameter darstellen und änderbar machen
    GewerbeRaummeterpreise =  arcpy.GetParameterAsText(i)
    i=i+1
    GewerbeWertezahlen = arcpy.GetParameterAsText(i)
    i=i+1
    #Eingabe: Baulandpreise  unbebaute Grundstücke (Gewerbe)
    GewerbeBaulandpreise = arcpy.GetParameterAsText(i)
    i=i+1
    #Hebesätze extrahieren
    #Grundsteuer A & B Sätze
    #arcpy.AddMessage("8")
    sql = "ags = " + "'"+ags+"'"
    #arcpy.AddMessage(sql)
    table3 = base_path+r'1_Basisdaten\FGBD_01_Basisdaten_deutschland.gdb\Steuersaetze_2010'
    #arcpy.AddMessage(table3)
    #arcpy.AddMessage(table3)
    rows = arcpy.SearchCursor(table3, sql)
    for row in rows:
        #arcpy.AddMessage("drin")
        GrundsteuerAHebesatz = row.getValue("Grundsteuer_A")
        #arcpy.AddMessage(GrundsteuerAHebesatz)
        GrundsteuerBHebesatz = row.getValue("Grundsteuer_B")
        #arcpy.AddMessage(GrundsteuerBHebesatz)
    del rows



    #arcpy.AddMessage(GrundsteuerAHebesatz)
    #arcpy.AddMessage(GrundsteuerBHebesatz)

    #Einwohnerzahl extrahieren
    sql = "ags = " + "'"+ags+"'"
    table3 = base_path+r'1_Basisdaten\FGBD_01_Basisdaten_deutschland.gdb\Bevoelkerungsdaten_2010'
    rows = arcpy.SearchCursor(table3, sql)
    for row in rows:
        einwohner = row.getValue("Einwohnerzahl")
    del rows
    #arcpy.AddMessage(einwohner)
    #arcpy.AddMessage("9")
    #Groessenklasse der Kommune berechnen
    groessenklasse = Einnahmen_lib.groessenklasseKommune(einwohner)
   # arcpy.AddMessage("10")
    #Grundsteuer A berechnen
    GrundsteuerA = Einnahmen_lib.grundsteuerA(landwirtschaftlicheVornutzung,GrundsteuerAHebesatz)
    #arcpy.AddMessage("11")
    #arcpy.AddMessage(GrundsteuerA)
    #GrundsteuerB berechnen
    #Teil Wohnen
    GrundsteuerBwohnen = Einnahmen_lib.grundsteuerBwohnen(gebaeudeanzahlEinfamilienhaus,miete1964Einfamilienhaus,gebaeudeanzahlZweifamilienhaus,miete1964Zweifamilienhaus,gebaeudeanzahlReihenhaus,miete1964Reihenhaus,gebaeudeanzahlMehrfamilienhaus,miete1964Mehrfamilienhaus,anzahlGaragen,mieteGarage,standAufsiedlung,groessenklasse,GrundsteuerBHebesatz)
    #arcpy.AddMessage("12")
    #arcpy.AddMessage(GrundsteuerBwohnen)
    #Teil unbebaut
    grundsteuerBunbebaut = Einnahmen_lib.grundsteuerBunbebaut(unbebauteFlaeche,baulandpreisUnbebaut,GrundsteuerBHebesatz)
    #arcpy.AddMessage("13")
    #arcpy.AddMessage(grundsteuerBunbebaut)
    #Teil Gewerbe
    grundsteuerBGewerbeEinnahme = Einnahmen_lib.grundsteuerBGewerbe(GewerbeNutzflaeche,GewerbeGrundflaeche,Gewerbegeschosshoehe,standAufsiedlung,GewerbeVersiegelteFlaeche,GewerbeRaummeterpreise,GewerbeBaulandpreise,GewerbeWertezahlen,flaechengroesse,GrundsteuerBHebesatz)
    #arcpy.AddMessage("14")
    #arcpy.AddMessage(grundsteuerBGewerbeEinnahme)
    #Teil gewerbe unbebaut
    grundsteuerBunbebautGewerbeEinnahmen = Einnahmen_lib.grundsteuerBunbebautGewerbe(nettobauland,standAufsiedlung,baulandpreisUnbebaut,GrundsteuerBHebesatz)
    #arcpy.AddMessage("15")
    #Zusammenrechnung zu den Grundsteuereinnahmen
    Grundsteuereinnahmen = GrundsteuerA + GrundsteuerBwohnen + grundsteuerBunbebaut + grundsteuerBGewerbeEinnahme +grundsteuerBunbebautGewerbeEinnahmen
    arcpy.AddMessage("Grundsteuereinnahmen: "+ str(Grundsteuereinnahmen))

    #Grundsteuer in Tabelle abspeichern
    sql = "ags = " + ags
    #arcpy.AddMessage(sql)
    #ergebnistabelle = base_path + r"Projekte\" +projektname+"\FGDB_32_Einnahmen_Tool.gdb\Grundsteuer"
    ergebnistabelle = os.path.join(base_path,"3_Projekte",projektname,"FGDB_32_Einnahmen_Projekt_"+projektname+".gdb","Grundsteuer")
    try:
        Update = arcpy.UpdateCursor(ergebnistabelle,sql)
        #arcpy.AddMessage("16")
        count = 0
        for row in Update:
            count = count +1
        #arcpy.AddMessage(count)
        if(count>0):
            for row in Update:
                row.grundsteuer_einnahmen = float(Grundsteuereinnahmen)
                Update.updateRow(row)
        else:
            Insert = arcpy.InsertCursor(ergebnistabelle)
            row = Insert.newRow()
            row.ags = ags
            row.grundsteuer_einnahmen = float(Grundsteuereinnahmen)
            Insert.insertRow(row)
            del Insert, row
        try:
            del Update
        except Exception as e:
            arcpy.AddMessage(e)
        arcpy.AddMessage("Grundsteuereinnahmen gespeichert")
    except Exception as e:

        arcpy.AddMessage(e)
except Exception as e:
    arcpy.AddMessage(e)
#Bis auf den Rückrechnungsindex für Mietpreise von 2010 ist alles funktionsfähig implementiert
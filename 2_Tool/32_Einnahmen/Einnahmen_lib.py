# -*- coding: utf-8 -*-
#Grundlagenberechnungen
def ags2kommune(ags):
    import arcpy, gc,os,sys
    gc.collect()
    #aktueller Pfad
    wcd = os.getcwd()
    rootPfad = str(sys.path[0]).split("2_Tool")[0]
    #Extraktion des Kommunennamens
    sql = "ags = " + str(ags)
    table = rootPfad +"\\00_Entwicklungsumgebung\\1_Basisdaten\\FGBD_01_Basisdaten_deutschland.gdb\\Kommunen"
    Kommunen = arcpy.SearchCursor(table, sql)
    for Kommune in Kommunen:
        Name = Kommune.Name
    gc.collect()
    return(Name)

def kommune2ags(kommune):
    import arcpy, gc,os
    #aktueller Pfad
    wcd = os.getcwd()
    rootPfad = wcd.split("2_")[0]
    #Extraktion des ags
    gc.collect()
    print kommune
    kommune = kommune.encode("utf-8")
    print kommune
    sql = "Name = " + kommune
    print sql
    sql = sql.decode("utf-8")
    print sql
    table = rootPfad +"\\00_Entwicklungsumgebung\\1_Basisdaten\\FGBD_01_Basisdaten_deutschland.gdb\\Kommunen"
    Kommunen = arcpy.SearchCursor(table, sql)
    for Kommune in Kommunen:
        ags = Kommune.ags
    gc.collect()
    return(ags)

######################################################
#Hier beginnt der Funktionsblock für den KFA NRW
######################################################

#Steuerkraftmesszahl
def einkommenssteuerkraftmesszahl(ags, jahr):
    ##Berechnung der Einkommenssteuerkraftmesszahl unter Angabe von dem Gemeindeschlüssel der
    #ausgewählten Kommune (ags) sowie dem Jahr(jahr)

    #01: Kompensationsleistung nach GFG NRW(steht noch aus, bis dahin als hardgecodeter Wert KL
    KL = 0.000035

    import arcpy, gc, os, sys
    #aktueller Pfad
    wcd = os.getcwd()
    rootPfad = rootPfad = str(sys.path[0]).split("2_Tool")[0]


    gc.collect()
    #02 Grundberechnungen
    vorvorjahr = int(jahr) - 2
    vorjahr = int(jahr) - 1

    #03: Einkommenssteueraufkommen extrahieren
    sql = "ags = '" +  ags+"'"
    table1 = rootPfad+"\\1_Basisdaten\\FGBD_01_Basisdaten_deutschland.gdb\\Steueraufkommen_" + str(vorvorjahr)
    arcpy.AddMessage(table1)
    table2 = rootPfad+ "\\1_Basisdaten\\FGBD_01_Basisdaten_deutschland.gdb\\Steueraufkommen_" + str(vorjahr)
    arcpy.AddMessage(table2)
    rows = arcpy.SearchCursor(table1, sql)
    for row in rows:
        EinkommenssteueraufkommenVorvorjahr = row.getValue("Einkommenssteueraufkommen")
    rows = arcpy.SearchCursor(table2, sql)
    for row in rows:
        EinkommenssteueraufkommenVorjahr = row.getValue("Einkommenssteueraufkommen")
    ESKM = (float(EinkommenssteueraufkommenVorvorjahr) * (0.5 + KL)) + (float(EinkommenssteueraufkommenVorjahr) * (0.5 + KL))
    gc.collect()
    return ESKM

def grundsteuerkraftmesszahlA(ags, jahr):
    ##Berechnung der GrundsteuerkraftmesszahlA, unter Angabe von dem Gemeindeschlüssel der
    #ausgewählten Kommune (ags) sowie dem Jahr(jahr)
    #01: fiktiver Hebesatz NRW
    HSNRW = 2.5
    import arcpy, gc
    #gc.collect()

    #02: Grundberechnungen
    vorvorjahr = int(jahr) - 2
    vorjahr = int(jahr) - 1

    #03: Grundsteueraufkommen berechnen
    sql = "ags = '" + str(ags) +"'"
    table1 = '../../1_Basisdaten/FGBD_01_Basisdaten_deutschland.gdb/Steueraufkommen_' + str(vorvorjahr)
    table2 = '../../1_Basisdaten/FGBD_01_Basisdaten_deutschland.gdb/Steueraufkommen_' + str(vorjahr)
    rows = arcpy.SearchCursor(table1, sql)
    for row in rows:
        GrundsteueraufkommenVorvorjahr = row.getValue("GrundsteueraufkommenA")
    rows = arcpy.SearchCursor(table2, sql)
    for row in rows:
        GrundsteueraufkommenVorjahr = row.getValue("GrundsteueraufkommenA")

    #04: Grundsteuerkraftmesszahl A berechnen
    table3 =  '../../1_Basisdaten/FGBD_01_Basisdaten_deutschland.gdb/Steuersaetze_' + str(jahr)
    rows = arcpy.SearchCursor(table3, sql)
    for row in rows:
        Grundsteuer = row.getValue("GrundsteuerA")
    GSKMA = (((float(GrundsteueraufkommenVorvorjahr) * 0.5) + (float(GrundsteueraufkommenVorjahr) * 0.5)) / float(Grundsteuer) ) * HSNRW
    gc.collect()
    return GSKMA

def grundsteuerkraftmesszahlB(ags, jahr):
    ##Berechnung der GrundsteuerkraftmesszahlB, unter Angabe von dem Gemeindeschlüssel der
    #ausgewählten Kommune (ags) sowie dem Jahr(jahr)
    #01: fiktiver Hebesatz NRW
    HSNRW = 2.5
    import arcpy, gc
    #gc.collect()

    #02: Grundberechnungen
    vorvorjahr = int(jahr) - 2
    vorjahr = int(jahr) - 1

    #03: Grundsteueraufkommen berechnen
    sql = "ags = '" + str(ags)+"'"
    table1 = '../../1_Basisdaten/FGBD_01_Basisdaten_deutschland.gdb/Steueraufkommen_' + str(vorvorjahr)
    table2 = '../../1_Basisdaten/FGBD_01_Basisdaten_deutschland.gdb/Steueraufkommen_' + str(vorjahr)
    rows = arcpy.SearchCursor(table1, sql)
    for row in rows:
        GrundsteueraufkommenVorvorjahr = row.getValue("GrundsteueraufkommenB")
    rows = arcpy.SearchCursor(table2, sql)
    for row in rows:
        GrundsteueraufkommenVorjahr = row.getValue("GrundsteueraufkommenB")

    #04: Grundsteuerkraftmesszahl B berechnen
    table3 = '../../1_Basisdaten/FGBD_01_Basisdaten_deutschland.gdb/Steuersaetze_' + str(jahr)
    rows = arcpy.SearchCursor(table3, sql)
    for row in rows:
        Grundsteuer = row.getValue("GrundsteuerB")
    GSKMB = (((float(GrundsteueraufkommenVorvorjahr) * 0.5) + (float(GrundsteueraufkommenVorjahr) * 0.5)) / float(Grundsteuer) ) * HSNRW
    gc.collect()
    return GSKMB

def umsatzsteuerkraftmesszahl(ags, jahr):
    ##Berechnung der Umsatzsteuerkraftmesszahl, unter Angabe von dem Gemeindeschlüssel der
    #ausgewählten Kommune (ags) sowie dem Jahr(jahr)
    import arcpy, gc
    gc.collect()

    #01: Grundberechnungen
    vorvorjahr = int(jahr) - 2
    vorjahr = int(jahr) - 1

    #02: Umsatzsteueraufkommen berechnen
    sql = "ags = '" + str(ags)+"'"
    table1 = '../../1_Basisdaten/FGBD_01_Basisdaten_deutschland.gdb/Steueraufkommen_' + str(vorvorjahr)
    table2 = '../../1_Basisdaten/FGBD_01_Basisdaten_deutschland.gdb/Steueraufkommen_' + str(vorjahr)
    rows = arcpy.SearchCursor(table1, sql)
    for row in rows:
        UmsatzsteueraufkommenVorvorjahr = row.getValue("Umsatzsteueraufkommen")
    rows = arcpy.SearchCursor(table2, sql)
    for row in rows:
        UmsatzsteueraufkommenVorjahr = row.getValue("Umsatzsteueraufkommen")

    #03: Umsatzsteuerkraftmesszahl berechnen
    USKM = float(UmsatzsteueraufkommenVorvorjahr) * 0.5 + float(UmsatzsteueraufkommenVorjahr) * 0.5
    gc.collect()
    return USKM

def gewerbesteuerkraftmesszahl(ags, jahr):
    ##Berechnung der Gewerbeteuerkraftmesszahl, unter Angabe von dem Gemeindeschlüssel der
    #ausgewählten Kommune (ags) sowie dem Jahr(jahr)
    import arcpy, gc
    gc.collect()
    #01: fiktiver Hebesatz NRW
    HSNRW = 2.5

    #02: Grundberechnungen
    vorvorjahr = int(jahr) - 2
    vorjahr = int(jahr) - 1

    #03: Steueraufkommen Vorjahr und Vorvorjahr
    sql = "ags = '" + str(ags) +"'"
    table1 = '../../1_Basisdaten/FGBD_01_Basisdaten_deutschland.gdb/Steueraufkommen_' + str(vorvorjahr)
    table2 = '../../1_Basisdaten/FGBD_01_Basisdaten_deutschland.gdb/Steueraufkommen_' + str(vorjahr)
    rows = arcpy.SearchCursor(table1, sql)
    for row in rows:
        GewerbesteueraufkommenVorvorjahr = row.getValue("Gewerbesteueraufkommen")
    rows = arcpy.SearchCursor(table2, sql)
    for row in rows:
        GewerbesteueraufkommenVorjahr = row.getValue("Gewerbesteueraufkommen")

    #04: Gewerbesteuerhebesätze Vorjahr und Vorvorjahr
    table3 = '../../1_Basisdaten/FGBD_01_Basisdaten_deutschland.gdb/Steuersaetze_' + str(vorvorjahr)
    table4 = '../../1_Basisdaten/FGBD_01_Basisdaten_deutschland.gdb/Steuersaetze_' + str(vorjahr)
    arcpy.AddMessage(sql)
    arcpy.AddMessage(table3)
    rows = arcpy.SearchCursor(table3, sql)
    for row in rows:
        GewerbesteuersatzVorvorjahr = row.getValue("Gewerbesteuer")
    rows = arcpy.SearchCursor(table4,sql)
    for row in rows:
        GewerbesteuersatzVorjahr = row.getValue("Gewerbesteuer")

    #05: Gewerbesteuerkraftmesszahl berechnen
    GWSKM = float(GewerbesteueraufkommenVorvorjahr) * 0.5 / float(GewerbesteuersatzVorvorjahr) + float(GewerbesteueraufkommenVorjahr) * 0.5 / float(GewerbesteuersatzVorjahr) * HSNRW
    gc.collect()
    return GWSKM
##Bis hier im diagramm dokumentiert
def gewerbesteuerumlagenmesszahl(ags, jahr):
    ##Berechnung der Gewerbesteuerumlagenmesszahl. unter Angabe von dem Gemeindeschlüssel der
    #ausgewählten Kommune (ags) sowie dem Jahr (jahr)
    import arcpy, gc
    gc.collect()
    #Vervielfältiger Gewerbesteuerumlage:
    xGWSU = 1.5
    vorvorjahr = int(jahr) - 2
    vorjahr = int(jahr) - 1
    sql = "ags = '" + str(ags)+"'"
    #Gewerbesteuerumlage Vorjahr und Vorvorjahr
    table1 = '../../1_Basisdaten/FGBD_01_Basisdaten_deutschland.gdb/Steueraufkommen_' + str(vorvorjahr)
    table2 = '../../1_Basisdaten/FGBD_01_Basisdaten_deutschland.gdb/Steueraufkommen_' + str(vorjahr)
    rows = arcpy.SearchCursor(table1, sql)
    for row in rows:
        GewerbesteuerumlageVorvorjahr = row.getValue("Gewerbesteuerumlage")
    rows = arcpy.SearchCursor(table2, sql)
    for row in rows:
        GewerbesteuerumlageVorjahr = row.getValue("Gewerbesteuerumlage")
    #Gewerbesteuerhebesätze Vorjahr und Vorvorjahr
    table3 = '../../1_Basisdaten/FGBD_01_Basisdaten_deutschland.gdb/Steuersaetze_' + str(vorvorjahr)
    table4 = '../../1_Basisdaten/FGBD_01_Basisdaten_deutschland.gdb/Steuersaetze_' + str(vorjahr)
    rows = arcpy.SearchCursor(table3, sql)
    for row in rows:
        GewerbesteuersatzVorvorjahr = row.getValue("Gewerbesteuer")
    rows = arcpy.SearchCursor(table4, sql)
    for row in rows:
        GewerbesteuersatzVorjahr = row.getValue("Gewerbesteuer")
    #Berechnung GWSUM nach Modell:
    GWSUM = float(GewerbesteuerumlageVorvorjahr) / GewerbesteuersatzVorvorjahr * xGWSU * 0.5 + float(GewerbesteuerumlageVorjahr) / GewerbesteuersatzVorjahr * xGWSU * 0.5
    gc.collect()
    return GWSUM
######################################################

def hauptansatz(ewz,zgz):
    import arcpy, math, gc
    gc.collect()
    ##Berechnung des Hauptansatzes für eine bestimmte Zahl an Einwohnern (ewz) und Zugezogenen (zgz)
    #Hauptansatz ohne Zugezogene
    #Variablen für den Counter initialisieren
    x = 0
    y = 1
    #Die Staffelklassen der Einwohner
    EWlist = [25000.0,38500.0,54500.0,73500.0,95000.0,120000.0,147000.0,177500.0,210500.0,246500.0,285000.0,326500.0,371000.0,418500.0,468500.0,521000.0,577000.0,635500.0,635501.0]
    #Die Staffelklassen des Hauptansatzes in %
    KLlist = [100.0,103.0,106.0,109.0,112.0,115.0,118.0,121.0,124.0,127.0,130.0,133.0,136.0,139.0,142.0,145.0,148.0,151.0,154.0]
    #Berechnung Der Hauptansatzstaffel laut Logik der Excel Tabelle
    #Alle 19 Klassen durchgehen
    while x != 18:
        #Wenn die Einwohnerzahl genau einer Staffelklassengrenze entspricht, den entsprechenden Prozentwert zuweisen
        if ewz == EWlist[x]:
            HAS = KLlist[x]
        #Wenn die Einwohnerzahl zwischen zwei Klassen liegt, den Prozentwert interpolieren
        elif ewz < EWlist[y] and ewz > EWlist[x]:
            HAS = KLlist[x] + (KLlist[y] - KLlist[x])/(EWlist[y] - EWlist[x])*(ewz - EWlist[x])
        x = x + 1
        y = y + 1
    #Wenn die Einwohnerzahl > 6355000 ist die HAS automatisch 154%
    if ewz > 635500:
        HAS = 154
    #Wenn die Einwohnerzahl < 25000 ist die HAS automatisch 154%
    if ewz < 25000:
        HAS = 100
    #HAS runden, durch Addition der 0,05 wird sichergestellt, dass immer nach oben aufgerundet wird
    HAS = round(HAS+0.05, 1)
    #Berechnung des Hauptansatzes ohne Zugezogene(ewz*HAS/100)
    HA = ewz*HAS/100

    #Hauptansatz mit Zugezogenen
    ew = ewz + zgz
    #Variablen für den Counter initialisieren
    x = 0
    y = 1
    while x != 18:
        #Wenn die Einwohnerzahl genau einer Staffelklassengrenze entspricht, den entsprechenden Prozentwert zuweisen
        if ew == EWlist[x]:
            HAS = KLlist[x]
        #Wenn die Einwohnerzahl zwischen zwei Klassen liegt, den Prozentwert interpolieren
        elif ew < EWlist[y] and ew > EWlist[x]:
            HAS = KLlist[x] + (KLlist[y] - KLlist[x])/(EWlist[y] - EWlist[x])*(ew - EWlist[x])
        x = x + 1
        y = y + 1
    #Wenn die Einwohnerzahl > 6355000 ist die HAS automatisch 154%
    if ew > 635500:
        HAS = 154
    #Wenn die Einwohnerzahl < 25000 ist die HAS automatisch 154%
    if ewz < 25000:
        HAS = 100
    #HAS runden, durch Addition der 0,05 wird sichergestellt, dass immer nach oben aufgerundet wird
    HAS = round(HAS+0.05, 1)
    #Berechnung des Hauptansatzes mit Zugezogenen(ewz*HAS/100)
    HA2 = ew*HAS/100
    #Berechnung Hauptansatz gesamt
    HAG = HA2 - HA
    gc.collect()
    return HAG

def soziallastenansatz(ags, jahr):
    ##Berechnung des Soziallastenasatzes für eine Kommune, unter Angabe von dem Gemeindeschlüssel der
    #ausgewählten Kommune (ags) sowie dem Jahr(jahr)
    import arcpy, gc
    gc.collect()
    sql = "ags = '" + str(ags)+"'"
    table1 = '../../1_Basisdaten/FGBD_01_Basisdaten_deutschland.gdb/Arbeitsmarkt_' + str(jahr)
    rows = arcpy.SearchCursor(table1, sql)
    for row in rows:
        Bedarfsgemeinschaften = row.getValue("Bedarfsgemeinschaften")
    SLA = float(Bedarfsgemeinschaften) * 9.6
    gc.collect()
    return SLA

def zentralitaetsansatz(ags, jahr):
    ##Berechnung des Zentralitätsansatzes für eine Kommune, unter Angabe von dem Gemeindeschlüssel der
    #ausgewählten Kommune (ags) sowie dem Jahr(jahr)
    import arcpy, gc
    gc.collect()
    sql = "ags = '" + str(ags)+"'"
    table1 = '../../1_Basisdaten/FGBD_01_Basisdaten_deutschland.gdb/Arbeitsmarkt_' + str(jahr)
    rows = arcpy.SearchCursor(table1, sql)
    for row in rows:
        SVPBAO = row.getValue("SVP_Beschaeftigte_AO")
    ZA = SVPBAO * 0.15
    gc.collect()
    return ZA

def schueleransatz(anzahl):
    ##Berechnung des Schueleransatzes für ein Baugebiet unter Angabe der Anzahö der Schüler im Neubaugebiet
    import arcpy, gc
    gc.collect()
    #Bis Daten aus dem bevölkerungsmodell zur tatsächlichen Verteilung der Schüler vorliegen, wird einfach eine gleichmäßige Verteilung der Schüler auf alle
    #14 Altersklassen angenommen
    alter06 = anzahl / 14
    alter07 = anzahl / 14
    alter08 = anzahl / 14
    alter09 = anzahl / 14
    alter10 = anzahl / 14
    alter11 = anzahl / 14
    alter12 = anzahl / 14
    alter13 = anzahl / 14
    alter14 = anzahl / 14
    alter15 = anzahl / 14
    alter16 = anzahl / 14
    alter17 = anzahl / 14
    alter18 = anzahl / 14
    alter19 = anzahl / 14

    #Verteilung der Schüler der verschiedenen Altersklassen auf die verschiedenen Schulformen
    #Zur einfacheren Aktualisierung ausserhalb der Berechnung in Variablen abgelegt
    #Grundschule
    GSKlasse01 = 0.97
    GSKlasse02 = 0.96
    GSKlasse03 = 0.96
    GSKlasse04 = 0.95
    #Volksschule
    VSKlasse05 = 0.14
    VSKlasse06 = 0.15
    VSKlasse07 = 0.17
    VSKlasse08 = 0.18
    VSKlasse09 = 0.21
    VSKlasse10 = 0.19
    VSKlasse11 = 0
    VSKlasse12 = 0
    VSKlasse12 = 0
    #Sonderschulen
    SSKlasse01 = 0.03
    SSKlasse02 = 0.04
    SSKlasse03 = 0.03
    SSKlasse04 = 0.04
    SSKlasse05 = 0.04
    SSKlasse06 = 0.04
    SSKlasse07 = 0.04
    SSKlasse08 = 0.04
    SSKlasse09 = 0.04
    SSKlasse10 = 0.05
    SSKlasse11 = 0
    SSKlasse12 = 0
    SSKlasse13 = 0
    #Realschulen
    RSKlasse05 = 0.27
    RSKlasse06 = 0.27
    RSKlasse07 = 0.27
    RSKlasse08 = 0.27
    RSKlasse09 = 0.26
    RSKlasse10 = 0.27
    RSKlasse11 = 0
    RSKlasse12 = 0
    #Gymnasien
    GYKlasse05 = 0.37
    GYKlasse06 = 0.36
    GYKlasse07 = 0.35
    GYKlasse08 = 0.34
    GYKlasse09 = 0.31
    GYKlasse10 = 0.32
    GYKlasse11 = 0.35
    GYKlasse12 = 0.32
    GYKlasse13 = 0.28
    #integrierte Gesamtschulen
    GESKlasse05 = 0.17
    GESKlasse06 = 0.17
    GESKlasse07 = 0.16
    GESKlasse08 = 0.16
    GESKlasse09 = 0.17
    GESKlasse10 = 0.16
    GESKlasse11 = 0.08
    GESKlasse12 = 0.07
    GESKlasse13 = 0.05
    #Waldorfschulen
    WSKlasseALLE = 0.01
    #Berufskolleg
    BKlasseALLE = 0

    #Aufteilung auf die verschiedenen Schulformen mit obigen Parametern
    #FEHLER? (alter10 * GSKlasse03)
    Grundschule = (alter06 * GSKlasse01)+(alter07 * GSKlasse02)+(alter08 * GSKlasse03)+(alter09 * GSKlasse04)+(alter10 * GSKlasse03)
    Hauptschule = (alter11*VSKlasse07)+(alter12*VSKlasse08)+(alter13*VSKlasse09)+(alter14*VSKlasse10)+(alter15*VSKlasse11)+(alter16*VSKlasse12)
    Realschule = (alter11*RSKlasse07)+(alter12*RSKlasse08)+(alter13*RSKlasse09)+(alter14*RSKlasse10)+(alter15*RSKlasse11)+(alter16*RSKlasse12)
    Gymnasium = (alter11*GYKlasse05)+(alter12*GYKlasse06)+(alter13*GYKlasse07)+(alter14*GYKlasse08)+(alter15*GYKlasse09)+(alter16*GYKlasse10)+(alter17*GYKlasse11)+(alter18*GYKlasse12)+(alter19*GYKlasse13)
    Gesamtschule = (alter10*GESKlasse05)+(alter11*GESKlasse06)+(alter12*GESKlasse07)+(alter13*GESKlasse08)+(alter14*GESKlasse09)+(alter15*GESKlasse10)+(alter16*GESKlasse11)+(alter17*GESKlasse12)+(alter18*GESKlasse13)
    Berufskolleg = (alter17*BKlasseALLE)+(alter18*BKlasseALLE)+(alter19*BKlasseALLE)
    Sonderschule = (alter06*SSKlasse01)+(alter07*SSKlasse02)+(alter08*SSKlasse03)+(alter09*SSKlasse04)+(alter10*SSKlasse05)+(alter11*SSKlasse06)+(alter12*SSKlasse07)+(alter13*SSKlasse08)+(alter14*SSKlasse09)+(alter15*SSKlasse10)+(alter16*SSKlasse11)+(alter17*SSKlasse12)+(alter18*SSKlasse13)
    #Vervielfältiger und Gewichtung hinzufügen
    Grundschule = Grundschule  * 0.96
    Hauptschule = (Hauptschule * 1.19) +((Hauptschule * 5.1) * 1.19)
    Realschule = Realschule*0.88
    Gymnasium = Gymnasium*0.96
    Gesamtschule = (Gesamtschule * 5.1)*1.46
    Berufskolleg = Berufskolleg * 0.54
    Sonderschule = (Sonderschule * 3) * 3.46
    Zwischensumme = Grundschule + Hauptschule + Realschule + Gymnasium + Gesamtschule + Berufskolleg + Sonderschule
    SA = round(Zwischensumme * 0.88)
    gc.collect()
    return SA

def investitionszuweisungen():
    #Berechnung der Schlüsselzuweisung, die Parameter müssen nachträglich hinzugefügt werden
    Einwohnerzahlanteil = 0.44 #ausgedachter Wert
    Gebietsflaechenanteil = 0.12 #ausgedachter Wert
    AnteilEW65 = 0.2 #ausgedachter Wert
    investitionszuweisungen = (439736000*0.7*Einwohnerzahlanteil) + (439736000*0.3*Gebietsflaechenanteil) + (44436000*AnteilEW65)
    return investitionszuweisungen

#########################################################################
#Dies schliesst den Funktionsblock für den KFA NRW ab
#########################################################################


######################################################
#Hier beginnt der Funktionsblock für Grundsteuer
######################################################
def grundsteuerA(landwirtschaftlicheFlaeche,kommunalerHebesatzA ):
    grundsteuerAeinnahme = float(landwirtschaftlicheFlaeche)*2200*0.006*float(kommunalerHebesatzA)

    return grundsteuerAeinnahme

def grundsteuerBwohnen(gebaeudeanzahlEinfamilienhaus,miete1964Einfamilienhaus, gebaeudeanzahlZweifamilienhaus,miete1964Zweifamilienhaus, gebaeudeanzahlReihenhaus,miete1964Reihenhaus,gebaeudeanzahlMehrfamilienhaus, miete1964Mehrfamilienhaus,anzahlGaragen,mieteGaragen,standAufsiedlung, groessenklasse, hebesatzGrundsteuerB):
    import arcpy
    #Berechnung der tatsächlichen Gebäudeanzahl
    AnzahlGebaeudeEinfamilienhaus = float(gebaeudeanzahlEinfamilienhaus) * (float(standAufsiedlung)/100)
    AnzahlGebaeudeZweifamilienhaus = float(gebaeudeanzahlZweifamilienhaus) * (float(standAufsiedlung)/100)
    AnzahlGebaeudeReihenhaus = float(gebaeudeanzahlReihenhaus) * (float(standAufsiedlung)/100)
    AnzahlGebaeudeMehrfamilienhaus = float(gebaeudeanzahlMehrfamilienhaus) * (float(standAufsiedlung)/100)

    #Berechnung der  Wohn/Nutzfläche in qm
    #Annahmen: Einfamilienhaus 150qm Zweifamilienhaus 300qm Mehrfamilienhaus 840qm Reihenhaus 100qm
    wohnflaecheEinfamilienhaeuser = AnzahlGebaeudeEinfamilienhaus * 150
    wohnflaecheZweifamilienhaeuser = AnzahlGebaeudeZweifamilienhaus * 300
    wohnflaecheReihenhaeuser = AnzahlGebaeudeReihenhaus * 100
    wohnflaecheMehrfamilienhaeuser = AnzahlGebaeudeMehrfamilienhaus * 840

    #Berechnung der Jahresrohmieten pro qm
    jahresrohmieteEinfamilienhaus = float(miete1964Einfamilienhaus) * 12
    jahresrohmieteZweifamilienhaus = float(miete1964Zweifamilienhaus) * 12
    jahresrohmieteReihenhaus = float(miete1964Reihenhaus) * 12
    jahresrohmieteMehrfamilienhaus = float(miete1964Mehrfamilienhaus) * 12

#Vervielfältiger festlegen
    groessenklasse = groessenklasse.encode("utf-8")
    if(groessenklasse == "bis 2000"):
        vervielfaeltigerEinfamilienhaus=13
        vervielfaeltigerZweifamilienhaus=11.4
        vervielfaeltigerMehrfamilienhaus=9.8
        vervielfaeltigerReihenhaus=9.8
        vervielfaeltigerMischgrundstueck1=9.9
        vervielfaeltigerMischgrundstueck2=9.6
        vervielfaeltigerGeschaeftsgrundstuecke=9.4


    if(groessenklasse == "über 2.000 bis 5.000"):
        vervielfaeltigerEinfamilienhaus=12.4
        vervielfaeltigerZweifamilienhaus=11
        vervielfaeltigerMehrfamilienhaus=9.7
        vervielfaeltigerReihenhaus=9.7
        vervielfaeltigerMischgrundstueck1=9.6
        vervielfaeltigerMischgrundstueck2=9.6
        vervielfaeltigerGeschaeftsgrundstuecke=9.2

    if(groessenklasse == "über 5.000 bis 10.000"):
        vervielfaeltigerEinfamilienhaus=12
        vervielfaeltigerZweifamilienhaus=10.6
        vervielfaeltigerMehrfamilienhaus=9.5
        vervielfaeltigerReihenhaus=9.5
        vervielfaeltigerMischgrundstueck1=9.2
        vervielfaeltigerMischgrundstueck2=8.9
        vervielfaeltigerGeschaeftsgrundstuecke=9

    if(groessenklasse == "über 10.000 bis 50.000"):
        vervielfaeltigerEinfamilienhaus=11.8
        vervielfaeltigerZweifamilienhaus=10.5
        vervielfaeltigerMehrfamilienhaus=9.2
        vervielfaeltigerReihenhaus=9.2
        vervielfaeltigerMischgrundstueck1=9.1
        vervielfaeltigerMischgrundstueck2=8.9
        vervielfaeltigerGeschaeftsgrundstuecke=9

    if(groessenklasse == "über 50.000 bis 100.000"):
        vervielfaeltigerEinfamilienhaus=11.8
        vervielfaeltigerZweifamilienhaus=10.5
        vervielfaeltigerMehrfamilienhaus=9
        vervielfaeltigerReihenhaus=9
        vervielfaeltigerMischgrundstueck1=9
        vervielfaeltigerMischgrundstueck2=8.7
        vervielfaeltigerGeschaeftsgrundstuecke=8.9

    if(groessenklasse == "über 100.000 bis 200.000"):
        vervielfaeltigerEinfamilienhaus=11.8
        vervielfaeltigerZweifamilienhaus=10.5
        vervielfaeltigerMehrfamilienhaus=9
        vervielfaeltigerReihenhaus=9
        vervielfaeltigerMischgrundstueck1=9
        vervielfaeltigerMischgrundstueck2=8.8
        vervielfaeltigerGeschaeftsgrundstuecke=8.9

    if(groessenklasse == "über 200.000 bis 500.000"):
        vervielfaeltigerEinfamilienhaus=11.8
        vervielfaeltigerZweifamilienhaus=10.5
        vervielfaeltigerMehrfamilienhaus=9
        vervielfaeltigerReihenhaus=9
        vervielfaeltigerMischgrundstueck1=9
        vervielfaeltigerMischgrundstueck2=8.8
        vervielfaeltigerGeschaeftsgrundstuecke=8.9

    if(groessenklasse == "über 500.000"):
        vervielfaeltigerEinfamilienhaus=11.9
        vervielfaeltigerZweifamilienhaus=10.5
        vervielfaeltigerMehrfamilienhaus=9.1
        vervielfaeltigerReihenhaus=9-1
        vervielfaeltigerMischgrundstueck1=9
        vervielfaeltigerMischgrundstueck2=8.8
        vervielfaeltigerGeschaeftsgrundstuecke=8.9
    #arcpy.AddMessage(vervielfaeltigerEinfamilienhaus)

#Einheitswert berechnen
    einheitswertEinfamilienhaeuser = float(wohnflaecheEinfamilienhaeuser)*float(jahresrohmieteEinfamilienhaus)*float(vervielfaeltigerEinfamilienhaus)+(float(anzahlGaragen)*float(mieteGaragen))
    einheitswertZweifamilienhaeuser = float(wohnflaecheZweifamilienhaeuser)*float(jahresrohmieteZweifamilienhaus)*float(vervielfaeltigerZweifamilienhaus)+(float(anzahlGaragen)*float(mieteGaragen))
    einheitswertReihenhaeuser = float(wohnflaecheReihenhaeuser)*float(jahresrohmieteReihenhaus)*float(vervielfaeltigerReihenhaus)+(float(anzahlGaragen)*float(mieteGaragen))
    einheitswertMehrfamilienhaeuser = float(wohnflaecheMehrfamilienhaeuser)*float(jahresrohmieteMehrfamilienhaus)*float(vervielfaeltigerMehrfamilienhaus)+(float(anzahlGaragen)*float(mieteGaragen))

#Steuermessbetrag berechnen
    steuermessbetragEinfamilenhaeuser = (38346.89*float(AnzahlGebaeudeEinfamilienhaus))*0.0026+((einheitswertEinfamilienhaeuser-(38346.89*float(AnzahlGebaeudeEinfamilienhaus)))*0.0035)
    steuermessbetragZweifamilienhaeuser = float(einheitswertZweifamilienhaeuser)*0.0031
    steuermessbetragReihenhaeuser = float(einheitswertReihenhaeuser)*0.0035
    steuermessbetragMehrfamilienhaeuser = float(einheitswertMehrfamilienhaeuser)*0.0035

#grundsteuereinnahme berechnen
    grundsteuerBwohnenEinnahme = (steuermessbetragEinfamilenhaeuser+steuermessbetragZweifamilienhaeuser+steuermessbetragReihenhaeuser+steuermessbetragMehrfamilienhaeuser)*float(hebesatzGrundsteuerB)
    return grundsteuerBwohnenEinnahme

def grundsteuerBunbebaut(unbebauteFlaeche,baulandpreisUnbebaut,hebesatzGrundsteuerB):
    einheitswert = float(baulandpreisUnbebaut)*10000*float(unbebauteFlaeche)
    steuermessbetrag = einheitswert * 0.0035
    grundsteuerBunbebautEinnahme = steuermessbetrag*float(hebesatzGrundsteuerB)
    return grundsteuerBunbebautEinnahme

def grundsteuerBunbebautGewerbe(nettobauland,standAufsiedlung,baulandpreisUnbebaut,hebesatzGrundsteuerB):
    unbebauteFlaeche = float(nettobauland)*(100-float(standAufsiedlung)/100)
    einheitswert = float(baulandpreisUnbebaut)*10000*float(unbebauteFlaeche)
    steuermessbetrag = einheitswert * 0.0035
    grundsteuerBunbebautGewerbeEinnahmen = steuermessbetrag * float(hebesatzGrundsteuerB)

    return grundsteuerBunbebautGewerbeEinnahmen

def grundsteuerBGewerbe(nutzflaeche,grundflaeche,geschosshoehe,standAufsiedlung,anteilVersiegelteFlaeche, gewerbeRaummeterpreis,GewerbeBaulandpreise,GewerbeWertezahlen, flaechengroesse,hebesatzGrundsteuerB):
#Berechung Ruaminhalt in m3
    rauminhalt = float(nutzflaeche)*float(geschosshoehe)*float(standAufsiedlung)/100
    wertGrundflaeche = float(flaechengroesse)*float(GewerbeBaulandpreise)*10000
    wertGebaeude =  rauminhalt * float(gewerbeRaummeterpreis)
    wertAussenanlagen = ((float(flaechengroesse)*10000*float(anteilVersiegelteFlaeche)/100)-float(grundflaeche))*8.2
    wertGesamt = wertGrundflaeche+wertGebaeude+wertAussenanlagen
    einheitswert = wertGesamt*float(GewerbeWertezahlen)/100
    steuermessbetrag = 0.0035*einheitswert
    if(rauminhalt == 0):
        grundsteuerBGewerbeEinnahme = 0
    else:
        grundsteuerBGewerbeEinnahme = float(hebesatzGrundsteuerB)/100*steuermessbetrag
    return grundsteuerBGewerbeEinnahme


    return grundsteuerBgewerbe

def groessenklasseKommune(einwohner):
    if(float(einwohner < 2000)):
        groessenklasse = "bis 2000"
    if(float(einwohner > 2000 and einwohner < 5000)):
        groessenklasse = "über 2.000 bis 5.000"
    if(float(einwohner > 5000 and einwohner < 10000)):
        groessenklasse = "über 5.000 bis 10.000"
    if(float(einwohner > 10000 and einwohner < 50000)):
        groessenklasse = "über 10.000 bis 50.000"
    if(float(einwohner > 50000 and einwohner < 100000)):
        groessenklasse = "über 50.000 bis 100.000"
    if(float(einwohner > 100000 and einwohner < 200000)):
        groessenklasse = "über 100.000 bis 200.000"
    if(float(einwohner > 200000 and einwohner < 500000)):
        groessenklasse = "über 200.000 bis 500.000"
    if(float(einwohner > 500000)):
        groessenklasse = "über 500.000"
    groessenklasse = groessenklasse.decode("utf-8")
    return groessenklasse

def ags_extrahieren(projektname):
    import arcpy,sys,os
    base_path = str(sys.path[0]).split("2_Tool")[0]
    print("Den AGS aus der Lage der Projektflaeche im Raum ermitteln")
    #arcpy.AddMessage("Den AGS aus der Lage der projektfläche im Raum ermitteln")
    projektFlaeche = os.path.join(base_path ,"3_Projekte",  projektname ,"FGDB_11_Definition_Projekt_" + projektname +".gdb","Teilflaechen_Plangebiet")
    bkg = os.path.join( base_path, "1_Basisdaten","FGBD_01_Basisdaten_deutschland.gdb","bkg_gemeinden")
    #ags aus BKG Daten extrahieren, dafür Gemeinde selektieren, die von Planfläche geschnitten wird
    #1. Feature Layer aus den bkg-daten erstellen
    try:
        arcpy.Delete_management("bkg_lyr")
    except:
        print""
    arcpy.MakeFeatureLayer_management(bkg,"bkg_lyr")
    #2.Spatial Select wo Planfläche bkg_lyr intersected
    arcpy.SelectLayerByLocation_management("bkg_lyr", "INTERSECT", projektFlaeche)
    #Wenn Flaeche = 1, ags extrahieren
    n = arcpy.GetCount_management("bkg_lyr").getOutput(0)
    if(int(n) ==1 ):
        gemeindeCursor = arcpy.SearchCursor("bkg_lyr")
        for gemeinde in gemeindeCursor:
            ags = gemeinde.AGS
    return ags

def gewerbesteuer(projektname,jahr,aufsiedlungsstand):

    #-------------------------------------------------------------------------------
    # Name:        32_Gewerbesteuer
    # Purpose:
    #
    # Author:      rieffel
    #
    # Created:     08.07.2013
    # Copyright:   (c) rieffel 2013
    # Licence:     <your licence>
    #-------------------------------------------------------------------------------


    import arcpy, sys, os
    #Pfad anlegen
    base_path = str(sys.path[0]).split("2_Tool")[0]
    wcd = os.getcwd()
    rootPfad = wcd.split("2_")[0]

    #ags aus BKG Daten extrahieren,
    ags = ags_extrahieren(projektname)
    #arcpy.AddMessage(ags)

    #02: Kommunalen Hebesatz und Kreisumlage aus der Tabelle Steuersaetze2010 im GrundannahmenOrdner via ags extrahieren
    sql = "ags = " + "'"+ags+"'"
    table3 = os.path.join(base_path,"1_Basisdaten","FGBD_01_Basisdaten_deutschland.gdb","Steuersaetze_2010")
    rows = arcpy.SearchCursor(table3, sql)
    count = 0
    for row in rows:
        count+=1
        #arcpy.AddMessage(row.Gewerbesteuer)

    if count == 0:
        #Falls mit dem AGS nichts gefunden wird auf Samtgemeinde testen und aktualisierten AGS verwenden
        ags = ags_samtgemeinde(projektname)
        #arcpy.AddMessage(ags)
        del rows
        sql = "ags = " + "'"+ags+"'"
        table3 = os.path.join(base_path,"1_Basisdaten","FGBD_01_Basisdaten_deutschland.gdb","Steuersaetze_2010")
        rows = arcpy.SearchCursor(table3, sql)
        count = 0
        for row in rows:
            count +=1
        if count == 0:
            arcpy.AddMessage("Keine Hebesaetze fur den AGS " + str(ags) + " gefunden, Abbruch...")
            sys.exit()
    table3 = os.path.join(base_path,"1_Basisdaten","FGBD_01_Basisdaten_deutschland.gdb","Steuersaetze_2010")
    rows = arcpy.SearchCursor(table3, sql)
    for row in rows:
        gewerbesteuerHebesatz = row.getValue("Gewerbesteuer")
        Kreisumlage = row.getValue("kreisumlage")
    del rows

    #03: Fiktiven Hebsatz festlegen
    fiktiverHebesatz= 403
    #ToDo: Fiktiver Hebesatz?

    #Iteriere durch die Wirtschaftsabschnitte und bilde Summe ueber die Ergebnisse
    wirtschaftsabschnitte = ["A–O","A/B","C","D","E","F","G","H","I","J","K","L","M","N","O"]

    gewerbesteueraufkommen = 0
    gewerbesteuerumlage = 0
    gewerbesteueraufkommenNachKFANRW = 0
    abschoepfungsquoteNRW = 0

    for wirtschaftsabschnitt in wirtschaftsabschnitte:

        try:
            #04: Gewerbesteuermessbetrag aus der Tabelle Gewerbesteuermessbeträge im Toolordner auslesen
            sql = "typ = " + "'"+wirtschaftsabschnitt+"'"
            table3 = os.path.join(base_path, '2_Tool','32_Einnahmen','FGDB_32_Einnahmen_Tool.gdb','gewerbesteuermessbetraege')
            rows = arcpy.SearchCursor(table3, sql)
            for row in rows:
                messbetragBRD = row.getValue("BRD")
                messbetragNRW = row.getValue("NRW")
                messbetragNISA = row.getValue("Niedersachsen")
            del rows

            #Berechnung des Gewerbesteueraufkommens
            #Gewerbesteuermessbetrag
            #05: Abfragen ob die KOmmune in NRW oder Niedersachsen liegt und messbetrag zuweisen
            #TODO: erweitern auf alle Bundeslänedr
            if(ags[1] == "5"):
                gewerbesteuermessbetrag = messbetragNRW
            elif(ags[1]=="3"):
                gewerbesteuermessbetrag = messbetragNISA
            else:
                gewerbesteuermessbetrag = messbetragBRD

            #06: Aufsiedlungsstand miteinbeziehen
            gewerbesteuermessbetrag = float(gewerbesteuermessbetrag)*float(aufsiedlungsstand)/100

            #07: gewerbestueraufkommen berechnen
            gewerbesteueraufkommen = gewerbesteuermessbetrag*float(gewerbesteuerHebesatz) + gewerbesteueraufkommen

            #08: Den Vervielfältiger extrahieren
            #wenn jahr < 2010 jahr = 2010, da der viervielfältiger nur ab 2010 vor liegt

            sql = "jahr = " + str(jahr)
            table3 = os.path.join(base_path,'2_Tool','32_Einnahmen','FGDB_32_Einnahmen_Tool.gdb','vervielfaeltiger_gewerbesteuer')
            rows = arcpy.SearchCursor(table3, sql)
            for row in rows:
                vervielfaeltiger = row.Gesamt_alteBL
            del rows
            #ToDo: Tabelle "vervielfaeltiger_gewerbesteuer' geht nur bis 2030

            #09: Gewerbesteuerumlage
            gewerbesteuerumlage = gewerbesteueraufkommen/float(gewerbesteuerHebesatz)*float(vervielfaeltiger) + gewerbesteuerumlage
            #10: Gewerbesteueraufkommen abzüglich Umlage
            gewerbesteueraufkommenMinusUmlage = gewerbesteueraufkommen - gewerbesteuerumlage
            #11: Abschöpfungsquote NRW
            abschoepfungsquoteNRW = (float(Kreisumlage)+0.9-0.9*float(Kreisumlage))*(fiktiverHebesatz-float(vervielfaeltiger))/(float(gewerbesteuerHebesatz)*100)+(float(vervielfaeltiger)/(float(gewerbesteuerHebesatz)*100)) + abschoepfungsquoteNRW
            #12: Gewerbesteueraufkommen nach KFA NRW
            gewerbesteueraufkommenNachKFANRW = gewerbesteueraufkommen*(1-abschoepfungsquoteNRW) + gewerbesteueraufkommenNachKFANRW

        except Exception as e:
            arcpy.AddMessage(e)

    arcpy.AddMessage(gewerbesteueraufkommen)
    arcpy.AddMessage(gewerbesteuerumlage)

    #13: Gewerbesteuereinnahmen in Tabelle abspeichern
    sql = "ags = " + "'"+ ags+"'"

    ergebnistabelle = os.path.join(base_path,"3_Projekte",projektname,"FGDB_32_Einnahmen_Projekt_"+projektname+".gdb","Gewerbesteuer")
    #arcpy.AddMessage(ergebnistabelle)
    try:
        Update = arcpy.UpdateCursor(ergebnistabelle,sql)
        count = 0
        for row in Update:
            count = count +1
        #arcpy.AddMessage(count)
        if(count>0):
            for row in Update:
                row.gewerbesteueraufkommen = float(gewerbesteueraufkommen)
                row.gewerbesteuerumlage = float(gewerbesteuerumlage)
                row.gewerbesteueraufkommenNachKFANRW = float(gewerbesteueraufkommenNachKFANRW)
                row.abschoepfungsquoteNRW = float(abschoepfungsquoteNRW)
                row.ags = ags
                Update.updateRow(row)
        else:
            Insert = arcpy.InsertCursor(ergebnistabelle)
            row = Insert.newRow()
            row.gewerbesteueraufkommen = float(gewerbesteueraufkommen)
            row.gewerbesteuerumlage = float(gewerbesteuerumlage)
            row.gewerbesteueraufkommenNachKFANRW = float(gewerbesteueraufkommenNachKFANRW)
            row.abschoepfungsquoteNRW = float(abschoepfungsquoteNRW)
            row.ags = ags
            Insert.insertRow(row)
            del Insert, row
        try:
            del Update, row,
        except Exception as e:
            arcpy.AddMessage(e)
    except Exception as e:

        arcpy.AddMessage(e)

def ags_samtgemeinde(projektname):#
    # TODO wenn json return = [] ags der samtgemeinde fuer eine neue abfrage nutzen
    import arcpy,sys,os
    base_path = str(sys.path[0]).split("2_Tool")[0]
    print("Den AGS aus der Lage der Projektflaeche im Raum ermitteln")
    #arcpy.AddMessage("Den AGS aus der Lage der projektfläche im Raum ermitteln")
    projektFlaeche = os.path.join(base_path ,"3_Projekte",  projektname ,"FGDB_11_Definition_Projekt_" + projektname +".gdb","Teilflaechen_Plangebiet")
    vgm = os.path.join( base_path, "1_Basisdaten","FGBD_01_Basisdaten_deutschland.gdb","vgm")
    #ags aus BKG Daten extrahieren, dafür Gemeinde selektieren, die von Planfläche geschnitten wird
    #1. Feature Layer aus den bkg-daten erstellen
    try:
        arcpy.Delete_management("vgm_lyr")
    except:
        print""
    arcpy.MakeFeatureLayer_management(vgm,"vgm_lyr")
    #2.Spatial Select wo Planfläche vgm_lyr intersected
    arcpy.SelectLayerByLocation_management("vgm_lyr", "INTERSECT", projektFlaeche)
    #Wenn Flaeche = 1, ags extrahieren
    n = arcpy.GetCount_management("vgm_lyr").getOutput(0)
    print n


    if(int(n) == 1 ):
        gemeindeCursor = arcpy.SearchCursor("vgm_lyr")
        for gemeinde in gemeindeCursor:
            ags_temp = gemeinde.SDV_RS
    else:
        arcpy.AddMessage("Die Projektflaechen liegen innerhalb mehrerer Gemeinden, das Tool unterstuetzt zur Zeit keine interkommunalen Projekte.")
        ## TODO Dateien loeschen und Projektregistrierung loeschen)
        sys.exit()
    ags = str(ags_temp[0:5])+str(ags_temp[6:])

    return ags

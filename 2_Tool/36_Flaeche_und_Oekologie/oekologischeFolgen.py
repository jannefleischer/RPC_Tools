# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# oekologischeFolgen.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# ILS gGmbH
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


import lib_oekologischeFolgen as f, arcpy, datetime, os, sys, xlsxwriter, imp
from xlsxwriter.utility import xl_rowcol_to_cell, xl_range

sheetlibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '11_Definition_Projekt','sheet_lib.py'))
sl = imp.load_source('sheet_lib', sheetlibpath)

#Parameter erstellen
i =0
projektName = "Template"
projektName = arcpy.GetParameterAsText(i)
i=i+1
region = arcpy.GetParameterAsText(i)
#if region == "Landkreis Harburg":
#    region = "Duesseldorf"

schrittmeldung = 'Oekologische Flaechenleistung ermitteln  \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

wcd = os.getcwd()
rootPfad = str(sys.path[0]).split("2_Tool")[0]
bodenbedeckungTabelle = os.path.join(rootPfad,"3_Projekte",projektName,"FGDB_36_Flaeche_und_Oekologie_Projekt_" + projektName + ".gdb","Bodenbedeckung")

bedeckungstabelle = arcpy.SearchCursor(bodenbedeckungTabelle)
NF_ueberbauteFlaechen = 0
NF_AsphaltBeton = 0
NF_Platten = 0
NF_Kleinpflaster = 0
NF_Rasengitter = 0
NF_Acker = 0
NF_Rasen = 0
NF_BaeumeStraeucher = 0
NF_Stauden = 0
NF_Wiese = 0
NF_Wasserflaeche = 0
PF_ueberbauteFlaechen = 0
PF_AsphaltBeton = 0
PF_Platten = 0
PF_Kleinpflaster = 0
PF_Rasengitter = 0
PF_Acker = 0
PF_Rasen = 0
PF_BaeumeStraeucher = 0
PF_Stauden = 0
PF_Wiese = 0
PF_Wasserflaeche = 0
for row in bedeckungstabelle:
    NF_ueberbauteFlaechen = NF_ueberbauteFlaechen + row.NF_ueberbauteFlaechen
    NF_AsphaltBeton = NF_AsphaltBeton + row.NF_AsphaltBeton
    NF_Platten = NF_Platten + row.NF_Platten
    NF_Kleinpflaster = NF_Kleinpflaster + row.NF_Kleinpflaster
    NF_Rasengitter = NF_Rasengitter + row.NF_Rasengitter
    NF_Acker = NF_Acker + row.NF_Acker
    NF_Rasen = NF_Rasen + row.NF_Rasen
    NF_BaeumeStraeucher = NF_BaeumeStraeucher + row.NF_BaeumeStraeucher
    NF_Stauden = NF_Stauden + row.NF_Stauden
    NF_Wiese = NF_Wiese + row.NF_Wiese
    NF_Wasserflaeche = NF_Wasserflaeche + row.NF_Wasserflaeche

    PF_ueberbauteFlaechen = PF_ueberbauteFlaechen + row.PF_ueberbauteFlaechen
    PF_AsphaltBeton = PF_AsphaltBeton + row.PF_AsphaltBeton
    PF_Platten = PF_Platten + row.PF_Platten
    PF_Kleinpflaster = PF_Kleinpflaster + row.PF_Kleinpflaster
    PF_Rasengitter = PF_Rasengitter + row.PF_Rasengitter
    PF_Acker = PF_Acker + row.PF_Acker
    PF_Rasen = PF_Rasen + row.PF_Rasen
    PF_BaeumeStraeucher = PF_BaeumeStraeucher + row.PF_BaeumeStraeucher
    PF_Stauden = PF_Stauden + row.PF_Stauden
    PF_Wiese = PF_Wiese + row.PF_Wiese
    PF_Wasserflaeche = PF_Wasserflaeche + row.PF_Wasserflaeche
bedeckungNullfall = [NF_ueberbauteFlaechen,NF_AsphaltBeton,NF_Platten,NF_Kleinpflaster,NF_Rasengitter,NF_Acker,NF_Rasen,NF_BaeumeStraeucher,NF_Stauden,NF_Wiese,NF_Wasserflaeche]
#bedeckungNullfall = [4.9,4.9,0,0,0,0,0,0,0,14.7,0]
arcpy.AddMessage(bedeckungNullfall)
bedeckungPlanfall = [PF_ueberbauteFlaechen,PF_AsphaltBeton,PF_Platten,PF_Kleinpflaster,PF_Rasengitter,PF_Acker,PF_Rasen,PF_BaeumeStraeucher,PF_Stauden,PF_Wiese,PF_Wasserflaeche]
#bedeckungPlanfall = [9.8,7.3,0,0,0,0,0,0,0,7.3,0]
arcpy.AddMessage(bedeckungPlanfall)


schrittmeldung = 'Integrationsgrad ermitteln  \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

i=i+1
gemeinsameGrenze = 0
gemeinsameGrenze = arcpy.GetParameterAsText(i)
i=i+1
gesamteGrenze = 0
gesamteGrenze = arcpy.GetParameterAsText(i)
#i=i+1
#neuinanspruchnameHA = 2.3
#neuinanspruchnameHA = arcpy.GetParameterAsText(i)
#neuinanspruchnameHA = neuinanspruchnameHA.replace(",",".")
#i=i+1
#bebauungsdichteWEproHA = 25
#bebauungsdichteWEproHA = arcpy.GetParameterAsText(i)
#i=i+1
#frueherBauluecke = "False"
#frueherBauluecke = arcpy.GetParameterAsText(i)
i=i+1
flaechentyp = "Wohnen"
flaechentyp = arcpy.GetParameterAsText(i)
i=i+1
schutzBoden = arcpy.GetParameterAsText(i)

try:

    #1.Lokale Effekte
    schrittmeldung = 'Oekologische Flaechenleistung bewerten  \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    oekologischeFlaechenleistungPunkte = f.oekologischeFolgen(bedeckungNullfall, bedeckungPlanfall)
    #Rueckgabe: Liste: ['Punktwert Nullfall=x', 'Punktwert Planfall=y']
    punktwertNullfall = oekologischeFlaechenleistungPunkte[0].split("=")[1]
    punktwertPlanfall = oekologischeFlaechenleistungPunkte[1].split("=")[1]

    #2a. Regionale Effekte - Landschaftszerschneidung
    schrittmeldung = 'Landschaftszerschneidung bewerten  \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    uzvr = f.uzvr(projektName, region)
    bewertungUZVRNullfall = uzvr[0]
    begegnungswahrscheinlichkeitUZVRNullfall = uzvr[1]
    begegnungswahrscheinlichkeitUZVRPlanfall = uzvr[2]
    groessterUZVR = uzvr[3]
    #
    # print("bewertungUZVRNullfall: "+str(bewertungUZVRNullfall) + "\n")
    # arcpy.AddMessage("bewertungUZVRNullfall: "+str(bewertungUZVRNullfall) + "\n")
    # print("begegnungswahrscheinlichkeitUZVRNullfall: "+str(begegnungswahrscheinlichkeitUZVRNullfall) + "\n")
    # arcpy.AddMessage("begegnungswahrscheinlichkeitUZVRNullfall: "+str(begegnungswahrscheinlichkeitUZVRNullfall) + "\n")
    # print("begegnungswahrscheinlichkeitUZVRPlanfall: "+str(begegnungswahrscheinlichkeitUZVRPlanfall) + "\n")
    # arcpy.AddMessage("begegnungswahrscheinlichkeitUZVRPlanfall: "+str(begegnungswahrscheinlichkeitUZVRPlanfall) + "\n")
    # print("groessterUZVR: "+str(groessterUZVR) + "\n")
    # arcpy.AddMessage("groessterUZVR: "+str(groessterUZVR) + "\n")

    #2b - Regionale Effekte - Kaltluftströmungen
    #Integration von KLAMM21

    #3a. Einordnung der Region Schutzstatus Biotope & Boden
    schrittmeldung = 'Betroffenheit von Schutzgebieten pruefen  \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    ueberschneidungen = f.oekologischeWertigkeit(projektName)
    ueberschneidungBiotope = ueberschneidungen[0].split("=")[1]
    ueberschneidungNaturschutzgebiete = ueberschneidungen[1].split("=")[1]
    ueberschneidungNationalparke = ueberschneidungen[2].split("=")[1]
    ueberschneidungFFHGebiete = ueberschneidungen[3].split("=")[1]
    ueberschneidungVogelschutzgebiete = ueberschneidungen[4].split("=")[1]
    if(ueberschneidungBiotope == 1 or ueberschneidungNaturschutzgebiete == 1 or ueberschneidungNationalparke == 1 or ueberschneidungFFHGebiete == 1 or ueberschneidungVogelschutzgebiete == 1):
        schutzstatusBiotope = 1
    else:
        schutzstatusBiotope = 0

    #Schutzstatus Boden
    #WMS einbinden und manuelle Kontrolle
        #Test auf Ueberschneidung der Planflaeche mit Schutzwuerdigen Boeden:
    schrittmeldung = 'Betroffenheit von schutzwuerdigen Boeden pruefen  \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    arcpy.AddMessage("Schutzwuerdige Boeden betroffen:" + schutzBoden)
    if str(schutzBoden) == "Ja":
        schutzStatusBoden = 1
    if str(schutzBoden) == "Nein":
        schutzStatusBoden = 0


    #3b - Einordnung in die Region - Flächeninanspruchname
    #Vorraussetzung: Integrationsgrad berechnen:
    schrittmeldung = 'Integration bewerten  \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    integrationsgrad = f.IntegrationsGrad(gemeinsameGrenze,gesamteGrenze)[0]
    bewertungIntegration = f.IntegrationsGrad(gemeinsameGrenze,gesamteGrenze)[1]
    #def flaechenInanspruchname(neuinanspruchname, projektName, bebauungsdichte, integrationsgrad,bauluecke,typ):
    flaecheninanspruchname = f.flaechenInanspruchname(integrationsgrad, flaechentyp)
    #bewertungQuantitaet = flaecheninanspruchname[0]
    #bewertungDichte = flaecheninanspruchname[1]
    #bewertungIntegration = flaecheninanspruchname[2]

    ##Pfade vorbereiten
    #aktueller Pfad
    schrittmeldung = 'Ergebnisse in Datenbank schreiben  \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    wcd = os.getcwd()
    rootPfad = str(sys.path[0]).split("2_Tool")[0]
    ergebnisTabelle = os.path.join(rootPfad,'3_Projekte',projektName,'FGDB_36_Flaeche_und_Oekologie_Projekt_'+projektName+'.gdb','Ergebnisse_oekologischeWertigkeit')
    ueberschneidungBiotope = int(ueberschneidungBiotope)
    ueberschneidungFFHGebiete = int(ueberschneidungFFHGebiete)
    ueberschneidungNationalparke = int(ueberschneidungNationalparke)
    ueberschneidungNaturschutzgebiete = int(ueberschneidungNaturschutzgebiete)
    ueberschneidungVogelschutzgebiete = int(ueberschneidungVogelschutzgebiete)
    punktwertNullfall = float(punktwertNullfall)
    punktwertPlanfall = float(punktwertPlanfall)
    begegnungswahrscheinlichkeitUZVRNullfall = float(begegnungswahrscheinlichkeitUZVRNullfall)
    begegnungswahrscheinlichkeitUZVRPlanfall = float(begegnungswahrscheinlichkeitUZVRPlanfall)
    bewertungUZVRNullfall = float(bewertungUZVRNullfall)
    schutzStatusBoden = int(schutzStatusBoden)
    integrationsgrad = float(integrationsgrad)
    bewertungIntegration = float(bewertungIntegration)
    groessterUZVR = groessterUZVR

    #Ergebnisse speichern
    #aktuelle Zeit
    time = datetime.datetime.now()
    timestamp = str(time.hour) + ":" + str(time.minute) + ":" + str(time.second) + "-" + str(time.day) + "/" + str(time.month) + "/" + str(time.year)
    #insert Cursor für die Ergebnistabelle erstellen
    ergebnisCursor = arcpy.InsertCursor(ergebnisTabelle)
    #eine neue Zeile für das Ergebnis dieses Durchlaufs anlegen
    ergebnisZeile = ergebnisCursor.newRow()
    ergebnisZeile.pwNull = punktwertNullfall
    ergebnisZeile.pwPlan = punktwertPlanfall
    ergebnisZeile.begeg_null = begegnungswahrscheinlichkeitUZVRNullfall
    ergebnisZeile.begeg_plan = begegnungswahrscheinlichkeitUZVRPlanfall
    ergebnisZeile.uvzr_null = bewertungUZVRNullfall
    ergebnisZeile.groeUZVR = groessterUZVR
    ergebnisZeile.Biotope = ueberschneidungBiotope
    ergebnisZeile.Naturschutzgebiete = ueberschneidungNaturschutzgebiete
    ergebnisZeile.Nationalparke = ueberschneidungNationalparke
    ergebnisZeile.FFH_Gebiete = ueberschneidungFFHGebiete
    ergebnisZeile.Vogelschutzgebiete = ueberschneidungVogelschutzgebiete
##    ergebnisZeile.statusBiotope = schutzstatusBiotope --> aufgrund fehlerhafter Abfrage wird dieser Schritt in der Ergebnisausgabe abgefragt
    ergebnisZeile.statusBoden = schutzStatusBoden
    ergebnisZeile.integration = integrationsgrad
    ergebnisZeile.bewertung_Integra = bewertungIntegration
    ergebnisZeile.timestamp = timestamp
    ergebnisCursor.insertRow(ergebnisZeile)
    arcpy.AddMessage("Schutzwürdige Böden betroffen? = " + str(schutzBoden))
    print("Ergebnisse gespeichert")
    arcpy.AddMessage("Ergebnisse gespeichert")
    del ergebnisCursor

except Exception as e:
    print e
    arcpy.AddMessage(e)
    try:
        del ergebnisCursor
    except:
        print"Trauer"




#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################

# Schritt 6 - Datenexport in Excel-Datei
schrittmeldung = 'Datenexport in Excel-Datei  \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

# Pfade setzen
base_path = str(sys.path[0]).split("2_Tool")[0]
workspace_projekt_oekologie = os.path.join(base_path,'3_Projekte',projektName,'FGDB_36_Flaeche_und_Oekologie_Projekt_'+projektName+'.gdb')
tablepath_Bodenbedeckung = os.path.join(workspace_projekt_oekologie,'Bodenbedeckung')
tablepath_Integration = os.path.join(workspace_projekt_oekologie,'Ergebnisse_Integrationsgrad')
tablepath_oekWert = os.path.join(workspace_projekt_oekologie,'Ergebnisse_oekologischeWertigkeit')
tablepath_Wohnflaechendichte = os.path.join(workspace_projekt_oekologie,'Ergebnisse_Wohnflaechendichte')
grafikpath_erlauterungstext = os.path.join(base_path,'2_Tool','36_Flaeche_und_Oekologie','Erlauterungstexte')

logo = os.path.join((str(sys.path[0]).split("2_Tool")[0]),"1_Basisdaten","logo_rpc.png")
ausgabeordner = os.path.join(base_path,'3_Projekte',projektName,'Ergebnisausgabe','Excel')
excelpfad = os.path.join(ausgabeordner,'36_Flaeche_und_Oekologie.xlsx')

try:
    os.remove(excelpfad)
except:
    pass

# Workbook und Tabellenblätter anlegen
wb = xlsxwriter.Workbook(excelpfad)
sl.infosheet(projektName, str("Projektrahmendaten").decode('utf-8'), wb)
ws2 = wb.add_worksheet('Methodik_Uebersicht')
ws3 = wb.add_worksheet('Methodik_lokale Effekte')
ws5 = wb.add_worksheet('Auswertungen_lokale Effekte')
ws6 = wb.add_worksheet('Methodik_regionale Effekte')
ws7 = wb.add_worksheet('Auswertungen_regionale Effekte')
ws8 = wb.add_worksheet('Methodik_Einordnung Region')
ws9 = wb.add_worksheet('Auswertungen_Einordnung Region')
#ws10 = wb.add_worksheet('Ergebnisuebersicht')
ws11 = wb.add_worksheet('Literatur')
ws4 = wb.add_worksheet('Rohdaten')
#ws12 = wb.add_worksheet('Rohdaten')

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
        ws6.write(x,y,"", format)
        ws7.write(x,y,"", format)
        ws8.write(x,y,"", format)
        ws9.write(x,y,"", format)
        # ws10.write(x,y,"", format)
        ws11.write(x,y,"", format)
        #ws12.write(x,y,"", format)

###Spaltenbreiten definieren
ws2.set_column(0, 0, 86)
ws3.set_column(0, 0, 86)
ws5.set_column(0, 0, 40)
ws6.set_column(0, 0, 86)
ws7.set_column(0, 0, 24)
ws8.set_column(0, 0, 86)
ws9.set_column(0, 0, 22)
ws11.set_column(0, 0, 86)


########
## Erläuterungstexte einfügen
# Pfade zu Grafiken herstellen
Text1 = os.path.join(grafikpath_erlauterungstext, 'Methodik_FlaecheOekologie1.png')
Text2 = os.path.join(grafikpath_erlauterungstext, 'Methodik_FlaecheOekologie2.png')
Text3 = os.path.join(grafikpath_erlauterungstext, 'Methodik_FlaecheOekologie3.png')
Text4a = os.path.join(grafikpath_erlauterungstext, 'Methodik_FlaecheOekologie4a.png')
Text4b = os.path.join(grafikpath_erlauterungstext, 'Methodik_FlaecheOekologie4b.png')
Text5 = os.path.join(grafikpath_erlauterungstext, 'Methodik_FlaecheOekologie5.png')
Text6 = os.path.join(grafikpath_erlauterungstext, 'Haftungsausschluss.png')

###Grafiken einfügen
ws2.insert_image(0, 0, Text1, {'x_scale': 0.32, 'y_scale': 0.32})
ws2.insert_image(40, 0, Text6, {'x_scale': 0.32, 'y_scale': 0.32})
ws3.insert_image(0, 0, Text2, {'x_scale': 0.32, 'y_scale': 0.32})
ws6.insert_image(0, 0, Text3, {'x_scale': 0.32, 'y_scale': 0.32})
ws8.insert_image(0, 0, Text4a, {'x_scale': 0.32, 'y_scale': 0.32})
ws8.insert_image(40, 0, Text4b, {'x_scale': 0.32, 'y_scale': 0.32})
ws11.insert_image(0, 0, Text5, {'x_scale': 0.32, 'y_scale': 0.32})


########
###### Tabellenblatt 4: Rohdaten einladen
## Teil 1: Bodenbedeckung
#Teil 1a Bezeichnungen Bodenbedeckung einfügen
j = 0
ws4.write(j, 0, 'Rohadtentabelle', bold)
j = j + 2
ws4.write(j, 0, 'Bodenbedeckung', bold)
j = j + 2
ws4.write(j, 0, 'Zeilennummer', normal)
i = 1
fieldnames = [f.name for f in arcpy.ListFields(tablepath_Bodenbedeckung)]
for fieldname in fieldnames:
    ws4.write(j, i, fieldname, normal)
    i = i + 1


# Teil 1b Werte Bodenbedeckung einfügen

#Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
rows = arcpy.SearchCursor(tablepath_Bodenbedeckung)

#Feldnamen auslesen
fieldnames = [f.name for f in arcpy.ListFields(tablepath_Bodenbedeckung)]

###Bodenbedeckung auslesen
j = j + 1
BBedYstart = j
wert = 0
for row in rows:
    i = 0
    for fieldname in fieldnames:
        try:
            wert = row.getValue(fieldname)
        except:
            wert = row.getValue(fieldname)
        ws4.write(j, i, wert, normal)
        i = i + 1
    j = j + 1
    BBedYend = j

# Teil 2: Ökologische Wertigkeit
#Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
rows = arcpy.SearchCursor(tablepath_oekWert)

#Feldnamen auslesen
fieldnames = [f.name for f in arcpy.ListFields(tablepath_oekWert)]

#Teil 2a: Bezeichnungen ökologische Wertigkeit einfügen
j = j + 3
ws4.write(j, 0, 'Oekologische Wertigkeit', bold)
i = 0
j = j + 1
for fieldname in fieldnames:
    column_with = len(fieldname)+2
    ws4.set_column(i, i, column_with)
    ws4.write(j, i, fieldname, normal)
    i = i + 1

#Teil 2b: Ergebnisse ökologische Wertigkeit auslesen
wert = 0
j = j + 1
for row in rows:
    i = 0
    for fieldname in fieldnames:
        try:
            wert = row.getValue(fieldname)
        except:
            wert = row.getValue(fieldname)
        ws4.write(j, i, wert, normal)
        i = i + 1
    j = j + 1
OekWertZeile = j - 1

# Teil 3: Wohnflächendichte
# Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
rows = arcpy.SearchCursor(tablepath_Wohnflaechendichte)

# Feldnamen auslesen
fieldnames = [f.name for f in arcpy.ListFields(tablepath_Wohnflaechendichte)]

#Teil 2a: Bezeichnungen Wohnflächendichte einfügen
if flaechentyp == "Wohnen":
    j = j + 3
    ws4.write(j, 0, 'Wohnflaechendichte', bold)
    i = 0
    j = j + 1
    j = j + 1
    for fieldname in fieldnames:
        column_with = len(fieldname)+2
        ws4.set_column(i, i, column_with)
        ws4.write(j, i, fieldname, normal)
        i = i + 1

    # Teil 2b: Ergebnisse Wohnflächendichte auslesen
    wert = 0
    j = j + 1
    for row in rows:
        i = 0
        for fieldname in fieldnames:
            try:
                wert = row.getValue(fieldname)
            except:
                wert = row.getValue(fieldname)
            ws4.write(j, i, wert, normal)
            i = i + 1
        j = j + 1
    WFDWertZeile = j - 1


    # Teil 3: Charts anlegen
    chart_wohnflaeche = wb.add_chart({'type': 'column'})
    chart_wohnflaeche.set_style(40)
    chart_wohnflaeche.set_size({'width': 800, 'height': 300})
    chart_wohnflaeche.set_chartarea({'border': {'none': True},'fill': {'none': True}})
    chart_wohnflaeche.set_legend({'none': 'true'})
    chart_wohnflaeche.set_title({'name': 'Wohnflaechendichte','name_font':  {'name': 'Tahoma', 'size': 9}})

    # Werte in Chartobjekte schreiben: WICHTIG: Tabellenblaetter mit Leerzeichen sind in jedem Fall mit einfachen ' einzuklammern und aussen " zu verwenden
    chart_wohnflaeche.add_series({
    'values': "='Auswertungen_Einordnung Regio'!$B$18:$B$20",
    'categories': "='Auswertungen_Einordnung Region'!$A$18:$A$20",
    })


########
###### Tabellenblatt 5: Uebersicht lokale Effekte
# Teil 1: Beschriftungen
j = 0
ws5.write(j, 0, 'Uebersicht lokale Effekte', bold)
j = j + 2
ws5.write(j, 0, 'Bodenbedeckung [in Hektar]', bold)
j = j + 1
ws5.write(j, 1, 'Nullfall', bold)
ws5.write(j, 2, 'Planfall', bold)
j = j + 1
ws5.write(j, 0, 'Ueberbaute Flaechen', bold)
j = j + 1
ws5.write(j, 0, 'Asphalt, Beton', bold)
j = j + 1
ws5.write(j, 0, 'Platten', bold)
j = j + 1
ws5.write(j, 0, 'Kleinpflaster', bold)
j = j + 1
ws5.write(j, 0, 'Wassergebundene Decke, Rasengittersteine', bold)
j = j + 1
ws5.write(j, 0, 'Offener Boden, Acker', bold)
j = j + 1
ws5.write(j, 0, 'Rasen', bold)
j = j + 1
ws5.write(j, 0, 'Baeume, Straeucher', bold)
j = j + 1
ws5.write(j, 0, 'Stauden', bold)
j = j + 1
ws5.write(j, 0, 'Wiese', bold)
j = j + 1
ws5.write(j, 0, 'Natuerliche Wasserflaeche', bold)
j = j + 3
ws5.write(j, 0, 'Bodenbedeckung [in Prozent]', bold)
j = j + 1
ws5.write(j, 1, 'Nullfall', bold)
ws5.write(j, 2, 'Planfall', bold)
j = j + 1
ws5.write(j, 0, 'Ueberbaute Flaechen', bold)
j = j + 1
ws5.write(j, 0, 'Asphalt, Beton', bold)
j = j + 1
ws5.write(j, 0, 'Platten', bold)
j = j + 1
ws5.write(j, 0, 'Kleinpflaster', bold)
j = j + 1
ws5.write(j, 0, 'Wassergebundene Decke, Rasengittersteine', bold)
j = j + 1
ws5.write(j, 0, 'Offener Boden, Acker', bold)
j = j + 1
ws5.write(j, 0, 'Rasen', bold)
j = j + 1
ws5.write(j, 0, 'Baeume, Straeucher', bold)
j = j + 1
ws5.write(j, 0, 'Stauden', bold)
j = j + 1
ws5.write(j, 0, 'Wiese', bold)
j = j + 1
ws5.write(j, 0, 'Natuerliche Wasserflaeche', bold)
j = j + 18
ws5.write(j, 0, 'Bewertung', bold)
j = j + 1
ws5.write(j, 0, 'Nullfall', normal)
ws5.write(j, 2, 'von 5 Punkten', normal)
j = j + 1
ws5.write(j, 0, 'Planfall', normal)
ws5.write(j, 2, 'von 5 Punkten', normal)
j = j + 1
ws5.write(j, 0, 'Gesamt', bold)
ws5.write(j, 2, 'von 5 Punkten', bold)


# Teil 2: Formeln und Werte einladen
formatDez = wb.add_format()
formatDez.set_num_format(0x02)
formatDez.set_bg_color('white')
formatDez.set_border(0)
j = 4
i = 1
x = 1
# Schleife für Nullfall und Planfall in Hektar
while j < 15:
    BBedRange = xl_range(BBedYstart,x,BBedYend-1,x)
    formulastring = '=SUM(Rohdaten!'+BBedRange+')'
    ws5.write_formula(j,i, formulastring,formatDez)
    j = j + 1
    x = x + 1
i = i + 1
j = 4
while j < 15:
    BBedRange = xl_range(BBedYstart,x,BBedYend-1,x)
    formulastring = '=SUM(Rohdaten!'+BBedRange+')'
    ws5.write_formula(j,i, formulastring,formatDez)
    j = j + 1
    x = x + 1

# Schleife für Nullfall und Planfall in Prozent
formatProz = wb.add_format()
formatProz.set_num_format(0x09)
formatProz.set_bg_color('white')
formatProz.set_border(0)
j = j + 4
i = 1
k = 4
while j < 30:
    RowColNull = xl_rowcol_to_cell(k,i)
    RowColPlan = xl_rowcol_to_cell(k,i+1)
    formulastringNull = '='+RowColNull+'/SUM(B$5:B$15)'
    formulastringPlan = '='+RowColPlan+'/SUM(C$5:C$15)'
    ws5.write_formula(j,i, formulastringNull,formatProz)
    ws5.write_formula(j,i+1, formulastringPlan,formatProz)
    k = k + 1
    j = j + 1

# Ergebniszusammenfassung Bodenbedeckung
j = j + 18
i = 1
RowColNull = xl_rowcol_to_cell(OekWertZeile, 7)
RowColPlan = xl_rowcol_to_cell(OekWertZeile, 8)
formulastringNull = '=Rohdaten!'+RowColNull+''
formulastringPlan = '=Rohdaten!'+RowColPlan+''
formulastringBOW = '=IF(B50=B49,IF(B50>5,5,IF(B50<1,1,B50)),IF(B49=(B50+1),IF(B50>5,5,IF(B50<1,1,B50)),IF(B49<B50,IF((1+B50)>5,5,IF((1+B50)<1,1,(1+B50))),IF(B49>B50,IF((B50-1)>5,5,IF((B50-1)<1,1,(B50-1)))))))'
ws5.write_formula(j,i, formulastringNull,normal)
ws5.write_formula(j+1,i, formulastringPlan,normal)
ws5.write_formula(j+2,i, formulastringBOW,bold)

# Teil 3: Charts anlegen
chart_Bodenbedeckung = wb.add_chart({'type': 'bar', 'subtype': 'percent_stacked'})
chart_Bodenbedeckung.set_style(40)
chart_Bodenbedeckung.set_size({'width': 800, 'height': 300})
chart_Bodenbedeckung.set_chartarea({'border': {'none': True},'fill': {'none': True}})
chart_Bodenbedeckung.set_legend({'position': 'bottom'})
chart_Bodenbedeckung.set_title({'name': 'Bodenbedeckungsarten','name_font':  {'name': 'Tahoma', 'size': 9}})

# Werte in Chartobjekte schreiben: WICHTIG: Tabellenblaetter mit Leerzeichen sind in jedem Fall mit einfachen ' einzuklammern und aussen " zu verwenden
chart_Bodenbedeckung.add_series({
'values': "='Auswertungen_lokale Effekte'!$B$5:$C$5",
'categories': "='Auswertungen_lokale Effekte'!$B$4:$C$4",
'name': 'Ueberbaute Flaechen',
})
chart_Bodenbedeckung.add_series({
'values': "='Auswertungen_lokale Effekte'!$B$6:$C$6",
'categories': "='Auswertungen_lokale Effekte'!$B$4:$C$4",
'name': 'Natuerliche Wasserflaeche',
})
chart_Bodenbedeckung.add_series({
'values': "='Auswertungen_lokale Effekte'!$B$7:$C$7",
'categories': "='Auswertungen_lokale Effekte'!$B$4:$C$4",
'name': 'Platten',
})
chart_Bodenbedeckung.add_series({
'values': "='Auswertungen_lokale Effekte'!$B$8:$C$8",
'categories': "='Auswertungen_lokale Effekte'!$B$4:$C$4",
'name': 'Baeume, Straeucher',
})
chart_Bodenbedeckung.add_series({
'values': "='Auswertungen_lokale Effekte'!$B$9:$C$9",
'categories': "='Auswertungen_lokale Effekte'!$B$4:$C$4",
'name': 'Wassergebundene Decke, Rasengittersteine',
})
chart_Bodenbedeckung.add_series({
'values': "='Auswertungen_lokale Effekte'!$B$10:$C$10",
'categories': "='Auswertungen_lokale Effekte'!$B$4:$C$4",
'name': 'Stauden',
})
chart_Bodenbedeckung.add_series({
'values': "='Auswertungen_lokale Effekte'!$B$11:$C$11",
'categories': "='Auswertungen_lokale Effekte'!$B$4:$C$4",
'name': 'Wiese',
})
chart_Bodenbedeckung.add_series({
'values': "='Auswertungen_lokale Effekte'!$B$12:$C$12",
'categories': "='Auswertungen_lokale Effekte'!$B$4:$C$4",
'name': 'Asphalt, Beton',
})
chart_Bodenbedeckung.add_series({
'values': "='Auswertungen_lokale Effekte'!$B$13:$C$13",
'categories': "='Auswertungen_lokale Effekte'!$B$4:$C$4",
'name': 'Offener Boden, Acker',
})
chart_Bodenbedeckung.add_series({
'values': "='Auswertungen_lokale Effekte'!$B$14:$C$14",
'categories': "='Auswertungen_lokale Effekte'!$B$4:$C$4",
'name': 'Kleinpflaster',
})
chart_Bodenbedeckung.add_series({
'values': "='Auswertungen_lokale Effekte'!$B$15:$C$15",
'categories': "='Auswertungen_lokale Effekte'!$B$4:$C$4",
'name': 'Rasen',
})


# Charts in Tabelle schreiben
ws5.insert_chart('A32', chart_Bodenbedeckung)
if flaechentyp == "Wohnen":
    ws9.insert_chart('A23', chart_wohnflaeche)


## Tabellenblatt 7: Übersicht regionale Effekte
# Teil 1 Beschriftungen einfügen
j = 0
i = 0
ws7.write(j, i, 'Uebersicht regionale Effekte', bold)
j = j + 2
ws7.write(j, i, 'Begegnungswahrscheinlichkeit', bold)
j = j + 1
ws7.write(j, i, 'Nullfall', normal)
i = i + 2
ws7.write(j, i, 'bei einem Index von 0 bis 1', normal)
i = 0
j = j + 1
ws7.write(j, i, 'Planfall', normal)
i = i + 2
ws7.write(j, i, 'bei einem Index von 0 bis 1', normal)
i = 0
j = j + 1
ws7.write(j, i, 'Bewertung', bold)
i = i + 2
ws7.write(j, i, 'von 5 Punkten', bold)
i = 0
j = j + 2
ws7.write(j, i, 'Unzerschnittene verkehrsarme Raeume', bold)
j = j + 1
ws7.write(j, i, 'Groesster tangierter UZVR', normal)
i = i + 2
ws7.write(j, i, 'Hektar', normal)
j = j + 1
i = 0
ws7.write(j, i, 'Bewertung UZVR', normal)
i = i + 2
ws7.write(j, i, 'von 5 Punkten', normal)

# Teil 2: Formeln und Werte einladen
formatHidden = wb.add_format()
formatHidden.set_num_format(0x01)
formatHidden.set_font_color('white')
formatHidden.set_bg_color('white')
formatHidden.set_border(0)

j = 3
i = 1
RowColBegN = xl_rowcol_to_cell(OekWertZeile, 9)
RowColBegP = xl_rowcol_to_cell(OekWertZeile, 10)
RowColUZVR = xl_rowcol_to_cell(OekWertZeile, 16)
RowColUZVRbew = xl_rowcol_to_cell(OekWertZeile, 11)
formulastringBegN = '=Rohdaten!'+RowColBegN+''
formulastringBegP = '=Rohdaten!'+RowColBegP+''
formulastringBegB1 = '=IF(AND(B4<B5+0.2,B4>B5-0.2),B5,IF(B5<=B4-0.2,B5-0.2,IF(B5>=B4+0.2,B5+0.2)))'
formulastringBegB2 = '=IF(F6>1,1,IF(F6<0,0,F6))'
formulastringBegB3 = '=IF(G6<0.2,1,IF(AND(G6>=0.2,G6<0.4),2,IF(AND(G6>=0.4,G6<0.6),3,IF(AND(G6>=0.6,G6<0.8),4,IF(G6>=0.8,5)))))'
formulastringUZVR = '=Rohdaten!'+RowColUZVR+''
formulastringUZVRbew = '=Rohdaten!'+RowColUZVRbew+''
ws7.write_formula(j,i, formulastringBegN,normal)
ws7.write_formula(j+1,i, formulastringBegP,normal)
ws7.write_formula(j+2,i+4, formulastringBegB1,formatHidden)
ws7.write_formula(j+2,i+5, formulastringBegB2,formatHidden)
ws7.write_formula(j+2,i, formulastringBegB3,bold)
ws7.write_formula(j+5,i, formulastringUZVR,formatDez)
ws7.write_formula(j+6,i, formulastringUZVRbew)

#ToDo: Hier sollten nach Möglichkeit noch eine Karte mit den UZVR und ggf. auch die Klassengrößen eingefügt werden

########
## Tabellenblatt 9: Übersicht Einordnung in Region
## Teil 1 Beschriftungen einfügen
j = 0
i = 0
ws9.write(j, i, 'Uebersicht Einordnung in Region', bold)
j = j + 2
ws9.write(j, i, 'Schutzgebiete und schutzwuerdige Boeden', bold)
j = j + 1
ws9.write(j, i, 'Biotope', normal)
j = j + 1
ws9.write(j, i, 'FFH Gebiete', normal)
j = j + 1
ws9.write(j, i, 'Nationalparke', normal)
j = j + 1
ws9.write(j, i, 'Naturschutzgebiete', normal)
j = j + 1
ws9.write(j, i, 'Vogelschutzgebiete', normal)
j = j + 2
ws9.write(j, i, 'Schutzgebiete', normal)
j = j + 1
ws9.write(j, i, 'Schutzwuerdige Boeden', normal)
j = j + 2
ws9.write(j, i, 'Integration', bold)
j = j + 1
ws9.write(j, i, 'Integrationsgrad', normal)
i = i + 2
ws9.write(j, i, 'grenzen an den Siedlungskoerper', normal)
i = 0
j = j + 1
ws9.write(j, i, 'Bewertung Integration', normal)
i = i + 2
ws9.write(j, i, 'von 5 Punkten', normal)
i = 0
j = j + 2
if flaechentyp == "Wohnen":
    ws9.write(j, i, 'Wohnflaechendichte', bold)
    j = j + 1
    ws9.write(j, i, 'Projektflaeche', normal)
    i = i + 2
    ws9.write(j, i, 'qm Wohnflaeche je Hektar Bauland', normal)
    i = 0
    j = j + 1
    ws9.write(j, i, 'Kreis', normal)
    i = i + 2
    ws9.write(j, i, 'qm Wohnflaeche je Hektar Bauland', normal)
    i = 0
    j = j + 1
    ws9.write(j, i, 'Kreistyp', normal)
    i = i + 2
    ws9.write(j, i, 'qm Wohnflaeche je Hektar Bauland', normal)
    i = 0
    j = j + 1
    ws9.write(j, i, 'Bewertung', normal)
    i = i + 2
    ws9.write(j, i, 'von 5 Punkten', normal)
    i = 0

# Teil 2: Formeln und Werte einladen
j = 3
i = 1
RowColBIO = xl_rowcol_to_cell(OekWertZeile, 2)
RowColFFH = xl_rowcol_to_cell(OekWertZeile, 3)
RowColNP = xl_rowcol_to_cell(OekWertZeile, 4)
RowColNSG = xl_rowcol_to_cell(OekWertZeile, 5)
RowColVSG = xl_rowcol_to_cell(OekWertZeile, 6)
RowColSWB = xl_rowcol_to_cell(OekWertZeile, 12)
RowColIG = xl_rowcol_to_cell(OekWertZeile, 14)
RowColBIG = xl_rowcol_to_cell(OekWertZeile, 15)
if flaechentyp == "Wohnen":
    RowColWDP = xl_rowcol_to_cell(WFDWertZeile, 4)
    RowColWDK = xl_rowcol_to_cell(WFDWertZeile, 5)
    RowColWDT = xl_rowcol_to_cell(WFDWertZeile, 7)
    RowColWDB = xl_rowcol_to_cell(WFDWertZeile, 3)
formulastringBIO = '=IF(Rohdaten!'+RowColBIO+'=1,"Ja","Nein")'
formulastringFFH = '=IF(Rohdaten!'+RowColFFH+'=1,"Ja","Nein")'
formulastringNP = '=IF(Rohdaten!'+RowColNP+'=1,"Ja","Nein")'
formulastringNSG = '=IF(Rohdaten!'+RowColNSG+'=1,"Ja","Nein")'
formulastringVSG = '=IF(Rohdaten!'+RowColVSG+'=1,"Ja","Nein")'
formulastringSG = '=IF(OR(B4="Ja",B5="Ja",B6="Ja",B7="Ja",B8="Ja")=TRUE,"Ja","Nein")'
formulastringSWB = '=IF(Rohdaten!'+RowColSWB+'=1,"Ja","Nein")'
formulastringIG = '=Rohdaten!'+RowColIG+''
formulastringBIG = '=Rohdaten!'+RowColBIG+''
if flaechentyp == "Wohnen":
    formulastringWDP = '=Rohdaten!'+RowColWDP+''
    formulastringWDK = '=Rohdaten!'+RowColWDK+''
    formulastringWDT = '=Rohdaten!'+RowColWDT+''
    formulastringWDB = '=Rohdaten!'+RowColWDB+''
ws9.write_formula(j,i, formulastringBIO,normal)
ws9.write_formula(j+1,i, formulastringFFH,normal)
ws9.write_formula(j+2,i, formulastringNP,normal)
ws9.write_formula(j+3,i, formulastringNSG,normal)
ws9.write_formula(j+4,i, formulastringVSG,normal)
ws9.write_formula(j+6,i, formulastringSG,normal)
ws9.write_formula(j+7,i, formulastringSWB,normal)
ws9.write_formula(j+10,i, formulastringIG,formatProz)
ws9.write_formula(j+11,i, formulastringBIG,normal)
if flaechentyp == "Wohnen":
    ws9.write_formula(j+14,i, formulastringWDP,normal)
    ws9.write_formula(j+15,i, formulastringWDK,normal)
    ws9.write_formula(j+16,i, formulastringWDT,normal)
    ws9.write_formula(j+17,i, formulastringWDB,normal)

######
#Workbook speichern
try:
    wb.close()
except:
    arcpy.AddMessage("Es liegt ein Fehler beim Speichern der Ausgabedatei vor. Ist diese ggf. noch geoeffnet?")


#############################################################################################################
# Endmeldung
print 'Berechnung abgeschlossen'
arcpy.AddMessage('Berechnung abgeschlossen')

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
# Funktionen
#
#############################################################################################################

def getRS(ags_in):
    base_path = str(sys.path[0]).split("2_Tool")[0]
    workspace_basisdaten = os.path.join(base_path,'1_Basisdaten','FGBD_01_Basisdaten_deutschland.gdb')

    VG250 = os.path.join(workspace_basisdaten,'VG250')
    where = '"AGS"'+" ='"+ ags_in + "'"

    rows = arcpy.SearchCursor(VG250, where)

    for row in rows:
        regionalschluessel = row.RS

    if regionalschluessel[2:] == "0000000000":
        regionalschluessel = regionalschluessel[0:2]

    return regionalschluessel

def getRS_VG(ags_in):
    base_path = str(sys.path[0]).split("2_Tool")[0]
    workspace_basisdaten = os.path.join(base_path,'1_Basisdaten','FGBD_01_Basisdaten_deutschland.gdb')

    VG250 = os.path.join(workspace_basisdaten,'VG250')
    where = '"AGS"'+" ='"+ ags_in + "'"

    rows = arcpy.SearchCursor(VG250, where)

    for row in rows:
        regionalschluessel = row.SN_L + row.SN_R + row.SN_K + row.SN_V1 + row.SN_V2

    return regionalschluessel


def getAnteilEKS(ags_input,jahr):
    query = "http://api.regenesis.pudo.org/cube/71231gj001/facts?cut=gemein.name:"+ags_input+"|jahr.text:"+str(jahr)

    queryresult = urllib2.urlopen(query)
    jsonContent = queryresult.read()
    data = json.loads(jsonContent)

    AnteilEKS = int(data[0][u'steu08'])
    time.sleep(0.5)
    return(AnteilEKS)


def getAnzHH(ags_input):
    query = "https://ergebnisse.zensus2011.de/auswertungsdb/download?csv="+ags_input+"&tableId=GWZ_4_1_0&locale=DE"

    queryresult = urllib2.urlopen(query).read()
    time.sleep(1)
    AnzHH = queryresult.split('Insgesamt;')[3].split(";")[0]


    time.sleep(0.5)
    return(AnzHH)

#############################################################################################################
#
# Beginne Hauptteil
#
#############################################################################################################

# Import arcpy modules
import arcpy, os, inspect, pyodbc, shutil, gc, sys, datetime, xlsxwriter, imp, urllib2, json, time
from xlsxwriter.utility import xl_rowcol_to_cell

sheetlibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '11_Definition_Projekt','sheet_lib.py'))
sl = imp.load_source('sheet_lib', sheetlibpath)

mdblibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '11_Definition_Projekt','tempmdb_lib.py'))
mdb = imp.load_source('tempmdb_lib', mdblibpath)

gc.collect()

arcpy.env.overwriteOutput = True

# Variablen definieren
projektname = arcpy.GetParameterAsText(0)
#projektname = "HCU_LKH_Bultweg"

#Pfade einrichten
base_path = str(sys.path[0]).split("2_Tool")[0]

workspace_basisdaten = os.path.join(base_path,'1_Basisdaten','FGBD_01_Basisdaten_deutschland.gdb')
workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
workspace_projekt_bevoelkerung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_22_BevModellierung_'+projektname+'.gdb')
workspace_projekt_einnahmen = os.path.join(base_path,'3_Projekte',projektname,'FGDB_32_Einnahmen_'+projektname+'.gdb')
workspace_tool_bevoelkerung = os.path.join(base_path,"2_Tool","22_Bevoelkerungsmodellierung","FGDB_22_Bevoelkerungsmodellierung_Tool.gdb")
workspace_tool_definition = os.path.join(base_path,"2_Tool","11_Definition_Projekt","FGDB_11_Definition_Projekt_Tool.gdb")
workspace_tool_einnahmen = os.path.join(base_path,"2_Tool","32_Einnahmen","FGDB_32_Einnahmen_Tool.gdb")

Teilflaechen_Plangebiet_Centroide = os.path.join(workspace_projekt_definition, "Teilflaechen_Plangebiet_Centroide")
Teilflaechen_Plangebiet_CentroideGK3 = os.path.join(workspace_projekt_definition, "Teilflaechen_Plangebiet_CentroideGK3")
gemeindenWirkraumEW_Centroide = os.path.join(workspace_projekt_definition,"gemeindenWirkraumEW_Centroide")
gemeindenWirkraumAP_Centroide = os.path.join(workspace_projekt_definition,"gemeindenWirkraumAP_Centroide")

input_table = os.path.join(workspace_projekt_bevoelkerung,'T02RECH_Input')

#############################################################################################################
#
# Durchlauf Auswirkungen im Umland
#
#############################################################################################################
beginmeldung = 'Durchlauf Einkommensteuer \n'
arcpy.AddMessage(beginmeldung)
print beginmeldung

#############################################################################################################
# Schritt 1
schrittmeldung = 'Ermittle kommunalen Anteil an Einkommensteuer und Anzahl Haushalte \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

EKST_01_Basisdaten = os.path.join(workspace_projekt_einnahmen,'EKST_01_Basisdaten')
arcpy.TruncateTable_management(EKST_01_Basisdaten)

umlandtabelle = os.path.join(workspace_projekt_einnahmen, "AWU_WanderungsfaktorEW")

rows = arcpy.SearchCursor(umlandtabelle)
for row in rows:
    ags = row.AGS
    ags_vg = row.AGS_VG
    ags_regenesis = row.AGS_Regenesis

    try:
        i = 0
        try:
            AnteilEKS10 = getAnteilEKS(ags_regenesis, 2010)*1000
            i+=1
        except:
            AnteilEKS10 = 0
        try:
            AnteilEKS11 = getAnteilEKS(ags_regenesis, 2011)*1000
            i+=1
        except:
            AnteilEKS11 = 0
        try:
            AnteilEKS12 = getAnteilEKS(ags_regenesis, 2012)*1000
            i+=1
        except:
            AnteilEKS12 = 0

        AnteilEKS = (AnteilEKS10+AnteilEKS11+AnteilEKS12)/i
        if AnteilEKS == 0:
            AnteilEKS = 2

        try:
            if ags_vg == "":
                AnzHH = getAnzHH(getRS(ags)).replace("(","").replace(")","")

            else:
                AnzHH = getAnzHH(getRS_VG(ags)).replace("(","").replace(")","")
        except:
            AnzHH = str(1)
            message = "Keine Haushalte fuer AGS " + ags + "gefunden. Wert wird auf 1 gesetzt."
            arcpy.AddMessage(message)

        rows_insert = arcpy.InsertCursor(EKST_01_Basisdaten)
        row_in = rows_insert.newRow()
        row_in.AGS = ags
        row_in.KAEST3Jahre = AnteilEKS
        row_in.HH2011 = AnzHH
        rows_insert.insertRow(row_in)

        message = "Daten fuer AGS: "+ags_regenesis+" wurden ermittelt: HH:" + str(AnzHH) +" EKS:"+ str(AnteilEKS)
        arcpy.AddMessage(message)

    except Exception as e:
        message = "Daten fuer AGS: "+ags_regenesis+" koennen nicht ermittelt werden: " + str(e)
        arcpy.AddMessage(message)
        sys.exit()

del row, rows, row_in, rows_insert

arcpy.AddMessage("\n")

#############################################################################################################
# Schritt 1
schrittmeldung = 'Aufsummieren der Einkommensteuer pro Haushalt \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

# Erzeuge EKST_02_ESTproHHRefZiel
eingangstabellen = [
    (workspace_projekt_einnahmen,'EKST_01_Basisdaten'),
    (workspace_projekt_einnahmen,'AWU_WanderungsfaktorEW')
]

ausgabetabelle = (workspace_projekt_einnahmen,'EKST_02_ESTproHHRefZiel')

sql = """SELECT EKST_01_Basisdaten.AGS, ([KAEST3Jahre]/[HH2011])*[AWU_Wanderungsfaktor] AS ESTProHHReferenz INTO EKST_02_ESTproHHRefZiel
FROM EKST_01_Basisdaten INNER JOIN AWU_WanderungsfaktorEW ON EKST_01_Basisdaten.AGS = AWU_WanderungsfaktorEW.AGS;
"""

mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

# Ermittle Summe ueber Tabelle
EKST_02_ESTproHH = os.path.join(workspace_projekt_einnahmen,'EKST_02_ESTproHHRefZiel')

EStProHHReferenzZielort = 0
rows = arcpy.SearchCursor(EKST_02_ESTproHH)
for row in rows:
    EStProHHReferenzZielort = EStProHHReferenzZielort + row.ESTproHHReferenz

# Erzeuge EKST_02_ESTproHHRefHerkunft
eingangstabellen = [
    (workspace_projekt_einnahmen,'EKST_01_Basisdaten')
]

ausgabetabelle = (workspace_projekt_einnahmen,'EKST_02_ESTproHHRefHerkunft')

sql = """SELECT EKST_01_Basisdaten.AGS, [KAEST3Jahre]/[HH2011] AS EStProHHRefHerkunft INTO EKST_02_ESTproHHRefHerkunft
FROM EKST_01_Basisdaten;
"""

mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

#############################################################################################################
# Schritt 1
schrittmeldung = 'Erzeuge Wohneinheitenuebersicht \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

# Ermittle Betrachtungszeitraum
projektrahmendaten = os.path.join(workspace_projekt_definition,'Projektrahmendaten')
rows = arcpy.SearchCursor(projektrahmendaten)
for row in rows:
    beginn = row.Beginn_Betrachtungszeitraum
    ende = row.Ende_Betrachtungszeitraum

del row, rows

EKST_03_WE_NBG = os.path.join(workspace_projekt_einnahmen,'EKST_03_WE_NBG')
arcpy.TruncateTable_management(EKST_03_WE_NBG)

#Iteriere ueber Jahre
gebaeudetypen = os.path.join(workspace_tool_definition,'Gebaeudetyp')
rows = arcpy.SearchCursor(gebaeudetypen)
for row in rows:
    gebaeudetyp = row.Gebaeudetyp

    message = "Berechne fuer: " + gebaeudetyp
    arcpy.AddMessage(message)

    #Iteriere ueber Eigentum / Miete
    miete_eigentum = ["Miete","Eigentum"]
    for e in miete_eigentum:

        Anzahl_WE = 0

        #Iteriere ueber Jahre
        for jahr in range(beginn,ende+1):

            Wohneinheiten_Details = os.path.join(workspace_projekt_definition,'Wohneinheiten_Details')

            where = '"Gebaeudetyp"'+" ='"+ gebaeudetyp + "' AND " + '"Miete_Eigentum"'+" ='"+ e + "' AND " + '"Jahr"'+" =" + str(jahr)

            rows = arcpy.SearchCursor(Wohneinheiten_Details,where)
            for row in rows:
                Anzahl_WE = Anzahl_WE + row.Anzahl_WE

            rows_insert = arcpy.InsertCursor(EKST_03_WE_NBG)
            row_in = rows_insert.newRow()
            row_in.Jahr = jahr
            row_in.Gebaeudetyp = gebaeudetyp
            row_in.Miete_Eigentum = e
            row_in.Anzahl_WE = Anzahl_WE
            rows_insert.insertRow(row_in)

arcpy.AddMessage("\n")


#############################################################################################################
# Schritt 4
schrittmeldung = 'Erzeuge EKST_04_Zuwachs \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

# Erzeuge EKST_04_Zuwachs
eingangstabellen = [
    (workspace_projekt_einnahmen,'EKST_03_WE_NBG'),
    (workspace_tool_einnahmen,'EKST_Korrekturfaktor_NBG')
]

ausgabetabelle = (workspace_projekt_einnahmen,'EKST_04_Zuwachs')

sql = """SELECT 'AAAA' AS AGS, [Jahr]+7 AS Betrachtungsjahr, Sum([Anzahl_WE]*[KorrekturfaktorNBG]*EStProHHReferenzZielort) AS EST_EUR INTO EKST_04_Zuwachs
FROM EKST_03_WE_NBG INNER JOIN EKST_Korrekturfaktor_NBG ON (EKST_03_WE_NBG.Miete_Eigentum = EKST_Korrekturfaktor_NBG.Miete_Eigentum) AND (EKST_03_WE_NBG.Gebaeudetyp = EKST_Korrekturfaktor_NBG.Gebaeudetyp)
GROUP BY 'AAAA', [Jahr]+7
HAVING ((([Jahr]+7)<=EndeBetrachtungszeitraum))
ORDER BY [Jahr]+7, Sum([Anzahl_WE]*[KorrekturfaktorNBG]*EStProHHReferenzZielort);
"""

sql = sql.replace("EStProHHReferenzZielort",str(EStProHHReferenzZielort)).replace("AAAA",ags).replace("EndeBetrachtungszeitraum",str(ende))

mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)


#############################################################################################################
# Schritt 4
schrittmeldung = 'Erzeuge EKST_05_Verlust \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

# Erzeuge EKST_05_Verlust
eingangstabellen = [
    (workspace_projekt_einnahmen,'EKST_03_WE_NBG'),
    (workspace_tool_einnahmen,'EKST_Korrekturfaktor_NBG'),
    (workspace_projekt_einnahmen,'EKST_02_ESTproHHRefHerkunft'),
    (workspace_projekt_einnahmen,'AWU_WanderungsfaktorEW')

]

ausgabetabelle = (workspace_projekt_einnahmen,'EKST_05_Verlust')

sql = """
SELECT [Jahr]+7 AS Betrachtungsjahr, EKST_02_ESTproHHRefHerkunft.AGS, Sum([Anzahl_WE]*[EStProHHRefHerkunft]*[KorrekturfaktorNBG]*[AWU_Wanderungsfaktor]*-1) AS EST_EUR INTO EKST_05_Verlust
FROM EKST_03_WE_NBG INNER JOIN EKST_Korrekturfaktor_NBG ON (EKST_03_WE_NBG.Miete_Eigentum = EKST_Korrekturfaktor_NBG.Miete_Eigentum) AND (EKST_03_WE_NBG.Gebaeudetyp = EKST_Korrekturfaktor_NBG.Gebaeudetyp), EKST_02_ESTproHHRefHerkunft INNER JOIN AWU_WanderungsfaktorEW ON EKST_02_ESTproHHRefHerkunft.AGS = AWU_WanderungsfaktorEW.AGS
GROUP BY [Jahr]+7, EKST_02_ESTproHHRefHerkunft.AGS
HAVING ((([Jahr]+7)<=EndeBetrachtungszeitraum))
ORDER BY [Jahr]+7, EKST_02_ESTproHHRefHerkunft.AGS;
"""

sql = sql.replace("EndeBetrachtungszeitraum",str(ende))
mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

# INSERT EKST_05_Verlust
eingangstabellen = [
    (workspace_projekt_einnahmen,'EKST_04_Zuwachs'),
    (workspace_projekt_einnahmen,'EKST_05_Verlust')

]

ausgabetabelle = (workspace_projekt_einnahmen,'EKST_04_Zuwachs')

sql = """
INSERT INTO EKST_04_Zuwachs ( Betrachtungsjahr, AGS, EST_EUR )
SELECT EKST_05_Verlust.Betrachtungsjahr, EKST_05_Verlust.AGS, EKST_05_Verlust.EST_EUR
FROM EKST_05_Verlust;
"""

mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)


#############################################################################################################
# Schritt 4
schrittmeldung = 'Erzeuge EKST_06_Summen \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

# Erzeuge EKST_04_Zuwachs
eingangstabellen = [
    (workspace_projekt_einnahmen,'EKST_04_Zuwachs')
]

ausgabetabelle = (workspace_projekt_einnahmen,'EKST_06_Bilanz')

sql = """SELECT EKST_04_Zuwachs.AGS, EKST_04_Zuwachs.Betrachtungsjahr, Sum(EKST_04_Zuwachs.EST_EUR) AS Bilanz_EST_EUR INTO EKST_06_Bilanz
FROM EKST_04_Zuwachs
GROUP BY EKST_04_Zuwachs.AGS, EKST_04_Zuwachs.Betrachtungsjahr;
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
excelpfad = os.path.join(ausgabeordner,'32_Einnahmen_Einkommensteuer.xlsx')

try:
    os.remove(excelpfad)
except:
    pass

# Workbook und Tabellenblätter anlegen
wb = xlsxwriter.Workbook(excelpfad)
sl.infosheet(projektname, str("Einkommensteuer").decode('utf-8'), wb)
ws1 = wb.add_worksheet('Methodik')
ws2 = wb.add_worksheet('Auswertungen')
ws3 = wb.add_worksheet('Grafiken')
ws4 = wb.add_worksheet('Rohdaten_Einkommensteuer')
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

ausgabetabelle = os.path.join(workspace_projekt_einnahmen,'EKST_06_Bilanz')

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
ws4.set_column('D:D', 18, money)

################################
#Methodikblatt einfuegen
methodik_grafik = os.path.join(base_path,"2_Tool","32_Einnahmen","Erlaeuterungstexte","Methodik_02_Einkommensteuer.png")
ws1.insert_image('B2', methodik_grafik, {'x_scale': 0.6, 'y_scale': 0.6}) #Korrigiert Verzerrung die bei 1x1 auftritt

################################
#Haftungsausschluss einfuegen
haftung_grafik = os.path.join(base_path,"2_Tool","32_Einnahmen","Erlaeuterungstexte","Haftungsausschluss.png")
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
    JahrListe.append(row.getValue("Betrachtungsjahr"))

AGSListe = sorted(set(AGSListe))
JahrListe = sorted(set(JahrListe))



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
        formula = "=SUMIFS(Rohdaten_Einkommensteuer!$D:$D,Rohdaten_Einkommensteuer!$B:$B,Auswertungen!B"+str(i+5)+",Rohdaten_Einkommensteuer!$C:$C,Auswertungen!"+alphabet[f+2]+"4)"
        ws2.write_formula(i+4, f+2, formula, money)
        i+=1
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
chart.set_title({'name': 'Einkommensteuer in Euro','name_font':  {'name': 'Tahoma', 'size': 9}})


i=0

for ags in AGSListe:

    i+=1

    chart.add_series({
            'name': ['Auswertungen', 3+i, 1, 3+i, 1],
            'categories': ['Auswertungen', 3, 2, 3, len(JahrListe)],
            'values':     ['Auswertungen', 3+i, 2, 3+i, len(JahrListe)], # Format: Zeile, Spalte Anfang, Zeile , Spalte Ende
        })

ws3.insert_chart('B2', chart)

################################
#Workbook speichern
try:
    wb.close()
except:
    print "Es liegt ein Fehler beim Speichern der Ausgabedatei vor. Ist diese ggf. noch geoeffnet?"
    arcpy.AddMessage("Es liegt ein Fehler beim Speichern der Ausgabedatei vor. Ist diese ggf. noch geoeffnet?")

#############################################################################################################


#############################################################################################################
# Schritt 4
schrittmeldung = 'temporaere Tabellen loeschen \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

deleteList = []

for e in deleteList:
    f = os.path.join(workspace_projekt_definition,e)
    try:
        arcpy.Delete_management(f)
    except:
        pass

gc.collect()
print "fertig"
arcpy.AddMessage('02_Einkommensteuer abgeschlossen')
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 02_Zentrale_Orte_OEPNV_Abfrage.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# HCU Hamburg
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


#############################################################################################################
# Import arcpy modules
import os
import sys
import urllib
import re
import datetime
import imp
import csv

import arcpy
from os.path import join


def main(parameters, messages):
    arcpy.env.overwriteOutput = True

    projektname = str(parameters[0].valueAsText)
    orte = []
    p1 = parameters[1].valueAsText
    if p1 is not None and p1 != "":
        orte.append(p1.replace('(','').replace('-','').replace(')','').encode('utf-8'))
    p2 = parameters[2].valueAsText
    if p2 is not None and p2 != "":
        orte.append(p2.replace('(','').replace('-','').replace(')','').encode('utf-8'))
    p3 = parameters[3].valueAsText
    if p3 is not None and p3 != "":
        orte.append(p3.replace('(','').replace('-','').replace(')','').encode('utf-8'))

    #Pfade einrichten
    base_path = str(sys.path[0]).split("2_Tool")[0]

    workspace_projekt_erreichbarkeit = join(base_path,'3_Projekte',projektname,'FGDB_Erreichbarkeit.gdb')
    zentrale_orte = workspace_projekt_erreichbarkeit+"\Zentrale_Orte_75km"

    #############################################################################################################
    # Schritt 1 - Formatierungen für das Bahn-Routing

    def _callback(matches):
        id = matches.group(1)
        try:
            return unichr(int(id))
        except:
            return id

    def decode_unicode_references(data):
        return re.sub("&#(\d+)(;|(?=\s))", _callback, data)

    codes = {
    " " : "%20",
    "!" : "%21",
    "\"" : "%22",
    "#" : "%23",
    "$" : "%24",
    "%" : "%25",
    "&" : "%26",
    "'" : "%27",
    "(" : "%28",
    ")" : "%29",
    "*" : "%2A",
    "+" : "%2B",
    "," : "%2C",
    "-" : "%2D",
    "." : "%2E",
    "/" : "%2F",
    ":" : "%3A",
    ";" : "%3B",
    "<" : "%3C",
    "=" : "%3D",
    ">" : "%3E",
    "?" : "%3F",
    "@" : "%40",
    "[" : "%5B",
    "\\" : "%5C",
    "]" : "%5D",
    "^" : "%5E",
    "_" : "%5F",
    "`" : "%60",
    "{" : "%7B",
    "|" : "%7C",
    "}" : "%7D",
    "~" : "%7E",
    " " : "%7F",
    "€" : "%80",
    " " : "%81",
    "‚" : "%82",
    "ƒ" : "%83",
    "„" : "%84",
    "…" : "%85",
    "†" : "%86",
    "‡" : "%87",
    "ˆ" : "%88",
    "‰" : "%89",
    "Š" : "%8A",
    "‹" : "%8B",
    "Œ" : "%8C",
    " " : "%8D",
    "Ž" : "%8E",
    " " : "%8F",
    " " : "%90",
    "‘" : "%91",
    "’" : "%92",
    "“" : "%93",
    "”" : "%94",
    "•" : "%95",
    "–" : "%96",
    "—" : "%97",
    "˜" : "%98",
    "™" : "%99",
    "š" : "%9A",
    "›" : "%9B",
    "œ" : "%9C",
    " " : "%9D",
    "ž" : "%9E",
    "Ÿ" : "%9F",
    " " : "%A0",
    "¡" : "%A1",
    "¢" : "%A2",
    "£" : "%A3",
    " " : "%A4",
    "¥" : "%A5",
    "|" : "%A6",
    "§" : "%A7",
    "¨" : "%A8",
    "©" : "%A9",
    "ª" : "%AA",
    "«" : "%AB",
    "¬" : "%AC",
    "¯" : "%AD",
    "®" : "%AE",
    "¯" : "%AF",
    "°" : "%B0",
    "±" : "%B1",
    "²" : "%B2",
    "³" : "%B3",
    "´" : "%B4",
    "µ" : "%B5",
    "¶" : "%B6",
    "·" : "%B7",
    "¸" : "%B8",
    "¹" : "%B9",
    "º" : "%BA",
    "»" : "%BB",
    "¼" : "%BC",
    "½" : "%BD",
    "¾" : "%BE",
    "¿" : "%BF",
    "À" : "%C0",
    "Á" : "%C1",
    "Â" : "%C2",
    "Ã" : "%C3",
    "Ä" : "%C4",
    "Å" : "%C5",
    "Æ" : "%C6",
    "Ç" : "%C7",
    "È" : "%C8",
    "É" : "%C9",
    "Ê" : "%CA",
    "Ë" : "%CB",
    "Ì" : "%CC",
    "Í" : "%CD",
    "Î" : "%CE",
    "Ï" : "%CF",
    "Ð" : "%D0",
    "Ñ" : "%D1",
    "Ò" : "%D2",
    "Ó" : "%D3",
    "Ô" : "%D4",
    "Õ" : "%D5",
    "Ö" : "%D6",
    " " : "%20", #%D7
    "Ø" : "%D8",
    "Ù" : "%D9",
    "Ú" : "%DA",
    "Û" : "%DB",
    "Ü" : "%DC",
    "Ý" : "%DD",
    "Þ" : "%DE",
    "ß" : "%DF",
    "à" : "%E0",
    "á" : "%E1",
    "â" : "%E2",
    "ã" : "%E3",
    "ä" : "%E4",
    "å" : "%E5",
    "æ" : "%E6",
    "ç" : "%E7",
    "è" : "%E8",
    "é" : "%E9",
    "ê" : "%EA",
    "ë" : "%EB",
    "ì" : "%EC",
    "í" : "%ED",
    "î" : "%EE",
    "ï" : "%EF",
    "ð" : "%F0",
    "ñ" : "%F1",
    "ò" : "%F2",
    "ó" : "%F3",
    "ô" : "%F4",
    "õ" : "%F5",
    "ö" : "%F6",
    "÷" : "%F7",
    "ø" : "%F8",
    "ù" : "%F9",
    "ú" : "%FA",
    "û" : "%FB",
    "ü" : "%FC",
    "ý" : "%FD",
    "þ" : "%FE",
    "ÿ" : "%FF"
    }

    def urlencode(text):
        text = text.replace("%", codes["%"])
        for code in codes:
            if code in text and code != "%":
                text = text.replace(code, codes[code])
        return text

    #############################################################################################################
    # Schritt 2 - Nächstgelegene Haltestelle identifizieren

    mittelpunkt = workspace_projekt_erreichbarkeit+"\Mittelpunkt_RPC_Gebiet"
    desc = arcpy.Describe(mittelpunkt)
    rows = arcpy.SearchCursor(mittelpunkt, "", "Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj","","")
    for row in rows:
        feat = row.getValue(desc.ShapeFieldName)
        pnt = feat.getPart()
    del rows, row

    # X und Y umformatieren für URL-Query
    x_start = ("%.6f" % pnt.X).replace('.','')
    y_start = ("%.6f" % pnt.Y).replace('.','')

    #str1 = '<div class="trow">'
    f=urllib.urlopen("http://mobile.bahn.de/bin/mobil/query.exe/dox?ld=9627&n=1&rt=1&use_realtime_filter=1&performLocating=2&tpl=stopsnear&look_maxdist=2000&look_stopclass=1023&look_x="+x_start+"&look_y="+y_start)
    ##print ("http://mobile.bahn.de/bin/mobil/query.exe/dox?ld=9627&n=1&rt=1&use_realtime_filter=1&performLocating=2&tpl=stopsnear&look_maxdist=2000&look_stopclass=1023&look_x="+x_start+"&look_y="+y_start)
    found = 0
    for zeilen in f:
        if found == 0:
            try:
                zeilen = decode_unicode_references(zeilen).encode('latin-1')
                starthaltestelle = zeilen.split('!">')[1].split('</a>')[0]
                print starthaltestelle
                found = 1
            except:
                pass
    del f

    if starthaltestelle.find(",")!=-1:
        bahn_start = str(urlencode(starthaltestelle.split(',')[0]))+urlencode(",")+"+"+str(urlencode(starthaltestelle.split(',')[1].strip()))
    else:
        bahn_start = str(urlencode(starthaltestelle))+urlencode(",")+"+"+str(urlencode(starthaltestelle.strip()))

    schrittmeldung = 'Naechstgelegene Haltestelle identifiziert  \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung


    #############################################################################################################
    # Schritt 3 - Routing-Abfrage

    # Automatische Ermittlung des Datums für den nächsten Montag (Feiertage werden NICHT berücksichtigt!)
    today = datetime.date.today()
    nextmonday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
    bahn_wochentag=str('Mo'+urlencode(",")+"+"+str(nextmonday.day)+"."+str(nextmonday.month)+"."+str(nextmonday.year))

    # Uhrzeit-Format um zwischen 7.00 und 18.00 stündlich zu routen
    bahn_uhrzeit = []
    for i in range(7,19):
        bahn_uhrzeit.append(str(i)+"%3A00")


    # Listen erstellen in die pro Ziel die jeweils minimalen Fahrtzeit + weitere Angaben geschrieben werden
    dauer_min = []
    verkehrsmittel_min = []
    abfahrt_min = []
    umsteigen_min = []

    def routing(ziel):
        try:
            # Check ob Ziel eindeutig. Wenn nicht --> erstes Suchergebnis aus drop-down Menü als Zielhalt übernehmen
            ##f=urllib.urlopen("http://reiseauskunft.bahn.de/bin/query.exe/dn?revia=yes&existOptimizePrice=1&country=DEU&dbkanal_007=L01_S01_D001_KIN0001_qf-bahn_LZ003&ignoreTypeCheck=yes&S="+bahn_start+"&REQ0JourneyStopsSID=A%3D1%40O%3D"+bahn_start+"%40X%3D10252485%40Y%3D53520371%40U%3D80%40L%3D000694208%40B%3D1%40p%3D1367864842%40&REQ0JourneyStopsS0A=7&Z="+ziel+"&REQ0JourneyStopsZID=&REQ0JourneyStopsZ0A=7&trip-type=single&date="+bahn_wochentag+"&time="+bahn_uhrzeit[0]+"&timesel=depart&returnTimesel=depart&optimize=0&start=1&qf.bahn.button.suchen=")
            f=urllib.urlopen("http://reiseauskunft.bahn.de/bin/query.exe/dn?S="+bahn_start+"&Z="+ziel+"%20Hbf&date="+bahn_wochentag+"&time="+bahn_uhrzeit[0]+"&start=1")
    ##        print ("http://reiseauskunft.bahn.de/bin/query.exe/dn?S="+bahn_start+"&Z="+ziel+"%20Hbf&date="+bahn_wochentag+"&time="+bahn_uhrzeit[0]+"&start=1")
    ##        messages.AddMessage("http://reiseauskunft.bahn.de/bin/query.exe/dn?S="+bahn_start+"&Z="+ziel+"%20Hbf&date="+bahn_wochentag+"&time="+bahn_uhrzeit[0]+"&start=1")
            for zeilen in f:
                    try:
                        fahrtziel = decode_unicode_references(zeilen)
                        fahrtziel = fahrtziel.split('<option value="S-6N1">')[1].split('</option>')[0]
                        ziel = fahrtziel
                        print str(fahrtziel)+' Fuer die URL-Query geaendert in '+str(ziel)
                    except:
                        pass

            # Eine query für jede Stunde
            dauer_list=[]
            abfahrt_list=[]
            umsteigen_list=[]
            verkehrsmittel_list=[]
            for i in bahn_uhrzeit:

                #f=urllib.urlopen("http://reiseauskunft.bahn.de/bin/query.exe/dn?revia=yes&existOptimizePrice=1&country=DEU&dbkanal_007=L01_S01_D001_KIN0001_qf-bahn_LZ003&ignoreTypeCheck=yes&S="+bahn_start+"&REQ0JourneyStopsSID=A%3D1%40O%3D"+bahn_start+"%40X%3D10252485%40Y%3D53520371%40U%3D80%40L%3D000694208%40B%3D1%40p%3D1367864842%40&REQ0JourneyStopsS0A=7&Z="+ziel+"&REQ0JourneyStopsZID=&REQ0JourneyStopsZ0A=7&trip-type=single&date="+bahn_wochentag+"&time="+i+"&timesel=depart&returnTimesel=depart&optimize=0&start=1&qf.bahn.button.suchen=")
                f=urllib.urlopen("http://reiseauskunft.bahn.de/bin/query.exe/dn?S="+bahn_start+"&Z="+ziel+"%20Hbf&date="+bahn_wochentag+"&time="+i+"&start=1")
                print "http://reiseauskunft.bahn.de/bin/query.exe/dn?S="+bahn_start+"&Z="+ziel+"%20Hbf&date="+bahn_wochentag+"&time="+i+"&start=1"

                str1='<td class="duration lastrow" rowspan="2">'
                str2='<div class="resultDep">'
                str3='<td class="changes lastrow" rowspan="2">'
                str4='<td class="products lastrow" rowspan="2">'

                abfahrt=""
                dauer=""
                umsteigen=""
                verkehrsmittel=""

                uu=0
                ii=0
                aa=0

                # HTML-Schnipsel identifizieren
                for zeilen in f:
                    if uu==1:
                        abfahrt=decode_unicode_references(zeilen.replace('\n',''))
                        abfahrt_list.append(abfahrt)
                        uu=0
                    if zeilen.find(str2)==0:
                        uu=1

                    if ii==1:
                        dauer=decode_unicode_references(zeilen.replace('\n',''))
                        dauer_minutes = sum(int(x) * 60 ** i for i,x in enumerate(reversed(dauer.split(":"))))
                        dauer_list.append(dauer_minutes)
                        ii=0
                    if zeilen.find(str1)==0:
                        ii=1

                    if aa==1:
                        verkehrsmittel=decode_unicode_references(zeilen.replace('\n',''))
                        verkehrsmittel_list.append(verkehrsmittel)
                        aa=0
                    if zeilen.find(str4)==0:
                        aa=1

                    if zeilen.find(str3)==0:
                        umsteigen = str(re.findall(r">[0-9]<",zeilen)).replace("'",'').replace(">",'').replace("<",'').replace("[",'').replace("]",'')
                        umsteigen_list.append(umsteigen)
                f.close()
                del abfahrt, dauer, verkehrsmittel, umsteigen

            # Herausfinden, welche der abgefragten Verbindungen die schnellste ist. Wert übergeben
            dauer_min_local = min(dauer_list)
            i=0
            matchcount = 0 # mehrere gleich schnelle Verbindungen --> ersten Eintrag weiter verwenden
            for dauer in dauer_list:
                if dauer_min_local == dauer and matchcount <1:
                    matchcount+=1
                    dauer_min.append(dauer_list[i])
                    verkehrsmittel_min.append(verkehrsmittel_list[i])
                    abfahrt_min.append(abfahrt_list[i])
                    umsteigen_min.append(umsteigen_list[i])
                i+=1
            del dauer_list, verkehrsmittel_list, abfahrt_list, umsteigen_list, dauer_min_local, dauer_minutes
        except:
            dauer_min.append("")
            verkehrsmittel_min.append("Fahrtzeit konnte nicht ermittelt werden")
            abfahrt_min.append(starthaltestelle.decode('latin-1'))
            umsteigen_min.append("")

    i=0
    for ort in orte:
        routing(ort)
        print abfahrt_min[i], ort, dauer_min[i], umsteigen_min[i], verkehrsmittel_min[i]
        i+=1

    schrittmeldung = 'Schnellste OEPNV-Verbindungen abgefragt \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung

    #############################################################################################################
    # Schritt 4 - Datenexport in temporäre .csv zur späteren Abholung durch den Ergebnissammler
    ausgabeordner = join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Abbildungen')
    with open(join(ausgabeordner,"Zentrale_Orte_temp.csv"), 'wb') as csvfile:
        writer = csv.writer(csvfile)
        i = 0
        for ort in orte:
            writer.writerow([abfahrt_min[i].encode('latin1'), ort, dauer_min[i], umsteigen_min[i],verkehrsmittel_min[i]])
            i+=1
        del writer, csvfile

    # Endmeldung
    print 'Berechnung abgeschlossen \n'
    messages.AddMessage('Berechnung abgeschlossen')
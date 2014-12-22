# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Author:      Basti
# Copyright:   (c) Basti 2014
# Fehlt verhalten bei Disconuter
#-------------------------------------------------------------------------------

import urllib
import re,gc,os
import arcpy
import xml.dom.minidom as minidom
import unicodedata
import time
gc.collect()

def _callback(matches):
    id = matches.group(1)
    try:
        return unichr(int(id))
    except:
        return id

def decode_unicode_references(data):
    return re.sub("&#(\d+)(;|(?=\s))", _callback, data)


def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if unicodedata.category(c) != 'Mn')

def _knoten_auslesen(knoten):
    return eval("('%s')" % (knoten.firstChild.data.strip()))

def gibmirxy(url):


    f=urllib.urlopen(url)
    dom = minidom.parse(f)
    gefunden=0
    for eintrag in dom.firstChild.childNodes:

            if eintrag.nodeName == "results":
                for knoten in eintrag.childNodes:
                    if knoten.nodeName == 'Result':

                         for knotena in knoten.childNodes:
                                if knotena.nodeName == "latitude":
                                    latitude = _knoten_auslesen(knotena)
                                elif knotena.nodeName == "longitude":
                                    longitude = _knoten_auslesen(knotena)
                                elif knotena.nodeName == "quality":
                                    quality = _knoten_auslesen(knotena)
                                    gefunden=1

##                         print url
                         break


    f.close()
    if gefunden==0:
        return 0, 0,0
    return  latitude,longitude,quality


projektname = arcpy.GetParameterAsText(0)
TypdesMarktes = arcpy.GetParameterAsText(1)
AlternativeFuerMarkttyp = arcpy.GetParameterAsText(2)
Discounter = arcpy.GetParameterAsText(3)

Name_desMarktes="Unbenannt"
if Name_desMarktes=="":
    Name_desMarktes="Unbenannt"
VKFL = arcpy.GetParameterAsText(4)
Strasse = arcpy.GetParameterAsText(5)
Hausnummer = arcpy.GetParameterAsText(6)
PLZ = arcpy.GetParameterAsText(7)
Ort = arcpy.GetParameterAsText(8)
try:
    Ortsteil=arcpy.GetParameterAsText(9)
except:
    Ortsteil=" "

try:
    radiobutton=arcpy.GetParameterAsText(10)
except:
    radiobutton=False


if radiobutton=="":
   radiobutton=False
arcpy.AddMessage("Georeferenzierung des Marktes")
##arcpy.AddMessage(projektname+" "+TypdesMarktes+" "+AlternativeFuerMarkttyp+" "+VKFL+" "+Strasse+" "+Hausnummer+" "+PLZ+" "+Ort+" "+radiobutton)
#Pfade einrichten
base_path = str(sys.path[0]).split("2_Tool")[0]

workspace_projekt = os.path.join(base_path, '3_Projekte', projektname,
                                 'FGDB_34_Wertveraenderungen_' + projektname + '.gdb')


arcpy.env.workspace=workspace_projekt
arcpy.env.overwriteOutput = True


##Strasse="Bremer Strasse"
##Hausnummer="36"
##Ort= "Tostedt"
##Ortsteil=""
##PLZ="21255"



Strasse=str(decode_unicode_references(Strasse).encode('utf-8'))
Strasse=Strasse.replace('ü','ue')
Strasse=Strasse.replace('ä','ae')
Strasse=Strasse.replace('ö','oe')
Strasse=Strasse.replace('ß','ss')
Strasse=Strasse.replace('é','e')
Strasse=Strasse.replace('Ü','Ue')
Strasse=Strasse.replace('Ä','Ae')
Strasse=Strasse.replace('Ö','Oe')

house=Hausnummer
postcode=PLZ

state=Ortsteil


state=str(decode_unicode_references(state).encode('utf-8'))
state=state.replace('ü','ue')
state=state.replace('ä','ae')
state=state.replace('ö','oe')
state=state.replace('Ü','Ue')
state=state.replace('Ö','Oe')
state=state.replace('Ä','Ae')
state=state.replace('ß','ss')


Ort=str(decode_unicode_references(Ort).encode('iso-8859-1'))
Ort=Ort.replace('ü','ue')
Ort=Ort.replace('ä','ae')
Ort=Ort.replace('ö','oe')
Ort=Ort.replace('Ü','Ue')
Ort=Ort.replace('Ö','Oe')
Ort=Ort.replace('Ä','Ae')
Ort=Ort.replace('ß','ss')

arcpy.AddMessage(Strasse)
arcpy.AddMessage(Ort)


url ='http://query.yahooapis.com/v1/public/yql?q=select * from geo.placefinder where house="'+house+'" and street="'+Strasse+'" and city="'+Ort+'"and country="Germany" and postal="'+str(postcode)+'"&appid=hxByDcDV34HxMu78xKN0b33dXezfkwQskuSVJ9PTUKswLDUaVicYpMWGQScmliWv7IP7SEgQKrlvWC7v1jbcU8gZJU62HTk'
##arcpy.AddMessage( url)
[lat,longi,a]=gibmirxy(url)
##print lat,longi,a
if lat==0 and longi==0 and a==0:
    arcpy.AddMessage("\n\n\n\nWARNUNG: ")
    arcpy.AddMessage("Georeferenzierung derzeit nicht moeglich")
    arcpy.AddMessage("Bitte versuchen sie es spaeter erneut")

    exit(1)

##arcpy.AddMessage( str(lat)+" "+ str(longi)+ " "+a)
if int(a)<85:

    Ort = Ort.split('-')[0]
    arcpy.AddMessage( "Georeferenzierung unter 85 % Qualitaet - erneute Abfrage mit anderen Variablen")

    url ='http://query.yahooapis.com/v1/public/yql?q=select * from geo.placefinder where house="'+house+'" and street="'+Strasse+'" and city="'+(Ort)+'"and state="'+state+'" and country="Germany" and postal="'+str(postcode)+'"&appid=hxByDcDV34HxMu78xKN0b33dXezfkwQskuSVJ9PTUKswLDUaVicYpMWGQScmliWv7IP7SEgQKrlvWC7v1jbcU8gZJU62HTk'
##                        arcpy.AddMessage( url)
##    print url
    [lat,longi,a]=gibmirxy(url)

if int(a)<85:

    Ort = state
    arcpy.AddMessage( "Georeferenzierung unter 85 % Qualitaet - erneute Abfrage mit anderen Variablen Typ 2 \n")

    url ='http://query.yahooapis.com/v1/public/yql?q=select * from geo.placefinder where house="'+house+'" and street="'+Strasse+'" and city="'+(Ort)+'" and country="Germany" and postal="'+str(postcode)+'"&appid=hxByDcDV34HxMu78xKN0b33dXezfkwQskuSVJ9PTUKswLDUaVicYpMWGQScmliWv7IP7SEgQKrlvWC7v1jbcU8gZJU62HTk'
    arcpy.AddMessage( url)
##    print url
    [lat,longi,a]=gibmirxy(url)

if int(a)<85:
    arcpy.AddMessage( "\n\nNoch immer unter 85 % Quali bitte Lat und Lon Koordinaten WGS84 angeben, um Qualitaet zu verbessern")
    arcpy.AddMessage( "\n\n\nABBRUCH DES VORGANGS\n\n\n")
    exit(1)

if lat==0 and longi==0 and a==0:
    arcpy.AddMessage( url)
    arcpy.AddMessage("\n\n\n\nWARNUNG: ")
    arcpy.AddMessage("Georeferenzierung derzeit nicht moeglich - Georeferenzierungswebsite down bzw. mit Verbindungsproblemen.")
    arcpy.AddMessage("Bitte versuchen sie es spaeter erneut.\n")

    exit(1)
arcpy.AddMessage("Georeferenziert")
if radiobutton==False:
    arcpy.AddMessage("keinen weiteren Markt festgelegt.")
    try:
        arcpy.DeleteRows_management(workspace_projekt+"\Neuer_Markt_temp")
##        arcpy.AddMessage("Neuer Markttabelle geleert")

    except:
        pass

    cur_NeuerMarkt= arcpy.InsertCursor(workspace_projekt+"\Neuer_Markt_temp")

    zeile=cur_NeuerMarkt.newRow()
    pnt = arcpy.CreateObject("Point")

##    arcpy.AddMessage(str(lat) + " "+ str(longi))

    pnt.X=float(longi)
    pnt.Y=float(lat)

##    arcpy.AddMessage(str(pnt.X) + " "+ str(pnt.Y))
    zeile.setValue("Id",600)
    zeile.setValue("Betriebstyp",str(TypdesMarktes))
    zeile.setValue("Name_postalisch",str(Name_desMarktes))
    zeile.setValue("PLZ",int(PLZ))
    zeile.setValue("Ortsteil",str(Ortsteil))
    zeile.setValue("Ort",str(Ort))
    zeile.setValue("Strasse",str(Strasse))
    zeile.setValue("HNR",str(Hausnummer))
    zeile.setValue("VKFL_Gesamt",int(VKFL))
    zeile.setValue("Lat",float(lat))
    zeile.setValue("Lon",float(longi))
    zeile.setValue("Qualitaet",int(a))
    zeile.shape = pnt
    cur_NeuerMarkt.insertRow(zeile)

    del cur_NeuerMarkt

else:
    arcpy.AddMessage("Ersten eingegebenen Markt georeferenzieren.")
    cur_NeuerMarkt= arcpy.InsertCursor(workspace_projekt+"\Neuer_Markt_temp")

    zeile=cur_NeuerMarkt.newRow()
    pnt = arcpy.CreateObject("Point")

##    arcpy.AddMessage(str(lat) + " "+ str(longi))

    pnt.X=float(longi)
    pnt.Y=float(lat)

##    arcpy.AddMessage(str(pnt.X) + " "+ str(pnt.Y))
    zeile.setValue("Id",601)
    zeile.setValue("Betriebstyp",str(TypdesMarktes))
    zeile.setValue("Name_postalisch",str(Name_desMarktes))
    zeile.setValue("PLZ",int(PLZ))
    zeile.setValue("Ortsteil",str(Ortsteil))
    zeile.setValue("Ort",str(Ort))
    zeile.setValue("Strasse",str(Strasse))
    zeile.setValue("HNR",str(Hausnummer))
    zeile.setValue("VKFL_Gesamt",int(VKFL))
    zeile.setValue("Lat",float(lat))
    zeile.setValue("Lon",float(longi))
    zeile.setValue("Qualitaet",int(a))
    zeile.shape = pnt
    cur_NeuerMarkt.insertRow(zeile)

    del cur_NeuerMarkt

    cur_Update_Neuer= arcpy.UpdateCursor(workspace_projekt+"\Neuer_Markt_temp")

    for row in cur_Update_Neuer:

        Strasse=str(decode_unicode_references(row.Strasse).encode('utf-8'))
        Strasse=Strasse.replace('ü','ue')
        Strasse=Strasse.replace('ä','ae')
        Strasse=Strasse.replace('ö','oe')
        Strasse=Strasse.replace('ß','ss')
        Strasse=Strasse.replace('é','e')

        house=str(row.HNR)
        postcode=str(row.PLZ)

        state=str(row.Ortsteil)


        state=str(decode_unicode_references(state).encode('utf-8'))
        state=state.replace('ü','ue')
        state=state.replace('ä','ae')
        state=state.replace('ö','oe')
        state=state.replace('Ü','Ue')
        state=state.replace('Ö','Oe')
        state=state.replace('Ä','Ae')
        state=state.replace('ß','ss')


        Ort=str(decode_unicode_references(row.Ort).encode('utf-8'))
        Ort=Ort.replace('ü','ue')
        Ort=Ort.replace('ä','ae')
        Ort=Ort.replace('ö','oe')
        Ort=Ort.replace('Ü','Ue')
        Ort=Ort.replace('Ö','Oe')
        Ort=Ort.replace('Ä','Ae')
        Ort=Ort.replace('ß','ss')


        url ='http://query.yahooapis.com/v1/public/yql?q=select * from geo.placefinder where house="'+house+'" and street="'+Strasse+'" and city="'+str(Ort)+'"and country="Germany" and postal="'+str(postcode)+'"&appid=hxByDcDV34HxMu78xKN0b33dXezfkwQskuSVJ9PTUKswLDUaVicYpMWGQScmliWv7IP7SEgQKrlvWC7v1jbcU8gZJU62HTk'
        ##arcpy.AddMessage( url)
        [lat,longi,a]=gibmirxy(url)
        ##print lat,longi,a
        if lat==0 and longi==0 and a==0:
            arcpy.AddMessage("\n\n\n\nWARNUNG: ")
            arcpy.AddMessage("Georeferenzierung derzeit nicht moeglich")
            arcpy.AddMessage("Bitte versuchen sie es spaeter erneut")

            exit(1)

        ##arcpy.AddMessage( str(lat)+" "+ str(longi)+ " "+a)
        if int(a)<85:

            Ort = Ort.split('-')[0]
            arcpy.AddMessage( "Georeferenzierung unter 85 % Qualitaet - erneute Abfrage mit anderen Variablen")

            url ='http://query.yahooapis.com/v1/public/yql?q=select * from geo.placefinder where house="'+house+'" and street="'+Strasse+'" and city="'+str(Ort)+'"and state="'+state+'" and country="Germany" and postal="'+str(postcode)+'"&appid=hxByDcDV34HxMu78xKN0b33dXezfkwQskuSVJ9PTUKswLDUaVicYpMWGQScmliWv7IP7SEgQKrlvWC7v1jbcU8gZJU62HTk'
        ##                        arcpy.AddMessage( url)
        ##    print url
            [lat,longi,a]=gibmirxy(url)

        if int(a)<85:

            Ort = state
            arcpy.AddMessage( "Georeferenzierung unter 85 % Qualitaet - erneute Abfrage mit anderen Variablen Typ 2 \n")

            url ='http://query.yahooapis.com/v1/public/yql?q=select * from geo.placefinder where house="'+house+'" and street="'+Strasse+'" and city="'+str(Ort)+'" and country="Germany" and postal="'+str(postcode)+'"&appid=hxByDcDV34HxMu78xKN0b33dXezfkwQskuSVJ9PTUKswLDUaVicYpMWGQScmliWv7IP7SEgQKrlvWC7v1jbcU8gZJU62HTk'
            arcpy.AddMessage( url)
        ##    print url
            [lat,longi,a]=gibmirxy(url)

        if int(a)<85:
            arcpy.AddMessage( "\n\nNoch immer unter 85 % Quali bitte Lat und Lon Koordinaten WGS84 angeben, um Qualitaet zu verbessern")
            arcpy.AddMessage( "\n\n\nABBRUCH DES VORGANGS\n\n\n")
            exit(1)

        if lat==0 and longi==0 and a==0:
            arcpy.AddMessage( url)
            arcpy.AddMessage("\n\n\n\nWARNUNG: ")
            arcpy.AddMessage("Georeferenzierung derzeit nicht moeglich - Georeferenzierungswebsite down bzw. mit Verbindungsproblemen.")
            arcpy.AddMessage("Bitte versuchen sie es spaeter erneut.\n")

            exit(1)

        pnt = arcpy.CreateObject("Point")

        arcpy.AddMessage(str(lat) + " "+ str(longi))

        pnt.X=float(longi)
        pnt.Y=float(lat)

        row.Lat=float(lat)
        row.Lon=float(longi)
        row.Qualitaet=int(a)
        row.shape=pnt
        cur_Update_Neuer.updateRow(row)

        break
    del cur_Update_Neuer


input_features = workspace_projekt+"\Neuer_Markt_temp"
output_features_class = workspace_projekt+"\Neuer_Markt"


out_coordinate_system=arcpy.SpatialReference('ETRS 1989 UTM Zone N32')

arcpy.Project_management(input_features, output_features_class, out_coordinate_system)
##arcpy.AddMessage(arcpy.GetMessages())
del input_features,output_features_class,out_coordinate_system
arcpy.AlterAliasName(workspace_projekt+"\Neuer_Markt", 'Neuer_Markt')
##try:
##    if arcpy.Exists("Neuer_Markt_temp"):
##        arcpy.Delete_management("Neuer_Markt_temp")
##except:
##    arcpy.AddMessage("Fehler beim löschen")



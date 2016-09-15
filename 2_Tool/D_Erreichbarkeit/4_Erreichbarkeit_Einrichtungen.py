# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 04_Erreichbarkeit_Einrichtungen.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# HCU Hamburg
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


import gc
import os
import re
import sys
import urllib
import time
import xml.dom.minidom as minidom
import urllib2
import math

import arcpy
import xlrd


#---------------------------------------------------------------------------------------
# Unicode kram
def _callback(matches):
    id = matches.group(1)
    try:
        return unichr(int(id))
    except:
        return id

def decode_unicode_references(data):
    return re.sub("&#(\d+)(;|(?=\s))", _callback, data)


def Koordinaten_derMittelp(workspace_definitionen):
    arcpy.AddMessage("Mittelpunkt des RPC Gebiets erstellen")
    try:
        arcpy.Delete_management(workspace_Erreichbarkeit+ "\Mittelpunkt_RPC_Gebiet")
    except:
        print "Mittelpunkte konnten nicht geloescht werden"

    try:
        arcpy.Delete_management(workspace_Erreichbarkeit+ "\Teilflaechen_Plangebiet")
    except:
        print "Error im Loeschen der Teilflaechen_Plangebiet"

    try:
        arcpy.Delete_management(workspace_Erreichbarkeit+ "\Flaeche_Plangebiet_dissolved")
    except:
        print "Error im Loeschen der Dissolve"

    if int(arcpy.GetCount_management(workspace_definitionen+"\Teilflaechen_Plangebiet").getOutput(0))>1:
        try:
            arcpy.Dissolve_management(workspace_definitionen+"\Teilflaechen_Plangebiet", workspace_Erreichbarkeit+ "\Flaeche_Plangebiet_dissolved")
        #Featur to Point nicht verwendbar weil Info Lizens
    ##    arcpy.FeatureToPoint_management(workspace_Erreichbarkeit+"\Flaeche_Plangebiet_dissolved",workspace_Erreichbarkeit+ "\Mittelpunkt_RPC_Gebiet", "CENTROID")
            fieldName1 = "xCentroid"
            fieldName2 = "yCentroid"
            # Expressions are calculated using the Shape Field's geometry property
            expression1 = "float(!SHAPE.CENTROID!.split()[0].replace(',','.'))"
            expression2 = "float(!SHAPE.CENTROID!.split()[1].replace(',','.'))"

            # Execute AddField
            arcpy.AddField_management(workspace_Erreichbarkeit+ "\Flaeche_Plangebiet_dissolved", fieldName1, "DOUBLE")
            arcpy.AddField_management(workspace_Erreichbarkeit+ "\Flaeche_Plangebiet_dissolved", fieldName2, "DOUBLE")

            # Execute CalculateField
            arcpy.CalculateField_management(workspace_Erreichbarkeit+ "\Flaeche_Plangebiet_dissolved", fieldName1, expression1,"PYTHON")
            arcpy.CalculateField_management(workspace_Erreichbarkeit+ "\Flaeche_Plangebiet_dissolved", fieldName2, expression2,"PYTHON")

            arcpy.CreateFeatureclass_management(workspace_Erreichbarkeit,"Mittelpunkt_RPC_Gebiet","POINT",workspace_Erreichbarkeit+ "\Flaeche_Plangebiet_dissolved","","","Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj")

            for a in arcpy.SearchCursor(workspace_Erreichbarkeit+ "\Flaeche_Plangebiet_dissolved"):

                print float(a.xCentroid),float( a.yCentroid)
                xy=arcpy.Point(a.xCentroid, a.yCentroid)


            # Open an InsertCursor and insert the new geometry
            #
            c = arcpy.InsertCursor(workspace_Erreichbarkeit+ "\Mittelpunkt_RPC_Gebiet", ["SHAPE@XY"])
            newRow = c.newRow()
            newRow.shape = xy
            c.insertRow(newRow)

            # Delete cursor object
            #
            del c,xy,newRow

        except:
            arcpy.AddError("Fehler beim Erstellen des Mittelpunktes")
            exit(1)


    else:
        try:
            arcpy.CopyFeatures_management(workspace_definitionen+"\Teilflaechen_Plangebiet", workspace_Erreichbarkeit+ "\Teilflaechen_Plangebiet")
            fieldName1 = "xCentroid"
            fieldName2 = "yCentroid"
            # Expressions are calculated using the Shape Field's geometry property
            expression1 = "float(!SHAPE.CENTROID!.split()[0].replace(',','.'))"
            expression2 = "float(!SHAPE.CENTROID!.split()[1].replace(',','.'))"

            # Execute AddField
            arcpy.AddField_management(workspace_Erreichbarkeit+ "\Teilflaechen_Plangebiet", fieldName1, "DOUBLE")
            arcpy.AddField_management(workspace_Erreichbarkeit+ "\Teilflaechen_Plangebiet", fieldName2, "DOUBLE")

            # Execute CalculateField
            arcpy.CalculateField_management(workspace_Erreichbarkeit+ "\Teilflaechen_Plangebiet", fieldName1, expression1,"PYTHON")
            arcpy.CalculateField_management(workspace_Erreichbarkeit+ "\Teilflaechen_Plangebiet", fieldName2, expression2,"PYTHON")

            # Creating a spatial reference object
    ##        spatial_reference = arcpy.SpatialReference(os.path.join(workspace_Erreichbarkeit+ "/Teilflaechen_Plangebiet"))
            arcpy.CreateFeatureclass_management(workspace_Erreichbarkeit,"Mittelpunkt_RPC_Gebiet","POINT",workspace_Erreichbarkeit+ "\Teilflaechen_Plangebiet","","","Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj")

            for a in arcpy.SearchCursor(workspace_Erreichbarkeit+ "\Teilflaechen_Plangebiet"):

                print float(a.xCentroid),float( a.yCentroid)
                xy=arcpy.Point(a.xCentroid, a.yCentroid)


            # Open an InsertCursor and insert the new geometry
            #
            c = arcpy.InsertCursor(workspace_Erreichbarkeit+ "\Mittelpunkt_RPC_Gebiet", ["SHAPE@XY"])
            newRow = c.newRow()
            newRow.shape = xy
            c.insertRow(newRow)

            # Delete cursor object
            #
            del c,xy,newRow
        except:
            arcpy.AddError("Fehler beim Erstellen des Mittelpunktes")
            exit(1)


    arcpy.AddXY_management(workspace_Erreichbarkeit+ "\Mittelpunkt_RPC_Gebiet")

    cur_Mittelpunkt = arcpy.SearchCursor(workspace_Erreichbarkeit+"\Mittelpunkt_RPC_Gebiet")
    for eineabfrage in cur_Mittelpunkt:
        Mittelpunkte_x=eineabfrage.getValue("POINT_X")
        Mittelpunkte_y=eineabfrage.getValue("POINT_Y")

    del cur_Mittelpunkt

##    print Mittelpunkte_x,Mittelpunkte_y



    return Mittelpunkte_x,Mittelpunkte_y



def deg2rad(deg) :
  return deg * (math.pi/180)


def getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2):
  R = 6371 #// Radius of the earth in km
  dLat = deg2rad(lat2-lat1)  #// deg2rad below
  dLon = deg2rad(lon2-lon1)
  a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) *  math.sin(dLon/2) * math.sin(dLon/2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  d = R * c #// Distance in km
  return d


def Selektierung_Einrichtungen(lat,lon):

    #zupruefendenEinrichtungen.append([rows.Kategorie,str(decode_unicode_references(rows.Schulname).encode("utf-8")),str(decode_unicode_references(rows.Strasse).encode("utf-8")),rows.PLZ,rows.ORT,rows.Lat,rows.Lon])
    #Muss geändert werden - dynamische Shapefiles
    cur_Einrichtungen_Schulen=arcpy.SearchCursor(workspace_Erreichbarkeit+"/Einrichtungen_Grundschule")
    cur_Einrichtungen_Kita=arcpy.SearchCursor(workspace_Erreichbarkeit+"/Einrichtungen_Kita")
    cur_Einrichtungen_Apotheke=arcpy.SearchCursor(workspace_Erreichbarkeit+"/Einrichtungen_Apotheke")
    cur_Einrichtungen_Arzt=arcpy.SearchCursor(workspace_Erreichbarkeit+"/Einrichtungen_Allgemeinmediziner")
    cur_Einrichtungen_Krankenhaus=arcpy.SearchCursor(workspace_Erreichbarkeit+"/Einrichtungen_Krankenhaeuser")
    cur_Einrichtungen_SM=arcpy.SearchCursor(workspace_Erreichbarkeit+"/Einrichtungen_Einzelhandel")
    cur_Einrichtungen_Sons=arcpy.SearchCursor(workspace_Erreichbarkeit+"/Einrichtungen_Sonstige")


    zupruefendenEinrichtungen=[]

    #Besprechen mit Sascha
    ausschlussdistanz=30

    for rows in cur_Einrichtungen_Schulen:
        if getDistanceFromLatLonInKm(rows.Lat,rows.Lon,lat,lon)<ausschlussdistanz:
            zupruefendenEinrichtungen.append([rows.Kategorie,rows.Name,rows.Strasse,rows.HNR,rows.PLZ,rows.ORT,rows.Lat,rows.Lon])

    for rows in cur_Einrichtungen_Kita:
        if getDistanceFromLatLonInKm(rows.Lat,rows.Lon,lat,lon)<ausschlussdistanz:
            zupruefendenEinrichtungen.append([rows.Kategorie,rows.Name,rows.Strasse,rows.HNR,rows.PLZ,rows.ORT,rows.Lat,rows.Lon])

    for rows in cur_Einrichtungen_Apotheke:
        if getDistanceFromLatLonInKm(rows.Lat,rows.Lon,lat,lon)<ausschlussdistanz:
            zupruefendenEinrichtungen.append([rows.Kategorie,rows.Name,rows.Strasse,rows.HNR,rows.PLZ,rows.ORT,rows.Lat,rows.Lon])

    for rows in cur_Einrichtungen_Arzt:
        if getDistanceFromLatLonInKm(rows.Lat,rows.Lon,lat,lon)<ausschlussdistanz:
            zupruefendenEinrichtungen.append([rows.Kategorie,rows.Name,rows.Strasse,rows.HNR,rows.PLZ,rows.ORT,rows.Lat,rows.Lon])

    for rows in cur_Einrichtungen_SM:
        if getDistanceFromLatLonInKm(rows.Lat,rows.Lon,lat,lon)<ausschlussdistanz:
            zupruefendenEinrichtungen.append([rows.Kategorie,rows.Name,rows.Strasse,rows.HNR,rows.PLZ,rows.ORT,rows.Lat,rows.Lon])

    for rows in cur_Einrichtungen_Krankenhaus:
        if getDistanceFromLatLonInKm(rows.Lat,rows.Lon,lat,lon)<ausschlussdistanz:
            zupruefendenEinrichtungen.append([rows.Kategorie,rows.Name,rows.Strasse,rows.HNR,rows.PLZ,rows.ORT,rows.Lat,rows.Lon])

    for rows in cur_Einrichtungen_Sons:
        if getDistanceFromLatLonInKm(rows.Lat,rows.Lon,lat,lon)<ausschlussdistanz:
            zupruefendenEinrichtungen.append([rows.Kategorie,rows.Name,rows.Strasse,rows.HNR,rows.PLZ,rows.ORT,rows.Lat,rows.Lon])

    return zupruefendenEinrichtungen


def Erreichbarkeit(lat,lon,zupruefendenEinrichtungen):

##    try:
##        arcpy.Delete_management(workspace_Erreichbarkeit+ "\Erreichbarkeit_zuFuss")
##    except:
##        pass
##    try:
##        arcpy.Delete_management(workspace_Erreichbarkeit+ "\Erreichbarkeit_Fahrrad")
##    except:
##        pass
##    try:
##        arcpy.Delete_management(workspace_Erreichbarkeit+ "\Erreichbarkeit_Pkw")
##    except:
##        pass
##    #alte gelöscht

##    #Ergebnistabelle vorbereiten -> rohling vorhanden 30min
##    arcpy.AddField_management(workspace_Erreichbarkeit+"/Einrichtungen30", "Name", "TEXT",250)
##    arcpy.AddField_management(workspace_Erreichbarkeit+"/Einrichtungen30", "Minuten", "TEXT",100)
##    arcpy.AddField_management(workspace_Erreichbarkeit+"/Einrichtungen30", "Km", "FLOAT")
##    arcpy.AddField_management(workspace_Erreichbarkeit+"/Einrichtungen30", "Kategorie", "TEXT",250)
##    arcpy.AddField_management(workspace_Erreichbarkeit+"/Einrichtungen30", "Strasse", "TEXT",250)
##    arcpy.AddField_management(workspace_Erreichbarkeit+"/Einrichtungen30", "HNR", "TEXT",50)
##    arcpy.AddField_management(workspace_Erreichbarkeit+"/Einrichtungen30", "Postleitzahl", "LONG")
##    arcpy.AddField_management(workspace_Erreichbarkeit+"/Einrichtungen30", "Ort", "TEXT",100)
##    arcpy.AddField_management(workspace_Erreichbarkeit+"/Einrichtungen30", "Lat", "FLOAT")
##    arcpy.AddField_management(workspace_Erreichbarkeit+"/Einrichtungen30", "Lon", "FLOAT")
##
##
##    #Cursor auf die Tabelle
##    cur_Einrichtungen30=arcpy.InsertCursor(workspace_Erreichbarkeit+"/Einrichtungen30")

    namendershapes=["zuFuss","Fahrrad","Pkw"]
    #Start ist bestimmt :>

    lat = str(lat)
    lat = lat.replace(',','.')

    lon = str(lon)
    lon = lon.replace(',','.')

    origin = lat+','+lon
    mode="pedestrian","bicycle","fastest"

    for c, typ in enumerate( mode):

        if arcpy.Exists(workspace_Erreichbarkeit+"/Erreichbarkeit_"+namendershapes[c]):
            #leeren der tabelle
            try:
                arcpy.DeleteRows_management(workspace_Erreichbarkeit+"/Erreichbarkeit_"+namendershapes[c])
                arcpy.AddMessage("Erreichbarkeit_"+namendershapes[c] +" -> Alte Inhalte geleert")

            except:
                arcpy.AddError("Alte "+"Erreichbarkeit_"+namendershapes[c]+"konnte nicht geleert werden.")
                arcpy.AddError("Bitte schliessen Sie alle Inhalte und restarten ArcGis erneut und ")
                arcpy.AddError("wiederholen Sie diesen Toolabschnitt.")
                exit(1)

        else:
            #erstelle es
            geometry_type = "POINT"
            template = ""
            has_m = "DISABLED"
            has_z = "DISABLED"
            # Creating a spatial reference object
            desc=arcpy.Describe(workspace_definitionen+"\Teilflaechen_Plangebiet")
            sp=desc.spatialReference
    ##        spatial_reference = arcpy.SpatialReference(os.path.join(workspace_definitionen,"Teilflaechen_Plangebiet"))
            arcpy.CreateFeatureclass_management(workspace_Erreichbarkeit, "Erreichbarkeit_"+namendershapes[c], geometry_type, template, has_m, has_z, sp)

            #Ergebnistabelle vorbereiten -> rohling erstellen
            arcpy.AddField_management(workspace_Erreichbarkeit+"/Erreichbarkeit_"+namendershapes[c], "Name", "TEXT",250)
            arcpy.AddField_management(workspace_Erreichbarkeit+"/Erreichbarkeit_"+namendershapes[c], "Minuten", "TEXT",100)
            arcpy.AddField_management(workspace_Erreichbarkeit+"/Erreichbarkeit_"+namendershapes[c], "Km", "FLOAT")
            arcpy.AddField_management(workspace_Erreichbarkeit+"/Erreichbarkeit_"+namendershapes[c], "Kategorie", "TEXT",250)
            arcpy.AddField_management(workspace_Erreichbarkeit+"/Erreichbarkeit_"+namendershapes[c], "Strasse", "TEXT",250)
            arcpy.AddField_management(workspace_Erreichbarkeit+"/Erreichbarkeit_"+namendershapes[c], "HNR", "TEXT",50)
            arcpy.AddField_management(workspace_Erreichbarkeit+"/Erreichbarkeit_"+namendershapes[c], "Postleitzahl", "LONG")
            arcpy.AddField_management(workspace_Erreichbarkeit+"/Erreichbarkeit_"+namendershapes[c], "Ort", "TEXT",100)
            arcpy.AddField_management(workspace_Erreichbarkeit+"/Erreichbarkeit_"+namendershapes[c], "Lat", "FLOAT")
            arcpy.AddField_management(workspace_Erreichbarkeit+"/Erreichbarkeit_"+namendershapes[c], "Lon", "FLOAT")

        #Cursor auf die Tabelle
        cur_Einrichtungen15=arcpy.InsertCursor(workspace_Erreichbarkeit+"/Erreichbarkeit_"+namendershapes[c])

        arcpy.AddMessage("Ermittlung der Entfernung zur Einrichtung. Verkehrstyp: "+str(namendershapes[c]))

        for einrichtungen in zupruefendenEinrichtungen:
##            mode= "pedestrian"
            ##mode="bicycle ","fastest","pedestrian"
            #System basiert auf http://open.mapquestapi.com/directions/

            lat = einrichtungen[6]
            lat = str(lat)
            lat = lat.replace(',','.')

            lon = einrichtungen[7]
            lon = str(lon)
            lon = lon.replace(',','.')

            destination = lat+','+lon
            time = 0
            distance = 0
            step = 0

            #openmapquest http://open.mapquestapi.com/directions/v1/route?outFormat=xml&from=40.037661,-76.305977&to=39.962532,-76.728099&callback=renderNarrative&routeType=shortest&unit=k

            query = 'http://open.mapquestapi.com/directions/v1/route?outFormat=xml&from='+origin+'&to='+destination+'+&callback=renderNarrative&routeType='+str(typ)+'&unit=k&narrativeType=none&key=Fmjtd%7Cluur2907ng%2Ca0%3Do5-9080l0'
##            print query
##            arcpy.AddMessage(query)

            xml = urllib2.urlopen(query)
            #arcpy.AddMessage(query)
            #print query

            e = xml.read()
            error = int( str(e).split('</info>')[0].split('</statusCode>')[0].replace('<?xml version="1.0" encoding="UTF-8"?>\n<response><info><statusCode>',''))
            if error==0:
                    try:
                        e = str(e).split('</boundingBox>')[1]

                        e = str(e).split('<legs>')[0]
                        #arcpy.AddMessage(e)
                        #print e

                        time = e.split('</fuelUsed>')[1].replace('</formattedTime>','').replace('<formattedTime>','')
                        if len(time) >=30:
                            time = '99:99:99'
                        distance = e.split('</distance>')[0].replace('<distance>','')
                        werte =(einrichtungen[1], time, distance.replace('.',','),einrichtungen[6],einrichtungen[7],einrichtungen[0],einrichtungen[2],einrichtungen[4],einrichtungen[5],einrichtungen[3])
        ##            print werte

        ##            arcpy.AddMessage(typ)
        ##            arcpy.AddMessage(werte)

                        if (int(werte[1].split(':')[0])==00 and int(werte[1].split(':')[1])<30 and c==0):
                            #zufuß <=10

##                            arcpy.AddMessage(werte[0])

                            row_Einrichtungen15=cur_Einrichtungen15.newRow()
                            pnt = arcpy.CreateObject("Point")

                            pnt.X=float(werte[4])
                            pnt.Y=float(werte[3])
                            row_Einrichtungen15.setValue("Name",(werte[0]))
                            row_Einrichtungen15.setValue("Minuten",werte[1])
                            row_Einrichtungen15.setValue("Km",werte[2])
                            row_Einrichtungen15.setValue("Lat",werte[3])
                            row_Einrichtungen15.setValue("Lon",werte[4])
                            row_Einrichtungen15.setValue("Kategorie",werte[5])
                            row_Einrichtungen15.setValue("Strasse",(werte[6]))
                            row_Einrichtungen15.setValue("HNR",str(werte[9]))
                            row_Einrichtungen15.setValue("Postleitzahl",werte[7])
                            row_Einrichtungen15.setValue("Ort",werte[8])

                            row_Einrichtungen15.shape = pnt
                            cur_Einrichtungen15.insertRow(row_Einrichtungen15)


                        elif (int(werte[1].split(':')[0])==00 and int(werte[1].split(':')[1])<30 and c==1):
                            #Fahrrad
                            row_Einrichtungen15=cur_Einrichtungen15.newRow()
                            pnt = arcpy.CreateObject("Point")

                            pnt.X=float(werte[4])
                            pnt.Y=float(werte[3])
                            row_Einrichtungen15.setValue("Name",(werte[0]))
                            row_Einrichtungen15.setValue("Minuten",werte[1])
                            row_Einrichtungen15.setValue("Km",werte[2])
                            row_Einrichtungen15.setValue("Lat",werte[3])
                            row_Einrichtungen15.setValue("Lon",werte[4])
                            row_Einrichtungen15.setValue("Kategorie",werte[5])
                            row_Einrichtungen15.setValue("Strasse",(werte[6]))
                            row_Einrichtungen15.setValue("HNR",str(werte[9]))
                            row_Einrichtungen15.setValue("Postleitzahl",werte[7])
                            row_Einrichtungen15.setValue("Ort",werte[8])

                            row_Einrichtungen15.shape = pnt
                            cur_Einrichtungen15.insertRow(row_Einrichtungen15)

                        elif(int(werte[1].split(':')[0])==00 and int(werte[1].split(':')[1])<30 and c==2):
                            #PKW
                            row_Einrichtungen15=cur_Einrichtungen15.newRow()
                            pnt = arcpy.CreateObject("Point")

                            pnt.X=float(werte[4])
                            pnt.Y=float(werte[3])
                            row_Einrichtungen15.setValue("Name",(werte[0]))
                            row_Einrichtungen15.setValue("Minuten",werte[1])
                            row_Einrichtungen15.setValue("Km",werte[2])
                            row_Einrichtungen15.setValue("Lat",werte[3])
                            row_Einrichtungen15.setValue("Lon",werte[4])
                            row_Einrichtungen15.setValue("Kategorie",werte[5])
                            row_Einrichtungen15.setValue("Strasse",(werte[6]))
                            row_Einrichtungen15.setValue("HNR",str(werte[9]))
                            row_Einrichtungen15.setValue("Postleitzahl",werte[7])
                            row_Einrichtungen15.setValue("Ort",werte[8])

                            row_Einrichtungen15.shape = pnt
                            cur_Einrichtungen15.insertRow(row_Einrichtungen15)
                    except:
                            arcpy.AddError("Fehler")
                            arcpy.AddError(query)
                            exit(1)

            else:
##                arcpy.AddMessage("Route nicht ermittelbar -> Skript wird dennoch weiter ausgefuehrt.")
                    pass
            xml.close()

        del cur_Einrichtungen15
        try:
            del row_Einrichtungen15
        except:
            pass



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

def xlsladen_undStandorteerstellen(pfad,Dateinamen):

    arcpy.AddMessage("Kopieren der Excelinhalte in die Feature Class "+Dateinamen.replace('\\','')+".")
##    arcpy.AddMessage(pfad)
    workbook = xlrd.open_workbook(pfad)
    worksheet = workbook.sheet_by_name('Tabelle1')
    num_rows = worksheet.nrows - 1
    num_cells = worksheet.ncols - 1
    curr_row = -1
    Fieldname=[]
    line=[]
    counter=0
    while curr_row < num_rows:

        Name=""
        Strasse=""
        Ort=""
        Ortsteil=""
        Postleitzahl=""
        Hausnummer=""
        Lat=""
        Lon=""


        curr_row += 1
        row = worksheet.row(curr_row)
    ##    print 'Row:', curr_row
        curr_cell = -1
        if curr_row ==0:
##            print "schon fertig"
            try:
                gdb=os.path.join(workspace_Erreichbarkeit,Dateinamen.replace('\\',''))

                cur = arcpy.InsertCursor(gdb)
            except:
                arcpy.AddError("\n\nBitte Schliessen sie ArcMap und starten sie es erneut. Eine der Datein ist geoeffnet und kann nicht durch das Tool bearbeitet werden.")
                arcpy.AddError("Abbruch des Tools.")
                exit(1)
        else:
##            try:

                row = cur.newRow()
                pnt = arcpy.CreateObject("Point")

                counter += 1

##                arcpy.AddMessage("Schreiben der Zeile "+str(counter)+" in die Feature Class. "+Dateinamen.replace('\\',''))
                cur= arcpy.InsertCursor(gdb)


                curr_cell += 1

                try:
                    row.Name=worksheet.cell_value(curr_row, curr_cell)
                    Name=worksheet.cell_value(curr_row, curr_cell)

                except:
                    row.Name="Undefinierter Name"
                    pass

                if Dateinamen=="\Einrichtungen_Sonstige":
                    curr_cell += 1


                    try:
                        row.Kategorie=worksheet.cell_value(curr_row, curr_cell)

                    except:
                        row.Kategorie="Sonstige"
    ##                    arcpy.AddError("Dateneingabe unvollständig - Postleitzahl fehlt")
    ##                    exit(1)
                        pass
                else:
                    row.Kategorie=Dateinamen.replace('\Einrichtungen_','').replace('.xls','')

                curr_cell += 1


                try:
                    row.PLZ=worksheet.cell_value(curr_row, curr_cell)
                    Postleitzahl=worksheet.cell_value(curr_row, curr_cell)
                except:
##                    arcpy.AddError("Dateneingabe unvollständig - Postleitzahl fehlt")
##                    exit(1)
                    pass

                curr_cell += 1

                try:
                    row.Ort=worksheet.cell_value(curr_row, curr_cell)
                    Ort=worksheet.cell_value(curr_row, curr_cell)
                except:
##                    arcpy.AddError("Dateneingabe unvollständig - Ort fehlt")
##                    exit(1)
                    pass

                curr_cell += 1

                try:
                    row.Ortsteil=worksheet.cell_value(curr_row, curr_cell)
                    Ortsteil=worksheet.cell_value(curr_row, curr_cell)
                except:
                    pass

                curr_cell += 1

                try:
                    row.Strasse=worksheet.cell_value(curr_row, curr_cell)
                    Strasse=worksheet.cell_value(curr_row, curr_cell)
                except:
##                    arcpy.AddError("Dateneingabe unvollständig - Strasse fehlt")
##                    exit(1)
                    pass

                curr_cell += 1

                try:

                    row.HNR=str(worksheet.cell_value(curr_row, curr_cell)).replace(' ','').replace('.0','')
                    Hausnummer=worksheet.cell_value(curr_row, curr_cell)
                except:
                    row.HNR=" "
                    pass

                curr_cell += 1

                try:
                    row.Lon=worksheet.cell_value(curr_row, curr_cell)
                    pnt.X=float(worksheet.cell_value(curr_row, curr_cell))
                    Lon=worksheet.cell_value(curr_row, curr_cell)
                except:
                    pass

                curr_cell += 1

                try:
                    row.Lat=worksheet.cell_value(curr_row, curr_cell)
                    pnt.Y=float(worksheet.cell_value(curr_row, curr_cell))
                    Lat=worksheet.cell_value(curr_row, curr_cell)
                except:
                    pass

                curr_cell += 1

                try:
                    row.Qualitaet=worksheet.cell_value(curr_row, curr_cell)
                except:
                    pass

                curr_cell += 1

                try:
                    row.Gemeindeklasse=worksheet.cell_value(curr_row, curr_cell)
                except:
                    pass





                if     (Strasse=="" or   Ort=="" or  Postleitzahl=="" ) and  (Lat=="" or Lon==""):
                    arcpy.AddError("Wichtige Eingabeinformation fehlt !")
                    arcpy.AddError("Ueberpruefen sie Zeile "+ str(counter)+ " in der Datei "+Dateinamen.replace('\\',''))
                    arcpy.AddError("Die Angabe von Strasse, Postleitzahl und Ort ist zwingend erforderlich falls keine Latitude und Longitude Koordinaten vorliegen.")
                    exit(1)

                row.shape = pnt
                cur.insertRow(row)

    del cur,row,gdb,workbook,worksheet
    return counter

def georeferenz(Shapefile_derEinrichtung):
    counter=0
    cur_Standorte_temp=arcpy.UpdateCursor(workspace_Erreichbarkeit+Shapefile_derEinrichtung)

    arcpy.AddMessage("Georeferenzierung der Eintraege in dem Shape "+str(Shapefile_derEinrichtung).replace('\\',''))
    for zeile in cur_Standorte_temp:

##        arcpy.AddMessage(str(zeile.Lat))
        if zeile.Lat ==None or zeile.Lon ==None or zeile.Lat==0 or zeile.Lon==0:
            pnt = arcpy.CreateObject("Point")
            counter+=1
##            arcpy.AddMessage("Georeferenzieren des Feature in Zeile "+str(counter))
            Strasse=str(decode_unicode_references(zeile.Strasse).encode('utf-8'))
            Strasse=Strasse.replace('ü','ue')
            Strasse=Strasse.replace('ä','ae')
            Strasse=Strasse.replace('ö','oe')
            Strasse=Strasse.replace('ß','ss')
            Strasse=Strasse.replace('é','e')

            house=str(zeile.HNR)
            postcode=str(zeile.PLZ)[:5]



            state=str(decode_unicode_references(zeile.Ortsteil).encode('utf-8'))
            state=state.replace('ü','ue')
            state=state.replace('ä','ae')
            state=state.replace('ö','oe')
            state=state.replace('Ü','Ue')
            state=state.replace('Ö','Oe')
            state=state.replace('Ä','Ae')
            state=state.replace('ß','ss')




            Ort=str(decode_unicode_references(zeile.Ort).encode('utf-8'))
            Ort=Ort.replace('ü','ue')
            Ort=Ort.replace('ä','ae')
            Ort=Ort.replace('ö','oe')
            Ort=Ort.replace('Ü','Ue')
            Ort=Ort.replace('Ö','Oe')
            Ort=Ort.replace('Ä','Ae')
            Ort=Ort.replace('ß','ss')

    ##                    arcpy.AddMessage(Strasse+" "+ Ort+ " "+ postcode+ " "+house)
            url ='http://query.yahooapis.com/v1/public/yql?q=select * from geo.placefinder where house="'+house+'" and street="'+Strasse+'" and city="'+str(Ort)+'"and country="Germany" and postal="'+str(postcode)+'"&appid=hxByDcDV34HxMu78xKN0b33dXezfkwQskuSVJ9PTUKswLDUaVicYpMWGQScmliWv7IP7SEgQKrlvWC7v1jbcU8gZJU62HTk'
##            arcpy.AddMessage( url)
            time.sleep(0.3)
            [lat,longi,a]=gibmirxy(url)
            ##print lat,longi,a

            if lat==0 and longi==0 and a==0:
##                arcpy.AddMessage( url)
                arcpy.AddError("\n\n\n\nFEHLER: ")
                arcpy.AddError("Georeferenzierung derzeit nicht moeglich - Georeferenzierungswebsite down bzw. mit Verbindungsproblemen.")
                arcpy.AddError("Bitte versuchen sie es spaeter erneut.\n")

                exit(1)
            if int(a)<85:

                arcpy.AddMessage("Georeferenzieren des Feature in Zeile "+str(counter)+" Name der Einrichtung: "+zeile.Name)
                arcpy.AddMessage( "Georeferenzierung Unter 85 % Georeferenzierungsqualitaet - erneute Abfrage mit anderen Variablen")

                url ='http://query.yahooapis.com/v1/public/yql?q=select * from geo.placefinder where house="'+house+'" and street="'+Strasse+'"and state="'+str(state)+'"  and country="Germany" and postal="'+str(postcode)+'"&appid=hxByDcDV34HxMu78xKN0b33dXezfkwQskuSVJ9PTUKswLDUaVicYpMWGQScmliWv7IP7SEgQKrlvWC7v1jbcU8gZJU62HTk'
    ##                        arcpy.AddMessage( url)
            ##    print url
                [lat,longi,a]=gibmirxy(url)
    ##                    arcpy.AddMessage( str(lat)+" "+ str(longi)+ " "+a)
            if int(a)<85:

                Ort = Ort.split('-')[0]

                arcpy.AddMessage("Georeferenzierung erneut unter 85 % Georeferenzierungsqualitaet - erneute Abfrage mit anderen Variablen Typ 1")

                url ='http://query.yahooapis.com/v1/public/yql?q=select * from geo.placefinder where house="'+house+'" and street="'+Strasse+'" and city="'+str(Ort)+'"and state="'+state+'" and country="Germany" and postal="'+str(postcode)+'"&appid=hxByDcDV34HxMu78xKN0b33dXezfkwQskuSVJ9PTUKswLDUaVicYpMWGQScmliWv7IP7SEgQKrlvWC7v1jbcU8gZJU62HTk'
    ##                        arcpy.AddMessage( url)
            ##    print url
                [lat,longi,a]=gibmirxy(url)
            ##    print lat,longi,a
            if int(a)<85:

                Ort = state
                arcpy.AddMessage( "Georeferenzierung erneut unter 85 % Georeferenzierungsqualitaet - erneute Abfrage mit anderen Variablen Typ 2 \n")

                url ='http://query.yahooapis.com/v1/public/yql?q=select * from geo.placefinder where house="'+house+'" and street="'+Strasse+'" and city="'+str(Ort)+'" and country="Germany" and postal="'+str(postcode)+'"&appid=hxByDcDV34HxMu78xKN0b33dXezfkwQskuSVJ9PTUKswLDUaVicYpMWGQScmliWv7IP7SEgQKrlvWC7v1jbcU8gZJU62HTk'
##                arcpy.AddMessage( url)
            ##    print url
                [lat,longi,a]=gibmirxy(url)

            if int(a)<85:
##                arcpy.AddError(url)
                arcpy.AddError( "\n\nNoch immer unter 85 % Georeferenzierungsqualitaet, bitte Lat und Lon im Koordinatensystem WGS84 in der Exceltabelle angeben.")
                arcpy.AddError("Eintragnummer in der Exceldatei: "+str(counter)+" Addresse:"+str(Strasse)+" "+str(house)+" "+str(postcode)+" "+str(Ort))
                arcpy.AddError("Zur manuellen Georeferenzierung kann beispielsweise Google Maps verwendet werden.")
                arcpy.AddError("Hilfestellung zur haendischen Georeferenzierung, falls keine Koordinaten bekannt sind, im unteren Bereich der Website: https://support.google.com/maps/answer/18539?hl=de")
                arcpy.AddError( "\n\nABBRUCH DES VORGANGS\n\n\n")
                exit(1)

            if lat==0 and longi==0 and a==0:
##                arcpy.AddMessage( url)
                arcpy.AddError("\n\n\n\nFEHLER: ")
                arcpy.AddError("Georeferenzierung derzeit nicht moeglich - Georeferenzierungswebsite down bzw. mit Verbindungsproblemen.")
                arcpy.AddError("Georeferenzierung Sie notfalls per Hand, um die Wartezeit zu umgehen.")
                arcpy.AddError("Hilfestellung zur haendischen Georeferenzierung im unteren Bereich der Website: https://support.google.com/maps/answer/18539?hl=de")
                arcpy.AddError("Bitte versuchen sie es spaeter erneut.\n")

                exit(1)

            pnt.X=float(longi)
            pnt.Y=float(lat)

            zeile.Lat=float(lat)
            zeile.Lon=float(longi)
            zeile.Qualitaet=int(a)


            zeile.shape = pnt
            cur_Standorte_temp.updateRow(zeile)

    arcpy.AddMessage("Es wurden "+str(counter)+" Einrichtung(en) neu georeferenziert")
    if counter < int(arcpy.GetCount_management(Shapefile_derEinrichtung).getOutput(0)):
        arcpy.AddMessage(str(int(arcpy.GetCount_management(Shapefile_derEinrichtung).getOutput(0))-counter)+" Einrichtung(en) wurden mit Georeferenzierung aus der Exceltabelle uebernommen")
    try:
        del cur_Standorte_temp,zeile
    except:
        pass


def dichtesteEntfernungproZeile(tabellen_name_pfad):
    fieldnames = [f.name for f in arcpy.ListFields(tabellen_name_pfad)]
    fieldnames = fieldnames[2:]
    cur_dichteste_Dist = arcpy.SearchCursor(tabellen_name_pfad)

    rueckgabearray=[]

    for jedezeile in cur_dichteste_Dist:
        kleinsteDistanz=999999999
        for spaltennamen in fieldnames:
            if jedezeile.getValue(str(spaltennamen))<=kleinsteDistanz and jedezeile.getValue(str(spaltennamen))!=0:
                kleinsteDistanz = jedezeile.getValue(str(spaltennamen))


        rueckgabearray.append(kleinsteDistanz)


##    print rueckgabearray
##    print len(rueckgabearray)

    del cur_dichteste_Dist,fieldnames

    return rueckgabearray

######################################################################################
#Programmeinstieg
gc.collect()

projektname = arcpy.GetParameterAsText(0)
Boolean_AlteDatenverwenden = arcpy.GetParameterAsText(1)
Kita = arcpy.GetParameterAsText(2)
Grundschulen = arcpy.GetParameterAsText(3)
Arzt = arcpy.GetParameterAsText(4)
Apotheken = arcpy.GetParameterAsText(5)
Krankenhaeuser = arcpy.GetParameterAsText(6)
Sonstige = arcpy.GetParameterAsText(7)
Boolean_Einzelhandel = arcpy.GetParameterAsText(8)
Einzelhandel = arcpy.GetParameterAsText(9)
Einzelhandel_feature = arcpy.GetParameterAsText(10)

#Pfade einrichten
base_path = str(sys.path[0]).split("2_Tool")[0]

workspace_definitionen=os.path.join(base_path, '3_Projekte', projektname,
                                 'FGDB_Definition_Projekt_' + projektname + '.gdb')
workspace_wertveraenderung=os.path.join(base_path, '3_Projekte', projektname,
                                 'FGDB_Standortkonkurrenz_Supermaerkte_' + projektname + '.gdb')
workspace_Erreichbarkeit = os.path.join(base_path, '3_Projekte', projektname,
                                 'FGDB_Erreichbarkeit_Projekt_' + projektname + '.gdb')
workspace_projekt = os.path.join(base_path, '3_Projekte', projektname)

arcpy.env.workspace=workspace_Erreichbarkeit
arcpy.env.overwriteOutput = True

if Boolean_AlteDatenverwenden=="true":
    a=("Verwendung der vorhandenen Daten")
    arcpy.AddMessage(a)
    print a
    if int(arcpy.GetCount_management(workspace_Erreichbarkeit+"\Einrichtungen_Einzelhandel").getOutput(0))>1:
        ceinz=1
    else:
        ceinz=0

    if int(arcpy.GetCount_management(workspace_Erreichbarkeit+"\Einrichtungen_Kita").getOutput(0))>1:
        ckita=1
    else:
        ckita=0

    if int(arcpy.GetCount_management(workspace_Erreichbarkeit+"\Einrichtungen_Grundschule").getOutput(0))>1:
        cgrund=1
    else:
        cgrund=0

    if int(arcpy.GetCount_management(workspace_Erreichbarkeit+"\Einrichtungen_Allgemeinmediziner").getOutput(0))>1:
        carzt=1
    else:
        carzt=0

    if int(arcpy.GetCount_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Krankenhaeuser")).getOutput(0))>1:
        ckrank=1
    else:
        ckrank=0

    if int(arcpy.GetCount_management(workspace_Erreichbarkeit+"\Einrichtungen_Apotheke").getOutput(0))>1:
        capo=1
    else:
        capo=0

    if int(arcpy.GetCount_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Sonstige")).getOutput(0))>1:
        csons=1
    else:
        csons=0

    if ckita!=0 or cgrund!=0 or carzt!=0 or capo!=0 or ckrank!=0 or ceinz!=0 or csons!=0:
        lon,lat=Koordinaten_derMittelp(workspace_definitionen)
        auswahl=Selektierung_Einrichtungen(lat,lon)
     ##   arcpy.AddMessage((auswahl))
        Erreichbarkeit(lat,lon,auswahl)
    else:
        arcpy.AddMessage("Keine Einrichtungen liegen in der direkten Umgebung zum RPC Gebiet ")
        arcpy.AddMessage("oder keine Einrichtungen wurden dem RPC Projekt hinzugefügt.")


else:
    arcpy.AddMessage("Feature Classes werden angelegt.")
    try:
        if arcpy.Exists("\Einrichtungen_Kita"):
            #leere es
            arcpy.DeleteRows_management(workspace_Erreichbarkeit+"\Einrichtungen_Kita")
        else:
            #erstelle es
            geometry_type = "POINT"
            template = ""
            has_m = "DISABLED"
            has_z = "DISABLED"
            # Creating a spatial reference object
            desc=arcpy.Describe(workspace_definitionen+"\Teilflaechen_Plangebiet")
            sp=desc.spatialReference
    ##        spatial_reference = arcpy.SpatialReference(os.path.join(workspace_definitionen,"Teilflaechen_Plangebiet"))
            arcpy.CreateFeatureclass_management(workspace_Erreichbarkeit, "Einrichtungen_Kita", geometry_type, template, has_m, has_z, sp)
            #Füge Spalten ein
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Kita", "Name", "TEXT",250)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Kita", "Kategorie", "TEXT",100)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Kita", "Strasse", "TEXT",250)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Kita", "HNR", "TEXT",10)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Kita", "Ort", "TEXT",250)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Kita", "Ortsteil","TEXT",250)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Kita", "PLZ", "LONG")
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Kita", "Lat", "DOUBLE")
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Kita", "Lon", "DOUBLE")
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Kita", "Qualitaet", "LONG")
    except:
            a= "Fehler in Erstellen der Einrichtungen_Kita Shape"
            arcpy.AddMessage(a)
            print a
    try:
        if arcpy.Exists("\Einrichtungen_Grundschule"):
            #leere es
            arcpy.DeleteRows_management(workspace_Erreichbarkeit+"\Einrichtungen_Grundschule")
        else:
            #erstelle es
            geometry_type = "POINT"
            template = ""
            has_m = "DISABLED"
            has_z = "DISABLED"
            # Creating a spatial reference object
            desc=arcpy.Describe(workspace_definitionen+"\Teilflaechen_Plangebiet")
            sp=desc.spatialReference
            arcpy.CreateFeatureclass_management(workspace_Erreichbarkeit, "Einrichtungen_Grundschule", geometry_type, template, has_m, has_z, sp)
            #Füge Spalten ein
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Grundschule", "Name", "TEXT",250)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Grundschule", "Kategorie", "TEXT",100)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Grundschule", "Strasse", "TEXT",250)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Grundschule", "HNR", "TEXT",10)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Grundschule", "Ort", "TEXT",250)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Grundschule", "Ortsteil","TEXT",250)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Grundschule", "PLZ", "LONG")
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Grundschule", "Lat", "DOUBLE")
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Grundschule", "Lon", "DOUBLE")
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Grundschule", "Qualitaet", "LONG")

    except:
        a= "Fehler in Erstellen der Einrichtungen_Grundschule Shape"
        arcpy.AddMessage(a)
        print a
    try:
        if arcpy.Exists("\Einrichtungen_Allgemeinmediziner"):
            #leere es
            arcpy.DeleteRows_management(workspace_Erreichbarkeit+"\Einrichtungen_Allgemeinmediziner")
        else:
            #erstelle es
            geometry_type = "POINT"
            template = ""
            has_m = "DISABLED"
            has_z = "DISABLED"
            # Creating a spatial reference object
            desc=arcpy.Describe(workspace_definitionen+"\Teilflaechen_Plangebiet")
            sp=desc.spatialReference
            arcpy.CreateFeatureclass_management(workspace_Erreichbarkeit, "Einrichtungen_Allgemeinmediziner", geometry_type, template, has_m, has_z, sp)
            #Füge Spalten ein
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Allgemeinmediziner", "Name", "TEXT",250)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Allgemeinmediziner", "Kategorie", "TEXT",100)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Allgemeinmediziner", "Strasse", "TEXT",250)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Allgemeinmediziner", "HNR", "TEXT",10)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Allgemeinmediziner", "Ort", "TEXT",250)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Allgemeinmediziner", "Ortsteil","TEXT",250)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Allgemeinmediziner", "PLZ", "LONG")
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Allgemeinmediziner", "Lat", "DOUBLE")
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Allgemeinmediziner", "Lon", "DOUBLE")
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Allgemeinmediziner", "Qualitaet", "LONG")
    except:
        a= "Fehler in Erstellen der Einrichtungen_Allgemeinmediziner Shape"
        arcpy.AddMessage(a)
        print a
    try:
        if arcpy.Exists("\Einrichtungen_Apotheke"):
            #leere es
            arcpy.DeleteRows_management(workspace_Erreichbarkeit+"\Einrichtungen_Apotheke")
        else:
            #erstelle es
            geometry_type = "POINT"
            template = ""
            has_m = "DISABLED"
            has_z = "DISABLED"
            # Creating a spatial reference object
            desc=arcpy.Describe(workspace_definitionen+"\Teilflaechen_Plangebiet")
            sp=desc.spatialReference
            arcpy.CreateFeatureclass_management(workspace_Erreichbarkeit, "Einrichtungen_Apotheke", geometry_type, template, has_m, has_z, sp)
            #Füge Spalten ein
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Apotheke", "Name", "TEXT",250)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Apotheke", "Kategorie", "TEXT",100)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Apotheke", "Strasse", "TEXT",250)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Apotheke", "HNR", "TEXT",10)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Apotheke", "Ort", "TEXT",250)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Apotheke", "Ortsteil","TEXT",250)
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Apotheke", "PLZ", "LONG")
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Apotheke", "Lat", "DOUBLE")
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Apotheke", "Lon", "DOUBLE")
            arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Apotheke", "Qualitaet", "LONG")

    except:
        a= "Fehler in Erstellen der Einrichtungen_Apotheke Shape"
        arcpy.AddMessage(a)
        print a
    try:
        if arcpy.Exists("\Einrichtungen_Krankenhaeuser"):
            #leere es
            arcpy.DeleteRows_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Krankenhaeuser"))
        else:
            #erstelle es
            geometry_type = "POINT"
            template = ""
            has_m = "DISABLED"
            has_z = "DISABLED"
            # Creating a spatial reference object
            desc=arcpy.Describe(workspace_definitionen+"\Teilflaechen_Plangebiet")
            sp=desc.spatialReference
            arcpy.CreateFeatureclass_management(workspace_Erreichbarkeit, "Einrichtungen_Krankenhaeuser", geometry_type, template, has_m, has_z, sp)
            #Füge Spalten ein
            arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Krankenhaeuser"), "Name", "TEXT",250)
            arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Krankenhaeuser"), "Kategorie", "TEXT",100)
            arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Krankenhaeuser"), "Strasse", "TEXT",250)
            arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Krankenhaeuser"), "HNR", "TEXT",10)
            arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Krankenhaeuser"), "Ort", "TEXT",250)
            arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Krankenhaeuser"), "Ortsteil","TEXT",250)
            arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Krankenhaeuser"), "PLZ", "LONG")
            arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Krankenhaeuser"), "Lat", "DOUBLE")
            arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Krankenhaeuser"), "Lon", "DOUBLE")
            arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Krankenhaeuser"), "Qualitaet", "LONG")

    except:
        a= "Fehler in Erstellen der Einrichtungen_Krankenhaeuser Shape"
        arcpy.AddMessage(a)
        print a

    try:
        if arcpy.Exists("\Einrichtungen_Sonstige"):
            #leere es
            arcpy.DeleteRows_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Sonstige"))
        else:
            #erstelle es
            geometry_type = "POINT"
            template = ""
            has_m = "DISABLED"
            has_z = "DISABLED"
            # Creating a spatial reference object
            desc=arcpy.Describe(workspace_definitionen+"\Teilflaechen_Plangebiet")
            sp=desc.spatialReference
            arcpy.CreateFeatureclass_management(workspace_Erreichbarkeit, "Einrichtungen_Sonstige", geometry_type, template, has_m, has_z, sp)
            #Füge Spalten ein
            arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Sonstige"), "Name", "TEXT",250)
            arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Sonstige"), "Kategorie", "TEXT",100)
            arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Sonstige"), "Strasse", "TEXT",250)
            arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Sonstige"), "HNR", "TEXT",10)
            arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Sonstige"), "Ort", "TEXT",250)
            arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Sonstige"), "Ortsteil","TEXT",250)
            arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Sonstige"), "PLZ", "LONG")
            arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Sonstige"), "Lat", "DOUBLE")
            arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Sonstige"), "Lon", "DOUBLE")
            arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Sonstige"), "Qualitaet", "LONG")

    except:
        a= "Fehler in Erstellen der Einrichtungen_Sonstige Shape"
        arcpy.AddMessage(a)
        print a

    if Boolean_Einzelhandel=="true":
        #Verwendung von 34 Versorgung Einzelhandel
        arcpy.AddMessage("Kopieren der Einzelhandelstandorte aus Tool 34_Versorgung.")
        try:
            arcpy.Delete_management("\Einrichtungen_Einzelhandel")
        except:
            pass
        try:
            arcpy.CopyFeatures_management(workspace_wertveraenderung+"\Standortdaten",workspace_Erreichbarkeit+"\Einrichtungen_Einzelhandel")
        except:
            a= "Einzelhandel Feature konnte nicht kopiert werden."
            arcpy.AddError(a)
            print a
            exit(1)
        arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Einzelhandel"), "Kategorie", "TEXT",100)
        arcpy.AddField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Einzelhandel"), "Name", "TEXT",250)

        arcpy.CalculateField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Einzelhandel"), "Kategorie", "'Einzelhandel'", "PYTHON")
        arcpy.CalculateField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Einzelhandel"), "Name"     , "[Name_postalisch]", "VB")
        arcpy.DeleteField_management(os.path.join(workspace_Erreichbarkeit,"Einrichtungen_Einzelhandel"), "Name_postalisch")


    else:
        try:
        #Einlesen bzw erst lesen
            if arcpy.Exists("\Einrichtungen_Einzelhandel"):
                #leere es
                arcpy.DeleteRows_management(workspace_Erreichbarkeit+"\Einrichtungen_Einzelhandel")
            else:
                #erstelle es
                geometry_type = "POINT"
                template = ""
                has_m = "DISABLED"
                has_z = "DISABLED"
                # Creating a spatial reference object
                desc=arcpy.Describe(workspace_definitionen+"\Teilflaechen_Plangebiet")
                sp=desc.spatialReference
                arcpy.CreateFeatureclass_management(workspace_Erreichbarkeit, "Einrichtungen_Einzelhandel", geometry_type, template, has_m, has_z, sp)

                arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Einzelhandel", "Name", "TEXT",250)
                arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Einzelhandel", "Kategorie", "TEXT",100)
                arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Einzelhandel", "Strasse", "TEXT",250)
                arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Einzelhandel", "HNR", "TEXT",10)
                arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Einzelhandel", "Ort", "TEXT",250)
                arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Einzelhandel", "Ortsteil","TEXT",250)
                arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Einzelhandel", "PLZ", "LONG")
                arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Einzelhandel", "Lat", "DOUBLE")
                arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Einzelhandel", "Lon", "DOUBLE")
                arcpy.AddField_management(workspace_Erreichbarkeit+"\Einrichtungen_Einzelhandel", "Qualitaet", "LONG")
        except:
            print "Fehler in Erstellen der Einrichtungen_Einzelhandel Shape"




    #Alles geleert bzw erstellt ->fuellen nun
    carzt=xlsladen_undStandorteerstellen(Arzt,"\Einrichtungen_Allgemeinmediziner")
    capo=xlsladen_undStandorteerstellen(Apotheken,"\Einrichtungen_Apotheke")
    if Boolean_Einzelhandel!="true":
        ceinz=xlsladen_undStandorteerstellen(Einzelhandel,"\Einrichtungen_Einzelhandel")
    else:
        ceinz=0
    cgrund=xlsladen_undStandorteerstellen(Grundschulen,"\Einrichtungen_Grundschule")
    ckita=xlsladen_undStandorteerstellen(Kita,"\Einrichtungen_Kita")
    ckrank=xlsladen_undStandorteerstellen(Krankenhaeuser,"\Einrichtungen_Krankenhaeuser")
    csons=xlsladen_undStandorteerstellen(Sonstige,"\Einrichtungen_Sonstige")

    if ckita>0:
        georeferenz("\Einrichtungen_Kita")
    if cgrund>0:
        georeferenz("\Einrichtungen_Grundschule")
    if carzt>0:
        georeferenz("\Einrichtungen_Allgemeinmediziner")
    if capo>0:
        georeferenz("\Einrichtungen_Apotheke")
    if ckrank>0:
        georeferenz("\Einrichtungen_Krankenhaeuser")
    if ceinz>0:
        georeferenz("\Einrichtungen_Einzelhandel")
    if csons>0:
        georeferenz("\Einrichtungen_Sonstige")

    if ckita!=0 or cgrund!=0 or carzt!=0 or capo!=0 or ckrank!=0 or ceinz!=0 or csons!=0:
        lon,lat=Koordinaten_derMittelp(workspace_definitionen)
        auswahl=Selektierung_Einrichtungen(lat,lon)
        Erreichbarkeit(lat,lon,auswahl)
    else:
        arcpy.AddMessage("Keine Einrichtungen liegen in der direkten Umgebung zum RPC Gebiet ")
        arcpy.AddMessage("oder keine Einrichtungen wurden dem RPC Projekt hinzugefuegt.")


    if arcpy.Exists(os.path.join(workspace_wertveraenderung,"Distanzmatrix_dichteste") )and arcpy.Exists(os.path.join(workspace_wertveraenderung,"Distanzmatrix_dichteste_planfall")) :
        nullfall=dichtesteEntfernungproZeile(workspace_wertveraenderung+"\Distanzmatrix_dichteste")
        planfall=dichtesteEntfernungproZeile(workspace_wertveraenderung+"\Distanzmatrix_dichteste_planfall")

        ergebnis=[a_i - b_i for a_i, b_i in zip(planfall,nullfall)]
        try:
            arcpy.DeleteField_management(workspace_wertveraenderung+"\Siedlungszahlendaten_planfall", "DichtesteDist")
        except:
            print "konnte nicht loeschen"

        try:
            arcpy.AddField_management(workspace_wertveraenderung+"\Siedlungszahlendaten_planfall", "DichtesteDist", "DOUBLE")
        except:
            a="Konnte Spalte nicht hinzufuegen. Keine Berechtigung auf Dateizugriff bitte Programm neustarten."
            print a
            arcpy.AddError(a)
            exit(1)
        cur_Siedlungszelle = arcpy.UpdateCursor(workspace_wertveraenderung+"\Siedlungszahlendaten_planfall")
        for c1, zeile in enumerate( cur_Siedlungszelle):
            zeile.setValue("DichtesteDist",ergebnis[c1-1])
            cur_Siedlungszelle.updateRow(zeile)
        print c1

        del cur_Siedlungszelle

        #Mach Foto
    else:
        a="34_Versorgung wurde nicht durchgefuehrt. Delta Entfernung zum naechsten Lebensmittelmarkt und Delta Entfernung zum Lebensmittelmarkt Einkaufsverhalten entfaellt"
        print a
        arcpy.AddMessage(a)



#Alle Datein vorbereitet

##lon,lat = Koordinaten_derMittelp()
##print lat, lon
##auswahl=Selektierung_Einrichtungen(lat,lon)
##Erreichbarkeit(lat,lon,auswahl)
##
####projektzieren()
##
##del projektname,pfadderExcel,workspace_Erreichbarkeit,base_path

gc.collect()

print "done"
arcpy.AddMessage("\nErfolgreich beendet\n\n")








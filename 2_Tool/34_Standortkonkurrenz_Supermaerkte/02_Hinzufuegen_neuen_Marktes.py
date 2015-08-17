# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 02_Hinzufuegen_neuen_Marktes.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# HCU Hamburg
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


import urllib,imp
import re,gc,os,sys
import arcpy
import xml.dom.minidom as minidom
import unicodedata
import time
gc.collect()
mdblibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '11_Definition_Projekt','tempmdb_lib.py'))
mdb = imp.load_source('tempmdb_lib', mdblibpath)

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
def Standorte_vorbereiten():
##    Damit ich alle IDS und Points habe -> vereine derzeitige Standpunkte + neuen Markt
##    und loesche dann in Distanzmatrix die spalten
    try:
        arcpy.Delete_management(os.path.join(workspace_projekt,"Standortdaten_planfall"))
    except:
        print "a"
        pass
    try:
        arcpy.DeleteFeatures_management(os.path.join(workspace_projekt,"Standortdaten_planfall"))
    except:
        print "c"
        pass
    try:
        arcpy.Copy_management(os.path.join(workspace_projekt,"Standortdaten"), os.path.join(workspace_projekt,"Standortdaten_planfall1"))
    except:
        a="Fehler Standortdaten_planfall konnte nicht erstellt werden"
        arcpy.AddError(a)
        print a
        exit(1)

    cur_NeuerM_Search=os.path.join(workspace_projekt,"Neuer_Markt")
    curIns_Standorteplan= os.path.join(workspace_projekt,"Standortdaten_planfall")

    try:
        arcpy.Merge_management(["Standortdaten_planfall1",cur_NeuerM_Search],curIns_Standorteplan)
    except:
        a="Error in Merge"
        arcpy.AddError(a)
        exit(1)

    try:
        arcpy.DeleteField_management(curIns_Standorteplan,"EntfallenderMarktID")
        arcpy.DeleteFeatures_management(os.path.join(workspace_projekt,"Standortdaten_planfall1"))
        arcpy.Delete_management(os.path.join(workspace_projekt,"Standortdaten_planfall1"))
    except:
        pass

    #Nun alles im Planfall
    del curIns_Standorteplan,cur_NeuerM_Search

def Siedlungszahlendaten_erstellen():
# neuer Makrt / Maerkte hinzugefuegt ->nun Siedlungszahlendaten ->dann erstelle Distanzmatrix
# Nimm dir den Punktfeature und leg netzdrueber
# verschneide das netz
# erstelle siedlungszellen
# loesche leere siedlungszellen

    if arcpy.Exists(os.path.join(workspace_projekt,"Punktlayer_Bev"))==False:
        b="PunktLayer fuer Bevoelkerungsprognose nicht vorhanden - Bitte widerholen Sie Schritt 1"
        print b
        arcpy.AddError(b)
        exit(1)
    schrittmeldung = 'Siedlungszellen werden erstellt \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung
    #ist da
    a=arcpy.Describe(os.path.join(workspace_projekt,"Punktlayer_Bev"))
    erster = (str(a.extent.XMin)+" "+str(a.extent.YMin)).replace('.',',')
    zweiter = (str(a.extent.XMin)+" "+str(a.extent.YMin+10)).replace('.',',')
    dritter = (str(a.extent.XMax)+" "+str(a.extent.YMax)).replace('.',',')
    del a
    try:
        arcpy.DeleteFeatures_management(os.path.join(workspace_projekt,"Siedlungszellen"))
        arcpy.Delete_management(os.path.join(workspace_projekt,"Siedlungszellen"))
    except:
        print "nicht loeschbar"
        pass
    try:
        #Siedlungszahlendaten ersetzen durch Siedlungszellen
        template_shape =os.path.join(workspace_projekt,"Punktlayer_Bev")

        arcpy.CreateFishnet_management(os.path.join(workspace_projekt,"Siedlungszellen"), erster, zweiter, "250", "250", "0", "0", dritter, "NO_LABELS", os.path.join(workspace_projekt,"Punktlayer_Bev"), "POLYGON")

#"539190,2846 5888257,9718" "539190,2846 5888267,9718" 250 250 0 0 "597767,9818 5928057,416"
        del template_shape
    except:
        b="Fehler - Fishnetz konnte nicht ueber Punktlayer erstellt werden!"
        print b
        arcpy.AddError(b)
        exit(1)

    #Verschneiden der Rasterzellen mit Gemeindeumringen
    schrittmeldung = 'Verschneiden der Rasterzellen mit Gemeindeumringen \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    try:
        arcpy.Delete_management(os.path.join(workspace_projekt,"Siedlungszellen_verschnitten"))
    except:
        pass

    gemeinden = os.path.join(workspace_Basis,'bkg_gemeinden')
    ausgabe = os.path.join(workspace_projekt,"Siedlungszellen_verschnitten")
    grid = os.path.join(workspace_projekt,"Siedlungszellen")
    Grid_Gemeinden_Layer = 'Grid_Gemeinden_Layer'

    inFeatures = [grid,gemeinden]
    arcpy.Union_analysis(inFeatures, ausgabe, "ALL", "", "GAPS")

    # Process: Feature-Layer erstellen
    arcpy.MakeFeatureLayer_management(ausgabe, Grid_Gemeinden_Layer, "", "", "")

    # Process: Layer nach Attributen auswaehlen
    arcpy.SelectLayerByAttribute_management(Grid_Gemeinden_Layer, "NEW_SELECTION", "\"FID_Siedlungszellen\" > 0")

    # Process: Features kopieren
    arcpy.CopyFeatures_management(Grid_Gemeinden_Layer, grid, "", "0", "0", "0")

    #############################################################################################################
    #SiedlungszellenIDs erzeugen
    schrittmeldung = 'SiedlungszellenIDs erzeugen \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    arcpy.AddField_management(grid, "SZ_ID", "LONG", 9, "", "", "SZ_ID", "NULLABLE", "REQUIRED")

    arcpy.CalculateField_management(grid, "SZ_ID", "!OBJECTID!", "PYTHON")

    try:
        arcpy.Delete_management(os.path.join(workspace_projekt,"Siedlungszellen_verschnitten"))
    except:
        pass

    del grid,ausgabe,Grid_Gemeinden_Layer,gemeinden
    #    ############################################################################################################################

    try:
        arcpy.DeleteField_management(os.path.join(workspace_projekt,"Siedlungszellen"), "Join_Count")
    except:
        pass
    punktlayer=os.path.join(workspace_projekt,"Punktlayer_Bev")
    siedlungszellenlayer_join=os.path.join(workspace_projekt,"Siedlungszellen_join")
    # Process: Raeumliche Verbindung
    arcpy.SpatialJoin_analysis(os.path.join(workspace_projekt,"Siedlungszellen"), punktlayer, siedlungszellenlayer_join, "JOIN_ONE_TO_ONE", "KEEP_ALL", "GEN \"GEN\" true true false 50 Text 0 0 ,First,#,"+os.path.join(workspace_projekt,"Siedlungszellen")+",GEN,-1,-1;AGS \"AGS\" true true false 12 Text 0 0 ,First,#,"+os.path.join(workspace_projekt,"Siedlungszellen")+",AGS,-1,-1;EWZ \"EWZ\" true true false 8 Double 0 0 ,First,#,"+os.path.join(workspace_projekt,"Siedlungszellen")+",EWZ,-1,-1;SZ_ID \"SZ_ID\" true true true 4 Long 0 0 ,First,#,"+os.path.join(workspace_projekt,"Siedlungszellen")+",SZ_ID,-1,-1", "INTERSECT", "", "")

    # Nachricht
    arcpy.AddMessage("Punkte mit Rasterzelle verschnitten \n")

    #############################################################################################################
    # Anteil der Punkte je Rasterzelle an Punkten im Gemeindelayer ermitteln

    # Feld "Anteil" erzeugen
    arcpy.AddField_management(siedlungszellenlayer_join, "Anteil", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    # Nachricht
    arcpy.AddMessage("Feld 'Anteil' hinzugefuegt \n")

    #############################################################################################################
    # Summe der Punktfeatures je Gemeinde ermitteln und in eine Tabelle schreiben
    joinField = "AGS"
    arcpy.Statistics_analysis(siedlungszellenlayer_join, str(siedlungszellenlayer_join)+"_stat", [["Join_Count", "SUM"]], joinField)

    # Nachricht
    arcpy.AddMessage("Summe je Gemeinde ermittelt \n")


    #############################################################################################################
    # Gesamtsumme der Punktfeatures je Gemeinde an den Siedlungszellenlayer anfuegen
    joinfeld = "AGS"

    jointable_name = str(siedlungszellenlayer_join)+"_stat"
    jointable = os.path.join(workspace_projekt,jointable_name)

    Siedlungszellen_Join = os.path.join(workspace_projekt,"Siedlungszellen_join")
    Siedlungszellen_Join_stat = os.path.join(workspace_projekt,"Siedlungszellen_join_stat")

    # Process: Feld verbinden
    arcpy.JoinField_management(Siedlungszellen_Join, joinField, jointable, joinField, "SUM_Join_Count")

    # Process: Features kopieren
    arcpy.CopyFeatures_management(Siedlungszellen_Join, os.path.join(workspace_projekt,"Siedlungszellen"), "", "0", "0", "0")

    # Nachricht
    arcpy.AddMessage("Joincount je Gemeinde angefuegt \n")


    #############################################################################################################
    # Anteile der Siedlungszellen an Gemeinde ermitteln

    # Process: Feld berechnen
    arcpy.CalculateField_management(os.path.join(workspace_projekt,"Siedlungszellen"), "Anteil", "divide(!SUM_JOIN_Count!,!Join_Count!)", "PYTHON", "def divide(a,b):\\n    if a == 0:\\n        value = 0\\n    else:\\n        value = float(b)/float(a)\\n    return value\\n\\n\\n")

    arcpy.AddMessage("Anteile ermittelt \n")

    #############################################################################################################
    # Erzeuge Spalte - Bevoelkerungszahl je Siedlungszelle
    schrittmeldung = 'Bevoelkerungszahl je Siedlungszelle \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    #Loesche Feld "SZ_Einwohner" (falls vorhanden)
    try:
        arcpy.DeleteField_management(os.path.join(workspace_projekt,"Siedlungszellen"), "SZ_Einwohner")
    except:
        pass

    # Feld "SZ_Einwohner" erzeugen
    arcpy.AddField_management(os.path.join(workspace_projekt,"Siedlungszellen"), "SZ_Einwohner", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    arcpy.CalculateField_management(os.path.join(workspace_projekt,"Siedlungszellen"), "SZ_Einwohner", "[Anteil] * [EWZ]", "VB", "")

    del Siedlungszellen_Join,Siedlungszellen_Join_stat
    try:
        arcpy.Delete_management(os.path.join(workspace_projekt,"Siedlungszellen_join"))
    except:
        pass
    try:
        arcpy.Delete_management(os.path.join(workspace_projekt,"Siedlungszellen_join_stat"))
    except:
        pass
    # ################################################################################
    #loesche leere Siedlungszellen

    grid = os.path.join(workspace_projekt,"Siedlungszellen")
    Grid_Gemeinden_Layer = 'Grid_Gemeinden_Layer_1'

    expression=' "SZ_Einwohner" = 0 or  "SZ_Einwohner" > 1700 '
    # Process: Feature-Layer erstellen
    arcpy.MakeFeatureLayer_management(grid, Grid_Gemeinden_Layer, "", "", "")


    # Execute SelectLayerByAttribute to determine which rows to delete
    test=arcpy.SelectLayerByAttribute_management(Grid_Gemeinden_Layer, "NEW_SELECTION", expression)

    # Execute GetCount and if some features have been selected, then execute
    #  DeleteRows to remove the selected rows.
    if int(arcpy.GetCount_management("Grid_Gemeinden_Layer_1").getOutput(0)) > 0:
        arcpy.DeleteRows_management("Grid_Gemeinden_Layer_1")

    del Grid_Gemeinden_Layer

    arcpy.Project_management(grid, os.path.join(workspace_projekt,"Siedlungszahlendaten"), "PROJCS['ETRS_1989_UTM_Zone_N32',GEOGCS['GCS_ETRS_1989',DATUM['D_ETRS_1989',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',32500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',9.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]", "'DHDN_To_WGS_1984_5x + DHDN_To_ETRS_1989_5'", "PROJCS['WGS_1984_UTM_Zone_32N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',9.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]")

    try:
        arcpy.DeleteFeatures_management(os.path.join(workspace_projekt,"Siedlungszellen"))
        arcpy.Delete_management(os.path.join(workspace_projekt,"Siedlungszellen"))
    except:
        pass

    del grid

def Distanzen_calc():
    try:
        arcpy.DeleteFeatures_management(os.path.join(workspace_projekt,"Distanzen_Markt_Sied"))
        arcpy.Delete_management(os.path.join(workspace_projekt,"Distanzen_Markt_Sied"))
    except:
        pass

    arcpy.AddMessage("Distanzberechnung mittels MS Access. Kann einige Minuten dauern...")
    #vorberechnungen fuer x und y der Rasterzellen
    inFeatures = os.path.join(workspace_projekt,"Siedlungszahlendaten")
    fieldPrecision = 18
    fieldScale = 11
    # Expressions are calculated using the Shape Field's geometry property
    expression1 = "float(!SHAPE.CENTROID!.replace(',','.').split()[0])"
    expression2 = "float(!SHAPE.CENTROID!.replace(',','.').split()[1])"

    try:
        # Execute AddField
        arcpy.AddField_management(inFeatures, "X", "DOUBLE",fieldPrecision, fieldScale)
        arcpy.AddField_management(inFeatures, "Y", "DOUBLE",fieldPrecision, fieldScale)
    except:
        pass
    # Execute CalculateField
    arcpy.CalculateField_management(inFeatures, "X", expression1,
                                    "PYTHON")
    arcpy.CalculateField_management(inFeatures, "Y", expression2,
                                    "PYTHON")

    del inFeatures
    #vorberechnungen fuer x und y der Rasterzellen
    inFeatures = os.path.join(workspace_projekt,'Standortdaten_planfall')
    fieldPrecision = 18
    fieldScale = 11
    # Expressions are calculated using the Shape Field's geometry property
##    expression1 = "float(!SHAPE.CENTROID!.replace(',','.').split()[0])"
##    expression2 = "float(!SHAPE.CENTROID!.replace(',','.').split()[1])"

    try:
        # Execute AddField
        arcpy.AddField_management(inFeatures, "X", "DOUBLE",fieldPrecision, fieldScale)
        arcpy.AddField_management(inFeatures, "Y", "DOUBLE",fieldPrecision, fieldScale)
    except:
        pass
    # Execute CalculateField
    arcpy.CalculateField_management(inFeatures, "X", expression1, "PYTHON")
    arcpy.CalculateField_management(inFeatures, "Y", expression2, "PYTHON")

    del inFeatures
    #Berechne Distanzen
    #Erstelle mdb
    #schreibe maekrte in tabelle1
    #schreibe polygonmittelpunkte in tabelle2
    #wende query darauf an
    #exportiere die distanzen in ein File
    #baue distanzmatrix
    eingangstabellen = [
        (workspace_projekt,'Standortdaten_planfall'),
        (workspace_projekt,'Siedlungszahlendaten')
    ]
    ausgabetabelle =(workspace_projekt,'Distanzen_Markt_Sied')
    sql="""SELECT  Standortdaten_planfall.ID AS ID_Markt, Siedlungszahlendaten.SZ_ID AS ID_Sied, [Standortdaten_planfall].[X]-[Siedlungszahlendaten].[X] AS difx , [Standortdaten_planfall].[Y]-[Siedlungszahlendaten].[Y] AS dify, IIf(((Sqr([difx]^2+[dify]^2))/1000)<=20000,Sqr([difx]^2+[dify]^2)/1000,0) AS Distanz
    INTO Distanzen_Markt_Sied
    FROM  Standortdaten_planfall ,Siedlungszahlendaten ORDER BY Standortdaten_planfall.ID"""

##    sql="""SELECT  Standortdaten_planfall.ID AS ID_Markt, Siedlungszahlendaten.SZ_ID AS ID_Sied, [Standortdaten_planfall].[X]-[Siedlungszahlendaten].[X] AS difx , [Standortdaten_planfall].[Y]-[Siedlungszahlendaten].[Y] AS dify, IIf(((Sqr([difx]^2+[dify]^2))/1000)<=20,Sqr([difx]^2+[dify]^2)/1000,0) AS Distanz
##    INTO Distanzen_Markt_Sied
##    FROM  Standortdaten_planfall ,Siedlungszahlendaten ORDER BY Standortdaten_planfall.ID"""

#todo
##SELECT tClient.Id, tStore.Id, [tClient].[X]-[tStore].[X] AS difX, [tClient].[Y]-[tStore].[Y] AS difY, Sqr([difX]^2+[difY]^2) AS distance
##FROM tClient, tStore
##WHERE (((Sqr(([tClient].[X]-[tStore].[X])^2+([tClient].[Y]-[tStore].[Y])^2))<=50));

    #"ID_Markt" =30 AND "ID_Sied" =136818
    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    cur_Update= arcpy.UpdateCursor(os.path.join(workspace_projekt,"Distanzen_Markt_Sied"))

    for row in cur_Update:
        if row.Distanz==0:
            cur_Update.deleteRow(row)


    del cur_Update

    schrittmeldung = 'Siedlungszellen wurden erstellt \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

def daten_einladen():
    cur_punktdistanz=arcpy.SearchCursor(os.path.join(workspace_projekt,"Distanzen_Markt_Sied"))


    array_punktdistanz=[]
    for zeile in cur_punktdistanz:
        array_punktdistanz.append([zeile.ID_Markt,zeile.ID_Sied,zeile.Distanz])

    del cur_punktdistanz

    return array_punktdistanz

def vorsortieren(array_alles):
    arcpy.AddMessage("Erstellung der Distanzmatrix. Kann einige Minuten dauern...")
    cur_siedlungszellen = arcpy.SearchCursor(os.path.join(workspace_projekt,"Siedlungszahlendaten"))
    cur_standortdaten = arcpy.SearchCursor(os.path.join(workspace_projekt,"Standortdaten_planfall"))

    array_sortiert=[]
    for eintrag in  array_alles:
        if len(array_sortiert)!=0:
            if ([c for c in array_sortiert if c[0]==eintrag[1]]):
                #einen eintrag gibt es schon
                for counter_array in array_sortiert:
                    if counter_array[0]==eintrag[1]:
                        #fuege dinge hinzu
                        if eintrag[2]>20:
                            eintrag[2] =0
                        counter_array.append([eintrag[0],eintrag[2]])
            else:
                #noch nicht im sortierten array
                if eintrag[2]>20:
                    eintrag[2] =0
                array_sortiert.append([eintrag[1],[eintrag[0],eintrag[2]]])


        else:
            if eintrag[2]>20:
                eintrag[2] =0
            array_sortiert.append([eintrag[1],[eintrag[0],eintrag[2]]])



##    print array_sortiert
##
##    for a in array_sortiert:
##        print len(a)
##        print a[1][1]
##        print a
##        print
##        for b in a:
##            print b
##
##
##        print
    array_sortiert=sorted(array_sortiert)
    return array_sortiert


def berechnestr(c):
##    arcpy.AddMessage(" ")
##    arcpy.AddMessage(c)
##    c=c/1000.
##    arcpy.AddMessage(c)
    ee=float(((-0.002*c) + 1.2291)*c)
##    arcpy.AddMessage(ee)
    return ee

def schreiben(array):

    try:
        arcpy.Delete_management(os.path.join(workspace_projekt,"Distanzmatrix"))
    except:
        print "a"
        pass
    try:
        arcpy.DeleteFeatures_management(os.path.join(workspace_projekt,"Distanzmatrix"))
    except:
        print "c"
        pass
    try:
        arcpy.CreateTable_management(workspace_projekt,"Distanzmatrix")
    except:
        a="Fehler Distanzmatrix konnte nicht erstellt werden"
        arcpy.AddError(a)
        print a
        exit(1)

    try:
        arcpy.AddField_management(os.path.join(workspace_projekt,"Distanzmatrix"),"Siedlungsid","LONG")
    except:
        pass

    cur_Maerkte=arcpy.SearchCursor(os.path.join(workspace_projekt,"Standortdaten_planfall"))

    for maerkte in cur_Maerkte:
        arcpy.AddField_management(os.path.join(workspace_projekt,"Distanzmatrix"),"ID_"+str(maerkte.Id),"FLOAT")

    del cur_Maerkte



    cur_InsertMatrix= arcpy.InsertCursor(os.path.join(workspace_projekt,"Distanzmatrix"))
    for einzelnezeilen in array:

        new_row_Matrix=cur_InsertMatrix.newRow()

        for c,eintraege in enumerate( einzelnezeilen):
            if c ==0:
                new_row_Matrix.setValue("Siedlungsid",eintraege)
            else:
                if eintraege==28887:
                    arcpy.AddMessage(eintraege[1])
                    arcpy.AddMessage(berechnestr(eintraege[1]))
                entfernung=berechnestr(eintraege[1])
                if entfernung>20:
                    entfernung=0

                new_row_Matrix.setValue("ID_"+str(eintraege[0]),entfernung)

        cur_InsertMatrix.insertRow(new_row_Matrix)


    del cur_InsertMatrix

    fieldnamess = [f.name for f in arcpy.ListFields(os.path.join(workspace_projekt,"Distanzmatrix"))]
    for spalten in fieldnamess[2:]:
        arcpy.CalculateField_management(os.path.join(workspace_projekt,"Distanzmatrix"), spalten, "updateValue( !"+spalten+"! )", "PYTHON", "def updateValue(value):\\n if value is None:\\n    return 0\\n else:\\n  return value\\n")

def loeschZuWeiteSiedlungsZel():
    cur_Siedlungszahlendaten= arcpy.UpdateCursor(os.path.join(workspace_projekt,"Siedlungszahlendaten"))
    cur_distanzmatrix = arcpy.SearchCursor(os.path.join(workspace_projekt,"Distanzmatrix"))

    counter=0
    for row_distanz in cur_distanzmatrix:
        for row_siedl in cur_Siedlungszahlendaten:
            if row_distanz.Siedlungsid ==row_siedl.SZ_ID:
                #alles okay
                break
            else:
                #nicht vorhanden
                cur_Siedlungszahlendaten.deleteRow(row_siedl)
                counter=counter+1

    del cur_distanzmatrix,cur_Siedlungszahlendaten
def erstelleDistanzmatrixen():
    try:
        arcpy.Delete_management(os.path.join(workspace_projekt,"Distanzmatrix_planfall"))
    except:
        print "a"
        pass
    try:
        arcpy.DeleteFeatures_management(os.path.join(workspace_projekt,"Distanzmatrix_planfall"))
    except:
        print "c"
        pass
    try:
        arcpy.Copy_management(os.path.join(workspace_projekt,"Distanzmatrix"), os.path.join(workspace_projekt,"Distanzmatrix_planfall"))
    except:
        a="Fehler Distanzmatrix_planfall konnte nicht erstellt werden"
        arcpy.AddError(a)
        print a
        exit(1)

    #Distanzmatrix beinhaltet momentan noch 600 und ggf 601 id
    try:
        arcpy.DeleteField_management(os.path.join(workspace_projekt,"Distanzmatrix"), "ID_600")
    except:
        a="Fehler Distanzmatrix, Spalte konnte nicht geloescht werden"
        arcpy.AddError(a)
        print a
        exit(1)

    try:
        arcpy.DeleteField_management(os.path.join(workspace_projekt,"Distanzmatrix"), "ID_601")
    except:
        pass
    #Nun sollte Distanzmatrix nur aus bestand bestehen

    cur_NeuerMarkte = arcpy.SearchCursor(os.path.join(workspace_projekt,"Neuer_Markt"))
    nummerMarkt=[]
    for a in cur_NeuerMarkte:
##        try:

            dropID=int(a.getValue("EntfallenderMarktID"))
##            arcpy.AddMessage( dropID)

            if dropID>-1:
                arcpy.DeleteField_management(os.path.join(workspace_projekt,"Distanzmatrix_planfall"), "ID_"+str(dropID))
                nummerMarkt.append(int(dropID))
##        except:
##            dropID=-1
##            arcpy.AddMessage( "Error in bka")
##            pass
##    arcpy.AddMessage(nummerMarkt)
    #nun sollte auch Distanzmatrix_planfall bereinigt sein

##    arcpy.AddMessage(str(len(nummerMarkt)))
    if(len(nummerMarkt)>0):
        nummerMarkt=sorted(nummerMarkt)
        cur_Check_StandPlan= arcpy.UpdateCursor(os.path.join(workspace_projekt,"Standortdaten_planfall"))
        for a in cur_Check_StandPlan:
            for b in nummerMarkt:
                if a.Id==b:
                    cur_Check_StandPlan.deleteRow(a)

        #nun sollte auch Standortdaten_planfall bereinigt sein
        del cur_Check_StandPlan
    del cur_NeuerMarkte

    try:
        arcpy.DeleteFeatures_management(os.path.join(workspace_projekt,"Siedlungszahlendaten_planfall"))
        arcpy.Delete_management(os.path.join(workspace_projekt,"Siedlungszahlendaten_planfall"))
    except:
        pass
    try:
        arcpy.CopyFeatures_management(os.path.join(workspace_projekt,"Siedlungszahlendaten"),os.path.join(workspace_projekt,"Siedlungszahlendaten_planfall"))
    except:
        v="Error beim Erstellen von Siedlungszahlendaten_planfall"
        arcpy.AddError(v)
        print v
        exit(1)




projektname = arcpy.GetParameterAsText(0)
##projektname='BastiFinalTostedt'
TypdesMarktes = arcpy.GetParameterAsText(1)
AlternativeFuerMarkttyp = arcpy.GetParameterAsText(2)
try:
    Discounter = arcpy.GetParameterAsText(3)
except:
    Discounter=False

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

NModerErw=arcpy.GetParameterAsText(10)

try:
    ErweiterMString=arcpy.GetParameterAsText(11)
except:
    ErweiterMString=""


try:
    radiobutton=arcpy.GetParameterAsText(12)
except:
    radiobutton=False


if radiobutton=="":
   radiobutton=False
arcpy.AddMessage("Georeferenzierung des Marktes")
##arcpy.AddMessage(projektname+" "+TypdesMarktes+" "+AlternativeFuerMarkttyp+" "+VKFL+" "+Strasse+" "+Hausnummer+" "+PLZ+" "+Ort+" "+radiobutton)
#Pfade einrichten
base_path = str(sys.path[0]).split("2_Tool")[0]

workspace_Basis = os.path.join(base_path, '1_Basisdaten', 'FGBD_01_Basisdaten_deutschland.gdb')
workspace_projekt = os.path.join(base_path, '3_Projekte', projektname,
                                 'FGDB_34_Standortkonkurrenz_Supermaerkte_' + projektname + '.gdb')


arcpy.env.workspace=workspace_projekt
arcpy.env.overwriteOutput = True

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

##arcpy.AddMessage(Strasse)
##arcpy.AddMessage(Ort)


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


    erweiterungsmarktid=-1
    boni=1

    if NModerErw=="Erweiterung":
        arcpy.AddMessage("Erweiterung")
        tablepath_maerkte = os.path.join(workspace_projekt,'Standortdaten')

        rows_uebergabepunkte = arcpy.SearchCursor(tablepath_maerkte)
        list_uebergabepunkte=[]
        Typpus = ErweiterMString.split(' | ')[0]
        strasse = ErweiterMString.split(' | ')[1]
        hnr = ErweiterMString.split(' | ')[2]
        ort =ErweiterMString.split(' | ')[3]
        qm = int(ErweiterMString.split(' | ')[4].replace(' qm',''))

        qm_alt=0
        fund =0
        for row in rows_uebergabepunkte :
            if row.Betriebstyp==Typpus and unicode(strasse)==unicode(row.Strasse) and hnr == row.HNR and unicode(ort) ==unicode( row.Ort) and qm == row.VKFL_Gesamt:
                fund=1
                qm_alt=row.VKFL_Gesamt
                erweiterungsmarktid=row.Id
                ##rows_uebergabepunkte.deleteRow(row)
                break

##                    arcpy.AddMessage(row.Betriebstyp==Typpus + " a  "+unicode(strasse)==unicode(row.Strasse) + "  a "+ hnr == row.HNR+ "  a "+ hnr == row.HNR + " a "+ unicode(ort) ==unicode( row.Ort)+  " a "+  qm == row.VKFL_gesamt)
##                    print row.Betriebstyp==Typpus + " a  "+unicode(strasse)==unicode(row.Strasse) + "  a "+ hnr == row.HNR+ "  a "+ hnr == row.HNR + " a "+ unicode(ort) ==unicode( row.Ort)+  " a "+  qm == row.VKFL_gesamt
        del rows_uebergabepunkte,tablepath_maerkte,row
        if fund==0:
            arcpy.AddError("Fehler der zuerweiternde Markt nicht gefunden")
            exit(1)
        else:
            #wurde gefunden
            Discounter=['Aktiv-Discount','e aktiv','diska','Netto(Edeka)','Netto','Lidl','Aldi','Penny','Norma','NP','treff 3000']
            found=0
            for g in Discounter:
                 if TypdesMarktes == g:
                    found=1

            if found==1 or Discounter==True:
                boni =1.47
            else:

                #checken ob betriebstyp sich aendert
                typen_alt=0
                if qm_alt <=400:
                    typen_alt=1
                elif qm_alt <=800:
                    typen_alt=2
                elif qm_alt <=1500:
                    typen_alt=3
                elif qm_alt <=2500:
                    typen_alt=4
                elif qm_alt <=5000:
                    typen_alt=5
                elif qm_alt >5000:
                    typen_alt=6

                qm_neu=VKFL
                typen_neu=0
                if qm_neu <=400:
                    typen_neu=1
                elif qm_neu <=800:
                    typen_neu=2
                elif qm_neu <=1500:
                    typen_neu=3
                elif qm_neu <=2500:
                    typen_neu=4
                elif qm_neu <=5000:
                    typen_neu=5
                elif qm_neu >5000:
                    typen_alt=6

                if typen_alt!= typen_neu:
                    boni=1.47
                else:
                    boni=1
    else:
        boni=1

##    arcpy.AddMessage(str(lat) + " "+ str(longi))

    pnt.X=float(longi)
    pnt.Y=float(lat)
##    arcpy.AddMessage("Absx "+str(pnt.X)+" y "+str(pnt.Y))
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
    zeile.setValue("Bonifaktor",float(boni))
    zeile.setValue("EntfallenderMarktID",int(erweiterungsmarktid))

    zeile.shape = pnt
    cur_NeuerMarkt.insertRow(zeile)

    del cur_NeuerMarkt

else:
    arcpy.AddMessage("Ersten eingegebenen Markt georeferenzieren.")
    cur_NeuerMarkt= arcpy.InsertCursor(workspace_projekt+"\Neuer_Markt_temp")

    zeile=cur_NeuerMarkt.newRow()
    pnt = arcpy.CreateObject("Point")


    erweiterungsmarktid=-1
    boni=1
    if NModerErw=="Erweiterung":
        arcpy.AddMessage("Erweiterung")
        tablepath_maerkte = os.path.join(workspace_projekt,'Standortdaten')

        rows_uebergabepunkte = arcpy.SearchCursor(tablepath_maerkte)
        list_uebergabepunkte=[]
        Typpus = ErweiterMString.split(' | ')[0]
        strasse = ErweiterMString.split(' | ')[1]
        hnr = ErweiterMString.split(' | ')[2]
        ort =ErweiterMString.split(' | ')[3]
        qm = int(ErweiterMString.split(' | ')[4].replace(' qm',''))

        qm_alt=0
        fund =0
        for row in rows_uebergabepunkte :
            if row.Betriebstyp==Typpus and unicode(strasse)==unicode(row.Strasse) and hnr == row.HNR and unicode(ort) ==unicode( row.Ort) and qm == row.VKFL_Gesamt:
                fund=1
                qm_alt=row.VKFL_Gesamt
                erweiterungsmarktid=row.Id
                ##rows_uebergabepunkte.deleteRow(row)
                break

    ##                    arcpy.AddMessage(row.Betriebstyp==Typpus + " a  "+unicode(strasse)==unicode(row.Strasse) + "  a "+ hnr == row.HNR+ "  a "+ hnr == row.HNR + " a "+ unicode(ort) ==unicode( row.Ort)+  " a "+  qm == row.VKFL_gesamt)
    ##                    print row.Betriebstyp==Typpus + " a  "+unicode(strasse)==unicode(row.Strasse) + "  a "+ hnr == row.HNR+ "  a "+ hnr == row.HNR + " a "+ unicode(ort) ==unicode( row.Ort)+  " a "+  qm == row.VKFL_gesamt
        del rows_uebergabepunkte,tablepath_maerkte,row
        if fund==0:
            arcpy.AddError("Fehler der zuerweiternde Markt nicht gefunden")
            exit(1)
        else:
            #wurde gefunden
            Discounter=['Aktiv-Discount','e aktiv','diska','Netto(Edeka)','Netto','Lidl','Aldi','Penny','Norma','NP','treff 3000']
            found=0
            for g in Discounter:
                 if TypdesMarktes == g:
                    found=1

            if found==1 or Discounter==True:
                boni =1.47
            else:

                #checken ob betriebstyp sich aendert
                typen_alt=0
                if qm_alt <=400:
                    typen_alt=1
                elif qm_alt <=800:
                    typen_alt=2
                elif qm_alt <=1500:
                    typen_alt=3
                elif qm_alt <=2500:
                    typen_alt=4
                elif qm_alt <=5000:
                    typen_alt=5
                elif qm_alt >5000:
                    typen_alt=6

                qm_neu=VKFL
                typen_neu=0
                if qm_neu <=400:
                    typen_neu=1
                elif qm_neu <=800:
                    typen_neu=2
                elif qm_neu <=1500:
                    typen_neu=3
                elif qm_neu <=2500:
                    typen_neu=4
                elif qm_neu <=5000:
                    typen_neu=5
                elif qm_neu >5000:
                    typen_alt=6

                if typen_alt!= typen_neu:
                    boni=1.47
                else:
                    boni=1
    else:
        boni=1


##    arcpy.AddMessage(str(lat) + " "+ str(longi))

    pnt.X=float(longi)
    pnt.Y=float(lat)
##    arcpy.AddMessage("Absx "+str(pnt.X)+" y "+str(pnt.Y))
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
    zeile.setValue("Bonifaktor",float(boni))
    zeile.setValue("EntfallenderMarktID",int(erweiterungsmarktid))
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

##        arcpy.AddMessage(str(lat) + " "+ str(longi))

        pnt.X=float(longi)
        pnt.Y=float(lat)

        row.Lat=float(lat)
        row.Lon=float(longi)
        row.Qualitaet=int(a)
        row.shape=pnt
        cur_Update_Neuer.updateRow(row)

        break
    del cur_Update_Neuer





input_features = os.path.join(workspace_projekt,"Neuer_Markt_temp")
output_features_class = os.path.join(workspace_projekt,"Neuer_Markt")


out_coordinate_system=arcpy.SpatialReference('ETRS 1989 UTM Zone N32')

arcpy.Project_management(input_features, output_features_class, out_coordinate_system)
##arcpy.AddMessage(arcpy.GetMessages())
del input_features,output_features_class,out_coordinate_system
arcpy.AlterAliasName(os.path.join(workspace_projekt,"Neuer_Markt"), 'Neuer_Markt')
##try:
##    if arcpy.Exists("Neuer_Markt_temp"):
##        arcpy.Delete_management("Neuer_Markt_temp")
##except:
##    arcpy.AddMessage("Fehler beim löschen")
gc.collect()
Siedlungszahlendaten_erstellen()
Standorte_vorbereiten()
Distanzen_calc()


blazuruck=daten_einladen()
dasruckarrry=vorsortieren(blazuruck)
schreiben(dasruckarrry)
loeschZuWeiteSiedlungsZel()
erstelleDistanzmatrixen()
gc.collect()

#ToDo

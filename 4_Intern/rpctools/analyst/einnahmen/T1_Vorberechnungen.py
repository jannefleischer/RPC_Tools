# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 01_Auswirkung_Umland.py
#
# Description: Erstellung der regionalen Auswirkungsabschätzung für das zu untersuchende Projekt
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# GGR Planung
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------
import os
import gc
import sys
import imp

import arcpy

#############################################################################################################
#
# Funktionen
#
#############################################################################################################

def getAGS(projektname):
    import arcpy,sys,os
    base_path = str(sys.path[0]).split("2_Tool")[0]
    projektFlaeche = join(base_path ,"3_Projekte",  projektname ,"FGDB_Definition_Projekt_" + projektname +".gdb","Teilflaechen_Plangebiet")
    bkg_gemeinden = join( base_path, "1_Basisdaten","FGBD_Basisdaten_deutschland.gdb","bkg_gemeinden")
    #ags aus BKG Daten extrahieren, dafür Gemeinde selektieren, die von Planfläche geschnitten wird
    #1. Feature Layer aus den bkg-daten erstellen
    try:
        arcpy.Delete_management("bkg_gemeinden_lyr")
    except:
        print""
    arcpy.MakeFeatureLayer_management(bkg_gemeinden,"bkg_gemeinden_lyr")
    #2.Spatial Select wo Planfläche vgm_lyr intersected
    arcpy.SelectLayerByLocation_management("bkg_gemeinden_lyr", "INTERSECT", projektFlaeche)
    #Wenn Flaeche = 1, ags extrahieren
    n = arcpy.GetCount_management("bkg_gemeinden_lyr").getOutput(0)
    print n

    if(int(n) == 1 ):
        gemeindeCursor = arcpy.SearchCursor("bkg_gemeinden_lyr")
        for gemeinde in gemeindeCursor:
            verbandsgemeinde = gemeinde.BEMERK
            ags = gemeinde.AGS
            RS = gemeinde.RS

    else:
        arcpy.AddMessage("Die Projektflaechen liegen innerhalb mehrerer Gemeinden, das Tool unterstuetzt zur Zeit keine interkommunalen Projekte.")
        ## TODO Dateien loeschen und Projektregistrierung loeschen)
        sys.exit()

    #Weiche nach Bundeslaendern und gemeinschaftsangehoerigen Gemeinden
    if verbandsgemeinde[0:3] != "gem":
        ags_vg = ""
        ags_regenesis = ags

    elif ags[0:2] == "03": #Niedersachsen
        print "NS"
        ags_vg = RS[0:5] + RS[9:]
        ags_regenesis = RS[0:5] + RS[6] + RS[7:]
        arcpy.AddMessage(ags_vg)


    elif ags[0:2] == "07": #Rheinland-Pfalz
        print "RP"
        ags_vg = RS[0:5] + RS[7:9]
        ags_regenesis = RS[0:5] + RS[7:]
        arcpy.AddMessage(ags_vg)

    return ags, ags_vg, ags_regenesis


def getReGenesisAGS(ags_input, verbandsgemeinde, RS):
    #Weiche nach Bundeslaendern und gemeinschaftsangehoerigen Gemeinden
    base_path = str(sys.path[0]).split("2_Tool")[0]
    workspace_basisdaten = join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb')
    VG250 = join(workspace_basisdaten,'VG250')
    where = '"AGS"'+" ='"+ ags_input + "'"

    ags_vg = ""
    ags_regenesis = ags_input

    #Rheinland-Pfalz
    if ags_input[0:2] == "07":

        if verbandsgemeinde[0:3] == "kre":
            ags_vg = ""
            ags_regenesis = ags_input

        elif verbandsgemeinde[0:3] == "gem":
            rows = arcpy.SearchCursor(VG250, where)
            for row in rows:
                ags_vg = row.SN_L + row.SN_R + row.SN_K + row.SN_V2
                ags_regenesis = ags_vg

        else:
            rows = arcpy.SearchCursor(VG250, where)
            for row in rows:
                ags_vg = row.SN_L + row.SN_R + row.SN_K + "00" + row.SN_G
                ags_regenesis = ags_vg

    #Niedersachsen
    elif ags_input[0:2] == "03":

        if verbandsgemeinde[0:3] == "kre":
            ags_vg = ""
            ags_regenesis = ags_input

        elif verbandsgemeinde[0:3] == "gem":
            rows = arcpy.SearchCursor(VG250, where)
            for row in rows:
                ags_vg = RS[0:5] + RS[6] + RS[7:9]
                ags_regenesis = ags_vg

        else:
            ags_vg = ""
            ags_regenesis = ags_input

    return ags_input, ags_vg, ags_regenesis

#############################################################################################################
#
# Beginne Hauptteil
#
#############################################################################################################

def main(parameters, messages):
    sheetlibpath = os.path.abspath(join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','sheet_lib.py'))
    sl = imp.load_source('sheet_lib', sheetlibpath)

    mdblibpath = os.path.abspath(join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','tempmdb_lib.py'))
    mdb = imp.load_source('tempmdb_lib', mdblibpath)

    poplibpath = os.path.abspath(join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','population_lib.py'))
    pop = imp.load_source('population_lib', poplibpath)

    gc.collect()

    arcpy.env.overwriteOutput = True

    # Variablen definieren
    projektname = parameters[0].value

    nettoZuzugsQuote_EW = parameters[1].value
    nettoZuzugsQuote_AP = parameters[2].value
    einzugsbereich_EW = parameters[3].value
    einzugsbereich_AP = parameters[4].value

    # Pfade einrichten
    base_path = str(sys.path[0]).split("2_Tool")[0]

    workspace_basisdaten = join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb')
    workspace_projekt_definition = join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt.gdb')
    workspace_projekt_einnahmen = join(base_path,'3_Projekte',projektname,'FGDB_Einnahmen.gdb')

    Teilflaechen_Plangebiet_Centroide = join(workspace_projekt_definition, "Teilflaechen_Plangebiet_Centroide")
    Teilflaechen_Plangebiet_CentroideGK3 = join(workspace_projekt_definition, "Teilflaechen_Plangebiet_CentroideGK3")
    gemeindenWirkraumEW_Centroide = join(workspace_projekt_definition,"gemeindenWirkraumEW_Centroide")
    gemeindenWirkraumAP_Centroide = join(workspace_projekt_definition,"gemeindenWirkraumAP_Centroide")

    #############################################################################################################
    #
    # Durchlauf Auswirkungen im Umland
    #
    #############################################################################################################
    beginmeldung = '\nDurchlauf Auswirkungen im Umland \n'
    arcpy.AddMessage(beginmeldung)
    print beginmeldung

    #############################################################################################################
    # Einwohnerzahl erzeugen
    pop.recalcPopulation(projektname)

    #############################################################################################################
    # Schritt 1
    schrittmeldung = 'Ermittle AGS der Kommune \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    ags_eigen = getAGS(projektname)[0]
    ags_vg_eigen = getAGS(projektname)[1]
    ags_regenesis_eigen = getAGS(projektname)[2]

    #############################################################################################################
    # Schritt 1
    schrittmeldung = 'Ermittle Kommunen im definierten Umkreis \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    inputGemeinden = join(workspace_basisdaten, 'bkg_gemeinden')
    gemeindenAuswirkungenAP = join(workspace_projekt_einnahmen, 'AWU_gemeindenWirkraumAP')
    gemeindenAuswirkungenEW = join(workspace_projekt_einnahmen, 'AWU_gemeindenWirkraumEW')
    projektflaechen = join(workspace_projekt_definition, 'Teilflaechen_Plangebiet')

    # Process: Layer lagebezogen auswählen
    arcpy.MakeFeatureLayer_management(inputGemeinden, "gemeinden_lyr")
    arcpy.MakeFeatureLayer_management(projektflaechen, "projektflaechen_lyr")

    umkreis_km = str(einzugsbereich_EW) + " Kilometers"
    arcpy.SelectLayerByLocation_management("gemeinden_lyr", "INTERSECT", "projektflaechen_lyr", umkreis_km, "NEW_SELECTION")
    arcpy.CopyFeatures_management("gemeinden_lyr", gemeindenAuswirkungenEW)

    # Process: Layer lagebezogen auswählen
    arcpy.MakeFeatureLayer_management(inputGemeinden, "gemeinden_lyr")
    arcpy.MakeFeatureLayer_management(projektflaechen, "projektflaechen_lyr")

    umkreis_km = str(einzugsbereich_AP) + " Kilometers"
    arcpy.SelectLayerByLocation_management("gemeinden_lyr", "INTERSECT", "projektflaechen_lyr", umkreis_km, "NEW_SELECTION")
    arcpy.CopyFeatures_management("gemeinden_lyr", gemeindenAuswirkungenAP)


    #############################################################################################################
    # Schritt 2
    schrittmeldung = 'Punktlayer aus Planflaechen erzeugen \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    # Create Centroid Layer
    try:
        arcpy.DeleteFeatures_management(Teilflaechen_Plangebiet_Centroide)
    except Exception as e:
        print 'Plangebiet Centroide nicht vorhanden, werden erstellt'

    arcpy.env.overwriteOutput = True
    arcpy.CreateFeatureclass_management(workspace_projekt_definition, "Teilflaechen_Plangebiet_Centroide", "POINT", "", "DISABLED", "DISABLED", projektflaechen, "", "0", "0", "0")

    # Create search cursor
    polygon_rows = arcpy.SearchCursor(projektflaechen)
    shapeName = arcpy.Describe(projektflaechen).shapeFieldName

    centroid_rows = arcpy.InsertCursor(Teilflaechen_Plangebiet_Centroide)

    for polygon_row in polygon_rows:
        feat = polygon_row.getValue(shapeName)

        latValue = str(feat.trueCentroid).split(' ')[1]
        lonValue = str(feat.trueCentroid).split(' ')[0]

        #print latValue, lonValue

        vertex = arcpy.CreateObject("Point")
        vertex.X = lonValue
        vertex.Y = latValue

        feature = centroid_rows.newRow()
        feature.shape = vertex
        centroid_rows.insertRow(feature)

    del centroid_rows
    del polygon_row
    del polygon_rows

    try:
        arcpy.DeleteFeatures_management(Teilflaechen_Plangebiet_CentroideGK3)
    except Exception as e:
        print 'Plangebiet CentroideGK3 nicht vorhanden, werden erstellt'

    arcpy.Project_management(Teilflaechen_Plangebiet_Centroide, Teilflaechen_Plangebiet_CentroideGK3, "PROJCS['DHDN_3_Degree_Gauss_Zone_3',GEOGCS['GCS_Deutsches_Hauptdreiecksnetz',DATUM['D_Deutsches_Hauptdreiecksnetz',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',3500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',9.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]", "DHDN_To_WGS_1984_5x", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
    arcpy.AddXY_management(Teilflaechen_Plangebiet_CentroideGK3)

    # Mittelpunkt der Teilflaechen ermitteln
    mw_y = []
    mw_x = []

    polygon_rows = arcpy.SearchCursor(Teilflaechen_Plangebiet_CentroideGK3)

    for polygon_row in polygon_rows:
        mw_x.append(polygon_row.POINT_X)
        mw_y.append(polygon_row.POINT_Y)

    mw_x = sum(mw_x)/len(mw_x)
    mw_y = sum(mw_y)/len(mw_y)


    #############################################################################################################
    # Schritt 3
    schrittmeldung = 'Punktlayer aus Umkreiskommunen (EW) erzeugen \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    # Process: Feature-Class erstellen
    try:
        arcpy.DeleteFeatures_management(gemeindenWirkraumEW_Centroide)
    except Exception as e:
        print 'Gemeinden-Wirkraum Centroide nicht vorhanden, werden erstellt'

    gemeindenWirkraumEW = join(workspace_projekt_einnahmen, 'AWU_gemeindenWirkraumEW')
    arcpy.CreateFeatureclass_management(workspace_projekt_definition, "gemeindenWirkraumEW_Centroide", "POINT", "", "DISABLED", "DISABLED", gemeindenWirkraumEW, "", "0", "0", "0")

    # Add new fields
    fieldName = "AGS"
    fieldAlias = "AGS"
    arcpy.DeleteField_management(gemeindenWirkraumEW_Centroide, fieldName)
    arcpy.AddField_management(gemeindenWirkraumEW_Centroide, fieldName, "TEXT", "", "", "",fieldAlias, "NULLABLE")

    fieldName = "AGS_VG"
    fieldAlias = "AGS_VG"
    arcpy.DeleteField_management(gemeindenWirkraumEW_Centroide, fieldName)
    arcpy.AddField_management(gemeindenWirkraumEW_Centroide, fieldName, "TEXT", "", "", "",fieldAlias, "NULLABLE")

    fieldName = "AGS_Regenesis"
    fieldAlias = "AGS_Regenesis"
    arcpy.DeleteField_management(gemeindenWirkraumEW_Centroide, fieldName)
    arcpy.AddField_management(gemeindenWirkraumEW_Centroide, fieldName, "TEXT", "", "", "",fieldAlias, "NULLABLE")

    # Create search cursor
    polygon_rows = arcpy.SearchCursor(gemeindenWirkraumEW)
    shapeName = arcpy.Describe(gemeindenWirkraumEW).shapeFieldName

    centroid_rows = arcpy.InsertCursor(gemeindenWirkraumEW_Centroide)

    for polygon_row in polygon_rows:
        feat = polygon_row.getValue(shapeName)
        ags = polygon_row.AGS
        verbandsgemeinde = polygon_row.BEMERK
        RS = polygon_row.RS

        ags_vg = getReGenesisAGS(ags, verbandsgemeinde, RS)[1]
        ags_regenesis = getReGenesisAGS(ags, verbandsgemeinde, RS)[2]

        arcpy.AddMessage(ags)
        arcpy.AddMessage(ags_regenesis)

        latValue = str(feat.trueCentroid).split(' ')[1]
        lonValue = str(feat.trueCentroid).split(' ')[0]

        #print latValue, lonValue

        vertex = arcpy.CreateObject("Point")
        vertex.X = lonValue
        vertex.Y = latValue

        feature = centroid_rows.newRow()
        feature.shape = vertex
        feature.AGS = ags
        feature.AGS_VG = ags_vg
        feature.AGS_Regenesis = ags_regenesis
        centroid_rows.insertRow(feature)

    del centroid_rows
    del polygon_row
    del polygon_rows

    arcpy.AddXY_management(gemeindenWirkraumEW_Centroide)

    schrittmeldung = '\n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    #############################################################################################################
    # Schritt 4
    schrittmeldung = 'Punktlayer aus Umkreiskommunen (AP) erzeugen \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    # Process: Feature-Class erstellen
    try:
        arcpy.DeleteFeatures_management(gemeindenWirkraumAP_Centroide)
    except Exception as e:
        print 'Gemeinden-Wirkraum Centroide nicht vorhanden, werden erstellt'

    gemeindenWirkraumAP = join(workspace_projekt_einnahmen, 'AWU_gemeindenWirkraumAP')
    arcpy.CreateFeatureclass_management(workspace_projekt_definition, "gemeindenWirkraumAP_Centroide", "POINT", "", "DISABLED", "DISABLED", gemeindenWirkraumAP, "", "0", "0", "0")

    # Add new fields
    fieldName = "AGS"
    fieldAlias = "AGS"
    arcpy.DeleteField_management(gemeindenWirkraumAP_Centroide, fieldName)
    arcpy.AddField_management(gemeindenWirkraumAP_Centroide, fieldName, "TEXT", "", "", "",fieldAlias, "NULLABLE")

    fieldName = "AGS_VG"
    fieldAlias = "AGS_VG"
    arcpy.DeleteField_management(gemeindenWirkraumAP_Centroide, fieldName)
    arcpy.AddField_management(gemeindenWirkraumAP_Centroide, fieldName, "TEXT", "", "", "",fieldAlias, "NULLABLE")

    fieldName = "AGS_Regenesis"
    fieldAlias = "AGS_Regenesis"
    arcpy.DeleteField_management(gemeindenWirkraumAP_Centroide, fieldName)
    arcpy.AddField_management(gemeindenWirkraumAP_Centroide, fieldName, "TEXT", "", "", "",fieldAlias, "NULLABLE")

    # Create search cursor
    polygon_rows = arcpy.SearchCursor(gemeindenWirkraumAP)
    shapeName = arcpy.Describe(gemeindenWirkraumAP).shapeFieldName

    centroid_rows = arcpy.InsertCursor(gemeindenWirkraumAP_Centroide)

    for polygon_row in polygon_rows:
        feat = polygon_row.getValue(shapeName)
        ags = polygon_row.AGS
        verbandsgemeinde = polygon_row.BEMERK
        RS = polygon_row.RS

        ags_vg = getReGenesisAGS(ags, verbandsgemeinde, RS)[1]
        ags_regenesis = getReGenesisAGS(ags, verbandsgemeinde, RS)[2]

        arcpy.AddMessage(ags)
        arcpy.AddMessage(ags_regenesis)

        latValue = str(feat.trueCentroid).split(' ')[1]
        lonValue = str(feat.trueCentroid).split(' ')[0]

        #print latValue, lonValue

        vertex = arcpy.CreateObject("Point")
        vertex.X = lonValue
        vertex.Y = latValue

        feature = centroid_rows.newRow()
        feature.shape = vertex
        feature.AGS = ags
        feature.AGS_VG = ags_vg
        feature.AGS_Regenesis = ags_regenesis
        centroid_rows.insertRow(feature)

    del centroid_rows
    del polygon_row
    del polygon_rows

    arcpy.AddXY_management(gemeindenWirkraumAP_Centroide)

    #############################################################################################################
    # Schritt 4
    schrittmeldung = '\nErzeuge Entfernungstabelle Einwohner \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    eingangstabellen = [
        (workspace_projekt_definition,'gemeindenWirkraumEW_Centroide'),
        (workspace_projekt_einnahmen,'AWU_gemeindenWirkraumEW')
    ]

    ausgabetabelle = (workspace_projekt_einnahmen,'AWU_DistanzenEW')

    sql = """SELECT gemeindenWirkraumEW_Centroide.AGS, gemeindenWirkraumEW_Centroide.AGS_VG, gemeindenWirkraumEW_Centroide.AGS_Regenesis, (([POINT_X]-mw_x)^2+([point_Y]-mw_y)^2)^(1/2) AS distanz, AWU_gemeindenWirkraumEW.EWZ INTO AWU_DistanzenEW
    FROM gemeindenWirkraumEW_Centroide INNER JOIN AWU_gemeindenWirkraumEW ON gemeindenWirkraumEW_Centroide.AGS = AWU_gemeindenWirkraumEW.AGS
    WHERE (((gemeindenWirkraumEW_Centroide.AGS)<>'AGSVALUE'));
    """

    sql = sql.replace("mw_x",str(mw_x)).replace("mw_y",str(mw_y)).replace("AGSVALUE",str(ags_eigen))
    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)


    #############################################################################################################
    # Schritt 3
    schrittmeldung = 'Erzeuge Entfernungstabelle Arbeitsplaetze \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    eingangstabellen = [
        (workspace_projekt_definition,'gemeindenWirkraumAP_Centroide'),
        (workspace_projekt_einnahmen,'AWU_gemeindenWirkraumAP')
    ]

    ausgabetabelle = (workspace_projekt_einnahmen,'AWU_DistanzenAP')

    sql = """
    SELECT gemeindenWirkraumAP_Centroide.AGS, gemeindenWirkraumAP_Centroide.AGS_VG, gemeindenWirkraumAP_Centroide.AGS_Regenesis, (([POINT_X]-mw_x)^2+([point_Y]-mw_y)^2)^(1/2) AS distanz, AWU_gemeindenWirkraumAP.EWZ INTO AWU_DistanzenAP
    FROM gemeindenWirkraumAP_Centroide INNER JOIN AWU_gemeindenWirkraumAP ON gemeindenWirkraumAP_Centroide.AGS = AWU_gemeindenWirkraumAP.AGS
    WHERE (((gemeindenWirkraumAP_Centroide.AGS)<>'AGSVALUE'));
    """

    sql = sql.replace("mw_x",str(mw_x)).replace("mw_y",str(mw_y)).replace("AGSVALUE",str(ags_eigen))
    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)


    #############################################################################################################
    # Schritt 4
    schrittmeldung = 'Berechne EW-Anteile entsprechend der Einwohnerzahl \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    # Maximale Distanz EW ermitteln
    maxlist = []
    ausgabetabelle = join(workspace_projekt_einnahmen,'AWU_DistanzenEW')
    rows = arcpy.SearchCursor(ausgabetabelle)
    for row in rows:
        maxlist.append(row.distanz)

    try:
        distEW_max = max(maxlist)
    except:
        distEW_max = 0

    # EWgewichtet erzeugen
    eingangstabellen = [
        (workspace_projekt_einnahmen,'AWU_DistanzenEW')
    ]

    ausgabetabelle = (workspace_projekt_einnahmen,'AWU_EWgewichtet')

    sql = """SELECT AWU_DistanzenEW.AGS, AWU_DistanzenEW.AGS_VG, AWU_DistanzenEW.AGS_Regenesis, AWU_DistanzenEW.distanz, AWU_DistanzenEW.EWZ, 1-[distanz]/distEW_max AS Faktor, (1-[distanz]/distEW_max)*[EWZ] AS AWU_EWgewichtet INTO AWU_EWgewichtet
    FROM AWU_DistanzenEW;
    """

    sql = sql.replace("distEW_max",str(distEW_max))
    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    # Summe EW ermitteln
    sumlist = []
    ausgabetabelle = join(workspace_projekt_einnahmen,'AWU_EWgewichtet')
    rows = arcpy.SearchCursor(ausgabetabelle)
    for row in rows:
        sumlist.append(row.AWU_EWgewichtet)
    sumEW = sum(sumlist)

    # Erzeuge Wanderungsfaktor
    eingangstabellen = [
        (workspace_projekt_einnahmen,'AWU_EWgewichtet')
    ]

    ausgabetabelle = (workspace_projekt_einnahmen,'AWU_WanderungsfaktorEW')

    nettoZuzugsQuote_EW = str(float(nettoZuzugsQuote_EW)/100)

    sql = """SELECT AWU_EWgewichtet.AGS, AWU_EWgewichtet.AGS_VG, AWU_EWgewichtet.AGS_Regenesis, ([AWU_EWgewichtet]/sumEW)*(nettoZuzugsQuote_EW) AS AWU_Wanderungsfaktor INTO AWU_WanderungsfaktorEW
    FROM AWU_EWgewichtet;
    """

    sql = sql.replace("sumEW",str(sumEW)).replace("nettoZuzugsQuote_EW",str(nettoZuzugsQuote_EW))
    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    # Ergaenze AGS der eigenen Kommune
    input = join(workspace_projekt_einnahmen,'AWU_WanderungsfaktorEW')
    rows = arcpy.InsertCursor(input)
    row = rows.newRow()
    row.AGS = ags_eigen
    row.AGS_VG = ags_vg_eigen
    row.AGS_Regenesis = ags_regenesis_eigen
    row.AWU_Wanderungsfaktor = float(nettoZuzugsQuote_EW)
    rows.insertRow(row)

    #############################################################################################################
    # Schritt 4
    schrittmeldung = 'Berechne AP-Anteile entsprechend der Arbeitsplatzverteilung \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    # Maximale Distanz AP ermitteln
    maxlist = []
    ausgabetabelle = join(workspace_projekt_einnahmen,'AWU_DistanzenAP')
    rows = arcpy.SearchCursor(ausgabetabelle)
    for row in rows:
        maxlist.append(row.distanz)

    try:
        distAP_max = max(maxlist)
    except:
        distAP_max = 0

    # EWgewichtet erzeugen
    eingangstabellen = [
        (workspace_projekt_einnahmen,'AWU_DistanzenAP')
    ]

    ausgabetabelle = (workspace_projekt_einnahmen,'AWU_APgewichtet')

    sql = """SELECT AWU_DistanzenAP.AGS, AWU_DistanzenAP.AGS_VG, AWU_DistanzenAP.AGS_Regenesis, AWU_DistanzenAP.distanz, AWU_DistanzenAP.EWZ, 1-[distanz]/distAP_max AS Faktor, (1-[distanz]/distAP_max)*[EWZ] AS AWU_APgewichtet INTO AWU_APgewichtet
    FROM AWU_DistanzenAP;
    """

    sql = sql.replace("distAP_max",str(distAP_max))
    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    # Summe EW ermitteln
    sumlist = []
    ausgabetabelle = join(workspace_projekt_einnahmen,'AWU_APgewichtet')
    rows = arcpy.SearchCursor(ausgabetabelle)
    for row in rows:
        sumlist.append(row.AWU_APgewichtet)
    sumAP = sum(sumlist)

    # Erzeuge Wanderungsfaktor
    eingangstabellen = [
        (workspace_projekt_einnahmen,'AWU_APgewichtet')
    ]

    ausgabetabelle = (workspace_projekt_einnahmen,'AWU_WanderungsfaktorAP')

    nettoZuzugsQuote_AP = str(float(nettoZuzugsQuote_AP)/100)

    sql = """SELECT AWU_APgewichtet.AGS, AWU_APgewichtet.AGS_VG, AWU_APgewichtet.AGS_Regenesis, ([AWU_APgewichtet]/sumAP)*(nettoZuzugsQuote_AP) AS AWU_Wanderungsfaktor INTO AWU_WanderungsfaktorAP
    FROM AWU_APgewichtet;
    """

    sql = sql.replace("sumAP",str(sumAP)).replace("nettoZuzugsQuote_AP",str(nettoZuzugsQuote_AP))
    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)

    # Ergaenze AGS der eigenen Kommune
    input = join(workspace_projekt_einnahmen,'AWU_WanderungsfaktorAP')
    rows = arcpy.InsertCursor(input)
    row = rows.newRow()
    row.AGS = ags_eigen
    row.AGS_VG = ags_vg_eigen
    row.AGS_Regenesis = ags_regenesis_eigen
    row.AWU_Wanderungsfaktor = float(nettoZuzugsQuote_AP)
    rows.insertRow(row)


    #############################################################################################################
    # Schritt 4
    schrittmeldung = 'Verteilung der EW auf Gemeinden \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    eingangstabellen = [
        (workspace_projekt_einnahmen,'AWU_WanderungsfaktorEW'),
        (workspace_projekt_definition,'Einwohnerzahl')
    ]

    ausgabetabelle = (workspace_projekt_einnahmen,'AWU_WanderungsergebnisEW')

    sql = """SELECT AWU_WanderungsfaktorEW.AGS, AWU_WanderungsfaktorEW.AGS_VG, AWU_WanderungsfaktorEW.AGS_Regenesis, Einwohnerzahl.Jahr, Sum([Einwohnerzahl]*[AWU_Wanderungsfaktor]) AS EW INTO AWU_WanderungsergebnisEW
    FROM Einwohnerzahl, AWU_WanderungsfaktorEW
    GROUP BY AWU_WanderungsfaktorEW.AGS, AWU_WanderungsfaktorEW.AGS_VG, AWU_WanderungsfaktorEW.AGS_Regenesis, Einwohnerzahl.Jahr
    ORDER BY AWU_WanderungsfaktorEW.AGS, AWU_WanderungsfaktorEW.AGS_VG, AWU_WanderungsfaktorEW.AGS_Regenesis, Einwohnerzahl.Jahr;
    """

    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)


    #############################################################################################################
    # Schritt 4
    schrittmeldung = 'Verteilung der AP auf Gemeinden \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    eingangstabellen = [
        (workspace_projekt_einnahmen,'AWU_WanderungsfaktorAP'),
        (workspace_projekt_definition,'Gewerbe_Beschaeftigte')
    ]

    ausgabetabelle = (workspace_projekt_einnahmen,'AWU_WanderungsergebnisAP')

    sql = """SELECT AWU_WanderungsfaktorAP.AGS, AWU_WanderungsfaktorAP.AGS_VG, AWU_WanderungsfaktorAP.AGS_Regenesis, Gewerbe_Beschaeftigte.Jahr, Gewerbe_Beschaeftigte.Branche, Sum([Anzahl]*[AWU_Wanderungsfaktor]) AS AP INTO AWU_WanderungsergebnisAP
    FROM Gewerbe_Beschaeftigte, AWU_WanderungsfaktorAP
    GROUP BY AWU_WanderungsfaktorAP.AGS, AWU_WanderungsfaktorAP.AGS_VG, AWU_WanderungsfaktorAP.AGS_Regenesis, Gewerbe_Beschaeftigte.Jahr, Gewerbe_Beschaeftigte.Branche
    ORDER BY AWU_WanderungsfaktorAP.AGS, AWU_WanderungsfaktorAP.AGS_VG, AWU_WanderungsfaktorAP.AGS_Regenesis, Gewerbe_Beschaeftigte.Jahr, Gewerbe_Beschaeftigte.Branche;
    """

    mdb.temp_mdb(eingangstabellen,sql,ausgabetabelle)


    #############################################################################################################
    # Schritt 4
    schrittmeldung = 'temporaere Tabellen loeschen \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    deleteList_a = ['gemeindenWirkraumAP','gemeindenWirkraumEW','gemeindenWirkraumAP_Centroide','gemeindenWirkraumEW_Centroide','Teilflaechen_Plangebiet_CentroideGK3']
    deleteList_b = ['AWU_APgewichtet','AWU_EWgewichtet','AWU_DistanzenAP','AWU_DistanzenEW']

    for e in deleteList_a:
        f = join(workspace_projekt_definition,e)
        try:
            arcpy.Delete_management(f)
        except:
            pass

    for e in deleteList_b:
        f = join(workspace_projekt_einnahmen,e)
        try:
            arcpy.Delete_management(f)
        except:
            pass

    gc.collect()
    print "fertig"
    arcpy.AddMessage('01_Auswirkung_Umland abgeschlossen')
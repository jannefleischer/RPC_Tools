# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      BastiTower
#
# Created:     03.09.2014
# Copyright:   (c) BastiTower 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#komplett neu geschrieben
import arcpy,gc,sys,os

def daten_einladen(tabelle_distanzen):
    cur_punktdistanz = arcpy.SearchCursor(workspace_projekt+tabelle_distanzen)

    array_punktdistanz=[]
    for zeile in cur_punktdistanz:
        array_punktdistanz.append([zeile.INPUT_FID,zeile.NEAR_FID,zeile.DISTANCE])

    del zeile,cur_punktdistanz

    return array_punktdistanz

def vorsortieren(shp_siedlungszellen,shp_standortdaten,array_alles):

    cur_siedlungszellen = arcpy.SearchCursor(workspace_projekt+shp_siedlungszellen)
    cur_standortdaten = arcpy.SearchCursor(workspace_projekt+shp_standortdaten)

    #INPUT_FID
    array_standortdaten=[]
    for zeile in cur_standortdaten:
        array_standortdaten.append([zeile.OBJECTID,zeile.Id])

    del zeile,cur_standortdaten

    #NEAR_FID
    array_siedlungszellen=[]
    for zeile in cur_siedlungszellen:
        array_siedlungszellen.append([zeile.OBJECTID,zeile.SZ_ID])

    del zeile,cur_siedlungszellen


##    print array_standortdaten
##    print array_siedlungszellen


    array_sortiert=[]


    for eintrag in  array_alles:
        nummer_stand=0
        numemr_sied=0
        for zeile_stand in array_standortdaten:
            if eintrag[0]==zeile_stand[0]:
                nummer_stand=zeile_stand[1]
                break


        for zeile_sied in array_siedlungszellen:
            if eintrag[1]==zeile_sied[0]:
                numemr_sied=zeile_sied[1]
                break


        if len(array_sortiert)!=0:
            if ([c for c in array_sortiert if c[0]==numemr_sied]):
                #einen eintrag gibt es schon
                for counter_array in array_sortiert:
                    if counter_array[0]==numemr_sied:
                        #fuege dinge hinzu
                        if eintrag[2]>20000:
                            eintrag[2] =0
                        counter_array.append([nummer_stand,eintrag[2]])
            else:
                #noch nicht im sortierten array
                if eintrag[2]>20000:
                    eintrag[2] =0
                array_sortiert.append([numemr_sied,[nummer_stand,eintrag[2]]])


        else:
            if eintrag[2]>20000:
                eintrag[2] =0
            array_sortiert.append([numemr_sied,[nummer_stand,eintrag[2]]])



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
    c=c/1000.
    ee=float(((-0.002*c) + 1.2291)*c)
    return ee

def schreiben(tabelle_distanzmatrix,shp_standortdaten,array):

    cur_standortdaten = arcpy.SearchCursor(workspace_projekt+shp_standortdaten)


    array_standortdaten=[]
    for zeile in cur_standortdaten:
        array_standortdaten.append(zeile.Id)

    del zeile,cur_standortdaten

    try:
        arcpy.Delete_management(workspace_projekt+tabelle_distanzmatrix)
    except:
        print " konnte Distanzmatrix nicht lieschen"

    try:
        arcpy.CreateTable_management(workspace_projekt,tabelle_distanzmatrix.replace('/',''))
    except:
        print"Fehler beim erstellen der Tabelle"
        return

    try:
        arcpy.AddField_management(workspace_projekt+tabelle_distanzmatrix, "Siedlungsid", "LONG")
        for spaltenname in array_standortdaten:
            arcpy.AddField_management(workspace_projekt+tabelle_distanzmatrix, "ID_"+str(spaltenname), "DOUBLE")
    except:
        print "Spaltenname Unexpected error:", sys.exc_info()[0]

    cur_InsertMatrix= arcpy.InsertCursor(workspace_projekt+tabelle_distanzmatrix)
    for einzelnezeilen in array:

        new_row_Matrix=cur_InsertMatrix.newRow()

        for c,eintraege in enumerate( einzelnezeilen):
            if c ==0:
                new_row_Matrix.setValue("Siedlungsid",eintraege)
            else:
                entfernung=berechnestr(eintraege[1])
                if entfernung>20:
                    entfernung=0

                new_row_Matrix.setValue("ID_"+str(eintraege[0]),entfernung)

        cur_InsertMatrix.insertRow(new_row_Matrix)


    del cur_InsertMatrix,new_row_Matrix

    fieldnamess = [f.name for f in arcpy.ListFields(workspace_projekt+tabelle_distanzmatrix)]
    for spalten in fieldnamess[2:]:
        arcpy.CalculateField_management(workspace_projekt+tabelle_distanzmatrix, spalten, "updateValue( !"+spalten+"! )", "PYTHON", "def updateValue(value):\\n if value is None:\\n    return 0\\n else:\\n  return value\\n")

def loeschZuWeiteSiedlungsZel(shape_siedlungszellen,shape_distantzmatrix):
    cur_Siedlungszellen= arcpy.UpdateCursor(shape_siedlungszellen)
    cur_distanzmatrix = arcpy.SearchCursor(shape_distantzmatrix)

    counter=0
    for row_distanz in cur_distanzmatrix:
        for row_siedl in cur_Siedlungszellen:
            if row_distanz.Siedlungsid ==row_siedl.SZ_ID:
                #alles okay
                break
            else:
                #nicht vorhanden
                cur_Siedlungszellen.deleteRow(row_siedl)
                counter=counter+1

    del cur_distanzmatrix,cur_Siedlungszellen

gc.collect()
projektname="HCU_ZGB_OTLindenEZH"
#Pfade einrichten
base_path = str(sys.path[0]).split("2_Tool")[0]

workspace_projekt = os.path.join(base_path, '3_Projekte', projektname,
                                 'FGDB_34_Wertveraenderungen_' + projektname + '.gdb')


arcpy.env.workspace=workspace_projekt
arcpy.env.overwriteOutput = True


blazuruck=daten_einladen("/Punktdistanz_Markt_Sied")
dasruckarrry=vorsortieren("/Siedlungszahlendaten_planfall_punkt","/Standortdaten",blazuruck)
schreiben("/Distanzmatrix_N_Basti","/Standortdaten",dasruckarrry)
loeschZuWeiteSiedlungsZel(workspace_projekt+"/Siedlungszahlendaten",workspace_projekt+"/Distanzmatrix_N_Basti")
gc.collect()


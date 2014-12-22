# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      GGR
#
# Created:     25.01.2013
# Copyright:   (c) GGR 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#1. Schneide aus Landkreis alle Telefonzellendaten raus
#2. Lege fishnetz 250 250 drüber
#3. kopiere alle Siedlungszellen raus
#4. Berechne entfernungen + 35% auf alle strecken

def Mittelpunkt():
    if arcpy.Exists(workspace_projekt_Teilhabe+"/Flaeche_Mittelpunkte")==False:
        # Set local variables
        inFeatures = workspace_projekt_def+"\Teilflaechen_Plangebiet"
        outFeatureClass = workspace_projekt_Teilhabe+"\Flaeche_gesamt"


        print inFeatures
        print outFeatureClass
        # Set local variables
    ##    arcpy.Dissolve_management(inFeatures, outFeatureClass, "", "", "SINGLE_PART","DISSOLVE_LINES")
        arcpy.Dissolve_management(inFeatures, outFeatureClass)

        inFeatures = workspace_projekt_Teilhabe+"\Flaeche_gesamt"
        outFeatureClass = workspace_projekt_Teilhabe+"\Flaeche_Mittelpunkte"

        arcpy.FeatureToPoint_management(inFeatures, outFeatureClass, "CENTROID")
        print "Habe es erstellt"
        del inFeatures,outFeatureClass
    print "schon vorhanden1"


    if arcpy.Exists(workspace_projekt_Teilhabe+"/Buffer20km")==False:
        arcpy.Buffer_analysis(workspace_projekt_Teilhabe+"/Flaeche_Mittelpunkte", workspace_projekt_Teilhabe+"/Buffer20km", "20000 Meter", "FULL", "ROUND", "LIST")
        print "Habe es erstellt2"

    print "schon vorhanden2"



def SelektiereZellen():
    if arcpy.Exists(workspace_projekt_Teilhabe+"/Sied20kmUmkreis")==False:
        # Make a layer and select cities which overlap the chihuahua polygon
        Marktdaten=workspace_projekt_Teilhabe+"/Standortdaten_36"
        arcpy.MakeFeatureLayer_management(workspace_vorlagen+"\Besiedelte_FlaechenDT","Besiedelte_FlaechenD1T_lyr")
##        arcpy.SelectLayerByLocation_management("Besiedelte_FlaechenD1T_lyr", 'intersect', workspace_projekt_Teilhabe+"/Buffer20km")
        arcpy.SelectLayerByLocation_management("Besiedelte_FlaechenD1T_lyr", 'intersect', Marktdaten,"20000 METER")

        # If features matched criteria write them to a new feature class
        matchcount = int(arcpy.GetCount_management("Besiedelte_FlaechenD1T_lyr").getOutput(0))
        print matchcount
        if matchcount == 0:
            print('no features matched spatial and attribute criteria')
            return 1
        else:
            arcpy.CopyFeatures_management("Besiedelte_FlaechenD1T_lyr", workspace_projekt_Teilhabe+"/Sied20kmUmkreis")

        #erstelle ID liste zum vergleichen

        try:

            arcpy.AddField_management(workspace_projekt_Teilhabe+"\Sied20kmUmkreis", "Verkn_Id", "LONG")
            # Process: Feld berechnen
            arcpy.CalculateField_management(workspace_projekt_Teilhabe+"\Sied20kmUmkreis", "Verkn_Id", "uniqueID()", "PYTHON_9.3", "counter = 0\\ndef uniqueID():\\n  global counter\\n  counter += 1\\n  return counter")
        except:
            print "fehler"
            arcpy.Delete_management(workspace_projekt_Teilhabe+"\Sied20kmUmkreis")
            return


        print "erstellt 3"
    print"schon vorhanden3"
    if arcpy.Exists(workspace_projekt_Teilhabe+"/Sied20kmUmkreis_p")==False:
        arcpy.FeatureToPoint_management(workspace_projekt_Teilhabe+"/Sied20kmUmkreis", workspace_projekt_Teilhabe+"/Sied20kmUmkreis_p","INSIDE")
        print "erstellt 4"
    print"schon vorhanden4"

def Verschneiden():

    print "as"

    #############################################################################################################
    #Verschneiden der Rasterzellen mit Gemeindeumringen
    schrittmeldung = 'Verschneiden der Rasterzellen mit Gemeindeumringen \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    gemeinden = os.path.join(workspace_basis,'bkg_gemeinden')
    ausgabe = os.path.join(workspace_projekt_Teilhabe,"Grid_Gemeinden")
    grid = os.path.join(workspace_projekt_Teilhabe,"Siedlungszellen")
    Grid_Gemeinden_Layer = 'Grid_Gemeinden_Layer'

    inFeatures = [grid,gemeinden]
    arcpy.Union_analysis(inFeatures, ausgabe, "ALL", "", "GAPS")

    # Process: Feature-Layer erstellen
    arcpy.MakeFeatureLayer_management(ausgabe, Grid_Gemeinden_Layer, "", "", "")

    # Process: Layer nach Attributen auswählen
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



def Bev_berech():

    #############################################################################################################
    # Eingangsdaten fuer Spatial Join

    #Loesche Feld "Join Count" (falls vorhanden)
    try:
        arcpy.DeleteField_management(workspace_projekt_Teilhabe+"/Siedlungszellen", "Join_Count")
    except:
        pass
    punktlayer=workspace_projekt_Teilhabe+"/Telefondaten"
    siedlungszellenlayer_join=workspace_projekt_Teilhabe+"/Siedlungszellen_join"
    # Process: Räumliche Verbindung
    arcpy.SpatialJoin_analysis(workspace_projekt_Teilhabe+"/Siedlungszellen", punktlayer, siedlungszellenlayer_join, "JOIN_ONE_TO_ONE", "KEEP_ALL", "GEN \"GEN\" true true false 50 Text 0 0 ,First,#,"+workspace_projekt_Teilhabe+"/Siedlungszellen"+",GEN,-1,-1;AGS \"AGS\" true true false 12 Text 0 0 ,First,#,"+workspace_projekt_Teilhabe+"/Siedlungszellen"+",AGS,-1,-1;EWZ \"EWZ\" true true false 8 Double 0 0 ,First,#,"+workspace_projekt_Teilhabe+"/Siedlungszellen"+",EWZ,-1,-1;SZ_ID \"SZ_ID\" true true true 4 Long 0 0 ,First,#,"+workspace_projekt_Teilhabe+"/Siedlungszellen"+",SZ_ID,-1,-1", "INTERSECT", "", "")

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
    jointable = os.path.join(workspace_projekt_Teilhabe,jointable_name)

    Siedlungszellen_Join = os.path.join(workspace_projekt_Teilhabe,"Siedlungszellen_join")
    Siedlungszellen_Join_stat = os.path.join(workspace_projekt_Teilhabe,"Siedlungszellen_join_stat")

    # Process: Feld verbinden
    arcpy.JoinField_management(Siedlungszellen_Join, joinField, jointable, joinField, "SUM_Join_Count")

    # Process: Features kopieren
    arcpy.CopyFeatures_management(Siedlungszellen_Join, workspace_projekt_Teilhabe+"/Siedlungszellen", "", "0", "0", "0")

    # Nachricht
    arcpy.AddMessage("Joincount je Gemeinde angefuegt \n")


    #############################################################################################################
    # Anteile der Siedlungszellen an Gemeinde ermitteln

    # Process: Feld berechnen
    arcpy.CalculateField_management(workspace_projekt_Teilhabe+"/Siedlungszellen", "Anteil", "divide(!SUM_JOIN_Count!,!Join_Count!)", "PYTHON", "def divide(a,b):\\n    if a == 0:\\n        value = 0\\n    else:\\n        value = float(b)/float(a)\\n    return value\\n\\n\\n")

    arcpy.AddMessage("Anteile ermittelt \n")

    #############################################################################################################
    # Erzeuge Spalte - Bevoelkerungszahl je Siedlungszelle
    schrittmeldung = 'Bevoelkerungszahl je Siedlungszelle \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    #Loesche Feld "SZ_Einwohner" (falls vorhanden)
    try:
        arcpy.DeleteField_management(workspace_projekt_Teilhabe+"/Siedlungszellen", "SZ_Einwohner")
    except:
        pass

    # Feld "SZ_Einwohner" erzeugen
    arcpy.AddField_management(workspace_projekt_Teilhabe+"/Siedlungszellen", "SZ_Einwohner", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    arcpy.CalculateField_management(workspace_projekt_Teilhabe+"/Siedlungszellen", "SZ_Einwohner", "[Anteil] * [EWZ]", "VB", "")



def loescheLeereZellen():
##        try:

            ausgabe = os.path.join(workspace_projekt_Teilhabe,"Grid_Gemeinden")
            grid = os.path.join(workspace_projekt_Teilhabe,"Siedlungszellen")
            Grid_Gemeinden_Layer = 'Grid_Gemeinden_Layer_1'

            expression=' "SZ_Einwohner" = 0 or  "SZ_Einwohner" > 1200 '
            # Process: Feature-Layer erstellen
            arcpy.MakeFeatureLayer_management(grid, Grid_Gemeinden_Layer, "", "", "")


            # Execute SelectLayerByAttribute to determine which rows to delete
            test=arcpy.SelectLayerByAttribute_management(Grid_Gemeinden_Layer, "NEW_SELECTION", expression)

            # Execute GetCount and if some features have been selected, then execute
            #  DeleteRows to remove the selected rows.
            if int(arcpy.GetCount_management("Grid_Gemeinden_Layer_1").getOutput(0)) > 0:
                arcpy.DeleteRows_management("Grid_Gemeinden_Layer_1")

##        except Exception, e:
##            # If an error occurred, print line number and error message
##            print "fehler"

def erstelleDist():

    env.workspace = workspace_projekt_Teilhabe
    arcpy.env.overwriteOutput = True
    try:
        arcpy.Delete_management(workspace_projekt_Teilhabe+ "\Distanzmatrix")
        arcpy.RefreshCatalog(workspace_projekt_Teilhabe)

    except:
        print"fehler"
        print "bitte aRcgis schliessen und neu starten"
        pass
    Marktdaten=workspace_projekt_Teilhabe+"/Standorte_LK_pro"
    cur_Maerkte=arcpy.SearchCursor(Marktdaten)
    #wohin
    arcpy.CreateTable_management(workspace_projekt_Teilhabe, "Distanzmatrix")

    Distanzmatrix =os.path.join(workspace_projekt_Teilhabe,"Distanzmatrix")

    arcpy.AddField_management(Distanzmatrix,"Siedlungsid","LONG")
    for maerkte in cur_Maerkte:
        arcpy.AddField_management(Distanzmatrix,"ID_"+str(maerkte.Id),"FLOAT")


    del Marktdaten,cur_Maerkte

def Distanzen_neu():
    in_features=os.path.join(workspace_projekt_Teilhabe,"Standorte_LK_pro")
    near_features=os.path.join(workspace_projekt_Teilhabe,"Siedlungszellen_points")
    arcpy.CreateTable_management(workspace_projekt_Teilhabe, "Distanzmatrix_vorher")
    out_table=os.path.join(workspace_projekt_Teilhabe,"Distanzmatrix_vorher")
    arcpy.PointDistance_analysis (in_features, near_features, out_table, "16,76 KILOMETER")


def baueDistanzmatrix():

    cur_Distanzvorher=arcpy.SearchCursor(workspace_projekt_Teilhabe+ "\Distanzmatrix_vorher")
    cur_Ins_Distmatrix= arcpy.InsertCursor(workspace_projekt_Teilhabe + "\Distanzmatrix")


    for a in cur_Distanzvorher:

        gefunden=0
        cur_UP_Distanz=arcpy.UpdateCursor(workspace_projekt_Teilhabe + "\Distanzmatrix")
        for cur_distm in cur_UP_Distanz:
            if a.NEAR_FID ==cur_distm.Siedlungsid:
                cur_distm.setValue("ID_"+str(a.INPUT_FID),berechnestr(a.DISTANCE))
                cur_UP_Distanz.updateRow(cur_distm)
                gefunden=1
                break
        try:
            del cur_distm
        except:
            pass
        if gefunden==0:
           c = cur_Ins_Distmatrix.newRow()
           c.setValue("Siedlungsid",a.NEAR_FID)
           c.setValue("ID_"+str(a.INPUT_FID),berechnestr(a.DISTANCE))
           cur_Ins_Distmatrix.insertRow(c)


def berechnestr(c):
    c=c/1000.
    ee=float(((-0.002*c) + 1.2291)*c)
    return ee

def Distanzen():

    grid = os.path.join(workspace_projekt_Teilhabe,"Siedlungszellen")
    Siedlungs_Layer = 'Siedlungsze'
    Maerkte_Layer='Maerkte'

    Maerkte=os.path.join(workspace_projekt_Teilhabe,"Standorte_LK_pro")
    cur_Standorte_MK=arcpy.SearchCursor(workspace_projekt_Teilhabe+"\Standorte_LK_pro")

    cur_Ins_Distmatrix= arcpy.InsertCursor(workspace_projekt_Teilhabe + "\Distanzmatrix")

    for maerkte_lauf in cur_Standorte_MK:

##        print maerkte_lauf.Id


        # Process: Feature-Layer erstellen
        arcpy.MakeFeatureLayer_management(grid, Siedlungs_Layer, "", "", "")
        arcpy.MakeFeatureLayer_management(Maerkte, Maerkte_Layer, "\"Id\" = "+str(maerkte_lauf.Id), "", "")

        # Execute SelectLayerByAttribute to determine which rows to delete
        arcpy.SelectLayerByLocation_management (Siedlungs_Layer, "WITHIN_A_DISTANCE", Maerkte_Layer,"19,81 KILOMETER","NEW_SELECTION")

        # Execute GetCount and if some features have been selected, then execute
        #  DeleteRows to remove the selected rows.
        print int(arcpy.GetCount_management(Siedlungs_Layer).getOutput(0))

        desc = arcpy.Describe(workspace_projekt_Teilhabe+"\Siedlungszellen")
        shapefieldname = desc.ShapeFieldName

        strecke=0.

        rowShape = maerkte_lauf.Shape
        rowCentroid = rowShape.centroid
##        print rowCentroid

        for a in arcpy.SearchCursor( Siedlungs_Layer):
            rowShape2 = a.Shape
            rowCentroid2 = rowShape2.centroid
##            print rowCentroid2.X
            gefunden=0
            try:
##                print "try"
                cur_UP_Distanz=arcpy.UpdateCursor(workspace_projekt_Teilhabe + "\Distanzmatrix")
                for b in cur_UP_Distanz :
                    if b.Siedlungsid == a.SZ_ID:
                        b.setValue("ID_"+str(maerkte_lauf.Id),streckeber(rowCentroid.X,rowCentroid.Y,rowCentroid2.X,rowCentroid2.Y))
                        cur_UP_Distanz.updateRow(b)
                        gefunden=1
                        break
                del b

            except:
##               print "except"
                pass
            if gefunden==0:
               c = cur_Ins_Distmatrix.newRow()
               c.setValue("Siedlungsid",a.SZ_ID)
               strecke=streckeber(rowCentroid.X,rowCentroid.Y,rowCentroid2.X,rowCentroid2.Y)
               c.setValue("ID_"+str(maerkte_lauf.Id),float(strecke+(strecke*0.35)))
               cur_Ins_Distmatrix.insertRow(c)
##                break
##                return

    del cur_Ins_Distmatrix,cur_Standorte_MK,cur_UP_Distanz

#(-0,002* Luftlinendistanz in km + 0,2291) * Luftlinendistanz in km
def streckeber(x,y,x_l,y_l):
    return float((-0.002 *(math.sqrt(float(math.pow(x-x_l,2)+math.pow(y-y_l,2)))*0.001)+0.2291)*(float(math.pow(x-x_l,2)+math.pow(y-y_l,2)))*0.001)

import arcpy,os,sys,gc,math
from arcpy import env

gc.collect()

#Pfade einrichten
base_path = str(sys.path[0]).split("2_Tool")[0]

arcpy.env.overwriteOutput = True

##projektname = arcpy.GetParameterAsText(0)
projektname="HCU_Salzdahlum"

workspace_basis = os.path.join(base_path,'1_Basisdaten','FGBD_01_Basisdaten_deutschland.gdb')
workspace_vorlagen=os.path.join(base_path,'2_Tool','37_Teilhabe_und_Erreichbarkeit','FGDB_37_Teilhabe_und_Erreichbarkeit_Tool.gdb')
workspace_projekt_def = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
workspace_projekt_Teilhabe = os.path.join(base_path,'3_Projekte',projektname,'FGDB_34_Wertveraenderungen_'+projektname+'.gdb')
workspace_projekt_ergebnis = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Abbildungen')

# Set environment settings
env.workspace = workspace_projekt_Teilhabe

##Mittelpunkt()
##SelektiereZellen()

Verschneiden()

Bev_berech()
loescheLeereZellen()


##erstelleDist()
##Distanzen_neu()
##baueDistanzmatrix()


gc.collect()
del workspace_projekt_def,workspace_projekt_ergebnis,workspace_projekt_Teilhabe,workspace_vorlagen,arcpy,env,workspace_basis

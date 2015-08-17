# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 01_Vorberechnungen.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# HCU Hamburg
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


import arcpy, os, sys, math, urllib , re, gc

# Variablen definieren
projektname = arcpy.GetParameterAsText(0)

base_path = str(sys.path[0]).split("2_Tool")[0]
workspace_basisdaten = os.path.join(base_path,'1_Basisdaten','FGBD_01_Basisdaten_deutschland.gdb')
workspace_projekt = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
workspace_erreichbarkeit = os.path.join(base_path,'3_Projekte',projektname,'FGDB_37_Erreichbarkeit_Projekt_'+projektname+'.gdb')
workspace_projekt_ergebnisse = os.path.join(base_path,'3_Projekte',projektname, 'Ergebnisausgabe', 'Abbildungen')
arcpy.env.workspace = workspace_projekt
arcpy.env.overwriteOutput = True

Orte_temp = os.path.join(workspace_erreichbarkeit,"Zentrale_Orte_75km_temp")

# Centroid des Gebiets ermitteln
try:
    if(arcpy.Exists(os.path.join(workspace_erreichbarkeit,"Mittelpunkt_RPC_Gebiet"))==True):
        arcpy.Delete_management(os.path.join(workspace_erreichbarkeit,"Mittelpunkt_RPC_Gebiet"))
except:
    arcpy.AddError( "Mittelpunkt_RPC_Gebiet konnten nicht geloescht werden1")

if int(arcpy.GetCount_management(os.path.join(workspace_projekt,"Teilflaechen_Plangebiet")).getOutput(0))>1:
    try:
        arcpy.Dissolve_management(os.path.join(workspace_projekt,"Teilflaechen_Plangebiet"),os.path.join(workspace_erreichbarkeit, "Flaeche_Plangebiet_dissolved"))
    #Featur to Point nicht verwendbar weil Info Lizens
        fieldName1 = "xCentroid"
        fieldName2 = "yCentroid"
        # Expressions are calculated using the Shape Field's geometry property
        expression1 = "float(!SHAPE.CENTROID!.split()[0].replace(',','.'))"
        expression2 = "float(!SHAPE.CENTROID!.split()[1].replace(',','.'))"

        # Execute AddField
        arcpy.AddField_management(os.path.join(workspace_erreichbarkeit,"Flaeche_Plangebiet_dissolved"), fieldName1, "DOUBLE")
        arcpy.AddField_management(os.path.join(workspace_erreichbarkeit,"Flaeche_Plangebiet_dissolved"), fieldName2, "DOUBLE")

        # Execute CalculateField
        arcpy.CalculateField_management(os.path.join(workspace_erreichbarkeit,"Flaeche_Plangebiet_dissolved"), fieldName1, expression1,"PYTHON")
        arcpy.CalculateField_management(os.path.join(workspace_erreichbarkeit,"Flaeche_Plangebiet_dissolved"), fieldName2, expression2,"PYTHON")

        # Creating a spatial reference object
    ##        spatial_reference = arcpy.SpatialReference(os.path.join(workspace_erreichbarkeit+ "/Teilflaechen_Plangebiet"))
        arcpy.CreateFeatureclass_management(workspace_erreichbarkeit,"Mittelpunkt_RPC_Gebiet","POINT",os.path.join(workspace_erreichbarkeit,"Flaeche_Plangebiet_dissolved"),"","","Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj")

        for a in arcpy.SearchCursor(os.path.join(workspace_erreichbarkeit,"Flaeche_Plangebiet_dissolved")):

            print float(a.xCentroid),float( a.yCentroid)
            xy=arcpy.Point(a.xCentroid, a.yCentroid)


        # Open an InsertCursor and insert the new geometry
        #
        c = arcpy.InsertCursor(os.path.join(workspace_erreichbarkeit,"Mittelpunkt_RPC_Gebiet"), ["SHAPE@XY"])
        newRow = c.newRow()
        newRow.shape = xy
        c.insertRow(newRow)

        # Delete cursor object
        #
        del c,xy,newRow

    except:
        arcpy.AddError("Fehler beim Erstellen des Mittelpunktes")
        exit(1)
    try:
        arcpy.Delete_management(os.path.join(workspace_erreichbarkeit,"Flaeche_Plangebiet_dissolved"))
        arcpy.DeleteFeatures_management(os.path.join(workspace_erreichbarkeit,"Flaeche_Plangebiet_dissolved"))
    except:
        arcpy.AddError( "Error im Loeschen der Dissolve")

else:
    arcpy.CopyFeatures_management(os.path.join(workspace_projekt,"Teilflaechen_Plangebiet"), os.path.join(workspace_erreichbarkeit,"Teilflaechen_Plangebiet"))
    try:

        fieldName1 = "xCentroid"
        fieldName2 = "yCentroid"
        # Expressions are calculated using the Shape Field's geometry property
        expression1 = "float(!SHAPE.CENTROID!.split()[0].replace(',','.'))"
        expression2 = "float(!SHAPE.CENTROID!.split()[1].replace(',','.'))"

        # Execute AddField
        arcpy.AddField_management(os.path.join(workspace_erreichbarkeit,"Teilflaechen_Plangebiet"), fieldName1, "DOUBLE")
        arcpy.AddField_management(os.path.join(workspace_erreichbarkeit,"Teilflaechen_Plangebiet"), fieldName2, "DOUBLE")

        # Execute CalculateField
        arcpy.CalculateField_management(os.path.join(workspace_erreichbarkeit,"Teilflaechen_Plangebiet"), fieldName1, expression1,"PYTHON")
        arcpy.CalculateField_management(os.path.join(workspace_erreichbarkeit,"Teilflaechen_Plangebiet"), fieldName2, expression2,"PYTHON")

        # Creating a spatial reference object
##        spatial_reference = arcpy.SpatialReference(os.path.join(workspace_erreichbarkeit+ "/Teilflaechen_Plangebiet"))
        arcpy.CreateFeatureclass_management(workspace_erreichbarkeit,"Mittelpunkt_RPC_Gebiet","POINT",os.path.join(workspace_erreichbarkeit,"Teilflaechen_Plangebiet"),"","","Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj")

        for a in arcpy.SearchCursor(os.path.join(workspace_erreichbarkeit,"Teilflaechen_Plangebiet")):

            print float(a.xCentroid),float( a.yCentroid)
            xy=arcpy.Point(a.xCentroid, a.yCentroid)


        # Open an InsertCursor and insert the new geometry
        #
        c = arcpy.InsertCursor(os.path.join(workspace_erreichbarkeit,"Mittelpunkt_RPC_Gebiet"), ["SHAPE@XY"])
        newRow = c.newRow()
        newRow.shape = xy
        c.insertRow(newRow)

        # Delete cursor object
        #
        del c,xy,newRow
##        arcpy.CopyFeatures_management(os.path.join(workspace_erreichbarkeit,"Teilflaechen_Plangebiet"),workspace_erreichbarkeit+ "\Mittelpunkt_RPC_Gebiet")
    ##    arcpy.FeatureToPoint_management(os.path.join(workspace_projekt,"Teilflaechen_Plangebiet"),workspace_erreichbarkeit+ "\Mittelpunkt_RPC_Gebiet", "CENTROID")
    except:
        arcpy.AddError("Fehler beim Erstellen des Mittelpunktes")
        exit(1)

    try:
        if arcpy.Exists(os.path.join(workspace_erreichbarkeit,"Teilflaechen_Plangebiet"))==True:
            arcpy.Delete_management(os.path.join(workspace_erreichbarkeit,"Teilflaechen_Plangebiet"))
    except:
        arcpy.AddError( "Error im Loeschen der Teilflaechen_Plangebiet")



schrittmeldung = 'Geographischer Mittelpunkt der RPC-Flaeche ermittelt'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

try:
##    arcpy.AddMessage(arcpy.Exists(os.path.join(workspace_projekt,"zwischenspeicher_sort1")))
    if arcpy.Exists(os.path.join(workspace_projekt,"zwischenspeicher_sort1")):
##        arcpy.Delete_management(workspace_projekt+"\zwischenspeicher_sort1")
        arcpy.Delete_management("zwischenspeicher_sort1")

except:
    arcpy.AddError("Ein Featureclass konnte nicht geloescht werden. Bitte ArcGis neu starten und erneut durchfuehren.\n")

try:
    if arcpy.Exists(os.path.join(workspace_projekt,"zwischenspeicher"))==True:
        arcpy.Delete_management(os.path.join(workspace_projekt,"zwischenspeicher"))
except:
    arcpy.AddError("Ein Featureclass konnte nicht geloescht werden. Bitte ArcGis neu starten und erneut durchfuehren.\n")
#####################################################################################
# 1. Zentrale Orte im Umkreis von 75km identifizieren

# Alle Zentralen Orte temporaer als Feature Layer einladen
arcpy.MakeFeatureLayer_management (os.path.join(workspace_basisdaten,"Zentrale_Orte"), "zwischenspeicher")

# Alle Zentralen Orte im Umkreis von 75km selektieren
arcpy.SelectLayerByLocation_management ("zwischenspeicher", "WITHIN_A_DISTANCE", workspace_erreichbarkeit+"\Mittelpunkt_RPC_Gebiet", "75000 meters", "NEW_SELECTION")

# Staedteliste nach Einwohnern sortieren
arcpy.Sort_management ("zwischenspeicher","zwischenspeicher_sort1", [["EW_2011", "DESCENDING"]])

# Die selektierten Orte Speichern
arcpy.CopyFeatures_management ("zwischenspeicher_sort1", Orte_temp)

# Wenn mmehr als 20 Orte im Umkreis, nur die 20 mit der hoechsten Einwohnerzahl behalten
rows = arcpy.SearchCursor(Orte_temp)
EW = []
for row in rows:
    EW.append(row.EW_2011)
if len(EW)>20:
    EW_min = EW[19]
else: EW_min = 0
del rows

arcpy.MakeFeatureLayer_management (Orte_temp, "zwischenspeicher2")
arcpy.SelectLayerByAttribute_management ("zwischenspeicher2", "", '"EW_2011" >= '+str(EW_min))
arcpy.CopyFeatures_management ("zwischenspeicher2", workspace_erreichbarkeit+"\Zentrale_Orte_75km")

# Temporaere Feature Class mit allen Zentralen Orten loeschen
#### Delete funktioniert nicht. Zudem ist mir ein Raetsel weshalb "zwischenspeicher_sort" Ueberhaupt in der .gdb vorkommt. Ist doch nur ein temporaerer Feature Layer
try:
    arcpy.DeleteFeatures_management (Orte_temp)
    arcpy.DeleteFeatures_management (workspace_erreichbarkeit+"\zwischenspeicher_sort")
except:
    pass

schrittmeldung = 'Zentrale Orte im Umkreis von 75km erfolgreich ausgelesen'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

#####################################################################################
# 2. Alle Haltestellen im Umkreis von 1.000m ermitteln

# Unicode kram
def _callback(matches):
    id = matches.group(1)
    try:
        return unichr(int(id))
    except:
        return id

def decode_unicode_references(data):
    return re.sub("&#(\d+)(;|(?=\s))", _callback, data)

# Multiple-Ring-Buffer im Radius von 500 & 1.000m erstellen
arcpy.MultipleRingBuffer_analysis(os.path.join(workspace_erreichbarkeit,"Mittelpunkt_RPC_Gebiet"),os.path.join(workspace_erreichbarkeit,"Buffer_1000_m_500_m_"), [500,1000], "meters", "", "NONE")


def Lese_Mittelpunkt(base_path,projektname):

    workspace_erreichbarkeit = os.path.join(base_path,'3_Projekte',projektname,'FGDB_37_Erreichbarkeit_Projekt_'+projektname+'.gdb')

    mittelpunkt = workspace_erreichbarkeit+"\Mittelpunkt_RPC_Gebiet"
    desc = arcpy.Describe(mittelpunkt)
    rows = arcpy.SearchCursor(mittelpunkt, "", "Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj","","")
    for row in rows:
        feat = row.getValue(desc.ShapeFieldName)
        pnt = feat.getPart()
    del rows, row

    # X und Y umformatieren fUer URL-Query
    x_start = ("%.6f" % pnt.X).replace('.','')
    y_start = ("%.6f" % pnt.Y).replace('.','')

    return x_start,y_start

#----------------------------------------------------------------------------------------
#Umgebung durchsuchen nach Haltestellen
def escape(html):
    rueck=[]
    for usd in html:
        usd=usd.decode('iso-8859-1')
        rueck.append(usd)
    return rueck

def such (kette):
    IBNR=[]
    distance=[]
    name=[]
    X=[]
    Y=[]
    str1="!id="
    str11="!dist="
    x="!X="
    y="!Y="
    str2='!">'
    str3="</a>"
    str4="!"
    for list in kette:
        IBNR.append(int(list[list.find(str1)+4:list.find(str11)]))
        distance.append(int(list[list.find(str11)+6:list.find(str2)]))
        if len(str((list[list.find(x)+3:list.find(y)])))==7:
            X.append(float("0"+(list[list.find(x)+3:list.find(y)])[:1]+"."+(list[list.find(x)+3:list.find(y)])[1:]))
        else:
            X.append(float((list[list.find(x)+3:list.find(y)])[:2]+"."+(list[list.find(x)+3:list.find(y)])[2:]))
        Y.append(float((list[list.find(y)+3:list.find(str1)])[:2]+"."+(list[list.find(y)+3:list.find(str1)])[2:]))
        name.append(decode_unicode_references(str(list[list.find(str2)+3:list.find(str3)])))

    return IBNR,distance,name,X,Y

def Haltestellen_in_der_Umgebung(base_path,projektname,bereich,Mittelp_x,Mittelp_y):

    workspace_erreichbarkeit = os.path.join(base_path,'3_Projekte',projektname,'FGDB_37_Erreichbarkeit_Projekt_'+projektname+'.gdb')

    str2 = '<a class="uLine"';
    bekannte=[]

    mein_x=str(Mittelp_x)
    mein_y=str(Mittelp_y)
    max_dist=str(bereich)

    # Abfrage Haltestellen bei DB-mobil
    f = urllib.urlopen("http://mobile.bahn.de/bin/mobil/query.exe/dox?ld=9627&n=1&rt=1&use_realtime_filter=1&performLocating=2&tpl=stopsnear&look_maxdist="+max_dist+"&look_stopclass=1023&look_x="+mein_x+"&look_y="+mein_y)
##    arcpy.AddMessage( "http://mobile.bahn.de/bin/mobil/query.exe/dox?ld=9627&n=1&rt=1&use_realtime_filter=1&performLocating=2&tpl=stopsnear&look_maxdist="+max_dist+"&look_stopclass=1023&look_x="+mein_x+"&look_y="+mein_y)
    for zeilen in f:
        if (zeilen.find(str2) == 0):
            bekannte.append(zeilen)
    f.close()

    # Decodieren
    bekannte = escape(bekannte)

    # Attribute auslesen
    [IBNR,distance,name,Halte_x,Halte_y]=such(bekannte)

    # Feature-Class mit allen oePNV-Haltestellen loeschen, falls sie bereits existiert
    try:
        arcpy.DeleteFeatures_management (os.path.join(workspace_erreichbarkeit,"OEPNV_Haltestellen"))
    except:
        pass
    try:
        arcpy.Delete_management (os.path.join(workspace_erreichbarkeit,"OEPNV_Haltestellen"))
    except:
        pass
    try:
        # Feature-Class zum Speichern der Haltestellen erstellen
        arcpy.CreateFeatureclass_management(workspace_erreichbarkeit, "OEPNV_Haltestellen", "POINT","","","","Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj")
    except:
        a="OEPNV_Haltestellen konnte nicht erstellt werden."
        arcpy.AddError(a)
        print a
        exit(1)
    target = os.path.join(workspace_erreichbarkeit,"OEPNV_Haltestellen")
    arcpy.AddField_management(target, "IBNR", "LONG")
    arcpy.AddField_management(target, "Name", "TEXT", 250)
    arcpy.AddField_management(target, "Distanz", "LONG")
    arcpy.AddField_management(target, "Lon", "FLOAT")
    arcpy.AddField_management(target, "Lat", "FLOAT")
    arcpy.AddField_management(target, "Name_short", "TEXT",250)
    del target

    # Daten in Feature-Class schreiben
    cur_Haltestellen= arcpy.InsertCursor(os.path.join(workspace_erreichbarkeit,"OEPNV_Haltestellen"))

    i = 0
    for n in IBNR:
        pnt = arcpy.CreateObject("Point")
        pnt.X = Halte_x[i]
        pnt.Y = Halte_y[i]

        row_Haltestellen = cur_Haltestellen.newRow()
        row_Haltestellen.IBNR = IBNR[i]
        row_Haltestellen.Distanz = distance[i]
        row_Haltestellen.Name = name[i]
        row_Haltestellen.Lat = Halte_y[i]
        row_Haltestellen.Lon = Halte_x[i]
        row_Haltestellen.shape = pnt
        try:
            row_Haltestellen.Name_short = name[i].split(",")[0]
        except:
            row_Haltestellen.Name_short = name[i]
        cur_Haltestellen.insertRow(row_Haltestellen)
        # Achtung, aktiver print loest bei AusfUehrung aus ArcGIS asci-decode-Fehler aus
        ##print IBNR[i], distance[i], name[i], Halte_y[i], Halte_x[i]
        i+=1
    del cur_Haltestellen
    return bekannte

# Funktionen ausfUehren
[Mittelp_x,Mittelp_y]=Lese_Mittelpunkt(base_path,projektname)
Daten=Haltestellen_in_der_Umgebung(base_path,projektname,1000,Mittelp_x,Mittelp_y)



if len(Daten)>0:
    print 'Haltestellen im 1.000m Radius ausgelesen \n'
    arcpy.AddMessage('Haltestellen im 1.000m Radius ausgelesen')
else:
    print 'Haltestellen im 2.000m Radius ausgelesen, da dichteste Haltestelle weiter als 1.000m vom RPC - Gebiet entfernt.\n'
    arcpy.AddMessage('Haltestellen im 2.000m Radius ausgelesen, da dichteste Haltestelle weiter als 1.000m vom RPC - Gebiet entfernt.')
    Haltestellen_in_der_Umgebung(base_path,projektname,2000,Mittelp_x,Mittelp_y)


# 3. Uebersichtskarte mit allen Haltestellen erzeugen

#Kopiere Template.mxd
mxd_template = arcpy.mapping.MapDocument(os.path.join(base_path, "2_Tool","37_Erreichbarkeit","37_Template_Kartenerzeugung","37_Haltestellenkarte_Template.mxd"))
mxdpfad = os.path.join(workspace_projekt_ergebnisse,'37_Karte_Haltestellen.mxd')
mxd_template.saveACopy(mxdpfad)

# Ersetze Datenquelle
Haltestellen_mxd = arcpy.mapping.MapDocument(mxdpfad)
templatepath = os.path.join(base_path,"2_Tool","37_Erreichbarkeit","37_Template_Kartenerzeugung","template.gdb")
resultpath = os.path.join(base_path,"3_Projekte",projektname,"FGDB_37_Erreichbarkeit_Projekt_"+projektname+".gdb")
Haltestellen_mxd.findAndReplaceWorkspacePaths(templatepath, resultpath)

templatepath = os.path.join(base_path,"3_Projekte", "Template","FGDB_37_Erreichbarkeit_Projekt_Template"+".gdb")
resultpath = os.path.join(base_path,"3_Projekte",projektname,"FGDB_11_Definition_Projekt_"+projektname+".gdb")
Haltestellen_mxd.findAndReplaceWorkspacePaths(templatepath, resultpath)
del templatepath, resultpath


# Setze Viewport neu
df = arcpy.mapping.ListDataFrames(Haltestellen_mxd)[0]
gebietLayer = arcpy.mapping.ListLayers(Haltestellen_mxd, "Buffer_1000_m_500_m_", df)[0]
arcpy.SelectLayerByAttribute_management(gebietLayer, "NEW_SELECTION", "\"OBJECTID\" > 0")
df.extent = gebietLayer.getSelectedExtent(False)
arcpy.SelectLayerByAttribute_management(gebietLayer, "CLEAR_SELECTION")
df.scale = df.scale * 1.2

arcpy.RefreshActiveView()
Haltestellen_mxd.save()
del mxd_template , df

#Exportiere Ergebnis
arcpy.mapping.ExportToJPEG(Haltestellen_mxd, os.path.join(workspace_projekt_ergebnisse, "37_Karte_Haltestellen.jpg"), "PAGE_LAYOUT",resolution=150)

schrittmeldung = 'Uebersichtskarte mit allen Haltestellen erstellt \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

del Haltestellen_mxd
# Endmeldung
print 'done \n'
arcpy.AddMessage('Vorberechnungen abgeschlossen')
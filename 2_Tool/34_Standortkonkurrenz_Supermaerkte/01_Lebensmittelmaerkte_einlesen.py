# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 01_Lebensmittelmaerkte_einlesen.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# HCU Hamburg
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


import arcpy
import xlsxwriter
import gc,os,re
import xlrd,sys
import urllib
import time
import xml.dom.minidom as minidom

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

def xlsladen_undStandorteerstellen(pfad):
    try:
        arcpy.DeleteRows_management(workspace_projekt+"\Standorte_temp")
        arcpy.AddMessage("Neue Standorte -> Alte Tabelle geleert")

    except:
        pass



    workbook = xlrd.open_workbook(pfad)
    worksheet = workbook.sheet_by_name('Tabelle1')
    num_rows = worksheet.nrows - 1
    num_cells = worksheet.ncols - 1
    curr_row = -1
    Fieldname=[]
    line=[]
    counter=0
    while curr_row < num_rows:

        Betriebstyp=""
        Strasse=""
        Ort=""
        Ortsteil=""
        Postleitzahl=""
        Hausnummer=""
        VKFL=""
        Lat=""
        Lon=""


        curr_row += 1
        row = worksheet.row(curr_row)
    ##    print 'Row:', curr_row
        curr_cell = -1
        if curr_row ==0:
##            print "schon fertig"
            gdb=workspace_projekt+"\Standorte_temp"

            cur = arcpy.InsertCursor(gdb)
            arcpy.AddMessage("Schreiben der Exceleintraege in die Feature Class.")
        else:
##            try:

                row = cur.newRow()
                pnt = arcpy.CreateObject("Point")

                counter += 1
##                if counter==38:
##                    counter =39
                row.Id=counter

                if (counter%50)==0:
                    arcpy.AddMessage(str(counter)+" Eintraege in die Feature Class geschrieben.")

                cur= arcpy.InsertCursor(gdb)


                curr_cell += 1

                try:
                    row.Betriebstyp=worksheet.cell_value(curr_row, curr_cell)
                    Betriebstyp=worksheet.cell_value(curr_row, curr_cell)

                except:
                    pass

                curr_cell += 1

                try:
                    row.Name_postalisch=worksheet.cell_value(curr_row, curr_cell)
                except:
                    pass

                curr_cell += 1

                try:
                    row.PLZ=worksheet.cell_value(curr_row, curr_cell)
                    Postleitzahl=worksheet.cell_value(curr_row, curr_cell)
                except:
                    arcpy.AddError("Dateneingabe unvollständig - Postleitzahl fehlt")
                    exit(1)
                    pass

                curr_cell += 1

                try:
                    row.Ort=worksheet.cell_value(curr_row, curr_cell)
                    Ort=worksheet.cell_value(curr_row, curr_cell)
                except:
                    arcpy.AddError("Dateneingabe unvollständig - Ort fehlt")
                    exit(1)
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
                    arcpy.AddError("Dateneingabe unvollständig - Strasse fehlt")
                    exit(1)
                    pass

                curr_cell += 1

                try:
                    row.HNR=str(worksheet.cell_value(curr_row, curr_cell)).replace('.0','')
                    Hausnummer=worksheet.cell_value(curr_row, curr_cell)
                except:
                    pass

                curr_cell += 1

                try:
                    row.VKFL_Gesamt=worksheet.cell_value(curr_row, curr_cell)
                    VKFL=worksheet.cell_value(curr_row, curr_cell)
                except:
                    arcpy.AddError("Dateneingabe unvollständig oder falsches Format - Verkaufsflaeche fehlt")
                    exit(1)
                    pass

                curr_cell += 1

                try:
                    row.Euro_pro_quadratmeter_VKF=worksheet.cell_value(curr_row, curr_cell)
                except:
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
                    #arcpy.AddMessage(float(worksheet.cell_value(curr_row, curr_cell)))
                    row.Lat=float(worksheet.cell_value(curr_row, curr_cell))
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

                curr_cell += 1

                try:
                    row.EW_Gemeindeverband=worksheet.cell_value(curr_row, curr_cell)
                except:
                    pass

                curr_cell += 1

                try:
                    row.Kaufkraft=worksheet.cell_value(curr_row, curr_cell)
                except:
                    pass

                curr_cell += 1

                try:
                    row.Betriebstyp_Attraktivitaet=worksheet.cell_value(curr_row, curr_cell)
                except:
                    pass

                curr_cell += 1

                try:
                    row.Betriebstyp_Funktion=worksheet.cell_value(curr_row, curr_cell)
                except:
                    pass




                if     Betriebstyp=="" or   Strasse=="" or   Ort=="" or  Postleitzahl=="" or  VKFL=="":
                    arcpy.AddError("Wichtige Eingabeinformation fehlt !")
                    arcpy.AddError("Ueberprufen sie Zeile "+ str(counter))
                    exit(1)

                row.shape = pnt
                cur.insertRow(row)

    del cur,row,gdb,workbook,worksheet

def georeferenz():
    counter=0
    cur_Standorte_temp=arcpy.UpdateCursor(os.path.join(workspace_projekt,"Standorte_temp"))
    arcpy.AddMessage("Georeferenzieren der Feature")
    for zeile in cur_Standorte_temp:


        if zeile.Lat ==None or zeile.Lon ==None or zeile.Lat==0 or zeile.Lon==0:
            pnt = arcpy.CreateObject("Point")
            counter=zeile.Id
            if (counter%50)==0:
                arcpy.AddMessage(str(counter)+" Features georeferenziert.")
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
            url ='http://query.yahooapis.com/v1/public/yql?q=select * from geo.placefinder where house="'+house+'" and street="'+Strasse+'" and city="'+str(Ort)+'" and country="Germany" and postal="'+str(postcode)+'"&appid=hxByDcDV34HxMu78xKN0b33dXezfkwQskuSVJ9PTUKswLDUaVicYpMWGQScmliWv7IP7SEgQKrlvWC7v1jbcU8gZJU62HTk'
    ##                    arcpy.AddMessage( url)
            time.sleep(0.1)
            [lat,longi,a]=gibmirxy(url)
            ##print lat,longi,a

            if lat==0 and longi==0 and a==0:
                arcpy.AddError( url)
                arcpy.AddError("\n\n\n\nFehler: ")
                arcpy.AddError("Georeferenzierung derzeit nicht moeglich - Georeferenzierungswebsite down bzw. mit Verbindungsproblemen.")
                arcpy.AddError("Bitte versuchen sie es spaeter erneut.\n")

                exit(1)
            if int(a)<85:


                arcpy.AddMessage( "Georeferenzierung Unter 85 % Qualitaet - erneute Abfrage mit anderen Variablen")

                url ='http://query.yahooapis.com/v1/public/yql?q=select * from geo.placefinder where house="'+house+'" and street="'+Strasse+'"and state="'+str(state)+'" and country="Germany" and postal="'+str(postcode)+'"&appid=hxByDcDV34HxMu78xKN0b33dXezfkwQskuSVJ9PTUKswLDUaVicYpMWGQScmliWv7IP7SEgQKrlvWC7v1jbcU8gZJU62HTk'
    ##                        arcpy.AddMessage( url)
            ##    print url
                [lat,longi,a]=gibmirxy(url)
    ##                    arcpy.AddMessage( str(lat)+" "+ str(longi)+ " "+a)
            if int(a)<85:

                Ort = Ort.split('-')[0]
                arcpy.AddMessage( "Georeferenzierung unter 85 % Qualitaet - erneute Abfrage mit anderen Variablen")

                url ='http://query.yahooapis.com/v1/public/yql?q=select * from geo.placefinder where house="'+house+'" and street="'+Strasse+'" and city="'+str(Ort)+'"and state="'+state+'" and country="Germany" and postal="'+str(postcode)+'"&appid=hxByDcDV34HxMu78xKN0b33dXezfkwQskuSVJ9PTUKswLDUaVicYpMWGQScmliWv7IP7SEgQKrlvWC7v1jbcU8gZJU62HTk'
    ##                        arcpy.AddMessage( url)
            ##    print url
                [lat,longi,a]=gibmirxy(url)
            ##    print lat,longi,a
            if int(a)<85:

                Ort = state
                arcpy.AddMessage( "Georeferenzierung unter 85 % Qualitaet - erneute Abfrage mit anderen Variablen Typ 2 \n")

                url ='http://query.yahooapis.com/v1/public/yql?q=select * from geo.placefinder where house="'+house+'" and street="'+Strasse+'" and city="'+str(Ort)+'" and country="Germany" and postal="'+str(postcode)+'"&appid=hxByDcDV34HxMu78xKN0b33dXezfkwQskuSVJ9PTUKswLDUaVicYpMWGQScmliWv7IP7SEgQKrlvWC7v1jbcU8gZJU62HTk'
                arcpy.AddMessage( url)
            ##    print url
                [lat,longi,a]=gibmirxy(url)

            if int(a)<84:
                arcpy.AddError( "\n\nNoch immer unter 85 % Quali bitte Lat und Lon Koordinaten WGS84 in der Datei Bestandsliste_Supermaerkte.xls angeben.")
                arcpy.AddError( "Diese Georeferenzierung wird dann verwendet.")
                arcpy.AddError( "\n\n\nABBRUCH DES VORGANGS\n\n\n")
                exit(1)

            if lat==0 and longi==0 and a==0:
                arcpy.AddError( url)
                arcpy.AddError("\n\n\n\nFehler: ")
                arcpy.AddError("Georeferenzierung derzeit nicht moeglich - Georeferenzierungswebsite down bzw. mit Verbindungsproblemen.")
                arcpy.AddError("Bitte versuchen sie es spaeter erneut.\n")

                exit(1)

            pnt.X=float(longi)
            pnt.Y=float(lat)

            zeile.Lat=float(lat)
            zeile.Lon=float(longi)
            zeile.Qualitaet=int(a)


            zeile.shape = pnt
            cur_Standorte_temp.updateRow(zeile)

    del cur_Standorte_temp

def projektzieren():
    input_features = os.path.join( workspace_projekt,"Standorte_temp")
    output_features_class = os.path.join(workspace_projekt,"Standortdaten")


    out_coordinate_system=arcpy.SpatialReference('ETRS 1989 UTM Zone N32')

    arcpy.Project_management(input_features, output_features_class, out_coordinate_system)
    ##arcpy.AddMessage(arcpy.GetMessages())
    del input_features,output_features_class,out_coordinate_system
    arcpy.AlterAliasName(os.path.join(workspace_projekt,"Standortdaten"), 'Standortdaten')

##    try:
##        if arcpy.Exists("Standorte_temp"):
##            arcpy.Delete_management("Standorte_temp")
##    except:
##        arcpy.AddMessage("Fehler beim Loeschen des Tempfiles ")
def punktlayerzumprojekt():
#   Punktlayer zum Porjekt kopieren - vorher alten punktlayer löschen im projekt und neuen hinzufügen
    try:
        arcpy.Delete_management(os.path.join(workspace_projekt,"Punktlayer_Bev"))
    except:
            print "nicht vorhanden"
            pass

    try:
        arcpy.Project_management(os.path.join(pfadPunktlayer), os.path.join(workspace_projekt,"Punktlayer_Bev"), "PROJCS['WGS_1984_UTM_Zone_32N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',9.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]", "", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433],METADATA['World',-180.0,-90.0,180.0,90.0,0.0,0.0174532925199433,0.0,1262]]")
##        arcpy.CopyFeatures_management(os.path.join(pfadPunktlayer),os.path.join(workspace_projekt,"Punktlayer_Bev"))

    except:
        a="Punktlayer konnte dem Projekt nicht hinzugefuegt werden."
        b="Bitte wiederholen Sie den Vorgang."
        print a , b

        arcpy.AddError(a)
        arcpy.AddError(b)
        exit(1)



projektname = arcpy.GetParameterAsText(0)
pfadderExcel = arcpy.GetParameterAsText(1)
pfadPunktlayer = arcpy.GetParameterAsText(2)
#Pfade einrichten
base_path = str(sys.path[0]).split("2_Tool")[0]

workspace_projekt = os.path.join(base_path, '3_Projekte', projektname,
                                 'FGDB_34_Standortkonkurrenz_Supermaerkte_' + projektname + '.gdb')


arcpy.env.workspace=workspace_projekt
arcpy.env.overwriteOutput = True


xlsladen_undStandorteerstellen(pfadderExcel)
georeferenz()
projektzieren()
punktlayerzumprojekt()



del projektname,pfadderExcel,workspace_projekt,base_path,pfadPunktlayer

gc.collect()

print "done"
arcpy.AddMessage("\nErfolgreich beendet\n\n")

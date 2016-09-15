# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 05_Ergebnissammler.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# HCU Hamburg
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


import os
import imp
import csv
import sys
import datetime

import arcpy
import xlsxwriter

# import sheet_lib as sl
sheetlibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','sheet_lib.py'))
sl = imp.load_source('sheet_lib', sheetlibpath)

projektname = str(arcpy.GetParameterAsText(0))


base_path = str(sys.path[0]).split("2_Tool")[0]
workspace_projekt = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt_'+projektname+'.gdb')
workspace_texte_erlaeterung = os.path.join(base_path,'2_Tool','D_Erreichbarkeit','Erlaeuterungstexte')
workspace_projekt_ergebnisse = os.path.join(base_path,'3_Projekte',projektname, 'Ergebnisausgabe', 'Abbildungen')
workspace_wertveraenderung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_Standortkonkurrenz_Supermaerkte_'+projektname+'.gdb')

arcpy.env.workspace = workspace_projekt
arcpy.env.overwriteOutput = True
#========================================================================================================================================
def erstelle_DichtesteEntfernung():

    if  arcpy.Exists(os.path.join(workspace_wertveraenderung,"Distanzmatrix"))==False or arcpy.Exists(os.path.join(workspace_wertveraenderung,"Distanzmatrix_planfall"))==False or arcpy.Exists(  os.path.join(workspace_wertveraenderung,"Siedlungszahlendaten"))==False:
        return -1

    cur_Search_Distanzm=arcpy.SearchCursor(os.path.join(workspace_wertveraenderung,"Distanzmatrix"))
    cur_Search_Distanzm_plan=arcpy.SearchCursor(os.path.join(workspace_wertveraenderung,"Distanzmatrix_planfall"))
    cur_Siedlungszellen=arcpy.UpdateCursor(os.path.join(workspace_wertveraenderung,"Siedlungszahlendaten"))

    try:
        arcpy.DeleteField_management(os.path.join(workspace_wertveraenderung,"Siedlungszahlendaten"),"d_Dist")
    except:
##        arcpy.AddMessage("Eroor1")
        pass
    try:
        arcpy.AddField_management(os.path.join(workspace_wertveraenderung,"Siedlungszahlendaten"), "d_Dist", "DOUBLE")
    except:
##        arcpy.AddMessage("Eroo2")
        pass


    #nun such fuer alle siedlungszellen die dichteste Distanz zu dem naechst dichten markt

    fieldnames = [f.name for f in arcpy.ListFields(os.path.join(workspace_wertveraenderung,"Distanzmatrix"))]
    fieldnames = fieldnames[2:]
##    print fieldnames

    vektor_d_dicht_vor=[]

    for zeilen in cur_Search_Distanzm:
        dist=999999
        for spalten in fieldnames:
            if dist > zeilen.getValue(spalten) and zeilen.getValue(spalten)!=0.:
                dist =zeilen.getValue(spalten)
        if dist==999999:
            dist=0
        vektor_d_dicht_vor.append([zeilen.Siedlungsid,dist])

##    print vektor_d_dicht_vor
##    print len(vektor_d_dicht_vor)




    fieldnames_nach = [f.name for f in arcpy.ListFields(os.path.join(workspace_wertveraenderung,"Distanzmatrix_planfall"))]
    fieldnames_nach = fieldnames_nach[2:]


    vektor_d_dicht_nach=[]

    for zeilen in cur_Search_Distanzm_plan:
        dist=999999
        for spalten in fieldnames_nach:
            if dist > zeilen.getValue(spalten) and zeilen.getValue(spalten)!=0.:
                dist =zeilen.getValue(spalten)
        if dist==999999:
            dist=0
        vektor_d_dicht_nach.append([zeilen.Siedlungsid,dist])

##    print vektor_d_dicht_nach
##    print len(vektor_d_dicht_nach)


    diff_Dist_veraenderung=[]
    for zeilen_1 in vektor_d_dicht_vor:
        found=0
        for zeilen_2 in vektor_d_dicht_nach:
            if zeilen_1[0]==zeilen_2[0]:
                found=1
                diff = ( zeilen_1[1]-zeilen_2[1])*1000.

                diff_Dist_veraenderung.append([zeilen_1[0],diff])
##                if diff >0:
##                    print ( zeilen_1[1]-zeilen_2[1])
##                    print ( zeilen_1[1]-zeilen_2[1])*1000.
##                    print float (( zeilen_1[1]-zeilen_2[1])*1000.)
##                    a = "%.2f" % float (( zeilen_1[1]-zeilen_2[1])*1000.)
##                    print "%.2f" % float (( zeilen_1[1]-zeilen_2[1])*1000.)
##                    print float(a)

                break
        if found==0:
            print "sehr komisch hier fehlt ne Siedlungszelle"



    for zeile in cur_Siedlungszellen:
        gefunden=0
        for eintraege in diff_Dist_veraenderung:
            if zeile.SZ_ID == eintraege[0]:
                gefunden=1
                a = "%.2f" % (eintraege[1])
                zeile.setValue("d_Dist",float(a))
                cur_Siedlungszellen.updateRow(zeile)
                break

        if gefunden==0:
            zeile.d_Dist=0
            cur_Siedlungszellen.updateRow(zeile)
            print "sollte nicht vorkommen aber nicht gefunden"

    del cur_Search_Distanzm,cur_Siedlungszellen,fieldnames
    return 0

def check_planungsflaeche():
    cur_Search=arcpy.SearchCursor(os.path.join(workspace_projekt,"Flaechenbilanz"))
    typus=0
    for a in cur_Search:
        print a.Flaechennutzung_S2
        if a.Flaechennutzung_S2=="Gemeinbedarfsflaeche" and typus<1:
            typus=1
        if a.Flaechennutzung_S2=="Nettowohnbauland" and typus<2:
            typus=2
        if a.Flaechennutzung_S2=="Einzelhandel" and typus<3:
            typus=3
        if "Gewerbeflaeche" in a.Flaechennutzung_S2 and typus<4:
            typus=4

    del cur_Search

    return typus

# ##########################################################################################################################
schrittmeldung = 'Datenexport in Excel-Datei  \n'
arcpy.AddMessage(schrittmeldung)
print schrittmeldung

#############################################################################################################
# 1. Dokument einrichten

# Pfade setzen
logo = os.path.join((str(sys.path[0]).split("2_Tool")[0]),"1_Basisdaten","logo_rpc.png")
ausgabeordner = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Excel')
excelpfad = os.path.join(ausgabeordner,'37_Erreichbarkeit.xlsx')

try:
    os.remove(excelpfad)
except:
    pass

# Workbook und Tabellenblaetter anlegen
wb = xlsxwriter.Workbook(excelpfad)
sl.infosheet(projektname, str("Erreichbarkeit"), wb)


# Styles anlegen
head = wb.add_format({'bold': True, 'font_size': '24', 'align': 'left','valign': 'vcenter', 'bg_color': 'white', 'border': '0'})
normal = wb.add_format({'font_size': '14', 'bg_color': 'white', 'border': '0'})
rechts = wb.add_format({'font_size': '14', 'align' : 'right', 'bg_color': 'white', 'border': '0'})
bold = wb.add_format({'bold': True, 'font_size': '14', 'bg_color': 'white', 'border': '0'})
bold_rechts = wb.add_format({'bold': True, 'font_size': '14', 'bg_color': 'white', 'border': '0', 'align' : 'right'})

background = wb.add_format({'bg_color': 'white', 'border': '0'})

#====================================================================================================================
#========================================================================================================================================
Nutzungstyp= check_planungsflaeche()
##arcpy.AddMessage(   Nutzungstyp)

if Nutzungstyp==0:
    a="Keine Ausgabe, da nur kein Planvorhaben angegeben ist."
    print a
    arcpy.AddError(a)
elif Nutzungstyp==1:
    a="Keine Ausgabe, da nur Gemeindebedarfsflaeche als Planvorhaben angegeben ist."
    print a
    arcpy.AddError(a)
elif Nutzungstyp==3 or Nutzungstyp==4:

    if Nutzungstyp==3:
        if erstelle_DichtesteEntfernung()==0:

            #Kopiere Template.mxd
            mxd_template = arcpy.mapping.MapDocument(os.path.join(base_path, "2_Tool","37_Erreichbarkeit","37_Template_Kartenerzeugung","37_Distanzen_Template.mxd"))
            mxdpfad = os.path.join(workspace_projekt_ergebnisse,'37_Distanzen.mxd')
            mxd_template.saveACopy(mxdpfad)

            # Ersetze Datenquelle
            Haltestellen_mxd = arcpy.mapping.MapDocument(mxdpfad)
            templatepath = os.path.join(base_path,"2_Tool","37_Erreichbarkeit","37_Template_Kartenerzeugung","template.gdb")
            resultpath = os.path.join(base_path,"3_Projekte",projektname,"FGDB_34_Standortkonkurrenz_Supermaerkte_"+projektname+".gdb")
            Haltestellen_mxd.findAndReplaceWorkspacePaths(templatepath, resultpath)


            # Setze Viewport neu
            df = arcpy.mapping.ListDataFrames(Haltestellen_mxd)[0]
            gebietLayer = arcpy.mapping.ListLayers(Haltestellen_mxd, "Siedlungszahlendaten", df)[0]

            ##print gebietLayer
            ##arcpy.SelectLayerByAttribute_management(gebietLayer, "NEW_SELECTION", "\"OBJECTID\" > 0")
            arcpy.SelectLayerByLocation_management(gebietLayer, "WITHIN_A_DISTANCE", os.path.join(workspace_wertveraenderung,"Neuer_Markt"), "1 Kilometers", "NEW_SELECTION")
            df.extent = gebietLayer.getSelectedExtent(False)
            arcpy.SelectLayerByAttribute_management(gebietLayer, "CLEAR_SELECTION")
            df.scale = df.scale * 2.5


            arcpy.RefreshActiveView()
            Haltestellen_mxd.save()
            del mxd_template , df,mxdpfad,templatepath,resultpath,gebietLayer

            #Exportiere Ergebnis
            arcpy.mapping.ExportToJPEG(Haltestellen_mxd, os.path.join(workspace_projekt_ergebnisse, "37_Distanz_veraenderung.jpg"), "PAGE_LAYOUT",resolution=300)

            schrittmeldung = 'Uebersichtskarte mit Differenzveraenderung erstellt \n'
            arcpy.AddMessage(schrittmeldung)
            print schrittmeldung

            del Haltestellen_mxd

        else:
            a="Toolpaket 34_Standortkonkurrenz_Supermaerkte nicht vollstaendig. Bitte starten Sie 34_Standortkonkurrenz_Supermaerkte erneut."
            print a
            arcpy.AddMessage(a)
            try:
                arcpy.Delete_management(os.path.join(workspace_projekt_ergebnisse, "37_Distanz_veraenderung.jpg"))
            except:
                pass

    #==================================================================================================================================================================================
    schrittmeldung = 'Grafiken erstellen  \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung
    #==================================================================================================================================================================================
##    arcpy.AddMessage(Nutzungstyp)
    if Nutzungstyp==3 and arcpy.Exists(os.path.join(workspace_projekt_ergebnisse, "37_Distanz_veraenderung.jpg")):
        #Einzelhandel
        ws11 = wb.add_worksheet('Methodik_')
        # Hintergrund weiss faerben
        for x in range(0,200):
            for y in range(0,200):
                ws11.write(x,y,"", background)

        # Pfade zu Grafiken herstellen
        Text1 = os.path.join(workspace_texte_erlaeterung, 'Methodik_ErreichbarkeitEinzelhandel.png')
        ###Grafiken einfügen
        ws11.insert_image(0, 0, Text1, {'x_scale': 0.32, 'y_scale': 0.32})

        ws12 = wb.add_worksheet('Karte Distanz_Maerkte')
        # Hintergrund weiss faerben
        for x in range(0,300):
            for y in range(0,300):
                ws12.write(x,y,"", background)

        # Pfade zu Grafiken herstellen
        image1 = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Abbildungen', "37_Distanz_veraenderung.jpg")
        ###Grafiken einfügen
        ws12.write(2, 1, "Veraenderung der Entfernung zum naechsten Markt insgesamt".decode('utf-8'), bold)
        ws12.insert_image('B4', image1, {'x_scale': 0.32, 'y_scale': 0.32})
        del image1


        #statistik berechnen - wie die veraenderung ausfaellt
        cur_Siedlungszellen=arcpy.SearchCursor(os.path.join(workspace_wertveraenderung,"Siedlungszahlendaten"))

        arra_Siedlung=[]
        for a in cur_Siedlungszellen:
            arra_Siedlung.append([int(a.SZ_Einwohner),a.d_Dist])

        del cur_Siedlungszellen,a

        array_u1500_neg=[]
        array_750bis1500_neg=[]
        array_250bis750_neg=[]
        array_250bis0_neg=[]
        array_0bis250_pos=[]
        array_250bis750_pos=[]
        array_750bis1500_pos=[]
        array_u1500_pos=[]

        for  a in arra_Siedlung:
            if a[1]< -1500:
                array_u1500_neg.append(a)
            elif a[1]<-750 and a[1]>=-1500:
                array_750bis1500_neg.append(a)
            elif a[1]<-250 and a[1]>=-750:
                array_250bis750_neg.append(a)
            elif a[1]>=-250 and a[1]<0:
                array_250bis0_neg.append(a)
            elif a[1]>0 and a[1]<=250:
                array_0bis250_pos.append(a)
            elif a[1]>250 and a[1]<=750:
                array_250bis750_pos.append(a)
            elif a[1]>750 and a[1]<=1500:
                array_750bis1500_pos.append(a)
            elif a[1]>1500 :
                array_u1500_pos.append(a)

        if len(array_u1500_neg)>0:
            b=0
            c=0
            for a in array_u1500_neg:
                b+=a[0] #Einwohner
                c+=a[1] #Distanz

            c=c/len(array_u1500_neg)
            del array_u1500_neg
            array_u1500_neg=[b,c]
        else:
            del array_u1500_neg
            array_u1500_neg=[0,0]
        if len(array_750bis1500_neg)>0:
            b=0
            c=0
            for a in array_750bis1500_neg:
                b+=a[0] #Einwohner
                c+=a[1] #Distanz

            c=c/len(array_750bis1500_neg)
            del array_750bis1500_neg
            array_750bis1500_neg=[b,c]
        else:
            del array_750bis1500_neg
            array_750bis1500_neg=[0,0]
        if len(array_250bis750_neg)>0:
            b=0
            c=0
            for a in array_250bis750_neg:
                b+=a[0] #Einwohner
                c+=a[1] #Distanz

            c=c/len(array_250bis750_neg)
            del array_250bis750_neg
            array_250bis750_neg=[b,c]
        else:
            del array_250bis750_neg
            array_250bis750_neg=[0,0]

        if len(array_250bis0_neg)>0:
            b=0
            c=0
            for a in array_250bis0_neg:
                b+=a[0] #Einwohner
                c+=a[1] #Distanz

            c=c/len(array_250bis0_neg)
            del array_250bis0_neg
            array_250bis0_neg=[b,c]
        else:
            del array_250bis0_neg
            array_250bis0_neg=[0,0]
        if len(array_0bis250_pos)>0:
            b=0
            c=0
            for a in array_0bis250_pos:
                b+=a[0] #Einwohner
                c+=a[1] #Distanz

            c=c/len(array_0bis250_pos)
            del array_0bis250_pos
            array_0bis250_pos=[b,c]
        else:
            del array_0bis250_pos
            array_0bis250_pos=[0,0]
        if len(array_250bis750_pos)>0:
            b=0
            c=0
            for a in array_250bis750_pos:
                b+=a[0] #Einwohner
                c+=a[1] #Distanz

            c=c/len(array_250bis750_pos)
            del array_250bis750_pos
            array_250bis750_pos=[b,c]
        else:
            del array_250bis750_pos
            array_250bis750_pos=[0,0]
        if len(array_750bis1500_pos)>0:
            b=0
            c=0
            for a in array_750bis1500_pos:
                b+=a[0] #Einwohner
                c+=a[1] #Distanz

            c=c/len(array_750bis1500_pos)
            del array_750bis1500_pos
            array_750bis1500_pos=[b,c]
        else:
            del array_750bis1500_pos
            array_750bis1500_pos=[0,0]
        if len(array_u1500_pos)>0:
            b=0
            c=0
            for a in array_u1500_pos:
                b+=a[0] #Einwohner
                c+=a[1] #Distanz

            c=c/len(array_u1500_pos)
            del array_u1500_pos
            array_u1500_pos=[b,c]
        else:
            del array_u1500_pos
            array_u1500_pos=[0,0]

        ws12.set_column(1, 1, 50)
        ws12.set_column(1, 2, 26)
        ws12.set_column(1, 3, 50)
        ws12.write(44,1, "Statistische Veraenderung der Entfernung zum naechsten Markt".decode('utf-8'), bold)
        ws12.write(46,1, "Entfernungen in Meter".decode('utf-8'), bold)
        ws12.write(46,2, "Anzahl der Einwohner".decode('utf-8'), bold)
        ws12.write(46,3, "Durchschnittliche neue Entfernung in Meter".decode('utf-8'), bold)
        oui=46
        oui=oui+1
        print type(array_u1500_neg[1])
        ws12.write(oui,1, "mehr als 1.500m Zunahme".decode('utf-8') )
        ws12.write(oui,2,  str(array_u1500_neg[0]).decode('utf-8'))
        try:
            ws12.write(oui,3, str("%.2f" % array_u1500_neg[1]).decode('utf-8'))
        except:
            ws12.write(oui,3, str(0).decode('utf-8'))

        oui=oui+1
        ws12.write(oui,1, "750 bis 1.500m Zunahme".decode('utf-8') )
        ws12.write(oui,2, str(array_750bis1500_neg[0]).decode('utf-8'))
        try:
            ws12.write(oui,3, str("%.2f" % array_750bis1500_neg[1]).decode('utf-8'))
        except:
            ws12.write(oui,3, str(0).decode('utf-8'))

        oui=oui+1
        ws12.write(oui,1, "250 bis 750m Zunahme".decode('utf-8') )
        ws12.write(oui,2, str(array_250bis750_neg[0]).decode('utf-8'))
        try:
            ws12.write(oui,3,str("%.2f" %array_250bis750_neg[1]).decode('utf-8'))
        except:
            ws12.write(oui,3, str(0).decode('utf-8'))

        oui=oui+1
        ws12.write(oui,1, "Zunahme bis zu 250m".decode('utf-8') )
        ws12.write(oui,2, str(array_250bis0_neg[0]).decode('utf-8'))
        try:
            ws12.write(oui,3,str("%.2f" %array_250bis0_neg[1]).decode('utf-8'))
        except:
            ws12.write(oui,3, str(0).decode('utf-8'))

        oui=oui+1
        ws12.write(oui,1, "Abnahme bis zu 250m".decode('utf-8') )
        ws12.write(oui,2, str(array_0bis250_pos[0]).decode('utf-8'))
        try:
            ws12.write(oui,3,str("%.2f" %array_0bis250_pos[1]).decode('utf-8'))
        except:
            ws12.write(oui,3, str(0).decode('utf-8'))

        oui=oui+1
        ws12.write(oui,1, "250 bis 750m Abnahme".decode('utf-8') )
        ws12.write(oui,2, str(array_250bis750_pos[0]).decode('utf-8'))
        try:
            ws12.write(oui,3, str("%.2f" %array_250bis750_pos[1]).decode('utf-8'))
        except:
            ws12.write(oui,3, str(0).decode('utf-8'))

        oui=oui+1
        ws12.write(oui,1, "750 bis 1.500m Abnahme".decode('utf-8') )
        ws12.write(oui,2, str(array_750bis1500_pos[0]).decode('utf-8'))
        try:
            ws12.write(oui,3, str("%.2f" %array_750bis1500_pos[1]).decode('utf-8'))
        except:
            ws12.write(oui,3, str(0).decode('utf-8'))

        oui=oui+1
        ws12.write(oui,1, "mehr als 1.500m Abnahme".decode('utf-8') )
        ws12.write(oui,2, str(array_u1500_pos[0]).decode('utf-8'))
        try:
            ws12.write(oui,3,str("%.2f" %array_u1500_pos[1]).decode('utf-8'))
        except:
            ws12.write(oui,3, str(0).decode('utf-8'))



        oui=oui+2
        ws12.write(oui,1,"Grundlage der Berechnungen sind Luftliniendistanzen unter Beruecksichtigung eines Ungenauigkeitsfaktors. Aus technischen Gruenden ist ein auf dem Strassennetz")
        ws12.write(oui+1,1,"basiertes Routing nicht moeglich. In der Naehe von Fluessen, groesseren Gebirgszuegen oder Naturschutzgebieten, die nur eingeschraenkt ueberwunden oder durchquert")
        ws12.write(oui+2,1,"werden koennen, kann dies unter Umstaenden zu Ungenauigkeiten in den Ergebnissen fuehren.")

    #==================================================================================================================================================================================
    else:
        ws1 = wb.add_worksheet('Methodik_')
        # Hintergrund weiss faerben
        for x in range(0,200):
            for y in range(0,200):
                ws1.write(x,y,"", background)

        # Pfade zu Grafiken herstellen
        Text1 = os.path.join(workspace_texte_erlaeterung, 'Methodik_ErreichbarkeitGewerbe.png')
        ###Grafiken einfügen
        ws1.insert_image(0, 0, Text1, {'x_scale': 0.32, 'y_scale': 0.32})
        del Text1
        #=====================================================================================================================



    # ############################################################################################################
    ws2 = wb.add_worksheet('Auswertung_Anbindung')
    ws2.set_column(1, 1, 60)
    ws2.set_column(2, 2, 30)
    ws2.set_column(3, 3, 25)
    ws2.set_column(4, 4, 22)
    ws2.set_column(5, 5, 50)

    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws2.write(x,y,"", background)

    # 2.Ergebnisse aus Erreichbarkeit Zentral Orte einlesen und schreiben

    today = datetime.date.today()
    nextmonday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
    abfahrt_min = []
    orte = []
    dauer_min = []
    umsteigen_min = []
    verkehrsmittel_min = []

    with open(os.path.join(workspace_projekt_ergebnisse,"Zentrale_Orte_temp.csv"), 'rb') as f:
        mycsv = csv.reader(f)
        for row in mycsv:
            abfahrt_min.append(row[0])
            orte.append(row[1])
            dauer_min.append(row[2])
            umsteigen_min.append(row[3])
            verkehrsmittel_min.append(row[4])
        del row, mycsv
        print abfahrt_min, orte, dauer_min, umsteigen_min, verkehrsmittel_min

    i=7
    n=0
    ws2.write(2, 1, "Erreichbarkeit ausgewaehlter Mittel- & Oberzentren mit dem OEPNV".decode('utf-8'), bold)
    ws2.write(3, 1, "Schnellste Verbindung, ermittelt durch Zugriff auf die Fahrplanauskunft der Deutschen Bahn".decode('utf-8'))
    ws2.write(4, 1, "Abgefragt fuer den ".decode('utf-8')+str(nextmonday.day)+"."+str(nextmonday.month)+"."+str(nextmonday.year)+" im Zeitraum zwischen 7 - 19 Uhr")
    ws2.write(6, 1, "Abfahrt (naechstgelegene Haltestelle)".decode('utf-8'), bold)
    ws2.write(6, 2, 'Ziel', bold)
    ws2.write(6, 3, 'Fahrtzeit in Minuten', bold_rechts)
    ws2.write(6, 4, 'Anzahl Umstiege', bold_rechts)
    ws2.write(6, 5, 'Verkehrsmittel', bold_rechts)
    for ort in orte:
        ws2.write(i, 1, abfahrt_min[n].decode('latin1'), normal)
        ws2.write(i, 2, ort.decode('utf-8'), normal)
        ws2.write(i, 3, dauer_min[n], rechts)
        ws2.write(i, 4, umsteigen_min[n], rechts)
        ws2.write(i, 5, verkehrsmittel_min[n], rechts)
        i+=1
        n+=1

    # ############################################################################################################
    ws31 = wb.add_worksheet('Methodik_Haltestellen')
    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws31.write(x,y,"", background)

    # Pfade zu Grafiken herstellen
    Text1 = os.path.join(workspace_texte_erlaeterung, 'Methodik_ErreichbarkeitWohnenAnbindungsqualitaet.png')
    ###Grafiken einfügen
    ws31.insert_image(0, 0, Text1, {'x_scale': 0.32, 'y_scale': 0.32})
    del Text1
    # ################################################################################################################
    # 3.Karte mit den Haltestellen in der Umgebung einfuegen

    ws3 = wb.add_worksheet("Karte_Haltestellen")

    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws3.write(x,y,"", background)

    ws3.write(1, 1, "Uebersichtskarte mit allen Haltestellen im Umkreis von 500m / 1.000m um das Projektgebiet".decode('utf-8'), bold)
    ws3.write(2, 1, "Ermittelt durch Zugriff auf die Fahrplanauskunft der Deutschen Bahn.")
    image = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Abbildungen', "37_Karte_Haltestellen.jpg")
    ws3.insert_image('B5', image, {'x_scale': 0.75, 'y_scale': 0.75})
    del image

    #############################################################################################################
    # 4.Diagramme und Daten aus Erreichbarkeit OePNV einlesen und schreiben

    name = []
    style = []
    datum = []
    name_long = []

    with open(os.path.join(workspace_projekt_ergebnisse,"Haltestellen.csv"), 'rb') as f:
        mycsv = csv.reader(f)
        for row in mycsv:
            name.append(row[0])
            style.append(row[1])
            datum.append(row[2])
            name_long.append(row[3])
        del row, mycsv
        print name, style, datum

    i=1
    for n in name:
        ws4 = wb.add_worksheet("Auswertung_Haltestelle0"+str(i)) #Excel-Sheet-Benennung =|= Haltestellenname zur Vermeidung von Codierungskonflikten

        # Hintergrund weiss faerben
        for x in range(0,200):
            for y in range(0,200):
                ws4.write(x,y,"", background)

        barcode = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Abbildungen', n+".png")
        if os.path.isfile(barcode):
            ws4.write(1, 1, "Visualisierung der OEPNV-Taktung an der Haltestelle ".decode('utf-8') + name_long[i-1].decode('latin-1'), bold)
            ws4.write(2, 1, "Ermittelt durch Zugriff auf die Fahrplanauskunft der Deutschen Bahn. Abgefragt fuer den ".decode('utf-8') + datum[i-1])
            if style[i-1] == "1":
                ws4.write(3, 1, "Farbliche Unterscheidung nach Art des Verkehrstraegers".decode('utf-8'))
            elif style[i-1] == "2":
                ws4.write(3, 1, "Farbliche Unterscheidung nach Fahrtziel".decode('utf-8'))
            elif style[i-1] == "3":
                ws4.write(3, 1, "Farbliche Unterscheidung nach OEPNV-Linie".decode('utf-8'))
            elif style[i-1] == "4":
                ws4.write(3, 1, "Linie mit der dichtesten Taktung farblich hervorgehoben".decode('utf-8'))
            ws4.insert_image('B6', barcode, {'x_scale': 0.3, 'y_scale': 0.3})
        else:
            pass
        i+=1
    del i, barcode
    ###### ###############################################################################################################################################
##    ws16 = wb.add_worksheet('Literatur')
##
##    # Pfade zu Grafiken herstellen
##    Text1 = os.path.join(workspace_texte_erlaeterung, 'Methodik_ErreichbarkeitWohnenLiteratur.png')
##    ###Grafiken einfügen
##    ws16.insert_image(0, 0, Text1, {'x_scale': 0.32, 'y_scale': 0.32})
##
##    del Text1


    #Workbook speichern
    try:
        wb.close()
    except IOError:
    	schrittmeldung = 'ACHTUNG \nDie Ergebnisstabelle konnte nicht gespreichert werden, da eine aeltere Version der Datei momentan in Excel geoeffnet ist. Bitte schliessen Sie diese Tabelle und fuehren Sie den Arbeitsschritt erneut aus. \n'
    	arcpy.AddError(schrittmeldung)
    	print schrittmeldung
        exit(1)








#kann nur noch Nettowohnen sein
else :
    #==================================================================================================================================================================================
    schrittmeldung = 'Grafiken erstellen  \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung
    #==================================================================================================================================================================================


    #Kopiere Template.mxd
    mxd_template = arcpy.mapping.MapDocument(os.path.join(base_path, "2_Tool","37_Erreichbarkeit","37_Template_Kartenerzeugung","37_Erreichbarkeit_Fahrrad_Template.mxd"))
    mxdpfad = os.path.join(workspace_projekt_ergebnisse,'37_Erreichbarkeit_Fahrrad.mxd')
    mxd_template.saveACopy(mxdpfad)

    # Ersetze Datenquelle
    Haltestellen_mxd = arcpy.mapping.MapDocument(mxdpfad)
    templatepath = os.path.join(base_path,"2_Tool","37_Erreichbarkeit","37_Template_Kartenerzeugung","template.gdb")
    resultpath = os.path.join(base_path,"3_Projekte",projektname,"FGDB_37_Erreichbarkeit_Projekt_"+projektname+".gdb")
    Haltestellen_mxd.findAndReplaceWorkspacePaths(templatepath, resultpath)


    # Setze Viewport neu
    df = arcpy.mapping.ListDataFrames(Haltestellen_mxd)[0]
    gebietLayer = arcpy.mapping.ListLayers(Haltestellen_mxd, "Buffer_1000_m_500_m_", df)[0]
    arcpy.SelectLayerByAttribute_management(gebietLayer, "NEW_SELECTION", "\"OBJECTID\" > 0")
    df.extent = gebietLayer.getSelectedExtent(False)
    arcpy.SelectLayerByAttribute_management(gebietLayer, "CLEAR_SELECTION")
    df.scale = df.scale * 3.0

    arcpy.RefreshActiveView()
    Haltestellen_mxd.save()
    del mxd_template , df,mxdpfad,templatepath,resultpath,gebietLayer

    #Exportiere Ergebnis
    arcpy.mapping.ExportToJPEG(Haltestellen_mxd, os.path.join(workspace_projekt_ergebnisse, "37_Erreichbarkeit_Fahrrad.jpg"), "PAGE_LAYOUT",resolution=150)

    schrittmeldung = 'Uebersichtskarte mit der Erreichbarkeit von Einrichtungen mit dem Fahrrad erstellt \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    del Haltestellen_mxd
    #==================================================================================================================================================================================
    #Kopiere Template.mxd
    mxd_template = arcpy.mapping.MapDocument(os.path.join(base_path, "2_Tool","37_Erreichbarkeit","37_Template_Kartenerzeugung","37_Erreichbarkeit_zuFuss_Template.mxd"))
    mxdpfad = os.path.join(workspace_projekt_ergebnisse,'37_Erreichbarkeit_zuFuss.mxd')
    mxd_template.saveACopy(mxdpfad)

    # Ersetze Datenquelle
    Haltestellen_mxd = arcpy.mapping.MapDocument(mxdpfad)
    templatepath = os.path.join(base_path,"2_Tool","37_Erreichbarkeit","37_Template_Kartenerzeugung","template.gdb")
    resultpath = os.path.join(base_path,"3_Projekte",projektname,"FGDB_37_Erreichbarkeit_Projekt_"+projektname+".gdb")
    Haltestellen_mxd.findAndReplaceWorkspacePaths(templatepath, resultpath)


    # Setze Viewport neu
    df = arcpy.mapping.ListDataFrames(Haltestellen_mxd)[0]
    gebietLayer = arcpy.mapping.ListLayers(Haltestellen_mxd, "Buffer_1000_m_500_m_", df)[0]
    arcpy.SelectLayerByAttribute_management(gebietLayer, "NEW_SELECTION", "\"OBJECTID\" > 0")
    df.extent = gebietLayer.getSelectedExtent(False)
    arcpy.SelectLayerByAttribute_management(gebietLayer, "CLEAR_SELECTION")
    df.scale = df.scale * 3.0

    arcpy.RefreshActiveView()
    Haltestellen_mxd.save()
    del mxd_template , df,mxdpfad,templatepath,resultpath,gebietLayer

    #Exportiere Ergebnis
    arcpy.mapping.ExportToJPEG(Haltestellen_mxd, os.path.join(workspace_projekt_ergebnisse, "37_Erreichbarkeit_zuFuss.jpg"), "PAGE_LAYOUT",resolution=150)

    schrittmeldung = 'Uebersichtskarte mit der Erreichbarkeit von Einrichtungen zu Fuss erstellt \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    del Haltestellen_mxd
    #==================================================================================================================================================================================
    #Kopiere Template.mxd
    mxd_template = arcpy.mapping.MapDocument(os.path.join(base_path, "2_Tool","37_Erreichbarkeit","37_Template_Kartenerzeugung","37_Erreichbarkeit_Pkw_Template.mxd"))
    mxdpfad = os.path.join(workspace_projekt_ergebnisse,'37_Erreichbarkeit_Pkw.mxd')
    mxd_template.saveACopy(mxdpfad)

    # Ersetze Datenquelle
    Haltestellen_mxd = arcpy.mapping.MapDocument(mxdpfad)
    templatepath = os.path.join(base_path,"2_Tool","37_Erreichbarkeit","37_Template_Kartenerzeugung","template.gdb")
    resultpath = os.path.join(base_path,"3_Projekte",projektname,"FGDB_37_Erreichbarkeit_Projekt_"+projektname+".gdb")
    Haltestellen_mxd.findAndReplaceWorkspacePaths(templatepath, resultpath)


    # Setze Viewport neu
    df = arcpy.mapping.ListDataFrames(Haltestellen_mxd)[0]
    gebietLayer = arcpy.mapping.ListLayers(Haltestellen_mxd, "Buffer_1000_m_500_m_", df)[0]
    arcpy.SelectLayerByAttribute_management(gebietLayer, "NEW_SELECTION", "\"OBJECTID\" > 0")
    df.extent = gebietLayer.getSelectedExtent(False)
    arcpy.SelectLayerByAttribute_management(gebietLayer, "CLEAR_SELECTION")
    df.scale = df.scale * 3.0

    arcpy.RefreshActiveView()
    Haltestellen_mxd.save()
    del mxd_template , df,mxdpfad,templatepath,resultpath,gebietLayer

    #Exportiere Ergebnis
    arcpy.mapping.ExportToJPEG(Haltestellen_mxd, os.path.join(workspace_projekt_ergebnisse, "37_Erreichbarkeit_Pkw.jpg"), "PAGE_LAYOUT",resolution=150)

    schrittmeldung = 'Uebersichtskarte mit der Erreichbarkeit von Einrichtungen mit dem Pkw erstellt \n'
    arcpy.AddMessage(schrittmeldung)
    print schrittmeldung

    del Haltestellen_mxd


    # ##################################################################################################################################################


    # ##################################################################################################################################################

    ws1 = wb.add_worksheet('Methodik_')
    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws1.write(x,y,"", background)

    # Pfade zu Grafiken herstellen
    Text1 = os.path.join(workspace_texte_erlaeterung, 'Methodik_ErreichbarkeitWohnen.png')
    ###Grafiken einfügen
    ws1.insert_image(0, 0, Text1, {'x_scale': 0.32, 'y_scale': 0.32})
    del Text1

    # ##################################################################################################################################################

    ws2 = wb.add_worksheet('Methodik_Erreichbarkeit(Einr.)')
    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws2.write(x,y,"", background)

    # Pfade zu Grafiken herstellen
    Text1 = os.path.join(workspace_texte_erlaeterung, 'Methodik_ErreichbarkeitWohnenPkwFahrradZuFuss.png')
    ###Grafiken einfügen
    ws2.insert_image(0, 0, Text1, {'x_scale': 0.32, 'y_scale': 0.32})
    del Text1

    #=====================================================================================================================
    ws111 = wb.add_worksheet("Auswertung_zu Fuss")

    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws111.write(x,y,"", background)

    barcode = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Abbildungen','37_Erreichbarkeit_zuFuss.jpg')
    if os.path.isfile(barcode):
        ws111.write(1, 1, "Visualisierung der Einrichtungen, die zu Fuss innerhalb von 30 Minuten errreicht werden koennen.".decode('utf-8'), bold)
        ws111.insert_image('B3', barcode, {'x_scale': 0.8, 'y_scale': 0.8})
        del barcode
    #=====================================================================================================================
    ws112 = wb.add_worksheet("Auswertung_Fahrrad")

    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws112.write(x,y,"", background)

    barcode = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Abbildungen','37_Erreichbarkeit_Fahrrad.jpg')
    if os.path.isfile(barcode):
        ws112.write(1, 1, "Visualisierung der Einrichtungen, die mit dem Fahrrad innerhalb von 30 Minuten errreicht werden koennen.".decode('utf-8'), bold)
        ws112.insert_image('B3', barcode, {'x_scale': 0.8, 'y_scale': 0.8})
        del barcode
    #=====================================================================================================================
    ws113 = wb.add_worksheet("Auswertung_Pkw")

    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws113.write(x,y,"", background)

    barcode = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Abbildungen','37_Erreichbarkeit_Pkw.jpg')
    if os.path.isfile(barcode):
        ws113.write(1, 1, "Visualisierung der Einrichtungen, die mit dem Pkw innerhalb von 30 Minuten errreicht werden koennen.".decode('utf-8'), bold)
        ws113.insert_image('B3', barcode, {'x_scale': 0.8, 'y_scale': 0.8})
        del barcode
    #=====================================================================================================================
    ws21 = wb.add_worksheet('Auswertung_Zentrale Orte')
    ws21.set_column(1, 1, 60)
    ws21.set_column(2, 2, 30)
    ws21.set_column(3, 3, 25)
    ws21.set_column(4, 4, 22)
    ws21.set_column(5, 5, 50)

    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws21.write(x,y,"", background)

    #############################################################################################################
    # 2.Ergebnisse aus Erreichbarkeit Zentral Orte einlesen und schreiben

    today = datetime.date.today()
    nextmonday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
    abfahrt_min = []
    orte = []
    dauer_min = []
    umsteigen_min = []
    verkehrsmittel_min = []

    with open(os.path.join(workspace_projekt_ergebnisse,"Zentrale_Orte_temp.csv"), 'rb') as f:
        mycsv = csv.reader(f)
        for row in mycsv:
            abfahrt_min.append(row[0])
            orte.append(row[1])
            dauer_min.append(row[2])
            umsteigen_min.append(row[3])
            verkehrsmittel_min.append(row[4])
        del row, mycsv
        print abfahrt_min, orte, dauer_min, umsteigen_min, verkehrsmittel_min

    i=7
    n=0
    ws21.write(2, 1, "Erreichbarkeit ausgewaehlter Mittel- & Oberzentren mit dem OEPNV".decode('utf-8'), bold)
    ws21.write(3, 1, "Schnellste Verbindung, ermittelt durch Zugriff auf die Fahrplanauskunft der Deutschen Bahn".decode('utf-8'))
    ws21.write(4, 1, "Abgefragt fuer den ".decode('utf-8')+str(nextmonday.day)+"."+str(nextmonday.month)+"."+str(nextmonday.year)+" im Zeitraum zwischen 7 - 19 Uhr")

    ws21.write(6, 1, "Abfahrt (naechstgelegene Haltestelle)".decode('utf-8'), bold)
    ws21.write(6, 2, 'Ziel', bold)
    ws21.write(6, 3, 'Fahrtzeit in Minuten', bold_rechts)
    ws21.write(6, 4, 'Anzahl Umstiege', bold_rechts)
    ws21.write(6, 5, 'Verkehrsmittel', bold_rechts)
    for ort in orte:
        ws21.write(i, 1, abfahrt_min[n].decode('latin1'), normal)
        ws21.write(i, 2, ort.decode('utf-8'), normal)
        ws21.write(i, 3, dauer_min[n], rechts)
        ws21.write(i, 4, umsteigen_min[n], rechts)
        ws21.write(i, 5, verkehrsmittel_min[n], rechts)
        i+=1
        n+=1

    #############################################################################################################

    ws31 = wb.add_worksheet('Methodik_Haltestellen')
    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws2.write(x,y,"", background)

    # Pfade zu Grafiken herstellen
    Text1 = os.path.join(workspace_texte_erlaeterung, 'Methodik_ErreichbarkeitWohnenAnbindungsqualitaet.png')
    ###Grafiken einfügen
    ws31.insert_image(0, 0, Text1, {'x_scale': 0.32, 'y_scale': 0.32})
    del Text1

    # ############################################################################################################
    # 3.Karte mit den Haltestellen in der Umgebung einfuegen

    ws3 = wb.add_worksheet("Karte_Haltestellen")

    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws3.write(x,y,"", background)

    ws3.write(1, 1, "Uebersichtskarte mit allen Haltestellen im Umkreis von 500m / 1.000m um das Projektgebiet".decode('utf-8'), bold)
    ws3.write(2, 1, "Ermittelt durch Zugriff auf die Fahrplanauskunft der Deutschen Bahn.")
    image = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Abbildungen', "37_Karte_Haltestellen.jpg")
    ws3.insert_image('B5', image, {'x_scale': 0.75, 'y_scale': 0.75})
    del image

    #############################################################################################################
    # 4.Diagramme und Daten aus Erreichbarkeit OePNV einlesen und schreiben

    name = []
    style = []
    datum = []
    name_long = []

    with open(os.path.join(workspace_projekt_ergebnisse,"Haltestellen.csv"), 'rb') as f:
        mycsv = csv.reader(f)
        for row in mycsv:
            name.append(row[0])
            style.append(row[1])
            datum.append(row[2])
            name_long.append(row[3])
        del row, mycsv
        print name, style, datum

    i=1
    for n in name:
        ws4 = wb.add_worksheet("Auswertung_Haltestelle0"+str(i)) #Excel-Sheet-Benennung =|= Haltestellenname zur Vermeidung von Codierungskonflikten

        # Hintergrund weiss faerben
        for x in range(0,200):
            for y in range(0,200):
                ws4.write(x,y,"", background)

        barcode = os.path.join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Abbildungen', n+".png")
        if os.path.isfile(barcode):
            ws4.write(1, 1, "Visualisierung der OEPNV-Taktung an der Haltestelle ".decode('utf-8') + name_long[i-1].decode('latin-1'), bold)
            ws4.write(2, 1, "Ermittelt durch Zugriff auf die Fahrplanauskunft der Deutschen Bahn. Abgefragt fuer den ".decode('utf-8') + datum[i-1])
            if style[i-1] == "1":
                ws4.write(3, 1, "Farbliche Unterscheidung nach Art des Verkehrstraegers".decode('utf-8'))
            elif style[i-1] == "2":
                ws4.write(3, 1, "Farbliche Unterscheidung nach Fahrtziel".decode('utf-8'))
            elif style[i-1] == "3":
                ws4.write(3, 1, "Farbliche Unterscheidung nach OEPNV-Linie".decode('utf-8'))
            elif style[i-1] == "4":
                ws4.write(3, 1, "Linie mit der dichtesten Taktung farblich hervorgehoben.".decode('utf-8'))
            ws4.write(4,1,"Ueberlagerung der unterschiedlichen Linien / Fahrtziele durch gleiche Abfahrtszeiten moeglich.")
            ws4.insert_image('B7', barcode, {'x_scale': 0.4, 'y_scale': 0.4})
        else:
            pass
        i+=1
    del i, barcode

    # ####################################################################################################################################

    ws16 = wb.add_worksheet('Literatur_Haftungsausschluss')

    # Pfade zu Grafiken herstellen
    Text1 = os.path.join(workspace_texte_erlaeterung, 'Methodik_Haftung.jpg')
    ###Grafiken einfügen
    ws16.insert_image(0, 0, Text1, {'x_scale': 0.32, 'y_scale': 0.32})

    del Text1

    #Workbook speichern
    try:
    	wb.close()
    except IOError:
    	schrittmeldung = 'ACHTUNG \nDie Ergebnisstabelle konnte nicht gespreichert werden, da eine aeltere Version der Datei momentan in Excel geoeffnet ist. Bitte schliessen Sie diese Tabelle und fuehren Sie den Arbeitsschritt erneut aus. \n'
    	arcpy.AddError(schrittmeldung)
    	print schrittmeldung

# Endmeldung
print 'Ergebnisse in Excel-Arbeitsmappe zusammengfuegt und exportiert \n'
arcpy.AddMessage('Ergebnisse in Excel-Arbeitsmappe zusammengfuegt und exportiert')




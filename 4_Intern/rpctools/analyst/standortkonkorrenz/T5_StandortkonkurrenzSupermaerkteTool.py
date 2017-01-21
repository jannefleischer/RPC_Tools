# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# 05_Standortkonkurrenz_Supermaerktetool.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# HCU Hamburg
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------


#Fertig nur noch abspeichern fehlt

import imp
import math
import sys
import gc
import os
import arcpy
import xlsxwriter


def main(parameters, messages):
    projektname = parameters[0].valueAsText

    #Pfade einrichten
    base_path = str(sys.path[0]).split("2_Tool")[0]
    # import sheet_lib as sl
    sheetlibpath = os.path.abspath(join(os.path.dirname( __file__ ), '..', '2_Projektverwaltung','sheet_lib.py'))
    sl = imp.load_source('sheet_lib', sheetlibpath)

    workspace_basis_daten_wert=join(base_path,'2_Tool',"G_Standortkonkurrenz_Supermaerkte",'FGDB_Standortkonkurrenz_Supermaerkte_Tool.gdb')
    workspace_texte_erlaeterung = join(base_path,'2_Tool','G_Standortkonkurrenz_Supermaerkte','Erlaeuterungstexte')
    workspace_projekt = join(base_path,'3_Projekte',projektname,'FGDB_Definition_Projekt.gdb')
    workspace_wertveraederung = join(base_path,'3_Projekte',projektname,'FGDB_Standortkonkurrenz_Supermaerkte.gdb')
    workspace_projekt_ergebnisse = join(base_path,'3_Projekte',projektname, 'Ergebnisausgabe', 'Abbildungen')

    schrittmeldung = 'Datenexport in Excel-Datei  \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung
    #==================================================================================================================================================================================
    #Kopiere Template.mxd
    try:
        arcpy.DeleteFeatures_management("Teilflaechen_Plangebiet")
    except:
        pass
    arcpy.Copy_management(join(workspace_projekt,"Teilflaechen_Plangebiet"),join(workspace_wertveraederung,"Teilflaechen_Plangebiet"))

    mxd_template = arcpy.mapping.MapDocument(join(base_path, "2_Tool","G_Standortkonkurrenz_Supermaerkte","Template_Kartenerzeugung","34_KK_Bindung_Template.mxd"))
    mxdpfad = join(workspace_projekt_ergebnisse,'34_KK_Bindung.mxd')
    mxd_template.saveACopy(mxdpfad)

    # Ersetze Datenquelle
    Haltestellen_mxd = arcpy.mapping.MapDocument(mxdpfad)
    templatepath = join(base_path,"2_Tool","G_Standortkonkurrenz_Supermaerkte","Template_Kartenerzeugung","template.gdb")
    resultpath = join(base_path,"3_Projekte",projektname,"FGDB_Standortkonkurrenz_Supermaerkte_"+projektname+".gdb")
    Haltestellen_mxd.findAndReplaceWorkspacePaths(templatepath, resultpath)

    #==================================================================================================================================================================================
    # Ersetze Datenquelle
    Haltestellen_mxd = arcpy.mapping.MapDocument(mxdpfad)
    templatepath = join(base_path,"2_Tool","G_Standortkonkurrenz_Supermaerkte","Template_Kartenerzeugung","template.gdb")
    resultpath = join(base_path,"3_Projekte",projektname,"FGDB_Standortkonkurrenz_Supermaerkte_"+projektname+".gdb")
    Haltestellen_mxd.findAndReplaceWorkspacePaths(templatepath, resultpath)
    # Setze Viewport neu
    df = arcpy.mapping.ListDataFrames(Haltestellen_mxd)[0]
    gebietLayer = arcpy.mapping.ListLayers(Haltestellen_mxd, "Siedlungszahlendaten_planfall", df)[0]

    arcpy.SelectLayerByLocation_management(gebietLayer, "WITHIN_A_DISTANCE", join(workspace_wertveraederung,"Neuer_Markt"), "1 Kilometers", "NEW_SELECTION")
    df.extent = gebietLayer.getSelectedExtent(False)
    arcpy.SelectLayerByAttribute_management(gebietLayer, "CLEAR_SELECTION")
    df.scale = df.scale * 2.5

    arcpy.RefreshActiveView()
    Haltestellen_mxd.save()
    del mxd_template , df,mxdpfad,templatepath,resultpath,gebietLayer

    #Exportiere Ergebnis
    arcpy.mapping.ExportToJPEG(Haltestellen_mxd, join(workspace_projekt_ergebnisse, "34_KK_Bindung.jpg"), "PAGE_LAYOUT",resolution=300)

    schrittmeldung = 'Uebersichtskarte der KK-Bindung erstellt \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung

    del Haltestellen_mxd

    #==================================================================================================================================================================================
    mxd_template = arcpy.mapping.MapDocument(join(base_path, "2_Tool","34_Standortkonkurrenz_Supermaerkte","34_Template_Kartenerzeugung","34_Bestand_Template.mxd"))
    mxdpfad = join(workspace_projekt_ergebnisse,'34_Bestand.mxd')
    mxd_template.saveACopy(mxdpfad)

    # Ersetze Datenquelle
    Haltestellen_mxd = arcpy.mapping.MapDocument(mxdpfad)
    templatepath = join(base_path,"2_Tool","G_Standortkonkurrenz_Supermaerkte","Template_Kartenerzeugung","template.gdb")
    resultpath = join(base_path,"3_Projekte",projektname,"FGDB_Standortkonkurrenz_Supermaerkte_"+projektname+".gdb")
    Haltestellen_mxd.findAndReplaceWorkspacePaths(templatepath, resultpath)
    # Setze Viewport neu
    df = arcpy.mapping.ListDataFrames(Haltestellen_mxd)[0]
    gebietLayer = arcpy.mapping.ListLayers(Haltestellen_mxd, "Einzelhandelstandorte", df)[0]

    ##print gebietLayer
    ##arcpy.SelectLayerByAttribute_management(gebietLayer, "NEW_SELECTION", "\"OBJECTID\" > 0")
    arcpy.SelectLayerByLocation_management(gebietLayer, "WITHIN_A_DISTANCE", join(workspace_wertveraederung,"Teilflaechen_Plangebiet"), "4 Kilometers", "NEW_SELECTION")
    df.extent = gebietLayer.getSelectedExtent(False)
    arcpy.SelectLayerByAttribute_management(gebietLayer, "CLEAR_SELECTION")
    df.scale = df.scale * 3.0

    arcpy.RefreshActiveView()
    Haltestellen_mxd.save()
    del mxd_template , df,mxdpfad,templatepath,resultpath,gebietLayer

    #Exportiere Ergebnis
    arcpy.mapping.ExportToJPEG(Haltestellen_mxd, join(workspace_projekt_ergebnisse, "34_Bestandregion.jpg"), "PAGE_LAYOUT",resolution=300)

    schrittmeldung = 'Uebersichtskarte der Bestandregion erstellt \n'
    messages.AddMessage(schrittmeldung)
    print schrittmeldung

    del Haltestellen_mxd
    #==================================================================================================================================================================================
    #############################################################################################################
    # 1. Dokument einrichten

    # Pfade setzen
    logo = join((str(sys.path[0]).split("2_Tool")[0]),"1_Basisdaten","logo_rpc.png")
    ausgabeordner = join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Excel')
    excelpfad = join(ausgabeordner,'Standortkonkurrenz_Supermaerkte.xlsx')

    try:
        os.remove(excelpfad)
    except:
        pass

    # Workbook und Tabellenblaetter anlegen
    wb = xlsxwriter.Workbook(excelpfad)
    sl.infosheet(projektname, str("Standortkonkurrenz_Supermaerkte").decode('utf-8'), wb)

    # Styles anlegen
    head = wb.add_format({'bold': True, 'font_size': '24', 'align': 'left','valign': 'vcenter', 'bg_color': 'white', 'border': '0'})
    normal = wb.add_format({'font_size': '14', 'bg_color': 'white', 'border': '0'})
    rechts = wb.add_format({'font_size': '14', 'align' : 'right', 'bg_color': 'white', 'border': '0'})
    bold = wb.add_format({'bold': True, 'font_size': '14', 'bg_color': 'white', 'border': '0'})
    bold_rechts = wb.add_format({'bold': True, 'font_size': '14', 'bg_color': 'white', 'border': '0', 'align' : 'right'})

    background = wb.add_format({'bg_color': 'white', 'border': '0'})

    ws2 = wb.add_worksheet('Methodik_Standortkonkurrenz')

    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws2.write(x,y,"", background)
    # 2.Beschreibung des Wirkungsfeldes
    image = join(workspace_texte_erlaeterung, 'Methodik_Standortkonkurrenz1.jpg')
    ws2.insert_image(0,0, image, {'x_scale': 0.32, 'y_scale': 0.32})
    del image
    #####################################################################################################################################
    ws3 = wb.add_worksheet('Expofunktion Standortkommune')
    ws3.set_column(1, 1, 35)
    ws3.set_column(1, 2, 20)
    ws3.set_column(1, 3, 23)
    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws3.write(x,y,"", background)
    #Dichtesten SM zum untersuchungsgebiet finden -> Gemeindeklasse erhalten

    try:
        arcpy.DeleteFeatures_management("MP_RPC_Gebiet")
        arcpy.Delete_management(join(workspace_wertveraederung,"MP_RPC_Gebiet"))
    except:
        pass
    try:
        # Local variables:
        MP_RPC_Gebiet = join(workspace_wertveraederung,"MP_RPC_Gebiet")
        Standortdaten_planfall = join(workspace_wertveraederung,"Standortdaten_planfall")

        # Process: Räumliche Verbindung
        arcpy.SpatialJoin_analysis(join(workspace_projekt,"Teilflaechen_Plangebiet"), Standortdaten_planfall, MP_RPC_Gebiet, "JOIN_ONE_TO_MANY", "KEEP_COMMON", "Gemeindeklasse \"Gemeindeklasse\" true true false 4 Long 0 0 ,First,#,"+Standortdaten_planfall+",Gemeindeklasse,-1,-1", "CLOSEST", "", "")
        del Standortdaten_planfall,MP_RPC_Gebiet
    except:
        messages.AddErrorMessage("Notwendige Datei konnte nicht kopiert werden.")
        exit(1)


    cur_Centroid_RPC= arcpy.SearchCursor(join(workspace_wertveraederung,"MP_RPC_Gebiet"))
    Gemeindeklasse=0
    for zeile in cur_Centroid_RPC:
        Gemeindeklasse=zeile.Gemeindeklasse
        break
    del zeile,cur_Centroid_RPC

    ##    messages.AddMessage(Gemeindeklasse)
    if Gemeindeklasse==1:
    #Ueber_100kEW:
        expofunktion="Ueber_100kEW"
    elif Gemeindeklasse==2:
    #Zwischen_50k_100kEW
        expofunktion="Zwischen_50k_100kEW"
    elif Gemeindeklasse==3:
    #Zwischen_20k_50kEW:
        expofunktion="Zwischen_20k_50kEW"
    elif Gemeindeklasse==4:
    #Zwischen_10k_20kEW:
        expofunktion="Zwischen_10k_20kEW"
    else:
        messages.AddErrorMessage("Fehler bei den Gemeindeklassen")
        print "Fehler bei den Gemeindeklassen"
        exit(1)

    cur_Expo_Funktion = arcpy.SearchCursor(join(workspace_basis_daten_wert,expofunktion))
    ##    spaltennamen = [f.name for f in arcpy.ListFields(join(workspace_basis_daten_wert,expofunktion))]
    ##    spaltennamen=spaltennamen[1:]
    ##    for n, spalten in  enumerate( spaltennamen):
    ##        if n==0:
    ##            ws3.write(2,n+1,str(spalten),bold)
    ##        else:
    ##            ws3.write(2,n+1,str(spalten),bold_rechts)

    ws3.write(3,1,"Betriebstyp",bold)
    ws3.write(3,2,"Faktor",bold_rechts)
    ws3.write(3,3,"Hochzahl",bold_rechts)

    k=0
    for n, zeilen in enumerate( cur_Expo_Funktion):
        ws3.write(n+4,1,zeilen.Typ.decode('utf-8'))
        ws3.write(n+4,2,zeilen.Faktor_EXP)
        ws3.write(n+4,3,zeilen.Hochzahl)
        k=n+4

    k=k+3
    ws3.write(k,1,"Abkuerzungen der Betriebstypen",bold)
    ws3.write(k+2,1,"Aldi = Aldi-Discounter ohne Verkaufsflaechenbegrenzung")
    ws3.write(k+3,1,"Penny = Penny-Discounter ohne Verkaufsflaechenbegrenzung")
    ws3.write(k+4,1,"Lidl = Lidl-Discounter ohne Verkaufsflaechenbegrenzung")
    ws3.write(k+5,1,"Netto(Edeka) = Netto(Edeka)-Discounter ohne Verkaufsflaechenbegrenzung")
    ws3.write(k+6,1,"(ggf. enthaelt die Liste weitere Discountmaerkte)")

    ws3.write(k+8,1,"kl. SM. (Anbieter) = kleiner Supermarkt mit einer Verkaufsflaeche zwischen 401 und 800 qm (Anbieter)")
    ws3.write(k+9,1,"mittl. SM (Anbieter) = Supermarkt mit einer Verkaufsflaeche zwischen 801 und 1.500 qm (Anbieter)")
    ws3.write(k+10,1,"gr. SM (Anbieter) = grosser Supermarkt mit einer Verkaufsflaeche zwischen 1.501 und 2.500 qm (Anbieter)")
    ws3.write(k+11,1,"V-Markt (Anbieter) = Verbrauchermarkt (Lebensmittelmarkt) mit einer Verkaufsflaeche zwischen 2.501 und 5.000 qm (Anbieter)")
    ws3.write(k+12,1,"SBW (Anbieter) = SB-Warenhaus (Lebensmittelmarkt) mit einer Verkaufsflaeche ab 5.001 qm (Anbieter)")
    ws3.write(k+13,1,"allg. = fasst die Anbieter des jeweiligen Betriebstyps (Groesse) zusammen, die nicht explizit aufgefuehrt werden")
    ws3.write(k+14,1,"kl. Nahversorgungsmarkt = Lebensmittelmarkt (kein Discounter) mit einer Verkaufsflaeche bis 400 qm")

    del cur_Expo_Funktion,k

    ################################################################################################################
    ws4 = wb.add_worksheet('Methodik_Konkurrenzsituation')
    ##ws4.set_column(1, 1, 120)
    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws4.write(x,y,"", background)
    # 2.Beschreibung des Wirkungsfeldes
    image = join(workspace_texte_erlaeterung, 'Methodik_Standortkonkurrenz2.jpg')
    ws4.insert_image(0,0, image, {'x_scale': 0.32, 'y_scale': 0.32})
    del image


    ################################################################################################################
    ws5 = wb.add_worksheet('Auswertung_Bestand Region')
    ws5.set_column(1, 1, 5)
    ws5.set_column(2, 2, 30)
    ws5.set_column(3, 3, 14)
    ws5.set_column(4, 4, 30)
    ws5.set_column(5, 6, 25)
    ws5.set_column(7, 7, 7)
    ws5.set_column(8, 8, 13)
    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws5.write(x,y,"", background)

    ws5.write(2, 1, 'Bestand Lebensmittelmaerkte in der Region'.decode('utf-8'), bold)
    ws5.write(3, 1, "ID".decode('utf-8'), bold)
    ws5.write(3, 2, "Name / Anbieter".decode('utf-8'), bold)
    ws5.write(3, 3, "Postleitzahl".decode('utf-8'), bold)
    ws5.write(3, 4, "Ort".decode('utf-8'), bold)
    ws5.write(3, 5, "Ortsteil".decode('utf-8'), bold)
    ws5.write(3, 6, "Strasse".decode('utf-8'), bold)
    ws5.write(3, 7, "HNR".decode('utf-8'), bold)
    ws5.write(3, 8, "VKFL gesamt".decode('utf-8'), bold)

    cur_Standorten = arcpy.SearchCursor(join(workspace_wertveraederung,"Standortdaten"))
    for n, zeile in enumerate( cur_Standorten):
        ws5.write(n+4,1,zeile.Id)
        ws5.write(n+4,2,zeile.Betriebstyp)
        ws5.write(n+4,3,zeile.PLZ)
        ws5.write(n+4,4,zeile.Ort)
        ws5.write(n+4,5,zeile.Ortsteil)
        ws5.write(n+4,6,zeile.Strasse)
        ws5.write(n+4,7,zeile.HNR)
        ws5.write(n+4,8,zeile.VKFL_gesamt)

    ws5.write(3, 10, "Uebersichtskarte des Einzelhandels in der Region".decode('utf-8'), bold)
    image = join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Abbildungen', "34_Bestandregion.jpg")
    ws5.insert_image('K5', image, {'x_scale': 0.25, 'y_scale': 0.25})
    del image


    ################################################################################################################
    ws6 = wb.add_worksheet('Methodik_Teilergebnisse 1')
    ##ws6.set_column(1, 1, 120)

    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws6.write(x,y,"", background)
    # 2.Beschreibung des Wirkungsfeldes
    image = join(workspace_texte_erlaeterung, 'Methodik_Standortkonkurrenz3.jpg')
    ws6.insert_image(0,0, image, {'x_scale': 0.32, 'y_scale': 0.32})
    del image

    ################################################################################################################
    ws7 = wb.add_worksheet('Grafik_KKBindung neuer Standort')


    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws7.write(x,y,"", background)

    ws7.write(2, 1, "Kaufkraftbindung durch den neuen bzw. erweiterten Markt".decode('utf-8'), bold)
    image = join(base_path,'3_Projekte',projektname,'Ergebnisausgabe','Abbildungen', "34_KK_Bindung.jpg")
    ws7.insert_image('B4', image, {'x_scale': 0.25, 'y_scale': 0.25})
    del image

    ################################################################################################################
    ws8 = wb.add_worksheet('Auswertung_Umsatz Planvorhabens')
    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws8.write(x,y,"", background)
    ws8.set_column(1, 1, 30)
    ws8.set_column(2, 2, 12)

    ws8.write(2, 1, "Umsatz des Planvorhabens".decode('utf-8'), bold)

    cur_statistik=arcpy.SearchCursor(join(workspace_wertveraederung,"Statistik_planfall"))
    umsaetze=[]
    for zeile in cur_statistik:
        umsaetze.append(zeile.SUM_ID_600)
        try:
            umsaetze.append(zeile.SUM_ID_601)
        except:
            #kein weiteren markt
            pass

    del cur_statistik
    ws8.write(3,1,"%.2f" % (umsaetze[0]/1000000))
    ws8.write(3,2,"Mio. Euro (brutto)".decode('utf-8'))

    if len(umsaetze)>1:
        ws8.write(4,1,"Zweites Vorhaben")
        ws8.write(5,1,"%.2f" % (umsaetze[1]/1000000))
        ws8.write(5,2,"Mio. Euro (brutto)".decode('utf-8'))
    del umsaetze

    ################################################################################################################
    ws9 = wb.add_worksheet('Methodik_Teilergebnisse2')
    ##ws9.set_column(1, 1, 120)
    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws9.write(x,y,"", background)
    # 2.Beschreibung des Wirkungsfeldes
    image = join(workspace_texte_erlaeterung, 'Methodik_Standortkonkurrenz4.jpg')
    ws9.insert_image(0,0, image, {'x_scale': 0.32, 'y_scale': 0.32})
    del image

    ################################################################################################################
    ws10 = wb.add_worksheet('Auswertung_Umsatzveraenderung')
    ws10.set_column(1, 1, 30)
    ws10.set_column(2, 2, 25)
    ws10.set_column(3, 3, 26)
    ws10.set_column(4, 4, 15)
    ws10.set_column(5, 5, 20)
    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws10.write(x,y,"", background)
    ws10.write(2, 1, "Umsatzveraenderung Bestand".decode('utf-8'), bold)
    ws10.write(4, 1, "Gemeinde".decode('utf-8'), bold)
    ws10.write(4, 2, "Umsatz Nullfall (Mio)".decode('utf-8'), bold)
    ws10.write(4, 3, "Umsatz Planfall (Mio)".decode('utf-8'), bold)
    ws10.write(4, 4, "Verlust in %".decode('utf-8'), bold)
    ws10.write(4, 5, "Verlust (absolut)".decode('utf-8'), bold)
    cur_verlustrech_sear= arcpy.SearchCursor(join(workspace_wertveraederung,"Verlustrechnung"))
    p=0
    for n, zeile in enumerate( cur_verlustrech_sear):
        if(" Zentrum" in zeile.GesamtGem):
            p=1
        ws10.write(n+5+p,1,zeile.GesamtGem)
        ws10.write(n+5+p,2,"%.2f" % (zeile.Umsatz_vorher/1000000))
        ws10.write(n+5+p,3,"%.2f" % (zeile.Umsatz_nachher/1000000))
        ws10.write(n+5+p,4,"%.2f" % zeile.Differenz_Proz)
        ws10.write(n+5+p,5,"%.2f" % (zeile.Differenz/1000000))

    del cur_verlustrech_sear

    ################################################################################################################
    ws11 = wb.add_worksheet('Methodik_Teilergebnisse3')
    ##ws11.set_column(1, 1, 120)
    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws11.write(x,y,"", background)
    # 2.Beschreibung des Wirkungsfeldes
    image = join(workspace_texte_erlaeterung, 'Methodik_Standortkonkurrenz5.jpg')
    ws11.insert_image(0,0, image, {'x_scale': 0.32, 'y_scale': 0.32})
    del image


    ################################################################################################################
    ws12 = wb.add_worksheet('Delta-Ausstattungskennziffern')
    ws12.set_column(1, 1, 30)
    ws12.set_column(2, 3, 37)
    ws12.set_column(4, 4, 37)
    ws12.set_column(5, 5, 30)
    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws12.write(x,y,"", background)
    ws12.write(2, 1, "Ausstattungskennziffern".decode('utf-8'), bold)
    ws12.write(4, 1, "Gemeinde".decode('utf-8'), bold)
    ws12.write(4, 2, "Verkaufsflaechendichte Nullfall".decode('utf-8'), bold)
    ws12.write(4, 3, "Verkaufsflaechendichte Planfall".decode('utf-8'), bold)
    ws12.write(4, 4, "Delta Betrachtung".decode('utf-8'), bold)

    cur_verlustrech_sear= arcpy.SearchCursor(join(workspace_wertveraederung,"Verkaufsflaeche"))

    for n, zeile in enumerate( cur_verlustrech_sear):
        ws12.write(n+5,1,zeile.Kommune)
        ws12.write(n+5,2,"%.2f" % zeile.Verkaufsflazent)
        ws12.write(n+5,3,"%.2f" % zeile.Verkaufsflazentpla)
        ws12.write(n+5,4,"%.2f" % zeile.Delta)

    del cur_verlustrech_sear
    ################################################################################################################
    ws12_1 = wb.add_worksheet('Einzelhandelzentralitaet')
    ws12_1.set_column(1, 1, 30)
    ws12_1.set_column(2, 3, 40)
    ws12_1.set_column(4, 4, 40)
    ws12_1.set_column(5, 5, 30)
    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws12_1.write(x,y,"", background)
    ws12_1.write(2, 1, "Einzelhandelzentralitaet".decode('utf-8'), bold)
    ws12_1.write(4, 1, "Gemeinde".decode('utf-8'), bold)
    ws12_1.write(4, 2, "Einzelhandelzentralitaet Nullfall".decode('utf-8'), bold)
    ws12_1.write(4, 3, "Einzelhandelzentralitaet Planfall".decode('utf-8'), bold)
    ws12_1.write(4, 4, "Delta Betrachtung".decode('utf-8'), bold)

    cur_verlustrech_sear= arcpy.SearchCursor(join(workspace_wertveraederung,"Einzelhzentrali"))

    for n, zeile in enumerate( cur_verlustrech_sear):
        ws12_1.write(n+5,1,zeile.Kommune)
        ws12_1.write(n+5,2,"%.2f" % zeile.Einzelhzentra)
        ws12_1.write(n+5,3,"%.2f" % zeile.Einzelhzentrapla)
        ws12_1.write(n+5,4,"%.2f" % zeile.Delta)

    del cur_verlustrech_sear
    ################################################################################################################
    ws13 = wb.add_worksheet('Bewertung')
    ##ws13.set_column(1, 1, 120)
    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws13.write(x,y,"", background)
    image = join(workspace_texte_erlaeterung, 'Methodik_Standortkonkurrenz6a.jpg')
    ws13.insert_image(0,0, image, {'x_scale': 0.32, 'y_scale': 0.32})
    del image
    image = join(workspace_texte_erlaeterung, 'Methodik_Standortkonkurrenz6b.jpg')
    ws13.insert_image(52,0, image, {'x_scale': 0.32, 'y_scale': 0.32})
    del image

    ################################################################################################################
    ws14 = wb.add_worksheet('Literatur_Haftungsausschluss')
    ##ws13.set_column(1, 1, 120)
    # Hintergrund weiss faerben
    for x in range(0,200):
        for y in range(0,200):
            ws14.write(x,y,"", background)
    image = join(workspace_texte_erlaeterung, 'Methodik_Standortkonkurrenz7.jpg')
    ws14.insert_image(0,0, image, {'x_scale': 0.32, 'y_scale': 0.32})
    del image

    #Workbook speichern
    try:
        wb.close()
    except IOError:
        schrittmeldung = 'ACHTUNG \nDie Ergebnisstabelle konnte nicht gespreichert werden, da eine aeltere Version der Datei momentan in Excel geöffnet ist. Bitte schließen Sie diese Tabelle und führen Sie den Arbeitsschritt erneut aus. \n'
        messages.AddErrorMessage(schrittmeldung)
        print schrittmeldung
        exit(1)

    #del base_path,workspace_basis_daten_wert,workspace_texte_erlaeterung,workspace_projekt,workspace_wertveraederung,workspace_projekt_ergebnisse
    # Endmeldung
    print 'Ergebnisse in Excel-Arbeitsmappe zusammengfuegt und exportiert \n'
    messages.AddMessage('Ergebnisse in Excel-Arbeitsmappe zusammengfuegt und exportiert')


    def Betriebstyperstellen(shp_Standortdaten):
        #shp_Standortdaten

        Discounter=['Aktiv-Discount','diska','Netto(Edeka)','Netto','Lidl','Aldi','Penny','Norma','NP','treff 3000']
        try:
            arcpy.AddField_management(join(workspace_projekt,shp_Standortdaten), "Betreibstyp_bzw_Anbeiter", "TEXT")
        except:
            print "error"
            exit(1)
            return
        cur_Standortdaten=arcpy.UpdateCursor(join(workspace_projekt,shp_Standortdaten))

        for maerkte in cur_Standortdaten:

    ##        print maerkte.Betriebstyp

            if ([g for g in Discounter if str(maerkte.Betriebstyp.encode('utf-8')).lower().replace(' ','') in str(g).lower().replace(' ','')] and maerkte.Betriebstyp.lower()!="Edeka".lower()):
                #Ja ein Discounter
        ##            print maerkte.Betriebstyp
        ##            print "Ja ein Discounter"
        ##            if maerkte.Id==60:
        ##                print str(maerkte.Betriebstyp).lower()
        ##                print "netto" in str(maerkte.Betriebstyp).lower() and "edeka" in  str(maerkte.Name_postalisch).lower()
        ##                print "netto" in str(maerkte.Betriebstyp).lower()
        ##                print "netto(edeka)" ==  str(maerkte.Name_postalisch).lower()
        ##                print str(maerkte.Betriebstyp).lower()=="netto(edeka)"

                if "aktiv-discount" in str(maerkte.Betriebstyp).lower() or  "aktiv discount" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter="Aktiv-Discount"
                elif "diska" in str(maerkte.Betriebstyp).lower() :
                    maerkte.Betreibstyp_bzw_Anbeiter="diska"
                elif "lidl" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter="Lidl"
                elif ("netto" in str(maerkte.Betriebstyp).lower() and "edeka" in  str(maerkte.Name_postalisch).lower() )or (str(maerkte.Betriebstyp).lower()=="netto(edeka)"):
                    maerkte.Betreibstyp_bzw_Anbeiter="Netto(Edeka)"
                elif "netto" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter="Netto"
                elif "aldi" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter="Aldi"
                elif "penny" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter="Penny"
                elif "norma" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter="Norma"
                elif "np" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter="NP"
                elif "treff 3000" in str(maerkte.Betriebstyp).lower():
                    maerkte.Betreibstyp_bzw_Anbeiter="treff 3000"
                else:
                    #Nicht vorhanden der Betriebstyp
                    messages.AddMessage("Discounter unbekannt")
                    messages.AddMessage("Betriebstyp nicht vorhanden MarktId: " + str(maerkte.Id))

                cur_Standortdaten.updateRow(maerkte)
            else:
                #Ein SM
        ##            print "Ja ein SM"
                if maerkte.VKFL_Gesamt<=400:
                    maerkte.Betreibstyp_bzw_Anbeiter="kl. Nahversorgungsmarkt"
                    cur_Standortdaten.updateRow(maerkte)
                elif maerkte.VKFL_Gesamt<=800:
                    #kl. SM Betreiber
                    string="kl. SM "
                    if "edeka" in str(maerkte.Betriebstyp).lower() or ("e" in str(maerkte.Betriebstyp).lower() and ("neukauf" in str(maerkte.Betriebstyp).lower() or "center" in str(maerkte.Betriebstyp).lower()))or ("e" in str(maerkte.Betriebstyp).lower() and "aktiv" in str(maerkte.Betriebstyp).lower() and "markt" in str(maerkte.Betriebstyp).lower())or ("nah" in str(maerkte.Betriebstyp).lower() and "gut" in str(maerkte.Betriebstyp).lower()):
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Edeka"
                    elif "marktkauf" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Marktkauf"
                    elif "kaufland" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Kaufland"
                    elif "coma" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Coma"
                    elif "combi" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Combi"
                    elif "familia" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Famila"
                    elif "globus" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"globus"
                    elif "migros" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Migros"
                    elif "hit" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"HIT"
                    elif "jibi" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Jibi"
                    elif "konsum-leipzig" in str(maerkte.Betriebstyp).lower() or "konsum leipzig" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Konsum-Leipzig"
                    elif "markant" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Markant"
                    elif "rewe" in str(maerkte.Betriebstyp).lower() or  "nahkauf" in str(maerkte.Betriebstyp).lower() :
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Rewe"
                    elif "tegut" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"tegut"
                    elif "perfetto" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Perfetto"
                    elif "v-markt" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"V-Markt"
                    elif "wasgau" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Wasgau"
                    elif "toom" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"toom"
                    elif "sky" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Sky"
                    elif "plaza" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"plaza"
                    elif "real" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"real"
                    elif "denns" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"denns"
                    elif "alnatura" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Alnatura"
                    elif "biomarkt" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"biomarkt"
                    elif "basic" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"basic"
                    elif "biocompany" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"biocompany"
                    elif "vitalia" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"vitalia"
                    elif "viv" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"viv"
                    else:
                        try:
                            Name_Markt=str(maerkte.Name_postalisch).split(' ')[0]
                        except:
                ##                        print "fehler namenmarkt"
                            Name_Markt=str(maerkte.Name_postalisch)
                        maerkte.Betreibstyp_bzw_Anbeiter=string+Name_Markt
                ##                    print "Unbekannter Betreiber "+str(maerkte.Betriebstyp)+ " Zuteilung kl. SM nicht moeglich\n"
                ##                    messages.AddMessage("Zuteilung kl. SM nicht moeglich")
                ##                    messages.AddMessage("Unbekannter Betreiber "+str(maerkte.Betriebstyp))
                    cur_Standortdaten.updateRow(maerkte)

                elif maerkte.VKFL_gesamt<=1500:
                    #mttl SM Betreiber
                    string="mittl. SM "
                    if "edeka" in str(maerkte.Betriebstyp).lower() or ("e" in str(maerkte.Betriebstyp).lower() and ("neukauf" in str(maerkte.Betriebstyp).lower() or "center" in str(maerkte.Betriebstyp).lower()))or ("e" in str(maerkte.Betriebstyp).lower() and "aktiv" in str(maerkte.Betriebstyp).lower() and "markt" in str(maerkte.Betriebstyp).lower())or ("nah" in str(maerkte.Betriebstyp).lower() and "gut" in str(maerkte.Betriebstyp).lower()):
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Edeka"
                    elif "marktkauf" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Marktkauf"
                    elif "kaufland" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Kaufland"
                    elif "coma" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Coma"
                    elif "combi" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Combi"
                    elif "familia" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Famila"
                    elif "globus" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"globus"
                    elif "migros" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Migros"
                    elif "hit" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"HIT"
                    elif "jibi" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Jibi"
                    elif "konsum-leipzig" in str(maerkte.Betriebstyp).lower() or "konsum leipzig" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Konsum-Leipzig"
                    elif "markant" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Markant"
                    elif "rewe" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Rewe"
                    elif "tegut" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"tegut"
                    elif "perfetto" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Perfetto"
                    elif "v-markt" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"V-Markt"
                    elif "wasgau" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Wasgau"
                    elif "toom" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"toom"
                    elif "sky" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Sky"
                    elif "plaza" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"plaza"
                    elif "real" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"real"
                    elif "denns" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"denns"
                    elif "alnatura" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Alnatura"
                    elif "biomarkt" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"biomarkt"
                    elif "basic" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"basic"
                    elif "biocompany" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"biocompany"
                    elif "vitalia" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"vitalia"
                    elif "viv" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"viv"
                    else:
                        try:
                            Name_Markt=str(maerkte.Name_postalisch).split(' ')[0]
                        except:
                ##                        print "fehler namenmarkt"
                            Name_Markt=str(maerkte.Name_postalisch)
                        maerkte.Betreibstyp_bzw_Anbeiter=string+Name_Markt
                ##                    messages.AddMessage("Zuteilung mittl. SM nicht moeglich")
                ##                    messages.AddMessage("Unbekannter Betreiber "+str(maerkte.Betriebstyp))
                    cur_Standortdaten.updateRow(maerkte)
                elif maerkte.VKFL_gesamt<=2500:
                    #gr SM Betreiber
                    string="gr. SM "
                    if "edeka" in str(maerkte.Betriebstyp).lower() or ("e" in str(maerkte.Betriebstyp).lower() and ("neukauf" in str(maerkte.Betriebstyp).lower() or "center" in str(maerkte.Betriebstyp).lower()))or ("e" in str(maerkte.Betriebstyp).lower() and "aktiv" in str(maerkte.Betriebstyp).lower() and "markt" in str(maerkte.Betriebstyp).lower())or ("nah" in str(maerkte.Betriebstyp).lower() and "gut" in str(maerkte.Betriebstyp).lower()):
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Edeka"
                    elif "marktkauf" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Marktkauf"
                    elif "kaufland" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Kaufland"
                    elif "coma" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Coma"
                    elif "combi" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Combi"
                    elif "familia" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Famila"
                    elif "globus" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"globus"
                    elif "migros" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Migros"
                    elif "hit" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"HIT"
                    elif "jibi" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Jibi"
                    elif "konsum-leipzig" in str(maerkte.Betriebstyp).lower() or "konsum leipzig" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Konsum-Leipzig"
                    elif "markant" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Markant"
                    elif "rewe" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Rewe"
                    elif "tegut" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"tegut"
                    elif "perfetto" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Perfetto"
                    elif "v-markt" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"V-Markt"
                    elif "wasgau" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Wasgau"
                    elif "toom" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"toom"
                    elif "sky" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Sky"
                    elif "plaza" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"plaza"
                    elif "real" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"real"
                    elif "denns" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"denns"
                    elif "alnatura" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Alnatura"
                    elif "biomarkt" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"biomarkt"
                    elif "basic" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"basic"
                    elif "biocompany" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"biocompany"
                    elif "vitalia" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"vitalia"
                    elif "viv" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"viv"
                    else:
                        try:
                            Name_Markt=str(maerkte.Name_postalisch).split(' ')[0]
                        except:
                ##                        print "fehler namenmarkt"
                            Name_Markt=str(maerkte.Name_postalisch)
                        maerkte.Betreibstyp_bzw_Anbeiter=string+Name_Markt
                ##                    messages.AddMessage("Zuteilung gr. SM nicht moeglich")
                ##                    messages.AddMessage("Unbekannter Betreiber "+str(maerkte.Betriebstyp))
                    cur_Standortdaten.updateRow(maerkte)
                elif maerkte.VKFL_gesamt<=5000:
                    #V-Markt SM Betreiber
                    string="V-Markt "
                    if "edeka" in str(maerkte.Betriebstyp).lower() or ("e" in str(maerkte.Betriebstyp).lower() and ("neukauf" in str(maerkte.Betriebstyp).lower() or "center" in str(maerkte.Betriebstyp).lower()))or ("e" in str(maerkte.Betriebstyp).lower() and "aktiv" in str(maerkte.Betriebstyp).lower() and "markt" in str(maerkte.Betriebstyp).lower())or ("nah" in str(maerkte.Betriebstyp).lower() and "gut" in str(maerkte.Betriebstyp).lower()):
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Edeka"
                    elif "marktkauf" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Marktkauf"
                    elif "kaufland" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Kaufland"
                    elif "coma" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Coma"
                    elif "combi" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Combi"
                    elif "familia" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Famila"
                    elif "globus" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"globus"
                    elif "migros" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Migros"
                    elif "hit" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"HIT"
                    elif "jibi" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Jibi"
                    elif "konsum-leipzig" in str(maerkte.Betriebstyp).lower() or "konsum leipzig" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Konsum-Leipzig"
                    elif "markant" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Markant"
                    elif "rewe" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Rewe"
                    elif "tegut" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"tegut"
                    elif "perfetto" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Perfetto"
                    elif "v-markt" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"V-Markt"
                    elif "wasgau" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Wasgau"
                    elif "toom" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"toom"
                    elif "sky" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Sky"
                    elif "plaza" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"plaza"
                    elif "real" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"real"
                    elif "denns" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"denns"
                    elif "alnatura" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Alnatura"
                    elif "biomarkt" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"biomarkt"
                    elif "basic" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"basic"
                    elif "biocompany" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"biocompany"
                    elif "vitalia" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"vitalia"
                    elif "viv" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"viv"
                    else:
                        try:
                            Name_Markt=str(maerkte.Name_postalisch).split(' ')[0]
                        except:
                ##                        print "fehler namenmarkt"
                            Name_Markt=str(maerkte.Name_postalisch)
                        maerkte.Betreibstyp_bzw_Anbeiter=string+Name_Markt
                ##                    messages.AddMessage("Zuteilung "+string+" nicht moeglich")
                ##                    messages.AddMessage("Unbekannter Betreiber "+str(maerkte.Betriebstyp))
                    cur_Standortdaten.updateRow(maerkte)
                elif maerkte.VKFL_gesamt>5000:
                    #SBW SM Betreiber
                    string="SBW "
                    if "edeka" in str(maerkte.Betriebstyp).lower() or ("e" in str(maerkte.Betriebstyp).lower() and ("neukauf" in str(maerkte.Betriebstyp).lower() or "center" in str(maerkte.Betriebstyp).lower()))or ("e" in str(maerkte.Betriebstyp).lower() and "aktiv" in str(maerkte.Betriebstyp).lower() and "markt" in str(maerkte.Betriebstyp).lower())or ("nah" in str(maerkte.Betriebstyp).lower() and "gut" in str(maerkte.Betriebstyp).lower()):
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Edeka"
                    elif "marktkauf" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Marktkauf"
                    elif "kaufland" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Kaufland"
                    elif "coma" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Coma"
                    elif "combi" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Combi"
                    elif "familia" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Famila"
                    elif "globus" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"globus"
                    elif "migros" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Migros"
                    elif "hit" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"HIT"
                    elif "jibi" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Jibi"
                    elif "konsum-leipzig" in str(maerkte.Betriebstyp).lower() or "konsum leipzig" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Konsum-Leipzig"
                    elif "markant" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Markant"
                    elif "rewe" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Rewe"
                    elif "tegut" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"tegut"
                    elif "perfetto" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Perfetto"
                    elif "v-markt" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"V-Markt"
                    elif "wasgau" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Wasgau"
                    elif "toom" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"toom"
                    elif "sky" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Sky"
                    elif "plaza" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"plaza"
                    elif "real" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"real"
                    elif "denns" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"denns"
                    elif "alnatura" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"Alnatura"
                    elif "biomarkt" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"biomarkt"
                    elif "basic" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"basic"
                    elif "biocompany" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"biocompany"
                    elif "vitalia" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"vitalia"
                    elif "viv" in str(maerkte.Betriebstyp).lower():
                        maerkte.Betreibstyp_bzw_Anbeiter=string+"viv"
                    else:
                        try:
                            Name_Markt=str(maerkte.Name_postalisch).split(' ')[0]
                        except:
                ##                        print "fehler namenmarkt"
                            Name_Markt=str(maerkte.Name_postalisch)
                        maerkte.Betreibstyp_bzw_Anbeiter=string+Name_Markt
                ##                    messages.AddMessage("Zuteilung "+string+" nicht moeglich")
                ##                    messages.AddMessage("Unbekannter Betreiber "+str(maerkte.Betriebstyp))
                    cur_Standortdaten.updateRow(maerkte)



        del cur_Standortdaten,maerkte




    # Sascha bereden - brauche zuteilung aller maerkte zu den typen - sind kl. Nahversorger alle unter 400 m² sofern keine Discounter!

    def Einwohnerfinden(shp_Standortdaten):
        pfad_standort= join(workspace_projekt,shp_Standortdaten)
        pfad_bkg_gemeinden=join(workspace_Basis,"bkg_gemeinden")
        Standortdaten_SpatialJoin = join(workspace_projekt,"Standortdaten_SpatialJoin")

        # Process: Räumliche Verbindung
        arcpy.SpatialJoin_analysis(pfad_standort, pfad_bkg_gemeinden, Standortdaten_SpatialJoin, "JOIN_ONE_TO_ONE", "KEEP_ALL", "Id \"Id\" true true false 4 Long 0 0 ,First,#,"+pfad_standort+",Id,-1,-1;Name_postalisch \"Name_postalisch\" true true false 255 Text 0 0 ,First,#,"+pfad_standort+",Name_postalisch,-1,-1;PLZ \"PLZ\" true true false 4 Long 0 0 ,First,#,"+pfad_standort+",PLZ,-1,-1;Ort \"Ort\" true true false 255 Text 0 0 ,First,#,"+pfad_standort+",Ort,-1,-1;Ortsteil \"Ortsteil\" true true false 255 Text 0 0 ,First,#,"+pfad_standort+",Ortsteil,-1,-1;Strasse \"Strasse\" true true false 255 Text 0 0 ,First,#,"+pfad_standort+",Strasse,-1,-1;HNR \"HNR\" true true false 255 Text 0 0 ,First,#,"+pfad_standort+",HNR,-1,-1;VKFL_Gesamt \"VKFL_Gesamt\" true true false 4 Long 0 0 ,First,#,"+pfad_standort+",VKFL_Gesamt,-1,-1;Euro_pro_quadratmeter_VKF \"Euro_pro_quadratmeter_VKF\" true true false 4 Long 0 0 ,First,#,"+pfad_standort+",Euro_pro_quadratmeter_VKF,-1,-1;Lon \"Lon\" true true false 4 Float 0 0 ,First,#,"+pfad_standort+",Lon,-1,-1;Lat \"Lat\" true true false 4 Float 0 0 ,First,#,"+pfad_standort+",Lat,-1,-1;Qualitaet \"Qualitaet\" true true false 4 Long 0 0 ,First,#,"+pfad_standort+",Qualitaet,-1,-1;Gemeindeklasse \"Gemeindeklasse\" true true false 4 Long 0 0 ,First,#,"+pfad_standort+",Gemeindeklasse,-1,-1;EW_Gemeindeverband \"EW_Gemeindeverband\" true true false 4 Long 0 0 ,First,#,"+pfad_standort+",EW_Gemeindeverband,-1,-1;Betriebstyp_Attraktivitaet \"Betriebstyp_Attraktivitaet\" true true false 255 Text 0 0 ,First,#,"+pfad_standort+",Betriebstyp_Attraktivitaet,-1,-1;Betriebstyp_Funktion \"Betriebstyp_Funktion\" true true false 255 Text 0 0 ,First,#,"+pfad_standort+",Betriebstyp_Funktion,-1,-1;Betriebstyp \"Betriebstyp\" true true false 150 Text 0 0 ,First,#,"+pfad_standort+",Betriebstyp,-1,-1;Bonifaktor \"Bonifaktor\" true true false 8 Double 0 0 ,First,#,"+pfad_standort+",Bonifaktor,-1,-1;Betreibstyp_bzw_Anbeiter \"Betreibstyp_bzw_Anbeiter\" true true false 255 Text 0 0 ,First,#,"+pfad_standort+",Betreibstyp_bzw_Anbeiter,-1,-1;Kaufkraft \"Kaufkraft\" true true false 8 Double 0 0 ,First,#,"+pfad_standort+",Kaufkraft,-1,-1;GEN \"GEN\" true true false 50 Text 0 0 ,First,#,"+pfad_bkg_gemeinden+",GEN,-1,-1;AGS \"AGS\" true true false 12 Text 0 0 ,First,#,"+pfad_bkg_gemeinden+",AGS,-1,-1;EWZ \"EWZ\" true true false 8 Double 0 0 ,First,#,"+pfad_bkg_gemeinden+",EWZ,-1,-1", "INTERSECT", "", "")

        arcpy.CopyFeatures_management(Standortdaten_SpatialJoin, pfad_standort, "", "0", "0", "0")

        try:
            arcpy.Delete_management(Standortdaten_SpatialJoin)
        except:
            pass

        try:
            arcpy.AddField_management(pfad_standort, "EW_Gemeindeverband", "LONG")
        except:
            pass

        arcpy.CalculateField_management(pfad_standort, "EW_Gemeindeverband", "!EWZ!", "PYTHON", "")
        del pfad_bkg_gemeinden,pfad_standort,Standortdaten_SpatialJoin

    def verkaufsflaeche_zent():
        cur_Standortdaten=arcpy.SearchCursor(join(workspace_projekt,"Standortdaten"))
        try:
            arcpy.Delete_management("Verkaufsflaeche")
            arcpy.Delete_management(join(workspace_projekt,"Verkaufsflaeche"))
        except:
            pass
        try:
            arcpy.DeleteFeatures_management("Verkaufsflaeche")
        except:
            pass

        try:

            arcpy.CreateTable_management(workspace_projekt,"Verkaufsflaeche")
        except:

            print"a) Fehler beim erstellen der Tabelle Verkaufsflaeche"
            messages.AddErrorMessage("Verkaufsflaechen Tabelle konnte nicht erstellt werden. Ggf. per Hand loeschen.")
            exit(1)


        try:
            arcpy.AddField_management(join(workspace_projekt,"Verkaufsflaeche"),"Kommune","TEXT")
            arcpy.AddField_management(join(workspace_projekt,"Verkaufsflaeche"),"AGS","TEXT")
            arcpy.AddField_management(join(workspace_projekt,"Verkaufsflaeche"),"Verkaufsflazent","DOUBLE")
            arcpy.AddField_management(join(workspace_projekt,"Verkaufsflaeche"),"Verkaufsflazentpla","DOUBLE")
            arcpy.AddField_management(join(workspace_projekt,"Verkaufsflaeche"),"Delta","DOUBLE")
        except:
            pass


        cur_Search_Sied = arcpy.SearchCursor(join(workspace_projekt,"Siedlungszahlendaten"))

        array_ags=[]
        for zellen in cur_Search_Sied:
            if len(array_ags)==0:
                array_ags.append(int(zellen.AGS))

            else:
                if len([r for r in array_ags if r==int(zellen.AGS)])==0:
                    array_ags.append(int(zellen.AGS))

        del cur_Search_Sied

        array_standortda=[]
        for speicher in cur_Standortdaten:
            if len([k for k in array_ags if k==int(speicher.AGS) ])>0:
                array_standortda.append([speicher.GSBEV,speicher.VKFL_Gesamt,int(speicher.AGS),speicher.GEN])

        del speicher

        ags_gemeinde_flaeche_einw=[]
        for eintraege in array_standortda:
            if len(ags_gemeinde_flaeche_einw)==0:
                ags_gemeinde_flaeche_einw.append([eintraege[2],eintraege[3],eintraege[1],eintraege[0],0])

            else:
                finden=0
                for gen in ags_gemeinde_flaeche_einw:
                    if gen[0]==eintraege[2]:
                        finden=1
                        gen[2]+=eintraege[1]
                        break
                if finden==0:
                    ags_gemeinde_flaeche_einw.append([eintraege[2],eintraege[3],eintraege[1],eintraege[0],0])


        ags_gemeinde_flaeche_einw=sorted(ags_gemeinde_flaeche_einw)
        cur_Sear_GGEN= arcpy.SearchCursor(join(workspace_Basis_Daten,"Gesamtgemeinden"))

        array_GGen=[]
        for speicher in cur_Sear_GGEN:
            array_GGen.append([int(speicher.AGS),speicher.Gen,int(speicher.VAGS),speicher.GGEN])

        del speicher,cur_Sear_GGEN

        array_ggen_umsatz=[]
        for einzelnegen in ags_gemeinde_flaeche_einw:
            found=0
            for gesamtgen in array_GGen:
                if int(einzelnegen[0])== int(gesamtgen[0]):
                    array_ggen_umsatz.append([gesamtgen[2],gesamtgen[3],einzelnegen[2],einzelnegen[3],einzelnegen[4]])
                    found=1
            if found ==0:
                print "Komisch"


        entg_ggen_umsatz=[]
        for asd in array_ggen_umsatz:
            if len(entg_ggen_umsatz)==0:
                entg_ggen_umsatz.append([asd[0],asd[1],asd[2],asd[3],asd[4]])

            else:
                findemich=0
                for allezusam in entg_ggen_umsatz:
                    if allezusam[0]==asd[0]:
                        allezusam[2]+=asd[2]
                        allezusam[3]=asd[3]
                        findemich=1

                if findemich==0:
                    entg_ggen_umsatz.append([asd[0],asd[1],asd[2],asd[3],asd[4]])


        for berechnung in entg_ggen_umsatz:
            try:
                berechnung[4]=float(berechnung[2])/float(berechnung[3])
            except:
                berechnung[4]=0


        entg_ggen_umsatz=sorted(entg_ggen_umsatz)

        cur_Ins_Verlust=arcpy.InsertCursor(join(workspace_projekt,"Verkaufsflaeche"))

        for bb in entg_ggen_umsatz:
            row= cur_Ins_Verlust.newRow()
            row.setValue("Kommune","SG/Stadt "+bb[1])
            row.setValue("AGS",bb[0])
            row.setValue("Verkaufsflazent",bb[4])
            cur_Ins_Verlust.insertRow(row)


        del cur_Ins_Verlust,ags_gemeinde_flaeche_einw,cur_Standortdaten,array_standortda,array_ggen_umsatz,entg_ggen_umsatz

        cur_Standortdaten=arcpy.SearchCursor(join(workspace_projekt,"Standortdaten_planfall"))

        array_standortda=[]
        for speicher in cur_Standortdaten:
            if len([k for k in array_ags if k==int(speicher.AGS) ])>0:
                array_standortda.append([speicher.GSBEV,speicher.VKFL_Gesamt,speicher.AGS,speicher.GEN])

        del speicher
        del array_ags

        ags_gemeinde_flaeche_einw=[]
        for eintraege in array_standortda:
            if len(ags_gemeinde_flaeche_einw)==0:
                ags_gemeinde_flaeche_einw.append([eintraege[2],eintraege[3],eintraege[1],eintraege[0],0])

            else:
                finden=0
                for gen in ags_gemeinde_flaeche_einw:
                    if gen[0]==eintraege[2]:
                        finden=1
                        gen[2]+=eintraege[1]
                        break
                if finden==0:
                    ags_gemeinde_flaeche_einw.append([eintraege[2],eintraege[3],eintraege[1],eintraege[0],0])



        ags_gemeinde_flaeche_einw=sorted(ags_gemeinde_flaeche_einw)
        cur_Sear_GGEN= arcpy.SearchCursor(join(workspace_Basis_Daten,"Gesamtgemeinden"))

        array_GGen=[]
        for speicher in cur_Sear_GGEN:
            array_GGen.append([int(speicher.AGS),speicher.Gen,int(speicher.VAGS),speicher.GGEN])

        del speicher,cur_Sear_GGEN

        array_ggen_umsatz=[]
        for einzelnegen in ags_gemeinde_flaeche_einw:
            found=0
            for gesamtgen in array_GGen:
                if int(einzelnegen[0])== int(gesamtgen[0]):
                    array_ggen_umsatz.append([gesamtgen[2],gesamtgen[3],einzelnegen[2],einzelnegen[3],einzelnegen[4]])
                    found=1
            if found ==0:
                print "Komisch"


        entg_ggen_umsatz=[]
        for asd in array_ggen_umsatz:
            if len(entg_ggen_umsatz)==0:
                entg_ggen_umsatz.append([asd[0],asd[1],asd[2],asd[3],asd[4]])

            else:
                findemich=0
                for allezusam in entg_ggen_umsatz:
                    if allezusam[0]==asd[0]:
                        allezusam[2]+=asd[2]
                        allezusam[3]=asd[3]
                        findemich=1

                if findemich==0:
                    entg_ggen_umsatz.append([asd[0],asd[1],asd[2],asd[3],asd[4]])


        for berechnung in entg_ggen_umsatz:
            try:
        ##        berechnung[4]=((berechnung[2]/berechnung[3])*100)-100
                berechnung[4]=float(berechnung[2])/float(berechnung[3])

            except:
                berechnung[4]=0


        entg_ggen_umsatz=sorted(entg_ggen_umsatz)

        cur_Up_Verlust=arcpy.UpdateCursor(join(workspace_projekt,"Verkaufsflaeche"))
        for updating in cur_Up_Verlust:
            findemich=0
            for arrayeintraege in entg_ggen_umsatz:

                if int( updating.AGS) == int( arrayeintraege[0]):
                    findemich=1
                    updating.setValue("Verkaufsflazentpla",arrayeintraege[4])
                    cur_Up_Verlust.updateRow(updating)
            if findemich==0:
                cur_Ins_Verlust=arcpy.InsertCursor(join(workspace_projekt,"Verkaufsflaeche"))
                ruw= cur_Ins_Verlust.newRow()
                ruw.setValue("Kommune","SG/Stadt "+arrayeintraege[1])
                ruw.setValue("AGS",arrayeintraege[0])
                ruw.setValue("Verkaufsflazent",0)
                ruw.setValue("Verkaufsflazentpla",arrayeintraege[4])
                cur_Ins_Verlust.insertRow(ruw)
                del cur_Ins_Verlust

        del ags_gemeinde_flaeche_einw,cur_Standortdaten,array_standortda,entg_ggen_umsatz
        arcpy.CalculateField_management(join(workspace_projekt,"Verkaufsflaeche"), "Delta", "-!Verkaufsflazent!+!Verkaufsflazentpla!", "PYTHON", "")
        cur_Check_Verk= arcpy.UpdateCursor(join(workspace_projekt,"Verkaufsflaeche"))
        for a in cur_Check_Verk:
            if a.Verkaufsflazent==0. and a.Verkaufsflazentpla ==0.:
                cur_Check_Verk.deleteRow(a)

        del cur_Check_Verk


    def betriebstyp_bestimmung(shp_Standortdaten):
        #shp_Standortdaten

        # Zusatzspalte mit Betriebstyp fuer Attraktivitaet
        try:
            arcpy.AddField_management(join(workspace_projekt,shp_Standortdaten), "Betriebstyp_Attraktivitaet", "TEXT",250)
            arcpy.AddField_management(join(workspace_projekt,shp_Standortdaten), "Gemeindeklasse", "LONG")
        except:
            pass
        #Cursor drauf
        cur_Standortdaten=arcpy.UpdateCursor(join(workspace_projekt,shp_Standortdaten))
        cur_Attraktivitaet_Info=arcpy.SearchCursor(join(workspace_Basis_Daten,"Attraktivitaet_Info"))

        Discounter=['Aktiv-Discount','e aktiv','diska','Netto(Edeka)','Netto','Lidl','Aldi','Penny','Norma','NP','treff 3000']



        array_Attraktivitaet_Info=[]
        for zeile in cur_Attraktivitaet_Info:
            array_Attraktivitaet_Info.append([zeile.Typ,zeile.ein_Markt_in_der_Naehe,zeile.zwei_Maerkte_in_der_Naehe,zeile.drei_Maerkte_in_der_Naehe,zeile.zweiter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe,zeile.dritter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe,zeile.dritter_Markt_wenn_erster_und_zweiter_Markt_mit_Abstand_in_der_N])

        del zeile,cur_Attraktivitaet_Info
    ##=WENN(N4>=100000;1;WENN(N4>=50000;2;WENN(N4>=20000;3;WENN(N4>=10000;4;WENN(N4>=1;5;0)))))
        #   AENDERUNG 8.3. EZ_Gemeindeverband zu GSBEV
        for row_standort in cur_Standortdaten:
            gefunden =0
            if row_standort.GSBEV>=100000:
                row_standort.Gemeindeklasse=1
            elif row_standort.GSBEV>=50000:
                row_standort.Gemeindeklasse=2
            elif row_standort.GSBEV>=20000:
                row_standort.Gemeindeklasse=3
            elif row_standort.GSBEV>=10000:
                row_standort.Gemeindeklasse=4
            elif row_standort.GSBEV>=1:
                row_standort.Gemeindeklasse=5
            else :
                row_standort.Gemeindeklasse=0

            #Variable SM kritisch
            for row_attraktiv in array_Attraktivitaet_Info:
                if row_standort.Betreibstyp_bzw_Anbeiter==row_attraktiv[0]  and "allg." not in row_standort.Betreibstyp_bzw_Anbeiter :
            ##                print "gefunden" , row_standort.Betreibstyp_bzw_Anbeiter
                    gefunden =1
                    row_standort.Betriebstyp_Attraktivitaet=row_standort.Betreibstyp_bzw_Anbeiter
                    cur_Standortdaten.updateRow(row_standort)
                    break
            del row_attraktiv

            if gefunden==0:
        ##            print "nicht gefunden"
        ##            print row_standort.Betreibstyp_bzw_Anbeiter
        ##            print len(row_standort.Betreibstyp_bzw_Anbeiter)
        ##            print row_standort.Betreibstyp_bzw_Anbeiter
        ##            print "edeka" in str(row_standort.Betreibstyp_bzw_Anbeiter).lower()
        ##            print

                variable=0
                if "allg." in  str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                    variable=1
                    print row_standort.Betreibstyp_bzw_Anbeiter


                if [f for f in Discounter if str(row_standort.Betreibstyp_bzw_Anbeiter).lower() in f.lower() ] and [c for c in array_Attraktivitaet_Info if  str(row_standort.Betreibstyp_bzw_Anbeiter).lower() != c[0].lower()] and variable==0 :
                    cur_IAttraktivitaet_Info=arcpy.InsertCursor(join(workspace_Basis_Daten,"Attraktivitaet_Info"))
                    row_cur_IAttraktivitaet_Info=cur_IAttraktivitaet_Info.newRow()
                    row_cur_IAttraktivitaet_Info.setValue("Typ",str(row_standort.Betreibstyp_bzw_Anbeiter))
                    row_cur_IAttraktivitaet_Info.setValue("ein_Markt_in_der_Naehe",1)
                    row_cur_IAttraktivitaet_Info.setValue("zwei_Maerkte_in_der_Naehe",0.59)
                    row_cur_IAttraktivitaet_Info.setValue("drei_Maerkte_in_der_Naehe",0.59)
                    row_cur_IAttraktivitaet_Info.setValue("zweiter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.34)
                    row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.06)
                    row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_und_zweiter_Markt_mit_Abstand_in_der_N",0.06)
                    cur_IAttraktivitaet_Info.insertRow(row_cur_IAttraktivitaet_Info)

                    del cur_IAttraktivitaet_Info
                    array_Attraktivitaet_Info.append([str(row_standort.Betreibstyp_bzw_Anbeiter),1,0.59,0.59,0.34,0.06,0.06])
                    row_standort.Betriebstyp_Attraktivitaet=str(row_standort.Betreibstyp_bzw_Anbeiter)
                    cur_Standortdaten.updateRow(row_standort)
            ##                print row_standort.Betreibstyp_bzw_Anbeiter
                elif "kaufland" in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                    row_standort.Betriebstyp_Attraktivitaet="gr.mittl.SM-V-Markt-SBW Kaufland"
                    cur_Standortdaten.updateRow(row_standort)



                elif "edeka" in str(row_standort.Betreibstyp_bzw_Anbeiter).lower() and "marktkauf" != row_standort.Name_postalisch.lower() :
                    if row_standort.VKFL_Gesamt<=800 and row_standort.VKFL_Gesamt>400:
                ##                    print "Zugeteilt zu kl. SM Edeka"
                        row_standort.Betriebstyp_Attraktivitaet="kl. SM Edeka"
                        cur_Standortdaten.updateRow(row_standort)
                    elif row_standort.VKFL_Gesamt>800:
                ##                    print "Zugeteilt zu gr. mittl. SM, V-Markt, SBW Edeka"
                        row_standort.Betriebstyp_Attraktivitaet="gr.mittl.SM-V-Markt-SBW Edeka"
                        cur_Standortdaten.updateRow(row_standort)
                    else:
                        print "Fehler zuordnung edeka"
                elif "edeka" in str(row_standort.Betreibstyp_bzw_Anbeiter).lower() and "marktkauf" == row_standort.Name_postalisch.lower():
                    vorhanden =0
                    if row_standort.VKFL_Gesamt<=800 and row_standort.VKFL_Gesamt>400:
                ##                    print "Zugeteilt zu kl. SM Marktkauf edeka"
                        for schaunach in array_Attraktivitaet_Info:
                            if "kl. SM Marktkauf" == schaunach[0]:
                                vorhanden=1
                                row_standort.Betriebstyp_Attraktivitaet="kl. SM Marktkauf"
                                cur_Standortdaten.updateRow(row_standort)
                                break
                        if vorhanden==0:
                            cur_IAttraktivitaet_Info=arcpy.InsertCursor(join(workspace_Basis_Daten,"Attraktivitaet_Info"))
                            row_cur_IAttraktivitaet_Info=cur_IAttraktivitaet_Info.newRow()
                            row_cur_IAttraktivitaet_Info.setValue("Typ","kl. SM Marktkauf")
                            row_cur_IAttraktivitaet_Info.setValue("ein_Markt_in_der_Naehe",1)
                            row_cur_IAttraktivitaet_Info.setValue("zwei_Maerkte_in_der_Naehe",0.87)
                            row_cur_IAttraktivitaet_Info.setValue("drei_Maerkte_in_der_Naehe",0.58)
                            row_cur_IAttraktivitaet_Info.setValue("zweiter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.44)
                            row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.32)
                            row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_und_zweiter_Markt_mit_Abstand_in_der_N",0.32)
                            cur_IAttraktivitaet_Info.insertRow(row_cur_IAttraktivitaet_Info)

                            del cur_IAttraktivitaet_Info
                            array_Attraktivitaet_Info.append(["kl. SM Marktkauf",1,0.87,0.58,0.44,0.32,0.32])



                            row_standort.Betriebstyp_Attraktivitaet="kl. SM Marktkauf"
                            cur_Standortdaten.updateRow(row_standort)

                    #gefaehrliche stelle
                    elif row_standort.VKFL_Gesamt>800:
                ##                    print "Zugeteilt zu gr. mittl. SM, V-Markt, SBW Edeka"
                        for schaunach in array_Attraktivitaet_Info:
                            if "gr.mittl.SM-V-Markt Marktkauf" == schaunach[0]:
                                vorhanden=1
                                row_standort.Betriebstyp_Attraktivitaet="gr.mittl.SM-V-Markt-SBW Marktkauf"
                                cur_Standortdaten.updateRow(row_standort)
                                break

                        if vorhanden==0:
                            cur_IAttraktivitaet_Info=arcpy.InsertCursor(join(workspace_Basis_Daten,"Attraktivitaet_Info"))
                            row_cur_IAttraktivitaet_Info=cur_IAttraktivitaet_Info.newRow()
                            row_cur_IAttraktivitaet_Info.setValue("Typ","gr.mittl.SM-V-Markt-SBW Marktkauf")
                            row_cur_IAttraktivitaet_Info.setValue("ein_Markt_in_der_Naehe",1)
                            row_cur_IAttraktivitaet_Info.setValue("zwei_Maerkte_in_der_Naehe",0.7)
                            row_cur_IAttraktivitaet_Info.setValue("drei_Maerkte_in_der_Naehe",0.5)
                            row_cur_IAttraktivitaet_Info.setValue("zweiter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.3)
                            row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.1)
                            row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_und_zweiter_Markt_mit_Abstand_in_der_N",0.05)
                            cur_IAttraktivitaet_Info.insertRow(row_cur_IAttraktivitaet_Info)

                            del cur_IAttraktivitaet_Info
                            array_Attraktivitaet_Info.append(["gr.mittl.SM-V-Markt-SBW Marktkauf",1,0.7,0.5,0.3,0.1,0.05])
                            row_standort.Betriebstyp_Attraktivitaet="gr.mittl.SM-V-Markt-SBW Marktkauf"
                            cur_Standortdaten.updateRow(row_standort)
                    else:
                        print "Fehler zuordnung Marktkauf"

                elif "sky" in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                    if row_standort.VKFL_Gesamt>800:
                ##                    print "Zugeteilt zu gr. mittl. SM, V-Markt, SBW Edeka"
                        row_standort.Betriebstyp_Attraktivitaet="gr.mittl.SM-V-Markt-SBW Sky"
                        cur_Standortdaten.updateRow(row_standort)
                    else:
                        print "Fehler zuordnung sky"

                elif "rewe" in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                    if row_standort.VKFL_Gesamt<=800 and row_standort.VKFL_Gesamt>400:
                ##                    print "Zugeteilt zu kl. SM Rewe"
                        row_standort.Betriebstyp_Attraktivitaet="kl. SM Rewe"
                        cur_Standortdaten.updateRow(row_standort)
                    elif row_standort.VKFL_Gesamt>800:
                ##                    print "Zugeteilt zu gr. mittl. SM, V-Markt, SBW Rewe"
                        row_standort.Betriebstyp_Attraktivitaet="gr.mittl.SM-V-Markt-SBW Rewe"
                        cur_Standortdaten.updateRow(row_standort)
                    else:
                        print "Fehler zuordnung Rewe"

                elif "famila" in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():

            ##                    print "Zugeteilt zu V-Markt-SBW-Famila"
                    row_standort.Betriebstyp_Attraktivitaet="gr.mittl.SM-V-Markt-SBW Famila"
                    cur_Standortdaten.updateRow(row_standort)

            ##            elif "sbw" in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
            ##                    vorhanden=0
            ##                    try:
            ##                        Name_Markt=str(row_standort.Name_postalisch).split(' ')[0]
            ##                    except:
            ####                        print "fehler namenmarkt"
            ##                        Name_Markt=str(row_standort.Name_postalisch)
            ##
            ##                    for schaunach in array_Attraktivitaet_Info:
            ##                        if "SBW "+ str(Name_Markt) == schaunach[0]:
            ##                            vorhanden=1
            ##                            row_standort.Betriebstyp_Attraktivitaet=schaunach[0]
            ##                            cur_Standortdaten.updateRow(row_standort)
            ##                            break
            ##
            ##                    if vorhanden==0:
            ##                        cur_IAttraktivitaet_Info=arcpy.InsertCursor(join(workspace_Basis_Daten,"Attraktivitaet_Info"))
            ##                        row_cur_IAttraktivitaet_Info=cur_IAttraktivitaet_Info.newRow()
            ##
            ##                        row_cur_IAttraktivitaet_Info.setValue("Typ","SBW "+ str(Name_Markt))
            ##                        row_cur_IAttraktivitaet_Info.setValue("ein_Markt_in_der_Naehe",1)
            ##                        row_cur_IAttraktivitaet_Info.setValue("zwei_Maerkte_in_der_Naehe",0.7)
            ##                        row_cur_IAttraktivitaet_Info.setValue("drei_Maerkte_in_der_Naehe",0.5)
            ##                        row_cur_IAttraktivitaet_Info.setValue("zweiter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.3)
            ##                        row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.1)
            ##                        row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_und_zweiter_Markt_mit_Abstand_in_der_N",0.05)
            ##                        cur_IAttraktivitaet_Info.insertRow(row_cur_IAttraktivitaet_Info)
            ##
            ##                        del cur_IAttraktivitaet_Info
            ##                        array_Attraktivitaet_Info.append(["SBW "+row_standort.Betreibstyp_bzw_Anbeiter,1,0.7,0.5,0.3,0.1,0.05])
            ##
            ##
            ##
            ##                        row_standort.Betriebstyp_Attraktivitaet=str("SBW "+ str(Name_Markt))
            ##                        cur_Standortdaten.updateRow(row_standort)
                elif "v-markt" in str(row_standort.Betreibstyp_bzw_Anbeiter).lower() or "sbw" in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                    vorhanden=0
                    try:
                        Name_Markt=str(row_standort.Name_postalisch).split(' ')[0]
                    except:
                        Name_Markt=str(row_standort.Name_postalisch)

                    for schaunach in array_Attraktivitaet_Info:
                        if "gr.mittl.SM-V-Markt-SBW "+ str(Name_Markt) == schaunach[0]:
                            vorhanden=1
                            row_standort.Betriebstyp_Attraktivitaet=schaunach[0]
                            cur_Standortdaten.updateRow(row_standort)
                            break

                    if vorhanden==0:
                        cur_IAttraktivitaet_Info=arcpy.InsertCursor(join(workspace_Basis_Daten,"Attraktivitaet_Info"))
                        row_cur_IAttraktivitaet_Info=cur_IAttraktivitaet_Info.newRow()

                        row_cur_IAttraktivitaet_Info.setValue("Typ","gr.mittl.SM-V-Markt-SBW "+ str(Name_Markt))
                        row_cur_IAttraktivitaet_Info.setValue("ein_Markt_in_der_Naehe",1)
                        row_cur_IAttraktivitaet_Info.setValue("zwei_Maerkte_in_der_Naehe",0.7)
                        row_cur_IAttraktivitaet_Info.setValue("drei_Maerkte_in_der_Naehe",0.5)
                        row_cur_IAttraktivitaet_Info.setValue("zweiter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.3)
                        row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.1)
                        row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_und_zweiter_Markt_mit_Abstand_in_der_N",0.05)
                        cur_IAttraktivitaet_Info.insertRow(row_cur_IAttraktivitaet_Info)

                        del cur_IAttraktivitaet_Info
                        array_Attraktivitaet_Info.append(["gr.mittl.SM-V-Markt-SBW "+ str(Name_Markt),1,0.7,0.5,0.3,0.1,0.05])

                        row_standort.Betriebstyp_Attraktivitaet="gr.mittl.SM-V-Markt-SBW "+ str(Name_Markt)
                        cur_Standortdaten.updateRow(row_standort)


                else:
                    #Es sind somit SM
                    if row_standort.VKFL_Gesamt<=800 and row_standort.VKFL_Gesamt>400:
                ##                    print "Zugeteilt zu kl. SM allg."
                        vorhanden=0
                        try:
                            Name_Markt=str(row_standort.Name_postalisch).split(' ')[0]
                        except:
                ##                        print "fehler namenmarkt " +row_standort.Name_postalisch
                            Name_Markt=str(row_standort.Name_postalisch)

                        for schaunach in array_Attraktivitaet_Info:
                            if "kl. SM "+ str(Name_Markt) == schaunach[0]:
                                vorhanden=1
                                row_standort.Betriebstyp_Attraktivitaet=schaunach[0]
                                cur_Standortdaten.updateRow(row_standort)
                                break

                        if vorhanden==0:
                            cur_IAttraktivitaet_Info=arcpy.InsertCursor(join(workspace_Basis_Daten,"Attraktivitaet_Info"))
                            row_cur_IAttraktivitaet_Info=cur_IAttraktivitaet_Info.newRow()

                            row_cur_IAttraktivitaet_Info.setValue("Typ","kl. SM "+ str(Name_Markt))
                            row_cur_IAttraktivitaet_Info.setValue("ein_Markt_in_der_Naehe",1)
                            row_cur_IAttraktivitaet_Info.setValue("zwei_Maerkte_in_der_Naehe",0.87)
                            row_cur_IAttraktivitaet_Info.setValue("drei_Maerkte_in_der_Naehe",0.58)
                            row_cur_IAttraktivitaet_Info.setValue("zweiter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.44)
                            row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.32)
                            row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_und_zweiter_Markt_mit_Abstand_in_der_N",0.32)
                            cur_IAttraktivitaet_Info.insertRow(row_cur_IAttraktivitaet_Info)

                            del cur_IAttraktivitaet_Info
                            array_Attraktivitaet_Info.append(["kl. SM "+ str(Name_Markt),1,0.87,0.58,0.44,0.32,0.32])

                            row_standort.Betriebstyp_Attraktivitaet="kl. SM "+ str(Name_Markt)
                            cur_Standortdaten.updateRow(row_standort)

                    elif row_standort.VKFL_Gesamt>800 and row_standort.VKFL_Gesamt<=1500:
                ##                    print "Zugeteilt zu mttl. SM allg"
                        vorhanden=0
                        try:
                            Name_Markt=str(row_standort.Name_postalisch).split(' ')[0]
                        except:
                ##                            print "fehler namenmarkt"
                            Name_Markt=str(row_standort.Name_postalisch)

                        for schaunach in array_Attraktivitaet_Info:
                            if "gr.mittl.SM-V-Markt-SBW "+ str(Name_Markt) == schaunach[0]:
                                vorhanden=1
                                row_standort.Betriebstyp_Attraktivitaet=schaunach[0]
                                cur_Standortdaten.updateRow(row_standort)
                                break

                        if vorhanden==0:
                            cur_IAttraktivitaet_Info=arcpy.InsertCursor(join(workspace_Basis_Daten,"Attraktivitaet_Info"))
                            row_cur_IAttraktivitaet_Info=cur_IAttraktivitaet_Info.newRow()

                            row_cur_IAttraktivitaet_Info.setValue("Typ","gr.mittl.SM-V-Markt-SBW "+ str(Name_Markt))
                            row_cur_IAttraktivitaet_Info.setValue("ein_Markt_in_der_Naehe",1)
                            row_cur_IAttraktivitaet_Info.setValue("zwei_Maerkte_in_der_Naehe",0.7)
                            row_cur_IAttraktivitaet_Info.setValue("drei_Maerkte_in_der_Naehe",0.5)
                            row_cur_IAttraktivitaet_Info.setValue("zweiter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.3)
                            row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.1)
                            row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_und_zweiter_Markt_mit_Abstand_in_der_N",0.05)
                            cur_IAttraktivitaet_Info.insertRow(row_cur_IAttraktivitaet_Info)

                            del cur_IAttraktivitaet_Info
                            array_Attraktivitaet_Info.append(["gr.mittl.SM-V-Markt-SBW "+ str(Name_Markt),1,0.7,0.5,0.3,0.1,0.05])

                            row_standort.Betriebstyp_Attraktivitaet="gr.mittl.SM-V-Markt-SBW "+ str(Name_Markt)
                            cur_Standortdaten.updateRow(row_standort)

                    elif row_standort.VKFL_Gesamt>1500 and row_standort.VKFL_Gesamt<=2500:
                ##                    print "Zugeteilt zu mttl. SM allg"
                        vorhanden=0
                        try:
                            Name_Markt=str(row_standort.Name_postalisch).split(' ')[0]
                        except:
                ##                        print "fehler namenmarkt"
                            Name_Markt=str(row_standort.Name_postalisch)

                        for schaunach in array_Attraktivitaet_Info:
                            if "gr.mittl.SM-V-Markt-SBW "+ str(Name_Markt) == schaunach[0]:
                                vorhanden=1
                                row_standort.Betriebstyp_Attraktivitaet=schaunach[0]
                                cur_Standortdaten.updateRow(row_standort)
                                break

                        if vorhanden==0:
                            cur_IAttraktivitaet_Info=arcpy.InsertCursor(join(workspace_Basis_Daten,"Attraktivitaet_Info"))
                            row_cur_IAttraktivitaet_Info=cur_IAttraktivitaet_Info.newRow()

                            row_cur_IAttraktivitaet_Info.setValue("Typ","gr.mittl.SM-V-Markt-SBW "+ str(Name_Markt))
                            row_cur_IAttraktivitaet_Info.setValue("ein_Markt_in_der_Naehe",1)
                            row_cur_IAttraktivitaet_Info.setValue("zwei_Maerkte_in_der_Naehe",0.7)
                            row_cur_IAttraktivitaet_Info.setValue("drei_Maerkte_in_der_Naehe",0.5)
                            row_cur_IAttraktivitaet_Info.setValue("zweiter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.3)
                            row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe",0.1)
                            row_cur_IAttraktivitaet_Info.setValue("dritter_Markt_wenn_erster_und_zweiter_Markt_mit_Abstand_in_der_N",0.05)
                            cur_IAttraktivitaet_Info.insertRow(row_cur_IAttraktivitaet_Info)

                            del cur_IAttraktivitaet_Info
                            array_Attraktivitaet_Info.append(["gr.mittl.SM-V-Markt-SBW "+ str(Name_Markt),1,0.7,0.5,0.3,0.1,0.05])

                            row_standort.Betriebstyp_Attraktivitaet="gr.mittl.SM-V-Markt-SBW "+ str(Name_Markt)
                            cur_Standortdaten.updateRow(row_standort)

                    else:
                        print "Fehler zuordnung "
                        print row_standort.Id


        del cur_Standortdaten,row_standort,array_Attraktivitaet_Info

    def betriebstyp_bestimmung_expF(shp_Standortdaten):
        #shp_Standortdaten
        try:

        # Zusatzspalte mit Betriebstyp fuer Attraktivitaet
            arcpy.AddField_management(join(workspace_projekt,shp_Standortdaten), "Betriebstyp_Funktion", "TEXT",250)
        except:
            pass
        #Cursor drauf
        cur_Standortdaten=arcpy.UpdateCursor(join(workspace_projekt,shp_Standortdaten))


        cur_ueber100kEW=arcpy.SearchCursor(join(workspace_Basis_Daten,"Ueber_100kEW"))

        Discounter=['Aktiv-Discount','e aktiv','diska','Netto(Edeka)','Netto','Lidl','Aldi','Penny','Norma','NP','treff 3000']

        array_ueber100kEw=[]
        for zeile in cur_ueber100kEW:
            array_ueber100kEw.append(zeile.Typ)

        del zeile,cur_ueber100kEW

        for row_standort in cur_Standortdaten:
            if row_standort.Betreibstyp_bzw_Anbeiter.lower() == 'Aldi'.lower():
                row_standort.Betriebstyp_Funktion='Aldi'
                cur_Standortdaten.updateRow(row_standort)
            elif row_standort.Betreibstyp_bzw_Anbeiter.lower() == 'Lidl'.lower():
                row_standort.Betriebstyp_Funktion='Lidl'
                cur_Standortdaten.updateRow(row_standort)
            elif row_standort.Betreibstyp_bzw_Anbeiter.lower() == 'Netto(Edeka)'.lower():
                row_standort.Betriebstyp_Funktion='Netto(Edeka)'
                cur_Standortdaten.updateRow(row_standort)
            elif row_standort.Betreibstyp_bzw_Anbeiter.lower() == 'Penny'.lower() or row_standort.Betreibstyp_bzw_Anbeiter.lower() == 'Netto(dsk)'.lower() or row_standort.Betreibstyp_bzw_Anbeiter.lower() == 'Norma'.lower():
                row_standort.Betriebstyp_Funktion='Penny'
                cur_Standortdaten.updateRow(row_standort)
            elif  'edeka' in str(row_standort.Betreibstyp_bzw_Anbeiter).lower() or  'rewe' in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():

                if row_standort.VKFL_Gesamt>400 and row_standort.VKFL_Gesamt<801:
                    if 'edeka' in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                        row_standort.Betriebstyp_Funktion='kl. SM Edeka'
                        cur_Standortdaten.updateRow(row_standort)
                    else:
                        row_standort.Betriebstyp_Funktion='kl. SM Rewe'
                        cur_Standortdaten.updateRow(row_standort)
                elif row_standort.VKFL_Gesamt>800 and row_standort.VKFL_Gesamt<1501:
                    if 'edeka' in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                        row_standort.Betriebstyp_Funktion='mittl. SM Edeka'
                        cur_Standortdaten.updateRow(row_standort)
                    else:
                        row_standort.Betriebstyp_Funktion='mittl. SM Rewe'
                        cur_Standortdaten.updateRow(row_standort)

                elif row_standort.VKFL_Gesamt>1500 and row_standort.VKFL_Gesamt<2501:
                    if 'edeka' in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                        row_standort.Betriebstyp_Funktion='gr. SM Edeka'
                        cur_Standortdaten.updateRow(row_standort)
                    else:
                        row_standort.Betriebstyp_Funktion='gr. SM Rewe'
                        cur_Standortdaten.updateRow(row_standort)
                elif row_standort.VKFL_Gesamt>2500 and row_standort.VKFL_Gesamt<5001:
                    if 'edeka' in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                        row_standort.Betriebstyp_Funktion='V-Markt Edeka'
                        cur_Standortdaten.updateRow(row_standort)
                    else:
                        row_standort.Betriebstyp_Funktion='V-Markt Rewe'
                        cur_Standortdaten.updateRow(row_standort)
                elif row_standort.VKFL_Gesamt>5000 :
                    if 'edeka' in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                        row_standort.Betriebstyp_Funktion='SBW Edeka'
                        cur_Standortdaten.updateRow(row_standort)
                    else:
                        row_standort.Betriebstyp_Funktion='SBW-Rewe'
                        cur_Standortdaten.updateRow(row_standort)
            elif 'famila' in str(row_standort.Betreibstyp_bzw_Anbeiter).lower():
                if row_standort.VKFL_Gesamt>2500 and row_standort.VKFL_Gesamt<5001:
                    row_standort.Betriebstyp_Funktion='V-Markt allg.'
                    cur_Standortdaten.updateRow(row_standort)
                elif row_standort.VKFL_Gesamt>5000:
                    row_standort.Betriebstyp_Funktion='SBW-Famila'
                    cur_Standortdaten.updateRow(row_standort)
                else:
                    row_standort.Betriebstyp_Funktion='gr. SM Famila'
                    cur_Standortdaten.updateRow(row_standort)

            elif  ([f for f in Discounter if str(row_standort.Betreibstyp_bzw_Anbeiter).lower() == f.lower() ]):
                row_standort.Betriebstyp_Funktion=row_standort.Betreibstyp_bzw_Anbeiter
                cur_Standortdaten.updateRow(row_standort)

            elif  ([f for f in Discounter if str(row_standort.Betreibstyp_bzw_Anbeiter).lower() != f.lower() ] and  row_standort.VKFL_Gesamt<401) or row_standort.Betreibstyp_bzw_Anbeiter == 'kl. Nahversorgungsmarkt' :
                row_standort.Betriebstyp_Funktion='kl. Nahversorgungsmarkt'
                cur_Standortdaten.updateRow(row_standort)

            elif  ([f for f in array_ueber100kEw if str(row_standort.Betreibstyp_bzw_Anbeiter).lower() == f.lower() ]):
                row_standort.Betriebstyp_Funktion=row_standort.Betreibstyp_bzw_Anbeiter
                cur_Standortdaten.updateRow(row_standort)

            elif row_standort.VKFL_Gesamt>400 and row_standort.VKFL_Gesamt<801:
                row_standort.Betriebstyp_Funktion='kl. SM allg.'
                cur_Standortdaten.updateRow(row_standort)
            elif row_standort.VKFL_Gesamt>800 and row_standort.VKFL_Gesamt<1501:
                row_standort.Betriebstyp_Funktion='mittl. SM allg.'
                cur_Standortdaten.updateRow(row_standort)
            elif row_standort.VKFL_Gesamt>1500 and row_standort.VKFL_Gesamt<2501:
                row_standort.Betriebstyp_Funktion='gr. SM allg.'
                cur_Standortdaten.updateRow(row_standort)
            elif row_standort.VKFL_Gesamt>2500 and row_standort.VKFL_Gesamt<5001:
                row_standort.Betriebstyp_Funktion='V-Markt allg.'
                cur_Standortdaten.updateRow(row_standort)
            elif row_standort.VKFL_Gesamt>5000 :
                row_standort.Betriebstyp_Funktion='SBW allg.'
                cur_Standortdaten.updateRow(row_standort)
            else:
                print "FEHLER"
                print row_standort.Betreibstyp_bzw_Anbeiter
                print

        del cur_Standortdaten,row_standort

    def EWZ_GGAGS_bestimmen(shp_Standortdaten):
        #ich muss aus ags gags machen
        # alle ags des gleichen werts zusammen + bev
        #ags den gags zuordnen und bev zusammen ermitteln
        cur_Standort = arcpy.SearchCursor(join(workspace_projekt,shp_Standortdaten))
        array_standort_ags_bev_gags_gbev=[]
        for a in cur_Standort:
            if len(array_standort_ags_bev_gags_gbev)==0:
                array_standort_ags_bev_gags_gbev.append([int(a.AGS),int(a.EW_Gemeindeverband),0,0])
            else:
                found =0
                for b in array_standort_ags_bev_gags_gbev:
                    if b[0]==int(a.AGS):
                        #Da EZ_Gemeindeverband bereits immer eine summe ist brauchen die nicht addiert werden
                ##                b[1]+=a.EW_Gemeindeverband
                        found=1
                        break
                if found ==0:
                    array_standort_ags_bev_gags_gbev.append([int(a.AGS),int(a.EW_Gemeindeverband),0,0])


        del a, cur_Standort

        ##print len(array_standort_ags_bev_gags_gbev) , array_standort_ags_bev_gags_gbev
        cur_Sear_GGEN= arcpy.SearchCursor(join(workspace_Basis_Daten,"Gesamtgemeinden"))

        array_ags_gags=[]
        for speicher in cur_Sear_GGEN:
            array_ags_gags.append([int(speicher.AGS),int(speicher.VAGS)])

        del speicher,cur_Sear_GGEN

        for z in array_standort_ags_bev_gags_gbev:
            for u in array_ags_gags:
                if z[0]==u[0]:
                    z[2]=u[1]
                    break


        #Problem
        #eine gags ist nicht immer vollkommen im projekt vorhanden
        #deshalb ->ags und bev aus kommunen feature
        # dann gags und bev addieren
        # das ergebniss dann mit array_ags_bev_gags_gbev verschneiden

        cur_Kommune = arcpy.SearchCursor(join(workspace_Basis,"bkg_gemeinden"))
        array_bkggem_ags_bev_gags=[]
        for uu in cur_Kommune:
            array_bkggem_ags_bev_gags.append([int(uu.AGS),int(uu.EWZ),0])

        del cur_Kommune,uu


        for tt in array_bkggem_ags_bev_gags:
            for aa in array_ags_gags:
                if(aa[0]==tt[0]):
                    tt[2]=aa[1]
                    break

        array_ags_bev_gags=[]
        for ee in array_bkggem_ags_bev_gags:
            if len(array_ags_bev_gags)==0:
                array_ags_bev_gags.append([ee[0],ee[1],ee[2]])

            else:
                found=0
                for qq in array_ags_bev_gags:
                    if qq[2]==ee[2]:
                        qq[1]+=ee[1]
                        found=1
                        break

                if found==0:
                    array_ags_bev_gags.append([ee[0],ee[1],ee[2]])

        ##print array_ags_bev_gags


        for i in array_standort_ags_bev_gags_gbev:
            for m in array_ags_bev_gags:
                if i[2]==m[2]:
                    i[3]=m[1]
                    break




        print array_standort_ags_bev_gags_gbev

        try:

            arcpy.AddField_management(join(workspace_projekt,shp_Standortdaten),"GSAGS","LONG")
            arcpy.AddField_management(join(workspace_projekt,shp_Standortdaten),"GSBEV","LONG")
        except:
            print "error im added"
            pass

        cur_UP_Stand= arcpy.UpdateCursor(join(workspace_projekt,shp_Standortdaten))

        for p in cur_UP_Stand:
            for o in array_standort_ags_bev_gags_gbev:
                if int(p.AGS)==o[0]:
                    p.setValue("GSAGS",o[2])
                    p.setValue("GSBEV",o[3])
                    cur_UP_Stand.updateRow(p)
                    break
        del array_ags_bev_gags,array_ags_gags,array_bkggem_ags_bev_gags,array_standort_ags_bev_gags_gbev
        del cur_UP_Stand

    def berechnung_siedlungsdaten(shp):
        #siedlung = Siedlungszahlendaten
        try:
            arcpy.AddField_management(join(workspace_projekt,shp), "Lebensmittel", "DOUBLE")
        except:
            messages.AddErrorMessage("Lebensmittel Spalte konnte nicht hinzugefuegt werden - Abbruch")
            exit(1)


        cur_Siedlungszellendaten=arcpy.UpdateCursor(join(workspace_projekt,shp))
        cur_Grundeinstellungen=arcpy.SearchCursor(join(workspace_Basis_Daten,"Grundeinstellungen"))
        cur_KK_Kennziffer_LM=arcpy.SearchCursor(join(workspace_Basis_Daten,"KK_Kennziffer_LM"))

        array_cur_Grundeinstellungen=[]
        for werte in cur_Grundeinstellungen:
            vs=[werte.Info,werte.Wert]
            array_cur_Grundeinstellungen.append(vs)

    ##    print array_cur_Grundeinstellungen[2][1]

        array_KK_Kennziffer_LM=[]
        for werte in cur_KK_Kennziffer_LM:
            vs=[werte.Ort,werte.Wert,werte.AGS]
            array_KK_Kennziffer_LM.append(vs)


        #Berechnung Lebensmittel Siedlungszellendaten
        try:

            for zeile in cur_Siedlungszellendaten:
                KK_Wert=0
                for suche in array_KK_Kennziffer_LM:
                    if int(zeile.AGS)==suche[2]:
                        KK_Wert=suche[1]
                        break
                del suche
                #not found
                if KK_Wert==0:
                    KK_Wert=1.

            ##            print zeile.SZ_Einwohner, array_cur_Grundeinstellungen[1][1] , array_cur_Grundeinstellungen[2][1] ,array_cur_Grundeinstellungen[1][1] * array_cur_Grundeinstellungen[2][1]
                g=(zeile.SZ_Einwohner*array_cur_Grundeinstellungen[1][1]*array_cur_Grundeinstellungen[2][1] *KK_Wert)
            ##            print g
                zeile.Lebensmittel=g    #*KK_Wert/100. #*array_cur_Grundeinstellungen[2][1]
                cur_Siedlungszellendaten.updateRow(zeile)
        except:
            messages.AddErrorMessage("Unexpected Error - Kontaktieren sie den Programmierer")
            exit(1)
            print "Unexpected error:", sys.exc_info()[0]

        del cur_Grundeinstellungen,cur_KK_Kennziffer_LM,cur_Siedlungszellendaten

    #------------------------------------------------------------------------------------------------------------
    #KK-Anteile Wahrsch
    def KK_Anteile_Wahrsch(shp_KK_Anteile_Wahrsch,shp_distanzmatrix,shp_standortdaten):
        #shp_KK_Anteile_Wahrsch=KK_Anteile_Wahrsch
        #shp_distanzmatrix=Distanzmatrix
        #shp_standortdaten=Standortdaten

        try:
            arcpy.Delete_management(join(workspace_projekt,shp_KK_Anteile_Wahrsch))
        except:
            print "fehler beim löschen - "+shp_KK_Anteile_Wahrsch
        try:

            arcpy.CreateTable_management(arcpy.env.workspace,shp_KK_Anteile_Wahrsch,shp_distanzmatrix)
        except:
            print"a) Fehler beim erstellen der Tabelle"+str(shp_distanzmatrix)
            return 1



        cur_Siedlungszellendaten=arcpy.SearchCursor(join(workspace_projekt,"Siedlungszahlendaten"))
        cur_Standortdaten=arcpy.SearchCursor(join(workspace_projekt,shp_standortdaten))

        #Neuer MarktID hier setzen
        neuerMarktID=600



    ##    cur_gesamt =arcpy.SearchCursor(shp+"/gesamt")
        #100.000 EW und mehr
        cur_Ueber_100kEW =arcpy.SearchCursor(join(workspace_Basis_Daten,"Ueber_100kEW"))
        #50.000 bis 100.000 EW
        cur_Zwischen_50k_100kEW =arcpy.SearchCursor(join(workspace_Basis_Daten,"Zwischen_50k_100kEW"))
        #20.000 bis 50.000 EW
        cur_Zwischen_20k_50kEW =arcpy.SearchCursor(join(workspace_Basis_Daten,"Zwischen_20k_50kEW"))
        #10.000 bis 20.000 EW
        cur_Zwischen_10k_20kEW =arcpy.SearchCursor(join(workspace_Basis_Daten,"Zwischen_10k_20kEW"))
        #unter 10.000 EW
        cur_Unter_10kEW =arcpy.SearchCursor(join(workspace_Basis_Daten,"Unter_10kEW"))

        cur_Distanzmatrix=arcpy.SearchCursor(join(workspace_projekt,shp_distanzmatrix))


    ##    array_gesamt=[]
    ##    for zeile in cur_gesamt:
    ##        vs=[zeile.Typ,zeile.Faktor_EXP,zeile.Hochzahl]
    ##        array_gesamt.append(vs)
    ##
    ##    del zeile,cur_gesamt

        array_Ueber_100kEW=[]
        for zeile in cur_Ueber_100kEW:
            array_Ueber_100kEW.append([zeile.Typ,zeile.Faktor_EXP,zeile.Hochzahl])
        del zeile,cur_Ueber_100kEW

        array_Zwischen_50k_100kEW=[]
        for zeile in cur_Zwischen_50k_100kEW:
            array_Zwischen_50k_100kEW.append([zeile.Typ,zeile.Faktor_EXP,zeile.Hochzahl])

        del zeile,cur_Zwischen_50k_100kEW

        array_Zwischen_20k_50kEW=[]
        for zeile in cur_Zwischen_20k_50kEW:
            array_Zwischen_20k_50kEW.append([zeile.Typ,zeile.Faktor_EXP,zeile.Hochzahl])

        del zeile,cur_Zwischen_20k_50kEW

        array_Zwischen_10k_20kEW=[]
        for zeile in cur_Zwischen_10k_20kEW:
            array_Zwischen_10k_20kEW.append([zeile.Typ,zeile.Faktor_EXP,zeile.Hochzahl])

        del zeile,cur_Zwischen_10k_20kEW

        array_Unter_10kEW=[]
        for zeile in cur_Unter_10kEW:
            array_Unter_10kEW.append([zeile.Typ,zeile.Faktor_EXP,zeile.Hochzahl])

        del zeile,cur_Unter_10kEW

        fieldnames = [f.name for f in arcpy.ListFields(join(workspace_projekt,shp_distanzmatrix))]

        cur_KK_Anteile_Wahrsch=arcpy.InsertCursor(join(workspace_projekt,shp_KK_Anteile_Wahrsch))

        array_Siedlungszellendaten=[]
        for zeile in cur_Siedlungszellendaten:
            array_Siedlungszellendaten.append([zeile.SZ_ID,zeile.GEN,zeile.GEN,zeile.SZ_Einwohner,zeile.Lebensmittel])
        del zeile,cur_Siedlungszellendaten

        array_Standortdaten=[]
        for zeile in cur_Standortdaten:
            array_Standortdaten.append([zeile.ID,zeile.Betriebstyp_Funktion,zeile.Gemeindeklasse,zeile.Bonifaktor])

        del zeile,cur_Standortdaten

        row_insert_KK_Anteile_Wahrsch=cur_KK_Anteile_Wahrsch.newRow()

        for zeile in cur_Distanzmatrix:
            for felder in fieldnames[2:]:
                MarktID= int(str(felder).replace('ID_',''))
                for standort_daten in array_Standortdaten:
                    if MarktID==standort_daten[0]:
                        if zeile.getValue('ID_'+str(MarktID))!=0. :
                            row_insert_KK_Anteile_Wahrsch.Siedlungsid=zeile.Siedlungsid
                            gemeindeklasse=standort_daten[2]

                            aufschlag_neuer_Markt=1.
                    ##                        if MarktID==neuerMarktID:
                    ##                            aufschlag_neuer_Markt=1.47
                            if standort_daten[3]!=None and standort_daten[3]!="":
                    ##                            print "boni faktor gesetzt " + str(MarktID)
                                aufschlag_neuer_Markt=standort_daten[3]


                    ##                    if gemeindeklasse==0:
                    ####                        print "GEsamt"
                    ##                                    for werte in array_gesamt:
                    ##                                        if standort_daten[1]==werte[0]:
                    ##
                    ##                                            Wert=float(werte[1])*math.exp(float(werte[2])*float(zeile.getValue('ID_'+str(MarktID))))*aufschlag_neuer_Markt
                    ####                                            print Wert
                    ##                                            row_insert_KK_Anteile_Wahrsch.setValue('ID_'+str(MarktID),Wert)
                            if gemeindeklasse==1:
                    ##                        print "GEsamt"
                                for werte in array_Ueber_100kEW:
                                    if standort_daten[1]==werte[0]:

                                        Wert=float(werte[1])*math.exp(float(werte[2])*float(zeile.getValue('ID_'+str(MarktID))))*aufschlag_neuer_Markt
                            ##                                            print Wert
                                        row_insert_KK_Anteile_Wahrsch.setValue('ID_'+str(MarktID),Wert)
                            elif gemeindeklasse==2:
                    ##                        print "GEsamt"
                                for werte in array_Zwischen_50k_100kEW:
                                    if standort_daten[1]==werte[0]:

                                        Wert=float(werte[1])*math.exp(float(werte[2])*float(zeile.getValue('ID_'+str(MarktID))))*aufschlag_neuer_Markt
                            ##                                            print Wert
                                        row_insert_KK_Anteile_Wahrsch.setValue('ID_'+str(MarktID),Wert)
                            elif gemeindeklasse==3:
                    ##                                    print "GEsamt"
                                for werte in array_Zwischen_20k_50kEW:
                                    if standort_daten[1]==werte[0]:
                        ##                                            print float(werte[1])
                        ##                                            print float(werte[2])
                        ##                                            print float(zeile.getValue('ID_'+str(MarktID)))/1000
                                        Wert=float(werte[1])*math.exp(float(werte[2])*float(zeile.getValue('ID_'+str(MarktID))))*aufschlag_neuer_Markt
                            ##                                            print Wert
                                        row_insert_KK_Anteile_Wahrsch.setValue('ID_'+str(MarktID),Wert)
                            elif gemeindeklasse==4:
                    ##                        print "GEsamt"
                                for werte in array_Zwischen_10k_20kEW:
                                    if standort_daten[1]==werte[0]:

                                        Wert=float(werte[1])*math.exp(float(werte[2])*float(zeile.getValue('ID_'+str(MarktID))))*aufschlag_neuer_Markt
                            ##                                            print Wert
                                        row_insert_KK_Anteile_Wahrsch.setValue('ID_'+str(MarktID),Wert)
                            elif gemeindeklasse==5:
                    ##                        print "GEsamt"
                                for werte in array_Unter_10kEW:
                                    if standort_daten[1]==werte[0]:

                                        Wert=float(werte[1])*math.exp(float(werte[2])*float(zeile.getValue('ID_'+str(MarktID))))*aufschlag_neuer_Markt
                            ##                                            print Wert
                                        row_insert_KK_Anteile_Wahrsch.setValue('ID_'+str(MarktID),Wert)
                        else:
                            row_insert_KK_Anteile_Wahrsch.Siedlungsid=zeile.Siedlungsid
                            row_insert_KK_Anteile_Wahrsch.setValue('ID_'+str(MarktID),0.)

            cur_KK_Anteile_Wahrsch.insertRow(row_insert_KK_Anteile_Wahrsch)

        del cur_KK_Anteile_Wahrsch,cur_Distanzmatrix



    def Kleinste_Distanzen(shp_distanzmatrix,shp_Standortdaten,shp_Distanzmatrix_dichteste):
        #shp_distanzmatrix= Distanzmatrix
        #shp_Standortdaten= Standortdaten
        #shp_Distanzmatrix_dichteste=Distanzmatrix_dichteste

        cur_Distanzmatrix=arcpy.SearchCursor(join(workspace_projekt,shp_distanzmatrix))
        cur_Standortdaten=arcpy.SearchCursor(join(workspace_projekt,shp_Standortdaten))

        fieldnamess = [f.name for f in arcpy.ListFields(join(workspace_projekt,shp_distanzmatrix))]

        fieldnames= fieldnamess[2:]
    ##    print fieldnames

        array_Standortdaten=[]
        for zeile in cur_Standortdaten:
            array_Standortdaten.append([zeile.ID,zeile.Betriebstyp_Attraktivitaet])

        del zeile,cur_Standortdaten


        array_betriebstyp_fieldid=[]
        for name in fieldnames:
            for zeile in array_Standortdaten:
                if int(str(name).replace('ID_',''))==zeile[0]:

                    if (len(array_betriebstyp_fieldid)==0):
                        array_betriebstyp_fieldid.append([zeile[1],zeile[0]])
                    else:
                        gefunden=0
                        for a in array_betriebstyp_fieldid:
                            if zeile[1]==a[0]:
                                a.append(zeile[0])
                                gefunden=1
                                break
                        if gefunden==0:
                            array_betriebstyp_fieldid.append([zeile[1],zeile[0]])
                        del a


    ##    print array_betriebstyp_fieldid

        try:
            arcpy.Delete_management("\\"+shp_Distanzmatrix_dichteste)
        except:
            print "fehler beim löschen - Distanzmatrix_dichteste"
        try:
            arcpy.CreateTable_management(workspace_projekt, shp_Distanzmatrix_dichteste)
        except:
            print "FEHLER beim erstellen - Distanzmatrix_dichteste"
            exit(1)


        #Hinzufuegen SiedlungsId Spalte
        arcpy.AddField_management(join(workspace_projekt,shp_Distanzmatrix_dichteste), fieldnamess[1], "LONG")


        #Tabelle vorbereiten
        for eintrag_machen in array_betriebstyp_fieldid:
            arcpy.AddField_management(join(workspace_projekt,shp_Distanzmatrix_dichteste), str(eintrag_machen[0]).replace('-','_').replace('(','_').replace(')','').replace(',','').replace('.','')+"_1", "DOUBLE")
            arcpy.AddField_management(join(workspace_projekt,shp_Distanzmatrix_dichteste), str(eintrag_machen[0]).replace('-','_').replace('(','_').replace(')','').replace(',','').replace('.','')+"_2", "DOUBLE")
            arcpy.AddField_management(join(workspace_projekt,shp_Distanzmatrix_dichteste), str(eintrag_machen[0]).replace('-','_').replace('(','_').replace(')','').replace(',','').replace('.','')+"_3", "DOUBLE")

        #Cursor auf die Tabelle
        cur_Distanzmatrix_dichteste=arcpy.InsertCursor(join(workspace_projekt,shp_Distanzmatrix_dichteste))

        for zeile in cur_Distanzmatrix:
            array_betriebstyp_entfernung=[]
            for field in fieldnames:
                Wert = zeile.getValue(field)
                for a in array_betriebstyp_fieldid:
                    zahl = int(str(field).replace('ID_',''))

                    if [c for c in a[1:] if int(str(field).replace('ID_',''))==c]: #int(str(field).replace('ID_','')) in a[1]:

                        if len(array_betriebstyp_entfernung)==0:
                            array_betriebstyp_entfernung.append([a[0],Wert,0,0])

                        else:
                            gefunden=0
                            for b in array_betriebstyp_entfernung:
                                if a[0]==b[0]:
                        ##                                if str(b[0])==u"gr. SM Edeka":
                        ##                                    print Wert
                        ##                                    print b[1]
                        ##                                    print b[2]
                        ##                                    print b[3]
                        ##                                    print
                                        #Muellzahlen
                                    if Wert ==0:
                                        gefunden=1
                                        break

                                    if b[1]>Wert:   # > gewechselt
                                        zw1=b[1]
                                        zw2=b[2]

                                        b[1]=Wert
                                        b[2]=zw1
                                        b[3]=zw2

                                    elif b[2]>Wert: # > gewechselt
                                        zw2=b[2]
                                        b[2]=Wert
                                        b[3]=zw2

                                    elif b[3]>Wert: # > gewechselt
                                        b[3]=Wert

                                    elif b[1]==0:
                                        b[1]=Wert

                                    elif b[2]==0:
                                        b[2]=Wert

                                    elif b[3]==0:
                                        b[3]=Wert


                                    gefunden=1
                                    break
                            del b
                            if gefunden==0:
                                array_betriebstyp_entfernung.append([a[0],Wert,0,0])

            try:

                row_Distanzmatrix_dichteste=cur_Distanzmatrix_dichteste.newRow()
            ##            print array_betriebstyp_entfernung
            ##            print
                for  eintraege in array_betriebstyp_entfernung:
                    for x,  dreitraege in enumerate( eintraege[1:]):
                ##                print "asd"
                ##                    print eintraege[0]
                        feldername=str(eintraege[0]).replace(',','').replace('.','').replace('-',' ').replace('(','_').replace(')','').replace(' ','_')+"_"+str(x+1)
                    ##                print feldername
                        row_Distanzmatrix_dichteste.setValue(str(feldername),dreitraege)
                        row_Distanzmatrix_dichteste.setValue(fieldnamess[1],zeile.getValue(fieldnamess[1]))
            except:
                print "Fehler "
                print fieldnamess[1]
            cur_Distanzmatrix_dichteste.insertRow(row_Distanzmatrix_dichteste)
            del array_betriebstyp_entfernung

        del cur_Distanzmatrix_dichteste,cur_Distanzmatrix,fieldnamess

    def Attraktivitaet(shp_Standortdaten,shp_Distanzmatrix_dichteste,shp_Distanzmatrix_dichteste_gewichtung):
        #shp_Standortdaten
        #shp_Distanzmatrix_dichteste
        #shp_Distanzmatrix_dichteste_gewichtung

        Maximaler_AbstandZwMK=1.000 # 2Km

        cur_Standortdaten=arcpy.SearchCursor(join(workspace_projekt,shp_Standortdaten))
        cur_Distanzmatrix_dichteste=arcpy.SearchCursor(join(workspace_projekt,shp_Distanzmatrix_dichteste))
        cur_Attraktivitaet_Info=arcpy.SearchCursor(join(workspace_Basis_Daten,"Attraktivitaet_Info"))

        fieldnames_infotabelle=[f.name for f in arcpy.ListFields(join(workspace_Basis_Daten,"Attraktivitaet_Info"))]

        try:
            arcpy.Delete_management(workspace_projekt+"\\"+shp_Distanzmatrix_dichteste_gewichtung)
        except:
            print "Fehler beim Löschen Distanzmatrix_dichteste_gewichtung"
        try:
            arcpy.CreateTable_management(workspace_projekt, shp_Distanzmatrix_dichteste_gewichtung,shp_Distanzmatrix_dichteste)
        except:
            print "FEHLER erstellen  - Distanzmatrix_dichteste_gewichtung"
            exit(1)
            pass


        fieldnamess = [f.name for f in arcpy.ListFields(join(workspace_projekt,shp_Distanzmatrix_dichteste))]
        cur_Distanzmatrix_dichteste_gewichtung=arcpy.InsertCursor(join(workspace_projekt,shp_Distanzmatrix_dichteste_gewichtung))




        fieldnames=fieldnamess[2:]

        array_Attraktivitaet_Info=[]
        for zeile in cur_Attraktivitaet_Info:
            array_Attraktivitaet_Info.append([zeile.Typ,zeile.ein_Markt_in_der_Naehe,zeile.zwei_Maerkte_in_der_Naehe,zeile.drei_Maerkte_in_der_Naehe,zeile.zweiter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe,zeile.dritter_Markt_wenn_erster_Markt_mit_Abstand_in_der_Naehe,zeile.dritter_Markt_wenn_erster_und_zweiter_Markt_mit_Abstand_in_der_N])

        del zeile,cur_Attraktivitaet_Info


        wert =[]


        for zeile in cur_Distanzmatrix_dichteste:
            row_Distanzmatrix_dichteste_gewichtung=cur_Distanzmatrix_dichteste_gewichtung.newRow()
            array_betriebstyp_gewichtung_zeile=[]
            for zeile1 in fieldnames:

                wert.append(zeile.getValue(str(zeile1)))
                if len(wert)==3:
            ##                print "drei werte"
                    wert1=wert[0]
                    wert2=wert[1]
                    wert3=wert[2]
                    wert=[]
                    ausspalte=[]

                    #ueberpruefe wie viele Entfernungen du eigentlich hast
                    #Nur ein Markt in der Gegend -> Abbruch
                    #Besprechen mit Sascha!
                    #veraendert nach email mit maengel von sachsa
                ##                if wert2==0 and wert3==0 and wert1==0 :
                ##                    ausspalte.append(None)
                ##                    ausspalte.append(None)
                ##                    ausspalte.append(None)
                ##                elif wert2==0 and wert3==0 :
                ##                    ausspalte.append(1)
                ##                    ausspalte.append(None)
                ##                    ausspalte.append(None)
                ##                else:
                ##                    if wert2==0.:
                ##                        wert2=1000
                ##                    if wert3==0.:
                ##                        wert3=1000

                ##                    print zeile1
                ##                    print wert1,wert2,wert3

                    #Berechnung 1
                    if wert1==0:
                        ausspalte.append(None)
                    elif wert2==0 and wert3==0:
                        ausspalte.append(1)
                    elif abs(wert2-wert1)>Maximaler_AbstandZwMK:
                        ausspalte.append(1)
                    elif wert3==0:
                        ausspalte.append(2)
                    elif abs(wert3-wert1)<Maximaler_AbstandZwMK:
                        ausspalte.append(3)
                    else:
                        ausspalte.append(2)

                    #was ist wenn der dritte wert 0 ist
                    #Berechnung 2
                    if wert2==0:
                        ausspalte.append(None)
                    elif abs(wert2-wert1)>Maximaler_AbstandZwMK:
                        ausspalte.append(4)
                    elif wert3==0:
                        ausspalte.append(2)
                    elif abs(wert3-wert1)<Maximaler_AbstandZwMK:
                        ausspalte.append(3)
                    else:
                        ausspalte.append(2)

                    #Berechnung 3
                    if wert3==0:
                        ausspalte.append(None)
                    elif abs(wert2-wert1)>Maximaler_AbstandZwMK:
                        ausspalte.append(5)
                    elif wert3==0:
                        ausspalte.append(2)
                    elif abs(wert3-wert1)<Maximaler_AbstandZwMK:
                        ausspalte.append(3)
                    elif abs(wert2-wert1)<Maximaler_AbstandZwMK:
                        ausspalte.append(6)


                    else:
                        #Fehler
                        print " Fehler attraktivitaet"

                ##                if (zeile.Siedlungsid==1921 or zeile.Siedlungsid==1956 or zeile.Siedlungsid==1994) and (zeile1 == "gr_SM_V_Markt_SBW_Famila_1" or zeile1 == "gr_SM_V_Markt_SBW_Famila_2"or zeile1 == "gr_SM_V_Markt_SBW_Famila_3"):
                ##                    print ausspalte, zeile.Siedlungsid,wert1 , wert2, wert3
                ##                if zeile1 == "Penny_1" or zeile1 == "Penny_2"or zeile1 == "Penny_3":
                ##
                ##                     print ausspalte , zeile.Siedlungsid

                    #Wert aus der Info tabelle fuer den Abstand holen
                    gesuchtgefunden=0
                    for abc in array_Attraktivitaet_Info:
                ##                    print
                ##                    print str(abc[0]).replace('.','').replace('(',' ').replace(')','').replace(',','').replace('_','').replace('-',' ').replace(' ','')
                ##                    print str(zeile1).replace('_3','').replace('_','')
                        if str(abc[0]).replace('.','').replace('(',' ').replace(')','').replace(',','').replace('_','').replace('-',' ').replace(' ','')==str(zeile1).replace('_3','').replace('_','').replace(' ',''):
                ##                        print "gefunden in Infotablee"
                            if ausspalte[0]== None:
                                array_betriebstyp_gewichtung_zeile.append([str(zeile1).replace('_3','').replace('_',' '),0,0,0])
                            elif ausspalte[1]== None:
                                array_betriebstyp_gewichtung_zeile.append([str(zeile1).replace('_3','').replace('_',' '),abc[ausspalte[0]],0,0])
                            elif ausspalte[2]== None:
                                array_betriebstyp_gewichtung_zeile.append([str(zeile1).replace('_3','').replace('_',' '),abc[ausspalte[0]],abc[ausspalte[1]],0])
                            else:
                                array_betriebstyp_gewichtung_zeile.append([str(zeile1).replace('_3','').replace('_',' '),abc[ausspalte[0]],abc[ausspalte[1]],abc[ausspalte[2]]])
                            gesuchtgefunden=1
                            break


                    if gesuchtgefunden==0:
                        print "not found in Infotabelle"
                        print str(zeile1).replace('_3','').replace('_',' ').replace(' ','')

                    del abc
                    ausspalte=[]
        ##                print array_betriebstyp_gewichtung_zeile


        ##        print array_betriebstyp_gewichtung_zeile
            #vor weg nur Id setzen bzw kopieren
            row_Distanzmatrix_dichteste_gewichtung.setValue(str(fieldnamess[1]),zeile.getValue(str(fieldnamess[1])))
        ##        print array_betriebstyp_gewichtung_zeile
            for asd in array_betriebstyp_gewichtung_zeile:
                if asd[1]==None:
                    asd[1]=0
                if asd[2]==None:
                    asd[2]=0

                if asd[3]==None:
                    asd[3]=0

                row_Distanzmatrix_dichteste_gewichtung.setValue(str(asd[0]).replace('.','').replace('_','').replace('-',' ').replace(' ','_').replace('(',' ').replace(')','')+"_1",asd[1])
                row_Distanzmatrix_dichteste_gewichtung.setValue(str(asd[0]).replace('.','').replace('_','').replace('-',' ').replace(' ','_').replace('(',' ').replace(')','')+"_2",asd[2])
                row_Distanzmatrix_dichteste_gewichtung.setValue(str(asd[0]).replace('.','').replace('_','').replace('-',' ').replace(' ','_').replace('(',' ').replace(')','')+"_3",asd[3])
            cur_Distanzmatrix_dichteste_gewichtung.insertRow(row_Distanzmatrix_dichteste_gewichtung)
    ##    print "done"


    def asd(shp_Siedlungszahlendaten,shp_Standortdaten,shp_Distanzmatrix,shp_KK_Anteile_Wahrsch,shp_Distanzmatrix_dichteste,shp_shp_Distanzmatrix_dichteste_gewichtung,shp_Verteilungsmasstab1,shp_Verteilungsmasstab2,shp_ET_Kaufkraft):
        #shp_Siedlungszahlendaten
        #shp_Standortdaten
        #shp_Distanzmatrix
        #shp_Distanzmatrix_dichteste
        #shp_shp_Distanzmatrix_dichteste_gewichtung
        #shp_KK_Anteile_Wahrsch
        #shp_Verteilungsmasstab1
        #shp_Verteilungsmasstab2
        #shp_ET_Kaufkraft

        cur_Siedlungszellendaten=arcpy.UpdateCursor(join(workspace_projekt,shp_Siedlungszahlendaten))

        cur_Distanzmatrix_dichteste=arcpy.SearchCursor(join(workspace_projekt,shp_Distanzmatrix_dichteste))
        cur_Distanzmatrix_dichteste_gewichtung=arcpy.SearchCursor(join(workspace_projekt,shp_shp_Distanzmatrix_dichteste_gewichtung))

        cur_Distanzmatrix=arcpy.SearchCursor(join(workspace_projekt,shp_Distanzmatrix))
        cur_Standortdaten=arcpy.SearchCursor(join(workspace_projekt,shp_Standortdaten))
        cur_KK_Anteile_Wahrsch=arcpy.SearchCursor(join(workspace_projekt,shp_KK_Anteile_Wahrsch))




        fieldnamess = [f.name for f in arcpy.ListFields(join(workspace_projekt,shp_Distanzmatrix))]

        fieldnames= fieldnamess[2:]
    ##    print fieldnames
    ##    print len (fieldnames)
        try:
            arcpy.Delete_management(join(workspace_projekt,shp_Verteilungsmasstab1))
            arcpy.Delete_management(join(workspace_projekt,shp_Verteilungsmasstab2))
            arcpy.Delete_management(join(workspace_projekt,shp_ET_Kaufkraft))
        except:
            print "fehler beim löschen - Verteilung"
        try:
            arcpy.CreateTable_management(workspace_projekt, shp_Verteilungsmasstab1,shp_Distanzmatrix)
            arcpy.CreateTable_management(workspace_projekt, shp_Verteilungsmasstab2,shp_Distanzmatrix)
            arcpy.CreateTable_management(workspace_projekt, shp_ET_Kaufkraft,shp_Distanzmatrix)
        except:
            exit(1)
            print "FEHLER beim Löschen - Verteilung"
            pass




        #curser drauf
        cur_Verteilungsmasstab1=arcpy.InsertCursor(join(workspace_projekt,shp_Verteilungsmasstab1))
        cur_Verteilungsmasstab2=arcpy.InsertCursor(join(workspace_projekt,shp_Verteilungsmasstab2))
        cur_Kaufkraft_ET=arcpy.InsertCursor(join(workspace_projekt,shp_ET_Kaufkraft))


        array_Siedlungszellendaten=[]
        for zeile in cur_Siedlungszellendaten:
            array_Siedlungszellendaten.append([zeile.SZ_ID,zeile.SZ_Einwohner,zeile.Lebensmittel])

        del zeile,cur_Siedlungszellendaten

    ##    print len(array_Siedlungszellendaten)

        array_Standortdaten=[]
        for zeile in cur_Standortdaten:
            array_Standortdaten.append([zeile.ID,zeile.Betriebstyp_Attraktivitaet])

        del zeile,cur_Standortdaten

    ##    print len(array_Standortdaten)


        for distmatrix in cur_Distanzmatrix:

            for b in cur_KK_Anteile_Wahrsch:

                for a in cur_Distanzmatrix_dichteste_gewichtung:

                    for abc in cur_Distanzmatrix_dichteste:

                ##                    print distmatrix.Siedlungsid
                ##                    print abc.Siedlungsid
                ##                    print a.Siedlungsid

                        array_irgendwas=[]
                        for name in fieldnames:
                ##                        print str(int(str(name).replace('ID_','')))
                            row_cur_Verteilungsmasstab1=cur_Verteilungsmasstab1.newRow()
                            for zeile in array_Standortdaten:
                                if int(str(name).replace('ID_',''))==zeile[0]:


                        ##                            print zeile [1] # name
                        ##                                print str(zeile[1]).replace('.','').replace('-',' ').replace(' ','_') + "_1"

                        ##                                print b.getValue(name)
                        ##                                print
                        ##                                print distmatrix.getValue(name)
                        ##                                print abc.getValue(str(zeile[1]).replace('.','').replace('-',' ').replace(' ','_') + "_1")
                        ##                                print abc.getValue(str(zeile[1]).replace('.','').replace('-',' ').replace(' ','_') + "_2")
                        ##                                print abc.getValue(str(zeile[1]).replace('.','').replace('-',' ').replace(' ','_') + "_3")

                        ##                                print str(zeile[1]).replace(',','').replace('.','').replace('-',' ').replace(' ','_') + "_1"
                        ##                                print abc.getValue(str(zeile[1]).replace(',','').replace('.','').replace('-',' ').replace(' ','_') + "_1")
                                    welchespalte=str(zeile[1]).replace(',','').replace('.','').replace('-',' ').replace(' ','_').replace('(','_').replace(')','')
                            ##                                print name
                            ##                                print welchespalte
                            ##                                print float(distmatrix.getValue(name))
                            ##                                print float(abc.getValue(welchespalte + "_1"))
                            ##                                print (abc.getValue(welchespalte + "_2"))
                            ##                                print (abc.getValue(welchespalte + "_3"))
                            ##                                print
                                    if distmatrix.getValue(name) == (abc.getValue(welchespalte+ "_1")) and distmatrix.getValue(name)!=0.:
                            ##                                    print str(zeile[1]).replace('.','').replace('-',' ').replace(' ','_') + "_1"
                            ##                                    print a.getValue(str(zeile[1]).replace('.','').replace('-',' ').replace(' ','_') + "_1")
                            ##                                    print welchespalte
                            ##                                    print name
                            ##                                    print (b.getValue(str(name))*100.)
                            ##                                    print a.getValue(welchespalte+ "_1")
                            ##                                    print

                                        array_irgendwas.append((b.getValue(str(name))*100.)*a.getValue(welchespalte+ "_1"))

                            ##                                    row_cur_Verteilungsmasstab1.setValue(str(name),b.getValue(str(name))*a.getValue(welchespalte + "_1"))

                                    elif distmatrix.getValue(name) == abc.getValue(welchespalte + "_2") and distmatrix.getValue(name)!=0.:
                            ##                                    print str(zeile[1]).replace('.','').replace('-',' ').replace(' ','_') + "_2"
                            ##                                    print a.getValue(str(zeile[1]).replace('.','').replace('-',' ').replace(' ','_') + "_2")
                            ##                                    print "ID_"+str(distmatrix.Siedlungsid)
                            ##                                    print welchespalte
                            ##                                    print name
                            ##                                    print (b.getValue(str(name))*100.)
                            ##                                    print a.getValue(welchespalte+ "_1")
                            ##                                    print
                                        array_irgendwas.append((b.getValue(str(name))*100.)*a.getValue(welchespalte + "_2"))
                            ##                                    row_cur_Verteilungsmasstab1.setValue(str(name),b.getValue(str(name))*a.getValue(welchespalte + "_2"))


                                    elif distmatrix.getValue(name) == abc.getValue(welchespalte+ "_3") and distmatrix.getValue(name)!=0.:
                            ##                                    print a.getValue(str(zeile[1]).replace('.','').replace('-',' ').replace(' ','_') + "_3")
                            ##                                    print welchespalte
                            ##                                    print name
                            ##                                    print (b.getValue(str(name))*100.)
                            ##                                    print a.getValue(welchespalte+ "_1")
                            ##                                    print
                                        array_irgendwas.append((b.getValue(str(name))*100.)*a.getValue(welchespalte + "_3"))
                            ##                                    row_cur_Verteilungsmasstab1.setValue(str(name),b.getValue(str(name))*a.getValue(welchespalte + "_3"))

                                    else:
                                        array_irgendwas.append(0.0)
                    ##                                    row_cur_Verteilungsmasstab1.setValue(str(name),0)


                            del zeile

                ##                    print array_irgendwas
                        row_cur_Verteilungsmasstab1.setValue(fieldnamess[1],distmatrix.Siedlungsid)
                        summe=0.0
                        for spaltenzahl, schreibe in enumerate( array_irgendwas):
                            row_cur_Verteilungsmasstab1.setValue(fieldnames[spaltenzahl],float(schreibe))
                            summe+=schreibe
                        cur_Verteilungsmasstab1.insertRow(row_cur_Verteilungsmasstab1)


                ##                    print len(array_irgendwas)
                ##                    print len(fieldnames)



                ##                    print summe
                        row_cur_Verteilungsmasstab2=cur_Verteilungsmasstab2.newRow()
                        row_cur_Kaufkraft_ET=cur_Kaufkraft_ET.newRow()
                ##                    test=0.0
                ##                    test1=0.0
                        nichtgefunden=0
                        for variable_array_Siedlungszellendaten in array_Siedlungszellendaten:

                            if variable_array_Siedlungszellendaten[0]==distmatrix.Siedlungsid:

                                for x, variable_array_irgendwas in enumerate( array_irgendwas):




                        ##                            array_irgendwas[x]=(variable_array_irgendwas/summe)*variable_array_Siedlungszellendaten[3]
                                    if summe!=0 and variable_array_irgendwas!=0:

                                        row_cur_Verteilungsmasstab2.setValue(fieldnames[x],variable_array_irgendwas/summe)
                                        row_cur_Kaufkraft_ET.setValue(fieldnames[x],(variable_array_irgendwas/summe)*variable_array_Siedlungszellendaten[2])
                                    else:
                                        row_cur_Verteilungsmasstab2.setValue(fieldnames[x],0.)
                                        row_cur_Kaufkraft_ET.setValue(fieldnames[x],0.)
                            ##                                test+=(variable_array_irgendwas/summe)*variable_array_Siedlungszellendaten[3]
                            ##                                test1+=variable_array_irgendwas/summe

                                    row_cur_Verteilungsmasstab2.setValue(str(fieldnamess[1]),variable_array_Siedlungszellendaten[0])
                                    row_cur_Kaufkraft_ET.setValue(str(fieldnamess[1]),variable_array_Siedlungszellendaten[0])

                                cur_Verteilungsmasstab2.insertRow(row_cur_Verteilungsmasstab2)
                                cur_Kaufkraft_ET.insertRow(row_cur_Kaufkraft_ET)
                                nichtgefunden=1
                                break
                        if nichtgefunden==0:
                            print " nicht gefunden FEHLER"
                            print distmatrix.Siedlungsid

                ##                    print test
                ##                    print test1
                ##                    print
                ##                        del variable_array_Siedlungszellendaten


                ##                    print array_irgendwas
                        del array_irgendwas
                        break

                    break
                break


        try:
            del row_cur_Verteilungsmasstab2,row_cur_Verteilungsmasstab1
            del cur_Distanzmatrix,cur_Distanzmatrix_dichteste,cur_Distanzmatrix_dichteste_gewichtung,row_cur_Kaufkraft_ET,cur_Kaufkraft_ET,cur_KK_Anteile_Wahrsch,cur_Verteilungsmasstab1,cur_Verteilungsmasstab2
        except:
            print"fehler beim löschen"




    def schreibe_KK(shp_Standortdaten,shp_ET_Kaufkraft,shp_Statistik):
        #shp_Standortdaten
        #shp_ET_Kaufkraft
        #shp_Statistik


        try:
            arcpy.AddField_management(join(workspace_projekt,shp_Standortdaten), "Kaufkraft", "DOUBLE")
        except:
            print "Unexpected error:", sys.exc_info()[0]

        fieldnamess = [f.name for f in arcpy.ListFields(join(workspace_projekt,shp_ET_Kaufkraft))]

        try:
            arcpy.Delete_management(shp_Statistik)
        except:
            print "fehler beim löschen - Statistik"

        g=[]
        for spalten in fieldnamess[2:]:
            g.append([str(spalten),"SUM"])
        arcpy.Statistics_analysis(workspace_projekt+shp_ET_Kaufkraft, workspace_projekt+shp_Statistik, g)

        fieldname = [f.name for f in arcpy.ListFields(join(workspace_projekt,shp_Statistik))]

        cur_Statistik= arcpy.SearchCursor(join(workspace_projekt,shp_Statistik))
        cur_Standortdaten= arcpy.UpdateCursor(join(workspace_projekt,shp_Standortdaten))

        for einezeile in cur_Statistik:
            for abc in fieldname[2:]:
                for zeile_standort in cur_Standortdaten:
                    if int(abc.replace('SUM_ID_',''))==zeile_standort.Id:
                        zeile_standort.Kaufkraft=einezeile.getValue(abc)
                        cur_Standortdaten.updateRow(zeile_standort)
                        break

        del cur_Standortdaten,cur_Statistik,fieldname,fieldnamess

    def bilde_gesamt(shp_Uebersicht,shp_Standortdaten):
        #shp_Uebersicht
        #shp_Standortdaten
        try:
            arcpy.Delete_management(shp_Uebersicht)
        except:
            print "fehler beim löschen - Uebersicht"
        try:
            arcpy.CreateTable_management(workspace_projekt,shp_Uebersicht.replace('/',''))
        except:
            print"Fehler beim erstellen der Tabelle bilde gesamt"
            return
        try:
            arcpy.AddField_management(workspace_projekt+shp_Uebersicht, "Marke", "TEXT")
            arcpy.AddField_management(workspace_projekt+shp_Uebersicht, "Kaufkraft_ges", "DOUBLE")
        except:
            print "Unexpected error:", sys.exc_info()[0]


        cur_Standortdaten=arcpy.SearchCursor(workspace_projekt+shp_Standortdaten)

        array_Standortdaten=[]
        for zeile in cur_Standortdaten:
            array_Standortdaten.append([zeile.Betriebstyp_Attraktivitaet,zeile.Kaufkraft,zeile.Id])

        del zeile,cur_Standortdaten

        neues_array=[]

        neues_array.append(array_Standortdaten[0])
        array_Standortdaten.pop(0)


        for inhalt_db in array_Standortdaten:
            gefundenn=0
            for inhalt_array in neues_array:
                if inhalt_db[0]==inhalt_array[0]: #and (int(inhalt_db[2])!=600 and int( inhalt_db[2])!=601) :
            ##                print inhalt_db[2]
                    inhalt_array[1]+=inhalt_db[1]
                    gefundenn=1
                    break

            if gefundenn==0:
                neues_array.append([inhalt_db[0],inhalt_db[1]])


    ##    print neues_array
        cur_Uebersicht= arcpy.InsertCursor(workspace_projekt+shp_Uebersicht)

        for inhalt in neues_array:
    ##        print type(inhalt[1])
            row_cur_Uebersicht=cur_Uebersicht.newRow()
            row_cur_Uebersicht.Kaufkraft_ges=inhalt[1]
            row_cur_Uebersicht.setValue("Marke",str(inhalt[0]))

            cur_Uebersicht.insertRow(row_cur_Uebersicht)

        del cur_Uebersicht
        del neues_array,array_Standortdaten


    def kaufkraft_inSied(shp_siedlungszellendaten,shp_kaufkraft):
        #shp_siedlungszellendaten
        #shp_kaufkraft
        try:
            arcpy.DeleteField_management(join(workspace_projekt,shp_siedlungszellendaten),"KK_Neu")
        except:
            pass

        try:
            arcpy.AddField_management(join(workspace_projekt,shp_siedlungszellendaten), "KK_Neu", "DOUBLE")


        except:
            print"error"
            return

        cur_Update_sied = arcpy.UpdateCursor(join(workspace_projekt,shp_siedlungszellendaten))
        cur_Update_etkk=arcpy.UpdateCursor(join(workspace_projekt,shp_kaufkraft))

        for a in cur_Update_sied:
            for b in cur_Update_etkk:
                if a.SZ_ID == b.Siedlungsid:
                    a.KK_neu=b.getValue("ID_600")*100./a.getValue("Lebensmittel")
                    cur_Update_sied.updateRow(a)
                    break


        try:
            arcpy.DeleteField_management(join(workspace_projekt,shp_siedlungszellendaten),"KK_Neu_2")
        except:
            pass

        try:
            arcpy.AddField_management(join(workspace_projekt,shp_siedlungszellendaten), "KK_Neu_2", "DOUBLE")
        except:
            print"error"
            return

        for a in cur_Update_sied:
            for b in cur_Update_etkk:
                if a.SZ_ID == b.Siedlungsid:
                    try:
                        a.KK_neu_2=b.getValue("ID_601")*100./a.getValue("Lebensmittel")
                    except:
                        print "markt 601 nicht vorhanden ->keine kk anhaengen an siedlungszellen"
                        return

                    cur_Update_sied.updateRow(a)
                    break

        del cur_Update_etkk,cur_Update_sied

    def einzelhandelszentrali():

        cur_Standortdaten=arcpy.SearchCursor(join(workspace_projekt,"Standortdaten"))
        cur_Siedlungszellen=arcpy.SearchCursor(join(workspace_projekt,"Siedlungszahlendaten"))

        try:
            arcpy.Delete_management("Einzelhzentrali")
            arcpy.Delete_management(join(workspace_projekt,"Einzelhzentrali"))
        except:
            pass
        try:
            arcpy.DeleteFeatures_management("Einzelhzentrali")
            arcpy.DeleteFeatures_management(join(workspace_projekt,"Einzelhzentrali"))
        except:
            pass
        try:
            arcpy.CreateTable_management(workspace_projekt,"Einzelhzentrali")
        except:
            print"a) Fehler beim erstellen der Tabelle Einzelhzentrali"
            exit(1)
        try:
            arcpy.AddField_management(join(workspace_projekt,"Einzelhzentrali"),"Kommune","TEXT")
            arcpy.AddField_management(join(workspace_projekt,"Einzelhzentrali"),"AGS","TEXT")
            arcpy.AddField_management(join(workspace_projekt,"Einzelhzentrali"),"Umsatz_vorher","DOUBLE")
            arcpy.AddField_management(join(workspace_projekt,"Einzelhzentrali"),"Umsatz_nachher","DOUBLE")
            arcpy.AddField_management(join(workspace_projekt,"Einzelhzentrali"),"Einzelhzentra","DOUBLE")
            arcpy.AddField_management(join(workspace_projekt,"Einzelhzentrali"),"Einzelhzentrapla","DOUBLE")
            arcpy.AddField_management(join(workspace_projekt,"Einzelhzentrali"),"Delta","DOUBLE")
        except:
            pass

        cur_Search_Sied = arcpy.SearchCursor(join(workspace_projekt,"Siedlungszahlendaten"))

        array_ags=[]
        for zellen in cur_Search_Sied:
            if len(array_ags)==0:
                array_ags.append(int(zellen.AGS))

            else:
                if len([r for r in array_ags if r==int(zellen.AGS)])==0:
                    array_ags.append(int(zellen.AGS))

        del cur_Search_Sied

        array_standortda=[]
        for speicher in cur_Standortdaten:
            if len([k for k in array_ags if k==int(speicher.AGS) ])>0:
                array_standortda.append([speicher.Id,speicher.Kaufkraft,int(speicher.AGS),speicher.GEN])

        del speicher
        auswahl=array_standortda

        ags_gemeinde_umsatz=[]
        for eintraege in array_standortda:
            if len(ags_gemeinde_umsatz)==0:
                ags_gemeinde_umsatz.append([eintraege[2],eintraege[3],eintraege[1],0,0])

            else:
                finden=0
                for gen in ags_gemeinde_umsatz:
                    if gen[0]==eintraege[2]:
                        finden=1
                        gen[2]+=eintraege[1]
                        break
                if finden==0:
                    ags_gemeinde_umsatz.append([eintraege[2],eintraege[3],eintraege[1],0,0])

        for zellen in cur_Siedlungszellen:
            finde=0
            for arrays in ags_gemeinde_umsatz:
                if int(zellen.AGS)==arrays[0]:
                    arrays[3]+=zellen.Lebensmittel
                    finde=1
                    break
            if finde==0:
                ags_gemeinde_umsatz.append([int(zellen.AGS),zellen.GEN,0,zellen.Lebensmittel,0])

        ags_gemeinde_umsatz=sorted(ags_gemeinde_umsatz)
        cur_Sear_GGEN= arcpy.SearchCursor(join(workspace_Basis_Daten,"Gesamtgemeinden"))

        array_GGen=[]
        for speicher in cur_Sear_GGEN:
            array_GGen.append([int(speicher.AGS),speicher.Gen,int(speicher.VAGS),speicher.GGEN])

        del speicher,cur_Sear_GGEN

        array_ggen_umsatz=[]
        for einzelnegen in ags_gemeinde_umsatz:
            found=0
            for gesamtgen in array_GGen:
                if int(einzelnegen[0])== int(gesamtgen[0]):
                    array_ggen_umsatz.append([gesamtgen[2],gesamtgen[3],einzelnegen[2],einzelnegen[3],einzelnegen[4]])
                    found=1
            if found ==0:
                print "Komisch"


        array_ggen_umsatz_Ori=[]
        for einzelnn in auswahl:
            for gesamtegen in array_GGen:
                if int(einzelnn[2])== int(gesamtegen[0]) and len([tt for tt in array_ggen_umsatz_Ori if tt[1]==int(gesamtegen[0]) ])==0:
                    array_ggen_umsatz_Ori.append([int(gesamtegen[2]),int(einzelnn[2])])

        entg_ggen_umsatz=[]
        for asd in array_ggen_umsatz:
            if len(entg_ggen_umsatz)==0:
                entg_ggen_umsatz.append([asd[0],asd[1],asd[2],asd[3],asd[4]])

            else:
                findemich=0
                for allezusam in entg_ggen_umsatz:
                    if allezusam[0]==asd[0]:
                        allezusam[2]+=asd[2]
                        allezusam[3]+=asd[3]
                        findemich=1

                if findemich==0:
                    entg_ggen_umsatz.append([asd[0],asd[1],asd[2],asd[3],asd[4]])

        for x, oui in enumerate( entg_ggen_umsatz):
            wobistdu=0
            for iuo in array_ggen_umsatz_Ori:
                if oui[0]==iuo[0]:
                    wobistdu=1
                    break

            if wobistdu==0:
                oui[2]=0
                oui[3]=0
                oui[4]=0
            del iuo

        for berechnung in entg_ggen_umsatz:
            try:
        ##        berechnung[4]=((berechnung[2]/berechnung[3])*100)-100
                berechnung[4]=(float(berechnung[2])/float(berechnung[3]))*100

            except:
                berechnung[4]=0

        entg_ggen_umsatz=sorted(entg_ggen_umsatz)

        cur_Ins_Verlust=arcpy.InsertCursor(join(workspace_projekt,"Einzelhzentrali"))

        for bb in entg_ggen_umsatz:
            if bb[2]!=0 and bb[3]!=0 and bb[4]!=0:
                row= cur_Ins_Verlust.newRow()
                row.setValue("Kommune","SG/Stadt "+bb[1])
                row.setValue("AGS",bb[0])
                row.setValue("Umsatz_vorher",bb[3])
                row.setValue("Einzelhzentra",bb[4])
                cur_Ins_Verlust.insertRow(row)


        del cur_Ins_Verlust,ags_gemeinde_umsatz,cur_Siedlungszellen,cur_Standortdaten, array_standortda,array_GGen,entg_ggen_umsatz,array_ggen_umsatz,auswahl,array_ggen_umsatz_Ori


        cur_Standortdaten=arcpy.SearchCursor(join(workspace_projekt,"Standortdaten_planfall"))
        cur_Siedlungszellen=arcpy.SearchCursor(join(workspace_projekt,"Siedlungszahlendaten_planfall"))


        array_standortda=[]
        for speicher in cur_Standortdaten:
            if len([k for k in array_ags if k==int(speicher.AGS) ])>0:
                array_standortda.append([speicher.Id,speicher.Kaufkraft,int(speicher.AGS),speicher.GEN])

        del speicher
        del array_ags
        auswahl=array_standortda

        ags_gemeinde_umsatz=[]
        for eintraege in array_standortda:
            if len(ags_gemeinde_umsatz)==0:
                ags_gemeinde_umsatz.append([eintraege[2],eintraege[3],eintraege[1],0,0])

            else:
                finden=0
                for gen in ags_gemeinde_umsatz:
                    if gen[0]==eintraege[2]:
                        finden=1
                        gen[2]+=eintraege[1]
                        break
                if finden==0:
                    ags_gemeinde_umsatz.append([eintraege[2],eintraege[3],eintraege[1],0,0])


        for zellen in cur_Siedlungszellen:
            finde=0
            for arrays in ags_gemeinde_umsatz:
                if int(zellen.AGS)==arrays[0]:
                    arrays[3]+=zellen.Lebensmittel
                    finde=1
                    break
            if finde==0:
                ags_gemeinde_umsatz.append([int(zellen.AGS),zellen.GEN,0,zellen.Lebensmittel,0])


        ags_gemeinde_umsatz=sorted(ags_gemeinde_umsatz)
        cur_Sear_GGEN= arcpy.SearchCursor(join(workspace_Basis_Daten,"Gesamtgemeinden"))

        array_GGen=[]
        for speicher in cur_Sear_GGEN:
            array_GGen.append([int(speicher.AGS),speicher.Gen,int(speicher.VAGS),speicher.GGEN])

        del speicher,cur_Sear_GGEN

        array_ggen_umsatz=[]
        for einzelnegen in ags_gemeinde_umsatz:
            found=0
            for gesamtgen in array_GGen:
                if int(einzelnegen[0])== int(gesamtgen[0]):
                    array_ggen_umsatz.append([gesamtgen[2],gesamtgen[3],einzelnegen[2],einzelnegen[3],einzelnegen[4]])
                    found=1
            if found ==0:
                print "Komisch"

        array_ggen_umsatz_Ori=[]
        for einzelnn in auswahl:
            for gesamtegen in array_GGen:
                if int(einzelnn[2])== int(gesamtegen[0]) and len([tt for tt in array_ggen_umsatz_Ori if tt[1]==int(gesamtegen[0]) ])==0:
                    array_ggen_umsatz_Ori.append([int(gesamtegen[2]),int(einzelnn[2])])


        entg_ggen_umsatz=[]
        for asd in array_ggen_umsatz:
            if len(entg_ggen_umsatz)==0:
                entg_ggen_umsatz.append([asd[0],asd[1],asd[2],asd[3],asd[4]])

            else:
                findemich=0
                for allezusam in entg_ggen_umsatz:
                    if allezusam[0]==asd[0]:
                        allezusam[2]+=asd[2]
                        allezusam[3]+=asd[3]
                        findemich=1

                if findemich==0:
                    entg_ggen_umsatz.append([asd[0],asd[1],asd[2],asd[3],asd[4]])

        for x, oui in enumerate( entg_ggen_umsatz):
            wobistdu=0
            for iuo in array_ggen_umsatz_Ori:
                if oui[0]==iuo[0]:
                    wobistdu=1
                    break

            if wobistdu==0:
                oui[2]=0
                oui[3]=0
                oui[4]=0
            del iuo

        for berechnung in entg_ggen_umsatz:
            try:
        ##        berechnung[4]=((berechnung[2]/berechnung[3])*100)-100
                berechnung[4]=(float(berechnung[2])/float(berechnung[3]))*100

            except:
                berechnung[4]=0

        entg_ggen_umsatz=sorted(entg_ggen_umsatz)
        cur_Up_Verlust=arcpy.UpdateCursor(join(workspace_projekt,"Einzelhzentrali"))
        for updating in cur_Up_Verlust:
            findemich=0
            for arrayeintraege in entg_ggen_umsatz:
                if int( updating.AGS) == int( arrayeintraege[0]):
                    findemich=1
                    updating.setValue("Umsatz_nachher",arrayeintraege[3])
                    updating.setValue("Einzelhzentrapla",arrayeintraege[4])
                    cur_Up_Verlust.updateRow(updating)
            if findemich==0 and arrayeintraege[2]!=0 and arrayeintraege[3]!=0 and arrayeintraege[4]!=0:
                cur_Ins_Verlust=arcpy.InsertCursor(join(workspace_projekt,"Einzelhzentrali"))
                ruw= cur_Ins_Verlust.newRow()
                ruw.setValue("Kommune","SG/Stadt "+ arrayeintraege[1])
                ruw.setValue("AGS",arrayeintraege[0])
                ruw.setValue("Umsatz_vorher",0)
                ruw.setValue("Einzelhzentra",0)
                ruw.setValue("Umsatz_nachher",arrayeintraege[3])
                ruw.setValue("Einzelhzentrapla",arrayeintraege[4])
                cur_Ins_Verlust.insertRow(ruw)
                del cur_Ins_Verlust

        del cur_Up_Verlust,ags_gemeinde_umsatz,cur_Siedlungszellen,cur_Standortdaten,array_GGen,entg_ggen_umsatz,array_ggen_umsatz
        arcpy.CalculateField_management(join(workspace_projekt,"Einzelhzentrali"), "Delta", "-!Einzelhzentra!+!Einzelhzentrapla!", "PYTHON", "")

        cur_Check_Einzel= arcpy.UpdateCursor(join(workspace_projekt,"Einzelhzentrali"))
        for a in cur_Check_Einzel:
            if a.Umsatz_vorher==0. and a.Umsatz_nachher ==0.:
                cur_Check_Einzel.deleteRow(a)
        del cur_Check_Einzel





    def verlustrechnung():


        cur_Standortdaten=arcpy.UpdateCursor(join(workspace_projekt,"Standortdaten"))
        try:
            arcpy.Delete_management("Verlustrechnung")
            arcpy.Delete_management(join(workspace_projekt,"Verlustrechnung"))
        except:
            pass

        try:
            arcpy.DeleteFeatures_management("Verlustrechnung")
            arcpy.DeleteFeatures_management(join(workspace_projekt,"Verlustrechnung"))
        except:
            pass
        try:
            arcpy.CreateTable_management(workspace_projekt,"Verlustrechnung")
        except:
            a="Fehler beim erstellen der Tabelle"+str("Verlustrechnung")
            messages.AddErrorMessage(a)
            print a
            exit(1)
        try:
            arcpy.AddField_management(join(workspace_projekt,"Verlustrechnung"),"GAGS","LONG")
            arcpy.AddField_management(join(workspace_projekt,"Verlustrechnung"),"GesamtGem","TEXT")
            arcpy.AddField_management(join(workspace_projekt,"Verlustrechnung"),"Umsatz_vorher","DOUBLE")
            arcpy.AddField_management(join(workspace_projekt,"Verlustrechnung"),"Umsatz_nachher","DOUBLE")
            arcpy.AddField_management(join(workspace_projekt,"Verlustrechnung"),"Differenz","DOUBLE")
            arcpy.AddField_management(join(workspace_projekt,"Verlustrechnung"),"Differenz_Proz","DOUBLE")
        except:
            pass

        cur_Ins_Verlust=arcpy.InsertCursor(join(workspace_projekt,"Verlustrechnung"))
        cur_Search_Sied = arcpy.SearchCursor(join(workspace_projekt,"Siedlungszahlendaten"))

        array_ags=[]
        for zellen in cur_Search_Sied:
            if len(array_ags)==0:
                array_ags.append(int(zellen.AGS))

            else:
                if len([r for r in array_ags if r==int(zellen.AGS)])==0:
                    array_ags.append(int(zellen.AGS))

        del cur_Search_Sied

        array_standortda=[]
        for speicher in cur_Standortdaten:
            if len([k for k in array_ags if k==int(speicher.AGS) ])>0:
                array_standortda.append([speicher.Id,speicher.Kaufkraft,int(speicher.AGS),speicher.GEN])

        del speicher,cur_Standortdaten


        ags_gemeinde_umsatz=[]
        for eintraege in array_standortda:
            if len(ags_gemeinde_umsatz)==0:
                ags_gemeinde_umsatz.append([eintraege[2],eintraege[3],eintraege[1]])

            else:
                finden=0
                for gen in ags_gemeinde_umsatz:
                    if gen[0]==eintraege[2]:
                        finden=1
                        gen[2]+=eintraege[1]
                        break
                if finden==0:
                    ags_gemeinde_umsatz.append([eintraege[2],eintraege[3],eintraege[1]])

        #zur gesamtgemeinde hinzufuegen

        cur_Sear_GGEN= arcpy.SearchCursor(join(workspace_Basis_Daten,"Gesamtgemeinden"))

        array_GGen=[]
        for speicher in cur_Sear_GGEN:
            array_GGen.append([int(speicher.AGS),speicher.Gen,int(speicher.VAGS),speicher.GGEN])

        del speicher,cur_Sear_GGEN

        array_ggen_umsatz=[]
        for einzelnegen in ags_gemeinde_umsatz:
            found=0
            for gesamtgen in array_GGen:
                if int(einzelnegen[0])== int(gesamtgen[0]):
                    array_ggen_umsatz.append([gesamtgen[2],gesamtgen[3],einzelnegen[2]])
                    found=1
            if found ==0:
                print "Komisch"



        entg_ggen_umsatz=[]

        for asd in array_ggen_umsatz:
            if len(entg_ggen_umsatz)==0:
                entg_ggen_umsatz.append([asd[0],asd[1],asd[2]])

            else:
                findemich=0
                for allezusam in entg_ggen_umsatz:
                    if allezusam[0]==asd[0]:
                        allezusam[2]+=asd[2]
                        findemich=1

                if findemich==0:
                    entg_ggen_umsatz.append([asd[0],asd[1],asd[2]])

        nullfall_entg_ggen_umsatz=entg_ggen_umsatz

        print nullfall_entg_ggen_umsatz

        for schreib in entg_ggen_umsatz:
            rows= cur_Ins_Verlust.newRow()
            rows.setValue("GAGS",schreib[0])
            if "Zentrum" not in  schreib[1]:
                rows.setValue("GesamtGem","SG/Stadt "+schreib[1])
            else:
                rows.setValue("GesamtGem",schreib[1])
            rows.setValue("Umsatz_vorher",schreib[2])
            cur_Ins_Verlust.insertRow(rows)

        del array_ggen_umsatz,entg_ggen_umsatz,array_GGen,array_standortda,cur_Ins_Verlust
        # ################################################################################################################
        cur_Standortdaten=arcpy.UpdateCursor(join(workspace_projekt,"Standortdaten_planfall"))

        array_standortda=[]
        for speicher in cur_Standortdaten:
            if len([k for k in array_ags if k==int(speicher.AGS) ])>0 and speicher.Id!=600 and speicher.Id!=601:
                array_standortda.append([speicher.Id,speicher.Kaufkraft,int(speicher.AGS),speicher.GEN])

        del speicher,cur_Standortdaten


        ags_gemeinde_umsatz=[]
        for eintraege in array_standortda:
            if len(ags_gemeinde_umsatz)==0:
                ags_gemeinde_umsatz.append([eintraege[2],eintraege[3],eintraege[1]])

            else:
                finden=0
                for gen in ags_gemeinde_umsatz:
                    if gen[0]==eintraege[2]:
                        finden=1
                        gen[2]+=eintraege[1]
                        break
                if finden==0:
                    ags_gemeinde_umsatz.append([eintraege[2],eintraege[3],eintraege[1]])

        #zur gesamtgemeinde hinzufuegen

        cur_Sear_GGEN= arcpy.SearchCursor(join(workspace_Basis_Daten,"Gesamtgemeinden"))

        array_GGen=[]
        for speicher in cur_Sear_GGEN:
            array_GGen.append([int(speicher.AGS),speicher.Gen,int(speicher.VAGS),speicher.GGEN])

        del speicher,cur_Sear_GGEN

        array_ggen_umsatz=[]
        for einzelnegen in ags_gemeinde_umsatz:
            found=0
            for gesamtgen in array_GGen:
                if int(einzelnegen[0])== int(gesamtgen[0]):
                    array_ggen_umsatz.append([gesamtgen[2],gesamtgen[3],einzelnegen[2]])
                    found=1
            if found ==0:
                print "Komisch"



        entg_ggen_umsatz=[]

        for asd in array_ggen_umsatz:
            if len(entg_ggen_umsatz)==0:
                entg_ggen_umsatz.append([asd[0],asd[1],asd[2]])

            else:
                findemich=0
                for allezusam in entg_ggen_umsatz:
                    if allezusam[0]==asd[0]:
                        allezusam[2]+=asd[2]
                        findemich=1

                if findemich==0:
                    entg_ggen_umsatz.append([asd[0],asd[1],asd[2]])



        print "Planfall", entg_ggen_umsatz
        planfall_entg_ggen_umsatz=entg_ggen_umsatz
        cur_UP_Verlust=arcpy.UpdateCursor(join(workspace_projekt,"Verlustrechnung"))

        for eintraege in cur_UP_Verlust:
            foundyou=0
            for zack in entg_ggen_umsatz:

                if eintraege.GAGS==zack[0]:
                    eintraege.setValue("Umsatz_nachher",zack[2])
                    foundyou=1
                    cur_UP_Verlust.updateRow(eintraege)

            if foundyou==0:
                cur_Ins_Verlust=arcpy.InsertCursor(join(workspace_projekt,"Verlustrechnung"))

                row= cur_Ins_Verlust.newRow()
                row.setValue("GAGS",zack[0])
                row.setValue("GesamtGem",zack[1])
                row.setValue("Umsatz_vorher",0)
                row.setValue("Umsatz_nachher",zack[2])
                cur_Ins_Verlust.insertRow(row)
                del cur_Ins_Verlust

        del array_ggen_umsatz,entg_ggen_umsatz,array_standortda,cur_UP_Verlust



    # ###################################################################################################################################
        cur_Zentren= arcpy.SearchCursor(join(workspace_projekt,"Zentren"))
        cur_Standortdaten=arcpy.UpdateCursor(join(workspace_projekt,"Standortdaten"))


        array_standortda=[]
        for speicher in cur_Standortdaten:
            if len([k for k in array_ags if k==int(speicher.AGS) ])>0:
                array_standortda.append([speicher.Id,speicher.Kaufkraft,int(speicher.AGS),speicher.GEN])
        del cur_Standortdaten,speicher

        array_zentren_ags_umsatz=[]
        for zen in cur_Zentren:
            for markt in array_standortda:
                if zen.Markt_1==markt[0]:
                    array_zentren_ags_umsatz.append([markt[2],zen.Zentren+str(" Zentrum"),markt[1]])
                    break

        del cur_Zentren

        for aa in array_zentren_ags_umsatz:
            for uu in array_GGen:
                if int(aa[0])==int (uu[0]):
                    aa[0]=uu[2]

        rest=[]
        for zz in array_zentren_ags_umsatz:
            for ii in nullfall_entg_ggen_umsatz:
                if zz[0]==ii[0]:
                    ii[2]-=zz[2]
                    print "treffer ", ii[1] , ii[2]
                    if len([k for k in rest if k[0]==ii[0]*100])>0:
                        for u in rest:
                            if u[0]==ii[0]*100:
                                u[2]=ii[2]
                                break
                    else:
                        rest.append([ii[0]*100,ii[1]+str(' Rest'),ii[2]])
                    break

        print rest

        final_zentren=[]
        for x, tz in enumerate( array_zentren_ags_umsatz):
            if len(final_zentren)==0:
                final_zentren.append([x,tz[1],tz[2]])

            else:
                pfund=0
                for a in final_zentren:
                    if tz[1]==a[1]:
                        a[2]+=tz[2]
                        pfund=1
                        break
                if pfund==0:
                    final_zentren.append([x,tz[1],tz[2]])

        cur_Ins_Verlust=arcpy.InsertCursor(join(workspace_projekt,"Verlustrechnung"))
        final_zentren=final_zentren+rest
        print final_zentren

        for schreib in final_zentren:
            rows= cur_Ins_Verlust.newRow()
            rows.setValue("GAGS",schreib[0])
            rows.setValue("GesamtGem", schreib[1])
            rows.setValue("Umsatz_vorher",schreib[2])
            cur_Ins_Verlust.insertRow(rows)

        del cur_Ins_Verlust,rest,final_zentren,array_zentren_ags_umsatz,nullfall_entg_ggen_umsatz
    # #############################################################################################
        cur_Zentren= arcpy.SearchCursor(join(workspace_projekt,"Zentren"))
        cur_Standortdaten=arcpy.UpdateCursor(join(workspace_projekt,"Standortdaten_planfall"))


        array_standortda=[]
        for speicher in cur_Standortdaten:
            if len([k for k in array_ags if k==int(speicher.AGS) ])>0 and speicher.Id!=600 and speicher.Id!=601:
                array_standortda.append([speicher.Id,speicher.Kaufkraft,int(speicher.AGS),speicher.GEN])
        del cur_Standortdaten,speicher

        array_zentren_ags_umsatz=[]
        for zen in cur_Zentren:
            for markt in array_standortda:
                if zen.Markt_1==markt[0]:
                    array_zentren_ags_umsatz.append([markt[2],zen.Zentren+str(" Zentrum"),markt[1]])
                    break

        del cur_Zentren

        for aa in array_zentren_ags_umsatz:
            for uu in array_GGen:
                if int(aa[0])==int (uu[0]):
                    aa[0]=uu[2]

        rest=[]
        for zz in array_zentren_ags_umsatz:
            for ii in planfall_entg_ggen_umsatz:
                if zz[0]==ii[0]:
                    ii[2]-=zz[2]
                    print "treffer ", ii[1] , ii[2]
                    if len([k for k in rest if k[0]==ii[0]*100])>0:
                        for u in rest:
                            if u[0]==ii[0]*100:
                                u[2]=ii[2]
                                break
                    else:
                        rest.append([ii[0]*100,ii[1]+str(' Rest'),ii[2]])
                    break

        print rest

        final_zentren=[]
        for x, tz in enumerate( array_zentren_ags_umsatz):
            if len(final_zentren)==0:
                final_zentren.append([x,tz[1],tz[2]])

            else:
                pfund=0
                for a in final_zentren:
                    if tz[1]==a[1]:
                        a[2]+=tz[2]
                        pfund=1
                        break
                if pfund==0:
                    final_zentren.append([x,tz[1],tz[2]])

        final_zentren=final_zentren+rest
        print final_zentren

        cur_UP_Verlust=arcpy.UpdateCursor(join(workspace_projekt,"Verlustrechnung"))

        for eintraege in cur_UP_Verlust:
            for adden in final_zentren:
                if eintraege.GAGS == adden[0] or eintraege.GAGS == adden[0]*100:
                    eintraege.setValue("Umsatz_nachher",adden[2])
                    cur_UP_Verlust.updateRow(eintraege)
                    break

        del rest,final_zentren,array_zentren_ags_umsatz,cur_UP_Verlust,planfall_entg_ggen_umsatz


        arcpy.CalculateField_management(join(workspace_projekt,"Verlustrechnung"), "Differenz", "-!Umsatz_vorher!+!Umsatz_nachher!", "PYTHON", "")
        arcpy.CalculateField_management(join(workspace_projekt,"Verlustrechnung"), "Differenz_Proz", "!Differenz!*100/!Umsatz_vorher!", "PYTHON", "")

    def Umsatz_dif():

        cur_Statistik=arcpy.UpdateCursor(workspace_projekt+"/Statistik")
        cur_Statistik_plan= arcpy.UpdateCursor(workspace_projekt+"/Statistik_planfall")

        try:
            arcpy.Delete_management(workspace_projekt+"/Diff_Umsatz")
        except:
            pass


        try:

            arcpy.CreateTable_management(arcpy.env.workspace,"Diff_Umsatz","Statistik_planfall")
        except:
            print"a) Fehler beim erstellen der Tabelle"+str("Diff_Umsatz")
            return 1

        fieldnames = [f.name for f in arcpy.ListFields(workspace_projekt+"/Statistik_planfall")]
        fieldnames=fieldnames[2:]
    ##    print fieldnames
        array=[]
        for c in cur_Statistik_plan:
            for a in cur_Statistik:
                for b in fieldnames:
                    try:
                        if (b=="SUM_ID_600" or b=="SUM_ID_601" ):
                            array.append([b,c.getValue(b)])
                        else:
                            dif=a.getValue(b)-c.getValue(b)
                            array.append([b,dif])

                    except:
                ##                    array.append([b,0])
                        pass

        print array

        cur_ins = arcpy.InsertCursor(workspace_projekt+"\Diff_Umsatz")
        zeile = cur_ins.newRow()
        for zu in range(len(array)):
            zeile.setValue(str(array[zu][0]),array[zu][1])

        cur_ins.insertRow(zeile)

        del cur_ins,cur_Statistik,cur_Statistik_plan

        fieldnames = [f.name for f in arcpy.ListFields(join(workspace_projekt,"Diff_Umsatz"))]
        fieldnames=fieldnames[2:]
        loeschfield=[]
        upd_cur_diif_um=arcpy.UpdateCursor(join(workspace_projekt,"Diff_Umsatz"))
        for a in upd_cur_diif_um:
            for spaltenchecker in fieldnames:
        ##            print spaltenchecker, a.getValue(spaltenchecker)
                if (a.getValue(spaltenchecker)==None):
                    loeschfield.append(str(spaltenchecker))

    ##    print loeschfield
        del upd_cur_diif_um ,a
        for zz in loeschfield:
    ##        print zz
            arcpy.DeleteField_management (join(workspace_projekt,"Diff_Umsatz"), str(zz))

    gc.collect()

    projektname = parameters[0].valueAsText

    #Pfade einrichten
    base_path = str(sys.path[0]).split("2_Tool")[0]

    workspace_Basis = join(base_path, '1_Basisdaten', 'FGBD_01_Basisdaten_deutschland.gdb')
    workspace_Basis_Daten = join(base_path, '2_Tool', '34_Standortkonkurrenz_Supermaerkte','FGDB_34_Standortkonkurrenz_Supermaerkte_Tool.gdb')
    workspace_projekt = join(base_path, '3_Projekte', projektname,
                                     'FGDB_34_Standortkonkurrenz_Supermaerkte_' + projektname + '.gdb')


    arcpy.env.workspace=workspace_projekt
    arcpy.env.overwriteOutput = True

    tablepath_neuer_markt = join(base_path,'3_Projekte',projektname,'FGDB_34_Standortkonkurrenz_Supermaerkte.gdb','Neuer_Markt')
    tablepath_siedlungszellen = join(base_path,'3_Projekte',projektname,'FGDB_34_Standortkonkurrenz_Supermaerkte.gdb','Siedlungszahlendaten')
    tablepath_standorte = join(base_path,'3_Projekte',projektname,'FGDB_34_Standortkonkurrenz_Supermaerkte.gdb','Standortdaten')
    tablepath_neuerMarkt = join(base_path,'3_Projekte',projektname,'FGDB_34_Standortkonkurrenz_Supermaerkte.gdb','Neuer_Markt')
    tablepath_zentren = join(base_path,'3_Projekte',projektname,'FGDB_34_Standortkonkurrenz_Supermaerkte.gdb','Zentren')
    tablepath_matrix = join(base_path,'3_Projekte',projektname,'FGDB_34_Standortkonkurrenz_Supermaerkte.gdb','Distanzmatrix_planfall')

    if arcpy.Exists(tablepath_siedlungszellen) and  arcpy.Exists(tablepath_standorte)and  arcpy.Exists(tablepath_neuerMarkt) and  arcpy.Exists(tablepath_zentren) and arcpy.Exists(tablepath_neuer_markt)and arcpy.Exists(tablepath_matrix):
        messages.AddMessage("Alle Daten vorhanden und bereit. Tool wird gestartet...")
    else:
        messages.AddErrorMessage("Datengrundlage nicht vollstaendig vorhanden. Bitte wiederholen Sie die vorherigen Tools")
        messages.AddErrorMessage("tritt der Error erneut auf kontaktieren Sie uns bitte.")
        exit(1)

    del tablepath_matrix,tablepath_siedlungszellen,tablepath_standorte,tablepath_neuerMarkt,tablepath_zentren


    #Ablauf
    messages.AddMessage("Beziehe notwendige Daten aus der Datenbank")
    Betriebstyperstellen("Standortdaten")
    Einwohnerfinden("Standortdaten")
    EWZ_GGAGS_bestimmen("Standortdaten")
    betriebstyp_bestimmung("Standortdaten")
    betriebstyp_bestimmung_expF("Standortdaten")
    messages.AddMessage("Erstelle Betriebstypenzuteilung")
    Betriebstyperstellen("Standortdaten_planfall")
    Einwohnerfinden("Standortdaten_planfall")
    EWZ_GGAGS_bestimmen("Standortdaten_planfall")
    betriebstyp_bestimmung("Standortdaten_planfall")
    betriebstyp_bestimmung_expF("Standortdaten_planfall")
    messages.AddMessage("Berechnung des Nullfalls starten")
    berechnung_siedlungsdaten("Siedlungszahlendaten")
    if KK_Anteile_Wahrsch("KK_Anteile_Wahrsch","Distanzmatrix","Standortdaten")==1:
        print "Fehler in KK_Anteile_Wahrsch"
        exit(1)

    messages.AddMessage("Die weiteren Berechnungsschritte benoetigen reichlich Zeit")
    Kleinste_Distanzen("Distanzmatrix","Standortdaten","Distanzmatrix_dichteste")
    messages.AddMessage("1/5 Berechnungsschritte")
    Attraktivitaet("Standortdaten","Distanzmatrix_dichteste","Distanzmatrix_dichteste_gewi")
    messages.AddMessage("2/5 Berechnungsschritte")
    #sd(shp_Siedlungszahlendaten,shp_Standortdaten,shp_Distanzmatrix,shp_KK_Anteile_Wahrsch,shp_Distanzmatrix_dichteste,shp_shp_Distanzmatrix_dichteste_gewichtung,shp_Verteilungsmasstab1,shp_Verteilungsmasstab2,shp_ET_Kaufkraft):
    asd("Siedlungszahlendaten","Standortdaten","Distanzmatrix","KK_Anteile_Wahrsch","Distanzmatrix_dichteste","Distanzmatrix_dichteste_gewi","Verteilungsmas_1","Verteilungsmas_2","ET_Kaufkraft")
    messages.AddMessage("3/5 Berechnungsschritte")
    schreibe_KK("/Standortdaten","/ET_Kaufkraft","/Statistik")
    messages.AddMessage("4/5 Berechnungsschritte")
    bilde_gesamt("/Uebersicht","/Standortdaten")

    messages.AddMessage("5/5 Berechnungsschritte")

    #------------------------------------------------------------------Berechnung Nullfall beendet
    messages.AddMessage("Berechnung des Planfalls starten")
    berechnung_siedlungsdaten("Siedlungszahlendaten_planfall")
    if KK_Anteile_Wahrsch("KK_Anteile_Wahrsch_planfall","Distanzmatrix_planfall","Standortdaten_planfall")==1:
        print "Fehler in KK_Anteile_Wahrsch_planfall"
        exit(1)

    messages.AddMessage("Die weiteren Berechnungsschritte benoetigen reichlich Zeit")
    Kleinste_Distanzen("Distanzmatrix_planfall","Standortdaten_planfall","Distanzmatrix_dichteste_planfall")
    messages.AddMessage("1/5 Berechnungsschritte")
    Attraktivitaet("Standortdaten_planfall","Distanzmatrix_dichteste_planfall","Distanzmatrix_dichteste_gewi_planfall")
    messages.AddMessage("2/5 Berechnungsschritte")
    #sd(shp_Siedlungszahlendaten,shp_Standortdaten,shp_Distanzmatrix,shp_KK_Anteile_Wahrsch,shp_Distanzmatrix_dichteste,shp_shp_Distanzmatrix_dichteste_gewichtung,shp_Verteilungsmasstab1,shp_Verteilungsmasstab2,shp_ET_Kaufkraft):
    asd("Siedlungszahlendaten_planfall","Standortdaten_planfall","Distanzmatrix_planfall","KK_Anteile_Wahrsch_planfall","Distanzmatrix_dichteste_planfall","Distanzmatrix_dichteste_gewi_planfall","Verteilungsmas_1_planfall","Verteilungsmas_2_planfall","ET_Kaufkraft_planfall")
    messages.AddMessage("3/5 Berechnungsschritte")
    schreibe_KK("/Standortdaten_planfall","/ET_Kaufkraft_planfall","/Statistik_planfall")
    messages.AddMessage("4/5 Berechnungsschritte")
    bilde_gesamt("/Uebersicht_planfall","/Standortdaten_planfall")
    messages.AddMessage("5/5 Berechnungsschritte")
    messages.AddMessage("Erstelle Abschlussbericht bzw. Deltabetrachtungen")
    verlustrechnung()
    einzelhandelszentrali()
    verkaufsflaeche_zent()
    kaufkraft_inSied("Siedlungszahlendaten_planfall","ET_Kaufkraft_planfall")
    Umsatz_dif()

    ErgebnisExport(projektname)

    gc.collect()

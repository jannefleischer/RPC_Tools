# -*- coding: cp1252 -*-

def ags_extrahieren(projektname):
    import arcpy,sys,os
    base_path = str(sys.path[0]).split("2_Tool")[0]
    print("Den AGS aus der Lage der Projektflaeche im Raum ermitteln")
    arcpy.AddMessage("Den AGS aus der Lage der projektfläche im Raum ermitteln")
    projektFlaeche = os.path.join(base_path ,"3_Projekte",  projektname ,"FGDB_11_Definition_Projekt_" + projektname +".gdb","Teilflaechen_Plangebiet")
    bkg = os.path.join( base_path, "1_Basisdaten","FGBD_01_Basisdaten_deutschland.gdb","bkg_gemeinden")
    #ags aus BKG Daten extrahieren, dafür Gemeinde selektieren, die von Planfläche geschnitten wird
    #1. Feature Layer aus den bkg-daten erstellen
    arcpy.MakeFeatureLayer_management(bkg,"bkg_lyr")
    #2.Spatial Select wo Planfläche bkg_lyr intersected
    arcpy.SelectLayerByLocation_management("bkg_lyr", "INTERSECT", projektFlaeche)
    #Wenn Flaeche = 1, ags extrahieren
    n = arcpy.GetCount_management("bkg_lyr").getOutput(0)
    if(int(n) ==1 ):
        gemeindeCursor = arcpy.SearchCursor("bkg_lyr")
        for gemeinde in gemeindeCursor:
            ags = gemeinde.AGS
    return ags

def ags_samtgemeinde(projektname):#
    # TODO wenn json return = [] ags der samtgemeinde fuer eine neue abfrage nutzen
    import arcpy,sys,os
    base_path = str(sys.path[0]).split("2_Tool")[0]
    print("Den AGS aus der Lage der Projektflaeche im Raum ermitteln")
    arcpy.AddMessage("Den AGS aus der Lage der projektfläche im Raum ermitteln")
    projektFlaeche = os.path.join(base_path ,"3_Projekte",  projektname ,"FGDB_11_Definition_Projekt_" + projektname +".gdb","Teilflaechen_Plangebiet")
    vgm = os.path.join( base_path, "1_Basisdaten","FGBD_01_Basisdaten_deutschland.gdb","vgm")
    #ags aus BKG Daten extrahieren, dafür Gemeinde selektieren, die von Planfläche geschnitten wird
    #1. Feature Layer aus den bkg-daten erstellen
    try:
        arcpy.Delete_management("vgm_lyr")
    except:
        print""
    arcpy.MakeFeatureLayer_management(vgm,"vgm_lyr")
    #2.Spatial Select wo Planfläche vgm_lyr intersected
    arcpy.SelectLayerByLocation_management("vgm_lyr", "INTERSECT", projektFlaeche)
    #Wenn Flaeche = 1, ags extrahieren
    n = arcpy.GetCount_management("vgm_lyr").getOutput(0)
    print n


    if(int(n) == 1 ):
        gemeindeCursor = arcpy.SearchCursor("vgm_lyr")
        for gemeinde in gemeindeCursor:
            ags_temp = gemeinde.SDV_RS
    else:
        arcpy.AddMessage("Die Projektflaechen liegen innerhalb mehrerer Gemeinden, das Tool unterstuetzt zur Zeit keine interkommunalen Projekte.")
        ## TODO Dateien loeschen und Projektregistrierung loeschen)
        sys.exit()
    ags = str(ags_temp[0:5])+str(ags_temp[6:])

    return ags


def bevdaten_download(projektname, ags, jahr, geschlecht):
    import urllib2, json, arcpy, sys,os
    from pprint import pprint
    #api endpunkt fuer die Tabelle "Fortschreibung des Bevoelkerungsstandes"
    #(http://regenesis.pudo.org/regional/statistics/fortschreibung-des-bevolkerungsstandes.12411.html)
    # Variablen definieren
    #Pfade einrichten
    base_path = str(sys.path[0]).split("2_Tool")[0]
    #workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
    workspace_projekt_bevoelkerung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_22_BevModellierung_'+projektname+'.gdb')
    #workspace_tool_bevoelkerung = os.path.join(base_path,"2_Tool","22_Bevoelkerungsmodellierung","FGDB_22_Bevoelkerungsmodellierung_Tool.gdb")
    bevoelkerung_gemeinde_pfad = os.path.join(workspace_projekt_bevoelkerung, "bevoelkerung")
    #bevoelkerung_gemeinde_grob_pfad = os.path.join(workspace_projekt_bevoelkerung, "bevoelkerung_altersgruppen")
    #wanderung_gemeinde_pfad = os.path.join(workspace_projekt_bevoelkerung, "wanderung_altersgruppen")
    #wanderungsraten_gemeinde_pfad = os.path.join(workspace_projekt_bevoelkerung, "wanderungsraten_altersgruppen")
    #raten_pfad = os.path.join(workspace_tool_bevoelkerung,"raten")
    #prognose_pfad = os.path.join(workspace_projekt_bevoelkerung, "bevoelkerung_prognose")


    #Abfrage Bevölkerungszahlen für die letzten 4 jahre
    iteratorjahr = int(jahr) - 3
    print iteratorjahr
    while iteratorjahr < int(jahr)+1:
        #Überprüfen ob schon eine Abfrage mit den gewählten parametern gemacht wurde (Bevoelkerung)
        where_clause = '"jahr" = ' + str(iteratorjahr) + " AND " + '"geschlecht" = ' + "'" + geschlecht + "' AND "+'"ags" = '+ "'" + str(ags) + "'"
        print where_clause
        bevoelkerung_gemeinde_test = arcpy.UpdateCursor(bevoelkerung_gemeinde_pfad, where_clause)
        iterator = 0
        for row in bevoelkerung_gemeinde_test:
            iterator +=1
        if (iterator>0):
            bevoelkerung_abfragen = False
            print "Datensatz zur Bevoelkerung schon vorhanden"
            arcpy.AddMessage("Datensatz zur Bevoelkerung schon vorhanden")
        else:
            bevoelkerung_abfragen = True
            print "Datensatz zur Bevoelkerung noch nicht vorhanden, wird abgefragt...."
            arcpy.AddMessage("Datensatz zur Bevoelkerung noch nicht vorhanden, wird abgefragt....")



        del bevoelkerung_gemeinde_test

        #Tabelle öffnen
        if (bevoelkerung_abfragen == True):
            bevoelkerung_gemeinde = arcpy.InsertCursor(bevoelkerung_gemeinde_pfad)
            row = bevoelkerung_gemeinde.newRow()
            url = "http://api.regenesis.pudo.org/cube/12411gj004/facts?" #<--Altersklassen Bevölkerung
            #url = "http://api.regenesis.pudo.org/cube/12411rj005/facts?" #Altersjahre
            parameter = "cut=gemein.name:" + str(ags)
            query = url+parameter
            print query
            try:
                queryresult = urllib2.urlopen(query)
                jsonContent = queryresult.read()
                #leeres Ergebnis abfangen falls der ags nichts zurueck gibt weil Samtgemeinde/Verwaltungsgemeinschaft
                if jsonContent == "[]":
                    arcpy.AddMessage("Die Abfrage mit dem AGS "+str(ags)+" hat kein Ergebnis gegeben. Test ob Samtgemeinde/VGM vorliegt..")
                    ags = ags_samtgemeinde(projektname)
                    parameter = "cut=gemein.name:" + str(ags)
                    query = url+parameter
                    queryresult = urllib2.urlopen(query)
                    jsonContent = queryresult.read()
                    #Falls die Abfrage mit dem zweiten AGS auch kein Ergebnis bringt, Programm mit Fehlermeldung beenden
                    if jsonContent == "[]":
                        arcpy.AddMessage("Es gab ein Problem mit der Ermittlung des AGS. Bitte ueberpruefen Sie die die Lage der Projektflaeche")
                        sys.exit()
                data = json.loads(jsonContent)
            except Exception as e:
                pprint(e)
            #json Datensatz Filtern und die Werte auf die entsprechenden Zellen verteilen
            #pprint(data)
            for eintrag in data:
                #pprint(eintrag)

                jahr_filter = "31.12."+str(iteratorjahr)
                geschlecht_filter = geschlecht
                #print jahr_filter
                #Jahr Filtern:
                if eintrag["stag.text"] == jahr_filter and eintrag["ges.name"] == geschlecht_filter:
                    column = eintrag["altx20.name"]
                    value = eintrag["bevstd"]
                    #print column
                    #print value
                    row.setValue(column, value)
                    row.ags = ags
                    row.jahr = iteratorjahr
                    row.geschlecht = geschlecht

            #tabelle updaten
            bevoelkerung_gemeinde.insertRow(row)
            del row, bevoelkerung_gemeinde
        iteratorjahr+=1
    #den ags an das ausfuehrungsskript zurueckgeben, damit  berechnungen mit dem richtigen ags ausgefuehert werden
    #Wichtig falls Samtgemeinde/VGM
    return ags

def wanderungsdaten_download(projektname, ags, jahr, geschlecht):
    import urllib2, json, arcpy, sys,os
    from pprint import pprint
    #api endpunkt fuer die Tabelle "Fortschreibung des Bevoelkerungsstandes"
    #(http://regenesis.pudo.org/regional/statistics/fortschreibung-des-bevolkerungsstandes.12411.html)
    # Variablen definieren
    #Pfade einrichten
    base_path = str(sys.path[0]).split("2_Tool")[0]
    #workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
    workspace_projekt_bevoelkerung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_22_BevModellierung_'+projektname+'.gdb')
    #workspace_tool_bevoelkerung = os.path.join(base_path,"2_Tool","22_Bevoelkerungsmodellierung","FGDB_22_Bevoelkerungsmodellierung_Tool.gdb")
   #bevoelkerung_gemeinde_pfad = os.path.join(workspace_projekt_bevoelkerung, "bevoelkerung")
    #bevoelkerung_gemeinde_grob_pfad = os.path.join(workspace_projekt_bevoelkerung, "bevoelkerung_altersgruppen")
    wanderung_gemeinde_pfad = os.path.join(workspace_projekt_bevoelkerung, "wanderung_altersgruppen")
    #wanderungsraten_gemeinde_pfad = os.path.join(workspace_projekt_bevoelkerung, "wanderungsraten_altersgruppen")
    #raten_pfad = os.path.join(workspace_tool_bevoelkerung,"raten")
    #prognose_pfad = os.path.join(workspace_projekt_bevoelkerung, "bevoelkerung_prognose")
    #Abfrage Wanderungsdaten
    #Wanderungsdaten für die letzten 5 Jahre downloaden um eine stabile Basis zur Berechnung der Daten zu entwickeln
    iteratorjahr = int(jahr) - 3
    print iteratorjahr
    while iteratorjahr < int(jahr)+1:
        #Überprüfen ob schon eine Abfrage mit den gewählten parametern gemacht wurde (Bevoelkerung)
        where_clause = '"jahr" = ' + str(iteratorjahr) + " AND " + '"geschlecht" = ' + "'" + geschlecht + "' AND "+'"ags" = '+ "'" + str(ags) + "'"
        print where_clause
        wanderung_gemeinde_test = arcpy.UpdateCursor(wanderung_gemeinde_pfad, where_clause)
        iterator = 0
        for row in wanderung_gemeinde_test:
            iterator +=1
        if (iterator>0):
            wanderung_abfragen = False
            print "Datensatz zur Wanderung schon vorhanden"
            arcpy.AddMessage("Datensatz zur Wanderung schon vorhanden")
        else:
            wanderung_abfragen = True
            print "Datensatz zur Wanderung noch nicht vorhanden, wird abgefragt...."
            arcpy.AddMessage("Datensatz zur Wanderung noch nicht vorhanden, wird abgefragt....")
        del wanderung_gemeinde_test
        #Tabelle öffnen
        if (wanderung_abfragen == True):
            wanderung_gemeinde = arcpy.InsertCursor(wanderung_gemeinde_pfad)
            row = wanderung_gemeinde.newRow()
            url = "http://api.regenesis.pudo.org/cube/12711gj001/facts?" #<--Altersklassen Wanderungen
            #url = "http://api.regenesis.pudo.org/cube/12411rj005/facts?" #Altersjahre
            parameter = "cut=gemein.name:" + str(ags)
            query = url+parameter
            print query
            try:
                queryresult = urllib2.urlopen(query)
                jsonContent = queryresult.read()
                #leeres Ergebnis abfangen falls der ags nichts zurueck gibt weil Samtgemeinde/Verwaltungsgemeinschaft
                if jsonContent == "[]":
                    arcpy.AddMessage("Die Abfrage mit dem AGS "+str(ags)+" hat kein Ergebnis gegeben. Test ob Samtgemeinde/VGM vorliegt..")
                    ags = ags_samtgemeinde(projektname)
                    parameter = "cut=gemein.name:" + str(ags)
                    query = url+parameter
                    queryresult = urllib2.urlopen(query)
                    jsonContent = queryresult.read()
                    data = json.loads(jsonContent)
                    #Falls die Abfrage mit dem zweiten AGS auch kein Ergebnis bringt, Programm mit Fehlermeldung beenden
                    if jsonContent == "[]":
                        arcpy.AddMessage("Es gab ein Problem mit der Ermittlung des AGS. Bitte ueberpruefen Sie die die Lage der Projektflaeche")
                        sys.exit()
                data = json.loads(jsonContent)

            except Exception as e:
                pprint(e)
            #json Datensatz Filtern und die Werte auf die entsprechenden Zellen verteilen
            for eintrag in data:
                #pprint(eintrag)
                jahr_filter = str(iteratorjahr)
                geschlecht_filter = geschlecht
                #Jahr Filtern:
                #print eintrag["jahr.text"] +" = " + jahr_filter + " " + eintrag["ges.name"] + " = " + geschlecht_filter
                if eintrag["jahr.text"] == jahr_filter and eintrag["ges.name"] == geschlecht_filter:
                    #pprint(eintrag["altx01.name"])
                    column = eintrag["altx01.name"]
                    #zuzuege minus fortzuege ergibt das wanderungssaldo
                    value = eintrag["bev081"] - eintrag["bev082"]
                    #print column
                    #print value
                    row.setValue(column, value)
                    row.ags = ags
                    row.jahr = iteratorjahr
                    row.geschlecht = geschlecht


            wanderung_gemeinde.insertRow(row)

            del row, wanderung_gemeinde
        iteratorjahr += 1

def wanderungsdaten_dissaggegieren(projektname, ags, jahr,geschlecht):
    import urllib2, json, arcpy, sys,os
    from pprint import pprint
    #api endpunkt fuer die Tabelle "Fortschreibung des Bevoelkerungsstandes"
    #(http://regenesis.pudo.org/regional/statistics/fortschreibung-des-bevolkerungsstandes.12411.html)
    # Variablen definieren
    #Pfade einrichten
    base_path = str(sys.path[0]).split("2_Tool")[0]
    workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
    workspace_projekt_bevoelkerung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_22_BevModellierung_'+projektname+'.gdb')
    workspace_tool_bevoelkerung = os.path.join(base_path,"2_Tool","22_Bevoelkerungsmodellierung","FGDB_22_Bevoelkerungsmodellierung_Tool.gdb")
    bevoelkerung_gemeinde_pfad = os.path.join(workspace_projekt_bevoelkerung, "bevoelkerung")
    bevoelkerung_gemeinde_grob_pfad = os.path.join(workspace_projekt_bevoelkerung, "bevoelkerung_altersgruppen")
    wanderung_gemeinde_pfad = os.path.join(workspace_projekt_bevoelkerung, "wanderung_altersgruppen")
    wanderung_gemeinde_fein_pfad = os.path.join(workspace_projekt_bevoelkerung, "wanderung")
    wanderungsraten_gemeinde_pfad = os.path.join(workspace_projekt_bevoelkerung, "wanderungsraten_altersgruppen")
    raten_pfad = os.path.join(workspace_tool_bevoelkerung,"raten")
    prognose_pfad = os.path.join(workspace_projekt_bevoelkerung, "bevoelkerung_prognose")

    #Daten für das Startjahr und die letzten 4 Jahre rückwirkend verarbeiten
    iteratorjahr = int(jahr) - 3
    while iteratorjahr < int(jahr)+1:
        #Überprüfen ob schon eine Dissaggregation durchgeführt wurde
        where_clause = '"jahr" = ' + str(iteratorjahr) + " AND " + '"geschlecht" = ' + "'" + geschlecht + "' AND "+'"ags" = '+ "'" + str(ags) + "'"
        #print where_clause
        wanderung_fein_test = arcpy.UpdateCursor(wanderung_gemeinde_fein_pfad, where_clause)
        iterator = 0
        for row in wanderung_fein_test:
            iterator +=1
        if (iterator>0):
            wanderung_dissaggregieren = False
            print "Datensatz zur Wanderung bereits dissaggregiert"
            arcpy.AddMessage("Datensatz zur Wanderung schon vorhanden")
        else:
            wanderung_dissaggregieren = True
            print "Datensatz zur Wanderung noch nicht dissaggregiert, wird dissaggregiert...."
            arcpy.AddMessage("Datensatz zur Wanderung noch nicht vorhanden, wird abgefragt....")
        del wanderung_fein_test
        #where_clause = '"jahr" = ' + str(iteratorjahr) + " AND " + '"geschlecht" = ' + "'" + geschlecht + "' AND "+'"ags" = '+ "'" + str(ags) + "'"

        if wanderung_dissaggregieren == True:
            print("Dissaggregation")
            arcpy.AddMessage("Dissaggregation")
            #Grobe Wanderungsdaten
            wanderung_grob = arcpy.SearchCursor(wanderung_gemeinde_pfad, where_clause)
            #Zieltabelle
            wanderung_fein = arcpy.InsertCursor(wanderung_gemeinde_fein_pfad)
            for zeile in wanderung_grob:
                row = wanderung_fein.newRow()
                row.jahr = iteratorjahr
                row.ags = ags
                row.geschlecht=geschlecht
                #Die grobe Verteilung anteilig auf die Feine Verteilung runter brechen, Anteil ergibt sich aus der
                #Anzahl der Jahre an der Gesamtanzahl (18 jahre für die erste Zeile)
                row.alt000b03 = float(zeile.alt000b18)/18*3
                row.alt003b06 = float(zeile.alt000b18)/18*3
                row.alt006b10 = float(zeile.alt000b18)/18*4
                row.alt010b15 = float(zeile.alt000b18)/18*5
                row.alt015b18 = float(zeile.alt000b18)/18*3
                row.alt018b20 = float(zeile.alt018b25)/7*2
                row.alt020b25 = float(zeile.alt018b25)/7*5
                row.alt025b30 = float(zeile.alt025b30)
                row.alt030b35 = float(zeile.alt030b50)/20*5
                row.alt035b40 = float(zeile.alt030b50)/20*5
                row.alt040b45 = float(zeile.alt030b50)/20*5
                row.alt045b50 = float(zeile.alt030b50)/20*5
                row.alt050b55 = float(zeile.alt050b65)/15*5
                row.alt055b60 = float(zeile.alt050b65)/15*5
                row.alt060b65 = float(zeile.alt050b65)/15*5
                row.alt065b75 = float(zeile.alt065um)/20*10
                row.alt075um = float(zeile.alt065um)/20*10

                wanderung_fein.insertRow(row)

            #löschen
            del wanderung_fein, wanderung_grob
        iteratorjahr +=1

def wanderungsraten_berechnen(projektname, ags, jahr,geschlecht):

    import arcpy, sys,os
    #api endpunkt fuer die Tabelle "Fortschreibung des Bevoelkerungsstandes"
    #(http://regenesis.pudo.org/regional/statistics/fortschreibung-des-bevolkerungsstandes.12411.html)
    # Variablen definieren
    #Pfade einrichten
    base_path = str(sys.path[0]).split("2_Tool")[0]
    workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
    workspace_projekt_bevoelkerung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_22_BevModellierung_'+projektname+'.gdb')
    workspace_tool_bevoelkerung = os.path.join(base_path,"2_Tool","22_Bevoelkerungsmodellierung","FGDB_22_Bevoelkerungsmodellierung_Tool.gdb")
    bevoelkerung_gemeinde_pfad = os.path.join(workspace_projekt_bevoelkerung, "bevoelkerung")
    bevoelkerung_gemeinde_grob_pfad = os.path.join(workspace_projekt_bevoelkerung, "bevoelkerung_altersgruppen")
    wanderung_gemeinde_pfad = os.path.join(workspace_projekt_bevoelkerung, "wanderung_altersgruppen")
    wanderung_gemeinde_fein_pfad = os.path.join(workspace_projekt_bevoelkerung, "wanderung")
    wanderungsraten_gemeinde_pfad = os.path.join(workspace_projekt_bevoelkerung, "wanderungsraten")
    raten_pfad = os.path.join(workspace_tool_bevoelkerung,"raten")
    prognose_pfad = os.path.join(workspace_projekt_bevoelkerung, "bevoelkerung_prognose")

    #Überprüfen ob schon eine Berechnung durchgeführt wurde
    where_clause ='"geschlecht" = ' + "'" + geschlecht + "' AND "+'"ags" = '+ "'" + str(ags) + "'"
    print where_clause
    wanderungsraten_test = arcpy.SearchCursor(wanderungsraten_gemeinde_pfad, where_clause)
    iterator = 0
    for row in wanderungsraten_test:
        iterator +=1
    if (iterator>0):
        raten_berechnen = False
        print "Wanderungsraten bereits berechnet"
        arcpy.AddMessage("Wanderungsrsten bereits berechnet")
    else:
        raten_berechnen = True
        print "Wanderungsraten noch nicht berechnet, werden berechnet...."
        arcpy.AddMessage("Wanderungsraten noch nicht berechnet, werden berechnet....")
    del wanderungsraten_test
    if raten_berechnen == True:
        wanderungsraten_dict = {}
        iteratorjahr = int(jahr)-3
        while(iteratorjahr<int(jahr)+1):
            where_clause = '"jahr" = ' + str(iteratorjahr) + " AND " + '"geschlecht" = ' + "'" + geschlecht + "' AND "+'"ags" = '+ "'" + str(ags) + "'"
            #print "iteratorjahr = " + str(iteratorjahr)
            print where_clause
            #print(wanderung_gemeinde_fein_pfad)
            print(bevoelkerung_gemeinde_pfad)

            wanderung = arcpy.SearchCursor(wanderung_gemeinde_fein_pfad,where_clause)
            bevoelkerung = arcpy.SearchCursor(bevoelkerung_gemeinde_pfad, where_clause)

            for row in wanderung:
                #print row
                wand_alt000b03 = row.alt000b03
                wand_alt003b06 	=row.alt003b06
                wand_alt006b10 	=row.alt006b10
                wand_alt010b15 	=row.alt010b15
                wand_alt015b18 	=row.alt015b18
                wand_alt018b20 	=row.alt018b20
                wand_alt020b25 	=row.alt020b25
                wand_alt025b30 	=row.alt025b30
                wand_alt030b35 	=row.alt030b35
                wand_alt035b40 	=row.alt035b40
                wand_alt040b45 	=row.alt040b45
                wand_alt045b50 	=row.alt045b50
                wand_alt050b55 	=row.alt050b55
                wand_alt055b60 	=row.alt055b60
                wand_alt060b65 	=row.alt060b65
                wand_alt065b75 	=row.alt065b75
                wand_alt075um 	=row.alt075um
            del wanderung

            for row in bevoelkerung:
                bev_alt000b03 = row.alt000b03
                bev_alt003b06 =row.alt003b06
                bev_alt006b10 =row.alt006b10
                bev_alt010b15 =row.alt010b15
                bev_alt015b18 =row.alt015b18
                bev_alt018b20 =row.alt018b20
                bev_alt020b25 =row.alt020b25
                bev_alt025b30 =row.alt025b30
                bev_alt030b35 =row.alt030b35
                bev_alt035b40 =row.alt035b40
                bev_alt040b45 =row.alt040b45
                bev_alt045b50 =row.alt045b50
                bev_alt050b55 =row.alt050b55
                bev_alt055b60 =row.alt055b60
                bev_alt060b65 =row.alt060b65
                bev_alt065b75 =row.alt065b75
                bev_alt075um =row.alt075um
            del bevoelkerung

            #Wanderungsrate berechnen
            rate_alt000b03 = wand_alt000b03/bev_alt000b03*100
            rate_alt003b06 	=	wand_alt003b06 	/	bev_alt003b06 	*100
            rate_alt006b10 	=	wand_alt006b10 	/	bev_alt006b10 	*100
            rate_alt010b15 	=	wand_alt010b15 	/	bev_alt010b15 	*100
            rate_alt015b18 	=	wand_alt015b18 	/	bev_alt015b18 	*100
            rate_alt018b20 	=	wand_alt018b20 	/	bev_alt018b20 	*100
            rate_alt020b25 	=	wand_alt020b25 	/	bev_alt020b25 	*100
            rate_alt025b30 	=	wand_alt025b30 	/	bev_alt025b30 	*100
            rate_alt030b35 	=	wand_alt030b35 	/	bev_alt030b35 	*100
            rate_alt035b40 	=	wand_alt035b40 	/	bev_alt035b40 	*100
            rate_alt040b45 	=	wand_alt040b45 	/	bev_alt040b45 	*100
            rate_alt045b50 	=	wand_alt045b50 	/	bev_alt045b50 	*100
            rate_alt050b55 	=	wand_alt050b55 	/	bev_alt050b55 	*100
            rate_alt055b60 	=	wand_alt055b60 	/	bev_alt055b60 	*100
            rate_alt060b65 	=	wand_alt060b65 	/	bev_alt060b65 	*100
            rate_alt065b75 	=	wand_alt065b75 	/	bev_alt065b75 	*100
            rate_alt075um 	=	wand_alt075um 	/	bev_alt075um 	*100
            #Rate fuer dieses Jahr in dem Dictionary ablegen
            wanderungsraten_dict.update({iteratorjahr : [rate_alt000b03 ,rate_alt003b06 ,rate_alt006b10 ,rate_alt010b15 ,rate_alt015b18 ,rate_alt018b20 ,rate_alt020b25 ,rate_alt025b30 ,rate_alt030b35 ,rate_alt035b40 ,rate_alt040b45 ,rate_alt045b50 ,rate_alt050b55 ,rate_alt055b60 ,rate_alt060b65 ,rate_alt065b75 ,rate_alt075um]})

            iteratorjahr+=1

        array1 = wanderungsraten_dict[int(jahr)]
        array2 = wanderungsraten_dict[int(jahr)-1]
        array3 = wanderungsraten_dict[int(jahr)-2]
        array4 = wanderungsraten_dict[int(jahr)-3]


        print array1
        print array2
        print array3
        print array4

        wanderungsraten_gemittelt = []
        i = 0
        while (i <= 16):

            rate = (array1[i]+array2[i]+array3[i]+array4[i]) / 4
            wanderungsraten_gemittelt.append(rate)
            i +=1
        print wanderungsraten_gemittelt
        #wanderungsraten in die tabelle eintragen
        wanderungsratenTabelle = arcpy.InsertCursor(wanderungsraten_gemeinde_pfad)
        row = wanderungsratenTabelle.newRow()
        row.alt000b03=wanderungsraten_gemittelt[0]
        row.alt003b06=wanderungsraten_gemittelt[1]
        row.alt006b10=wanderungsraten_gemittelt[2]
        row.alt010b15=wanderungsraten_gemittelt[3]
        row.alt015b18=wanderungsraten_gemittelt[4]
        row.alt018b20=wanderungsraten_gemittelt[5]
        row.alt020b25=wanderungsraten_gemittelt[6]
        row.alt025b30=wanderungsraten_gemittelt[7]
        row.alt030b35=wanderungsraten_gemittelt[8]
        row.alt035b40=wanderungsraten_gemittelt[9]
        row.alt040b45=wanderungsraten_gemittelt[10]
        row.alt045b50=wanderungsraten_gemittelt[11]
        row.alt050b55=wanderungsraten_gemittelt[12]
        row.alt055b60=wanderungsraten_gemittelt[13]
        row.alt060b65=wanderungsraten_gemittelt[14]
        row.alt065b75=wanderungsraten_gemittelt[15]
        row.alt075um=wanderungsraten_gemittelt[16]
        row.ags = ags
        row.geschlecht = geschlecht
        wanderungsratenTabelle.insertRow(row)

        del wanderungsratenTabelle


def bevoelkerungsprognose(projektname, ags, jahr, geschlecht):
    import arcpy, sys,os
    #api endpunkt fuer die Tabelle "Fortschreibung des Bevoelkerungsstandes"
    #(http://regenesis.pudo.org/regional/statistics/fortschreibung-des-bevolkerungsstandes.12411.html)
    # Variablen definieren
    #Pfade einrichten
    base_path = str(sys.path[0]).split("2_Tool")[0]
    workspace_projekt_definition = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
    workspace_projekt_bevoelkerung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_22_BevModellierung_'+projektname+'.gdb')
    workspace_tool_bevoelkerung = os.path.join(base_path,"2_Tool","22_Bevoelkerungsmodellierung","FGDB_22_Bevoelkerungsmodellierung_Tool.gdb")
    bevoelkerung_gemeinde_pfad = os.path.join(workspace_projekt_bevoelkerung, "bevoelkerung")
    bevoelkerung_gemeinde_grob_pfad = os.path.join(workspace_projekt_bevoelkerung, "bevoelkerung_altersgruppen")
    wanderung_gemeinde_pfad = os.path.join(workspace_projekt_bevoelkerung, "wanderung_altersgruppen")
    wanderung_gemeinde_fein_pfad = os.path.join(workspace_projekt_bevoelkerung, "wanderung")
    wanderungsraten_gemeinde_pfad = os.path.join(workspace_projekt_bevoelkerung, "wanderungsraten")
    raten_pfad = os.path.join(workspace_tool_bevoelkerung,"raten")
    prognose_pfad = os.path.join(workspace_projekt_bevoelkerung, "bevoelkerung_prognose")

    raten_pfad = os.path.join(workspace_tool_bevoelkerung,"raten")
    #Laden der Mortalitaets- und Fertilitaetsraten
    where_clause_fertilitaet = '"geschlecht" = ' + "'" + geschlecht + "'"+' AND "typ" =' +" '"+"fertilitaet'"
    where_clause_mortalitaet = '"geschlecht" = ' + "'" + geschlecht + "'"+' AND "typ" =' +" '"+"mortalitaet'"
    fertilitaetsratenArray = []
    mortalitaetsratenArray = []
    fertilitaetsraten = arcpy.SearchCursor(raten_pfad,where_clause_fertilitaet)
    mortalitaetsraten = arcpy.SearchCursor(raten_pfad,where_clause_mortalitaet)
    #Bevölkerungsdaten
    bevoelkerungArray = []
    where_clause = '"jahr" = ' + str(jahr) + " AND " + '"geschlecht" = ' + "'" + geschlecht + "' AND "+'"ags" = '+ "'" + str(ags) + "'"
    bevoelkerung = arcpy.SearchCursor(bevoelkerung_gemeinde_pfad, where_clause)
    #Wanderungsraten
    wanderungArray = []
    where_clause_wanderung = '"geschlecht" = ' + "'" + geschlecht + "' AND "+'"ags" = '+ "'" + str(ags) + "'"
    wanderungsraten = arcpy.SearchCursor(wanderungsraten_gemeinde_pfad, where_clause_wanderung)

    #Auslesen der Daten
    for row in fertilitaetsraten:
        #print "Fertilitaet"
        alt000b03=row.alt000b03
        alt003b06=row.alt003b06
        alt006b10=row.alt006b10
        alt010b15=row.alt010b15
        alt015b18=row.alt015b18
        alt018b20=row.alt018b20
        alt020b25=row.alt020b25
        alt025b30=row.alt025b30
        alt030b35=row.alt030b35
        alt035b40=row.alt035b40
        alt040b45=row.alt040b45
        alt045b50=row.alt045b50
        alt050b55=row.alt050b55
        alt055b60=row.alt055b60
        alt060b65=row.alt060b65
        alt065b75=row.alt065b75
        alt075um=row.alt075um

        del row
    fertilitaetsratenArray = [alt000b03,alt003b06,alt006b10,alt010b15,alt015b18,alt018b20,alt020b25,alt025b30,alt030b35,alt035b40,alt040b45,alt045b50,alt050b55,alt055b60,alt060b65,alt065b75,alt075um ]

    for row in mortalitaetsraten:
        #print "Mortalitaet"
        alt000b03=row.alt000b03
        alt003b06=row.alt003b06
        alt006b10=row.alt006b10
        alt010b15=row.alt010b15
        alt015b18=row.alt015b18
        alt018b20=row.alt018b20
        alt020b25=row.alt020b25
        alt025b30=row.alt025b30
        alt030b35=row.alt030b35
        alt035b40=row.alt035b40
        alt040b45=row.alt040b45
        alt045b50=row.alt045b50
        alt050b55=row.alt050b55
        alt055b60=row.alt055b60
        alt060b65=row.alt060b65
        alt065b75=row.alt065b75
        alt075um=row.alt075um

        del row
    mortalitaetsratenArray = [alt000b03,alt003b06,alt006b10,alt010b15,alt015b18,alt018b20,alt020b25,alt025b30,alt030b35,alt035b40,alt040b45,alt045b50,alt050b55,alt055b60,alt060b65,alt065b75,alt075um ]



    for row in bevoelkerung:
        #print "Bevölkerung"
        alt000b03=row.alt000b03
        alt003b06=row.alt003b06
        alt006b10=row.alt006b10
        alt010b15=row.alt010b15
        alt015b18=row.alt015b18
        alt018b20=row.alt018b20
        alt020b25=row.alt020b25
        alt025b30=row.alt025b30
        alt030b35=row.alt030b35
        alt035b40=row.alt035b40
        alt040b45=row.alt040b45
        alt045b50=row.alt045b50
        alt050b55=row.alt050b55
        alt055b60=row.alt055b60
        alt060b65=row.alt060b65
        alt065b75=row.alt065b75
        alt075um=row.alt075um

        del row
    bevoelkerungArray = [alt000b03,alt003b06,alt006b10,alt010b15,alt015b18,alt018b20,alt020b25,alt025b30,alt030b35,alt035b40,alt040b45,alt045b50,alt050b55,alt055b60,alt060b65,alt065b75,alt075um ]


    for row in wanderungsraten:
        #print "Wanderung"
        alt000b03=row.alt000b03
        alt003b06=row.alt003b06
        alt006b10=row.alt006b10
        alt010b15=row.alt010b15
        alt015b18=row.alt015b18
        alt018b20=row.alt018b20
        alt020b25=row.alt020b25
        alt025b30=row.alt025b30
        alt030b35=row.alt030b35
        alt035b40=row.alt035b40
        alt040b45=row.alt040b45
        alt045b50=row.alt045b50
        alt050b55=row.alt050b55
        alt055b60=row.alt055b60
        alt060b65=row.alt060b65
        alt065b75=row.alt065b75
        alt075um=row.alt075um

        del row
    wanderungArray = [alt000b03,alt003b06,alt006b10,alt010b15,alt015b18,alt018b20,alt020b25,alt025b30,alt030b35,alt035b40,alt040b45,alt045b50,alt050b55,alt055b60,alt060b65,alt065b75,alt075um ]

    del fertilitaetsraten,mortalitaetsraten,bevoelkerung,wanderungsraten

    #Bevölkerungsmodellierung Schritt eins: Wanderungsraten
    a = []
    i = 0
    while i <= 16:
        b = bevoelkerungArray[i] + (bevoelkerungArray[i]*wanderungArray[i]/100)
        #b = round(b,0)
        a.append(b)
        i+=1
    #print a

    #Bevölkerungsmodellierung Schritt 2: Mortalitaetsraten
    #print mortalitaetsratenArray
    c = []
    i = 0
    while i <= 16:
        d = a[i] - (a[i]*mortalitaetsratenArray[i]/100)
        #d = round(d,0)
        d = d
        c.append(d)
        i += 1
    #print c
    #ergebnis für männliche Berechnung speichern, nach der Berechnung der Geburtszahlen werdne 50% der Geburten auf die kleinste Altersgruppe der Männlichen Bevölkerung
    #aufgeschlagen
    #if (geschlecht == 'gesm'):
    #    ergebnisCursorGesm = arcpy.InsertCursor(bevoelkerung_gemeinde_pfad)
    #    row = ergebnisCursorGesm.newRow()
    #    row.alt000b03 = c[0]
    #    row.alt003b06 = c[1]
    #    row.alt006b10 = c[2]
    #    row.alt010b15 = c[3]
    #    row.alt015b18 = c[4]
    #    row.alt018b20 = c[5]
    #    row.alt020b25 = c[6]
    #    row.alt025b30 = c[7]
    #    row.alt030b35 = c[8]
    #    row.alt035b40 = c[9]
    #    row.alt040b45 = c[10]
    #    row.alt045b50 = c[11]
    #    row.alt050b55 = c[12]
    #    row.alt055b60 = c[13]
    #    row.alt060b65 = c[14]
    #    row.alt065b75 = c[15]
    #    row.alt075um = c[16]
    #    row.geschlecht = geschlecht
    #    row.ags = ags
    #    row.jahr = int(jahr) +1
    #    ergebnisCursorGesm.insertRow(row)
    #    del row, ergebnisCursorGesm

    #Bevölkerungsmodellierung Schritt 3: Fertilitätsraten
    #print geschlecht

    #print "drin"
    e = []
    i = 0
    g = 0
    while i<= 16:
        f = (c[i] * fertilitaetsratenArray[i]/100)
        e.append(f)
        #print fertilitaetsratenArray[i]
        #Die Geburten jeder Altersklasse insgesamt aufsummieren
        g = g + f
        i = i+1

        #h= kleinste altersgruppe + die Geburten
        #die andere Hälfte am Ende direkt in das Männliche Ergebnis rein schreiben
    h = c[0] + g
    #print h
    ergebnisCursorGesw = arcpy.InsertCursor(bevoelkerung_gemeinde_pfad)
    row = ergebnisCursorGesw.newRow()
    row.alt000b03 = h
    row.alt003b06 = c[1]
    row.alt006b10 = c[2]
    row.alt010b15 = c[3]
    row.alt015b18 = c[4]
    row.alt018b20 = c[5]
    row.alt020b25 = c[6]
    row.alt025b30 = c[7]
    row.alt030b35 = c[8]
    row.alt035b40 = c[9]
    row.alt040b45 = c[10]
    row.alt045b50 = c[11]
    row.alt050b55 = c[12]
    row.alt055b60 = c[13]
    row.alt060b65 = c[14]
    row.alt065b75 = c[15]
    row.alt075um = c[16]
    row.geschlecht = geschlecht
    row.ags = ags
    row.jahr = int(jahr) +1
    ergebnisCursorGesw.insertRow(row)
    del row, ergebnisCursorGesw
        ##50% der Geburten auf die kleinste Klasse der männlichen Prognose aufschlagen
        #where_clause_update =  '"jahr" = ' + str(int(jahr)+1) + " AND " + '"geschlecht" = ' + "'gesm' AND "+'"ags" = '+ "'" + str(ags) + "'"
        #updateCursor = arcpy.UpdateCursor( bevoelkerung_gemeinde_pfad,where_clause_update )
        #for row in updateCursor:
        #    row.alt000b03 = row.alt000b03 + (g/2)
        #    updateCursor.updateRow(row)
        #try:
        #    del updateCursor, row
        #except:
        #    print ""

def prognoseEinrechnen(projektname,ags, geschlecht, jahr ):
    import sys, arcpy, os


    base_path = str(sys.path[0]).split("2_Tool")[0]
    projektGDBPfad = os.path.join(base_path,'3_Projekte',projektname,'FGDB_11_Definition_Projekt_'+projektname+'.gdb')
    workspace_projekt_bevoelkerung = os.path.join(base_path,'3_Projekte',projektname,'FGDB_22_BevModellierung_'+projektname+'.gdb')
    bevoelkerung_gemeinde_pfad = os.path.join(workspace_projekt_bevoelkerung, "bevoelkerung")
    saldo_projekt_pfad = os.path.join(workspace_projekt_bevoelkerung,"saldo")
    prognose_pfad = os.path.join(projektGDBPfad,"RegionPrognose_gesamt")
    where_clause = '"jahr" = ' + str(jahr) + " AND " + '"geschlecht" = ' + "'" + geschlecht + "' AND "+'"ags" = '+ "'" + str(ags) + "'"

    bevoelkerung_Cursor = arcpy.UpdateCursor(bevoelkerung_gemeinde_pfad,where_clause)
    #saldo_Cursor = arcpy.SearchCursor(saldo_projekt_pfad,where_clause)
    ##Hinzuzuaddierende Salden extrahieren
    #for row in saldo_Cursor:
    #    alt000b03=row.alt000b03
    #    alt003b06=row.alt003b06
    #    alt006b10=row.alt006b10
    #    alt010b15=row.alt010b15
    #    alt015b18=row.alt015b18
    #    alt018b20=row.alt018b20
    #    alt020b25=row.alt020b25
    #    alt025b30=row.alt025b30
    #    alt030b35=row.alt030b35
    #    alt035b40=row.alt035b40
    #    alt040b45=row.alt040b45
    #    alt045b50=row.alt045b50
    #    alt050b55=row.alt050b55
    #    alt055b60=row.alt055b60
    #    alt060b65=row.alt060b65
    #    alt065b75=row.alt065b75
    #    alt075um=row.alt075um
    #
    #salden = [alt000b03,alt003b06,alt006b10,alt010b15,alt015b18,alt018b20,alt020b25,alt025b30,alt030b35,alt035b40,alt040b45,alt045b50,alt050b55,alt055b60,alt060b65,alt065b75,alt075um]
    ##print salden
    #del row, saldo_Cursor
    ##Salden hinzufuegen
    #for row in bevoelkerung_Cursor:
    #    row.setValue("alt000b03",row.getValue("alt000b03") + salden[0])
    #    row.setValue("alt003b06",row.getValue("alt003b06") + salden[1])
    #    row.setValue("alt006b10",row.getValue("alt006b10") + salden[2])
    #    row.setValue("alt010b15",row.getValue("alt010b15") + salden[3])
    #    row.setValue("alt015b18",row.getValue("alt015b18") + salden[4])
    #    row.setValue("alt018b20",row.getValue("alt018b20") + salden[5])
    #    row.setValue("alt020b25",row.getValue("alt020b25") + salden[6])
    #    row.setValue("alt025b30",row.getValue("alt025b30") + salden[7])
    #    row.setValue("alt030b35",row.getValue("alt030b35") + salden[8])
    #    row.setValue("alt035b40",row.getValue("alt035b40") + salden[9])
    #    row.setValue("alt040b45",row.getValue("alt040b45") + salden[10])
    #    row.setValue("alt045b50",row.getValue("alt045b50") + salden[11])
    #    row.setValue("alt050b55",row.getValue("alt050b55") + salden[12])
    #    row.setValue("alt055b60",row.getValue("alt055b60") + salden[13])
    #    row.setValue("alt060b65",row.getValue("alt060b65") + salden[14])
    #    row.setValue("alt065b75",row.getValue("alt065b75") + salden[15])
    #    row.setValue("alt075um",row.getValue("alt075um") + salden[16])
    #    bevoelkerung_Cursor.updateRow(row)
    #Berechnete Bevoelkerungszahlen in einen Array zum Abgleich mit den Zahlen der Prognose schreiben
    for row in bevoelkerung_Cursor:
        Berechnung_alt000b03 = row.getValue("alt000b03")
        Berechnung_alt003b06 = row.getValue("alt003b06")
        Berechnung_alt006b10 = row.getValue("alt006b10")
        Berechnung_alt010b15 = row.getValue("alt010b15")
        Berechnung_alt015b18 = row.getValue("alt015b18")
        Berechnung_alt018b20 = row.getValue("alt018b20")
        Berechnung_alt020b25 = row.getValue("alt020b25")
        Berechnung_alt025b30 = row.getValue("alt025b30")
        Berechnung_alt030b35 = row.getValue("alt030b35")
        Berechnung_alt035b40 = row.getValue("alt035b40")
        Berechnung_alt040b45 = row.getValue("alt040b45")
        Berechnung_alt045b50 = row.getValue("alt045b50")
        Berechnung_alt050b55 = row.getValue("alt050b55")
        Berechnung_alt055b60 = row.getValue("alt055b60")
        Berechnung_alt060b65 = row.getValue("alt060b65")
        Berechnung_alt065b75 = row.getValue("alt065b75")
        Berechnung_alt075um = row.getValue("alt075um")

    berechnung = [Berechnung_alt000b03,Berechnung_alt003b06,Berechnung_alt006b10,Berechnung_alt010b15,Berechnung_alt015b18,Berechnung_alt018b20,Berechnung_alt020b25,Berechnung_alt025b30,Berechnung_alt030b35,Berechnung_alt035b40,Berechnung_alt040b45,Berechnung_alt045b50,Berechnung_alt050b55,Berechnung_alt055b60,Berechnung_alt060b65,Berechnung_alt065b75,Berechnung_alt075um]


#Prognosedaten extrahieren
    if jahr < 2012:
        jahr = 2012
    if jahr > 2048:
        jahr = 2048
    where_clause = '"jahr" = ' + str(jahr) + " AND " + '"geschlecht" = ' + "'" + geschlecht + "'"
    prognose_Cursor = arcpy.SearchCursor(prognose_pfad,where_clause)
    #Werte der Bevoelkerungsprognose extrahieren
    for row1 in prognose_Cursor:
        Prognose_alt000b03=row1.alt000b03
        Prognose_alt003b06=row1.alt003b06
        Prognose_alt006b10=row1.alt006b10
        Prognose_alt010b15=row1.alt010b15
        Prognose_alt015b18=row1.alt015b18
        Prognose_alt018b20=row1.alt018b20
        Prognose_alt020b25=row1.alt020b25
        Prognose_alt025b30=row1.alt025b30
        Prognose_alt030b35=row1.alt030b35
        Prognose_alt035b40=row1.alt035b40
        Prognose_alt040b45=row1.alt040b45
        Prognose_alt045b50=row1.alt045b50
        Prognose_alt050b55=row1.alt050b55
        Prognose_alt055b60=row1.alt055b60
        Prognose_alt060b65=row1.alt060b65
        Prognose_alt065b75=row1.alt065b75
        Prognose_alt075um=row1.alt075um

    prognose = [Prognose_alt000b03,Prognose_alt003b06,Prognose_alt006b10,Prognose_alt010b15,Prognose_alt015b18,Prognose_alt018b20,Prognose_alt020b25,Prognose_alt025b30,Prognose_alt030b35,Prognose_alt035b40,Prognose_alt040b45,Prognose_alt045b50,Prognose_alt050b55,Prognose_alt055b60,Prognose_alt060b65,Prognose_alt065b75,Prognose_alt075um]

    #Progonose und Berechnung vergleichen und die Abweichung ermitteln

    counter = 0
    while counter <= 16:
        berechnung_aktuell = berechnung[counter]
        prognose_aktuell = prognose[counter]
        #berechnung der differenz
        differenz = prognose_aktuell - berechnung_aktuell
        #Betrag der Differenz
        differenz = abs(differenz)
        #Wenn die Differenz mehr als 10% der Berechnung sind, Mittelwert aus Berechnung und Prognose erstellen
        differenz_prozent = differenz / berechnung_aktuell

        if differenz_prozent >= 0.1:
            arcpy.AddMessage("Die berechnete Bevoelkerungszahl und die Prognose unterscheiden sich um " + str(differenz_prozent*100) + " Prozent, daher wird der Mittelwert aus der Prognose ("+ str(prognose_aktuell) + ") und der Berechnung ("+ str(berechnung_aktuell)+") gebildet.")
            mittelwert_aktuell = (prognose_aktuell + berechnung_aktuell) / 2
            arcpy.AddMessage("Ermittelter Wert: " + str(mittelwert_aktuell))
            if counter == 0:
                row.setValue("alt000b03",mittelwert_aktuell)
            if counter == 1:
                row.setValue("alt003b06",mittelwert_aktuell)
            if counter == 2:
                row.setValue("alt006b10",mittelwert_aktuell)
            if counter == 3:
                row.setValue("alt010b15",mittelwert_aktuell)
            if counter == 4:
                row.setValue("alt015b18",mittelwert_aktuell)
            if counter == 5:
                row.setValue("alt018b20",mittelwert_aktuell)
            if counter == 6:
                row.setValue("alt020b25",mittelwert_aktuell)
            if counter == 7:
                row.setValue("alt025b30",mittelwert_aktuell)
            if counter == 8:
                row.setValue("alt030b35",mittelwert_aktuell)
            if counter == 9:
                row.setValue("alt035b40",mittelwert_aktuell)
            if counter == 10:
                row.setValue("alt040b45",mittelwert_aktuell)
            if counter == 11:
                row.setValue("alt045b50",mittelwert_aktuell)
            if counter == 12:
                row.setValue("alt050b55",mittelwert_aktuell)
            if counter == 13:
                row.setValue("alt055b60",mittelwert_aktuell)
            if counter == 14:
                row.setValue("alt060b65",mittelwert_aktuell)
            if counter == 15:
                row.setValue("alt065b75",mittelwert_aktuell)
            if counter == 16:
                row.setValue("alt075um",mittelwert_aktuell)
            bevoelkerung_Cursor.updateRow(row)
        counter += 1
    del row, bevoelkerung_Cursor,











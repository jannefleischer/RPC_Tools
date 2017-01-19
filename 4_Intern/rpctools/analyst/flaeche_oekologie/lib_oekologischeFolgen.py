# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# REGIOPROJEKTCHECK
# lib_oekologischeFolgen.py
#
# Description:
# PROJECT URL: http://www.regioprojektcheck.de
#
# Author:
# ILS gGmbH
#
# LICENSE: The MIT License (MIT) Copyright (c) 2014 RPC Consortium
# ---------------------------------------------------------------------------

import arcpy, os, datetime, sys, gc

def oekologischeFolgen(bedeckungNullfall, bedeckungPlanfall):
    try:
        arcpy.AddMessage("================================")
        print("================================")
        arcpy.AddMessage("Oekologische Bewertung berechnen:")
        print("Oekologische Bewertung berechnen:")
        #bedeckungNullfall / bedeckungPLanfall: Eine PythonListe, welche die Bodenbedeckung in ha für die folgenden Kategorien angibt
        #liste = [überbaute Flächen, Asphalt/Beton, Platten, Kleinpflaster, Wassergebundene Decke/Rasengittersteine, Offener Boden/ Acker, Rasen, Bäume/Sträucher,Stauden,Wiese,Natürliche Wasserfläche]
    #####################################################################################################################
        ##Anteile der Bodenbedeckung berechnen
        #Gesammtsumme für Nullfall und Planfall berechnen
        x=0
        for typ in bedeckungNullfall:
            x = x+typ
    ##    print x

        y=0
        for typ in bedeckungPlanfall:
            y = y+typ
    ##    print y

        #Anteile der Bodenbedeckung berechnen
        anteileNullfall = []
        for typ in bedeckungNullfall:
            z = typ/x
            z = round(z,1)
            anteileNullfall.append(z)
    ##    print anteileNullfall

        anteilePlanfall = []
        for typ in bedeckungPlanfall:
            u = typ/y
            u = round(u,1)
            anteilePlanfall.append(u)
    ##    print anteilePlanfall
    #####################################################################################################################
        ##ökologische Flächenleistungsparameter
        #Keys:
        #Überbaute Fläche = uF
        #Asphalt / Beton = A
        #Platten = P
        #Kleinpflaster = kP
        #wassergeb. Decke / Rasengittersteine = wD
        #offener Boden / Acker = oB
        #Rasen =R
        #Bäume / Sträucher = B
        #Stauden = ST
        #Wiese = W
        #natürliche Wasserflächen = nW

        #Klima - Wärmespeicherung
        WS = [0,0,0.1,0.2,0.3,0.3,1,0.8,0.9,1,1]
        #Klima - Staubbindevermögen
        SB = [0,0,0,0.1,0.1,0.1,0.2,0.8,0.4,0.4,1]
        #Boden - Schadstoffrückhaltung
        SR = [0,0,0.2,0.3,0.4,0.5,0.8,0.8,0.8,0.8,0]
        #Boden  - Porosität und Durchlässigkeit
        PD = [0,0.1,0.2,0.4,0.6,1,0.8,1,1,1,1]
        #Boden - Antropogene Bodenüberformung
        AB = [0,0,0,0,0,0.8,0.8,0.8,0.8,1,1]
        #Wasser - Oberflächenabfluss
        OA = [0,0.1,0.4,0.7,0.6,1,0.8,1,1,1,0]
        #Wasser - Grundwasserneubildung
        GN = [0,0,0.3,0.5,0.8,1,0.5,0.4,0.5,0.5,1]
        #Wasser - Regenwasserversickerung
        RV = [0,0.1,0.4,0.5,0.5,1,0.8,0.9,0.9,1,1]
        #FloraFauna - Biotopausbildungsvermögen
        BV = [0.1,0.1,0.2,0.3,0.4,0.5,0.6,0.9,0.9,1,1]

    #####################################################################################################################
    ##Ökologische Flächenleistungen
    #Ökowert Nullfall
        it = 0
        varWS = 0
        varSB = 0
        varSR = 0
        varPD = 0
        varAB = 0
        varOA = 0
        varGN = 0
        varRV = 0
        varBV = 0
        for anteil in anteileNullfall:

            a=anteil * WS[it]
            varWS = varWS + a

            b = anteil * SB[it]
            varSB = varSB + b

            c = anteil * SR[it]
            varSR = varSR + c

            d = anteil * PD[it]
            varPD = varPD + d

            e = anteil * AB[it]
            varAB = varAB + e

            f = anteil * OA[it]
            varOA = varOA + f

            g = anteil * GN[it]
            varGN = varGN + g

            h = anteil * RV[it]
            varRV = varRV + h

            i = anteil * BV[it]
            varBV = varBV + i

            it = it+1
    ##    print varWS
    ##    print varSB
    ##    print varSR
    ##    print varPD
    ##    print varAB
    ##    print varOA
    ##    print varGN
    ##    print varRV
    ##    print varBV

        oekowertNullfall = round(((varWS + varSB + varSR + varPD + varAB + varOA + varGN + varRV + varBV) / 9),2)
    #ÖkowertPlanfall
        it = 0
        varWS = 0
        varSB = 0
        varSR = 0
        varPD = 0
        varAB = 0
        varOA = 0
        varGN = 0
        varRV = 0
        varBV = 0
        for anteil in anteilePlanfall:

            a=anteil * WS[it]
            varWS = varWS + a

            b = anteil * SB[it]
            varSB = varSB + b

            c = anteil * SR[it]
            varSR = varSR + c

            d = anteil * PD[it]
            varPD = varPD + d

            e = anteil * AB[it]
            varAB = varAB + e

            f = anteil * OA[it]
            varOA = varOA + f

            g = anteil * GN[it]
            varGN = varGN + g

            h = anteil * RV[it]
            varRV = varRV + h

            i = anteil * BV[it]
            varBV = varBV + i

            it = it+1
    ##    print varWS
    ##    print varSB
    ##    print varSR
    ##    print varPD
    ##    print varAB
    ##    print varOA
    ##    print varGN
    ##    print varRV
    ##    print varBV

        oekowertPlanfall = round(((varWS + varSB + varSR + varPD + varAB + varOA + varGN + varRV + varBV) / 9),2)
        if(oekowertNullfall<0.2):
            punktwertNullfall = 1
        elif(oekowertNullfall>=0.2 and oekowertNullfall<0.4):
            punktwertNullfall = 2
        elif(oekowertNullfall>=0.4 and oekowertNullfall<0.6):
            punktwertNullfall = 3
        elif(oekowertNullfall >= 0.6 and oekowertNullfall<0.8):
            punktwertNullfall = 4
        elif(oekowertNullfall>=0.8):
            punktwertNullfall = 5
        else:
            punktwertNullfall = 0
        punktwertNullfallText = "Punktwert Nullfall=" + str(punktwertNullfall)
        arcpy.AddMessage(punktwertNullfallText)
        print (punktwertNullfallText)

        if(oekowertPlanfall<0.2):
            punktwertPlanfall = 1
        elif(oekowertPlanfall>=0.2 and oekowertPlanfall<0.4):
            punktwertPlanfall = 2
        elif(oekowertPlanfall>=0.4 and oekowertPlanfall<0.6):
            punktwertPlanfall = 3
        elif(oekowertPlanfall >= 0.6 and oekowertPlanfall<0.8):
            punktwertPlanfall = 4
        elif(oekowertPlanfall>=0.8):
            punktwertPlanfall = 5
        else:
            punktwertPlanfall = 0
        punktwertPlanfallText = "Punktwert Planfall=" + str(punktwertPlanfall)
        arcpy.AddMessage(punktwertPlanfallText)
        print (punktwertPlanfallText)
    #entsprechende Ergebnisse müssen via return zurück gegeben werden
        return [punktwertNullfallText,punktwertPlanfallText]
    except Exception as e:
        return e

def oekologischeWertigkeit(projektName):
    ##In diesem Modul wir überprüft, ob die Planfläche sich mit verschiedenen, schützenswerten Naturgebieten überschneidet
    try:
        arcpy.AddMessage("========================")
        arcpy.AddMessage("Raeumliche Ueberschneidungen")
        print("========================")
        print("Raeumliche Ueberschneidungen:")
        #aktuelle Zeit
        time = datetime.datetime.now()

        timestamp = str(time.hour) + ":" + str(time.minute) + ":" + str(time.second) + "-" + str(time.day) + "/" + str(time.month) + "/" + str(time.year)

        #aktueller Pfad
        #wcd = sys.path[0].split("\\2_Tool")[0]
        wcd = str(sys.path[0]).split("2_Tool")[0]
        #wcd = sys.path[0]
        #arcpy.AddMessage(wcd)

        #wcd = os.getcwd()
        rootPfad = wcd
        #rootPfad = rootPfad + "\\00_Entwicklungsumgebung"
        #Pfad zur Ergebnistabelle

##        ergebnisTabelle = rootPfad + "\\3_Projekte\\" + projektName + "\\FGDB_36_Flaeche_und_Oekologie_Projekt_" + projektName + ".gdb\\Ergebnisse_oekologischeWertigkeit"
##        #insert Cursor für die Ergebnistabelle erstellen
##        ergebnisCursor = arcpy.InsertCursor(ergebnisTabelle)
##        #eine neue Zeile für das Ergebnis dieses Durchlaufs anlegen
##        ergebnisZeile = ergebnisCursor.newRow()
        #Die Flächen des Plangebietes als Layer verfügbar machen

        flaechenPlangebiet = os.path.join(rootPfad,"3_Projekte",projektName,"FGDB_Definition_Projekt_"+projektName+ ".gdb","Teilflaechen_Plangebiet")
        arcpy.MakeFeatureLayer_management(flaechenPlangebiet,"flaechenPlangebiet_lyr")
        #Aus der Featureclass eine Liste mit allen Schutzgebieten iterieren
        arcpy.env.workspace = os.path.join(rootPfad,"2_Tool","F_Flaeche_und_Oekologie","FGDB_Flaeche_und_Oekologie_Tool.gdb","NRW")
        #print arcpy.env.workspace
        #arcpy.AddMessage(arcpy.env.workspace)
        liste = arcpy.ListFeatureClasses()
        #arcpy.AddMessage(liste)
        #Printausgabe
        #über diese Liste iterieren und auf Überschneidungen mit dem Plangebiet prüfen
        rueckgabe = []
        #print liste
        for gebiet in liste:
            #Layer erstellen
            arcpy.MakeFeatureLayer_management(gebiet,"schutzgebiet_lyr")
            #Alle Flächen des BiotopeLayers auswählen, die sich mit den Plangebietsflächen überschneiden
            arcpy.SelectLayerByLocation_management("schutzgebiet_lyr", "INTERSECT", "flaechenPlangebiet_lyr")
            #das Ergebnis durchzählen, wenn x>0 gibt es Überschneidungen, ansonsten keine
            rows = arcpy.SearchCursor("schutzgebiet_lyr")
            x = 0
            for row in rows:
                x = x+1
            #Printausgabe
            arcpy.AddMessage(gebiet + ":"+str(x))
            print(gebiet + ":"+str(x))
            #In der Ergebnistabelle  wert für das spezifische Schutzgebiet auf '1' stellen
##            if(x>0):
##                if(gebiet == "Biotope"):
##                    ergebnisZeile.Biotope = 1
##                if(gebiet == "FFH_Gebiete"):
##                    ergebnisZeile.FFH_Gebiete = 1
##                if(gebiet == "Nationalparke"):
##                    ergebnisZeile.Nationalparke = 1
##                if(gebiet == "Naturschutzgebiete"):
##                    ergebnisZeile.Naturschutzgebiete = 1
##                if(gebiet == "Vogelschutzgebiete"):
##                    ergebnisZeile.Vogelschutzgebiete = 1
##
##            else:
##                if(gebiet == "Biotope"):
##                    ergebnisZeile.Biotope = 0
##                if(gebiet == "FFH_Gebiete"):
##                    ergebnisZeile.FFH_Gebiete = 0
##                if(gebiet == "Nationalparke"):
##                    ergebnisZeile.Nationalparke = 0
##                if(gebiet == "Naturschutzgebiete"):
##                    ergebnisZeile.Naturschutzgebiete = 0
##                if(gebiet == "Vogelschutzgebiete"):
##                    ergebnisZeile.Vogelschutzgebiete = 0
            y = gebiet + "="+str(x)
            y = y.encode("utf-8")
            rueckgabe.append(y)

            arcpy.Delete_management("schutzgebiet_lyr")
##        ergebnisZeile.timestamp = timestamp
##        ergebnisCursor.insertRow(ergebnisZeile)
        #eine 1 steht inder Ergebnistabelle für Überschneidungen, eine 0 für keine Überschneidungen

        try:
            del liste, gebiet, #ergebnisCursor
        except:
            print("Sperren löschen fehlgeschlagen, bitte Programm neu starten")
        return rueckgabe
    except Exception as e:
        arcpy.AddMessage(e)
        #rueckgabe = (e)
        #return rueckgabe
        try:
            del liste, gebiet,# ergebnisCursor
        except:
            print("")


def IntegrationsGrad(GrenzeSiedlungskoerper,GrenzeGesamt):
    #Länge der Grenze der Projektfläche zum bestehenden Siedlungskörper (in m)
    #Länge der gesamten Grenze der Projektfläche (Umfang) (in m)
    integrationsgrad = float(GrenzeSiedlungskoerper)/float(GrenzeGesamt)
    #arcpy.AddMessage(integrationsgrad)
    if integrationsgrad < 0.25:
        bewertung = 1
    elif integrationsgrad < 0.5:
        bewertung = 2
    elif integrationsgrad < 0.75:
        bewertung = 3
    elif integrationsgrad < 1:
        bewertung = 4
    elif integrationsgrad >= 1:
        bewertung = 5
    else:
        bewertung = 0
    bewertungIntegration = bewertung
    return [integrationsgrad,bewertung]

def uzvr(projektName, Region):
    arcpy.AddMessage("========================")
    arcpy.AddMessage("Unzerschnittene verkehrsarme Raeume: Nullfall\n")
    print("========================")
    print("Unzerschnittene verkehrsarme Raeume: Nullfall\n")
    try:
        #Pfad zu den Geodaten
         #aktueller Pfad
        #arcpy.AddMessage(sys.path[0])
        wcd = sys.path[0].split("\\2_Tool")[0]
        #arcpy.AddMessage(wcd)
        #Pfad zur Ergebnistabelle
        projektOrdner = os.path.join(wcd,"3_Projekte",projektName,"FGDB_Flaeche_und_Oekologie_Projekt_" + projektName +".gdb")
        #arcpy.AddMessage(projektOrdner)
        #ergebnisTabelle = rootPfad + "\\3_Projekte\\" + projektName + "\\FGDB_36_Flaeche_und_Oekologie_Projekt_" + projektName + ".gdb\\Ergebnisse_oekologischeWertigkeit"
        ergebnisTabelle = os.path.join(projektOrdner,"Ergebnisse_oekologischeWertigkeit")
       # arcpy.AddMessage(ergebnisTabelle)
        #Pfad zu den Geodaten
        #projektFlaeche = rootPfad + "\\3_Projekte\\" + projektName + "\\FGDB_11_Definition_Projekt_" + projektName + ".gdb\\Teilflaechen_Plangebiet"
        projektFlaeche = os.path.join(wcd,"3_Projekte",projektName,"FGDB_Definition_Projekt_" + projektName+".gdb","Teilflaechen_Plangebiet")
        #arcpy.AddMessage(projektFlaeche)
        #Pfad zu den UZVR
        #uzvr =rootPfad + "\\2_Tool\\36_Flaeche_und_Oekologie\\FGDB_36_Flaeche_und_Oekologie_Tool.gdb\\uzvr_de"

        # uzvr = os.path.join(wcd,"3_Projekte",projektName,"FGDB_36_Flaeche_und_Oekologie_Projekt_" + projektName +".gdb","uzvr_de")
        # auskommentiert, da die uzvr jetzt zentral vorgehalten werden

        uzvr = os.path.join(wcd,"2_Tool","F_Flaeche_und_Oekologie","FGDB_Flaeche_und_Oekologie_Tool.gdb","uzvr_de")

        #arcpy.AddMessage(uzvr)
        #Nullfall
        #alle UVZR auswählen, die durch die Planfläche tangiert werden

        #1. Feature Layer aus den uzvr erstellen
        arcpy.MakeFeatureLayer_management(uzvr,"uzvr_lyr")
        #arcpy.AddMessage("2")

        #2.Spatial Select wo Planfläche uzvr_lyr intersected
        print("1. Prüfung auf Überschneidung und Auswahl der UZVR, die von dem Plangebiet geschnitten werden")
        arcpy.AddMessage("1. Prüfung auf Überschneidung und Auswahl der UZVR, die von dem Plangebiet geschnitten werden")
        arcpy.SelectLayerByLocation_management("uzvr_lyr", "INTERSECT", projektFlaeche)
        print("Anzahl der Flaechen: " + str(arcpy.GetCount_management("uzvr_lyr")) + "\n")
        arcpy.AddMessage("Anzahl der Flaechen: " + str(arcpy.GetCount_management("uzvr_lyr")) + "\n")

        #3.Feld hinzufügen & Fläche berechnen (nur wenn Überschneidung mit UZVR)
        #3a. Prüfung ob Überschneidung mit UZVR
        rows = arcpy.SearchCursor("uzvr_lyr")
        CountUZVR = 0
        for row in rows:
            CountUZVR = CountUZVR + 1
            #Printausgabe
            # arcpy.AddMessage("Geschnittene UZVR: " + CountUZVR + "\n")
            # print("Geschnittene UZVR: " + CountUZVR)

        if(CountUZVR == 0):
            bewertungUZVR = 5
            begegnungswahrscheinlichkeit = 1
            begegnungswahrscheinlichkeit_clipped = 1
            groessteUZVR = 0
            print("Keine UZVR betroffen")
            arcpy.AddMessage("Keine UZVR betroffen")
        else:
            print("2. Flaechengroesse berechnen\n")
            arcpy.AddMessage("2. Flaechengroesse berechnen\n")
            arcpy.AddField_management("uzvr_lyr", "Flaeche_ha","Float")
            expression =  "!shape.area@HECTARES!"
            arcpy.CalculateField_management("uzvr_lyr","Flaeche_ha",expression,"PYTHON")

            #4. Gesamtflaeche der betroffenen Flaechen ermitteln
            print("3. Gesamtflaeche der betroffenen Flaechen ermitteln")
            arcpy.AddMessage("3. Gesamtflaeche der betroffenen Flaechen ermitteln")
            uzvr_betroffen = arcpy.SearchCursor("uzvr_lyr")
            flaecheHA = 0
            groessteUZVR = 0
            for flaeche in uzvr_betroffen:
                if(flaeche > groessteUZVR):
                    groessteUZVR = flaeche
                flaecheHA = flaecheHA + float(flaeche.Flaeche_ha)
            groUZVR = groessteUZVR.Flaeche_ha

            print("groUZVR1: "+ str(groUZVR) + "\n")
            arcpy.AddMessage("groUZVR1: "+ str(groUZVR) + "\n")

            print("Groesste betroffene Teilflaeche: "+ str(groessteUZVR) + " ha")
            arcpy.AddMessage("Groesste betroffene Teilflaeche: "+ str(groessteUZVR.Flaeche_ha) + " ha")
            print("Gesamtflaeche: "+str(flaecheHA)+" ha\n")
            arcpy.AddMessage("Gesamtflaeche: "+str(flaecheHA)+" ha\n")

            #5. Begegnungswahrscheinlichkeit berechnen
            print("4. Begegnungswahrschinlichkeit berechnen")
            arcpy.AddMessage("4. Begegnungswahrschinlichkeit berechnen")
            if(flaecheHA == 0):
                begegnungswahrscheinlichkeit = 1
            else:
                begegnungswahrscheinlichkeit = 0
                gebiet = arcpy.SearchCursor("uzvr_lyr")
                for flaeche in gebiet:
                    begegnungswahrscheinlichkeit = begegnungswahrscheinlichkeit + ((flaeche.Flaeche_ha/flaecheHA)*(flaeche.Flaeche_ha/flaecheHA))
            print("Begegnungswahrscheinlichkeit: "+ str(begegnungswahrscheinlichkeit) + "\n")
            arcpy.AddMessage("Begegnungswahrscheinlichkeit: "+ str(begegnungswahrscheinlichkeit)+"\n")

            #6. Effektive Maschenweite berechnen
            print("5. Effektive Maschenweite berechnen")
            arcpy.AddMessage("5. Effektive Maschenweite berechnen")
            effektiveMaschenweite = begegnungswahrscheinlichkeit * flaecheHA
            print("Effektive Maschenweite: "+str(effektiveMaschenweite) + "\n")
            arcpy.AddMessage("Effektive Maschenweite: "+str(effektiveMaschenweite) + "\n")


            #Berechnungen Planfall1
            arcpy.AddMessage("Unzerschnittene verkehrsarme Raeume: Planfall 1\n")
            print("Unzerschnittene verkehrsarme Raeume: Planfall 1\n")

            #1. Genaue Verschneidung der betroffenen Gebiete und der Planflaeche
            print("1. Genaue Verschneidung der betroffenen Gebiete und der Planflaeche\n")
            arcpy.AddMessage("1. Genaue Verschneidung der betroffenen Gebiete und der Planflaeche\n")
            arcpy.Clip_analysis(uzvr, projektFlaeche, "in_memory\\uzvr_lyr_clipped")

            #2. Groesse der genau verschnittenen Flaechen berechnen
            print("2. Groesse der genau verschnittenen Flaechen berechnen")
            arcpy.AddMessage("2. Groesse der genau verschnittenen Flaechen berechnen")
            #Feld neu berechnen
            expression =  "!shape.area@HECTARES!"
            arcpy.CalculateField_management("in_memory\\uzvr_lyr_clipped","Flaeche_ha",expression,"PYTHON")
            #Flaechen aufsummieren
            uzvr_betroffen_clipped = arcpy.SearchCursor("in_memory\\uzvr_lyr_clipped")
            flaecheHA_clipped = 0
            for flaeche in uzvr_betroffen_clipped:
                flaecheHA_clipped = flaecheHA_clipped + float(flaeche.Flaeche_ha)
            print("Gesamtflaeche: "+str(flaecheHA_clipped)+" ha\n")
            arcpy.AddMessage("Gesamtflaeche: "+str(flaecheHA_clipped)+" ha\n")
            #3. Begegnungswahrscheinlichkeit berechnen
            print("3. Begegnungswahrscheinlichkeit berechnen")
            arcpy.AddMessage("3. Begegnungswahrscheinlichkeit berechnen")
            if(flaecheHA_clipped == 0):
                begegnungswahrscheinlichkeit_clipped = 1
            else:
                begegnungswahrscheinlichkeit_clipped = 0
                gebiet = arcpy.SearchCursor("in_memory\\uzvr_lyr_clipped")
                for flaeche in gebiet:
                    begegnungswahrscheinlichkeit_clipped = begegnungswahrscheinlichkeit_clipped + ((flaeche.Flaeche_ha/flaecheHA_clipped)*(flaeche.Flaeche_ha/flaecheHA_clipped))
            print("Begegnungswahrscheinlichkeit: "+ str(begegnungswahrscheinlichkeit_clipped) + "\n")
            arcpy.AddMessage("Begegnungswahrscheinlichkeit: "+ str(begegnungswahrscheinlichkeit_clipped)+"\n")
            #4. Effektive Maschenweite berechnen
            print("4. Effektive Maschenweite berechnen")
            arcpy.AddMessage("4. Effektive Maschenweite berechnen")
            effektiveMaschenweite_clipped = begegnungswahrscheinlichkeit_clipped * flaecheHA_clipped
            print("Effektive Maschenweite: "+str(effektiveMaschenweite_clipped) + "\n")
            arcpy.AddMessage("Effektive Maschenweite: "+str(effektiveMaschenweite_clipped) + "\n")

            #Verteilung der UZVR in der Bewertungsebene (Region)
            # groessteUZVR = str(groessteUZVR)
            # groessteUZVR = groessteUZVR.replace(",",".")
            # if (Region == "Braunschweig-Salzgitter-Wolfenbuettel"):
            #     if (groessteUZVR < 1):
            #         bewertungUZVR = 5
            #     elif (groessteUZVR >= 1 and groessteUZVR <= 4.90):
            #         bewertungUZVR = 4
            #     elif (groessteUZVR >= 4.90 and groessteUZVR <= 31.80):
            #         bewertungUZVR = 3
            #     elif (groessteUZVR >= 31.80 and groessteUZVR <= 269.32):
            #         bewertungUZVR = 2
            #     elif (groessteUZVR > 269.32):
            #         bewertungUZVR = 1
            #
            # #Werte müssen noch für Region ermittelt werden
            # if (Region == "In und um Duesseldorf"):
            #     if (groessteUZVR < 1):
            #         bewertungUZVR = 5
            #     elif (groessteUZVR >= 1 and groessteUZVR <= 1.55):
            #         bewertungUZVR = 4
            #     elif (groessteUZVR >=1.55 and groessteUZVR <= 2.69):
            #         bewertungUZVR = 3
            #     elif (groessteUZVR >= 2.69 and groessteUZVR <= 5.09):
            #         bewertungUZVR = 2
            #     elif (groessteUZVR > 5.09):
            #         bewertungUZVR = 1
            #
            # if (Region == "Kreis Euskirchen"):
            #     if (groessteUZVR < 1):
            #         bewertungUZVR = 5
            #     elif (groessteUZVR >= 1 and groessteUZVR <= 5.67):
            #         bewertungUZVR = 4
            #     elif (groessteUZVR >=5.67 and groessteUZVR <= 307.30):
            #         bewertungUZVR = 3
            #     elif (groessteUZVR >= 307.30 and groessteUZVR <= 1594.22):
            #         bewertungUZVR = 2
            #     elif (groessteUZVR > 1594.22):
            #         bewertungUZVR = 1
            #
            # if (Region == "Kreis Unna"):
            #     if (groessteUZVR < 1):
            #         bewertungUZVR = 5
            #     elif (groessteUZVR >= 1 and groessteUZVR <= 8.59):
            #         bewertungUZVR = 4
            #     elif (groessteUZVR >=8.59 and groessteUZVR <= 34.56):
            #         bewertungUZVR = 3
            #     elif (groessteUZVR >= 34.56 and groessteUZVR <= 262.24):
            #         bewertungUZVR = 2
            #     elif (groessteUZVR > 262.24):
            #         bewertungUZVR = 1
            #
            # if (Region == "Landkreis Harburg"):
            #     if (groessteUZVR < 1):
            #         bewertungUZVR = 5
            #     elif (groessteUZVR >= 1 and groessteUZVR <= 5.79):
            #         bewertungUZVR = 4
            #     elif (groessteUZVR >=5.79 and groessteUZVR <= 54.77):
            #         bewertungUZVR = 3
            #     elif (groessteUZVR >= 54.77 and groessteUZVR <= 585.00):
            #         bewertungUZVR = 2
            #     elif (groessteUZVR > 585.00):
            #         bewertungUZVR = 1
            #
            # if (Region == "Landkreis Wolfenbuettel"):
            #     if (groessteUZVR < 1):
            #         bewertungUZVR = 5
            #     elif (groessteUZVR >= 1 and groessteUZVR <= 35.06):
            #         bewertungUZVR = 4
            #     elif (groessteUZVR >=35.06 and groessteUZVR <= 285.28):
            #         bewertungUZVR = 3
            #     elif (groessteUZVR >= 285.28 and groessteUZVR <= 637.15):
            #         bewertungUZVR = 2
            #     elif (groessteUZVR > 637.15):
            #         bewertungUZVR = 1
            #
            # if (Region == "Rheinisch-Bergischer Kreis"):
            #     if (groessteUZVR < 1):
            #         bewertungUZVR = 5
            #     elif (groessteUZVR >= 1 and groessteUZVR <= 9.59):
            #         bewertungUZVR = 4
            #     elif (groessteUZVR >=9.59 and groessteUZVR <= 107.75):
            #         bewertungUZVR = 3
            #     elif (groessteUZVR >= 107.75 and groessteUZVR <= 450.41):
            #         bewertungUZVR = 2
            #     elif (groessteUZVR > 450.41):
            #         bewertungUZVR = 1


            if (Region == "Braunschweig-Salzgitter-Wolfenbuettel"):
                if (groUZVR < 1):
                    bewertungUZVR = 5
                elif (groUZVR >= 1 and groUZVR <= 4.90):
                    bewertungUZVR = 4
                elif (groUZVR >= 4.90 and groUZVR <= 31.80):
                    bewertungUZVR = 3
                elif (groUZVR >= 31.80 and groUZVR <= 269.32):
                    bewertungUZVR = 2
                elif (groUZVR > 269.32):
                    bewertungUZVR = 1

            #Werte müssen noch für Region ermittelt werden
            if (Region == "In und um Duesseldorf"):
                if (groUZVR < 1):
                    bewertungUZVR = 5
                elif (groUZVR >= 1 and groUZVR <= 1.55):
                    bewertungUZVR = 4
                elif (groUZVR >=1.55 and groUZVR <= 2.69):
                    bewertungUZVR = 3
                elif (groUZVR >= 2.69 and groUZVR <= 5.09):
                    bewertungUZVR = 2
                elif (groUZVR > 5.09):
                    bewertungUZVR = 1

            if (Region == "Kreis Euskirchen"):
                if (groUZVR < 1):
                    bewertungUZVR = 5
                elif (groUZVR >= 1 and groUZVR <= 5.67):
                    bewertungUZVR = 4
                elif (groUZVR >=5.67 and groUZVR <= 307.30):
                    bewertungUZVR = 3
                elif (groUZVR >= 307.30 and groUZVR <= 1594.22):
                    bewertungUZVR = 2
                elif (groUZVR > 1594.22):
                    bewertungUZVR = 1

            if (Region == "Kreis Unna"):
                if (groUZVR < 1):
                    bewertungUZVR = 5
                elif (groUZVR >= 1 and groUZVR <= 8.59):
                    bewertungUZVR = 4
                elif (groUZVR >=8.59 and groUZVR <= 34.56):
                    bewertungUZVR = 3
                elif (groUZVR >= 34.56 and groUZVR <= 262.24):
                    bewertungUZVR = 2
                elif (groUZVR > 262.24):
                    bewertungUZVR = 1

            if (Region == "Landkreis Harburg"):
                if (groUZVR < 1):
                    bewertungUZVR = 5
                elif (groUZVR >= 1 and groUZVR <= 5.79):
                    bewertungUZVR = 4
                elif (groUZVR >=5.79 and groUZVR <= 54.77):
                    bewertungUZVR = 3
                elif (groUZVR >= 54.77 and groUZVR <= 585.00):
                    bewertungUZVR = 2
                elif (groUZVR > 585.00):
                    bewertungUZVR = 1

            if (Region == "Landkreis Wolfenbuettel"):
                if (groUZVR < 1):
                    bewertungUZVR = 5
                elif (groUZVR >= 1 and groUZVR <= 35.06):
                    bewertungUZVR = 4
                elif (groUZVR >=35.06 and groUZVR <= 285.28):
                    bewertungUZVR = 3
                elif (groUZVR >= 285.28 and groUZVR <= 637.15):
                    bewertungUZVR = 2
                elif (groUZVR > 637.15):
                    bewertungUZVR = 1

            if (Region == "Rheinisch-Bergischer Kreis"):
                if (groUZVR < 1):
                    bewertungUZVR = 5
                elif (groUZVR >= 1 and groUZVR <= 9.59):
                    bewertungUZVR = 4
                elif (groUZVR >=9.59 and groUZVR <= 107.75):
                    bewertungUZVR = 3
                elif (groUZVR >= 107.75 and groUZVR <= 450.41):
                    bewertungUZVR = 2
                elif (groUZVR > 450.41):
                    bewertungUZVR = 1

            #
            # print("bewertungUZVR: "+str(bewertungUZVR) + "\n")
            # arcpy.AddMessage("bewertungUZVR: "+str(bewertungUZVR) + "\n")
            # print("begegnungswahrscheinlichkeit: "+str(begegnungswahrscheinlichkeit) + "\n")
            # arcpy.AddMessage("begegnungswahrscheinlichkeit: "+str(begegnungswahrscheinlichkeit) + "\n")
            # print("begegnungswahrscheinlichkeit_clipped: "+str(begegnungswahrscheinlichkeit_clipped) + "\n")
            # arcpy.AddMessage("begegnungswahrscheinlichkeit_clipped: "+str(begegnungswahrscheinlichkeit_clipped) + "\n")
            # print("groessteUZVR: "+str(groessteUZVR) + "\n")
            # arcpy.AddMessage("groessteUZVR: "+str(groessteUZVR) + "\n")
            # print("groUZVR2: "+str(groUZVR) + "\n")
            # arcpy.AddMessage("groUZVR2: "+str(groUZVR) + "\n")

        rueckgabe = [bewertungUZVR, begegnungswahrscheinlichkeit,begegnungswahrscheinlichkeit_clipped,groUZVR]
        return rueckgabe

    except:
        e = sys.exc_info()[0]
        raise e
    #return bewertung
    finally:
        del uzvr_betroffen, uzvr_betroffen_clipped
        gc.collect()
        arcpy.Delete_management("in_memory\\uzvr_lyr_clipped")


#Flaecheninanspruchname'

def flaechenInanspruchname(integrationsgrad,typ):
    integrationsgrad = integrationsgrad.replace(",",".")
    integrationsgrad = float(integrationsgrad)
    #arcpy.AddMessage("========================")
    #arcpy.AddMessage("Bewertung der Flaecheninanspruchname\n")
    #print("========================")
    #print("Bewertung der Flaecheninanspruchname\n")
    #neuinanspruchname = float (neuinanspruchname)
    ##Bewertung Quantitaet
    #try:
    #    if (neuinanspruchname == 0):
    #        bewertungQuantitaet = 1
    #    if ((12-neuinanspruchname) <= 10 ):
    #        bewertungQuantitaet = 0.5
    #    if ((12-neuinanspruchname) >= 10 ):
    #        bewertungQuantitaet = 0
    #    print("Bewertung der Flächenneuinanspruchname: " + str(bewertungQuantitaet) + "\n")
    #    arcpy.AddMessage("Bewertung der Flächenneuinanspruchname: " + str(bewertungQuantitaet)+ "\n")

    try:
        bewertungQuantitaet = 0
        bewertungDichte = 0
        ##Bewertung Dichte
        #wcd = os.getcwd()
        #rootPfad = sys.path[0].split("2_")[0]
        ##Pfad zu den bkg Daten
        #projektFlaeche = rootPfad + "\\3_Projekte\\" + projektName + "\\FGDB_11_Definition_Projekt_" + projektName + ".gdb\\Teilflaechen_Plangebiet"
        #bkg = rootPfad + "\\1_Basisdaten\\FGBD_01_Basisdaten_deutschland.gdb\\bkg_gemeinden"
        ##Einwohnerzahl aus BKG Daten extrahieren, dafür Gemeinde selektieren, die von Planfläche geschnitten wird
        ##1. Feature Layer aus den bkg-daten erstellen
        #arcpy.MakeFeatureLayer_management(bkg,"bkg_lyr")
        ##2.Spatial Select wo Planfläche bkg_lyr intersected
        #arcpy.SelectLayerByLocation_management("bkg_lyr", "INTERSECT", projektFlaeche)
        ##Wenn Flaeche = 1, EWZ extrahieren
        #n = arcpy.GetCount_management("bkg_lyr").getOutput(0)
        #if(int(n) ==1 ):
        #    gemeindeCursor = arcpy.SearchCursor("bkg_lyr")
        #    for gemeinde in gemeindeCursor:
        #        ewz = gemeinde.EWZ
        #if(int(n)>=2):
        #    print("Die Teilflaeche schneidet mehr als eine Gemeinde oder liegt ausserhalb Deutschlands.\n Bitte ueberpruefen Sie die raeumliche Auspraegung der Datei 'Teilfalechen_Plangebiet' im Projektordner")
        #    arcpy.AddMessage("Die Teilflaeche schneidet mehr als eine Gemeinde oder liegt ausserhalb Deutschlands.\n Bitte ueberpruefen Sie die raeumliche Auspraegung der Datei 'Teilfalechen_Plangebiet' im Projektordner")
        #    print("Anzahl der geschnittenen Gemeinden: " + str(arcpy.GetCount_management("bkg_lyr")) + "\n")
        #    arcpy.AddMessage("Anzahl der Flaechen: " + str(arcpy.GetCount_management("bkg_lyr")) + "\n")
        #    sys.exit("Die Teilflaeche schneidet mehr als eine Gemeinde oder liegt ausserhalb Deutschlands.\n Bitte ueberpruefen Sie die raeumliche Auspraegung der Datei 'Teilfalechen_Plangebiet' im Projektordner")
        #if(ewz<=50000):
        #    if(bebauungsdichte <= 20):
        #        bewertungDichte = 0
        #    if(bebauungsdichte >= 20 and bebauungsdichte <23):
        #        bewertungDichte = 0.3
        #    if(bebauungsdichte >= 23 and bebauungsdichte < 26):
        #        bewertungDichte = 0.6
        #    if(bebauungsdichte >= 26):
        #        bewertungDichte = 1
        #if(ewz > 50000 and ewz <= 100000):
        #    if(bebauungsdichte <= 27):
        #        bewertungDichte = 0
        #    if(bebauungsdichte >= 27 and bebauungsdichte <29):
        #        bewertungDichte = 0.3
        #    if(bebauungsdichte >= 29 and bebauungsdichte < 43):
        #        bewertungDichte = 0.6
        #    if(bebauungsdichte >= 43):
        #        bewertungDichte = 1
        #if(ewz > 100000):
        #    if(bebauungsdichte <= 35):
        #        bewertungDichte = 0
        #    if(bebauungsdichte >= 35 and bebauungsdichte <39):
        #        bewertungDichte = 0.3
        #    if(bebauungsdichte >= 39 and bebauungsdichte < 44):
        #        bewertungDichte = 0.6
        #    if(bebauungsdichte >= 44):
        #        bewertungDichte = 1
        #print("Bewertung der Bebauungsdichte: " + str(bewertungDichte) + "\n")
        #arcpy.AddMessage("Bewertung der Bebauungsdichte: " + str(bewertungDichte)+ "\n")
        #arcpy.AddMessage("Integrationsgrad = " + str(integrationsgrad))
        #if (bauluecke == "true"):
        #    integrationsgrad = 100
        #bewertung Integrationsgrad (integrationsgrad wird vorher berechnet, als parameter mit zum skript uebergeben!)

        ## von Alex von hier kommentiert (29.9.)
        # if(typ=="Gewerbe"):
        #     if (integrationsgrad <=50):
        #         bewertungIntegration = (integrationsgrad*2/100)
        #     else:
        #         bewertungIntegration = 100
        # if(typ=="Wohnen"):
        #     bewertungIntegration = integrationsgrad/100
        # if(typ=="Einzelhandel"):
        #     bewertungIntegration = integrationsgrad/100
        ## von Alex bis hier kommentiert (29.9.)

        #print("Bewertung des Integrationsgrades: "+ str(bewertungIntegration)+"\n")
        #arcpy.AddMessage("Bewertung des Integrationsgrades: "+ str(bewertungIntegration)+"\n")
        rueckgabe = [bewertungQuantitaet,bewertungDichte,bewertungIntegration]

        return rueckgabe
    except Exception as e:
        return e

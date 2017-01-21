# -*- coding: utf-8 -*-

import time
import datetime
import sys
import imp
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell, xl_col_to_name
import arcpy, os
import gc
from rpctools.utils.params import Tool


class Nutzungen(Tool):
    _param_projectname = 'FGDB_Definition_Projekt.gdb'

    def run(self):

        parameters = self.par
        messages = self.mes

        projectname = parameters[0].valueAsText
        parameterString = parameters[1].valueAsText

        Teilflaeche_Plangebiet = parameterString.split(" | ")[0]
        tabelle_gebaude = self.get_table('Gebaeude_Details')
        tabelle_wohneinheiten_details = self.get_table('Wohneinheiten_Details')
        tabelle_verkaufsflaechen = self.get_table('Versorgung_Verkaufsflaechen')
        tabelle_gewerbe = self.get_table('Gewerbe_Teilflaechen')
        tabelle_betriebsflaeche = self.get_table('Gewerbe_Betriebsflaechen')
        tabelle_betriebsstruktur = self.get_table('Gewerbe_Betriebsstruktur')
        tabelle_gewerbeanteile = self.get_table('Gewerbe_Anteile')

        #Alte Eingaben löschen

        with arcpy.da.UpdateCursor(tabelle_gebaude, 'Teilflaeche_Plangebiet') as cursor:
            for row in cursor:
                if row[0] == Teilflaeche_Plangebiet:
                    cursor.deleteRow()

        with arcpy.da.UpdateCursor(tabelle_wohneinheiten_details, 'Teilflaeche_Plangebiet') as cursor:
            for row in cursor:
                if row[0] == Teilflaeche_Plangebiet:
                    cursor.deleteRow()

        with arcpy.da.UpdateCursor(tabelle_verkaufsflaechen, 'Teilflaeche_Plangebiet') as cursor:
            for row in cursor:
                if row[0] == Teilflaeche_Plangebiet:
                    cursor.deleteRow()

        with arcpy.da.UpdateCursor(tabelle_gewerbe, 'teilflaeche') as cursor:
            for row in cursor:
                if row[0] == Teilflaeche_Plangebiet:
                    cursor.deleteRow()

        with arcpy.da.UpdateCursor(tabelle_betriebsflaeche, 'teilflaeche') as cursor:
            for row in cursor:
                if row[0] == Teilflaeche_Plangebiet:
                    cursor.deleteRow()

        with arcpy.da.UpdateCursor(tabelle_betriebsstruktur, 'teilflaeche') as cursor:
            for row in cursor:
                if row[0] == Teilflaeche_Plangebiet:
                    cursor.deleteRow()

        with arcpy.da.UpdateCursor(tabelle_gewerbeanteile, 'teilflaeche') as cursor:
            for row in cursor:
                if row[0] == Teilflaeche_Plangebiet:
                    cursor.deleteRow()

        # WOHNGEBÄUDE

        flaechenbilanz = self.get_table('Flaechenbilanz')
        plangebiet = self.get_table('Teilflaechen_Plangebiet')

        cursor = arcpy.da.UpdateCursor(plangebiet, ['Name','Beginn_Nutzung','Aufsiedlungsdauer'])
        for row in cursor:
            if row[0] == parameters[1].valueAsText:
                row[1] = parameters[2].valueAsText
                row[2] = parameters[3].valueAsText
                cursor.updateRow(row)

        for i in range(0,int(parameters[3].valueAsText)):

            jahr = int(parameters[2].valueAsText) + i

            messages.AddMessage(jahr)
            Insert = arcpy.da.InsertCursor(tabelle_gebaude, ['Teilflaeche_Plangebiet','Gebaeudetyp','Anzahl_Gebaeude','Jahr'])
            row = ["","","",""]

            #Ein- und Zweifamilienhäuser
            if int(parameters[4].valueAsText) >0:
                row[0] = parameters[1].valueAsText
                row[1] = "Einfamilienhaus"
                row[2] = int(parameters[4].valueAsText) / int(parameters[3].valueAsText)
                row[3] = jahr
                Insert.insertRow(row)

            #Doppelhäuser
            if int(parameters[5].valueAsText) >0:
                row[0] = parameters[1].valueAsText
                row[1] = "Zweifamilien- oder Doppelhaus"
                row[2] =  int(parameters[5].valueAsText) / int(parameters[3].valueAsText)
                row[3] = jahr
                Insert.insertRow(row)

            #Reihenhäuser
            if int(parameters[6].valueAsText) >0:
                row[0] = parameters[1].valueAsText
                row[1] = "Reihenhaus"
                row[2] =  int(parameters[6].valueAsText) / int(parameters[3].valueAsText)
                row[3] = jahr
                Insert.insertRow(row)

            #Mehrfamilienhäuser
            if int(parameters[7].valueAsText) >0:
                row[0] = parameters[1].valueAsText
                row[1] = "Mehrfamilienhaus"
                row[2] =  int(parameters[7].valueAsText) / int(parameters[3].valueAsText)
                row[3] = jahr
                Insert.insertRow(row)

            del row, Insert

            #tabelle "Wohneinheiten_Details" oeffnen und Werte fuer Miete_Eigentum. und Anzahl Wohneinheiten speichern
            tabelle_wohneinheiten_details = self.get_table('Wohneinheiten_Details')

            Insert = arcpy.da.InsertCursor(tabelle_wohneinheiten_details, ['Gebaeudetyp','Teilflaeche_Plangebiet','Miete_Eigentum','EW_je_WE','Jahr','Anzahl_WE', 'Ant_Eigentuemer'])
            row = ["","","","","","",""]

            #Ein- und Zweifamilienhäuser
            eigentum = int(parameters[8].valueAsText)
            miete = 100 - int(parameters[8].valueAsText)
            nutzungstypen = [(eigentum,'Eigentum'),(miete,'Miete')]

            for nutzungstyp in nutzungstypen:
                row[0] = "Einfamilienhaus"
                row[1] = parameters[1].valueAsText
                row[2] = nutzungstyp[1]
                row[3] = float((parameters[12].valueAsText.split(" ")[0]).replace(",", "."))
                row[4] = jahr
                row[5] = int(parameters[4].valueAsText) / int(parameters[3].valueAsText) * nutzungstyp[0] / 100
                row[6] = parameters[8].valueAsText
                Insert.insertRow(row)

            #Doppelhäuser
            eigentum = int(parameters[9].valueAsText)
            miete = 100 - int(parameters[9].valueAsText)
            nutzungstypen = [(eigentum,'Eigentum'),(miete,'Miete')]

            for nutzungstyp in nutzungstypen:
                row[0] = "Zweifamilien- oder Doppelhaus"
                row[1] = parameters[1].valueAsText
                row[2] = nutzungstyp[1]
                row[3] = float((parameters[12].valueAsText.split(" ")[0]).replace(",", "."))
                row[4] = jahr
                row[5] = int(parameters[4].valueAsText) / int(parameters[3].valueAsText) * nutzungstyp[0] / 100
                row[6] = parameters[9].valueAsText
                Insert.insertRow(row)

            #Reihenhäuser
            eigentum = int(parameters[10].valueAsText)
            miete = 100 - int(parameters[10].valueAsText)
            nutzungstypen = [(eigentum,'Eigentum'),(miete,'Miete')]

            for nutzungstyp in nutzungstypen:
                row[0] = "Reihenhaus"
                row[1] = parameters[1].valueAsText
                row[2] = nutzungstyp[1]
                row[3] = float((parameters[12].valueAsText.split(" ")[0]).replace(",", "."))
                row[4] = jahr
                row[5] = int(parameters[4].valueAsText) / int(parameters[3].valueAsText) * nutzungstyp[0] / 100
                row[6] = parameters[10].valueAsText
                Insert.insertRow(row)

            #RMehrfamilienhäuser
            eigentum = int(parameters[11].valueAsText)
            miete = 100 - int(parameters[11].valueAsText)
            nutzungstypen = [(eigentum,'Eigentum'),(miete,'Miete')]

            for nutzungstyp in nutzungstypen:
                row[0] = "Mehrfamilienhaus"
                row[1] = parameters[1].valueAsText
                row[2] = nutzungstyp[1]
                row[3] = float((parameters[12].valueAsText.split(" ")[0]).replace(",", "."))
                row[4] = jahr
                row[5] = int(parameters[4].valueAsText) / int(parameters[3].valueAsText) * nutzungstyp[0] / 100
                row[6] = parameters[11].valueAsText
                Insert.insertRow(row)

        del row, Insert


        # GEWERBE

        Insert = arcpy.InsertCursor(tabelle_gewerbeanteile)
        row = Insert.newRow()
        row.setValue("teilflaeche", parameters[1].valueAsText)
        row.setValue("branche", parameters[17].valueAsText)
        row.setValue("Anteil_A", parameters[18].valueAsText)
        row.setValue("Anteil_B", parameters[19].valueAsText)
        row.setValue("Anteil_C", parameters[20].valueAsText)
        row.setValue("Anteil_D", parameters[21].valueAsText)
        row.setValue("Anteil_E", parameters[22].valueAsText)
        row.setValue("Anteil_F", parameters[23].valueAsText)
        row.setValue("Anteil_Zuzug", parameters[24].valueAsText)
        row.setValue("Anteil_Eigentum", parameters[25].valueAsText)
        Insert.insertRow(row)
        del row, Insert

        def beschaeftigte_gewerbe(projektname):

            #Pfade anlegen
            base_path = str(sys.path[0]).split("2_Tool")[0]
            shape_bkggemeiden=join(base_path,'1_Basisdaten','FGBD_Basisdaten_deutschland.gdb','bkg_gemeinden')
            workspace_Basis_Daten_Versor=join(base_path,'2_Tool',"G_Standortkonkurrenz_Supermaerkte",'FGDB_Standortkonkurrenz_Supermaerkte_Tool.gdb')
            workspace_Basis_Daten=join(base_path,'2_Tool',"3_Art und Mass der Nutzung",'FGDB_Definition_Projekt_Tool.gdb')
            shape_teilflaeche = self.folders.get_table('Teilflaechen_Plangebiet')
            workspace_definition= join(self.folders.get_projectpath(), 'FGDB_Definition_Projekt.gdb')


            # Process: Layer lagebezogen auswählen
            arcpy.MakeFeatureLayer_management(shape_bkggemeiden, 'bkg_gemeinden_lyr')
            arcpy.SelectLayerByLocation_management('bkg_gemeinden_lyr', "CONTAINS",shape_teilflaeche , "", "NEW_SELECTION")


            # If features matched criterias write them to a new feature class
            matchcount = int(arcpy.GetCount_management('bkg_gemeinden_lyr').getOutput(0))
            if matchcount == 0:
                b='Zuordnung zu einer Gemeinde unmoeglich - Kontaktieren Sie den Programmierer.'
                print b
                messages.AddMessage(b)
                exit(1)
            else:
                AGS=0
                GAGS=0
                cur_Search_Lry=arcpy.SearchCursor('bkg_gemeinden_lyr')
                for a in cur_Search_Lry:
                    AGS=int(a.AGS)
                    print "AGS ",AGS
                    break
                del cur_Search_Lry

                cur_Sear_GGEN= arcpy.SearchCursor(join(workspace_Basis_Daten_Versor,"Gesamtgemeinden"))

                array_ags_gags=[]
                for speicher in cur_Sear_GGEN:
                    array_ags_gags.append([int(speicher.AGS),int(speicher.VAGS)])

                del speicher,cur_Sear_GGEN

                for b in array_ags_gags:
                    if AGS==b[0]:
                        GAGS=b[1]
                        print "GAGS ",GAGS
                        break

                del array_ags_gags

                array_branche_anzahl=[]
                cur_Search_beschaeftigte= arcpy.SearchCursor(join(workspace_definition,"Gewerbe_Teilflaechen"))

                for c in cur_Search_beschaeftigte:
                    if len(array_branche_anzahl)==0:
                        array_branche_anzahl.append([str(c.branche),(c.beschaeftigte)])
                    else:
                        if len([t for t in array_branche_anzahl if t[0]==c.Branche])>0:
                            #bereits vorhanden
                            for z in array_branche_anzahl:
                                if z[0]==c.branche:
                                    z[1]+=(c.beschaeftigte)


                        else:
                            array_branche_anzahl.append([str(c.branche),(c.beschaeftigte)])

                print array_branche_anzahl
                del cur_Search_beschaeftigte



                #gesamtgemeinde + anzahl beschaeftigte pro branche -> multiplikation -> fertig
                gesamt_anzahl=0
                for hh in array_branche_anzahl:
                    gesamt_anzahl+=hh[1]

                print gesamt_anzahl
                gesamt_anzahl=round(gesamt_anzahl)
                print "Gesamt anzahl ",gesamt_anzahl
                array_ergebnis=[]

                print "Teilzeit"
                cur_Search_teilzeit = arcpy.SearchCursor(join(workspace_Basis_Daten,"gewerbe_teilzeit"))
                for p in cur_Search_teilzeit:
                    laenge= len(str(p.NR))
                    if (p.Nr == int(str(GAGS)[:laenge])):
                ##                print p.Nr
                        b1=0
                        faktor=0
                        for branchen in array_branche_anzahl:
                            faktor=p.getValue(branchen[0])
                            b1 += (faktor*branchen[1])/100.
                    ##                    print "Faktor ",faktor,"Branche",branchen[0],"Anzahl Besch",branchen[1] ,"Ergebnis",faktor*branchen[1]
                        b1=int(b1)
                        array_ergebnis.append(["Teilzeit",b1])
                        break
            ##        print "Summe der einzelnen Ergebnisse ",b1
            ##        print array_ergebnis
                del cur_Search_teilzeit
            ##        print "Geringfuegig"
                cur_Search_gering = arcpy.SearchCursor(join(workspace_Basis_Daten,"gewerbe_geringfuegig"))
                for p in cur_Search_gering:
                    laenge= len(str(p.NR))
                    if (p.Nr == int(str(GAGS)[:laenge])):
                        b1=0
                        faktor=0
                        for branchen in array_branche_anzahl:
                            faktor=p.getValue(branchen[0])
                            b1 += (faktor*branchen[1])/100.
                            print "Faktor ",faktor ,"Ergebnis",b1
                        b1=int(b1)
                        array_ergebnis.append(["Geringfuegig",b1])
                        break

            ##        print array_ergebnis
                del cur_Search_gering
                print "Akademisch"
                cur_Search_akademisch = arcpy.SearchCursor(join(workspace_Basis_Daten,"gewerbe_akademisch"))
                for p in cur_Search_akademisch:
                    laenge= len(str(p.NR))
                    if (p.Nr == int(str(GAGS)[:laenge])):
                        b1=0
                        faktor=0
                        for branchen in array_branche_anzahl:
                            faktor=p.getValue(branchen[0])
                            b1 += (faktor*branchen[1])/100.
                            print "Faktor ",faktor ,"Ergebnis",b1
                        b1=int(b1)
                        array_ergebnis.append(["Hochschulausbildung",b1])
                        array_ergebnis.append(["Gesamt",int(gesamt_anzahl)])
                        break

                print array_ergebnis
                del cur_Search_akademisch,array_branche_anzahl,gesamt_anzahl


                try:
                    arcpy.Delete_management(join(workspace_definition,"Gewerbe_Beschaeftigte_Zahlen"))
            ##            arcpy.Delete_management(join(workspace_definition,"Gewerbe_Beschaeftigte_Zahlen"))
            ##            arcpy.DeleteFeatures_management("Gewerbe_Beschaeftigte_Zahlen")
                except:
                    pass


                try:
                    arcpy.CreateTable_management(workspace_definition,"Gewerbe_Beschaeftigte_Zahlen")

                except:
                    a="Fehler Gewerbe_Beschaeftigte_Zahlen konnte nicht erstellt werden. Bitte ArcGis neustarten oder alle Files schliessen."
                    print a
                    messages.AddErrorMessage(a)
                    exit(1)

                try:
                    arcpy.AddField_management(join(workspace_definition,"Gewerbe_Beschaeftigte_Zahlen"), "Info", "TEXT",250)
                    arcpy.AddField_management(join(workspace_definition,"Gewerbe_Beschaeftigte_Zahlen"), "Anzahl", "LONG")

                except:
                    a="Fehler Gewerbe_Beschaeftigte_Zahlen konnte nicht erstellt werden. Bitte ArcGis neustarten oder alle Files schliessen."
                    print a
                    messages.AddErrorMessage(a)
                    exit(1)

                cur_Ins_beschaef= arcpy.InsertCursor(join(workspace_definition,"Gewerbe_Beschaeftigte_Zahlen"))
                for a in array_ergebnis:
                    row = cur_Ins_beschaef.newRow()
                    row.setValue("Info",a[0])
                    row.setValue("Anzahl",a[1])
                    cur_Ins_beschaef.insertRow(row)

                del cur_Ins_beschaef



        schrittmeldung = 'Eingaben werden gelesen \n'
        messages.AddMessage(schrittmeldung)
        print schrittmeldung

        #Parameter aus Tool auslesen

        projektname = parameters[0].valueAsText
        teilflaeche = parameters[1].valueAsText
        startjahr = parameters[2].valueAsText
        aufsiedlungsdauer = parameters[3].valueAsText
        gebtyp = parameters[17].valueAsText
        zuzugsquote = parameters[24].valueAsText
        eigentumsquote = parameters[25].valueAsText
        Ant_Betr_VerarbGew = parameters[18].valueAsText
        Ant_Betr_BauGew = parameters[19].valueAsText
        Ant_Betr_HanKfZ = parameters[20].valueAsText
        Ant_Betr_VerLag = parameters[21].valueAsText
        Ant_Betr_FrWiTeDi = parameters[22].valueAsText
        Ant_Betr_SoDi = parameters[23].valueAsText

        if gebtyp != "<kein Gewerbegebiet vorhanden>":

            ######################################################
            #Prüfung der Branchenstruktur auf 100%
            SummeBranchen = int(Ant_Betr_VerarbGew) + int(Ant_Betr_BauGew) + int(Ant_Betr_HanKfZ) + int(Ant_Betr_VerLag) + int(Ant_Betr_FrWiTeDi) + int(Ant_Betr_SoDi)

            if SummeBranchen < 100:
                schrittmeldung = 'Die Summe der Branchenanteile liegt unter 100 Prozent. Bitte ueberpruefen Sie Ihre Angaben \n'
            elif SummeBranchen > 100:
                schrittmeldung = 'Die Summe der Branchenanteile liegt ueber 100 Prozent. Bitte ueberpruefen Sie Ihre Angaben \n'
            else:
                ######################################################
                #Zeitstempel definieren
                import time
                import datetime
                ts = time.time()
                timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                ######################################################
                #Flaechenbilanz berechnen

                #Pfade anlegen
                base_path = str(sys.path[0]).split("2_Tool")[0]
                tabelle_flaechenbilanzgrundlage = self.folders.get_base_table('FGDB_Definition_Projekt_Tool.gdb','gewerbe_flaechenutzungsbilanz')
                tabelle_flaechennutzung = self.folders.get_table('Flaechenbilanz_Planung_Prozent')
                shape_teilflaeche = self.folders.get_table('Teilflaechen_Plangebiet')
                flaechenbilanz = self.folders.get_table('Flaechenbilanz')

                #Größe der Gewerbefläche auslesen
                flaechenbilanz_cursor = arcpy.SearchCursor(flaechenbilanz)

                for row in flaechenbilanz_cursor:
                    if row.Teilflaeche_Plangebiet == teilflaeche and row.Flaechennutzung_S2 == "Gewerbeflaeche":
                        flaechengroesse = row.Flaeche_ha


                #In Abhaengigkeit vom Gebietstyp die Flaechenbilanz definieren
                # Dazu zunächst die Anteilswerte aus Grundlagentabelle auslesen
                rows_flaechenbilanzgrundlage = arcpy.SearchCursor(tabelle_flaechenbilanzgrundlage)
                ant_s2_allgGruen = 0
                ant_s2_strBeglGruen = 0
                ant_s2_InErsch = 0
                ant_s2_GewBauland = 0

                for row in rows_flaechenbilanzgrundlage:
                    if row.Flaechennutzung_S1 == "Gruenflaeche":
                        if row.Flaechennutzung_S2 == "Allgemeine Gruenflaechen":
                            if gebtyp == "Industriegebiet":
                                ant_s2_allgGruen = row.Industriegebiet
                            elif gebtyp == "Logistikgebiet":
                                ant_s2_allgGruen = row.Logistikgebiet
                            elif gebtyp == "Klassisches Gewerbegebiet":
                                ant_s2_allgGruen = row.Klass_Gewerbe
                            elif gebtyp == "Kleinteiliges Gewerbegebiet":
                                ant_s2_allgGruen = row.Klein_Gewerbe
                            elif gebtyp == "Hoeherwertiges Gewerbegebiet":
                                ant_s2_allgGruen = row.Hoeher_Gewerbe
                            elif gebtyp == "Technologiepark, Wissenschaftspark":
                                ant_s2_allgGruen = row.TechWissPark
                        if row.Flaechennutzung_S2 == "Strassenbegleitgruen":
                            if gebtyp == "Industriegebiet":
                                ant_s2_strBeglGruen = row.Industriegebiet
                            elif gebtyp == "Logistikgebiet":
                                ant_s2_strBeglGruen = row.Logistikgebiet
                            elif gebtyp == "Klassisches Gewerbegebiet":
                                ant_s2_strBeglGruen = row.Klass_Gewerbe
                            elif gebtyp == "Kleinteiliges Gewerbegebiet":
                                ant_s2_strBeglGruen = row.Klein_Gewerbe
                            elif gebtyp == "Hoeherwertiges Gewerbegebiet":
                                ant_s2_strBeglGruen = row.Hoeher_Gewerbe
                            elif gebtyp == "Technologiepark, Wissenschaftspark":
                                ant_s2_strBeglGruen = row.TechWissPark
                    if row.Flaechennutzung_S1 == "Erschliessungsflaeche":
                        if row.Flaechennutzung_S2 == "Oeffentlich - Innere Erschliessung":
                            if gebtyp == "Industriegebiet":
                                ant_s2_InErsch = row.Industriegebiet
                            elif gebtyp == "Logistikgebiet":
                                ant_s2_InErsch = row.Logistikgebiet
                            elif gebtyp == "Klassisches Gewerbegebiet":
                                ant_s2_InErsch = row.Klass_Gewerbe
                            elif gebtyp == "Kleinteiliges Gewerbegebiet":
                                ant_s2_InErsch = row.Klein_Gewerbe
                            elif gebtyp == "Hoeherwertiges Gewerbegebiet":
                                ant_s2_InErsch = row.Hoeher_Gewerbe
                            elif gebtyp == "Technologiepark, Wissenschaftspark":
                                ant_s2_InErsch = row.TechWissPark
                    if row.Flaechennutzung_S1 == "Nettobauland":
                        if row.Flaechennutzung_S2 == "Gewerbeflaeche":
                            if gebtyp == "Industriegebiet":
                                ant_s2_GewBauland = row.Industriegebiet
                            elif gebtyp == "Logistikgebiet":
                                ant_s2_GewBauland = row.Logistikgebiet
                            elif gebtyp == "Klassisches Gewerbegebiet":
                                ant_s2_GewBauland = row.Klass_Gewerbe
                            elif gebtyp == "Kleinteiliges Gewerbegebiet":
                                ant_s2_GewBauland = row.Klein_Gewerbe
                            elif gebtyp == "Hoeherwertiges Gewerbegebiet":
                                ant_s2_GewBauland = row.Hoeher_Gewerbe
                            elif gebtyp == "Technologiepark, Wissenschaftspark":
                                ant_s2_GewBauland = row.TechWissPark


                # und dann die definierten Anteile mit der Projektflaeche multiplizieren
                s2_allgGrue = flaechengroesse * ant_s2_allgGruen / 100
                s2_strBeglGrue = flaechengroesse * ant_s2_strBeglGruen / 100
                s2_InErsch = flaechengroesse * ant_s2_InErsch / 100
                s2_GewBauland = flaechengroesse * ant_s2_GewBauland / 100


                ######################################################
                # Anzahl der Betriebe nach Branchen bestimmen
                schrittmeldung = 'Branchenstrukturberechnung wird vorbereitet \n'
                messages.AddMessage(schrittmeldung)
                print schrittmeldung

                # erstmal Pfade definieren
                tabelle_BFG = self.folders.get_base_table('FGDB_Definition_Projekt_Tool.gdb','gewerbe_betriebsflaechengroesse')
                tabelle_betriebsstruktur = self.folders.get_table('Gewerbe_Betriebsstruktur')

                # dann zunächst die Betriebsanteile mit den definierten Parzellengrößen gewichten
                rows_BFG = arcpy.SearchCursor(tabelle_BFG)

                for row in rows_BFG:
                    if row.Branche == "C":
                        BFG_Betr_VerarbGew = float(row.Betriebsflaechengroesse_ha)
                    if row.Branche == "F":
                        BFG_Betr_BauGew = float(row.Betriebsflaechengroesse_ha)
                    if row.Branche == "G":
                        BFG_Betr_HanKfZ = float(row.Betriebsflaechengroesse_ha)
                    if row.Branche == "H":
                        BFG_Betr_VerLag = float(row.Betriebsflaechengroesse_ha)
                    if row.Branche == "M":
                        BFG_Betr_FrWiTeDi = float(row.Betriebsflaechengroesse_ha)
                    if row.Branche == "N":
                        BFG_Betr_SoDi = float(row.Betriebsflaechengroesse_ha)

                Flaeche_Betr_VerarbGew_temp = float(Ant_Betr_VerarbGew) * BFG_Betr_VerarbGew
                Flaeche_Betr_BauGew_temp = float(Ant_Betr_BauGew) * BFG_Betr_BauGew
                Flaeche_Betr_HanKfZ_temp = float(Ant_Betr_HanKfZ) * BFG_Betr_HanKfZ
                Flaeche_Betr_VerLag_temp = float(Ant_Betr_VerLag) * BFG_Betr_VerLag
                Flaeche_Betr_FrWiTeDi_temp = float(Ant_Betr_FrWiTeDi) * BFG_Betr_FrWiTeDi
                Flaeche_Betr_SoDi_temp = float(Ant_Betr_SoDi) * BFG_Betr_SoDi

                Flaeche_Gesamt_Temp = Flaeche_Betr_VerarbGew_temp + Flaeche_Betr_BauGew_temp + Flaeche_Betr_HanKfZ_temp + Flaeche_Betr_VerLag_temp + Flaeche_Betr_FrWiTeDi_temp + Flaeche_Betr_SoDi_temp

                #daraus die Flächenanteile ermitteln
                schrittmeldung = 'Gewerbeflaeche nach Branchen wird berechnet \n'
                messages.AddMessage(schrittmeldung)
                print schrittmeldung

                gewerbebauland = float(s2_GewBauland)
                Flaeche_Betr_VerarbGew = float(Flaeche_Betr_VerarbGew_temp) / float(Flaeche_Gesamt_Temp) * float(gewerbebauland)
                Flaeche_Betr_BauGew = float(Flaeche_Betr_BauGew_temp) / float(Flaeche_Gesamt_Temp) * float(gewerbebauland)
                Flaeche_Betr_HanKfZ = float(Flaeche_Betr_HanKfZ_temp) / float(Flaeche_Gesamt_Temp) * float(gewerbebauland)
                Flaeche_Betr_VerLag = float(Flaeche_Betr_VerLag_temp) / float(Flaeche_Gesamt_Temp) * float(gewerbebauland)
                Flaeche_Betr_FrWiTeDi = float(Flaeche_Betr_FrWiTeDi_temp) / float(Flaeche_Gesamt_Temp) * float(gewerbebauland)
                Flaeche_Betr_SoDi = float(Flaeche_Betr_SoDi_temp) / float(Flaeche_Gesamt_Temp) * float(gewerbebauland)

                #und über die BFG wieder zur Anzahl der Betriebe
                schrittmeldung = 'Betriebszahl nach Branchen wird berechnet \n'
                messages.AddMessage(schrittmeldung)
                print schrittmeldung
                BFGfaktor = 1.00
                if gebtyp == "Industriegebiet":
                    BFGfaktor = 1.50
                elif gebtyp == "Logistikgebiet":
                    BFGfaktor = 1.50
                elif gebtyp == "Klassisches Gewerbegebiet":
                    BFGfaktor = 1.00
                elif gebtyp == "Kleinteiliges Gewerbegebiet":
                    BFGfaktor = 0.70
                elif gebtyp == "Hoeherwertiges Gewerbegebiet":
                    BFGfaktor = 0.90
                elif gebtyp == "Technologiepark, Wissenschaftspark":
                    BFGfaktor = 0.85
                Anz_Betr_VerarbGew = Flaeche_Betr_VerarbGew / (BFG_Betr_VerarbGew * BFGfaktor)
                Anz_Betr_BauGew = Flaeche_Betr_BauGew / (BFG_Betr_BauGew * BFGfaktor)
                Anz_Betr_HanKfZ = Flaeche_Betr_HanKfZ / (BFG_Betr_HanKfZ * BFGfaktor)
                Anz_Betr_VerLag = Flaeche_Betr_VerLag / (BFG_Betr_VerLag * BFGfaktor)
                Anz_Betr_FrWiTeDi = Flaeche_Betr_FrWiTeDi / (BFG_Betr_FrWiTeDi * BFGfaktor)
                Anz_Betr_SoDi = Flaeche_Betr_SoDi / (BFG_Betr_SoDi * BFGfaktor)

                #Betriebsflaechen nach Branchen in Tabelle schreiben
                tabelle_betriebsflaeche = self.folders.get_table('Gewerbe_Betriebsflaechen')
                tabelle_betriebsflaeche_Insert = arcpy.InsertCursor(tabelle_betriebsflaeche)

                rowBFins = tabelle_betriebsflaeche_Insert.newRow()

                rowBFins.teilflaeche = teilflaeche
                rowBFins.gebietstyp = str(gebtyp)
                rowBFins.Betriebsflaeche_C = float(Flaeche_Betr_VerarbGew)
                rowBFins.Betriebsflaeche_F = float(Flaeche_Betr_BauGew)
                rowBFins.Betriebsflaeche_G = float(Flaeche_Betr_HanKfZ)
                rowBFins.Betriebsflaeche_H = float(Flaeche_Betr_VerLag)
                rowBFins.Betriebsflaeche_M = float(Flaeche_Betr_FrWiTeDi)
                rowBFins.Betriebsflaeche_N = float(Flaeche_Betr_SoDi)
                rowBFins.timestamp = str(timestamp)

                tabelle_betriebsflaeche_Insert.insertRow(rowBFins)


                #und nun noch die Beschäftigten berechnen
                schrittmeldung = 'Beschaeftigtenzahl nach Branchen wird berechnet \n'
                messages.AddMessage(schrittmeldung)
                print schrittmeldung

                tabelle_FKZ = self.folders.get_base_table('FGDB_Definition_Projekt_Tool.gdb','gewerbe_flaechenkennziffern')
                rows_FKZ = arcpy.SearchCursor(tabelle_FKZ)

                for row in rows_FKZ:
                    if row.Branche == "C":
                        FKZ_VerarbGew = float(row.Beschaeftigte_je_Hektar)
                    if row.Branche == "F":
                        FKZ_BauGew = float(row.Beschaeftigte_je_Hektar)
                    if row.Branche == "G":
                        FKZ_HanKfZ = float(row.Beschaeftigte_je_Hektar)
                    if row.Branche == "H":
                        FKZ_VerLag = float(row.Beschaeftigte_je_Hektar)
                    if row.Branche == "M":
                        FKZ_FrWiTeDi = float(row.Beschaeftigte_je_Hektar)
                    if row.Branche == "N":
                        FKZ_SoDi = float(row.Beschaeftigte_je_Hektar)

                Besch_VerarbGew = float(Flaeche_Betr_VerarbGew) * float(FKZ_VerarbGew)
                Besch_BauGew = float(Flaeche_Betr_BauGew) * float(FKZ_BauGew)
                Besch_HanKfZ = float(Flaeche_Betr_HanKfZ) * float(FKZ_HanKfZ)
                Besch_VerLag = float(Flaeche_Betr_VerLag) * float(FKZ_VerLag)
                Besch_FrWiTeDi = float(Flaeche_Betr_FrWiTeDi) * float(FKZ_FrWiTeDi)
                Besch_SoDi = float(Flaeche_Betr_SoDi) * float(FKZ_SoDi)

                ################################################
                ### Aufsiedlugnsdauer einrechnen
                schrittmeldung = 'Aufsiedlungsdauer wird auf Flaechen-, Betriebs- Beschaeftigtenstruktur umgelegt \n'
                messages.AddMessage(schrittmeldung)
                print schrittmeldung

                #### Aufsiedlugnsdauer Betriebe
                # zuletzt die Anzahl noch in die Ausgabetabelle schreiben und dabei mit der Aufsiedlungszeit verrechnen
                tabelle_parameter_aufsiedlungsdauer = self.folders.get_base_table('FGDB_Definition_Projekt_Tool.gdb','gewerbe_aufsiedlungsdauer')
                tabelle_gewerbe_betriebsstruktur_Insert = arcpy.InsertCursor(tabelle_betriebsstruktur)

                #für Branche C
                anzahl_betriebe_start = Anz_Betr_VerarbGew
                aufsiedlungsdauer = str(aufsiedlungsdauer)

                sql = "Dauer_Jahre = " + str(aufsiedlungsdauer)

                tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer, sql)
                parameter_jahr

                row2 = tabelle_parameter_aufsiedlungsdauer_Search.next()
                row3 = tabelle_gewerbe_betriebsstruktur_Insert.newRow()

                # setze Parameter Anzahl Betriebe für jedes Jahr
                YEARS = 30
                for i in range(YEARS):
                    parameter_jahr = getattr(row2, 'Jahr{}'.format(i+1))
                    value = anzahl_betriebe_start * parameter_jahr
                    setattr(row3, 'anzahl_betriebe_jahr_{}'.format(i), value)
                setattr(row3, 'anzahl_betriebe_jahr_{}'.format(i + 1), value)

                del tabelle_parameter_aufsiedlungsdauer_Search

                row3.projekt = projektname
                row3.teilflaeche = teilflaeche
                row3.branche = "C"
                row3.ID_ts = timestamp

                tabelle_gewerbe_betriebsstruktur_Insert.insertRow(row3)

                #für Branche F
                anzahl_betriebe_start = Anz_Betr_BauGew
                aufsiedlungsdauer = str(aufsiedlungsdauer)

                sql = "Dauer_Jahre = " + str(aufsiedlungsdauer)
                row3 = tabelle_gewerbe_betriebsstruktur_Insert.newRow()

                row3.anzahl_betriebe_jahr_0 = anzahl_betriebe_start * parameter_jahr1
                row3.anzahl_betriebe_jahr_1 = anzahl_betriebe_start * parameter_jahr2
                row3.anzahl_betriebe_jahr_2 = anzahl_betriebe_start * parameter_jahr3
                row3.anzahl_betriebe_jahr_3 = anzahl_betriebe_start * parameter_jahr4
                row3.anzahl_betriebe_jahr_4 = anzahl_betriebe_start * parameter_jahr5
                row3.anzahl_betriebe_jahr_5 = anzahl_betriebe_start * parameter_jahr6
                row3.anzahl_betriebe_jahr_6 = anzahl_betriebe_start * parameter_jahr7
                row3.anzahl_betriebe_jahr_7 = anzahl_betriebe_start * parameter_jahr8
                row3.anzahl_betriebe_jahr_8 = anzahl_betriebe_start * parameter_jahr9
                row3.anzahl_betriebe_jahr_9 = anzahl_betriebe_start * parameter_jahr10
                row3.anzahl_betriebe_jahr_10 = anzahl_betriebe_start * parameter_jahr11
                row3.anzahl_betriebe_jahr_11 = anzahl_betriebe_start * parameter_jahr12
                row3.anzahl_betriebe_jahr_12 = anzahl_betriebe_start * parameter_jahr13
                row3.anzahl_betriebe_jahr_13 = anzahl_betriebe_start * parameter_jahr14
                row3.anzahl_betriebe_jahr_14 = anzahl_betriebe_start * parameter_jahr15
                row3.anzahl_betriebe_jahr_15 = anzahl_betriebe_start * parameter_jahr16
                row3.anzahl_betriebe_jahr_16 = anzahl_betriebe_start * parameter_jahr17
                row3.anzahl_betriebe_jahr_17 = anzahl_betriebe_start * parameter_jahr18
                row3.anzahl_betriebe_jahr_18 = anzahl_betriebe_start * parameter_jahr19
                row3.anzahl_betriebe_jahr_19 = anzahl_betriebe_start * parameter_jahr20
                row3.anzahl_betriebe_jahr_20 = anzahl_betriebe_start * parameter_jahr21
                row3.anzahl_betriebe_jahr_21 = anzahl_betriebe_start * parameter_jahr22
                row3.anzahl_betriebe_jahr_22 = anzahl_betriebe_start * parameter_jahr23
                row3.anzahl_betriebe_jahr_23 = anzahl_betriebe_start * parameter_jahr24
                row3.anzahl_betriebe_jahr_24 = anzahl_betriebe_start * parameter_jahr25
                row3.anzahl_betriebe_jahr_25 = anzahl_betriebe_start * parameter_jahr26
                row3.anzahl_betriebe_jahr_26 = anzahl_betriebe_start * parameter_jahr27
                row3.anzahl_betriebe_jahr_27 = anzahl_betriebe_start * parameter_jahr28
                row3.anzahl_betriebe_jahr_28 = anzahl_betriebe_start * parameter_jahr29
                row3.anzahl_betriebe_jahr_29 = anzahl_betriebe_start * parameter_jahr30
                row3.anzahl_betriebe_jahr_30 = anzahl_betriebe_start * parameter_jahr30
                row3.projekt = projektname
                row3.teilflaeche = teilflaeche
                row3.branche = "F"
                row3.ID_ts = timestamp

                tabelle_gewerbe_betriebsstruktur_Insert.insertRow(row3)


                #für Branche G
                anzahl_betriebe_start = Anz_Betr_HanKfZ
                aufsiedlungsdauer = str(aufsiedlungsdauer)

                sql = "Dauer_Jahre = " + str(aufsiedlungsdauer)
                row3 = tabelle_gewerbe_betriebsstruktur_Insert.newRow()

                row3.anzahl_betriebe_jahr_0 = anzahl_betriebe_start * parameter_jahr1
                row3.anzahl_betriebe_jahr_1 = anzahl_betriebe_start * parameter_jahr2
                row3.anzahl_betriebe_jahr_2 = anzahl_betriebe_start * parameter_jahr3
                row3.anzahl_betriebe_jahr_3 = anzahl_betriebe_start * parameter_jahr4
                row3.anzahl_betriebe_jahr_4 = anzahl_betriebe_start * parameter_jahr5
                row3.anzahl_betriebe_jahr_5 = anzahl_betriebe_start * parameter_jahr6
                row3.anzahl_betriebe_jahr_6 = anzahl_betriebe_start * parameter_jahr7
                row3.anzahl_betriebe_jahr_7 = anzahl_betriebe_start * parameter_jahr8
                row3.anzahl_betriebe_jahr_8 = anzahl_betriebe_start * parameter_jahr9
                row3.anzahl_betriebe_jahr_9 = anzahl_betriebe_start * parameter_jahr10
                row3.anzahl_betriebe_jahr_10 = anzahl_betriebe_start * parameter_jahr11
                row3.anzahl_betriebe_jahr_11 = anzahl_betriebe_start * parameter_jahr12
                row3.anzahl_betriebe_jahr_12 = anzahl_betriebe_start * parameter_jahr13
                row3.anzahl_betriebe_jahr_13 = anzahl_betriebe_start * parameter_jahr14
                row3.anzahl_betriebe_jahr_14 = anzahl_betriebe_start * parameter_jahr15
                row3.anzahl_betriebe_jahr_15 = anzahl_betriebe_start * parameter_jahr16
                row3.anzahl_betriebe_jahr_16 = anzahl_betriebe_start * parameter_jahr17
                row3.anzahl_betriebe_jahr_17 = anzahl_betriebe_start * parameter_jahr18
                row3.anzahl_betriebe_jahr_18 = anzahl_betriebe_start * parameter_jahr19
                row3.anzahl_betriebe_jahr_19 = anzahl_betriebe_start * parameter_jahr20
                row3.anzahl_betriebe_jahr_20 = anzahl_betriebe_start * parameter_jahr21
                row3.anzahl_betriebe_jahr_21 = anzahl_betriebe_start * parameter_jahr22
                row3.anzahl_betriebe_jahr_22 = anzahl_betriebe_start * parameter_jahr23
                row3.anzahl_betriebe_jahr_23 = anzahl_betriebe_start * parameter_jahr24
                row3.anzahl_betriebe_jahr_24 = anzahl_betriebe_start * parameter_jahr25
                row3.anzahl_betriebe_jahr_25 = anzahl_betriebe_start * parameter_jahr26
                row3.anzahl_betriebe_jahr_26 = anzahl_betriebe_start * parameter_jahr27
                row3.anzahl_betriebe_jahr_27 = anzahl_betriebe_start * parameter_jahr28
                row3.anzahl_betriebe_jahr_28 = anzahl_betriebe_start * parameter_jahr29
                row3.anzahl_betriebe_jahr_29 = anzahl_betriebe_start * parameter_jahr30
                row3.anzahl_betriebe_jahr_30 = anzahl_betriebe_start * parameter_jahr30
                row3.projekt = projektname
                row3.teilflaeche = teilflaeche
                row3.branche = "G"
                row3.ID_ts = timestamp

                tabelle_gewerbe_betriebsstruktur_Insert.insertRow(row3)


                #für Branche H
                anzahl_betriebe_start = Anz_Betr_VerLag
                aufsiedlungsdauer = str(aufsiedlungsdauer)

                sql = "Dauer_Jahre = " + str(aufsiedlungsdauer)
                row3 = tabelle_gewerbe_betriebsstruktur_Insert.newRow()

                row3.anzahl_betriebe_jahr_0 = anzahl_betriebe_start * parameter_jahr1
                row3.anzahl_betriebe_jahr_1 = anzahl_betriebe_start * parameter_jahr2
                row3.anzahl_betriebe_jahr_2 = anzahl_betriebe_start * parameter_jahr3
                row3.anzahl_betriebe_jahr_3 = anzahl_betriebe_start * parameter_jahr4
                row3.anzahl_betriebe_jahr_4 = anzahl_betriebe_start * parameter_jahr5
                row3.anzahl_betriebe_jahr_5 = anzahl_betriebe_start * parameter_jahr6
                row3.anzahl_betriebe_jahr_6 = anzahl_betriebe_start * parameter_jahr7
                row3.anzahl_betriebe_jahr_7 = anzahl_betriebe_start * parameter_jahr8
                row3.anzahl_betriebe_jahr_8 = anzahl_betriebe_start * parameter_jahr9
                row3.anzahl_betriebe_jahr_9 = anzahl_betriebe_start * parameter_jahr10
                row3.anzahl_betriebe_jahr_10 = anzahl_betriebe_start * parameter_jahr11
                row3.anzahl_betriebe_jahr_11 = anzahl_betriebe_start * parameter_jahr12
                row3.anzahl_betriebe_jahr_12 = anzahl_betriebe_start * parameter_jahr13
                row3.anzahl_betriebe_jahr_13 = anzahl_betriebe_start * parameter_jahr14
                row3.anzahl_betriebe_jahr_14 = anzahl_betriebe_start * parameter_jahr15
                row3.anzahl_betriebe_jahr_15 = anzahl_betriebe_start * parameter_jahr16
                row3.anzahl_betriebe_jahr_16 = anzahl_betriebe_start * parameter_jahr17
                row3.anzahl_betriebe_jahr_17 = anzahl_betriebe_start * parameter_jahr18
                row3.anzahl_betriebe_jahr_18 = anzahl_betriebe_start * parameter_jahr19
                row3.anzahl_betriebe_jahr_19 = anzahl_betriebe_start * parameter_jahr20
                row3.anzahl_betriebe_jahr_20 = anzahl_betriebe_start * parameter_jahr21
                row3.anzahl_betriebe_jahr_21 = anzahl_betriebe_start * parameter_jahr22
                row3.anzahl_betriebe_jahr_22 = anzahl_betriebe_start * parameter_jahr23
                row3.anzahl_betriebe_jahr_23 = anzahl_betriebe_start * parameter_jahr24
                row3.anzahl_betriebe_jahr_24 = anzahl_betriebe_start * parameter_jahr25
                row3.anzahl_betriebe_jahr_25 = anzahl_betriebe_start * parameter_jahr26
                row3.anzahl_betriebe_jahr_26 = anzahl_betriebe_start * parameter_jahr27
                row3.anzahl_betriebe_jahr_27 = anzahl_betriebe_start * parameter_jahr28
                row3.anzahl_betriebe_jahr_28 = anzahl_betriebe_start * parameter_jahr29
                row3.anzahl_betriebe_jahr_29 = anzahl_betriebe_start * parameter_jahr30
                row3.anzahl_betriebe_jahr_30 = anzahl_betriebe_start * parameter_jahr30
                row3.projekt = projektname
                row3.teilflaeche = teilflaeche
                row3.branche = "H"
                row3.ID_ts = timestamp

                tabelle_gewerbe_betriebsstruktur_Insert.insertRow(row3)

                #für Branche M
                anzahl_betriebe_start = Anz_Betr_FrWiTeDi
                aufsiedlungsdauer = str(aufsiedlungsdauer)

                sql = "Dauer_Jahre = " + str(aufsiedlungsdauer)
                row3 = tabelle_gewerbe_betriebsstruktur_Insert.newRow()

                row3.anzahl_betriebe_jahr_0 = anzahl_betriebe_start * parameter_jahr1
                row3.anzahl_betriebe_jahr_1 = anzahl_betriebe_start * parameter_jahr2
                row3.anzahl_betriebe_jahr_2 = anzahl_betriebe_start * parameter_jahr3
                row3.anzahl_betriebe_jahr_3 = anzahl_betriebe_start * parameter_jahr4
                row3.anzahl_betriebe_jahr_4 = anzahl_betriebe_start * parameter_jahr5
                row3.anzahl_betriebe_jahr_5 = anzahl_betriebe_start * parameter_jahr6
                row3.anzahl_betriebe_jahr_6 = anzahl_betriebe_start * parameter_jahr7
                row3.anzahl_betriebe_jahr_7 = anzahl_betriebe_start * parameter_jahr8
                row3.anzahl_betriebe_jahr_8 = anzahl_betriebe_start * parameter_jahr9
                row3.anzahl_betriebe_jahr_9 = anzahl_betriebe_start * parameter_jahr10
                row3.anzahl_betriebe_jahr_10 = anzahl_betriebe_start * parameter_jahr11
                row3.anzahl_betriebe_jahr_11 = anzahl_betriebe_start * parameter_jahr12
                row3.anzahl_betriebe_jahr_12 = anzahl_betriebe_start * parameter_jahr13
                row3.anzahl_betriebe_jahr_13 = anzahl_betriebe_start * parameter_jahr14
                row3.anzahl_betriebe_jahr_14 = anzahl_betriebe_start * parameter_jahr15
                row3.anzahl_betriebe_jahr_15 = anzahl_betriebe_start * parameter_jahr16
                row3.anzahl_betriebe_jahr_16 = anzahl_betriebe_start * parameter_jahr17
                row3.anzahl_betriebe_jahr_17 = anzahl_betriebe_start * parameter_jahr18
                row3.anzahl_betriebe_jahr_18 = anzahl_betriebe_start * parameter_jahr19
                row3.anzahl_betriebe_jahr_19 = anzahl_betriebe_start * parameter_jahr20
                row3.anzahl_betriebe_jahr_20 = anzahl_betriebe_start * parameter_jahr21
                row3.anzahl_betriebe_jahr_21 = anzahl_betriebe_start * parameter_jahr22
                row3.anzahl_betriebe_jahr_22 = anzahl_betriebe_start * parameter_jahr23
                row3.anzahl_betriebe_jahr_23 = anzahl_betriebe_start * parameter_jahr24
                row3.anzahl_betriebe_jahr_24 = anzahl_betriebe_start * parameter_jahr25
                row3.anzahl_betriebe_jahr_25 = anzahl_betriebe_start * parameter_jahr26
                row3.anzahl_betriebe_jahr_26 = anzahl_betriebe_start * parameter_jahr27
                row3.anzahl_betriebe_jahr_27 = anzahl_betriebe_start * parameter_jahr28
                row3.anzahl_betriebe_jahr_28 = anzahl_betriebe_start * parameter_jahr29
                row3.anzahl_betriebe_jahr_29 = anzahl_betriebe_start * parameter_jahr30
                row3.anzahl_betriebe_jahr_30 = anzahl_betriebe_start * parameter_jahr30
                row3.projekt = projektname
                row3.teilflaeche = teilflaeche
                row3.branche = "M"
                row3.ID_ts = timestamp

                tabelle_gewerbe_betriebsstruktur_Insert.insertRow(row3)

                #für Branche N
                anzahl_betriebe_start = Anz_Betr_SoDi
                aufsiedlungsdauer = str(aufsiedlungsdauer)

                sql = "Dauer_Jahre = " + str(aufsiedlungsdauer)
                row3 = tabelle_gewerbe_betriebsstruktur_Insert.newRow()

                row3.anzahl_betriebe_jahr_0 = anzahl_betriebe_start * parameter_jahr1
                row3.anzahl_betriebe_jahr_1 = anzahl_betriebe_start * parameter_jahr2
                row3.anzahl_betriebe_jahr_2 = anzahl_betriebe_start * parameter_jahr3
                row3.anzahl_betriebe_jahr_3 = anzahl_betriebe_start * parameter_jahr4
                row3.anzahl_betriebe_jahr_4 = anzahl_betriebe_start * parameter_jahr5
                row3.anzahl_betriebe_jahr_5 = anzahl_betriebe_start * parameter_jahr6
                row3.anzahl_betriebe_jahr_6 = anzahl_betriebe_start * parameter_jahr7
                row3.anzahl_betriebe_jahr_7 = anzahl_betriebe_start * parameter_jahr8
                row3.anzahl_betriebe_jahr_8 = anzahl_betriebe_start * parameter_jahr9
                row3.anzahl_betriebe_jahr_9 = anzahl_betriebe_start * parameter_jahr10
                row3.anzahl_betriebe_jahr_10 = anzahl_betriebe_start * parameter_jahr11
                row3.anzahl_betriebe_jahr_11 = anzahl_betriebe_start * parameter_jahr12
                row3.anzahl_betriebe_jahr_12 = anzahl_betriebe_start * parameter_jahr13
                row3.anzahl_betriebe_jahr_13 = anzahl_betriebe_start * parameter_jahr14
                row3.anzahl_betriebe_jahr_14 = anzahl_betriebe_start * parameter_jahr15
                row3.anzahl_betriebe_jahr_15 = anzahl_betriebe_start * parameter_jahr16
                row3.anzahl_betriebe_jahr_16 = anzahl_betriebe_start * parameter_jahr17
                row3.anzahl_betriebe_jahr_17 = anzahl_betriebe_start * parameter_jahr18
                row3.anzahl_betriebe_jahr_18 = anzahl_betriebe_start * parameter_jahr19
                row3.anzahl_betriebe_jahr_19 = anzahl_betriebe_start * parameter_jahr20
                row3.anzahl_betriebe_jahr_20 = anzahl_betriebe_start * parameter_jahr21
                row3.anzahl_betriebe_jahr_21 = anzahl_betriebe_start * parameter_jahr22
                row3.anzahl_betriebe_jahr_22 = anzahl_betriebe_start * parameter_jahr23
                row3.anzahl_betriebe_jahr_23 = anzahl_betriebe_start * parameter_jahr24
                row3.anzahl_betriebe_jahr_24 = anzahl_betriebe_start * parameter_jahr25
                row3.anzahl_betriebe_jahr_25 = anzahl_betriebe_start * parameter_jahr26
                row3.anzahl_betriebe_jahr_26 = anzahl_betriebe_start * parameter_jahr27
                row3.anzahl_betriebe_jahr_27 = anzahl_betriebe_start * parameter_jahr28
                row3.anzahl_betriebe_jahr_28 = anzahl_betriebe_start * parameter_jahr29
                row3.anzahl_betriebe_jahr_29 = anzahl_betriebe_start * parameter_jahr30
                row3.anzahl_betriebe_jahr_30 = anzahl_betriebe_start * parameter_jahr30
                row3.projekt = projektname
                row3.teilflaeche = teilflaeche
                row3.branche = "N"
                row3.ID_ts = timestamp

                tabelle_gewerbe_betriebsstruktur_Insert.insertRow(row3)



                #### Aufsiedlugnsdauer Beschäftigte
                # zuletzt die Anzahl noch in die Ausgabetabelle schreiben und dabei mit der Aufsiedlungszeit verrechnen
                tabelle_parameter_aufsiedlungsdauer = self.folders.get_base_table('FGDB_Definition_Projekt_Tool.gdb','gewerbe_aufsiedlungsdauer')
                tabelle_beschaeftigte = self.folders.get_table('Gewerbe_Beschaeftigte')
                tabelle_beschaeftigte_insert = arcpy.InsertCursor(tabelle_beschaeftigte)
                tabelle_projektrahmendaten = self.folders.get_table('Projektrahmendaten')

                #Beschaeftigte Branche C / Besch_VerarbGew
                anzahl_Besch_max = float(Besch_VerarbGew)
                aufsiedlungsdauer = str(aufsiedlungsdauer)
                tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer)

                rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
                for row in rows_projektrahmen:
                    ende = row.Ende_Betrachtungszeitraum
                    ende = long(ende) + 1

                anfang = long(startjahr)
                dauer = long(aufsiedlungsdauer)
                jahr = long(startjahr) - 1
                Besch_Jahr = 0
                Besch_Jahr_neu = 0
                row3 = tabelle_beschaeftigte_insert.newRow()
                jahrcount = -1
                jahraufsiedlung = 1
                vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

                for jahr in range(anfang, ende):
                    jahrcount = jahrcount + 1
                    jahr = jahr + 1
                    if jahr < vollaufsiedlung:
                        parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
                        Besch_Jahr = float(anzahl_Besch_max) * float(parameter_jahr)
                        Besch_Jahr = float(Besch_Jahr)
                        Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                        Besch_Jahr_neu = float(Besch_Jahr_neu)
                        jahraufsiedlung = jahraufsiedlung + 1

                    else:
                        Besch_Jahr = float(anzahl_Besch_max)
                        Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                        Besch_Jahr_neu = float(Besch_Jahr_neu)

                    row3.jahr = long(jahrcount) + long(startjahr)
                    row3.Teilflaeche_Plangebiet = teilflaeche
                    row3.Branche = "C"
                    row3.Anzahl = float(Besch_Jahr)
                    row3.Anzahl_neu = float(Besch_Jahr_neu)
                    row3.ID_ts = timestamp
                    tabelle_beschaeftigte_insert.insertRow(row3)


                #Beschaeftigte Branche F / Besch_BauGew
                anzahl_Besch_max = float(Besch_BauGew)
                aufsiedlungsdauer = str(aufsiedlungsdauer)
                tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer)

                rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
                for row in rows_projektrahmen:
                    ende = row.Ende_Betrachtungszeitraum
                    ende = long(ende) + 1

                anfang = long(startjahr)
                dauer = long(aufsiedlungsdauer)
                jahr = long(startjahr) - 1
                Besch_Jahr = 0
                Besch_Jahr_neu = 0
                row3 = tabelle_beschaeftigte_insert.newRow()
                jahrcount = -1
                jahraufsiedlung = 1
                vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

                for jahr in range(anfang, ende):
                    jahrcount = jahrcount + 1
                    jahr = jahr + 1
                    if jahr < vollaufsiedlung:
                        parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
                        Besch_Jahr = float(anzahl_Besch_max) * float(parameter_jahr)
                        Besch_Jahr = float(Besch_Jahr)
                        Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                        Besch_Jahr_neu = float(Besch_Jahr_neu)
                        jahraufsiedlung = jahraufsiedlung + 1

                    else:
                        Besch_Jahr = float(anzahl_Besch_max)
                        Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                        Besch_Jahr_neu = float(Besch_Jahr_neu)

                    row3.jahr = long(jahrcount) + long(startjahr)
                    row3.Teilflaeche_Plangebiet = teilflaeche
                    row3.Branche = "F"
                    row3.Anzahl = float(Besch_Jahr)
                    row3.Anzahl_neu = float(Besch_Jahr_neu)
                    row3.ID_ts = timestamp
                    tabelle_beschaeftigte_insert.insertRow(row3)


                #Beschaeftigte Branche G / Besch_HanKfZ
                anzahl_Besch_max = float(Besch_HanKfZ)
                aufsiedlungsdauer = str(aufsiedlungsdauer)
                tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer)

                rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
                for row in rows_projektrahmen:
                    ende = row.Ende_Betrachtungszeitraum
                    ende = long(ende) + 1

                anfang = long(startjahr)
                dauer = long(aufsiedlungsdauer)
                jahr = long(startjahr) - 1
                Besch_Jahr = 0
                Besch_Jahr_neu = 0
                row3 = tabelle_beschaeftigte_insert.newRow()
                jahrcount = -1
                jahraufsiedlung = 1
                vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

                for jahr in range(anfang, ende):
                    jahrcount = jahrcount + 1
                    jahr = jahr + 1
                    if jahr < vollaufsiedlung:
                        parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
                        Besch_Jahr = float(anzahl_Besch_max) * float(parameter_jahr)
                        Besch_Jahr = float(Besch_Jahr)
                        Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                        Besch_Jahr_neu = float(Besch_Jahr_neu)
                        jahraufsiedlung = jahraufsiedlung + 1

                    else:
                        Besch_Jahr = float(anzahl_Besch_max)
                        Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                        Besch_Jahr_neu = float(Besch_Jahr_neu)

                    row3.jahr = long(jahrcount) + long(startjahr)
                    row3.Teilflaeche_Plangebiet = teilflaeche
                    row3.Branche = "G"
                    row3.Anzahl = float(Besch_Jahr)
                    row3.Anzahl_neu = float(Besch_Jahr_neu)
                    row3.ID_ts = timestamp
                    tabelle_beschaeftigte_insert.insertRow(row3)

                Besch_FrWiTeDi = float(Flaeche_Betr_FrWiTeDi) * float(FKZ_FrWiTeDi)
                Besch_SoDi = float(Flaeche_Betr_SoDi) * float(FKZ_SoDi)
                #Beschaeftigte Branche H / Besch_VerLag
                anzahl_Besch_max = float(Besch_VerLag)
                aufsiedlungsdauer = str(aufsiedlungsdauer)
                tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer)

                rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
                for row in rows_projektrahmen:
                    ende = row.Ende_Betrachtungszeitraum
                    ende = long(ende) + 1

                anfang = long(startjahr)
                dauer = long(aufsiedlungsdauer)
                jahr = long(startjahr) - 1
                Besch_Jahr = 0
                Besch_Jahr_neu = 0
                row3 = tabelle_beschaeftigte_insert.newRow()
                jahrcount = -1
                jahraufsiedlung = 1
                vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

                for jahr in range(anfang, ende):
                    jahrcount = jahrcount + 1
                    jahr = jahr + 1
                    if jahr < vollaufsiedlung:
                        parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
                        Besch_Jahr = float(anzahl_Besch_max) * float(parameter_jahr)
                        Besch_Jahr = float(Besch_Jahr)
                        Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                        Besch_Jahr_neu = float(Besch_Jahr_neu)
                        jahraufsiedlung = jahraufsiedlung + 1

                    else:
                        Besch_Jahr = float(anzahl_Besch_max)
                        Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                        Besch_Jahr_neu = float(Besch_Jahr_neu)

                    row3.jahr = long(jahrcount) + long(startjahr)
                    row3.Teilflaeche_Plangebiet = teilflaeche
                    row3.Branche = "H"
                    row3.Anzahl = float(Besch_Jahr)
                    row3.Anzahl_neu = float(Besch_Jahr_neu)
                    row3.ID_ts = timestamp
                    tabelle_beschaeftigte_insert.insertRow(row3)


                Besch_SoDi = float(Flaeche_Betr_SoDi) * float(FKZ_SoDi)
                #Beschaeftigte Branche M / Besch_FrWiTeDi
                anzahl_Besch_max = float(Besch_FrWiTeDi)
                aufsiedlungsdauer = str(aufsiedlungsdauer)
                tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer)

                rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
                for row in rows_projektrahmen:
                    ende = row.Ende_Betrachtungszeitraum
                    ende = long(ende) + 1

                anfang = long(startjahr)
                dauer = long(aufsiedlungsdauer)
                jahr = long(startjahr) - 1
                Besch_Jahr = 0
                Besch_Jahr_neu = 0
                row3 = tabelle_beschaeftigte_insert.newRow()
                jahrcount = -1
                jahraufsiedlung = 1
                vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

                for jahr in range(anfang, ende):
                    jahrcount = jahrcount + 1
                    jahr = jahr + 1
                    if jahr < vollaufsiedlung:
                        parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
                        Besch_Jahr = float(anzahl_Besch_max) * float(parameter_jahr)
                        Besch_Jahr = float(Besch_Jahr)
                        Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                        Besch_Jahr_neu = float(Besch_Jahr_neu)
                        jahraufsiedlung = jahraufsiedlung + 1

                    else:
                        Besch_Jahr = float(anzahl_Besch_max)
                        Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                        Besch_Jahr_neu = float(Besch_Jahr_neu)

                    row3.jahr = long(jahrcount) + long(startjahr)
                    row3.Teilflaeche_Plangebiet = teilflaeche
                    row3.Branche = "M"
                    row3.Anzahl = float(Besch_Jahr)
                    row3.Anzahl_neu = float(Besch_Jahr_neu)
                    row3.ID_ts = timestamp
                    tabelle_beschaeftigte_insert.insertRow(row3)


                #Beschaeftigte Branche N / Besch_SoDi
                anzahl_Besch_max = float(Besch_SoDi)
                aufsiedlungsdauer = str(aufsiedlungsdauer)
                tabelle_parameter_aufsiedlungsdauer_Search = arcpy.SearchCursor(tabelle_parameter_aufsiedlungsdauer)

                rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
                for row in rows_projektrahmen:
                    ende = row.Ende_Betrachtungszeitraum
                    ende = long(ende) + 1

                anfang = long(startjahr)
                dauer = long(aufsiedlungsdauer)
                jahr = long(startjahr) - 1
                Besch_Jahr = 0
                Besch_Jahr_neu = 0
                row3 = tabelle_beschaeftigte_insert.newRow()
                jahrcount = -1
                jahraufsiedlung = 1
                vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

                for jahr in range(anfang, ende):
                    jahrcount = jahrcount + 1
                    jahr = jahr + 1
                    if jahr < vollaufsiedlung:
                        parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
                        Besch_Jahr = float(anzahl_Besch_max) * float(parameter_jahr)
                        Besch_Jahr = float(Besch_Jahr)
                        Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                        Besch_Jahr_neu = float(Besch_Jahr_neu)
                        jahraufsiedlung = jahraufsiedlung + 1

                    else:
                        Besch_Jahr = float(anzahl_Besch_max)
                        Besch_Jahr_neu = float(Besch_Jahr) * float(zuzugsquote) / 100
                        Besch_Jahr_neu = float(Besch_Jahr_neu)

                    row3.jahr = long(jahrcount) + long(startjahr)
                    row3.Teilflaeche_Plangebiet = teilflaeche
                    row3.Branche = "N"
                    row3.Anzahl = float(Besch_Jahr)
                    row3.Anzahl_neu = float(Besch_Jahr_neu)
                    row3.ID_ts = timestamp
                    tabelle_beschaeftigte_insert.insertRow(row3)

                ##############################
                ## Gebaeude berechnen

                schrittmeldung = 'Gebaeudedaten werden berechnet \n'
                messages.AddMessage(schrittmeldung)
                print str(schrittmeldung)

                tabelle_gebaeudegrundlagen = self.folders.get_base_table('FGDB_Definition_Projekt_Tool.gdb','gewerbe_gebaeude')
                tabelle_gebaeudedetails = self.folders.get_table('Gebaeude_Details')
                tabelle_gebaeudedetails_insert = arcpy.InsertCursor(tabelle_gebaeudedetails)

                rows_GGF = arcpy.SearchCursor(tabelle_gebaeudegrundlagen)
                GGF_halle = 0
                GGF_verwaltung = 0
                GeVo_halle = 0
                GeVo_verwlatung = 0

                for row in rows_GGF:
                    if row.Branche == "C":
                        GGF_halle_VerarbGew = float(row.anteil_halle) * float(Flaeche_Betr_VerarbGew)
                        GGF_verwaltung_VerarbGew = float(row.anteil_verwaltung) * float(Flaeche_Betr_VerarbGew)
                        GeVo_halle_VerarbGew = float(GGF_halle_VerarbGew) * float(row.hoehe_halle)
                        GeVo_verwaltung_VerarbGew = float(GGF_verwaltung_VerarbGew) * float(row.hoehe_verwaltung)
                        GGF_halle = float(GGF_halle) + float(GGF_halle_VerarbGew)
                        GGF_verwaltung = float(GGF_verwaltung) + float(GGF_verwaltung_VerarbGew)
                        GeVo_halle = float(GeVo_halle) + float(GeVo_halle_VerarbGew)
                        GeVo_verwlatung = float(GeVo_verwlatung) + float(GeVo_verwaltung_VerarbGew)
                    if row.Branche == "F":
                        GGF_halle_BauGew = float(row.anteil_halle) * float(Flaeche_Betr_BauGew)
                        GGF_verwaltung_BauGew = float(row.anteil_verwaltung) * float(Flaeche_Betr_BauGew)
                        GeVo_halle_BauGew = float(GGF_halle_BauGew) * float(row.hoehe_halle)
                        GeVo_verwaltung_BauGew = float(GGF_verwaltung_BauGew) * float(row.hoehe_verwaltung)
                        GGF_halle = float(GGF_halle) + float(GGF_halle_BauGew)
                        GGF_verwaltung = float(GGF_verwaltung) + float(GGF_verwaltung_BauGew)
                        GeVo_halle = float(GeVo_halle) + float(GeVo_halle_BauGew)
                        GeVo_verwlatung = float(GeVo_verwlatung) + float(GeVo_verwaltung_BauGew)
                    if row.Branche == "G":
                        GGF_halle_HanKfZ = float(row.anteil_halle) * float(Flaeche_Betr_HanKfZ)
                        GGF_verwaltung_HanKfZ = float(row.anteil_verwaltung) * float(Flaeche_Betr_HanKfZ)
                        GeVo_halle_HanKfZ = float(GGF_halle_HanKfZ) * float(row.hoehe_halle)
                        GeVo_verwaltung_HanKfZ = float(GGF_verwaltung_HanKfZ) * float(row.hoehe_verwaltung)
                        GGF_halle = float(GGF_halle) + float(GGF_halle_HanKfZ)
                        GGF_verwaltung = float(GGF_verwaltung) + float(GGF_verwaltung_HanKfZ)
                        GeVo_halle = float(GeVo_halle) + float(GeVo_halle_HanKfZ)
                        GeVo_verwlatung = float(GeVo_verwlatung) + float(GeVo_verwaltung_HanKfZ)
                    if row.Branche == "H":
                        GGF_halle_VerLag = float(row.anteil_halle) * float(Flaeche_Betr_VerLag)
                        GGF_verwaltung_VerLag = float(row.anteil_verwaltung) * float(Flaeche_Betr_VerLag)
                        GeVo_halle_VerLag = float(GGF_halle_VerLag) * float(row.hoehe_halle)
                        GeVo_verwaltung_VerLag = float(GGF_verwaltung_VerLag) * float(row.hoehe_verwaltung)
                        GGF_halle = float(GGF_halle) + float(GGF_halle_VerLag)
                        GGF_verwaltung = float(GGF_verwaltung) + float(GGF_verwaltung_VerLag)
                        GeVo_halle = float(GeVo_halle) + float(GeVo_halle_VerLag)
                        GeVo_verwlatung = float(GeVo_verwlatung) + float(GeVo_verwaltung_VerLag)
                    if row.Branche == "M":
                        GGF_halle_FrWiTeDi = float(row.anteil_halle) * float(Flaeche_Betr_FrWiTeDi)
                        GGF_verwaltung_FrWiTeDi = float(row.anteil_verwaltung) * float(Flaeche_Betr_FrWiTeDi)
                        GeVo_halle_FrWiTeDi = float(GGF_halle_FrWiTeDi) * float(row.hoehe_halle)
                        GeVo_verwaltung_FrWiTeDi = float(GGF_verwaltung_FrWiTeDi) * float(row.hoehe_verwaltung)
                        GGF_halle = float(GGF_halle) + float(GGF_halle_FrWiTeDi)
                        GGF_verwaltung = float(GGF_verwaltung) + float(GGF_verwaltung_FrWiTeDi)
                        GeVo_halle = float(GeVo_halle) + float(GeVo_halle_FrWiTeDi)
                        GeVo_verwlatung = float(GeVo_verwlatung) + float(GeVo_verwaltung_FrWiTeDi)
                    if row.Branche == "N":
                        GGF_halle_SoDi = float(row.anteil_halle) * float(Flaeche_Betr_SoDi)
                        GGF_verwaltung_SoDi = float(row.anteil_verwaltung) * float(Flaeche_Betr_SoDi)
                        GeVo_halle_SoDi = float(GGF_halle_SoDi) * float(row.hoehe_halle)
                        GeVo_verwaltung_SoDi = float(GGF_verwaltung_SoDi) * float(row.hoehe_verwaltung)
                        GGF_halle = float(GGF_halle) + float(GGF_halle_SoDi)
                        GGF_verwaltung = float(GGF_verwaltung) + float(GGF_verwaltung_SoDi)
                        GeVo_halle = float(GeVo_halle) + float(GeVo_halle_SoDi)
                        GeVo_verwlatung = float(GeVo_verwlatung) + float(GeVo_verwaltung_SoDi)


                ## Gebaeude für Hallen nach Aufsiedlugnszeit berechnen
                aufsiedlungsdauer = str(aufsiedlungsdauer)
                rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
                for row in rows_projektrahmen:
                    ende = row.Ende_Betrachtungszeitraum
                    ende = long(ende) + 1

                anfang = long(startjahr)
                dauer = long(aufsiedlungsdauer)
                jahr = long(startjahr) - 1
                GGF_jahr = 0
                GeVo_jahr = 0
                grundstuecksflaeche_jahr = 0

                rowGeb = tabelle_gebaeudedetails_insert.newRow()
                jahrcount = -1
                jahraufsiedlung = 1
                vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

                for jahr in range(anfang, ende):
                    jahrcount = jahrcount + 1
                    jahr = jahr + 1
                    if jahr < vollaufsiedlung:
                        parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
                        GGF_jahr = float(GGF_halle) * float(parameter_jahr) * 10000
                        GeVo_jahr = float(GeVo_halle) * float(parameter_jahr) * 10000
                        grundstuecksflaeche_jahr = float(gewerbebauland) * float(parameter_jahr) * 10000
                        jahraufsiedlung = jahraufsiedlung + 1
                    else:
                        GGF_jahr = float(GGF_halle) * 10000
                        GeVo_jahr = float(GeVo_halle) * 10000
                        grundstuecksflaeche_jahr = float(gewerbebauland) * 10000

                    rowGeb.jahr = long(jahrcount) + long(startjahr)
                    rowGeb.Teilflaeche_Plangebiet = teilflaeche
                    rowGeb.Gebaeudetyp = "Hallen"
                    rowGeb.Grundstuecksflaeche_qm = float(grundstuecksflaeche_jahr)
                    rowGeb.Ueberbaute_Flaeche = float(GGF_jahr)
                    rowGeb.Bruttorauminhalt_m3 = float(GeVo_jahr)
                    rowGeb.Geb_ID = timestamp

                    tabelle_gebaeudedetails_insert.insertRow(rowGeb)

                ## Gebaeude für Bürogebaude nach Aufsiedlugnszeit berechnen
                aufsiedlungsdauer = str(aufsiedlungsdauer)
                rows_projektrahmen = arcpy.SearchCursor(tabelle_projektrahmendaten)
                for row in rows_projektrahmen:
                    ende = row.Ende_Betrachtungszeitraum
                    ende = long(ende) + 1

                anfang = long(startjahr)
                dauer = long(aufsiedlungsdauer)
                jahr = long(startjahr) - 1
                GGF_jahr = 0
                GeVo_jahr = 0
                grundstuecksflaeche_jahr = 0


                rowGeb = tabelle_gebaeudedetails_insert.newRow()
                jahrcount = -1
                jahraufsiedlung = 1
                vollaufsiedlung = long(startjahr) + long(aufsiedlungsdauer)

                for jahr in range(anfang, ende):
                    jahrcount = jahrcount + 1
                    jahr = jahr + 1
                    if jahr < vollaufsiedlung:
                        parameter_jahr = float(jahraufsiedlung) / float(aufsiedlungsdauer)
                        GGF_jahr = float(GGF_verwaltung) * float(parameter_jahr) * 10000
                        GeVo_jahr = float(GeVo_verwlatung) * float(parameter_jahr) * 10000
                        grundstuecksflaeche_jahr = float(gewerbebauland) * float(parameter_jahr) * 10000
                        jahraufsiedlung = jahraufsiedlung + 1
                    else:
                        GGF_jahr = float(GGF_verwaltung) * 10000
                        GeVo_jahr = float(GeVo_verwlatung) * 10000
                        grundstuecksflaeche_jahr = float(gewerbebauland) * 10000

                    rowGeb.jahr = long(jahrcount) + long(startjahr)
                    rowGeb.Teilflaeche_Plangebiet = teilflaeche
                    rowGeb.Gebaeudetyp = "Buerogebaeude"
                    rowGeb.Grundstuecksflaeche_qm = float(grundstuecksflaeche_jahr)
                    rowGeb.Ueberbaute_Flaeche = float(GGF_jahr)
                    rowGeb.Bruttorauminhalt_m3 = float(GeVo_jahr)
                    rowGeb.Geb_ID = timestamp

                    tabelle_gebaeudedetails_insert.insertRow(rowGeb)

                ###############################
                ## Tabelle Gewerbe_teilflaechen fuellen

                schrittmeldung = 'Projektinformationen werden zusammengefasst und in Datenbank geschrieben \n'
                messages.AddMessage(schrittmeldung)
                print str(schrittmeldung)

                tabelle_teilflaeche = self.folders.get_table('Gewerbe_Teilflaechen')
                tabelle_teilflaeche_insert = arcpy.InsertCursor(tabelle_teilflaeche)
                rowTF = tabelle_teilflaeche_insert.newRow()

                # Zeile für Branche C / VerarbGew
                rowTF.teilflaeche = teilflaeche
                rowTF.gebietstyp = str(gebtyp)
                rowTF.branche = "C"
                rowTF.aufsiedlungsdauer = long(aufsiedlungsdauer)
                rowTF.zuzugsquote = long(zuzugsquote)
                rowTF.nettobauland = float(gewerbebauland)
                rowTF.bruttoflaeche = float(flaechengroesse)
                rowTF.beschaeftigte = float(Besch_VerarbGew)
                rowTF.anzahlBetriebe = int(Anz_Betr_VerarbGew)
                rowTF.timestamp = timestamp

                tabelle_teilflaeche_insert.insertRow(rowTF)

                # Zeile für Branche F / BauGew
                rowTF.teilflaeche = teilflaeche
                rowTF.gebietstyp = str(gebtyp)
                rowTF.branche = "F"
                rowTF.aufsiedlungsdauer = long(aufsiedlungsdauer)
                rowTF.zuzugsquote = long(zuzugsquote)
                rowTF.nettobauland = float(gewerbebauland)
                rowTF.bruttoflaeche = float(flaechengroesse)
                rowTF.beschaeftigte = float(Besch_BauGew)
                rowTF.anzahlBetriebe = int(Anz_Betr_BauGew)
                rowTF.timestamp = timestamp

                tabelle_teilflaeche_insert.insertRow(rowTF)

                # Zeile für Branche G / HanKfZ
                rowTF.teilflaeche = teilflaeche
                rowTF.gebietstyp = str(gebtyp)
                rowTF.branche = "G"
                rowTF.aufsiedlungsdauer = long(aufsiedlungsdauer)
                rowTF.zuzugsquote = long(zuzugsquote)
                rowTF.nettobauland = float(gewerbebauland)
                rowTF.bruttoflaeche = float(flaechengroesse)
                rowTF.beschaeftigte = float(Besch_HanKfZ)
                rowTF.anzahlBetriebe = int(Anz_Betr_HanKfZ)
                rowTF.timestamp = timestamp

                tabelle_teilflaeche_insert.insertRow(rowTF)

                # Zeile für Branche H / VerLag
                rowTF.teilflaeche = teilflaeche
                rowTF.gebietstyp = str(gebtyp)
                rowTF.branche = "H"
                rowTF.aufsiedlungsdauer = long(aufsiedlungsdauer)
                rowTF.zuzugsquote = long(zuzugsquote)
                rowTF.nettobauland = float(gewerbebauland)
                rowTF.bruttoflaeche = float(flaechengroesse)
                rowTF.beschaeftigte = float(Besch_VerLag)
                rowTF.anzahlBetriebe = int(Anz_Betr_VerLag)
                rowTF.timestamp = timestamp

                tabelle_teilflaeche_insert.insertRow(rowTF)

                # Zeile für Branche M / FrWiTeDi
                rowTF.teilflaeche = teilflaeche
                rowTF.gebietstyp = str(gebtyp)
                rowTF.branche = "M"
                rowTF.aufsiedlungsdauer = long(aufsiedlungsdauer)
                rowTF.zuzugsquote = long(zuzugsquote)
                rowTF.nettobauland = float(gewerbebauland)
                rowTF.bruttoflaeche = float(flaechengroesse)
                rowTF.beschaeftigte = float(Besch_FrWiTeDi)
                rowTF.anzahlBetriebe = int(Anz_Betr_FrWiTeDi)
                rowTF.timestamp = timestamp

                tabelle_teilflaeche_insert.insertRow(rowTF)

                # Zeile für Branche N / SoDi
                rowTF.teilflaeche = teilflaeche
                rowTF.gebietstyp = str(gebtyp)
                rowTF.branche = "N"
                rowTF.aufsiedlungsdauer = long(aufsiedlungsdauer)
                rowTF.zuzugsquote = long(zuzugsquote)
                rowTF.nettobauland = float(gewerbebauland)
                rowTF.bruttoflaeche = float(flaechengroesse)
                rowTF.beschaeftigte = float(Besch_SoDi)
                rowTF.anzahlBetriebe = int(Anz_Betr_SoDi)
                rowTF.timestamp = timestamp

                tabelle_teilflaeche_insert.insertRow(rowTF)


                beschaeftigte_gewerbe(projektname)
                schrittmeldung = 'Die Berechnungen sind abgeschlossen  \n'
                messages.AddMessage(schrittmeldung)
                print str(schrittmeldung)










            ##########################################################################
            ##########################################################################
            ##########################################################################
            ##########################################################################
            ##########################################################################
            ## Ergebnisausgabe
                schrittmeldung = 'Die Ergebnisausgabe wird erzeugt. Dies kann wenige Minuten in Anspruch nehmen. \n'
                messages.AddMessage(schrittmeldung)
                print str(schrittmeldung)

                # Pfade setzen
                base_path = str(sys.path[0]).split("2_Tool")[0]
                workspace_projekt_gewerbe = join(self.folders.get_projectpath(), 'FGDB_Definition_Projekt.gdb')
                tablepath_gewerbe = join(workspace_projekt_gewerbe,'Gewerbe_Teilflaechen')
                tablepath_Beschaeftigte = join(workspace_projekt_gewerbe,'Gewerbe_Beschaeftigte')
                tablepath_Flaechenbilanz = join(workspace_projekt_gewerbe,'Flaechenbilanz')
                tablepath_Gebaeude = join(workspace_projekt_gewerbe,'Gebaeude_Details')
                tablepath_Betriebe = join(workspace_projekt_gewerbe,'Gewerbe_Betriebsstruktur')
                grafikpath_erlauterungstext = self.folders.get_base_table(u'Erläuterungstexte')

                logo = join(grafikpath_erlauterungstext, "logo_rpc.png")
                ausgabeordner = join(self.folders.get_projectpath(), 'Ergebnisausgabe','Excel')
                excelpfad = join(ausgabeordner,'11_Projektdefinition_Gewerbe.xlsx')

                try:
                    os.remove(excelpfad)
                except:
                    pass

                # Workbook und Tabellenblätter anlegen
                wb = xlsxwriter.Workbook(excelpfad)
                sl.infosheet(projektname, str("Projektinformation").decode('utf-8'), wb)
                ws2 = wb.add_worksheet('Erlaeuterungen')
                ws3 = wb.add_worksheet('Tabellen')
                ws4 = wb.add_worksheet('Grafiken')
                ws4_1 = wb.add_worksheet('Art der Arbeitsplaetze')
                ws5 = wb.add_worksheet('Rohdaten')

                ##Styles anlegen
                bold = wb.add_format({'bold': True})
                bold.set_align('vtop')
                bold.set_bg_color('white')
                bold.set_border(0)

                wrap = wb.add_format()
                wrap.set_text_wrap()
                wrap.set_align('vtop')
                wrap.set_bg_color('white')
                wrap.set_border(0)

                normal = wb.add_format()
                normal.set_bg_color('white')
                normal.set_border(0)

                formatDez = wb.add_format()
                formatDez.set_num_format(0x02)
                formatDez.set_bg_color('white')
                formatDez.set_border(0)

                formatDez1 = wb.add_format()
                formatDez1.set_num_format(0x01)
                formatDez1.set_bg_color('white')
                formatDez1.set_border(0)

                ###Hintergrund weiss faerben
                format = wb.add_format()
                format.set_bg_color('white')
                format.set_border(0)


                for x in range(0,200):
                    for y in range(0,200):
                        ws2.write(x,y,"", format)
                        ws3.write(x,y,"", format)
                        ws4.write(x,y,"", format)

                        ws4_1.write(x,y,"", format)

                        ws5.write(x,y,"", format)

                ###Spaltenbreiten definieren
                ws2.set_column(0, 0, 86)
                for x in range(0,200):
                    ws3.set_column(x, 0, 10)
                ws4.set_column(0, 0, 75)

                ### ToDo: Für Überschriften im Tabellenblatt noch Zellen zusammenfügen und grau einfärben

                ########
                ## Erläuterungstexte einfügen
                # Pfade zu Grafiken herstellen und einfügen
                Erlaeuterung = join(grafikpath_erlauterungstext, 'Gewerbe.png')
                # ws2.insert_image(0, 0, Erlaeuterung, {'x_scale': 0.32, 'y_scale': 0.32})

                ###### Tabellenblatt 5: Rohdaten einladen
                ## Rohdaten tablepath_gewerbe
                #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
                rows = arcpy.SearchCursor(tablepath_gewerbe)
                #Feldnamen auslesen
                fieldnames = [f.name for f in arcpy.ListFields(tablepath_gewerbe)]

                j = 1
                for row in rows:
                    i = 0
                    for fieldname in fieldnames:
                        try:
                            wert = string(row.getValue(fieldname))
                        except:
                            wert = row.getValue(fieldname)
                        ws5.write(j, i, wert,formatDez)
                        i = i+1

                    j = j+1


                #Felder als Header in Worksheet einfuegen
                i = 0
                for fieldname in fieldnames:
                    column_with = len(fieldname)+2
                    ws5.set_column(i, i, column_with)
                    ws5.write(0, i, fieldname, bold)
                    i = i+1


                ## Rohdaten tablepath_Beschaeftigte
                #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
                rows = arcpy.SearchCursor(tablepath_Beschaeftigte)
                #Feldnamen auslesen
                fieldnames = [f.name for f in arcpy.ListFields(tablepath_Beschaeftigte)]

                irestart = i + 2

                j = 1
                for row in rows:
                    i = irestart
                    for fieldname in fieldnames:
                        try:
                            wert = string(row.getValue(fieldname))
                        except:
                            wert = row.getValue(fieldname)
                        ws5.write(j, i, wert,formatDez)
                        i = i+1

                    j = j+1

                #Felder als Header in Worksheet einfuegen
                i = irestart
                for fieldname in fieldnames:
                    column_with = len(fieldname)+2
                    ws5.set_column(i, i, column_with)
                    ws5.write(0, i, fieldname, bold)
                    i = i+1


                ## Rohdaten tablepath_Flaechenbilanz
                #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
                rows = arcpy.SearchCursor(tablepath_Flaechenbilanz)
                #Feldnamen auslesen
                fieldnames = [f.name for f in arcpy.ListFields(tablepath_Flaechenbilanz)]

                irestart = i + 2

                j = 1
                for row in rows:
                    i = irestart
                    for fieldname in fieldnames:
                        try:
                            wert = string(row.getValue(fieldname))
                        except:
                            wert = row.getValue(fieldname)
                        ws5.write(j, i, wert,formatDez)
                        i = i+1

                    j = j+1

                #Felder als Header in Worksheet einfuegen
                i = irestart
                for fieldname in fieldnames:
                    column_with = len(fieldname)+2
                    ws5.set_column(i, i, column_with)
                    ws5.write(0, i, fieldname, bold)
                    i = i+1


                ## Rohdaten tablepath_Gebaeude
                #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
                rows = arcpy.SearchCursor(tablepath_Gebaeude)
                #Feldnamen auslesen
                fieldnames = [f.name for f in arcpy.ListFields(tablepath_Gebaeude)]

                irestart = i + 2

                j = 1
                for row in rows:
                    i = irestart
                    for fieldname in fieldnames:
                        try:
                            wert = string(row.getValue(fieldname))
                        except:
                            wert = row.getValue(fieldname)
                        ws5.write(j, i, wert,formatDez)
                        i = i+1

                    j = j+1

                #Felder als Header in Worksheet einfuegen
                i = irestart
                for fieldname in fieldnames:
                    column_with = len(fieldname)+2
                    ws5.set_column(i, i, column_with)
                    ws5.write(0, i, fieldname, bold)
                    i = i+1



                ## Rohdaten tablepath_Betriebe
                #Durch Ergebniszeilen iterieren und Werte in Excel einfuegen
                rows = arcpy.SearchCursor(tablepath_Betriebe)
                #Feldnamen auslesen
                fieldnames = [f.name for f in arcpy.ListFields(tablepath_Betriebe)]

                irestart = i + 2

                j = 1
                for row in rows:
                    i = irestart
                    for fieldname in fieldnames:
                        try:
                            wert = string(row.getValue(fieldname))
                        except:
                            wert = row.getValue(fieldname)
                        ws5.write(j, i, wert,formatDez)
                        i = i+1

                    j = j+1

                #Felder als Header in Worksheet einfuegen
                i = irestart
                for fieldname in fieldnames:
                    column_with = len(fieldname)+2
                    ws5.set_column(i, i, column_with)
                    ws5.write(0, i, fieldname, bold)
                    i = i+1


                ###### Tabellenblatt 3: Tabellen erstellen
                ## Tabelle Projektuebersicht
                j = 0
                i = 0
                ws3.write(j, i, 'Projektuebersicht', bold)
                j = j + 1
                ws3.write(j, i, 'Teilflaeche', bold)
                i = i + 1
                ws3.write(j, i, 'Gebietstyp', bold)
                i = i + 1
                ws3.write(j, i, 'Aufsiedlungsdauer [Jahre]', bold)
                i = i + 1
                ws3.write(j, i, 'Zuzugsquote [%]', bold)
                i = i + 1
                ws3.write(j, i, 'Nettobauland [Hektar]', bold)
                i = i + 1
                ws3.write(j, i, 'Bruttobauland [Hektar]', bold)
                i = i + 1
                ws3.write(j, i, 'Beschaeftigte', bold)
                i = i + 1
                ws3.write(j, i, 'Betriebe', bold)
                i = i + 1
                ws3.write(j, i, 'Branche', bold)
                j = j + 1
                i = 0
                for x in range(2,8):
                    cell = xl_rowcol_to_cell(j-1,i+1)
                    ws3.write(j, i, '=Rohdaten!'+cell+'', normal)
                    i = i + 1
                    cell = xl_rowcol_to_cell(j-1,i+1)
                    ws3.write(j, i, '=Rohdaten!'+cell+'', normal)
                    i = i + 1
                    cell = xl_rowcol_to_cell(j-1,i+1)
                    ws3.write(j, i, '=Rohdaten!'+cell+'', formatDez1)
                    i = i + 1
                    cell = xl_rowcol_to_cell(j-1,i+1)
                    ws3.write(j, i, '=Rohdaten!'+cell+'', formatDez1)
                    i = i + 1
                    cell = xl_rowcol_to_cell(j-1,i+1)
                    ws3.write(j, i, '=Rohdaten!'+cell+'', formatDez)
                    i = i + 1
                    cell = xl_rowcol_to_cell(j-1,i+1)
                    ws3.write(j, i, '=Rohdaten!'+cell+'', formatDez)
                    i = i + 1
                    cell = xl_rowcol_to_cell(j-1,i+1)
                    ws3.write(j, i, '=Rohdaten!'+cell+'', formatDez1)
                    i = i + 1
                    cell = xl_rowcol_to_cell(j-1,i+1)
                    ws3.write(j, i, '=Rohdaten!'+cell+'', formatDez)
                    i = i + 1
                    cell = xl_rowcol_to_cell(j-1,i+1)
                    ws3.write(j, i, '=Rohdaten!'+cell+'', normal)
                    i = 0
                    j = j + 1

                ## Tabelle Beschäftigte
                j = j + 2
                i = 0
                ws3.write(j, i, 'Beschaeftigte', bold)
                j = j + 1
                ws3.write(j, i, 'Branche', bold)
                i = i + 1
                ws3.write(j, i, '=MIN(Rohdaten!O:O)', bold)
                for x in range(2, 32):
                    i = i + 1
                    jahrcell = xl_rowcol_to_cell(j,i-1)
                    ws3.write(j, i, '='+jahrcell+'+1', bold)
                j = j + 1
                i = 1
                ws3.write(j, 0, 'C', normal)
                zellebranche = xl_rowcol_to_cell(j,0)
                zeilejahr = j - 1
                for x in range(2, 33):
                    spaltejahr = x - 1
                    jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                    ws3.write(j, i, '=SUMIFS(Rohdaten!$R:$R,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                    i = i + 1
                j = j + 1
                i = 1
                ws3.write(j, 0, 'F', normal)
                zellebranche = xl_rowcol_to_cell(j,0)
                for x in range(2, 33):
                    spaltejahr = x - 1
                    jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                    ws3.write(j, i, '=SUMIFS(Rohdaten!$R:$R,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                    i = i + 1
                j = j + 1
                i = 1
                ws3.write(j, 0, 'G', normal)
                zellebranche = xl_rowcol_to_cell(j,0)
                for x in range(2, 33):
                    spaltejahr = x - 1
                    jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                    ws3.write(j, i, '=SUMIFS(Rohdaten!$R:$R,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                    i = i + 1
                j = j + 1
                i = 1
                ws3.write(j, 0, 'H', normal)
                zellebranche = xl_rowcol_to_cell(j,0)
                for x in range(2, 33):
                    spaltejahr = x - 1
                    jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                    ws3.write(j, i, '=SUMIFS(Rohdaten!$R:$R,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                    i = i + 1
                j = j + 1
                i = 1
                ws3.write(j, 0, 'M', normal)
                zellebranche = xl_rowcol_to_cell(j,0)
                for x in range(2, 33):
                    spaltejahr = x - 1
                    jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                    ws3.write(j, i, '=SUMIFS(Rohdaten!$R:$R,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                    i = i + 1
                j = j + 1
                i = 1
                ws3.write(j, 0, 'N', normal)
                zellebranche = xl_rowcol_to_cell(j,0)
                for x in range(2, 33):
                    spaltejahr = x - 1
                    jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                    ws3.write(j, i, '=SUMIFS(Rohdaten!$R:$R,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                    i = i + 1
                j = j + 1


                ## Tabelle Neue Beschaeftigte
                j = j + 2
                i = 0
                ws3.write(j, i, 'Neue Beschaeftigte', bold)
                j = j + 1
                ws3.write(j, i, 'Branche', bold)
                i = i + 1
                jahrcellbetrieb = xl_rowcol_to_cell(j,i)
                ws3.write(j, i, '=MIN(Rohdaten!O:O)', bold)
                i = 1
                for x in range(2, 32):
                    i = i + 1
                    jahrcell = xl_rowcol_to_cell(j,i-1)
                    ws3.write(j, i, '='+jahrcell+'+1', bold)
                j = j + 1
                i = 1
                ws3.write(j, 0, 'C', normal)
                zellebranche = xl_rowcol_to_cell(j,0)
                zeilejahr = j - 1
                for x in range(2, 33):
                    spaltejahr = x - 1
                    jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                    ws3.write(j, i, '=SUMIFS(Rohdaten!$S:$S,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                    i = i + 1
                j = j + 1
                i = 1
                ws3.write(j, 0, 'F', normal)
                zellebranche = xl_rowcol_to_cell(j,0)
                for x in range(2, 32):
                    spaltejahr = x - 1
                    jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                    ws3.write(j, i, '=SUMIFS(Rohdaten!$S:$S,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                    i = i + 1
                j = j + 1
                i = 1
                ws3.write(j, 0, 'G', normal)
                zellebranche = xl_rowcol_to_cell(j,0)
                for x in range(2, 33):
                    spaltejahr = x - 1
                    jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                    ws3.write(j, i, '=SUMIFS(Rohdaten!$S:$S,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                    i = i + 1
                j = j + 1
                i = 1
                ws3.write(j, 0, 'H', normal)
                zellebranche = xl_rowcol_to_cell(j,0)
                for x in range(2, 33):
                    spaltejahr = x - 1
                    jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                    ws3.write(j, i, '=SUMIFS(Rohdaten!$S:$S,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                    i = i + 1
                j = j + 1
                i = 1
                ws3.write(j, 0, 'M', normal)
                zellebranche = xl_rowcol_to_cell(j,0)
                for x in range(2, 33):
                    spaltejahr = x - 1
                    jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                    ws3.write(j, i, '=SUMIFS(Rohdaten!$S:$S,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                    i = i + 1
                j = j + 1
                i = 1
                ws3.write(j, 0, 'N', normal)
                zellebranche = xl_rowcol_to_cell(j,0)
                for x in range(2, 33):
                    spaltejahr = x - 1
                    jahrcell = xl_rowcol_to_cell(zeilejahr,spaltejahr)
                    ws3.write(j, i, '=SUMIFS(Rohdaten!$S:$S,Rohdaten!$Q:$Q,Tabellen!'+zellebranche+',Rohdaten!$O:$O,Tabellen!'+jahrcell+')', formatDez1)
                    i = i + 1
                j = j + 1


                ## Tabelle Betriebe
                j = j + 2
                i = 0
                ws3.write(j, i, 'Betriebe', bold)
                j = j + 1
                ws3.write(j, i, 'Branche', bold)
                i = i + 1
                ws3.write(j, i, '='+jahrcellbetrieb+'', bold)
                i = 1
                for x in range(2, 32):
                    i = i + 1
                    jahrcell = xl_rowcol_to_cell(j,i-1)
                    ws3.write(j, i, '='+jahrcell+'+1', bold)
                bracol = xl_col_to_name(46)
                colcount = 46
                jahrcol = xl_col_to_name(colcount)
                j = j + 1
                i = 1

                ws3.write(j, 0, 'C', normal)
                zellebranche = xl_rowcol_to_cell(j,0)
                for x in range(2, 33):
                    colcount = colcount + 1
                    jahrcol = xl_col_to_name(colcount)
                    spaltejahr = x - 1
                    ws3.write(j, i, '=SUMIF(Rohdaten!'+bracol+':'+bracol+',Tabellen!'+zellebranche+',Rohdaten!'+jahrcol+':'+jahrcol+')', formatDez)
                    i = i + 1
                j = j + 1
                i = 1

                ws3.write(j, 0, 'F', normal)
                zellebranche = xl_rowcol_to_cell(j,0)
                colcount = 46
                for x in range(2, 33):
                    colcount = colcount + 1
                    jahrcol = xl_col_to_name(colcount)
                    spaltejahr = x - 1
                    ws3.write(j, i, '=SUMIF(Rohdaten!'+bracol+':'+bracol+',Tabellen!'+zellebranche+',Rohdaten!'+jahrcol+':'+jahrcol+')', formatDez)
                    i = i + 1
                j = j + 1
                i = 1

                ws3.write(j, 0, 'G', normal)
                zellebranche = xl_rowcol_to_cell(j,0)
                colcount = 46
                for x in range(2, 33):
                    colcount = colcount + 1
                    jahrcol = xl_col_to_name(colcount)
                    spaltejahr = x - 1
                    ws3.write(j, i, '=SUMIF(Rohdaten!'+bracol+':'+bracol+',Tabellen!'+zellebranche+',Rohdaten!'+jahrcol+':'+jahrcol+')', formatDez)
                    i = i + 1
                j = j + 1
                i = 1

                ws3.write(j, 0, 'H', normal)
                zellebranche = xl_rowcol_to_cell(j,0)
                colcount = 46
                for x in range(2, 33):
                    colcount = colcount + 1
                    jahrcol = xl_col_to_name(colcount)
                    spaltejahr = x - 1
                    ws3.write(j, i, '=SUMIF(Rohdaten!'+bracol+':'+bracol+',Tabellen!'+zellebranche+',Rohdaten!'+jahrcol+':'+jahrcol+')', formatDez)
                    i = i + 1
                j = j + 1
                i = 1

                ws3.write(j, 0, 'M', normal)
                zellebranche = xl_rowcol_to_cell(j,0)
                colcount = 46
                for x in range(2, 33):
                    colcount = colcount + 1
                    jahrcol = xl_col_to_name(colcount)
                    spaltejahr = x - 1
                    ws3.write(j, i, '=SUMIF(Rohdaten!'+bracol+':'+bracol+',Tabellen!'+zellebranche+',Rohdaten!'+jahrcol+':'+jahrcol+')', formatDez)
                    i = i + 1
                j = j + 1
                i = 1

                ws3.write(j, 0, 'N', normal)
                zellebranche = xl_rowcol_to_cell(j,0)
                colcount = 46
                for x in range(2, 33):
                    colcount = colcount + 1
                    jahrcol = xl_col_to_name(colcount)
                    spaltejahr = x - 1
                    ws3.write(j, i, '=SUMIF(Rohdaten!'+bracol+':'+bracol+',Tabellen!'+zellebranche+',Rohdaten!'+jahrcol+':'+jahrcol+')', formatDez)
                    i = i + 1
                j = j + 1
                i = 1

            ###### Charts anlegen
                # Chart Branchenstruktur anlegen
                chart_Branchenstruktur = wb.add_chart({'type': 'bar', 'subtype': 'percent_stacked'})
                chart_Branchenstruktur.set_style(40)
                chart_Branchenstruktur.set_size({'width': 529, 'height': 226})
                chart_Branchenstruktur.set_chartarea({'border': {'none': True},'fill': {'none': True}})
                chart_Branchenstruktur.set_legend({'position': 'right'})
                chart_Branchenstruktur.set_title({'name': 'Branchenstruktur','name_font':  {'name': 'Calibri', 'size': 12}})

                # Werte in Chartobjekte schreiben
                chart_Branchenstruktur.add_series({
                    'values': "=Tabellen!$G$3:$H$3",
                    'categories': "=Tabellen!$G$2:$H$2",
                    'name': "=Tabellen!$I$3",
                })
                chart_Branchenstruktur.add_series({
                    'values': "=Tabellen!$G$4:$H$4",
                    'categories': "=Tabellen!$G$2:$H$2",
                    'name': "=Tabellen!$I$4",
                })
                chart_Branchenstruktur.add_series({
                    'values': "=Tabellen!$G$5:$H$5",
                    'categories': "=Tabellen!$G$2:$H$2",
                    'name': "=Tabellen!$I$5",
                })
                chart_Branchenstruktur.add_series({
                    'values': "=Tabellen!$G$6:$H$6",
                    'categories': "=Tabellen!$G$2:$H$2",
                    'name': "=Tabellen!$I$6",
                })
                chart_Branchenstruktur.add_series({
                    'values': "=Tabellen!$G$7:$H$7",
                    'categories': "=Tabellen!$G$2:$H$2",
                    'name': "=Tabellen!$I$7",
                })
                chart_Branchenstruktur.add_series({
                    'values': "=Tabellen!$G$8:$H$8",
                    'categories': "=Tabellen!$G$2:$H$2",
                    'name': "=Tabellen!$I$8",
                })

                # Chart Beschaeftigte anlegen
                chart_Beschaeftigte = wb.add_chart({'type': 'bar'})
                chart_Beschaeftigte.set_style(40)
                chart_Beschaeftigte.set_size({'width': 529, 'height': 283})
                chart_Beschaeftigte.set_chartarea({'border': {'none': True},'fill': {'none': True}})
                chart_Beschaeftigte.set_title({'name': 'Beschaeftigte nach Branche','name_font':  {'name': 'Calibri', 'size': 12}})
                chart_Beschaeftigte.set_legend({'none': True})

                # Werte in Chartobjekte schreiben
                chart_Beschaeftigte.add_series({
                    'values': "=Tabellen!$G$3:$G$8",
                    'categories': "=Tabellen!$I$3:$I$8",
                })

                # Chart Betriebe anlegen
                chart_Betriebe = wb.add_chart({'type': 'bar'})
                chart_Betriebe.set_style(40)
                chart_Betriebe.set_size({'width': 529, 'height': 283})
                chart_Betriebe.set_chartarea({'border': {'none': True},'fill': {'none': True}})
                chart_Betriebe.set_title({'name': 'Betriebe nach Branche','name_font':  {'name': 'Calibri', 'size': 12}})
                chart_Betriebe.set_legend({'none': True})

                # Werte in Chartobjekte schreiben
                chart_Betriebe.add_series({
                    'values': "=Tabellen!$H$3:$H$8",
                    'categories': "=Tabellen!$I$3:$I$8",
                    'name': "=Tabellen!$I$8",
                })


                # Chart Beschaeftigte kum anlegen
                chart_Besch_kum = wb.add_chart({'type': 'area', 'subtype': 'stacked'})
                chart_Besch_kum.set_style(40)
                chart_Besch_kum.set_size({'width': 529, 'height': 283})
                chart_Besch_kum.set_chartarea({'border': {'none': True},'fill': {'none': True}})
                chart_Besch_kum.set_legend({'position': 'bottom'})
                chart_Besch_kum.set_title({'name': 'Beschaeftigte im Zeitverlauf','name_font':  {'name': 'Calibri', 'size': 12}})

                # Werte in Chartobjekte schreiben
                chart_Besch_kum.add_series({
                    'values': "=Tabellen!$B$13:$AF$13",
                    'categories': "=Tabellen!$B$12:$AF$12",
                    'name': "=Tabellen!$A$13",
                })
                chart_Besch_kum.add_series({
                    'values': "=Tabellen!$B$14:$AF$14",
                    'categories': "=Tabellen!$B$12:$AF$12",
                    'name': "=Tabellen!$A$14",
                })
                chart_Besch_kum.add_series({
                    'values': "=Tabellen!$B$15:$AF$15",
                    'categories': "=Tabellen!$B$12:$AF$12",
                    'name': "=Tabellen!$A$15",
                })
                chart_Besch_kum.add_series({
                    'values': "=Tabellen!$B$16:$AF$16",
                    'categories': "=Tabellen!$B$12:$AF$12",
                    'name': "=Tabellen!$A$16",
                })
                chart_Besch_kum.add_series({
                    'values': "=Tabellen!$B$17:$AF$17",
                    'categories': "=Tabellen!$B$12:$AF$12",
                    'name': "=Tabellen!$A$17",
                })
                chart_Besch_kum.add_series({
                    'values': "=Tabellen!$B$18:$AF$18",
                    'categories': "=Tabellen!$B$12:$AF$12",
                    'name': "=Tabellen!$A$18",
                })




                # Chart Betriebe kum anlegen
                chart_Betriebe_kum = wb.add_chart({'type': 'area', 'subtype': 'stacked'})
                chart_Betriebe_kum.set_style(40)
                chart_Betriebe_kum.set_size({'width': 529, 'height': 283})
                chart_Betriebe_kum.set_chartarea({'border': {'none': True},'fill': {'none': True}})
                chart_Betriebe_kum.set_legend({'position': 'bottom'})
                chart_Betriebe_kum.set_title({'name': 'Betriebe im Zeitverlauf','name_font':  {'name': 'Calibri', 'size': 12}})

                # Werte in Chartobjekte schreiben
                chart_Betriebe_kum.add_series({
                    'values': "=Tabellen!$B$33:$AF$33",
                    'categories': "=Tabellen!$B$32:$AF$32",
                    'name': "=Tabellen!$A$33",
                })
                chart_Betriebe_kum.add_series({
                    'values': "=Tabellen!$B$34:$AF$34",
                    'categories': "=Tabellen!$B$32:$AF$32",
                    'name': "=Tabellen!$A$34",
                })
                chart_Betriebe_kum.add_series({
                    'values': "=Tabellen!$B$35:$AF$35",
                    'categories': "=Tabellen!$B$32:$AF$32",
                    'name': "=Tabellen!$A$35",
                })
                chart_Betriebe_kum.add_series({
                    'values': "=Tabellen!$B$36:$AF$36",
                    'categories': "=Tabellen!$B$32:$AF$32",
                    'name': "=Tabellen!$A$36",
                })
                chart_Betriebe_kum.add_series({
                    'values': "=Tabellen!$B$37:$AF$37",
                    'categories': "=Tabellen!$B$32:$AF$32",
                    'name': "=Tabellen!$A$37",
                })
                chart_Betriebe_kum.add_series({
                    'values': "=Tabellen!$B$38:$AF$38",
                    'categories': "=Tabellen!$B$32:$AF$32",
                    'name': "=Tabellen!$A$38",
                })



                # Charts in Tabelle schreiben
                ws4.insert_chart('A2', chart_Branchenstruktur)
                ws4.insert_chart('A14', chart_Beschaeftigte)
                ws4.insert_chart('A29', chart_Betriebe)
                ws4.insert_chart('A44', chart_Besch_kum)
                ws4.insert_chart('A59', chart_Betriebe_kum)

                ######
                #Gewerbe Beschaeftigte Art der beschaeftigung
                if arcpy.Exists(self.folders.get_table("Gewerbe_Beschaeftigte_Zahlen")):
                    path_beschaeftigte_Zahlen= self.folders.get_table("Gewerbe_Beschaeftigte_Zahlen")
                    datenauslesen=[]
                    for uu in arcpy.SearchCursor(path_beschaeftigte_Zahlen):
                        datenauslesen.append(uu.Anzahl)

                    if len(datenauslesen)==4:
                        #Alles okay mit den Daten - eigentlich quatsch aber absicherung

                        ws4_1.write(2, 1, "Art der Arbeitsplaetze".decode('utf-8'), bold)
                        ws4_1.write(4, 1, "Von den   "+str(datenauslesen[3])+"   Arbeitsplaetzen, die durch die Gewerbeansiedlung entstehen werden, sind vermutlich".decode('utf-8'))
                        ws4_1.write(5, 1, str(datenauslesen[0])+"   Arbeitsplaetze fuer Teilzeitbeschaeftigte,")
                        ws4_1.write(6, 1, str(datenauslesen[1])+"   Arbeitsplaetze fuer geringfuegig entlohnte Beschaeftigte (Minijobber) und")
                        ws4_1.write(7, 1, str(datenauslesen[2])+"   Arbeitsplaetze fuer Beschaeftigte mit einer akademischen Ausbildung (d.h. mit Fach- oder Hochschulabschluss).")

                        del path_beschaeftigte_Zahlen, datenauslesen


                #Workbook speichern
                try:
                    wb.close()
                except:
                    messages.AddMessage("Es liegt ein Fehler beim Speichern der Ausgabedatei vor. Ist diese ggf. noch geoeffnet?")

                schrittmeldung = 'Die Ergebnisausgabe wurde erzeugt. Das Tool wurde erfolgreich angewendet.  \n'
                messages.AddMessage(schrittmeldung)



        #EINZELHANDEL
        projectname = parameters[0].valueAsText
        tabelle_gebaude = self.get_table('Gebaeude_Details')
        Insert = arcpy.InsertCursor(tabelle_gebaude)
        row = Insert.newRow()
        row.Teilflaeche_Plangebiet = parameters[1].valueAsText
        row.Gebaeudetyp = "Einzelhandel"
        Insert.insertRow(row)
        del row, Insert

        #tabelle "Wohneinheiten_Details" oeffnen und Werte fuer Miete_Eigentum, Qualitastsstufe und Anzahl Wohneinheiten speichern
        tabelle_wohneineheiten_details = self.get_table('Wohneinheiten_Details')
        Insert = arcpy.InsertCursor(tabelle_wohneineheiten_details)
        row = Insert.newRow()
        row.Gebaeudetyp = "Einzelhandel"
        row.Wohnflaeche_qm = 0
        row.Teilflaeche_Plangebiet = parameters[1].valueAsText
        row.Miete_Eigentum = 100
        row.Anzahl_WE = 0
        row.Jahr = jahr
        row.EW_je_WE = 0
        Insert.insertRow(row)
        del row, Insert

        #tabelle "Versorgung_Verkaufsflaechen" oeffnen und Werte  speichern
        tabelle_Versorgung_Verkaufsflaechen = self.get_table('Versorgung_Verkaufsflaechen')
        Insert = arcpy.InsertCursor(tabelle_Versorgung_Verkaufsflaechen)
        row = Insert.newRow()
        row.Teilflaeche_Plangebiet = parameters[1].valueAsText
        row.Verkaufsflaeche = parameters[26].valueAsText
        Insert.insertRow(row)
        del row, Insert
        gc.collect()